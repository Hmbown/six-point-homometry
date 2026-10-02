"""Independent exact attacks on the six-note shadow and dyad proofs.

No functions from six_shadow.py or six_explore.py are used. Signed matchings
are enumerated edge by edge from direct modular equations. Matrix checks use
integer Bareiss determinants and Fraction elimination, not SymPy. The trusted
homometry reference is used only for additional ICV checks on small examples.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from math import comb, gcd, prod
from pathlib import Path
import hashlib
import json
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from homometry import icv as reference_icv

EDGES = tuple(combinations(range(6), 2))


def determinant(matrix):
    """Fraction-free Bareiss elimination, including row swaps."""
    a = [list(map(int, row)) for row in matrix]
    size = len(a)
    assert all(len(row) == size for row in a)
    if not size:
        return 1
    sign, previous = 1, 1
    for k in range(size - 1):
        pivot_row = next((i for i in range(k, size) if a[i][k]), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, size):
            for j in range(k + 1, size):
                numerator = pivot * a[i][j] - a[i][k] * a[k][j]
                quotient, remainder = divmod(numerator, previous)
                assert remainder == 0
                a[i][j] = quotient
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]


def rational_pivots(matrix):
    """Exact row elimination; returns pivot columns."""
    a = [list(map(Fraction, row)) for row in matrix]
    if not a:
        return ()
    row, columns = 0, []
    for column in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][column]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        divisor = a[row][column]
        a[row] = [x / divisor for x in a[row]]
        for i in range(row + 1, len(a)):
            multiplier = a[i][column]
            if multiplier:
                a[i] = [x - multiplier * y for x, y in zip(a[i], a[row])]
        columns.append(column)
        row += 1
        if row == len(a):
            break
    return tuple(columns)


def matvec(matrix, vector):
    return [sum(x * y for x, y in zip(row, vector)) for row in matrix]


def integer_autocorrelation(points, n=None):
    return Counter((x - y) % n if n else x - y for x in points for y in points)


def icv(points, n):
    out = [0] * (n // 2)
    for x, y in combinations(points, 2):
        difference = (x - y) % n
        out[min(difference, n - difference) - 1] += 1
    return tuple(out)


def canon(points, n):
    # Unlike the production six-note code, include all translations.
    return min(tuple(sorted((sign * x + shift) % n for x in points))
               for shift in range(n) for sign in (1, -1))


def independent_matchings(a, b, n):
    """DFS over A edges in lexicographic order, with individual B choices."""
    candidates = []
    for i, j in EDGES:
        choices = []
        for index, (k, ell) in enumerate(EDGES):
            for sign in (-1, 1):
                if ((a[j] - a[i]) - sign * (b[ell] - b[k])) % n == 0:
                    choices.append((index, (i, j, k, ell, sign)))
        candidates.append(choices)

    def dfs(index, used, labels):
        if index == 15:
            assert used == (1 << 15) - 1
            yield tuple(labels)
            return
        for target, label in candidates[index]:
            flag = 1 << target
            if not used & flag:
                labels.append(label)
                yield from dfs(index + 1, used | flag, labels)
                labels.pop()

    return dfs(0, 0, [])


def matching_matrix(labels):
    matrix = []
    for i, j, k, ell, sign in labels:
        row = [0] * 10
        if i:
            row[i - 1] -= 1
        if j:
            row[j - 1] += 1
        if k:
            row[k + 4] += sign
        if ell:
            row[ell + 4] -= sign
        matrix.append(row)
    return matrix


def cramer_kernel_lift(matrix, vector, n):
    """Independent constructive lift: Cramer determinants, not adjugates."""
    columns = rational_pivots(matrix)
    rank = len(columns)
    if not rank:
        return list(vector), 1, rank
    transpose = [[row[c] for row in matrix] for c in columns]
    rows = rational_pivots(transpose)
    pivot_matrix = [[matrix[i][j] for j in columns] for i in rows]
    delta = determinant(pivot_matrix)
    assert delta and gcd(delta, n) == 1
    free = [i for i in range(len(vector)) if i not in columns]
    rhs = [-sum(matrix[i][j] * vector[j] for j in free) for i in rows]
    w = [delta * x for x in vector]
    for index, column in enumerate(columns):
        replaced = [row[:] for row in pivot_matrix]
        for i in range(rank):
            replaced[i][index] = rhs[i]
        w[column] = determinant(replaced)
    inverse = pow(delta, -1, n)
    z = [inverse * x for x in w]
    assert not any(matvec(matrix, z))
    assert all((x - y) % n == 0 for x, y in zip(z, vector))
    return z, delta, rank


def polynomial_sum(*terms):
    out = Counter()
    for polynomial in terms:
        out.update(polynomial)
    return Counter({exponent: value for exponent, value in out.items() if value})


def polynomial_product(left, right):
    out = Counter()
    for a, ca in left.items():
        for b, cb in right.items():
            out[tuple(x + y for x, y in zip(a, b))] += ca * cb
    return Counter({exponent: value for exponent, value in out.items() if value})


def polynomial_reverse(polynomial):
    return Counter({tuple(-x for x in e): c for e, c in polynomial.items()})


def polynomial_autocorrelation(points):
    polynomial = Counter(points)
    return polynomial_product(polynomial, polynomial_reverse(polynomial))


def test_determinant_checker():
    randomizer = random.Random(730251)
    checked = 0
    for size in range(6):
        for _ in range(20):
            matrix = [[randomizer.randrange(-3, 4) for _ in range(size)]
                      for _ in range(size)]
            leibniz = 0
            for permutation in permutations(range(size)):
                inversions = sum(permutation[i] > permutation[j]
                                 for i in range(size) for j in range(i + 1, size))
                leibniz += (-1) ** inversions * prod(
                    matrix[i][permutation[i]] for i in range(size))
            assert determinant(matrix) == leibniz
            checked += 1
    return {"matrices_against_leibniz": checked}


def test_incidence_minors():
    incidence = []
    for i, j in EDGES:
        row = [0] * 5
        if i:
            row[i - 1] = -1
        row[j - 1] = 1
        incidence.append(row)
    counts = Counter()
    for size in range(6):
        for rows in combinations(range(15), size):
            for columns in combinations(range(5), size):
                delta = determinant([[incidence[i][j] for j in columns] for i in rows])
                assert delta in (-1, 0, 1)
                counts[delta] += 1
    # Row sign changes and row permutations do not change absolute minors.
    assert sum(counts.values()) == comb(20, 5)
    return {"square_minors": sum(counts.values()), "determinants": dict(counts)}


def test_formal_identities():
    bloom_a = ((0, 0), (1, 0), (-2, 1), (-2, 2), (0, 2), (-1, 3))
    bloom_b = ((0, 0), (1, 0), (2, 1), (-1, 2), (1, 2), (-1, 3))
    table = polynomial_autocorrelation(bloom_a)
    assert table == polynomial_autocorrelation(bloom_b)
    zero = (0,) * 6
    a = (1, 0, 0, 0, 0, 0)
    b = (0, 1, 0, 0, 0, 0)
    ab = (1, 1, 0, 0, 0, 0)
    c = tuple(tuple(int(i == j) for i in range(6)) for j in range(2, 6))
    left = polynomial_sum(polynomial_autocorrelation((*c, zero, ab)),
                          Counter({e: -v for e, v in polynomial_autocorrelation((*c, a, b)).items()}))
    shell = polynomial_sum(Counter(c),
                           polynomial_product(Counter({ab: 1}), polynomial_reverse(Counter(c))),
                           Counter((zero, a, b, ab)))
    right = polynomial_product(Counter({(-1, -1, 0, 0, 0, 0): 1}), shell)
    right = polynomial_product(right, Counter({zero: 1, a: -1}))
    right = polynomial_product(right, Counter({zero: 1, b: -1}))
    assert left == right
    return {"bloom_table": [[list(e), v] for e, v in sorted(table.items())],
            "bloom_support": len(table), "dyad_identity_terms": len(left)}


def test_constructive_lift():
    generic = [([[0, 0], [0, 0]], [2, 4], 5),
               ([[2, 1]], [1, 1], 3),
               ([[-2, 3], [-4, 6], [0, 0]], [1, 4], 5),
               ([[2, 0], [0, 3]], [0, 0], 5)]
    for matrix, vector, n in generic:
        assert all(x % n == 0 for x in matvec(matrix, vector))
        cramer_kernel_lift(matrix, vector, n)
    randomizer = random.Random(251257)
    statistics = []
    for n in (257, 263, 257 * 263, 257 ** 2):
        checked, ranks, determinants, max_coordinate = 0, Counter(), set(), 0
        while checked < 8:
            p, q = randomizer.randrange(n), randomizer.randrange(n)
            a = tuple(sorted(x % n for x in (0, p, q - 2*p, 2*q - 2*p, 2*q, 3*q - p)))
            b = tuple(sorted(x % n for x in (0, p, q + 2*p, 2*q - p, 2*q + p, 3*q - p)))
            if len(set(a)) != 6 or len(set(b)) != 6:
                continue
            assert integer_autocorrelation(a, n) == integer_autocorrelation(b, n)
            labels = next(independent_matchings(a, b, n))
            matrix = matching_matrix(labels)
            vector = [(x - a[0]) % n for x in a[1:]] + [(x - b[0]) % n for x in b[1:]]
            z, delta, rank = cramer_kernel_lift(matrix, vector, n)
            lifted_a, lifted_b = (0, *z[:5]), (0, *z[5:])
            assert len(set(lifted_a)) == len(set(lifted_b)) == 6
            assert integer_autocorrelation(lifted_a) == integer_autocorrelation(lifted_b)
            assert abs(delta) <= 252
            ranks[rank] += 1
            determinants.add(delta)
            max_coordinate = max(max_coordinate, max(map(abs, z)))
            checked += 1
        statistics.append({"n": n, "lifts": checked, "ranks": dict(ranks),
                           "determinants": sorted(determinants),
                           "largest_absolute_coordinate": max_coordinate})
    return {"generic_cases": len(generic), "modular_bloom_cases": statistics}


def test_antipodal_and_minor_caveats():
    n, points = 12, (0, 1, 2, 3, 4, 6)
    labels = [(i, j, i, j, -1 if (i, j) == (0, 5) else 1) for i, j in EDGES]
    bad = matching_matrix(labels)
    vector = list(points[1:]) * 2
    assert all(x % n == 0 for x in matvec(bad, vector))
    # The other edge equations force A_5=B_5, while the antipodal equation
    # forces A_5=-B_5. Over Z this makes both zero, contradicting residue 6.
    assert len(rational_pivots(bad)) == 6
    good = matching_matrix([(i, j, i, j, 1) for i, j in EDGES])
    assert not any(matvec(good, vector))
    # Coprime minors are sufficient, not necessary: (3,-2) is an integer
    # kernel vector of [2,3], yet neither minor is coprime to modulus 6.
    assert matvec([[2, 3]], [3, -2]) == [0]
    assert gcd(2, 6) != 1 and gcd(3, 6) != 1
    return {"bad_antipodal_matching_rank": 6, "same_pair_has_integer_lift": True,
            "coprime_minor_condition_is_not_necessary": True}


def test_saved_shadow_certificates():
    summaries = []
    directory = ROOT / "results/2026-09-30-six-shadow"
    names = [f"n{n}.json" for n in (17, 18, 19, 21, 23, 31)]
    names += ["shell_type2_n18.json", "shell_type3_n18.json"]
    for name in names:
        path = directory / name
        payload = json.loads(path.read_text())
        n = payload["n"]
        a, b = payload["a"], payload["b"]
        assert payload["decision"] == "purely-cyclic"
        assert len(set(a)) == len(set(b)) == 6
        assert integer_autocorrelation(a, n) == integer_autocorrelation(b, n)
        assert icv(a, n) == reference_icv(a, n) == reference_icv(b, n)
        assert canon(a, n) != canon(b, n)
        independently_found = {tuple(labels) for labels in independent_matchings(a, b, n)}
        records = payload["certificates"]
        supplied = [tuple(sorted(tuple(label) for label in r["labels"])) for r in records]
        assert len(set(supplied)) == len(supplied)  # no duplicate-padding
        assert set(supplied) == independently_found  # no omitted matching/sign
        assert len(records) == payload["checked_matchings"] == payload["expected_matchings"]
        vector = [(x - a[0]) % n for x in a[1:]] + [(x - b[0]) % n for x in b[1:]]
        ranks, determinants, divisors = Counter(), Counter(), Counter()
        for record in records:
            labels = record["labels"]
            assert sorted((i, j) for i, j, _, _, _ in labels) == list(EDGES)
            assert sorted((k, ell) for _, _, k, ell, _ in labels) == list(EDGES)
            matrix = matching_matrix(labels)
            assert matrix == record["matrix"]
            assert all(x % n == 0 for x in matvec(matrix, vector))
            rank = len(rational_pivots(matrix))
            assert rank == record["rank"]
            rows, columns = record["minor_rows"], record["minor_columns"]
            assert len(rows) == len(columns) == rank
            assert len(set(rows)) == len(rows) and len(set(columns)) == len(columns)
            minor = [[matrix[i][j] for j in columns] for i in rows]
            delta = determinant(minor)
            assert delta == record["determinant"] != 0
            assert abs(delta) <= comb(rank, sum(j < 5 for j in columns)) <= 252
            ranks[rank] += 1
            determinants[delta] += 1
            if rank == 10:
                assert any(vector)  # zero integer kernel cannot lift input
            else:
                smith = record["smith"]
                row = smith["row_combination"]
                assert len(row) == len(matrix) and all(isinstance(x, int) for x in row)
                coefficients = [sum(row[i] * matrix[i][j] for i in range(15)) for j in range(10)]
                rhs = [-x // n for x in matvec(matrix, vector)]
                value = sum(x * y for x, y in zip(row, rhs))
                assert value == smith["value"]
                divisor = smith["divisor"]
                if divisor:
                    assert all(x % divisor == 0 for x in coefficients)
                    assert value % divisor != 0
                else:
                    assert not any(coefficients) and value != 0
                divisors[divisor] += 1
        assert dict(ranks) == {int(k): v for k, v in payload["ranks"].items()}
        summaries.append({"case": path.stem, "n": n, "a": a, "b": b, "matchings": len(records),
                          "ranks": dict(ranks), "determinants": dict(determinants),
                          "rejection_divisors": dict(divisors),
                          "payload_sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    return summaries


def test_parametric_purely_cyclic_families():
    families = (
        (((0, 0), (1, 0), (1, 1), (0, 2), (1, 3), (1, 4)),
         ((0, 0), (1, 0), (1, 1), (1, 2), (0, 3), (1, 4))),
        (((0, 0), (1, 0), (0, 1), (0, 2), (1, 3), (0, 4)),
         ((0, 0), (1, 0), (0, 1), (1, 2), (0, 3), (0, 4))),
        (((0, 0), (1, 0), (0, 1), (0, 3), (1, 3), (0, 5)),
         ((0, 0), (1, 0), (0, 1), (0, 3), (0, 4), (1, 4))))
    bins = ((1, 0), (-1, 1), (0, 1), (1, 1), (-1, 2), (0, 2),
            (1, 2), (-1, 3), (0, 3))
    names = ("n18.json", "shell_type2_n18.json", "shell_type3_n18.json")
    summaries = []

    def edge_difference(points, edge):
        i, j = edge
        return tuple(points[j][k]-points[i][k] for k in range(2))

    def distances(points):
        output = []
        for edge in EDGES:
            delta = edge_difference(points, edge)
            possible = [index for index, value in enumerate(bins)
                        if delta == value or delta == (-value[0], 6-value[1])]
            assert len(possible) == 1
            output.append(possible[0])
        return output

    def formal_correlation(points):
        return Counter((x[0]-y[0], (x[1]-y[1]) % 6) for x in points for y in points)

    def gap_word(points, n):
        assert points == tuple(sorted(points))
        return tuple(points[i+1]-points[i] for i in range(5)) + (n-points[-1],)

    def gap_canon(word):
        candidates = []
        for sequence in (word, word[::-1]):
            for offset in range(6):
                candidates.append(sequence[offset:]+sequence[:offset])
        return min(candidates)

    for family_type, ((A_coeff, B_coeff), name) in enumerate(zip(families, names), 1):
        assert formal_correlation(A_coeff) == formal_correlation(B_coeff)
        assert Counter(distances(A_coeff)) == Counter(distances(B_coeff))
        payload = json.loads((ROOT / "results/2026-09-30-six-shadow" / name).read_text())
        prototype_A = tuple(p+3*q for p, q in A_coeff)
        prototype_B = tuple(p+3*q for p, q in B_coeff)
        assert list(prototype_A) == payload["a"] and list(prototype_B) == payload["b"]
        # Direct symbolic edge compatibility equals prototype compatibility.
        # The strict bin inequalities make it the compatibility graph at every
        # point of 0<a<m/2, not merely at the prototype ratio 1/3.
        compatibility_checked = 0
        for A_edge, B_edge, sign in product(EDGES, EDGES, (-1, 1)):
            dx, dy = edge_difference(A_coeff, A_edge), edge_difference(B_coeff, B_edge)
            symbolic = (dx[0]-sign*dy[0], dx[1]-sign*dy[1])
            compatible = symbolic[0] == 0 and symbolic[1] % 6 == 0
            numeric = (symbolic[0]+3*symbolic[1]) % 18 == 0
            assert compatible == numeric
            compatibility_checked += 1
        labels = {tuple(x) for x in independent_matchings(prototype_A, prototype_B, 18)}
        supplied = {tuple(sorted(tuple(y) for y in c["labels"])) for c in payload["certificates"]}
        assert labels == supplied and len(labels) == 384
        Va = [x[0] for x in A_coeff[1:]+B_coeff[1:]]
        Vm = [x[1] for x in A_coeff[1:]+B_coeff[1:]]
        rejections = Counter()
        for certificate in payload["certificates"]:
            matrix = matching_matrix(certificate["labels"])
            assert not any(matvec(matrix, Va))
            mVm = matvec(matrix, Vm)
            assert all(x % 6 == 0 for x in mVm)
            rhs = [-x // 6 for x in mVm]
            combination = certificate["smith"]["row_combination"]
            coefficients = [sum(combination[i]*matrix[i][j] for i in range(15))
                            for j in range(10)]
            target = sum(x*y for x, y in zip(combination, rhs))
            assert all(x % 6 == 0 for x in coefficients)
            assert target % 6 != 0
            assert target == certificate["smith"]["value"]
            rejections[target % 6] += 1
        # Additional samples check formulas, strict bins, cyclic homometry,
        # and nontriviality by gap words, including inflated parameters and
        # enormous moduli where direct T/I translation loops are unsuitable.
        samples = [(m, a) for m in range(3, 51) for a in range(1, (m-1)//2+1)]
        samples += [(1_000_003, 1), (1_000_003, 500_001), (1_000_008, 12)]
        for m, a in samples:
            n = 6*m
            X = tuple(p*a+q*m for p, q in A_coeff)
            Y = tuple(p*a+q*m for p, q in B_coeff)
            assert X == tuple(sorted(set(X))) and Y == tuple(sorted(set(Y)))
            assert X[-1] < n and Y[-1] < n
            numerical_bins = [p*a+q*m for p, q in bins]
            assert numerical_bins == sorted(set(numerical_bins))
            assert integer_autocorrelation(X, n) == integer_autocorrelation(Y, n)
            gx, gy = gap_word(X, n), gap_word(Y, n)
            assert gap_canon(gx) != gap_canon(gy)
            assert min(gx) == min(gy) == a
        summaries.append({"type": family_type, "prototype": name,
                          "all_matchings": len(labels), "symbolic_row_rejections": len(labels),
                          "edge_sign_compatibilities_checked": compatibility_checked,
                          "Va": Va, "Vm": Vm, "nonzero_remainders_mod6": dict(rejections),
                          "parameter_samples": len(samples)})
    return {"parameter_chamber": "integer 0<a<m/2, n=6m", "families": summaries,
            "universal_step": "fixed distance bins and exact coefficient-vector/witness identities"}


def periodic(values, step, n):
    return all(values[x] == values[(x + step) % n] for x in range(n))


def positive_periodic_decomposition(values, a, b, n):
    """Build the complete coset-intersection grid with residue classes."""
    da, db, dh = gcd(a, n), gcd(b, n), gcd(a, b, n)
    cells = {}
    for x in range(n):
        key = (x % da, x % db)
        if key in cells:
            assert cells[key] == values[x]
        else:
            cells[key] = values[x]
    u, v = {}, {}
    for h in range(dh):
        rows = list(range(h, da, dh))
        columns = list(range(h, db, dh))
        anchor = columns[0]
        minimum = min(cells[i, anchor] for i in rows)
        for i in rows:
            u[i] = cells[i, anchor] - minimum
        for j in columns:
            v[j] = min(cells[i, j] for i in rows)
    U, V = [u[x % da] for x in range(n)], [v[x % db] for x in range(n)]
    assert all(isinstance(x, int) and x >= 0 for x in U + V)
    assert periodic(U, a, n) and periodic(V, b, n)
    assert values == [x + y for x, y in zip(U, V)]
    return U, V


def recover_common_sets(values, a, b, n):
    corners = {0, a, b, (a + b) % n}
    assert len(corners) == 4 and all(values[x] == 1 for x in corners)
    remaining = set(range(n)) - corners
    options = []
    while remaining:
        x = min(remaining)
        y = (a + b - x) % n
        assert y in remaining and values[x] == values[y]
        q = values[x]
        assert q in (0, 1, 2)
        if x == y:
            assert q in (0, 2)
            options.append((frozenset({x}) if q else frozenset(),))
        elif q == 0:
            options.append((frozenset(),))
        elif q == 1:
            options.append((frozenset({x}), frozenset({y})))
        else:
            options.append((frozenset({x, y}),))
        remaining -= {x, y}
    for choice in product(*options):
        common = frozenset().union(*choice)
        assert len(common) == 4 and not (common & corners)
        yield common


def test_dyad_extension():
    checked, homometric, per_n = 0, 0, []
    for n in range(8, 15):
        nchecked, nhomometric = 0, 0
        for a, b in product(range(1, n), repeat=2):
            corners = {0, a, b, (a + b) % n}
            if len(corners) != 4:
                continue
            for common in combinations(sorted(set(range(n)) - corners), 4):
                A, B = (*common, 0, (a + b) % n), (*common, a, b)
                nchecked += 1
                same = integer_autocorrelation(A, n) == integer_autocorrelation(B, n)
                shell = Counter(common)
                shell.update((a + b - x) % n for x in common)
                shell.update(corners)
                values = [shell[x] for x in range(n)]
                mixed = [values[x] - values[(x-a) % n] - values[(x-b) % n]
                         + values[(x-a-b) % n] for x in range(n)]
                assert same == (not any(mixed))
                if gcd(a, n) == 1:
                    assert same == periodic(values, b, n)
                if not same:
                    continue
                nhomometric += 1
                U, V = positive_periodic_decomposition(values, a, b, n)
                ha, hb = n // gcd(a, n), n // gcd(b, n)
                assert sum(U) + sum(V) == 12
                assert sum(U) % ha == sum(V) % hb == 0
                assert min(ha, hb) <= 12
                if ha > 12:
                    assert not any(U) and periodic(values, b, n)
                candidates = list(recover_common_sets(values, a, b, n))
                assert frozenset(common) in candidates
                for candidate in candidates:
                    assert integer_autocorrelation((*candidate, 0, (a+b) % n), n) == integer_autocorrelation((*candidate, a, b), n)
        checked += nchecked
        homometric += nhomometric
        per_n.append({"n": n, "shapes": nchecked, "homometric_shapes": nhomometric})
    n, a, b, common = 8, 4, 1, (2, 3, 6, 7)
    shell = Counter(common)
    shell.update((a+b-x) % n for x in common)
    shell.update((0, a, b, (a+b) % n))
    assert integer_autocorrelation((*common, 0, 5), n) == integer_autocorrelation((*common, 4, 1), n)
    assert not periodic([shell[x] for x in range(n)], b, n)
    return {"shapes": checked, "homometric_shapes": homometric, "per_n": per_n,
            "nonunit_necessity_example": {"n": n, "a": a, "b": b, "C": common}}


def test_nonnegative_decomposition_edge_cases():
    checked, decomposable = 0, 0
    for n in range(1, 7):
        for a, b in product(range(n), repeat=2):
            for raw in product(range(3), repeat=n):
                values = list(raw)
                mixed = [values[x]-values[(x-a) % n]-values[(x-b) % n]
                         +values[(x-a-b) % n] for x in range(n)]
                try:
                    positive_periodic_decomposition(values, a, b, n)
                    has_decomposition = True
                except AssertionError:
                    has_decomposition = False
                assert has_decomposition == (not any(mixed))
                decomposable += has_decomposition
                checked += 1
    return {"range": [1, 6], "coefficient_values": [0, 1, 2],
            "vectors_and_step_choices": checked, "decomposable": decomposable,
            "includes_zero_steps_and_zero_mass": True}


def test_order_six_generator():
    checked, genuine, reference_checked = 0, 0, 0
    for n in (12, 18, 24, 30, 36):
        for b in range(1, n):
            if n // gcd(b, n) != 6:
                continue
            H = {(i * b) % n for i in range(6)}
            for a in sorted(set(range(n)) - H):
                S = H | {(a+x) % n for x in H}
                corners = {0, a, b, (a+b) % n}
                remaining, orbits = S - corners, []
                while remaining:
                    x = min(remaining)
                    y = (a+b-x) % n
                    assert y in remaining and x != y
                    orbits.append((x, y))
                    remaining -= {x, y}
                assert len(orbits) == 4
                for bits in product((0, 1), repeat=4):
                    common = {orbits[i][bits[i]] for i in range(4)}
                    A, B = common | {0, (a+b) % n}, common | {a, b}
                    assert len(A) == len(B) == 6
                    assert integer_autocorrelation(A, n) == integer_autocorrelation(B, n)
                    if n <= 24:
                        assert icv(A, n) == reference_icv(tuple(A), n) == reference_icv(tuple(B), n)
                        reference_checked += 1
                    genuine += canon(A, n) != canon(B, n)
                    checked += 1
    examples = []
    for n, b, common, shift, expected_a, expected_b in (
            (18, 3, (12, 13, 16, 7), 6, (0, 1, 4, 6, 10, 13), (0, 1, 4, 7, 9, 13)),
            (24, 4, (16, 17, 21, 9), 8, (0, 1, 5, 8, 13, 17), (0, 1, 5, 9, 12, 17))):
        A = tuple(sorted((x + shift) % n for x in (*common, 0, 1+b)))
        B = tuple(sorted((x + shift) % n for x in (*common, 1, b)))
        assert A == expected_a and B == expected_b
        assert canon(A, n) != canon(B, n)
        examples.append({"n": n, "A": A, "B": B, "icv": icv(A, n)})
    return {"outputs": checked, "genuine_outputs_with_multiplicity": genuine,
            "reference_checked": reference_checked, "examples": examples}


def test_direct_sum_exclusion():
    checked = 0
    for n in range(6, 15):
        for u in range(1, n):
            for v, w in combinations(range(1, n), 2):
                Q = (0, v, w)
                A = {(p+q) % n for p in (0, u) for q in Q}
                if len(A) != 6:
                    continue
                flipped_two = {(-p+q) % n for p in (0, u) for q in Q}
                flipped_three = {(p-q) % n for p in (0, u) for q in Q}
                assert flipped_two == {(x-u) % n for x in A}
                assert flipped_three == {(u-x) % n for x in A}
                checked += 1
    return {"collision_free_modular_products": checked}


def independent_h6_edges(n):
    edges = set()
    if n % 6:
        return edges
    for b in range(1, n):
        if n // gcd(b, n) != 6:
            continue
        subgroup = {(i * b) % n for i in range(6)}
        for a in sorted(set(range(n)) - subgroup):
            corners = {0, a, b, (a+b) % n}
            remaining = (subgroup | {(a+x) % n for x in subgroup}) - corners
            orbits = []
            while remaining:
                x = min(remaining)
                y = (a+b-x) % n
                assert y in remaining and x != y
                orbits.append((x, y))
                remaining -= {x, y}
            assert len(orbits) == 4
            for bits in product((0, 1), repeat=4):
                common = tuple(orbits[i][bits[i]] for i in range(4))
                A = canon((*common, 0, (a+b) % n), n)
                B = canon((*common, a, b), n)
                if A != B:
                    edges.add(tuple(sorted((A, B))))
    return edges


def independent_shape_alignment(A, B, n):
    # Any four-point intersection contains a matched point. Generate shifts
    # from point pairs rather than looping over all possible translations.
    aset = set(A)
    for sign in (-1, 1):
        shifts = {(x-sign*y) % n for x in A for y in B}
        for shift in shifts:
            image = {(sign*y+shift) % n for y in B}
            common = aset & image
            if len(common) == 4 and (sum(aset-common)-sum(image-common)) % n == 0:
                return True
    return False


def test_saved_shell_certificates():
    directory = ROOT / "results/2026-09-30-six-shell"
    summaries, total_certificates, total_gap_shapes = [], 0, 0
    for n in range(12, 61):
        path = directory / f"n{n}.json"
        payload = json.loads(path.read_text())
        inventory = json.loads((ROOT / f"results/2026-09-30-six-inventory/n{n}.json").read_text())
        families = inventory["families"]
        membership, gaps = {}, set()
        for family in families:
            members = [tuple(x) for x in family["members"]]
            for member in members:
                assert icv(member, n) == tuple(family["icv"])
                if n <= 24:
                    assert icv(member, n) == reference_icv(member, n)
            for pair in combinations(members, 2):
                key = tuple(sorted(pair))
                assert key not in membership
                membership[key] = family["combined_components"] > 1
                if membership[key]:
                    # These saved gap families all have two members, so a
                    # disconnected-family label is also a missing-pair label.
                    assert len(members) == 2
                    gaps.add(key)
        h6_edges = independent_h6_edges(n)
        seen, counts = set(), Counter()
        for record in payload["pairs"]:
            A, B = record["x"], record["y"]
            key = tuple(sorted((tuple(A), tuple(B))))
            assert key in membership and key not in seen
            seen.add(key)
            assert integer_autocorrelation(A, n) == integer_autocorrelation(B, n)
            shape = record["shape"]
            a, b, common = shape["a"], shape["b"], shape["common"]
            assert len(set(common)) == 4
            corners = {0, a, b, (a+b) % n}
            assert len(corners) == 4 and not set(common) & corners
            raw_a, raw_b = sorted((*common, 0, (a+b) % n)), sorted((*common, a, b))
            assert raw_a == shape["raw_a"] and raw_b == shape["raw_b"]
            anchor, alignment = shape["a_anchor"], shape["b_alignment"]
            assert sorted((x+anchor) % n for x in raw_a) == A
            assert sorted((x+anchor) % n for x in raw_b) == sorted(
                (alignment["sign"]*x+alignment["shift"]) % n for x in B)
            shell = Counter(common)
            shell.update((a+b-x) % n for x in common)
            shell.update(corners)
            w, u, v = shape["w"], shape["u"], shape["v"]
            assert len(w) == len(u) == len(v) == n
            assert w == [shell[x] for x in range(n)]
            assert all(isinstance(x, int) and x >= 0 for x in w+u+v)
            assert periodic(u, a, n) and periodic(v, b, n)
            assert [x+y for x, y in zip(u, v)] == w and sum(w) == 12
            ha, hb = n // gcd(a, n), n // gcd(b, n)
            assert (ha, hb) == (shape["order_a"], shape["order_b"])
            assert sum(u) % ha == sum(v) % hb == 0 and min(ha, hb) <= 12
            assert periodic([w[x]-w[(x-b) % n] for x in range(n)], a, n)
            # Binary/reflection recovery conditions are checked directly.
            assert all(w[x] == w[(a+b-x) % n] for x in range(n))
            assert all(w[x] == 1 for x in corners)
            assert all(w[x] in (0, 1, 2) for x in set(range(n))-corners)
            assert all(w[x] in (0, 2) for x in set(range(n))-corners
                       if (2*x-a-b) % n == 0)
            is_h6 = key in h6_edges
            assert (record["h6"] is not None) == is_h6
            if is_h6:
                h6 = record["h6"]
                sa, sb, C = h6["a"], h6["b"], h6["common"]
                assert n // gcd(sb, n) == 6 and len(set(C)) == 4
                H = {(i*sb) % n for i in range(6)}
                assert sa not in H
                S, R = H | {(sa+x) % n for x in H}, {0, sa, sb, (sa+sb) % n}
                reflected = {(sa+sb-x) % n for x in C}
                assert not set(C) & reflected
                assert set(C) | reflected == S-R
                recovered = tuple(sorted((canon((*C, 0, (sa+sb) % n), n),
                                          canon((*C, sa, sb), n))))
                assert recovered == key
            assert record["menu_gap"] == membership[key]
            counts["shape_pairs"] += 1
            counts["gap_shape_pairs"] += record["menu_gap"]
            counts["h6_pairs"] += is_h6
            counts["gap_h6_pairs"] += record["menu_gap"] and is_h6
        assert h6_edges <= seen  # no h6 output omitted from shape inventory
        assert {k: v for k, v in counts.items() if v} == {
            k: v for k, v in payload["summary"].items() if v}
        independently_found_shapes = {pair for pair in membership if independent_shape_alignment(*pair, n)}
        assert independently_found_shapes == seen  # full shape-search completeness
        independently_found_gaps = independently_found_shapes & gaps
        assert independently_found_gaps <= h6_edges
        total_certificates += len(seen)
        total_gap_shapes += len(independently_found_gaps)
        summaries.append({"n": n, "shape_certificates": len(seen),
                          "all_inventory_pairs_searched": len(membership),
                          "h6_edges": len(h6_edges), "menu_gap_pairs": len(gaps),
                          "gap_shape_pairs": len(independently_found_gaps),
                          "payload_sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        if n % 12 == 0:
            print(f"checked shell payloads through n={n}", flush=True)
    return {"range": [12, 60], "shape_certificates": total_certificates,
            "gap_shape_pairs": total_gap_shapes, "per_n": summaries,
            "limit": "gap membership is relative to saved inherited strict+Bloom menu"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    output = {"method": "independent DFS, Bareiss determinants, Fraction rank, direct divisibility witnesses"}
    for name, test in (("determinant_checker", test_determinant_checker),
                       ("incidence_minors", test_incidence_minors),
                       ("formal_identities", test_formal_identities),
                       ("constructive_lift", test_constructive_lift),
                       ("antipodal_and_minor_caveats", test_antipodal_and_minor_caveats),
                       ("saved_shadow_certificates", test_saved_shadow_certificates),
                       ("parametric_purely_cyclic_families", test_parametric_purely_cyclic_families),
                       ("dyad_extension", test_dyad_extension),
                       ("nonnegative_decomposition_edge_cases", test_nonnegative_decomposition_edge_cases),
                       ("order_six_generator", test_order_six_generator),
                       ("direct_sum_exclusion", test_direct_sum_exclusion),
                       ("saved_shell_certificates", test_saved_shell_certificates)):
        output[name] = test()
        print(f"PASS {name}", flush=True)
    output["seconds"] = round(time.monotonic() - started, 3)
    output["test_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(output, sort_keys=True) + "\n")
    print(f"PASS all independent attacks ({output['seconds']}s)", flush=True)


if __name__ == "__main__":
    main()
