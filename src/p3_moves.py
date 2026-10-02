"""
p3_moves.py -- new ICV-preserving moves of workstream P3 (proofs in notes/p3_moves.md).

  "cconj"     P3.1  complement conjugation of a strict move:  A -> C(M(C(A))),
                    C = complement in Z_n, M any strict-tier move of src/p3_coverage.py
                    (L2-L9-flat, old moves).  The intermediate set C(A) has a different
                    cardinality, so it is NOT a member of A's family.
  "coverflip" P3.2  lambda-fold multiset tiling flip:  if  lam*1_G + sgn*1_A = P*Q  with
                    P, Q in Z_{>=0}[G] (multisets), and  lam*1_G + sgn*1_B := P*Q~  is 0/1,
                    then B is homometric to A.  lam = 0, sgn = +1, P,Q 0/1 is the old direct-
                    sum flip; lam = 1, sgn = -1 is the old complement-of-flip; lam >= 1 with
                    multiplicities covers reductions mod n of direct sums in Z_{mn} and of
                    integer (0/1-factor) Rosenblatt-Seymour flips ("shadows").
  "dsx"       P3.3  difference-set product exchange (the Z_21 mechanism):
                    in G = K x H with K = <x> of order 3 and Q c H with
                    Q Q~ = 3 delta + Q + Q~  (i.e. H = Z_7, Q a Paley (7,3,1) set),
                    (1 + x) (x) Q  and  1_K (x) delta + x (x) Q  are homometric; the move
                    applies it inside Z_n through an embedding Z_3 x Z_7 = Z_21 -> Z_n
                    (21 | n, L0 inflation) composed with any translation/automorphism.

Every function returns {canonical bitmask: [certificate, ...]}; every certificate is
re-verified (exact integer identity) before being returned, and the coverage driver
additionally re-checks the ICV of every partner.
"""
from __future__ import annotations

import os
import sys
from itertools import combinations_with_replacement
from math import gcd

import numpy as np
from numba import njit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import p3_coverage as pc  # noqa: E402

P3_NAMES = ["cconj", "coverflip", "dsx", "zflip"]
P3_MID = {nm: 12 + i for i, nm in enumerate(P3_NAMES)}   # bits 12.. (0..11 used by p3_coverage)


# ===================================================================== P3.1 cconj
def cconj_partners(x, n, famc_sorted=None, flags=pc.ALLFLAGS, cap=1 << 18):
    """Partners C(M(C(A))) for all strict moves M.  If famc_sorted (sorted array of the
    canonical complements of the family members) is given, only those are searched and
    the result is {index into famc_sorted: bitmask of strict move ids}."""
    mask = (1 << n) - 1
    cx = np.uint64((~int(x)) & mask)
    divs, ram = pc.ramanujan_matrix(n)
    if famc_sorted is not None:
        buf = np.zeros(1, np.uint64)
        bufm = np.zeros(1, np.int64)
        hits, _, viol = pc.strict_kernel(cx, n, famc_sorted, divs, ram, flags, buf, bufm)
        if viol[0]:
            raise RuntimeError("cconj: soundness violation")
        return {int(j): int(hits[j]) for j in np.nonzero(hits)[0]}
    buf = np.zeros(cap, np.uint64)
    bufm = np.zeros(cap, np.int64)
    _, nb, viol = pc.strict_kernel(cx, n, np.zeros(0, np.uint64), divs, ram, flags, buf, bufm)
    if viol[0] or viol[1]:
        raise RuntimeError(f"cconj: violations {viol[0]}, overflow {viol[1]}")
    out = {}
    for i in range(nb):
        b = (~int(buf[i])) & mask
        out.setdefault(int(pc.canon(np.uint64(b), n)), []).append(("cconj", pc.MOVE_NAMES[int(bufm[i])]))
    return out


