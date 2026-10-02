"""
fastmoves.py -- numba bitset versions of the three implemented mechanisms in
src/homometry.py (Babbitt complement, 0/1 direct-sum flip, complement-of-flip)
and of explain_family.  Semantics replicate homometry.mechanism_edges exactly:

  direct_sum_flips(S):  for every t in S translate S so t -> 0; for every
     proper divisor d of k (2 <= d < k), m = k/d, every B = {0} + (d-1) other
     elements of S, every C = {0} + (m-1) other elements of S with
     B + C = S and all |B||C| sums distinct, emit canon(B - C) if |B - C| = k.
     (Implementation: given B, the admissible C are exactly the sets of
     translates c in S, 0 in C, with c + B subset of S, pairwise disjoint, m of
     them -- disjoint union of m translates of a d-set has k elements and lies
     in S, so it equals S.  This is the same set of (B, C) pairs the reference
     loops over.)
  edge(A, B), |A| = k:
     babbitt-complement   2k == n and canon(A^c) == B
     direct-sum-flip      B in flips(A) or A in flips(B)
     complement-of-flip   2k != n and (canon(B^c) in flips(canon(A^c)) or vice versa)
  a family is explained iff its members are connected by edges.

Bit convention: bit i <-> element i; canonical = lexicographically smallest
sorted tuple in the dihedral orbit (see fastcensus.c header).
"""
from __future__ import annotations

import numpy as np
from numba import njit, prange

U = np.uint64
MAXF = 4096  # max flips stored per set (checked)


@njit(inline="always")
def _rotr(x, t, n, mask):
    t = t % n
    if t == 0:
        return x
    return ((x >> np.uint64(t)) | (x << np.uint64(n - t))) & mask


@njit(inline="always")
def _lexless(a, b):
    d = a ^ b
    if d == 0:
        return False
    low = d & (~d + np.uint64(1))
    return (a & low) != 0


@njit
def _rev(x, n):
    r = np.uint64(0)
    for i in range(n):
        if (x >> np.uint64(i)) & np.uint64(1):
            r |= np.uint64(1) << np.uint64(n - 1 - i)
    return r


@njit
def _popcount(x):
    c = 0
    while x:
        x &= x - np.uint64(1)
        c += 1
    return c


@njit
def _ctz(x):
    c = 0
    while (x & np.uint64(1)) == 0:
        x >>= np.uint64(1)
        c += 1
    return c


@njit
def canon(x, n):
    mask = (np.uint64(1) << np.uint64(n)) - np.uint64(1)
    best = np.uint64(0)
    first = True
    y = x
    while y:
        t = _ctz(y)
        y &= y - np.uint64(1)
        z = _rotr(x, t, n, mask)
        if first or _lexless(z, best):
            best = z
            first = False
    r = _rev(x, n)
    y = r
    while y:
        t = _ctz(y)
        y &= y - np.uint64(1)
        z = _rotr(r, t, n, mask)
        if _lexless(z, best):
            best = z
    return best


@njit
def _add(out, cnt, v):
    for i in range(cnt):
        if out[i] == v:
            return cnt
    if cnt >= out.shape[0]:
        raise ValueError("flip buffer overflow")
    out[cnt] = v
    return cnt + 1


@njit
def _tile(S, B, n, mask, T, nT, start, need, union, Cset, out, cnt, k):
    """choose `need` more translates c from T[start:] (disjoint from union)."""
    if need == 0:
        # all translates chosen; flip = union over c of (B - c)
        flip = np.uint64(0)
        y = Cset
        while y:
            c = _ctz(y)
            y &= y - np.uint64(1)
            flip |= _rotr(B, c, n, mask)
        if _popcount(flip) == k:
            cnt = _add(out, cnt, canon(flip, n))
        return cnt
    for i in range(start, nT - need + 1):
        c = T[i]
        Bc = _rotr(B, (n - c) % n, n, mask)  # B + c
        if (Bc & union) == 0:
            cnt = _tile(S, B, n, mask, T, nT, i + 1, need - 1, union | Bc,
                        Cset | (np.uint64(1) << np.uint64(c)), out, cnt, k)
    return cnt


@njit
def _cover(S, B, n, mask, union, Cset, out, cnt, k):
    """exact cover of S by disjoint translates B + c (lowest-uncovered-element
    branching; each tiling found exactly once)."""
    if union == S:
        flip = np.uint64(0)
        y = Cset
        while y:
            c = _ctz(y)
            y &= y - np.uint64(1)
            flip |= _rotr(B, c, n, mask)  # B - c
        if _popcount(flip) == k:
            cnt = _add(out, cnt, canon(flip, n))
        return cnt
    s = _ctz(S & ~union)
    yb = B
    while yb:
        b = _ctz(yb)
        yb &= yb - np.uint64(1)
        c = (s - b) % n
        Bc = _rotr(B, (n - c) % n, n, mask)  # B + c
        if (Bc & ~S) == 0 and (Bc & union) == 0:
            cnt = _cover(S, B, n, mask, union | Bc, Cset | (np.uint64(1) << np.uint64(c)), out, cnt, k)
    return cnt


