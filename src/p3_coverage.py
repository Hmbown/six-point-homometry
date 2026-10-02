"""
p3_coverage.py -- fast (numba, bitset) coverage of ALL stored Z-families by the
move grammar of notes/p2_moves.md (workstream P3).

Tiers (a family is "connected" at a tier if the graph on its members whose
edges are single moves of that tier is connected):

  old          : Babbitt complement (k = n/2), 0/1 direct-sum flip, and the
                 complement-conjugated direct-sum flip ("compflip")
  strict       : old + L2 translate, L3 swap, L4 halfturn, L5 reflect, L6 unit,
                 L7 halfcoset, L8 signflip, L9 coset-flat (strict criterion).
                 L0 (inflation) is implicit: every lemma above is a group-ring
                 identity, and identities in Z[Z_d] map under x -> x^m into
                 Z[Z_dm], so moves of an inflated set are found directly.
                 EXCLUDED: L1 block-exact and L9' coset-exact (iff-criteria).
  strict+L10   : strict + L10 3-term Cayley unit (reported separately because it
                 is nearly universal at prime n; see notes/p2_moves_review.md).
  (+ P3 moves) : with --p3, the new moves of src/p3_moves.py are added as a
                 further tier "strict+P3" and "strict+P3+L10".

Cardinalities k > n/2: moves are computed directly only when --direct-large is
given; by default a k > n/2 family is scored by its complement family (the
complement-conjugation meta-move C o M o C, Lemma P3.0 in notes/p3_moves.md).

Every partner produced here is re-checked by ICV comparison inside the kernel
("soundness violations", must be 0).  The fast kernels are cross-checked against
src/moves.py (the P2 reference implementation of the same lemmas) by
tests/test_p3_moves.py.

usage:
  python3 src/p3_coverage.py --nmin 8 --nmax 20 --jobs 6
      writes results/p3_coverage_8_{nmax}.csv, results/p3_unexplained_n{n}.txt,
             results/p3_coverage/summary_n{n}.json
"""
from __future__ import annotations

import argparse
import csv
import gzip
import json
import os
import sys
import time
from collections import Counter, defaultdict
from itertools import combinations
from math import gcd

import numpy as np
from numba import njit

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from fastmoves import _flips_into, MAXF  # noqa: E402

MOVE_NAMES = ["babbitt", "dsflip", "compflip", "translate", "swap", "halfturn",
              "reflect", "unit", "halfcoset", "signflip", "coset-flat", "cayley"]
MID = {m: i for i, m in enumerate(MOVE_NAMES)}
OLD = ["babbitt", "dsflip", "compflip"]
STRICT = OLD + ["translate", "swap", "halfturn", "reflect", "unit", "halfcoset",
                "signflip", "coset-flat"]
L10 = ["cayley"]


def bits(names):
    b = 0
    for m in names:
        b |= 1 << MID[m]
    return b


# ===================================================================== bit utils
@njit(cache=True, inline="always")
def popc(x):
    c = 0
    while x:
        x &= x - np.uint64(1)
        c += 1
    return c


@njit(cache=True, inline="always")
def ctz(x):
    c = 0
    while (x & np.uint64(1)) == 0:
        x >>= np.uint64(1)
        c += 1
    return c


@njit(cache=True)
def addc(x, s, n):
    """x + s (element i -> i + s mod n)."""
    s = s % n
    if s == 0:
        return x
    mask = (np.uint64(1) << np.uint64(n)) - np.uint64(1)
    return ((x << np.uint64(s)) | (x >> np.uint64(n - s))) & mask


@njit(cache=True)
def negm(x, n):
    """-x (element i -> -i mod n)."""
    r = np.uint64(0)
    y = x
    while y:
        i = ctz(y)
        y &= y - np.uint64(1)
        r |= np.uint64(1) << np.uint64((n - i) % n)
    return r


@njit(cache=True)
def mulm(x, u, n):
    r = np.uint64(0)
    y = x
    while y:
        i = ctz(y)
        y &= y - np.uint64(1)
        r |= np.uint64(1) << np.uint64((u * i) % n)
    return r


@njit(cache=True)
def lexless(a, b):
    d = a ^ b
    if d == 0:
        return False
    low = d & (~d + np.uint64(1))
    return (a & low) != 0


