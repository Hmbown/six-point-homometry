"""Exact six-note parallelogram-dyad certificates and order-six generators.

The complete shape grammar is Theorem D in the dated proof.  This module
recognizes alignments and constructs their nonnegative periodic weights;
it does not claim that all six-note pairs have this shape.
"""
from __future__ import annotations

import argparse
from collections import Counter
from itertools import product
import json
from math import gcd
from pathlib import Path
import time

from six_explore import canon, icv


ROOT = Path(__file__).resolve().parents[1]


def parametric_families(m, a):
    """Theorem H's three purely cyclic pairs in Z_(6m), 0<a<m/2.

    Lists are sorted in this parameter range.  Non-shadow is established by
    stable signed matchings plus exact parametric divisibility certificates,
    rather than by a bounded factor or integer-coordinate search.
    """
    if not isinstance(m, int) or not isinstance(a, int) or not 0 < 2 * a < m:
        raise ValueError("require integer parameters 0 < a < m/2")
    return (
        ((0,a,a+m,2*m,a+3*m,a+4*m), (0,a,a+m,a+2*m,3*m,a+4*m)),
        ((0,a,m,2*m,a+3*m,4*m), (0,a,m,a+2*m,3*m,4*m)),
        ((0,a,m,3*m,a+3*m,5*m), (0,a,m,3*m,4*m,a+4*m)),
    )


def periodic_decomposition(w, a, b):
    """Nonnegative integral U+V, periodic by a/b, or None if no such split.

    Independent of a Fourier transform: construct the complete orbit grid on
    each <a,b>-coset and test its additive cell relations exactly.
    """
    n = len(w)
    if not n or any(not isinstance(x, int) or x < 0 for x in w):
        raise ValueError("expected nonnegative integer coefficients")
    ga, gb = gcd(a, n), gcd(b, n)
    gl = gcd(ga, gb)
    cells = {}
    for x, value in enumerate(w):
        key = x % ga, x % gb
        if key in cells and cells[key] != value:
            return None
        cells[key] = value
    ua, vb = [0] * ga, [0] * gb
    for r in range(gl):
        ia, jb = list(range(r, ga, gl)), list(range(r, gb, gl))
        i0, j0 = ia[0], jb[0]
        minimum = min(cells[i, j0] for i in ia)
        for i in ia:
            ua[i] = cells[i, j0] - minimum
        for j in jb:
            vb[j] = cells[i0, j] - cells[i0, j0] + minimum
        if any(ua[i] + vb[j] != cells[i, j] or vb[j] < 0 for i in ia for j in jb):
            return None
    u, v = tuple(ua[x % ga] for x in range(n)), tuple(vb[x % gb] for x in range(n))
    assert all(u[x] + v[x] == w[x] for x in range(n))
    assert all(u[x] == u[(x + a) % n] and v[x] == v[(x + b) % n] for x in range(n))
    return u, v


def recover_common(w, a, b):
    """Generate every binary C allowed by the reflection/coefficient conditions."""
    n = len(w)
    corners = {0, a % n, b % n, (a + b) % n}
    if len(corners) != 4 or sum(w) != 12 or any(w[x] != 1 for x in corners):
        return
    options = []
    seen = set(corners)
    for x in range(n):
        if x in seen:
            continue
        y = (a + b - x) % n
        if w[x] != w[y] or w[x] not in (0, 1, 2):
            return
        seen.update((x, y))
        if x == y:
            if w[x] == 1:
                return
            options.append(((),) if w[x] == 0 else ((x,),))
        elif w[x] == 0:
            options.append(((),))
        elif w[x] == 1:
            options.append(((x,), (y,)))
        else:
            options.append(((x, y),))
    for choices in product(*options):
        c = tuple(sorted(x for choice in choices for x in choice))
        assert len(c) == len(set(c)) == 4
        yield c


