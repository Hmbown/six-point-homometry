"""Cardinality-six census, independent point/bitset method versus the C gap method.

No all-cardinality enumeration. The point method considers every anchored
six-subset and its twelve anchored rigid images. Signatures use exact directed
bit correlations (the antipodal entry is halved). Supports 6 <= n <= 63.
Run with the pinned interpreter; JSON files are per-n resumable checkpoints.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
from math import comb
from pathlib import Path
import time

import numpy as np
from numba import njit

ROOT = Path(__file__).resolve().parents[1]


@njit(cache=True)
def _popcount(x):
    total = 0
    while x:
        x &= x - np.uint64(1)
        total += 1
    return total


@njit(cache=True)
def _points(n):
    rows = []
    full = (np.uint64(1) << np.uint64(n)) - np.uint64(1)
    for a in range(1, n - 4):
        for b in range(a + 1, n - 3):
            for c in range(b + 1, n - 2):
                for d in range(c + 1, n - 1):
                    for e in range(d + 1, n):
                        s = (0, a, b, c, d, e)
                        mask = np.uint64(0)
                        for p in s:
                            mask |= np.uint64(1) << np.uint64(p)
                        keep = True
                        for anchor in s:
                            for sign in (1, -1):
                                other = np.uint64(0)
                                for p in s:
                                    other |= np.uint64(1) << np.uint64((sign * (p - anchor)) % n)
                                diff = mask ^ other
                                if diff:
                                    first = diff & (np.uint64(0) - diff)
                                    if other & first:
                                        keep = False
                                        break
                            if not keep:
                                break
                        if not keep:
                            continue
                        lo, hi = np.uint64(0), np.uint64(0)
                        for distance in range(1, n // 2 + 1):
                            shifted = ((mask << np.uint64(distance)) |
                                       (mask >> np.uint64(n - distance))) & full
                            count = _popcount(mask & shifted)
                            if 2 * distance == n:
                                count //= 2
                            if distance <= 16:
                                lo |= np.uint64(count) << np.uint64(4 * (distance - 1))
                            else:
                                hi |= np.uint64(count) << np.uint64(4 * (distance - 17))
                        rows.append((mask, lo, hi))
    return rows


def mask_tuple(mask):
    return tuple(i for i in range(mask.bit_length()) if (mask >> i) & 1)


def point_census(n):
    if not 6 <= n <= 63:
        raise ValueError("point method supports 6 <= n <= 63")
    buckets = {}
    rows = _points(n)
    for mask, lo, hi in rows:
        buckets.setdefault((int(lo), int(hi)), []).append(mask_tuple(int(mask)))
    families = {}
    for (lo, hi), members in buckets.items():
        if len(members) < 2:
            continue
        vector = tuple(((lo if d < 16 else hi) >> (4 * (d % 16))) & 15
                       for d in range(n // 2))
        families[vector] = sorted(members)
    return families, len(rows)


def gap_census(n):
    # Independent C enumerator: positive cyclic gaps, with a different symmetry
    # traversal and unordered pair-distance kernel. Restrict the caller to k=6.
    from fastcensus import z_families_fast
    return {v: sorted(m) for v, m in z_families_fast(n, sizes=[6]).items()}


def inherited_families(n):
    path = ROOT / "results" / "fastcensus" / f"families_n{n}.txt.gz"
    if not path.exists():
        return None
    families = []
    with gzip.open(path, "rt") as stream:
        for line in stream:
            k, masks = line.rstrip().split("\t")
            if int(k) == 6:
                families.append(sorted(mask_tuple(int(mask, 16)) for mask in masks.split()))
    return sorted(families)


def serialize(families):
    return [{"icv": list(v), "members": [list(a) for a in sorted(m)]}
            for v, m in sorted(families.items())]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nmin", type=int, default=12)
    parser.add_argument("--nmax", type=int, default=32)
    parser.add_argument("--reference-max", type=int, default=18)
    parser.add_argument("--out", type=Path, default=ROOT / "results/2026-09-30-six-census")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--compare-inherited", action="store_true")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    summaries = []
    for n in range(args.nmin, args.nmax + 1):
        path = args.out / f"n{n}.json"
        if args.resume and path.exists():
            old = json.loads(path.read_text())
            if old.get("methods") != ["anchored-points-bitcorrelation", "C-positive-gaps-pairdistances"]:
                raise ValueError(f"unverified checkpoint: {path}")
            summaries.append(old["summary"])
            print(f"n={n} resumed verified checkpoint", flush=True)
            continue
        print(f"n={n} start anchored candidates={comb(n - 1, 5)}", flush=True)
        start = time.monotonic()
        points, classes = point_census(n)
        seconds_points = time.monotonic() - start
        start = time.monotonic()
        gaps = gap_census(n)
        seconds_gaps = time.monotonic() - start
        if points != gaps:
            raise AssertionError(f"independent methods disagree at n={n}")
        checked_reference = n <= args.reference_max
        if checked_reference:
            from homometry import z_families
            assert points == {v: sorted(m) for v, m in z_families(n, sizes=[6]).items()}, n
        inherited = None
        if args.compare_inherited:
            inherited = inherited_families(n)
            if inherited is not None:
                assert sorted(points.values()) == inherited, n
        payload = serialize(points)
        summary = dict(n=n, classes=classes, families=len(points),
                       pairs=sum(len(m) * (len(m) - 1) // 2 for m in points.values()),
                       largest=max(map(len, points.values()), default=0),
                       seconds_points=round(seconds_points, 3), seconds_gaps=round(seconds_gaps, 3),
                       reference=checked_reference, inherited=inherited is not None)
        result = {"status": "COMPUTED", "methods": ["anchored-points-bitcorrelation", "C-positive-gaps-pairdistances"],
                  "summary": summary, "families": payload,
                  "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
        temp = path.with_suffix(".tmp")
        temp.write_text(json.dumps(result, sort_keys=True) + "\n")
        temp.replace(path)
        summaries.append(summary)
        print(json.dumps(summary), flush=True)
    with (args.out / "summary.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(summaries[0]))
        writer.writeheader()
        writer.writerows(summaries)


if __name__ == "__main__":
    main()
