"""
moves.py -- explicit ICV-preserving moves (workstream P2).

Every move here takes a pitch-class set A in Z_n and returns partner sets B,
each of which is homometric to A (same ICV) by a lemma proved IN FULL in
notes/p2_moves.md.  The lemma numbers below refer to that file.

Group-ring conventions (Z[Z_n]):
  * an element is a length-n integer numpy vector f, f[g] = coefficient of x^g;
  * f * h = cyclic convolution;  f~ (reverse) = f(x^{-1}), i.e. f~[g] = f[-g];
  * for a set A, 1_A 1_A~ is the autocorrelation; two sets are homometric
    iff their autocorrelations agree (equivalently, iff their ICVs agree).

Moves (name used in certificates -> lemma):
  "translate"   L2  block translation with periodic cross-correlation
  "swap"        L3  co-symmetric block swap  U + x^t V  <->  U + x^-t V
  "halfturn"    L4  block half-turn, z-invariant symmetrised cross-correlation
  "reflect"     L5  block reflection with annihilated asymmetry
  "unit"        L6  multiplication by a unit fixing the autocorrelation
  "halfcoset"   L7  complement inside the occupied cosets of H (half-filled)
  "signflip"    L8  torsion spectral unit with values +-1 (per divisor layer)
  "coset-flat"  L9  coset-wise automorphism, flat (strict) criterion
  "coset-exact" L9' coset-wise automorphism, exact per-coset-class criterion
  "cayley"      L10 Cayley unit P~/P of a 3-term P (rational-cofactor flip)
Moves of type "block-exact" (L1) / "coset-exact" (L9') use an iff-criterion
for their SHAPE; they are sound but have weaker explanatory content (see notes).

Old moves (src/homometry.py): Babbitt complement, 0/1 direct-sum flip,
complement-of-flip; re-exported as "babbitt", "dsflip".
"""
from __future__ import annotations

import os
import sys
from itertools import combinations, product
from math import gcd
from typing import Dict, List, Sequence, Tuple

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from homometry import complement, dihedral_canon, direct_sum_flips  # noqa: E402

PCSet = Tuple[int, ...]


# ------------------------------------------------------------ group ring
def ind(S: Sequence[int], n: int) -> np.ndarray:
    v = np.zeros(n, dtype=np.int64)
    for s in S:
        v[s % n] += 1
    return v