@njit
def _flips_into(x, n, out):
    """Fast version (same output set as the literal loop below / reference):
    (1) only one translate t (the lowest element) is needed: if S - t = B (+) C
        with 0 in B, C, then S = (B+t) (+) C, and for any other t0 in S,
        t0 = b0 + c0 uniquely, giving S - t0 = (B+t-b0) (+) (C-c0) whose flip
        is a translate of B - C;
    (2) only |B| = d <= m = k/d is needed: (C, B) is also a solution and
        C - B = -(B - C) has the same dihedral canonical form;
    (3) C is found by exact cover instead of combinations.
    Equality with the reference is tested in tests/test_fastcensus.py."""
    mask = (np.uint64(1) << np.uint64(n)) - np.uint64(1)
    k = _popcount(x)
    cnt = 0
    oth = np.empty(64, np.int64)
    idx = np.empty(64, np.int64)
    S = _rotr(x, _ctz(x), n, mask)  # contains 0
    no = 0
    y = S & (mask - np.uint64(1))
    while y:
        e = _ctz(y)
        y &= y - np.uint64(1)
        oth[no] = e
        no += 1
    for d in range(2, k):
        if k % d != 0 or d * d > k:
            continue
        r = d - 1
        for i in range(r):
            idx[i] = i
        while True:
            B = np.uint64(1)
            for i in range(r):
                B |= np.uint64(1) << np.uint64(oth[idx[i]])
            cnt = _cover(S, B, n, mask, B, np.uint64(1), out, cnt, k)
            j = r - 1
            while j >= 0 and idx[j] == no - r + j:
                j -= 1
            if j < 0:
                break
            idx[j] += 1
            for i in range(j + 1, r):
                idx[i] = idx[i - 1] + 1
    return cnt


@njit
def _flips_into_literal(x, n, out):
    """Literal transcription of homometry.direct_sum_flips (all translates,
    all divisors, combination search). Kept for cross-checking."""
    mask = (np.uint64(1) << np.uint64(n)) - np.uint64(1)
    k = _popcount(x)
    cnt = 0
    T = np.empty(64, np.int64)
    oth = np.empty(64, np.int64)
    idx = np.empty(64, np.int64)
    y0 = x
    while y0:
        t = _ctz(y0)
        y0 &= y0 - np.uint64(1)
        S = _rotr(x, t, n, mask)  # contains 0
        no = 0
        y = S & (mask - np.uint64(1))
        while y:
            e = _ctz(y)
            y &= y - np.uint64(1)
            oth[no] = e
            no += 1
        for d in range(2, k):
            if k % d != 0:
                continue
            m = k // d
            r = d - 1  # choose r of oth
            for i in range(r):
                idx[i] = i
            while True:
                B = np.uint64(1)
                for i in range(r):
                    B |= np.uint64(1) << np.uint64(oth[idx[i]])
                # admissible translates c in S\{0} with B + c subset of S
                nT = 0
                yy = S & (mask - np.uint64(1))
                while yy:
                    c = _ctz(yy)
                    yy &= yy - np.uint64(1)
                    Bc = _rotr(B, (n - c) % n, n, mask)
                    if (Bc & ~S) == 0 and (Bc & B) == 0:
                        T[nT] = c
                        nT += 1
                if nT >= m - 1:
                    cnt = _tile(S, B, n, mask, T, nT, 0, m - 1, B, np.uint64(1), out, cnt, k)
                # next combination
                j = r - 1
                while j >= 0 and idx[j] == no - r + j:
                    j -= 1
                if j < 0:
                    break
                idx[j] += 1
                for i in range(j + 1, r):
                    idx[i] = idx[i - 1] + 1
    return cnt


@njit
def flips(x, n):
    out = np.empty(MAXF, np.uint64)
    c = _flips_into(x, n, out)
    return out[:c].copy()


@njit
def flips_literal(x, n):
    out = np.empty(MAXF, np.uint64)
    c = _flips_into_literal(x, n, out)
    return out[:c].copy()


@njit
def _contains(arr, cnt, v):
    for i in range(cnt):
        if arr[i] == v:
            return True
    return False


@njit
def _find(p, x):
    while p[x] != x:
        p[x] = p[p[x]]
        x = p[x]
    return x


