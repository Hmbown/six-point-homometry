"""
homometry.py -- core, dependency-light library for the Homometry Program.

Conventions
-----------
* A pitch-class set in n-EDO is a tuple of distinct ints in range(n).
* "Canonical form" = lexicographically smallest sorted tuple in the orbit
  under the dihedral group (T_n / I). Translation-only canon is also given.
* Two sets are HOMOMETRIC (Z-related, if not T_n/I-equivalent) iff they have
  the same interval-class vector (ICV). The ICV is computed with exact integer
  arithmetic; the DFT is only used as an independent floating-point cross-check.

Everything here is deliberately simple and readable, so that it can serve as
the REFERENCE implementation. Faster implementations (C, numba, bitsets) must
be validated against this file before their output is trusted.
"""
from __future__ import annotations

import cmath
from collections import Counter, defaultdict
from itertools import combinations
from typing import Dict, Iterable, Iterator, List, Sequence, Tuple

PCSet = Tuple[int, ...]


# ----------------------------------------------------------------- basics
def normalize(s: Iterable[int], n: int) -> PCSet:
    return tuple(sorted({x % n for x in s}))


def icv(s: Sequence[int], n: int) -> Tuple[int, ...]:
    """Interval-class vector, length floor(n/2). Entry d-1 counts pairs at
    cyclic distance d. (For even n the last entry is the 'tritone' class.)"""
    v = [0] * (n // 2)
    for a, b in combinations(s, 2):
        d = (a - b) % n
        d = min(d, n - d)
        v[d - 1] += 1
    return tuple(v)


def dihedral_canon(s: Sequence[int], n: int) -> PCSet:
    best = None
    for t in range(n):
        for sg in (1, -1):
            x = tuple(sorted((sg * a + t) % n for a in s))
            if best is None or x < best:
                best = x
    return best


def translation_canon(s: Sequence[int], n: int) -> PCSet:
    best = None
    for t in range(n):
        x = tuple(sorted((a + t) % n for a in s))
        if best is None or x < best:
            best = x
    return best


def complement(s: Sequence[int], n: int) -> PCSet:
    ss = set(s)
    return tuple(x for x in range(n) if x not in ss)


def invert(s: Sequence[int], n: int) -> PCSet:
    return normalize((-a for a in s), n)


# --------------------------------------------------------- enumeration
def bracelets(n: int, k: int) -> Iterator[PCSet]:
    """All T_n/I classes of k-subsets of Z_n (canonical reps).
    Reference-speed: O(C(n-1,k-1) * n * k)."""
    if k == 0:
        yield ()
        return
    for rest in combinations(range(1, n), k - 1):
        s = (0,) + rest
        if dihedral_canon(s, n) == s:
            yield s


def z_families(n: int, sizes: Iterable[int] | None = None) -> Dict[Tuple[int, ...], List[PCSet]]:
    """Map ICV -> list of canonical reps, keeping only ICVs shared by >= 2
    distinct T_n/I classes (i.e. genuine Z-families)."""
    if sizes is None:
        sizes = range(2, n - 1)
    fam: Dict[Tuple[int, ...], List[PCSet]] = defaultdict(list)
    for k in sizes:
        for s in bracelets(n, k):
            fam[icv(s, n)].append(s)
    return {v: c for v, c in fam.items() if len(c) > 1}


# ------------------------------------------------------ Fourier view
def dft(s: Sequence[int], n: int) -> List[complex]:
    return [sum(cmath.exp(-2j * cmath.pi * k * a / n) for a in s) for k in range(n)]


def dft_magnitudes(s: Sequence[int], n: int, digits: int = 9) -> Tuple[float, ...]:
    return tuple(round(abs(z), digits) for z in dft(s, n)[: n // 2 + 1])


# ----------------------------------------------- generating mechanisms
def _divisors(k: int) -> List[int]:
    return [d for d in range(2, k) if k % d == 0]


def direct_sum_flips(s: Sequence[int], n: int) -> set:
    """All partners obtained by the 0/1 direct-sum flip:
        if  S = B (+) C  in Z_n  (all |B||C| sums distinct),
        then B (+) (-C) is homometric to S.
    Returns the set of canonical forms of such partners (possibly including S's
    own class when the flip is trivial). This is ONLY the 0/1-factor case of the
    Rosenblatt-Seymour mechanism; factors with other integer coefficients (and
    general 'spectral units') are NOT covered -- that gap is a research target."""
    k = len(s)
    out = set()
    for t in s:
        S = sorted((a - t) % n for a in s)  # contains 0
        Sset = set(S)
        others = [x for x in S if x != 0]
        for d in _divisors(k):
            m = k // d
            for brest in combinations(others, d - 1):
                B = (0,) + brest
                for crest in combinations(others, m - 1):
                    C = (0,) + crest
                    sums = {(b + c) % n for b in B for c in C}
                    if len(sums) != k or sums != Sset:
                        continue
                    flip = {(b - c) % n for b in B for c in C}
                    if len(flip) == k:
                        out.add(dihedral_canon(flip, n))
    return out


def mechanism_edges(A: PCSet, B: PCSet, n: int) -> List[str]:
    """Which known mechanisms directly connect canonical classes A and B?"""
    why = []
    k = len(A)
    if 2 * k == n and dihedral_canon(complement(A, n), n) == B:
        why.append("babbitt-complement")
    if B in direct_sum_flips(A, n) or A in direct_sum_flips(B, n):
        why.append("direct-sum-flip")
    cA = dihedral_canon(complement(A, n), n)
    cB = dihedral_canon(complement(B, n), n)
    if 2 * k != n and (cB in direct_sum_flips(cA, n) or cA in direct_sum_flips(cB, n)):
        why.append("complement-of-flip")
    return why


def explain_family(members: List[PCSet], n: int) -> Dict:
    """Build the graph whose edges are known mechanisms; report whether the
    family is connected (= fully 'explained' by known mechanisms)."""
    idx = {m: i for i, m in enumerate(members)}
    parent = list(range(len(members)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    edges = []
    for a, b in combinations(members, 2):
        w = mechanism_edges(a, b, n)
        if w:
            edges.append((a, b, w))
            parent[find(idx[a])] = find(idx[b])
    comps = len({find(i) for i in range(len(members))})
    return {"size": len(members), "components": comps, "explained": comps == 1, "edges": edges}


# --------------------------------------------- higher-order content
def k_deck(s: Sequence[int], n: int, k: int) -> Counter:
    """Multiset of translation classes of k-subsets of s."""
    return Counter(translation_canon(sub, n) for sub in combinations(s, k))


def same_k_deck_up_to_inversion(A: Sequence[int], B: Sequence[int], n: int, k: int) -> bool:
    dA = k_deck(A, n, k)
    return dA == k_deck(B, n, k) or dA == k_deck(invert(B, n), n, k)


def higher_order_families(n: int, k: int, sizes: Iterable[int] | None = None) -> List[List[PCSet]]:
    """Groups of distinct T_n/I classes sharing the same k-deck (up to
    inversion). k=2 reproduces the ordinary Z-relation."""
    if sizes is None:
        sizes = range(k + 1, n - 1)
    groups: List[List[PCSet]] = []
    for size in sizes:
        buckets: Dict[Tuple, List[PCSet]] = defaultdict(list)
        for s in bracelets(n, size):
            d1 = tuple(sorted(k_deck(s, n, k).items()))
            d2 = tuple(sorted(k_deck(invert(s, n), n, k).items()))
            buckets[min(d1, d2)].append(s)
        groups += [g for g in buckets.values() if len(g) > 1]
    return groups