def conv(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Exact cyclic convolution in Z[Z_n]."""
    out = np.zeros(len(a), dtype=np.int64)
    for i in np.nonzero(a)[0]:
        out += a[i] * np.roll(b, int(i))
    return out


def rev(a: np.ndarray) -> np.ndarray:
    return np.roll(a[::-1], 1)


def shift(a: np.ndarray, s: int) -> np.ndarray:
    return np.roll(a, s)


def autocorr(S: Sequence[int], n: int) -> np.ndarray:
    a = ind(S, n)
    return conv(a, rev(a))


def icv_fast(S: Sequence[int], n: int) -> Tuple[int, ...]:
    v = [0] * (n // 2)
    S = list(S)
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            d = (S[i] - S[j]) % n
            v[min(d, n - d) - 1] += 1
    return tuple(v)


def _splits(A: Sequence[int], max_block: int | None = None):
    """(U, W) with A = U disjoint-union W, both nonempty."""
    A = list(A)
    k = len(A)
    top = k - 1 if max_block is None else min(k - 1, max_block)
    for r in range(1, top + 1):
        for W in combinations(A, r):
            Ws = set(W)
            yield [a for a in A if a not in Ws], list(W)


def _add(out: Dict, B, n: int, k: int, cert) -> None:
    Bs = tuple(sorted({b % n for b in B}))
    if len(Bs) == k:
        out.setdefault(Bs, []).append(cert)


# ------------------------------------------------------------ L2 translate
def translation_moves(A: Sequence[int], n: int) -> Dict[PCSet, list]:
    """L2: if (1 - x^s) U W~ = 0 then U + x^s W is homometric to U + W."""
    out: Dict = {}
    k = len(A)
    for U, W in _splits(A):
        P = conv(ind(U, n), rev(ind(W, n)))
        for s in range(1, n):
            if np.array_equal(shift(P, s), P):
                _add(out, U + [w + s for w in W], n, k, ("translate", tuple(U), tuple(W), s))
    return out


# ------------------------------------------------------------ L3 swap
def swap_moves(A: Sequence[int], n: int) -> Dict[PCSet, list]:
    """L3: A = U + x^t V with U V~ = V U~  ==>  U + x^{-t} V homometric."""
    out: Dict = {}
    k = len(A)
    for U, W in _splits(A):
        u = ind(U, n)
        for t in range(1, n):
            v = shift(ind(W, n), -t)          # V = x^{-t} W
            if np.array_equal(conv(u, rev(v)), conv(v, rev(u))):
                _add(out, U + [w - 2 * t for w in W], n, k, ("swap", tuple(U), tuple(W), t))
    return out


# ------------------------------------------------------------ L4 half-turn
def halfturn_moves(A: Sequence[int], n: int) -> Dict[PCSet, list]:
    """L4 (n even, z = x^{n/2}): (1 - z)(U W~ + W U~) = 0 ==> U + zW homometric."""
    out: Dict = {}
    if n % 2:
        return out
    k, m = len(A), n // 2
    for U, W in _splits(A):
        u, w = ind(U, n), ind(W, n)
        C = conv(u, rev(w)) + conv(w, rev(u))
        if np.array_equal(shift(C, m), C):
            _add(out, U + [x + m for x in W], n, k, ("halfturn", tuple(U), tuple(W)))
    return out


# ------------------------------------------------------------ L5 reflect
def reflection_moves(A: Sequence[int], n: int) -> Dict[PCSet, list]:
    """L5: U (W~ - x^{-s} W) = 0  ==>  U + x^s W~  (= U u (s - W)) homometric."""
    out: Dict = {}
    k = len(A)
    for U, W in _splits(A):
        u, w = ind(U, n), ind(W, n)
        for s in range(n):
            if not conv(u, rev(w) - shift(w, -s)).any():
                _add(out, U + [s - x for x in W], n, k, ("reflect", tuple(U), tuple(W), s))
    return out


# ------------------------------------------------------------ L6 unit
def unit_moves(A: Sequence[int], n: int) -> Dict[PCSet, list]:
    """L6: if the autocorrelation of A is invariant under g -> u g (u a unit),
    then uA is homometric to A."""
    out: Dict = {}
    k = len(A)
    ac = autocorr(A, n)
    for u in range(2, n):
        if gcd(u, n) != 1:
            continue
        perm = np.array([ac[(u * g) % n] for g in range(n)])
        if np.array_equal(perm, ac):
            _add(out, [u * a for a in A], n, k, ("unit", u))
    return out


# ------------------------------------------------------------ L7 half-coset complement
def halfcoset_moves(A: Sequence[int], n: int) -> Dict[PCSet, list]:
    """L7: H <= Z_n of even order h; if every coset of H meets A in 0 or h/2
    points, then (A + H) minus A is homometric to A."""
    out: Dict = {}
    k = len(A)
    Aset = set(A)
    for h in range(2, n + 1, 2):
        if n % h:
            continue
        q = n // h
        cnt: Dict[int, int] = {}
        for a in A:
            cnt[a % q] = cnt.get(a % q, 0) + 1
        if all(c == h // 2 for c in cnt.values()):
            B = [c + q * j for c in cnt for j in range(h) if (c + q * j) not in Aset]
            _add(out, B, n, k, ("halfcoset", h))
    return out


# ------------------------------------------------------------ L8 sign flips
def divisors(n: int) -> List[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def _phi(m: int) -> int:
    return sum(1 for j in range(1, m + 1) if gcd(j, m) == 1)


def _mobius(m: int) -> int:
    r, p = 1, 2
    while p * p <= m:
        if m % p == 0:
            m //= p
            if m % p == 0:
                return 0
            r = -r
        p += 1
    return -r if m > 1 else r


def ramanujan(d: int, x: int) -> int:
    """c_d(x) = sum over k in (Z/d)^* of exp(2 pi i k x / d)  (an integer):
    c_d(x) = mu(d/g) phi(d) / phi(d/g),  g = gcd(d, x)."""
    g = gcd(d, x)
    return _mobius(d // g) * _phi(d) // _phi(d // g)


def sign_unit(eps: Dict[int, int], n: int) -> np.ndarray:
    """n * u_eps as an integer vector:  u_eps = sum_d eps_d e_d, where e_d is the
    primitive idempotent of Q[Z_n] for the layer {k : n/gcd(k,n) = d}:
    e_d(g) = c_d(g)/n."""
    v = np.zeros(n, dtype=np.int64)
    for d, e in eps.items():
        v += e * np.array([ramanujan(d, g) for g in range(n)], dtype=np.int64)
    return v


def signflip_moves(A: Sequence[int], n: int, max_layers: int = 12) -> Dict[PCSet, list]:
    """L8: for eps: {d | n} -> {+1,-1}, u_eps is a rational spectral unit with
    u_eps * u_eps = delta_0; if 1_A * u_eps is a 0/1 vector it is homometric to A."""
    out: Dict = {}
    k = len(A)
    ds = divisors(n)
    if len(ds) > max_layers:
        raise ValueError("too many divisor layers")
    a = ind(A, n)
    base = {d: np.array([ramanujan(d, g) for g in range(n)], dtype=np.int64) for d in ds}
    layers = {d: conv(a, base[d]) for d in ds}          # n * (A e_d)
    for signs in product((1, -1), repeat=len(ds) - 1):
        eps = dict(zip(ds[1:], signs))
        eps[1] = 1                                      # |B| = |A| forces eps_1 = +1
        tot = sum(eps[d] * layers[d] for d in ds)       # = n * (A * u_eps)
        if all(s == 1 for s in signs):
            continue
        if np.all((tot == 0) | (tot == n)):
            B = [g for g in range(n) if tot[g] == n]
            _add(out, B, n, k, ("signflip", tuple(sorted(d for d in ds if eps[d] < 0))))
    return out


# ------------------------------------------------------------ L9 coset-wise automorphism
def _icv_batch(X: np.ndarray, n: int) -> np.ndarray:
    """ICVs of many sets at once; X shape (N, k)."""
    N, k = X.shape
    iu, ju = np.triu_indices(k, 1)
    D = (X[:, iu] - X[:, ju]) % n
    D = np.minimum(D, n - D) - 1                          # -1 marks a repeated point
    out = np.zeros((N, n // 2 + 1), dtype=np.int64)
    rows = np.repeat(np.arange(N), len(iu))
    np.add.at(out, (rows, np.where(D.ravel() < 0, n // 2, D.ravel())), 1)
    return out


def coset_decomposition(A: Sequence[int], n: int, h: int):
    """H = (n/h) Z_n of order h. Returns (q, reps, contents) with the part of A
    in coset c equal to c + q * contents[c] (contents in Z_h)."""
    q = n // h
    cos: Dict[int, List[int]] = {}
    for a in A:
        cos.setdefault(a % q, []).append(((a - a % q) // q) % h)
    reps = sorted(cos)
    return q, reps, {c: sorted(cos[c]) for c in reps}


def coset_flat_condition(A, n, h, u, svec) -> bool:
    """L9 strict criterion: with U_c the coset contents (in Z[Z_h]), sigma = (y -> y^u):
       sum_c sigma(U_c U_c~) = sum_c U_c U_c~,   and for c != d:
       y^{s_c - s_d} sigma(U_c U_d~) = U_c U_d~ ."""
    q, reps, U = coset_decomposition(A, n, h)
    vec = {c: ind(U[c], h) for c in reps}
    sig = lambda f: np.bincount([(u * g) % h for g in range(h)], weights=f, minlength=h).astype(np.int64)
    diag = sum(conv(vec[c], rev(vec[c])) for c in reps)
    if not np.array_equal(sig(diag), diag):
        return False
    for (i, c), (j, d) in product(enumerate(reps), repeat=2):
        if c == d:
            continue
        P = conv(vec[c], rev(vec[d]))
        if not np.array_equal(shift(sig(P), svec[i] - svec[j]), P):
            return False
    return True


def coset_automorphism_moves(A: Sequence[int], n: int, max_candidates: int = 200000,
                             strict_only: bool = False) -> Dict[PCSet, list]:
    """L9/L9': for H of order h, u a unit mod h and shifts s_c in Z_h (one per
    occupied coset, s_first = 0), B = union_c (c + q*(s_c + u*U_c)).
    B is returned iff it is homometric to A (L9' exact criterion, checked here by
    comparing ICVs, which L9' proves equivalent), tagged 'coset-flat' when the
    strict L9 criterion also holds."""
    out: Dict = {}
    k = len(A)
    Aicv = np.array(list(icv_fast(A, n)) + [0])
    for h in range(2, n + 1):
        if n % h:
            continue
        q, reps, U = coset_decomposition(A, n, h)
        C = len(reps)
        if h ** (C - 1) > max_candidates:
            continue
        tuples = list(product(range(h), repeat=C - 1))
        S = np.zeros((len(tuples), C), dtype=np.int64)
        if C > 1:
            S[:, 1:] = np.array(tuples, dtype=np.int64)
        for u in range(1, h):
            if gcd(u, h) != 1:
                continue
            cols = []
            for i, c in enumerate(reps):
                for x in U[c]:
                    cols.append(c + q * ((S[:, i] + u * x) % h))
            X = np.stack(cols, axis=1)
            ok = np.all(_icv_batch(X, n) == Aicv, axis=1)
            for r in np.nonzero(ok)[0]:
                svec = tuple(int(v) for v in S[r])
                if u == 1 and not any(svec):
                    continue
                flat = coset_flat_condition(A, n, h, u, svec)
                if strict_only and not flat:
                    continue
                _add(out, X[r].tolist(), n, k, ("coset-flat" if flat else "coset-exact", h, u, svec))
    return out



# ------------------------------------------------------------ L10 Cayley unit of a 3-term P
def three_term_vanishes(supp: Sequence[int], signs: Sequence[int], n: int) -> bool:
    """Exact test whether P^(k) = 0 for some k, where P = sum signs[j] x^supp[j]
    (three terms, signs +-1).  By Lemma L10a (notes): a vanishing sum of three unit
    complex numbers with coefficients +-1 is, after moving the minus signs across,
    either alpha+beta+gamma = 0 with {alpha,beta,gamma} a rotated set of cube roots
    of unity, or alpha+beta = gamma with alpha/gamma, beta/gamma = exp(+-i pi/3)."""
    if sum(1 for s in signs if s < 0) >= 2:
        signs = [-s for s in signs]
    for k in range(n):
        e = [(k * a) % n for a in supp]
        if all(s > 0 for s in signs):
            if n % 3 == 0:
                d = sorted(((e[1] - e[0]) % n, (e[2] - e[0]) % n))
                if d == [n // 3, 2 * n // 3]:
                    return True
        else:
            j = [i for i in range(3) if signs[i] < 0][0]
            others = [i for i in range(3) if i != j]
            if n % 6 == 0:
                d = sorted(((e[i] - e[j]) % n for i in others))
                if d == [n // 6, 5 * n // 6]:
                    return True
    return False


def cayley_moves(A: Sequence[int], n: int,
                 patterns=((1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1))) -> Dict[PCSet, list]:
    """L10: P = 3-term element of Z[Z_n] (coefficients +-1) with P^(k) != 0 for all k.
    If B := 1_A * P~ * P^{-1} is a 0/1 vector, then B is homometric to A.
    Certificate checked EXACTLY: the integer identity B*P = A*P~ plus the exact
    non-vanishing test above.  (Equivalently A = P*Q, B = P~*Q with Q = A*P^{-1}
    a RATIONAL cofactor: a Rosenblatt-Seymour flip with rational cofactor.)"""
    out: Dict = {}
    k = len(A)
    a = ind(A, n)
    Ah = np.fft.fft(a)
    for x, y in combinations(range(1, n), 2):
        supp = (0, x, y)
        for sg in patterns:
            p = np.zeros(n, dtype=np.int64)
            for pos, c in zip(supp, sg):
                p[pos] += c
            Ph = np.fft.fft(p)
            if np.min(np.abs(Ph)) < 1e-9:
                continue                      # (numerically) singular: skip
            b = np.real(np.fft.ifft(Ah * np.conj(Ph) / Ph))
            br = np.round(b).astype(np.int64)
            if np.max(np.abs(b - br)) > 1e-6 or not np.all((br == 0) | (br == 1)):
                continue
            if not np.array_equal(conv(br, p), conv(a, rev(p))):
                continue
            if three_term_vanishes(supp, sg, n):
                continue
            _add(out, [int(g) for g in np.nonzero(br)[0]], n, k, ("cayley", supp, sg))
    return out

# ------------------------------------------------------------ L1 general block motion
def block_exact_moves(A: Sequence[int], n: int) -> Dict[PCSet, list]:
    """L1 (iff criterion for the shape): B = U + g(W), g a rigid motion of Z_n,
    homometric iff U W~ + W U~ = U g(W)~ + g(W) U~.  Sound but weakly explanatory."""
    out: Dict = {}
    k = len(A)
    for U, W in _splits(A):
        u, w = ind(U, n), ind(W, n)
        C = conv(u, rev(w)) + conv(w, rev(u))
        for s in range(n):
            for sg in (1, -1):
                if s == 0 and sg == 1:
                    continue
                gW = [(sg * x + s) % n for x in W]
                g = ind(gW, n)
                if np.array_equal(conv(u, rev(g)) + conv(g, rev(u)), C):
                    _add(out, U + gW, n, k, ("block-exact", tuple(U), tuple(W), sg, s))
    return out


# ------------------------------------------------------------ old moves
def old_moves(A: Sequence[int], n: int) -> Dict[PCSet, list]:
    out: Dict = {}
    k = len(A)
    if 2 * k == n:
        _add(out, complement(A, n), n, k, ("babbitt",))
    for B in direct_sum_flips(A, n):
        _add(out, B, n, k, ("dsflip",))
    return out


STRUCTURAL = {
    "translate": translation_moves,
    "swap": swap_moves,
    "halfturn": halfturn_moves,
    "reflect": reflection_moves,
    "unit": unit_moves,
    "halfcoset": halfcoset_moves,
    "signflip": signflip_moves,
    "cayley": cayley_moves,
}


def all_moves(A: Sequence[int], n: int, include=("old", "structural", "coset"),
              ) -> Dict[PCSet, list]:
    """Union of partners, keyed by DIHEDRAL CANONICAL form; values = certificates."""
    res: Dict[PCSet, list] = {}

    def merge(d):
        for B, certs in d.items():
            res.setdefault(dihedral_canon(B, n), []).extend(certs)

    if "old" in include:
        merge(old_moves(A, n))
    if "structural" in include:
        for f in STRUCTURAL.values():
            try:
                merge(f(A, n))
            except ValueError:
                pass
    if "coset" in include:
        merge(coset_automorphism_moves(A, n))
    if "block" in include:
        merge(block_exact_moves(A, n))
    return res