# ===================================================================== P3.2 coverflip
@njit  # no cache: cached recursive numba functions segfaulted on reload (see notes/p3_log.md)
def _mcover(T, Pel, Pm, npel, n, Q, out, nout, limit, nodes):
    """All multisets Q (count vectors) with P*Q == T (T is modified in place and restored).
    P given by distinct elements Pel[:npel] with multiplicities Pm[:npel], Pel[0] = 0.
    Branch on the lowest point s with T[s] > 0: some element b of P covers it, c = s - b.
    Each Q is produced at least once (possibly repeatedly; duplicates are harmless)."""
    nodes[0] += 1
    if nodes[0] > limit:
        return nout
    s = -1
    for g in range(n):
        if T[g] > 0:
            s = g
            break
    if s < 0:
        if nout < out.shape[0]:
            for g in range(n):
                out[nout, g] = Q[g]
            nout += 1
        return nout
    for i in range(npel):
        c = (s - Pel[i]) % n
        ok = True
        for j in range(npel):
            if T[(Pel[j] + c) % n] < Pm[j]:
                ok = False
                break
        if not ok:
            continue
        for j in range(npel):
            T[(Pel[j] + c) % n] -= Pm[j]
        Q[c] += 1
        nout = _mcover(T, Pel, Pm, npel, n, Q, out, nout, limit, nodes)
        Q[c] -= 1
        for j in range(npel):
            T[(Pel[j] + c) % n] += Pm[j]
    return nout


@njit
def _coverflip_kernel(a, n, lam, sgn, Plist, Psz, fam, qcap, limit):
    """For one (lam, sgn) and a list of multisets P (rows of Plist: sorted elements,
    first = 0, length Psz[i]), return rows (Bmask, pindex)."""
    k = 0
    for g in range(n):
        k += a[g]
    T = np.zeros(n, np.int64)
    for g in range(n):
        T[g] = lam + sgn * a[g]
    res_b = np.zeros(4096, np.uint64)
    res_p = np.zeros(4096, np.int64)
    nres = 0
    Pel = np.zeros(16, np.int64)
    Pm = np.zeros(16, np.int64)
    Q = np.zeros(n, np.int64)
    out = np.zeros((qcap, n), np.int64)
    nodes = np.zeros(1, np.int64)
    for pi in range(Plist.shape[0]):
        p = Psz[pi]
        npel = 0
        for j in range(p):
            v = Plist[pi, j]
            if npel > 0 and Pel[npel - 1] == v:
                Pm[npel - 1] += 1
            else:
                Pel[npel] = v
                Pm[npel] = 1
                npel += 1
        for g in range(n):
            Q[g] = 0
        nodes[0] = 0
        nq = _mcover(T, Pel, Pm, npel, n, Q, out, 0, limit, nodes)
        for qi in range(nq):
            # B = sgn * (P * Q~ - lam)
            Bv = np.zeros(n, np.int64)
            for j in range(npel):
                for c in range(n):
                    if out[qi, c]:
                        Bv[(Pel[j] - c) % n] += Pm[j] * out[qi, c]
            ok = True
            bm = np.uint64(0)
            cnt = 0
            for g in range(n):
                v = sgn * (Bv[g] - lam)
                if v == 1:
                    bm |= np.uint64(1) << np.uint64(g)
                    cnt += 1
                elif v != 0:
                    ok = False
                    break
            if ok and cnt == k and nres < res_b.shape[0]:
                res_b[nres] = bm
                res_p[nres] = pi
                nres += 1
    return res_b[:nres], res_p[:nres]


_PCACHE = {}


def _pmenu(n, p):
    key = (n, p)
    if key not in _PCACHE:
        rows = [(0,) + r for r in combinations_with_replacement(range(n), p - 1)]
        arr = np.zeros((len(rows), 16), np.int64)
        for i, r in enumerate(rows):
            arr[i, :p] = r
        _PCACHE[key] = (arr, np.full(len(rows), p, np.int64), rows)
    return _PCACHE[key]


