"""
fastcensus.py -- driver for the C bitset Z-family enumerator (src/fastcensus.c).

Validated against the reference src/homometry.z_families (tests/test_fastcensus.py).

Python API
----------
    build()                      -> path to compiled binary (recompiles if stale)
    z_families_fast(n, sizes=None, direct=False)
        -> {ICV tuple: [canonical tuples...]}, same content as
           homometry.z_families(n, sizes) (members sorted lexicographically).
           direct=False: k > n/2 families are derived from k' = n-k by
           complementation inside the C code (see the proof in fastcensus.c
           header; this is also covered by the tests, which compare against the
           reference that enumerates every k directly).

CLI (census with checkpoints)
-----------------------------
    python3 src/fastcensus.py --nmin 8 --nmax 32 [--store-max 30] [--threads 14]
        writes   results/fastcensus/summary_n{n}.json   (checkpoint per n)
                 results/fastcensus/families_n{n}.txt.gz (if n <= store-max)
                 results/census_fast_8_{nmax}.csv
    Family file format: one family per line "k<TAB>hex hex ..." where each hex
    word is a bitmask (bit i <-> pitch class i) of a canonical representative.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import json
import os
import subprocess
import sys
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, "fastcensus.c")
BIN = os.path.join(ROOT, "build", "fastcensus")


def build(force: bool = False) -> str:
    os.makedirs(os.path.dirname(BIN), exist_ok=True)
    if force or not os.path.exists(BIN) or os.path.getmtime(BIN) < os.path.getmtime(SRC):
        cmd = ["cc", "-O3", "-march=native", "-o", BIN, SRC, "-lpthread"]
        subprocess.run(cmd, check=True)
    return BIN


def mask_to_tuple(m: int) -> tuple:
    out, i = [], 0
    while m:
        if m & 1:
            out.append(i)
        m >>= 1
        i += 1
    return tuple(out)


def tuple_to_mask(s) -> int:
    m = 0
    for x in s:
        m |= 1 << x
    return m


def icv_mask(m: int, n: int) -> tuple:
    full = (1 << n) - 1
    v = []
    for d in range(1, n // 2 + 1):
        r = ((m >> d) | (m << (n - d))) & full
        c = bin(m & r).count("1")
        if 2 * d == n:
            c //= 2
        v.append(c)
    return tuple(v)


def run_k_raw(n: int, k: int, comp: bool = True, threads: int = 14, passes: int = 1):
    """Yield raw output lines 'k\thex hex ...' of one C run."""
    b = build()
    cmd = [b, str(n), str(k), "-t", str(threads), "-P", str(passes)]
    if comp:
        cmd.append("-c")
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1 << 20)
    for line in p.stdout:
        yield line
    err = p.stderr.read()
    if p.wait() != 0:
        raise RuntimeError(f"fastcensus failed n={n} k={k}: {err}")
    sys.stderr.write("    [c] " + err)


def run_k(n: int, k: int, comp: bool = True, threads: int = 14, passes: int = 1):
    """Yield (k, [masks]) for every family found by one C run."""
    b = build()
    cmd = [b, str(n), str(k), "-t", str(threads), "-P", str(passes)]
    if comp:
        cmd.append("-c")
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1 << 20)
    for line in p.stdout:
        kk, rest = line.rstrip("\n").split("\t")
        yield int(kk), [int(h, 16) for h in rest.split()]
    err = p.stderr.read()
    if p.wait() != 0:
        raise RuntimeError(f"fastcensus failed n={n} k={k}: {err}")


def _plan(n: int, sizes, direct: bool):
    """list of (k, comp) C runs covering `sizes`."""
    ks = sorted(set(sizes))
    runs, covered = [], set()
    for k in ks:
        if k in covered:
            continue
        if direct or 2 * k <= n:
            comp = (not direct) and 2 * k < n and (n - k) in ks
            runs.append((k, comp))
            covered.add(k)
            if comp:
                covered.add(n - k)
        else:
            kk = n - k
            if kk in covered:
                continue
            runs.append((kk, True))
            covered.update({kk, k})
    return runs


def z_families_fast(n: int, sizes=None, direct: bool = False, threads: int = 14):
    if sizes is None:
        sizes = range(2, n - 1)
    sizes = [k for k in sizes if 2 <= k <= n - 2]
    want = set(sizes)
    fam = {}
    for k, comp in _plan(n, sizes, direct):
        for kk, masks in run_k(n, k, comp=comp, threads=threads):
            if kk not in want:
                continue
            mem = [mask_to_tuple(m) for m in masks]
            fam[icv_mask(masks[0], n)] = sorted(mem)
    return fam


# ------------------------------------------------------------------ census
def census_n(n: int, outdir: str, store: bool, threads: int = 14, passes: int = 1) -> dict:
    t0 = time.time()
    by_card: Counter = Counter()
    hist: Counter = Counter()
    nfam = 0
    fh = gzip.open(os.path.join(outdir, f"families_n{n}.txt.gz.part"), "wt", compresslevel=6) if store else None
    for k in range(2, n // 2 + 1):
        tk = time.time()
        cnt_k = 0
        for line in run_k_raw(n, k, comp=True, threads=threads, passes=passes):
            tab = line.index("\t")
            by_card[int(line[:tab])] += 1
            hist[line.count(" ", tab) + 1] += 1
            nfam += 1
            cnt_k += 1
            if fh:
                fh.write(line)
        print(f"  n={n} k={k} (+{n-k}) families={cnt_k} {time.time()-tk:.1f}s", flush=True)
    if fh:
        fh.close()
        os.replace(os.path.join(outdir, f"families_n{n}.txt.gz.part"), os.path.join(outdir, f"families_n{n}.txt.gz"))
    row = {
        "n": n,
        "z_families": nfam,
        "max_family": max(hist, default=0),
        "families_by_cardinality": {str(k): by_card[k] for k in sorted(by_card)},
        "family_size_histogram": {str(s): hist[s] for s in sorted(hist)},
        "seconds": round(time.time() - t0, 2),
        "families_file": f"families_n{n}.txt.gz" if store else None,
    }
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=8)
    ap.add_argument("--nmax", type=int, default=28)
    ap.add_argument("--store-max", type=int, default=30, help="store family lists for n <= this")
    ap.add_argument("--threads", type=int, default=14)
    ap.add_argument("--passes", type=int, default=0, help="0 = auto (bounded memory)")
    ap.add_argument("--outdir", default=os.path.join(ROOT, "results", "fastcensus"))
    ap.add_argument("--csv", default=None)
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    build()
    for n in range(a.nmin, a.nmax + 1):
        ck = os.path.join(a.outdir, f"summary_n{n}.json")
        if os.path.exists(ck):
            print(f"n={n}: checkpoint exists, skipping", flush=True)
            continue
        passes = a.passes or (1 if n <= 36 else 2 if n <= 38 else 8 if n <= 40 else 32)
        row = census_n(n, a.outdir, store=n <= a.store_max, threads=a.threads, passes=passes)
        with open(ck + ".part", "w") as f:
            json.dump(row, f)
        os.replace(ck + ".part", ck)
        print(json.dumps(row), flush=True)
    # CSV over every n that has a checkpoint in [8, nmax]
    rows = []
    for n in range(8, a.nmax + 1):
        ck = os.path.join(a.outdir, f"summary_n{n}.json")
        if os.path.exists(ck):
            rows.append(json.load(open(ck)))
    out_csv = a.csv or os.path.join(ROOT, "results", f"census_fast_8_{a.nmax}.csv")
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["n", "z_families", "max_family", "families_by_cardinality", "family_size_histogram", "seconds"])
        for r in rows:
            w.writerow([r["n"], r["z_families"], r["max_family"],
                        json.dumps(r["families_by_cardinality"]), json.dumps(r["family_size_histogram"]), r["seconds"]])
    print("wrote", out_csv)


if __name__ == "__main__":
    main()