@njit(parallel=True)
def explain_families(masks, offsets, n):
    """masks: flat uint64 array of canonical members; family f = masks[offsets[f]:offsets[f+1]].
    Returns int64 array of component counts per family (1 == explained)."""
    nf = offsets.shape[0] - 1
    comps = np.zeros(nf, np.int64)
    mask = (np.uint64(1) << np.uint64(n)) - np.uint64(1)
    for f in prange(nf):
        a0 = offsets[f]
        sz = offsets[f + 1] - a0
        k = _popcount(masks[a0])
        F = np.empty((sz, MAXF), np.uint64)
        nF = np.zeros(sz, np.int64)
        FC = np.empty((sz, MAXF), np.uint64)
        nFC = np.zeros(sz, np.int64)
        cm = np.empty(sz, np.uint64)
        for i in range(sz):
            nF[i] = _flips_into(masks[a0 + i], n, F[i])
            cm[i] = canon((~masks[a0 + i]) & mask, n)
            if 2 * k != n:
                nFC[i] = _flips_into(cm[i], n, FC[i])
        par = np.arange(sz)
        for i in range(sz):
            A = masks[a0 + i]
            for j in range(i + 1, sz):
                B = masks[a0 + j]
                e = False
                if 2 * k == n and cm[i] == B:
                    e = True
                if not e and (_contains(F[i], nF[i], B) or _contains(F[j], nF[j], A)):
                    e = True
                if not e and 2 * k != n and (_contains(FC[i], nFC[i], cm[j]) or _contains(FC[j], nFC[j], cm[i])):
                    e = True
                if e:
                    ri = _find(par, i)
                    rj = _find(par, j)
                    par[ri] = rj
        c = 0
        for i in range(sz):
            if _find(par, i) == i:
                c += 1
        comps[f] = c
    return comps


# ------------------------------------------------------------ python glue
def to_mask(s) -> int:
    m = 0
    for x in s:
        m |= 1 << x
    return m


def to_tuple(m: int) -> tuple:
    return tuple(i for i in range(64) if (m >> i) & 1)


def direct_sum_flips_fast(s, n, literal=False) -> set:
    """Same as homometry.direct_sum_flips (returns set of canonical tuples)."""
    f = flips_literal if literal else flips
    return {to_tuple(int(v)) for v in f(np.uint64(to_mask(s)), n)}


def explain_many(families, n):
    """families: list of lists of canonical tuples (or int masks).
    Returns list of component counts (1 == explained)."""
    import random
    order = list(range(len(families)))
    random.Random(12345).shuffle(order)  # load balance across prange threads
    families = [families[i] for i in order]
    flat, offs = [], [0]
    for fam in families:
        for m in fam:
            flat.append(m if isinstance(m, int) else to_mask(m))
        offs.append(len(flat))
    if not families:
        return []
    comps = explain_families(np.array(flat, dtype=np.uint64), np.array(offs, dtype=np.int64), n)
    out = [0] * len(order)
    for pos, i in enumerate(order):
        out[i] = int(comps[pos])
    return out


# ------------------------------------------------------------ coverage CLI
def _load_families(path):
    import gzip
    fams = []
    with gzip.open(path, "rt") as f:
        for line in f:
            kk, rest = line.rstrip("\n").split("\t")
            fams.append([int(h, 16) for h in rest.split()])
    return fams


def coverage_n(n, famdir, outdir, chunk=200000):
    """Unexplained-family count for n from the stored fast-census family file."""
    import gzip, json, os, time
    from collections import Counter
    t0 = time.time()
    fams = _load_families(os.path.join(famdir, f"families_n{n}.txt.gz"))
    comps = []
    for i in range(0, len(fams), chunk):
        comps += explain_many(fams[i:i + chunk], n)
    unexpl = [f for f, c in zip(fams, comps) if c != 1]
    by_card = Counter(bin(f[0]).count("1") for f in unexpl)
    by_size = Counter(len(f) for f in unexpl)
    row = {"n": n, "z_families": len(fams), "unexplained_families": len(unexpl),
           "unexplained_by_cardinality": {str(k): by_card[k] for k in sorted(by_card)},
           "unexplained_by_family_size": {str(k): by_size[k] for k in sorted(by_size)},
           "components_histogram": {str(k): v for k, v in sorted(Counter(int(c) for c in comps).items())},
           "seconds": round(time.time() - t0, 1)}
    os.makedirs(outdir, exist_ok=True)
    with gzip.open(os.path.join(outdir, f"unexplained_n{n}.txt.gz"), "wt") as f:
        for fam in unexpl:
            f.write(f"{bin(fam[0]).count('1')}\t" + " ".join(f"{m:x}" for m in fam) + "\n")
    with open(os.path.join(outdir, f"coverage_n{n}.json"), "w") as f:
        json.dump(row, f)
    return row


if __name__ == "__main__":
    import argparse, json, os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=17)
    ap.add_argument("--nmax", type=int, default=20)
    ap.add_argument("--famdir", default=os.path.join(root, "results", "fastcensus"))
    ap.add_argument("--outdir", default=os.path.join(root, "results", "fastcensus"))
    a = ap.parse_args()
    for n in range(a.nmin, a.nmax + 1):
        if os.path.exists(os.path.join(a.outdir, f"coverage_n{n}.json")):
            print(f"n={n}: done already"); continue
        print(json.dumps(coverage_n(n, a.famdir, a.outdir)), flush=True)
