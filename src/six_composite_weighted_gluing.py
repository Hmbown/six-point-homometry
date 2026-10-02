"""Small exact weighted-list gluing certificate; no finite modulus sampling."""
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import permutations, product
import json
from math import comb
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LOCAL_CERT = ROOT / "src"
sys.path.insert(0, str(LOCAL_CERT))
from six_prime_power_lifts import certificate as paired_lift_table
from six_prime_power_endpoint_lifts import certificate as endpoint_lift_table

CX = ((2, -4), (5, -4), (-4, -1), (-4, 2), (2, 2), (-1, 5))
CY = ((-1, -4), (2, -4), (5, -1), (-4, 2), (2, 2), (-4, 5))
RHO_X = (3, 2, 5, 4, 0, 1)
RHO_Y = (5, 3, 0, 4, 1, 2)
LINES = ((0, 1), (1, 0), (1, 1), (1, -1), (1, 2), (1, -2),
         (1, 3), (2, 1), (2, -1), (2, 3), (3, 1), (3, 2))
CHI = {"X": {13: (2, 4, 0, 5, 1, 3), 19: (1, 0, 3, 2, 5, 4)},
       "Y": {13: (3, 2, 1, 0, 5, 4), 19: (1, 0, 4, 5, 2, 3)}}


def compose_rows(p, q):
    return tuple(q[p[i]] for i in range(6))


def powers(rho):
    return (tuple(range(6)), rho, compose_rows(rho, rho))


def positive_autos(rows, line):
    values = tuple(x * line[0] + y * line[1] for x, y in rows)
    return tuple(perm for perm in permutations(range(6))
                 if values == tuple(values[j] for j in perm))


def poly_add(*terms):
    out = defaultdict(int)
    for coefficient, polynomial in terms:
        for monomial, value in polynomial.items():
            out[monomial] += coefficient * value
    return {key: value for key, value in out.items() if value}


def poly_mul(left, right):
    out = defaultdict(int)
    for (a, b), x in left.items():
        for (c, d), y in right.items():
            out[a + c, b + d] += x * y
    return {key: value for key, value in out.items() if value}


def centered_moment(rows, degree):
    return { (degree - j, j): sum(comb(degree, j) * a ** (degree - j) * b ** j
                                  for a, b in rows)
             for j in range(degree + 1)}


def moment_certificate():
    s = {(2, 0): 1, (1, 1): -1, (0, 2): 1}
    e = {(2, 1): 1, (1, 2): -1}
    d = {(3, 0): 2, (2, 1): -3, (1, 2): -3, (0, 3): 2}
    result = {}
    for name, rows, sign in (("X", CX, -1), ("Y", CY, 1)):
        m3 = centered_moment(rows, 3)
        m5 = centered_moment(rows, 5)
        expected3 = poly_add((6, d), (sign * 243, e))
        expected5 = poly_add((15, poly_mul(s, poly_add((38, d), (sign * 567, e)))))
        assert {key: value for key, value in m3.items() if value} == expected3
        assert {key: value for key, value in m5.items() if value} == expected5
        result[name] = {"m3_coefficients_a_descending": list(m3.values()),
                        "m5_coefficients_a_descending": list(m5.values()),
                        "m5_identity": "15 s (38 d - 567 e)" if sign == -1 else
                                       "15 s (38 d + 567 e)"}
    return result


