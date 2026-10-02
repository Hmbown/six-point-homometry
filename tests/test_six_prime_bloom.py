"""Independent small-modulus and saved-census checks for prime Bloom counts."""
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from homometry import dihedral_canon, icv, z_families
from six_prime_bloom import (X_COEFFICIENTS, Y_COEFFICIENTS, bloom_points, canonical,
                             classify_parameter, compare_saved_census, enumerate_prime,
                             integer_collision_lines, pairs_from_result, parse_primes,
                             reference_parameter_pairs)


def test_canonical_against_reference():
    # All subsets of two small rings, including empty/full and symmetric sets.
    for n in (7, 8):
        for mask in range(1 << n):
            points = tuple(i for i in range(n) if mask >> i & 1)
            assert canonical(points, n) == dihedral_canon(points, n), (n, points)
    for n in (11, 13, 17, 19, 23):
        for a in range(n):
            for b in range(n):
                for points in bloom_points(a, b, n):
                    assert canonical(points, n) == dihedral_canon(tuple(sorted(set(points))), n), (n, a, b, points)


def test_formal_homometry_and_collision_lines():
    # This is an integer-vector identity, independent of reduction/canonicalizer.
    def directed_distance_multiset(points):
        return Counter((u - v, x - y) for u, x in points for v, y in points)
    assert directed_distance_multiset(X_COEFFICIENTS) == directed_distance_multiset(Y_COEFFICIENTS)
    lines = integer_collision_lines()
    assert sum(len(line["witnesses"]) for line in lines) == 30
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23):
        for a in range(p):
            for b in range(p):
                x, y = bloom_points(a, b, p)
                by_support = len(set(x)) < 6 or len(set(y)) < 6
                by_lines = any((witness["raw_coefficients"][0] * a +
                                witness["raw_coefficients"][1] * b) % p == 0
                               for line in lines for witness in line["witnesses"])
                assert by_support == by_lines, (p, a, b)
                assert (classify_parameter(a, b, p)[0] == "collision") == by_support


def test_parameter_image_reference_and_census():
    for p in (2, 3, 5, 7, 11, 13, 17, 19):
        result = enumerate_prime(p)
        actual = {tuple(tuple(x) for x in rec["pair"]): [tuple(v) for v in rec["parameters"]]
                  for rec in result["fibers"]}
        assert actual == reference_parameter_pairs(p), p
        summary = result["summary"]
        assert summary["parameters"] == sum(summary[key] for key in
                  ("collision_parameters", "congruent_parameters", "admissible_parameters"))
        assert sum(len(rec["parameters"]) for rec in result["fibers"]) == summary["admissible_parameters"]
        for pair in actual:
            assert icv(pair[0], p) == icv(pair[1], p) and pair[0] != pair[1]
        census = compare_saved_census(result)
        if census:
            assert census["all_bloom_pairs_present"]
    reference_census = {tuple(sorted((a, b))) for family in z_families(13, sizes=[6]).values()
                        for a, b in combinations(family, 2)}
    assert pairs_from_result(enumerate_prime(13)) == reference_census


def test_exact_edge_cases_and_unquotiented_units():
    # These edge cases include many collisions and few surviving pairs.
    p13 = enumerate_prime(13)
    assert p13["summary"]["pairs"] == 2
    assert p13["summary"]["fiber_histogram"] == {12: 2}
    p17 = enumerate_prime(17)
    assert p17["summary"]["pairs"] == 8
    assert p17["summary"]["fiber_histogram"] == {12: 8}
    assert classify_parameter(0, 0, 17) == ("collision", None)
    assert classify_parameter(1, 0, 17) == ("collision", None)
    # Multiplication by2 gives another T/I pair: both must remain counted.
    category, pair = classify_parameter(1, 6, 19)
    assert category == "admissible"
    multiplied = tuple(sorted(canonical([2 * x for x in endpoint], 19) for endpoint in pair))
    assert multiplied != pair
    assert pair in pairs_from_result(enumerate_prime(19))
    assert multiplied in pairs_from_result(enumerate_prime(19))
    for p in (0, 1, 4, 15):
        try:
            enumerate_prime(p)
        except ValueError:
            pass
        else:
            raise AssertionError(f"accepted composite/nonprime modulus{p}")
    assert parse_primes(["13,17", "19..29"]) == [13, 17, 19, 23, 29]