def shape_certificate(a_set, b_set, n):
    """Try every rigid alignment of B to A and return an exact dyad certificate."""
    aset = set(a_set)
    if len(aset) != 6 or len(set(b_set)) != 6:
        raise ValueError("expected six-subsets")
    for sign in (1, -1):
        for shift in range(n):
            bimage = {(sign * x + shift) % n for x in b_set}
            c = aset & bimage
            if len(c) != 4:
                continue
            xx, yy = sorted(aset - c), sorted(bimage - c)
            if (sum(xx) - sum(yy)) % n:
                continue
            anchor = xx[0]
            a, b = tuple((y - anchor) % n for y in yy)
            common = tuple(sorted((x - anchor) % n for x in c))
            w = [0] * n
            for x in common:
                w[x] += 1
                w[(a + b - x) % n] += 1
            for x in (0, a, b, (a + b) % n):
                w[x] += 1
            split = periodic_decomposition(w, a, b)
            if split is None:
                continue
            u, v = split
            assert common in set(recover_common(w, a, b))
            raw_a, raw_b = tuple(sorted(common + (0, (a + b) % n))), tuple(sorted(common + (a, b)))
            assert canon(raw_a, n) == canon(a_set, n) and canon(raw_b, n) == canon(b_set, n)
            assert icv(raw_a, n) == icv(raw_b, n)
            return dict(a=a, b=b, common=common, order_a=n // gcd(a, n), order_b=n // gcd(b, n),
                        w=w, u=u, v=v, raw_a=raw_a, raw_b=raw_b,
                        b_alignment=dict(sign=sign, shift=shift), a_anchor=anchor)
    return None


def h6_edges(n):
    """Exact h=6 reflection-shell generator, with parameters kept per T/I edge."""
    if n % 6:
        return {}
    result = {}
    for b in range(1, n):
        if n // gcd(b, n) != 6:
            continue
        h = {(j * b) % n for j in range(6)}
        for a in range(n):
            if a in h:
                continue
            support = h | {(a + x) % n for x in h}
            w = tuple(int(x in support) for x in range(n))
            for c in recover_common(w, a, b):
                x, y = canon(c + (0, (a + b) % n), n), canon(c + (a, b), n)
                if x == y:
                    continue
                assert len(x) == len(y) == 6 and icv(x, n) == icv(y, n)
                result.setdefault(tuple(sorted((x, y))), dict(a=a, b=b, common=c))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nmin", type=int, default=12)
    parser.add_argument("--nmax", type=int, default=60)
    parser.add_argument("--out", type=Path, default=ROOT / "results/2026-09-30-six-shell")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for n in range(args.nmin, args.nmax + 1):
        dest = args.out / f"n{n}.json"
        if args.resume and dest.exists():
            continue
        start = time.monotonic()
        families = json.loads((ROOT / f"results/2026-09-30-six-inventory/n{n}.json").read_text())["families"]
        h6 = h6_edges(n)
        rows, counts = [], Counter()
        for family in families:
            # Classification by the new shape is exact on each pair; menu
            # connectivity counts are inherited single-pass labels only.
            members = [tuple(a) for a in family["members"]]
            from itertools import combinations
            for x, y in combinations(members, 2):
                cert = shape_certificate(x, y, n)
                if cert:
                    gap = family["combined_components"] > 1
                    counts["shape_pairs"] += 1
                    counts["gap_shape_pairs"] += gap
                    counts["h6_pairs"] += (x, y) in h6
                    counts["gap_h6_pairs"] += gap and (x, y) in h6
                    rows.append(dict(x=x, y=y, shape=cert, h6=h6.get((x, y)), menu_gap=gap))
        payload = dict(n=n, summary=dict(counts), pairs=rows,
                       status="COMPUTED-UNVALIDATED coverage until independent certificate audit",
                       seconds=round(time.monotonic() - start, 3))
        temp = dest.with_suffix(".tmp")
        temp.write_text(json.dumps(payload, sort_keys=True) + "\n")
        temp.replace(dest)
        print(n, dict(counts), payload["seconds"], flush=True)


if __name__ == "__main__":
    main()