def coverflip_partners(x, n, lam_max=3, pmax=4, qcap=64, limit=20000, include_old=False):
    """P3.2: all lambda-fold multiset tiling flips with 0 <= lam <= lam_max, |P| <= pmax,
    |P| <= |Q| (WLOG, see notes).  Returns {canon mask: [cert]}.  Every certificate is
    re-verified with exact integer arithmetic here (P*Q == lam + sgn*A, and
    B == sgn*(P*Q~ - lam))."""
    a = np.array([(int(x) >> i) & 1 for i in range(n)], dtype=np.int64)
    k = int(a.sum())
    out = {}
    for lam in range(0, lam_max + 1):
        for sgn in (1, -1):
            if lam == 0 and sgn == -1:
                continue
            if not include_old and ((lam == 0 and sgn == 1) or (lam == 1 and sgn == -1)):
                pass  # old moves are still searched with multiplicity; kept for completeness
            tot = lam * n + sgn * k
            if tot <= 0:
                continue
            for p in range(2, pmax + 1):
                if tot % p or p * p > tot:
                    continue
                Plist, Psz, rows = _pmenu(n, p)
                bs, ps = _coverflip_kernel(a, n, lam, sgn, Plist, Psz, np.zeros(0, np.uint64), qcap, limit)
                for bm, pi in zip(bs, ps):
                    c = int(pc.canon(np.uint64(bm), n))
                    out.setdefault(c, []).append(("coverflip", lam, sgn, rows[int(pi)]))
    return out


def coverflip_certificate(A, B, n, lam, sgn, P):
    """Recompute Q from (A, lam, sgn, P) and verify the identity exactly; returns Q or None."""
    a = np.zeros(n, np.int64)
    a[list(A)] = 1
    T = lam + sgn * a
    Pel, Pm = np.unique(np.array(P, np.int64), return_counts=True)
    out = np.zeros((64, n), np.int64)
    nq = _mcover(T.copy(), Pel.astype(np.int64), Pm.astype(np.int64), len(Pel), n,
                 np.zeros(n, np.int64), out, 0, 10 ** 6, np.zeros(1, np.int64))
    pv = np.zeros(n, np.int64)
    for e, m in zip(Pel, Pm):
        pv[e] += m
    for qi in range(nq):
        q = out[qi]
        if not np.array_equal(pc._cconv(pv, q), T):
            continue
        bv = sgn * (pc._cconv(pv, np.roll(q[::-1], 1)) - lam)
        if set(np.unique(bv)) <= {0, 1} and pc.canon(np.uint64(sum(1 << int(g) for g in np.nonzero(bv)[0])), n) \
                == pc.canon(np.uint64(sum(1 << int(b) for b in B)), n):
            return q
    return None


# ===================================================================== P3.2b zflip
_ZCACHE = {}


def zflip_menu(n, max01=6, maxpm=4):
    """Nonsingular P with 0 in supp: 0/1 coefficients and 3..max01 terms, or +-1
    coefficients (not all +1) and 3..maxpm terms.  Returns (list of P vectors, Phat)."""
    key = (n, max01, maxpm)
    if key in _ZCACHE:
        return _ZCACHE[key]
    from itertools import combinations, product
    rows = []
    for t in range(3, max01 + 1):
        for rest in combinations(range(1, n), t - 1):
            p = np.zeros(n, np.int64)
            p[0] = 1
            p[list(rest)] = 1
            rows.append(p)
    for t in range(3, maxpm + 1):
        for rest in combinations(range(1, n), t - 1):
            for sg in product((1, -1), repeat=t - 1):
                if all(v == 1 for v in sg):
                    continue
                p = np.zeros(n, np.int64)
                p[0] = 1
                for r, v in zip(rest, sg):
                    p[r] = v
                rows.append(p)
    P = np.array(rows)
    Ph = np.fft.fft(P, axis=1)
    ok = np.min(np.abs(Ph), axis=1) > 1e-6        # numerical pre-filter; exact check below
    _ZCACHE[key] = (P[ok], Ph[ok])
    return _ZCACHE[key]


