"""
validate_literature.py -- reproduce published classifications against brute force.

Erickson & Jones, "Homometric subsets of Z_n with cardinality 5: classification
and enumeration", arXiv:2412.08997 (read: v2, 13 Jun 2025; v3 exists, 2026 -- the
agent must re-check against v3). Theorem 4.1 (types A-G) and Theorem 4.4
(generating function) are encoded below and compared with src/homometry.py.

usage: python src/validate_literature.py --nmax 40
"""
import argparse, os, sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(__file__))
from homometry import bracelets, icv, dihedral_canon

def brute_k5(n):
    fam = defaultdict(list)
    for s in bracelets(n, 5):
        fam[icv(s, n)].append(s)
    return sorted(sorted(c) for c in fam.values() if len(c) > 1)

def ej_types(n, g_scale_m=True):
    """Theorem 4.1 of Erickson-Jones, transcribed from v2.
    g_scale_m: Type G as printed uses 8i, 4i; scaling by m (8im, 4im) is what the
    continuous version (3.5) implies. Both are tested."""
    out = []
    def add(t, sets):
        cl = [dihedral_canon([x % n for x in s], n) for s in sets]
        if all(len(set(x % n for x in s)) == 5 for s in sets):
            out.append((t, cl))
    if n % 2 == 0:
        m = n // 2
        for i in range(1, m):
            for j in range(1, m):
                if not (2 * i < m and 2 * j < m and i != j): continue
                if 3 * j == m and 6 * i != m: continue
                add("A", [[0, i, i + j, m + i - j, m], [0, m + i, i + j, m + i - j, m]])
    if n % 5 == 0:
        m = n // 5
        for i in range(1, 5 * m // 2 + 1):
            if 2 * i in (m, 2 * m, 3 * m, 4 * m): continue
            add("B", [[0, i, m, 2 * m, 2 * m + i], [0, i, m, m + i, 3 * m]])
    if n % 6 == 0:
        m = n // 6
        for i in range(1, m // 2 + 1):
            add("C", [[0, m + i, 2 * m, 2 * m + i, 4 * m], [0, 2 * m, 2 * m + i, 3 * m + i, 4 * m]])
        for i in range(1, 3 * m):
            if not 2 * i < 3 * m or 2 * i == m or i == m: continue
            add("D", [[i, m - i, 2 * m, 2 * m + i, 3 * m], [0, i, m - i, 2 * m + i, 5 * m]])
        for i in range(1, m):
            if not 2 * i < m: continue
            add("E", [[0, i, m + i, 2 * m + i, 3 * m], [0, i, m, 2 * m, 3 * m + i], [0, m - i, m, 2 * m, 4 * m - i]])
    if n % 8 == 0:
        m = n // 8
        for i in range(1, 4 * m):
            if i in (m, 2 * m, 3 * m): continue
            add("F", [[0, i, m, 2 * m + i, 4 * m], [0, i, m + i, 2 * m, 4 * m + i]])
    if n % 20 == 0:
        m = n // 20
        for i in range(1, 5):
            k = i * m if g_scale_m else i
            add("G", [[0, 5 * m, 8 * k, 15 * m + 4 * k, 5 * m - 4 * k], [0, 5 * m, 4 * k, 15 * m + 8 * k, 15 * m - 4 * k]])
    return out

def ej_gf_coeffs(N):
    """Coefficients h_n of Theorem 4.4 via power-series arithmetic."""
    def series(num, den_factors):
        s = [0] * (N + 1)
        for e, c in num: 
            if e <= N: s[e] += c
        for d in den_factors:          # divide by (1 - x^d)
            for k in range(d, N + 1):
                s[k] += s[k - d]
        return s
    parts = [series([(10, 2)], [2, 4, 4]), series([(10, 1), (15, 4)], [5, 10]),
             series([(12, 1), (18, 1)], [6, 12]), series([(16, 4)], [8, 8]),
             series([(20, 4)], [20])]
    return [sum(p[k] for p in parts) for k in range(N + 1)]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--nmax", type=int, default=30)
    a = ap.parse_args()
    h = ej_gf_coeffs(a.nmax)
    ok_all = True
    for n in range(5, a.nmax + 1):
        brute = brute_k5(n)
        for scale in (True, False):
            typed = ej_types(n, scale)
            fams = sorted(sorted(cl) for _, cl in typed)
            fams_dedup = sorted({tuple(f) for f in fams})
            same = [list(f) for f in fams_dedup] == brute
            if scale or n % 20 == 0:
                tag = "G*m" if scale else "G as printed"
                print(f"n={n:3d} brute={len(brute):4d} gf={h[n]:4d} typed={len(fams):4d} "
                      f"typed==brute:{same} dup-free:{len(fams)==len(fams_dedup)} [{tag}]")
            if scale:
                ok_all &= same and len(brute) == h[n] and len(fams) == len(fams_dedup)
    print("ALL CONSISTENT (with G scaled by m)" if ok_all else "MISMATCH FOUND -- investigate")

if __name__ == "__main__":
    main()
