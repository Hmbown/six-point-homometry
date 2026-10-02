"""Independent bounded adversarial controls for the general matching note.

The rank, determinant, maximal-minor gcd and direct-tree controls below use
only the standard library and do not import an author implementation.
SymPy's separate Smith decomposition is used only for the final change-of-
variables checks; its full identity and both unimodular determinants are
verified. This is finite evidence, not a substitute for the written proof.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from math import gcd
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1] / "src"))


def determinant(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    result = Fraction(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return 0
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            result = -result
        value = a[j][j]
        result *= value
        for i in range(j + 1, len(a)):
            multiplier = a[i][j] / value
            for h in range(j + 1, len(a)):
                a[i][h] -= multiplier * a[j][h]
            a[i][j] = 0
    assert result.denominator == 1
    return int(result)


def rank(matrix):
    if not matrix:
        return 0
    a = [[Fraction(x) for x in row] for row in matrix]
    r = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        for i in range(r + 1, len(a)):
            multiplier = a[i][j] / a[r][j]
            for h in range(j, len(a[0])):
                a[i][h] -= multiplier * a[r][h]
        r += 1
        if r == len(a):
            break
    return r


def minor(matrix, rows, columns):
    return [[matrix[i][j] for j in columns] for i in rows]


def matching_matrix(k, permutation, signs):
    edges = tuple(combinations(range(k), 2))
    incidence = []
    for i, j in edges:
        incidence.append([int(v == j) - int(v == i) for v in range(1, k)])
    return [incidence[e] + [-signs[e] * x for x in incidence[permutation[e]]]
            for e in range(len(edges))]


def torsion_order(matrix):
    r = rank(matrix)
    if not r:
        return r, 1
    result = 0
    for rows in combinations(range(len(matrix)), r):
        for columns in combinations(range(len(matrix[0])), r):
            result = gcd(result, abs(determinant(minor(matrix, rows, columns))))
    assert result > 0
    return r, result


def tree_count(k, edges):
    count = 0
    for selected in combinations(edges, k - 1):
        components = [{v} for v in range(k)]
        for a, b in selected:
            ia = next(i for i, part in enumerate(components) if a in part)
            ib = next(i for i, part in enumerate(components) if b in part)
            if ia == ib:
                break
            components[ia] |= components[ib]
            del components[ib]
        else:
            assert len(components) == 1
            count += 1
    return count


def chosen_minor_tree_bound(k, matrix):
    r, t = torsion_order(matrix)
    columns = list(range(k - 1))
    assert rank(minor(matrix, range(len(matrix)), columns)) == k - 1
    for j in range(k - 1, 2 * k - 2):
        extended = columns + [j]
        if rank(minor(matrix, range(len(matrix)), extended)) > len(columns):
            columns.append(j)
    assert len(columns) == r
    for rows in combinations(range(len(matrix)), r):
        det = abs(determinant(minor(matrix, rows, columns)))
        if det:
            break
    else:
        raise AssertionError("no nonzero full-first-block minor")
    edges = tuple(combinations(range(k), 2))
    trees = tree_count(k, [edges[i] for i in rows])
    assert det % t == 0 and 1 <= t <= det <= trees
    assert trees * k * (k - 1) ** (k - 1) <= (2 * r) ** (k - 1)
    assert t * k <= 4 ** (k - 1)
    if r == k - 1:
        assert trees == det == t == 1
    return r, t


def test_incidence_minors():
    for k in range(2, 5):
        edges = tuple(combinations(range(k), 2))
        b = [[int(v == j) - int(v == i) for v in range(1, k)]
             for i, j in edges]
        for size in range(k):
            for rows in combinations(range(len(edges)), size):
                for columns in combinations(range(k - 1), size):
                    assert determinant(minor(b, rows, columns)) in (-1, 0, 1)


def test_all_triangle_presentations():
    observed = Counter()
    for permutation in permutations(range(3)):
        for signs in product((-1, 1), repeat=3):
            matrix = matching_matrix(3, permutation, signs)
            pair = chosen_minor_tree_bound(3, matrix)
            observed[pair] += 1
    assert set(observed) == {(2, 1), (3, 2)} and sum(observed.values()) == 48
    for sign in (-1, 1):
        assert chosen_minor_tree_bound(2, matching_matrix(2, (0,), (sign,))) == (1, 1)
    print("triangle rank/torsion distribution", dict(sorted(observed.items())))


def test_arbitrary_rank_samples():
    rng = random.Random(20261001)
    observed = set()
    for k, samples in ((4, 40), (5, 8)):
        m = k * (k - 1) // 2
        for index in range(samples):
            permutation = list(range(m))
            if index:
                rng.shuffle(permutation)
            signs = tuple(1 if index == 0 else rng.choice((-1, 1)) for _ in range(m))
            observed.add((k, *chosen_minor_tree_bound(k, matching_matrix(k, permutation, signs))))
    # The structured C4 example forces positive free rank and nontrivial torsion.
    observed.add((4, *chosen_minor_tree_bound(4, c4_matrix())))
    assert (4, 3, 1) in observed and (4, 5, 4) in observed
    assert {entry[1] for entry in observed if entry[0] == 4} >= {3, 5, 6}
    print("sample cardinality/rank/torsion triples", sorted(observed))


def add(a, b, moduli):
    return tuple((x + y) % n for x, y, n in zip(a, b, moduli))


def negate(a, moduli):
    return tuple((-x) % n for x, n in zip(a, moduli))


def correlation(points, moduli):
    return Counter(add(b, negate(a, moduli), moduli) for a in points for b in points)


def canonical_ti(points, moduli):
    return min(tuple(sorted(add(negate(origin, moduli), x, moduli) for x in reflected))
               for reflected in (points, tuple(negate(x, moduli) for x in points))
               for origin in reflected)


def test_low_k_abelian_and_coefficient_scope():
    checked = 0
    for moduli in ((4,), (5,), (8,), (2, 2), (2, 4), (2, 2, 2), (3, 3)):
        group = tuple(product(*(range(n) for n in moduli)))
        for k in (1, 2, 3):
            fibres = {}
            for points in combinations(group, k):
                signature = tuple(sorted(correlation(points, moduli).items()))
                canonical = canonical_ti(points, moduli)
                assert signature not in fibres or fibres[signature] == canonical
                fibres[signature] = canonical
                checked += 1
    moduli = (2, 2, 2)
    a = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0))
    b = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
    ca, cb = correlation(a, moduli), correlation(b, moduli)
    assert ca != cb
    assert all(value % 2 == 0 for value in ca.values())
    assert all(value % 2 == 0 for value in cb.values())
    print("low-k binary abelian examples checked", checked)


def c4_matrix():
    # A01 -> B23, A02 -> B01, A03 -> B02, A12 -> B13,
    # A13 -> -B03, A23 -> B12, in lexicographic edge order.
    return matching_matrix(4, (5, 0, 1, 4, 2, 3), (1, 1, 1, 1, -1, 1))


def test_positive_rank_counterexample():
    # Work exactly in Z x C4; the free coordinate is never reduced.
    a = ((0, 0), (1, 0), (1, 1), (0, 2))
    b = ((0, 0), (1, 1), (0, 2), (1, 2))
    def directed(points):
        return Counter((y[0] - x[0], (y[1] - x[1]) % 4) for x in points for y in points)
    assert directed(a) == directed(b)
    for sign in (-1, 1):
        for origin in a:
            transformed = {(sign * (x[0] - origin[0]), sign * (x[1] - origin[1]) % 4) for x in a}
            assert transformed != set(b)
    assert sorted(x[0] for x in a) == sorted(x[0] for x in b) == [0, 0, 1, 1]
    assert torsion_order(c4_matrix()) == (5, 4)
    aa, bb = tuple((x[0] + 3 * x[1]) % 12 for x in a), tuple((x[0] + 3 * x[1]) % 12 for x in b)
    assert correlation(tuple((x,) for x in aa), (12,)) == correlation(tuple((x,) for x in bb), (12,))
    assert canonical_ti(tuple((x,) for x in aa), (12,)) != canonical_ti(tuple((x,) for x in bb), (12,))
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    from homometry import icv, dihedral_canon
    assert icv(aa, 12) == icv(bb, 12)
    assert dihedral_canon(aa, 12) != dihedral_canon(bb, 12)


def test_smith_lift_direction():
    from sympy import Matrix, ZZ
    from sympy.polys.matrices import DomainMatrix
    from sympy.polys.matrices.normalforms import smith_normal_decomp
    matrix = Matrix(c4_matrix())
    domain = DomainMatrix.from_Matrix(matrix).convert_to(ZZ)
    dd, pp, qq = smith_normal_decomp(domain)
    d, p, q = (value.to_Matrix() for value in (dd, pp, qq))
    assert p * matrix * q == d
    assert abs(p.det()) == abs(q.det()) == 1
    r = 5
    assert abs(d[4, 4]) == 4 and all(abs(d[i, i]) == 1 for i in range(4))
    checked = 0
    for n in (4, 8, 12, 13):
        for free in range(n):
            for torsion in range(n):
                if 4 * torsion % n:
                    continue
                v = Matrix([free, free + torsion, 2 * torsion,
                            free + torsion, 2 * torsion, free + 2 * torsion]) % n
                assert matrix * v % n == Matrix.zeros(6, 1)
                z = q.inv() * v % n
                liftable = all(z[i] == 0 for i in range(r))
                assert liftable == (torsion == 0)
                if gcd(n, 4) == 1:
                    assert liftable
                if liftable:
                    w = q * Matrix([0] * r + [z[r]])
                    assert matrix * w == Matrix.zeros(6, 1) and w % n == v
                checked += 1
    # gcd(n,t)>1 allows a successful exact lift when the realized torsion is zero.
    assert gcd(12, 4) > 1
    print("Smith full-identity modular lift cases checked", checked)


def main():
    started = time.monotonic()
    tests = (test_incidence_minors, test_all_triangle_presentations,
             test_arbitrary_rank_samples, test_low_k_abelian_and_coefficient_scope,
             test_positive_rank_counterexample, test_smith_lift_direction)
    for test in tests:
        test()
        print("PASS", test.__name__, flush=True)
    print("passed", len(tests), "groups; seconds", time.monotonic() - started)


if __name__ == "__main__":
    main()