@njit(cache=True)
def canon(x, n):
    """Lexicographically smallest sorted tuple in the dihedral orbit (bitmask)."""
    best = x
    first = True
    for s in range(n):
        z = addc(x, s, n)
        if first or lexless(z, best):
            best = z
            first = False
    r = negm(x, n)
    for s in range(n):
        z = addc(r, s, n)
        if lexless(z, best):
            best = z
    return best


@njit(cache=True)
def icv_of(x, n, out):
    for d in range(1, n // 2 + 1):
        c = popc(x & addc(x, d, n))
        if 2 * d == n:
            c //= 2
        out[d - 1] = c


# ===================================================================== recorder
@njit(cache=True)
def _record(y, mid, n, k, icvA, tmp, fam, hits, buf, bufm, nb, viol):
    """Register partner y produced by move mid.  Returns updated nb.
    fam non-empty: only family members are recorded (hits[j] |= 1<<mid).
    fam empty: every (canon, mid) pair goes to buf/bufm (test mode)."""
    if popc(y) != k:
        return nb
    icv_of(y, n, tmp)
    for i in range(n // 2):
        if tmp[i] != icvA[i]:
            viol[0] += 1
            return nb
    c = canon(y, n)
    if fam.shape[0] > 0:
        lo, hi = 0, fam.shape[0] - 1
        while lo <= hi:
            md = (lo + hi) // 2
            if fam[md] == c:
                hits[md] |= np.int64(1) << np.int64(mid)
                return nb
            elif fam[md] < c:
                lo = md + 1
            else:
                hi = md - 1
        return nb
    for i in range(nb):
        if buf[i] == c and bufm[i] == mid:
            return nb
    if nb < buf.shape[0]:
        buf[nb] = c
        bufm[nb] = mid
        nb += 1
    else:
        viol[1] += 1  # overflow flag
    return nb


# ===================================================================== kernel
@njit(cache=True)
def strict_kernel(x, n, fam, divs, ram, flags, buf, bufm):
    """All strict-tier moves (ids 0..10) applied to the set x (bitmask).
    ram: (len(divs), n) Ramanujan-sum rows c_d(g) for L8.
    flags: bitmask of move ids to run.
    Returns (hits, nb, viol)."""
    k = popc(x)
    mask = (np.uint64(1) << np.uint64(n)) - np.uint64(1)
    hits = np.zeros(max(fam.shape[0], 1), np.int64)
    viol = np.zeros(2, np.int64)
    nb = 0
    icvA = np.zeros(n // 2, np.int64)
    icv_of(x, n, icvA)
    tmp = np.zeros(n // 2, np.int64)
    el = np.zeros(k, np.int64)
    y = x
    i = 0
    while y:
        el[i] = ctz(y)
        y &= y - np.uint64(1)
        i += 1

    # ---------------- old moves
    if flags & 1 and 2 * k == n:
        nb = _record((~x) & mask, 0, n, k, icvA, tmp, fam, hits, buf, bufm, nb, viol)
    if flags & 2:
        out = np.empty(MAXF, np.uint64)
        c = _flips_into(x, n, out)
        for j in range(c):
            nb = _record(out[j], 1, n, k, icvA, tmp, fam, hits, buf, bufm, nb, viol)
    if flags & 4:
        out = np.empty(MAXF, np.uint64)
        cx = (~x) & mask
        c = _flips_into(cx, n, out)
        for j in range(c):
            nb = _record((~out[j]) & mask, 2, n, k, icvA, tmp, fam, hits, buf, bufm, nb, viol)

    # ---------------- block moves L2-L5
    P = np.zeros(n, np.int64)
    R = np.zeros(n, np.int64)
    Ue = np.zeros(k, np.int64)
    We = np.zeros(k, np.int64)
    if flags & (8 | 16 | 32 | 64):
        full = (1 << k) - 1
        for sub in range(1, full):
            W = np.uint64(0)
            nu = 0
            nw = 0
            for j in range(k):
                if (sub >> j) & 1:
                    W |= np.uint64(1) << np.uint64(el[j])
                    We[nw] = el[j]
                    nw += 1
                else:
                    Ue[nu] = el[j]
                    nu += 1
            U = x ^ W
            for g in range(n):
                P[g] = 0
                R[g] = 0
            for a in range(nu):
                for b in range(nw):
                    P[(Ue[a] - We[b]) % n] += 1
                    R[(Ue[a] + We[b]) % n] += 1
            # L2 translate: P periodic with period s
            if flags & 8:
                pmin = n
                for d in divs:
                    if d == n:
                        continue
                    ok = True
                    for g in range(n):
                        if P[(g + d) % n] != P[g]:
                            ok = False
                            break
                    if ok:
                        pmin = d
                        break
                s = pmin
                while s < n:
                    Wp = addc(W, s, n)
                    if (Wp & U) == 0:
                        nb = _record(U | Wp, 3, n, k, icvA, tmp, fam, hits, buf, bufm, nb, viol)
                    s += pmin
            # L3 swap: P[g - v] == P[-g], v = 2t
            if flags & 16:
                for v in range(1, n):
                    if n % 2 == 0 and v % 2 == 1:
                        continue
                    ok = True
                    for g in range(n):
                        if P[(g - v) % n] != P[(n - g) % n]:
                            ok = False
                            break
                    if ok:
                        Wp = addc(W, n - v, n)
                        if (Wp & U) == 0:
                            nb = _record(U | Wp, 4, n, k, icvA, tmp, fam, hits, buf, bufm, nb, viol)
            # L4 halfturn: C = P + P~ is n/2-periodic
            if flags & 32 and n % 2 == 0:
                m = n // 2
                ok = True
                for g in range(n):
                    if P[g] + P[(n - g) % n] != P[(g + m) % n] + P[(n - g - m) % n]:
                        ok = False
                        break
                if ok:
                    Wp = addc(W, m, n)
                    if (Wp & U) == 0:
                        nb = _record(U | Wp, 5, n, k, icvA, tmp, fam, hits, buf, bufm, nb, viol)
            # L5 reflect: P[g] == R[g + s]  ->  U + (s - W)
            if flags & 64:
                nW = negm(W, n)
                for s in range(n):
                    ok = True
                    for g in range(n):
                        if P[g] != R[(g + s) % n]:
                            ok = False
                            break
                    if ok:
                        Wp = addc(nW, s, n)
                        if (Wp & U) == 0:
                            nb = _record(U | Wp, 6, n, k, icvA, tmp, fam, hits, buf, bufm, nb, viol)

    # ---------------- L6 unit
    if flags & 128:
        ac = np.zeros(n, np.int64)
        for a in range(k):
            for b in range(k):
                ac[(el[a] - el[b]) % n] += 1
        for u in range(2, n):
            if _gcd(u, n) != 1:
                continue
            ok = True
            for g in range(n):
                if ac[(u * g) % n] != ac[g]:
                    ok = False
                    break
            if ok:
                nb = _record(mulm(x, u, n), 7, n, k, icvA, tmp, fam, hits, buf, bufm, nb, viol)

    # ---------------- L7 halfcoset
    if flags & 256:
        for h in divs:
            if h % 2 or h < 2:
                continue
            q = n // h
            cnt = np.zeros(q, np.int64)
            for a in range(k):
                cnt[el[a] % q] += 1
            ok = True
            for c in range(q):
                if cnt[c] != 0 and cnt[c] != h // 2:
                    ok = False
                    break
            if ok:
                Hc = np.uint64(0)
                for c in range(q):
                    if cnt[c]:
                        for j in range(h):
                            Hc |= np.uint64(1) << np.uint64(c + q * j)
                nb = _record(Hc ^ x, 8, n, k, icvA, tmp, fam, hits, buf, bufm, nb, viol)

    # ---------------- L8 signflip (exact integers: tot = n * A u_eps)
    if flags & 512:
        nd = divs.shape[0]
        lay = np.zeros((nd, n), np.int64)
        for di in range(nd):
            for a in range(k):
                for g in range(n):
                    lay[di, (el[a] + g) % n] += ram[di, g]
        tot = np.zeros(n, np.int64)
        # divs[0] == 1 always has sign +1
        for pat in range(1, 1 << (nd - 1)):
            for g in range(n):
                tot[g] = lay[0, g]
            for di in range(1, nd):
                sg = -1 if (pat >> (di - 1)) & 1 else 1
                for g in range(n):
                    tot[g] += sg * lay[di, g]
            ok = True
            B = np.uint64(0)
            for g in range(n):
                if tot[g] == n:
                    B |= np.uint64(1) << np.uint64(g)
                elif tot[g] != 0:
                    ok = False
                    break
            if ok:
                nb = _record(B, 9, n, k, icvA, tmp, fam, hits, buf, bufm, nb, viol)

    # ---------------- L9 coset-flat (strict criterion, solved directly)
    if flags & 1024:
        for h in divs:
            if h < 2:
                continue
            q = n // h
            occ = np.zeros(q, np.int64)
            Uc = np.zeros(q, np.uint64)
            for a in range(k):
                c = el[a] % q
                Uc[c] |= np.uint64(1) << np.uint64((el[a] // q) % h)
            C = 0
            for c in range(q):
                if Uc[c]:
                    occ[C] = c
                    C += 1
            # cross-correlations in Z_h
            PP = np.zeros((C, C, h), np.int64)
            for i1 in range(C):
                for i2 in range(C):
                    ya = Uc[occ[i1]]
                    while ya:
                        aa = ctz(ya)
                        ya &= ya - np.uint64(1)
                        yb = Uc[occ[i2]]
                        while yb:
                            bb = ctz(yb)
                            yb &= yb - np.uint64(1)
                            PP[i1, i2, (aa - bb) % h] += 1
            D = np.zeros(h, np.int64)
            for i1 in range(C):
                for g in range(h):
                    D[g] += PP[i1, i1, g]
            for u in range(1, h):
                if _gcd(u, h) != 1:
                    continue
                uinv = 1
                while (uinv * u) % h != 1:
                    uinv += 1
                ok = True
                for g in range(h):
                    if D[(u * g) % h] != D[g]:
                        ok = False
                        break
                if not ok:
                    continue
                # allowed[i1, i2] = bitmask of delta = s_i1 - s_i2
                allowed = np.zeros((C, C), np.uint64)
                for i1 in range(C):
                    for i2 in range(C):
                        if i1 == i2:
                            continue
                        am = np.uint64(0)
                        for dl in range(h):
                            ok2 = True
                            for g in range(h):
                                if PP[i1, i2, (uinv * (g - dl)) % h] != PP[i1, i2, g]:
                                    ok2 = False
                                    break
                            if ok2:
                                am |= np.uint64(1) << np.uint64(dl)
                        allowed[i1, i2] = am
                # DFS over s_1..s_{C-1}, s_0 = 0
                s = np.zeros(C, np.int64)
                pos = 1
                if C == 1:
                    if u != 1:
                        B = np.uint64(0)
                        c = occ[0]
                        yb = Uc[c]
                        while yb:
                            bb = ctz(yb)
                            yb &= yb - np.uint64(1)
                            B |= np.uint64(1) << np.uint64(c + q * ((u * bb) % h))
                        nb = _record(B, 10, n, k, icvA, tmp, fam, hits, buf, bufm, nb, viol)
                    continue
                s[1] = -1
                while pos >= 1:
                    s[pos] += 1
                    if s[pos] >= h:
                        pos -= 1
                        continue
                    good = True
                    for i2 in range(pos):
                        dl = (s[pos] - s[i2]) % h
                        if not (allowed[pos, i2] >> np.uint64(dl)) & np.uint64(1):
                            good = False
                            break
                    if not good:
                        continue
                    if pos == C - 1:
                        triv = u == 1
                        if triv:
                            for i1 in range(C):
                                if s[i1] != 0:
                                    triv = False
                        if not triv:
                            B = np.uint64(0)
                            for i1 in range(C):
                                c = occ[i1]
                                yb = Uc[c]
                                while yb:
                                    bb = ctz(yb)
                                    yb &= yb - np.uint64(1)
                                    B |= np.uint64(1) << np.uint64(c + q * ((s[i1] + u * bb) % h))
                            nb = _record(B, 10, n, k, icvA, tmp, fam, hits, buf, bufm, nb, viol)
                    else:
                        pos += 1
                        s[pos] = -1
    return hits, nb, viol


@njit(cache=True)
def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# ===================================================================== L10 (numpy)
_CAYLEY_CACHE = {}


def cayley_table(n):
    """Nonsingular 3-term P (0 in supp, coefficients +-1): list of (supp, signs) and
    the matrix R = conj(P^)/P^ (rows)."""
    if n in _CAYLEY_CACHE:
        return _CAYLEY_CACHE[n]
    from moves import three_term_vanishes
    Ps, rows, pint = [], [], []
    for x, y in combinations(range(1, n), 2):
        for sg in ((1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)):
            supp = (0, x, y)
            if three_term_vanishes(supp, sg, n):
                continue
            p = np.zeros(n, dtype=np.int64)
            for pos, c in zip(supp, sg):
                p[pos] += c
            Ph = np.fft.fft(p)
            Ps.append((supp, sg))
            rows.append(np.conj(Ph) / Ph)
            pint.append(p)
    R = np.array(rows) if rows else np.zeros((0, n), complex)
    _CAYLEY_CACHE[n] = (Ps, R, np.array(pint))
    return _CAYLEY_CACHE[n]


def _cconv(a, b):
    n = len(a)
    out = np.zeros(n, dtype=np.int64)
    for i in np.nonzero(a)[0]:
        out += a[i] * np.roll(b, int(i))
    return out


def cayley_partners(x, n):
    """L10: all 0/1 B with B*P = A*P~ for a nonsingular 3-term P; exact check.
    Returns {canon mask: [cert, ...]}."""
    Ps, R, pint = cayley_table(n)
    a = np.array([(x >> i) & 1 for i in range(n)], dtype=np.int64)
    k = int(a.sum())
    Ah = np.fft.fft(a)
    Bm = np.real(np.fft.ifft(Ah[None, :] * R, axis=1))
    Br = np.rint(Bm)
    ok = (np.max(np.abs(Bm - Br), axis=1) < 1e-6) & np.all((Br == 0) | (Br == 1), axis=1) \
        & (Br.sum(axis=1) == k)
    out = {}
    arev = None
    for r in np.nonzero(ok)[0]:
        b = Br[r].astype(np.int64)
        p = pint[r]
        prev = np.roll(p[::-1], 1)
        if not np.array_equal(_cconv(b, p), _cconv(a, prev)):
            continue
        m = 0
        for g in np.nonzero(b)[0]:
            m |= 1 << int(g)
        out.setdefault(int(canon(np.uint64(m), n)), []).append(("cayley",) + Ps[r])
    return out


# ===================================================================== helpers
def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def ramanujan_matrix(n):
    from moves import ramanujan
    ds = divisors(n)
    return np.array(ds, dtype=np.int64), np.array([[ramanujan(d, g) for g in range(n)] for d in ds],
                                                  dtype=np.int64)


def to_mask(S):
    m = 0
    for s in S:
        m |= 1 << s
    return m


def to_tuple(m):
    return tuple(i for i in range(64) if (m >> i) & 1)


ALLFLAGS = (1 << 11) - 1


def strict_partners(A, n, flags=ALLFLAGS, cap=1 << 16):
    """Python API (test mode): {canon tuple: set(move names)} for all strict-tier
    moves of A, WITHOUT restriction to a family."""
    divs, ram = ramanujan_matrix(n)
    buf = np.zeros(cap, np.uint64)
    bufm = np.zeros(cap, np.int64)
    _, nb, viol = strict_kernel(np.uint64(to_mask(A)), n, np.zeros(0, np.uint64), divs, ram,
                                flags, buf, bufm)
    if viol[0] or viol[1]:
        raise RuntimeError(f"soundness violations {viol[0]}, overflow {viol[1]}")
    out = defaultdict(set)
    for i in range(nb):
        out[to_tuple(int(buf[i]))].add(MOVE_NAMES[int(bufm[i])])
    return dict(out)


# ===================================================================== families
def load_families(n):
    path = os.path.join(ROOT, "results", "fastcensus", f"families_n{n}.txt.gz")
    fams = []
    with gzip.open(path, "rt") as f:
        for line in f:
            kk, rest = line.rstrip("\n").split("\t")
            fams.append((int(kk), [int(h, 16) for h in rest.split()]))
    return fams


class UF:
    def __init__(self, m):
        self.p = list(range(m))

    def f(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def u(self, a, b):
        self.p[self.f(a)] = self.f(b)

    def comps(self):
        return len({self.f(i) for i in range(len(self.p))})


def ncomp(sz, edges, allowed_bits):
    uf = UF(sz)
    for (i, j), b in edges.items():
        if b & allowed_bits:
            uf.u(i, j)
    return uf.comps()


_EXTRA = None  # optional P3 move hook: f(mask, n, fam_sorted) -> {index: bitmask(extra ids)}


def family_edges(args):
    """Edges of one family: {(i, j): move bitmask} over member indices (sorted order)."""
    n, members, with_l10, extra = args
    fam = np.array(sorted(members), dtype=np.uint64)
    divs, ram = ramanujan_matrix(n)
    buf = np.zeros(1, np.uint64)
    bufm = np.zeros(1, np.int64)
    edges = defaultdict(int)
    viol = 0
    idx = {int(m): i for i, m in enumerate(fam)}
    for i, x in enumerate(fam):
        hits, _, v = strict_kernel(x, n, fam, divs, ram, ALLFLAGS, buf, bufm)
        viol += int(v[0])
        for j in np.nonzero(hits)[0]:
            if j != i:
                edges[tuple(sorted((i, int(j))))] |= int(hits[j])
        if with_l10:
            for c in cayley_partners(int(x), n):
                j = idx.get(c)
                if j is not None and j != i:
                    edges[tuple(sorted((i, j)))] |= 1 << MID["cayley"]
    if extra and ncomp(len(fam), edges, bits(STRICT)) > 1:
        import p3_moves
        mask = (1 << n) - 1
        comp = [int(canon(np.uint64((~int(m)) & mask), n)) for m in fam]
        order = sorted(range(len(fam)), key=lambda t: comp[t])
        famc = np.array([comp[t] for t in order], dtype=np.uint64)
        for i, x in enumerate(fam):
            for jc, b in p3_moves.cconj_partners(int(x), n, famc).items():
                j = order[jc]
                if j != i and b & bits(STRICT):
                    edges[tuple(sorted((i, j)))] |= 1 << p3_moves.P3_MID["cconj"]
            for c, names in p3_moves.p3_partners(int(x), n).items():
                j = idx.get(c)
                if j is not None and j != i:
                    b = 0
                    for nm in names:
                        b |= 1 << p3_moves.P3_MID[nm]
                    edges[tuple(sorted((i, j)))] |= b
    return [int(m) for m in fam], dict(edges), viol


def compute_n(n, jobs, direct_large=False, extra=False, verbose=True):
    fams = load_families(n)
    t0 = time.time()
    work = [(n, f, True, extra) for k, f in fams if direct_large or 2 * k <= n]
    kof = [k for k, f in fams if direct_large or 2 * k <= n]
    # biggest families first for load balance
    if jobs > 1:
        from multiprocessing import Pool
        with Pool(jobs) as p:
            res = p.map(family_edges, work, chunksize=8)
    else:
        res = [family_edges(w) for w in work]
    tiers = {"old": bits(OLD), "strict": bits(STRICT), "strict+L10": bits(STRICT + L10)}
    per_lemma = [m for m in MOVE_NAMES if m not in ("babbitt",)]
    if extra:
        import p3_moves
        pb = 0
        for nm in p3_moves.P3_NAMES:
            pb |= 1 << p3_moves.P3_MID[nm]
        tiers["strict+P3"] = bits(STRICT) | pb
        tiers["strict+P3+L10"] = bits(STRICT + L10) | pb
        per_lemma += list(p3_moves.P3_NAMES)
    rows = []
    viol = 0
    status = {}   # canon of first member -> row
    for k, (members, edges, v) in zip(kof, res):
        viol += v
        sz = len(members)
        row = {"k": k, "size": sz, "members": members, "edges": edges}
        for t, b in tiers.items():
            row[t] = ncomp(sz, edges, b)
        row["alone"] = {}
        for m in per_lemma:
            mid = MID[m] if m in MID else __import__("p3_moves").P3_MID[m]
            row["alone"][m] = ncomp(sz, edges, 1 << mid) == 1
        rows.append(row)
        for mm in members:
            status[mm] = row
    # large k via complement
    if not direct_large:
        mask = (1 << n) - 1
        for k, f in fams:
            if 2 * k <= n:
                continue
            c = int(canon(np.uint64((~f[0]) & mask), n))
            src = status[c]
            row = {"k": k, "size": len(f), "members": f, "edges": None, "via_complement": True}
            for t in tiers:
                row[t] = src[t]
            row["alone"] = dict(src["alone"])
            rows.append(row)
    if verbose:
        print(f"n={n}: {len(fams)} families, {len(work)} computed directly, "
              f"{time.time()-t0:.1f}s, soundness violations={viol}", flush=True)
    return rows, list(tiers), viol, time.time() - t0


def icv_tuple(m, n):
    out = []
    for d in range(1, n // 2 + 1):
        r = ((m << d) | (m >> (n - d))) & ((1 << n) - 1)
        c = bin(m & r).count("1")
        if 2 * d == n:
            c //= 2
        out.append(c)
    return tuple(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=8)
    ap.add_argument("--nmax", type=int, default=20)
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--direct-large", action="store_true")
    ap.add_argument("--p3", action="store_true", help="add the P3 moves of src/p3_moves.py")
    ap.add_argument("--tag", default="")
    ap.add_argument("--csv", default=None)
    a = ap.parse_args()
    outdir = os.path.join(ROOT, "results")
    sumdir = os.path.join(outdir, "p3_coverage")
    os.makedirs(sumdir, exist_ok=True)
    csvp = a.csv or os.path.join(outdir, f"p3_coverage_{a.nmin}_{a.nmax}{a.tag}.csv")
    csvrows = []
    for n in range(a.nmin, a.nmax + 1):
        rows, tiers, viol, secs = compute_n(n, a.jobs, a.direct_large, a.p3)
        # table by (k, size)
        agg = defaultdict(lambda: Counter())
        for r in rows:
            for key in ((r["k"], r["size"]), ("all", "all")):
                agg[key]["families"] += 1
                for t in tiers:
                    agg[key]["unexpl " + t] += r[t] > 1
        for (k, sz), c in sorted(agg.items(), key=lambda z: (str(z[0][0]).zfill(3), str(z[0][1]).zfill(3))):
            d = {"n": n, "k": k, "family_size": sz, "families": c["families"]}
            for t in tiers:
                d["unexpl " + t] = c["unexpl " + t]
            csvrows.append(d)
        tot = agg[("all", "all")]
        print("   " + "  ".join(f"{t}: {tot[t if t == 'families' else 'unexpl ' + t]}" for t in ["families"] + tiers),
              flush=True)
        # unexplained listing
        with open(os.path.join(outdir, f"p3_unexplained_n{n}{a.tag}.txt"), "w") as f:
            f.write(f"# n={n}: Z-families NOT connected by the strict tier ({'+'.join(STRICT)})\n")
            f.write("# columns: k, family size, #components strict, #components strict+L10"
                    + (", strict+P3, strict+P3+L10" if a.p3 else "")
                    + ", via_complement, ICV, members (canonical tuples)\n")
            for r in rows:
                if r["strict"] > 1:
                    extra = [r[t] for t in tiers if t.startswith("strict+P3")]
                    f.write("\t".join(str(v) for v in [r["k"], r["size"], r["strict"], r["strict+L10"]] + extra
                                      + [int(r.get("via_complement", False)),
                                         icv_tuple(r["members"][0], n),
                                         " ".join(str(to_tuple(m)).replace(" ", "") for m in r["members"])]) + "\n")
        summ = {"n": n, "seconds": round(secs, 1), "soundness_violations": viol,
                "families": len(rows), "tiers": tiers,
                "unexplained": {t: sum(r[t] > 1 for r in rows) for t in tiers},
                "alone": dict(Counter(m for r in rows for m, v in r["alone"].items() if v))}
        with open(os.path.join(sumdir, f"summary_n{n}{a.tag}.json"), "w") as f:
            json.dump(summ, f)
    with open(csvp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(csvrows[0].keys()))
        w.writeheader()
        for r in csvrows:
            w.writerow(r)
    print("wrote", csvp)


if __name__ == "__main__":
    main()