def test_parameter_symmetry_orbits_and_exclusions():
    # Independent formulas from the symmetry proof; none is used by the
    # production enumerator. Thus orbit agreement checks identifications rather
    # than making the direct enumeration assume a fiber size.
    def orbit(a, b, p):
        reached = {(a % p, b % p)}
        pending = list(reached)
        while pending:
            x, y = pending.pop()
            for partner in ((-y % p, (x - y) % p), (y, x), (-x % p, -y % p)):
                if partner not in reached:
                    reached.add(partner)
                    pending.append(partner)
        return reached
    for p in (13, 17, 19, 23, 29, 31, 37, 41, 43, 131, 251, 1009):
        result_path = ROOT / f"results/2026-09-30-six-prime-count/p{p}.json"
        result = json.loads(result_path.read_text()) if result_path.exists() else enumerate_prime(p)
        inv2, inv3 = pow(2, -1, p), pow(3, -1, p)
        expected = {(0, 1)} | {(1, s % p) for s in
                    (0, 1, -1, 2, -2, 3, inv2, -inv2, 3 * inv2, inv3, 2 * inv3)}
        assert len(expected) == 12
        assert {tuple(x) for x in result["exclusion_directions"]["collision"]} == expected
        assert result["exclusion_directions"]["congruent"] == []
        controls = result["fibers"] if p <= 43 else result["fibers"][::max(1, len(result["fibers"]) // 8)]
        for rec in controls:
            parameters = {tuple(x) for x in rec["parameters"]}
            assert len(parameters) == 12
            assert orbit(*rec["parameters"][0], p) == parameters, (p, rec)
        for direction in expected:
            assert classify_parameter(*direction, p)[0] == "collision"


def test_generated_artifacts():
    directory = ROOT / "results/2026-09-30-six-prime-count"
    for path in sorted(directory.glob("p*.json")):
        result = json.loads(path.read_text())
        p = result["summary"]["p"]
        parameters = set()
        histogram = Counter()
        reference_indices = set(range(len(result["fibers"]))) if p <= 43 else {
            0, len(result["fibers"]) // 3, 2 * len(result["fibers"]) // 3,
            len(result["fibers"]) - 1}
        for index, rec in enumerate(result["fibers"]):
            pair = tuple(tuple(x) for x in rec["pair"])
            assert pair[0] < pair[1]
            assert all(len(endpoint) == 6 for endpoint in pair)
            if index in reference_indices:
                assert all(dihedral_canon(endpoint, p) == endpoint for endpoint in pair)
            assert icv(pair[0], p) == icv(pair[1], p)
            histogram[len(rec["parameters"])] += 1
            for a, b in rec["parameters"]:
                assert (a, b) not in parameters
                parameters.add((a, b))
                assert classify_parameter(a, b, p) == ("admissible", pair)
        assert dict(sorted(histogram.items())) == {int(k): v for k, v in
                                                result["summary"]["fiber_histogram"].items()}
        assert len(parameters) == result["summary"]["admissible_parameters"]
        saved = compare_saved_census(result)
        assert saved == result["saved_census_comparison"]


if __name__ == "__main__":
    for test in (test_canonical_against_reference, test_formal_homometry_and_collision_lines,
                 test_parameter_image_reference_and_census,
                 test_exact_edge_cases_and_unquotiented_units,
                 test_parameter_symmetry_orbits_and_exclusions, test_generated_artifacts):
        test()
        print("PASS", test.__name__, flush=True)