def gluing_certificate():
    paired = defaultdict(list)
    endpoint = {"X": defaultdict(list), "Y": defaultdict(list)}
    line_records = []
    for line_index, line in enumerate(LINES):
        hx, hy = positive_autos(CX, line), positive_autos(CY, line)
        assert len(hx) == len(hy) == (4 if line_index < 3 else 2)
        line_records.append({"index": line_index, "primitive_vector": line,
                             "positive_autos_X": hx, "positive_autos_Y": hy})
        for rotation, (px, py) in enumerate(zip(powers(RHO_X), powers(RHO_Y))):
            for ax, ay in product(hx, hy):
                paired[compose_rows(px, ax), compose_rows(py, ay)].append(
                    (rotation, line_index))
            for ax in hx:
                endpoint["X"][compose_rows(px, ax)].append((rotation, line_index))
            for ay in hy:
                endpoint["Y"][compose_rows(py, ay)].append((rotation, line_index))
    assert len(paired) == 219
    assert Counter(map(len, paired.values())) == {1: 216, 12: 3}
    assert all(len({rotation for rotation, line in witnesses}) == 1
               for witnesses in paired.values())
    endpoint_records = {}
    for name, rho in (("X", RHO_X), ("Y", RHO_Y)):
        positive = endpoint[name]
        assert len(positive) == 57
        assert Counter(map(len, positive.values())) == {1: 54, 12: 3}
        assert all(len({rotation for rotation, line in witnesses}) == 1
                   for witnesses in positive.values())
        negative = {prime: tuple(compose_rows(power, CHI[name][prime])
                                 for power in powers(rho)) for prime in (13, 19)}
        assert set(negative[13]).isdisjoint(negative[19])
        assert set(positive).isdisjoint(negative[13])
        assert set(positive).isdisjoint(negative[19])
        endpoint_records[name] = {
            "positive_patterns": [{"permutation": perm, "witnesses": witnesses,
                                   "unique_rotation": witnesses[0][0]}
                                  for perm, witnesses in sorted(positive.items())],
            "negative_reflection_cosets": negative,
            "positive_negative_disjoint": True,
            "negative_13_19_disjoint": True}
    return {"lines": line_records,
            "paired_patterns": [{"permutation_X": key[0], "permutation_Y": key[1],
                                 "witnesses": witnesses,
                                 "unique_rotation": witnesses[0][0]}
                                for key, witnesses in sorted(paired.items())],
            "paired_patterns_count": len(paired),
            "paired_rotation_conflicts": 0,
            "endpoint": endpoint_records}


def weighted_lift_extension():
    result = {}
    for kind, table in paired_lift_table().items():
        base = (1, 0) if kind == "E" else (1, 2)
        for row in table["patterns"]:
            matrix = row["twelve_w_matrix"]
            image = tuple(sum(matrix[i][j] * base[j] for j in range(2))
                          for i in range(2))
            assert image == tuple(12 * coordinate for coordinate in base)
        result["paired_" + kind] = {"patterns": len(table["patterns"]),
                                   "all_collision_branches_give_w_v": True}
    for kind, table in endpoint_lift_table().items():
        base = (1, 0) if kind == "E" else (1, 2)
        for row in table["patterns"]:
            matrix = row["twelve_w_matrix"]
            image = tuple(sum(matrix[i][j] * base[j] for j in range(2))
                          for i in range(2))
            assert image == tuple(12 * coordinate for coordinate in base)
        result["endpoint_" + kind] = {"patterns": len(table["patterns"]),
                                     "all_collision_branches_give_w_v": True}
    return result


if __name__ == "__main__":
    payload = {"status": "COMPUTED",
               "scope": "small exact coefficient tables; theorem fresh review pending",
               "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
               "local_dependencies_sha256": {
                   name: sha256((LOCAL_CERT / name).read_bytes()).hexdigest()
                   for name in ("six_prime_power_lifts.py", "six_prime_power_endpoint_lifts.py")},
               "moment_identities": moment_certificate(),
               "weighted_lift_extension": weighted_lift_extension(),
               "gluing": gluing_certificate()}
    path = ROOT / "results/2026-09-30-six-composite-global-attempt/certificate.json"
    path.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"paired_patterns": payload["gluing"]["paired_patterns_count"],
                      "paired_rotation_conflicts": 0,
                      "positive_endpoint_patterns_each": 57,
                      "endpoint_rotation_conflicts": 0,
                      "positive_negative_cosets_disjoint": True,
                      "weighted_collision_lift_branches_verified": 64}))
    print(json.dumps({"certificate": str(path),
                      "sha256": sha256(path.read_bytes()).hexdigest()}))
