"""Independent directed-correlation and rational certificate controls."""
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
import random
import sys

from sympy import Matrix, Rational, factor, simplify, sqrt, symbols

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from homometry import icv, dihedral_canon
from weighted_six_incidence import (SEEDS, benchmark_real_branches,
                                   benchmark_elimination, benchmark_fourier_certificate, build_certificates,
                                   incidence_data, weighted_coefficients)


def directed(support, n, weights):
    x = [0] * n
    for p, w in zip(support, weights):
        x[p] = w
    return [sum(x[t] * x[(t+d) % n] for t in range(n)) for d in range(n)]


def folded(support, n, weights):
    c = directed(support, n, weights)
    return [c[0]] + [c[d] / 2 if 2*d == n else c[d] for d in range(1, n//2+1)]


def decode(m):
    return [[F(x) for x in row] for row in m]


def pivots(m):
    a = [list(map(F, row)) for row in m]
    row = 0
    if not a:
        return []
    cols = []
    for c in range(len(a[0])):
        p = next((p for p in range(row, len(a)) if a[p][c]), None)
        if p is None:
            continue
        a[row], a[p] = a[p], a[row]
        scale = a[row][c]
        a[row] = [x/scale for x in a[row]]
        for p in range(len(a)):
            if p != row and a[p][c]:
                q = a[p][c]
                a[p] = [x-q*y for x, y in zip(a[p], a[row])]
        cols.append(c)
        row += 1
        if row == len(a):
            break
    return cols


def determinant(m):
    a = [list(map(F, row)) for row in m]
    value = F(1)
    for col in range(len(a)):
        pivot = next((p for p in range(col, len(a)) if a[p][col]), None)
        if pivot is None:
            return F(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            value = -value
        value *= a[col][col]
        for row in range(col+1, len(a)):
            q = a[row][col] / a[col][col]
            a[row] = [x-q*y for x, y in zip(a[row], a[col])]
    return value


def independent_jacobian(n, a, b):
    # Polarization at ones, evaluated through full directed autocorrelation.
    columns = []
    for index in range(12):
        u, v = [F(1)] * 6, [F(1)] * 6
        u0, v0 = [F(0)] * 6, [F(0)] * 6
        if index < 6:
            u[index] += 1
            u0[index] = 1
        else:
            v[index-6] += 1
            v0[index-6] = 1
        columns.append([p-q-r+s for p, q, r, s in zip(
            folded(a, n, u), folded(b, n, v), folded(a, n, u0), folded(b, n, v0))])
    return list(map(list, zip(*columns)))


def test_reference_and_random_weights():
    rng = random.Random(20261001)
    for n, a, b in SEEDS:
        assert icv(a, n) == icv(b, n)
        assert dihedral_canon(a, n) != dihedral_canon(b, n)
        assert tuple(weighted_coefficients(a, n, [1]*6)) == (6,) + icv(a, n)
        for s in (a, b):
            for _ in range(8):
                w = [F(rng.randrange(-5, 6), rng.randrange(1, 5)) for _ in s]
                expected = folded(s, n, w)
                actual = list(weighted_coefficients(s, n, w))
                assert all(F(x) == y for x, y in zip(actual, expected))
    print("PASS reference controls and 208 rational weighted correlation comparisons")


def test_saved_certificates():
    path = ROOT / "results/2026-10-01-weighted-six-incidence/certificates.json"
    saved = json.loads(path.read_text()) if path.exists() else build_certificates()
    for cert, (n, a, b) in zip(saved["seeds"], SEEDS):
        j = decode(cert["jacobian"])
        assert j == independent_jacobian(n, a, b)
        assert len(pivots(j)) == cert["rank_incidence"]
        assert len(pivots([row[:6] for row in j])) == cert["rank_a"]
        assert len(pivots([row[6:] for row in j])) == cert["rank_b"]
        minor = cert["rank_minor"]
        m = [[j[i][k] for k in minor["columns"]] for i in minor["rows"]]
        assert determinant(m) == F(minor["determinant"]) != 0
        t = decode(cert["normalized_tangent"])
        dim = cert["normalized_tangent_dimension"]
        assert len(pivots(t)) == dim == 12-len(pivots(j+[[F(1)]*12]))
        for col in range(dim):
            v = [row[col] for row in t]
            assert sum(v) == 0
            assert all(sum(x*y for x, y in zip(row, v)) == 0 for row in j)
        assert len(cert["left_null"]) == len(j)-len(pivots(j))
        for ell0, h0 in zip(cert["left_null"], cert["quadratic_obstructions"]):
            ell = [row[0] for row in decode(ell0)]
            assert all(sum(ell[d]*j[d][col] for d in range(len(j))) == 0 for col in range(12))
            h = decode(h0)
            # Reconstruct each quadratic form by exact polarization in tangent
            # coordinates, using only the independent directed correlation.
            def q(v):
                f = [x-y for x, y in zip(folded(a, n, v[:6]), folded(b, n, v[6:]))]
                return sum(x*y for x, y in zip(ell, f))
            vectors = [[row[col] for row in t] for col in range(dim)]
            for i in range(dim):
                assert h[i][i] == q(vectors[i])
                for k in range(i):
                    both = [x+y for x, y in zip(vectors[i], vectors[k])]
                    assert h[i][k] == (q(both)-q(vectors[i])-q(vectors[k]))/2
    print("PASS 13 independently reconstructed Jacobian/rank/tangent/quadratic certificates")


def test_benchmark_global_elimination_and_branches():
    n, a, b = SEEDS[4]
    for branch in benchmark_real_branches():
        left, right = directed(a, n, branch["a"]), directed(b, n, branch["b"])
        assert all(simplify(x-y) == 0 for x, y in zip(left, right))
    r = symbols("r", real=True)
    k2 = (2*r*r+r+2)/5
    tk = (3*r*r-r+3)/5
    # Independent clearing of the norm equation, rather than reading the
    # production symbolic factorization as a certificate.
    cleared = factor(5*(2*r*r+r+2)*(3*(r*r+1)-2*r*r/k2-3*k2-tk*tk/k2))
    assert cleared == 9*(r-1)**2*(r*r+3*r+1)
    assert list(Matrix([9, 9, -36, 9, 9])) == benchmark_elimination()["eliminant_coefficients"]
    print("PASS all three exact real benchmark branches and independent norm eliminant")


def test_persistence_and_critical_same_support():
    n, a, b = SEEDS[6]
    va = [1, -1, 1, -1, -1, 1]
    vb = [-1, 1, -1, -1, 1, 1]
    for t in [F(-2), F(-1, 3), F(0), F(1, 5), F(3)]:
        aa, bb = [1+t*x for x in va], [1+t*x for x in vb]
        assert directed(a, n, aa) == directed(b, n, bb)
    n, a, _ = SEEDS[4]
    v = [1, -1, 1, -1, -1, 1]
    for t in [F(1, 7), F(2, 3)]:
        aa, bb = [1+t*x for x in v], [1-t*x for x in v]
        assert directed(a, n, aa) == directed(a, n, bb)
    stabilizer = [(sg, shift) for sg in [1, -1] for shift in range(n)
                  if {(sg*x+shift) % n for x in a} == set(a)]
    assert stabilizer == [(1, 0)]
    cert = benchmark_fourier_certificate()
    u, v = cert["u"], cert["v"]
    value = [0] * 36
    for i, c in enumerate(u):
        for position in a:
            value[i+position] += c
    for i, c in enumerate(v):
        value[i+21] += c
        value[i] -= c
    assert value == [cert["constant"]] + [0]*35
    # The R2 residual quadratic is indefinite, hence has two distinct real
    # null directions; the note uses this plus implicit elimination.
    d = incidence_data(*SEEDS[1])
    h = d["projected"][0]
    assert d["tangent"].cols == 2 and h.det() == Rational(-621, 25)
    print("PASS R7 persistence, nontrivial positive same-support R5 ambiguity, no-Fourier-zero Bezout and R2 saddle")


if __name__ == "__main__":
    test_reference_and_random_weights()
    test_saved_certificates()
    test_benchmark_global_elimination_and_branches()
    test_persistence_and_critical_same_support()