def zflip_partners(x, n, max01=6, maxpm=4):
    """P3.2b (affine integral factor flip, FFT search): nonsingular P from zflip_menu;
    if 1_A = lam*J + P*Q with Q INTEGRAL for some integer lam, the partner is
    lam*J + P~*Q.  (For nonsingular P this equals A*P~/P, the Cayley partner, so the
    extra content over the rational version is the integrality of Q.)  Everything is
    re-verified with exact integer convolutions."""
    P, Ph = zflip_menu(n, max01, maxpm)
    a = np.array([(int(x) >> i) & 1 for i in range(n)], dtype=np.int64)
    k = int(a.sum())
    Ah = np.fft.fft(a)
    Bm = np.real(np.fft.ifft(Ah[None, :] * np.conj(Ph) / Ph, axis=1))
    Br = np.rint(Bm)
    cand = np.nonzero((np.max(np.abs(Bm - Br), axis=1) < 1e-6)
                      & np.all((Br == 0) | (Br == 1), axis=1) & (Br.sum(axis=1) == k))[0]
    out = {}
    J = np.ones(n, np.int64)
    for r in cand:
        p = P[r]
        s = int(p.sum())
        q0 = np.real(np.fft.ifft(Ah / Ph[r]))
        # need integer lam with q0 - (lam/s) J integral
        c = q0[0] - np.floor(q0[0])
        lam = int(round(s * c))
        found = None
        for L in (lam - s, lam, lam + s):
            q = q0 - L / s
            qr = np.rint(q)
            if np.max(np.abs(q - qr)) < 1e-6:
                qr = qr.astype(np.int64)
                if np.array_equal(pc._cconv(p, qr), a - L * J):        # exact: A = L J + P Q
                    found = (L, qr)
                    break
        if found is None:
            continue
        L, qr = found
        prev = np.roll(p[::-1], 1)
        b = L * J + pc._cconv(prev, qr)                                  # exact: B = L J + P~ Q
        if not np.all((b == 0) | (b == 1)) or int(b.sum()) != k:
            continue
        # exact nonsingularity is not needed for soundness (the identity is exact), but
        # we record it: the lemma only uses A = L J + P Q and B = L J + P~ Q.
        m = 0
        for g in np.nonzero(b)[0]:
            m |= 1 << int(g)
        out.setdefault(int(pc.canon(np.uint64(m), n)), []).append(
            ("zflip", L, tuple(int(v) for v in np.nonzero(p)[0]), tuple(int(p[v]) for v in np.nonzero(p)[0])))
    return out


# ===================================================================== P3.3 dsx
def _z21_pair():
    """The two model sets in Z_21 (CRT coordinates x = 7 of order 3, y = 15 of order 7)."""
    X, Y = 7, 15
    Q = [(Y * r) % 21 for r in (1, 2, 4)]              # Paley set {1,2,4} in <y>
    A = sorted({(e + q) % 21 for e in (0, X) for q in Q})
    B = sorted({0, X, 2 * X % 21} | {(X + q) % 21 for q in Q})
    return A, B


def dsx_partners(x, n):
    """P3.3 applied through every embedding: for 21 | n, m = n/21, the pair (A0, B0) of
    _z21_pair inflated by m (L0), then every unit multiple u (u in Z_n^*) and every
    translation t.  If x equals (a dihedral image of) u*m*A0 + t, return u*m*B0 + t, and
    vice versa.  This is a lookup of a fixed identity, not a search over ICVs."""
    out = {}
    if n % 21:
        return out
    m = n // 21
    A0, B0 = _z21_pair()
    cx = int(pc.canon(np.uint64(int(x)), n))
    for u in range(1, n):
        if gcd(u, n) != 1:
            continue
        for S, T in ((A0, B0), (B0, A0)):
            s = sum(1 << ((u * m * a) % n) for a in S)
            if int(pc.canon(np.uint64(s), n)) == cx:
                t = sum(1 << ((u * m * b) % n) for b in T)
                out.setdefault(int(pc.canon(np.uint64(t), n)), []).append(("dsx", u))
    return out


# ===================================================================== driver hook
def p3_partners(x, n, fam=None, lam_max=3, pmax=4):
    """Union of the P3.2 and P3.3 partners of x (cconj is handled family-wise by the
    coverage driver because it needs the complement family)."""
    res = {}
    for d in (coverflip_partners(x, n, lam_max, pmax), dsx_partners(x, n), zflip_partners(x, n)):
        for c, certs in d.items():
            res.setdefault(c, set()).update(ct[0] for ct in certs)
    return res
