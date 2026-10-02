"""Exact 40-pattern singular lift certificate, using only integer arithmetic."""
from collections import Counter
from hashlib import sha256
from itertools import permutations, product
import json
from math import gcd
from pathlib import Path

CX = ((2, -4), (5, -4), (-4, -1), (-4, 2), (2, 2), (-1, 5))
CY = ((-1, -4), (2, -4), (5, -1), (-4, 2), (2, 2), (-4, 5))
TWELVE_INVERSE_FIRST_TWO = ((-4, 4), (-5, 2))


def multiply(rows, matrix):
    return tuple(tuple(sum(row[h] * matrix[h][j] for h in range(2))
                       for j in range(2)) for row in rows)


def scalar_values(rows, v):
    return tuple(sum(row[j] * v[j] for j in range(2)) for row in rows)


def matching_perms(source, target, base, sign):
    values = scalar_values(source, base)
    target_values = scalar_values(target, base)
    return tuple(perm for perm in permutations(range(6))
                 if values == tuple(sign * target_values[j] for j in perm))


def egcd(a, b):
    if b == 0:
        return abs(a), 1 if a >= 0 else -1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def bezout(values):
    divisor = 0
    coefficients = []
    for value in values:
        new_divisor, old_factor, new_factor = egcd(divisor, value)
        coefficients = [old_factor * coefficient for coefficient in coefficients]
        coefficients.append(new_factor)
        divisor = new_divisor
    assert sum(x * y for x, y in zip(coefficients, values)) == divisor
    return divisor, coefficients


def certificate():
    result = {}
    for kind, base in (("E", (1, 0)), ("D", (1, 2))):
        records = []
        for swap in (0, 1):
            sign = 1 if kind == "E" or not swap else -1
            target_x, target_y = (CX, CY) if not swap else (CY, CX)
            perms_x = matching_perms(CX, target_x, base, sign)
            perms_y = matching_perms(CY, target_y, base, sign)
            assert len(perms_x) == len(perms_y) == (4 if kind == "E" else 2)
            assert not matching_perms(CX, target_x, base, -sign)
            assert not matching_perms(CY, target_y, base, -sign)
            for px, py in product(perms_x, perms_y):
                first_two = tuple(tuple(sign * x for x in target_x[px[i]])
                                  for i in (0, 1))
                matrix = multiply(TWELVE_INVERSE_FIRST_TWO, first_two)
                residuals = tuple(tuple(row[j] - 12 * sign * target_x[px[i]][j]
                                        for j in range(2))
                                  for i, row in enumerate(multiply(CX, matrix)))
                residuals += tuple(tuple(row[j] - 12 * sign * target_y[py[i]][j]
                                         for j in range(2))
                                   for i, row in enumerate(multiply(CY, matrix)))
                assert all(row[0] == (0 if kind == "E" else -2 * row[1])
                           for row in residuals)
                divisor, coefficients = bezout([row[1] for row in residuals])
                if divisor:
                    unit_part = divisor
                    for prime in (2, 3):
                        while unit_part % prime == 0:
                            unit_part //= prime
                    assert unit_part == 1
                    verdict = "actual collision: b=0" if kind == "E" else "actual collision: b=2a"
                else:
                    expected = ((12, 0), (0, 12)) if not swap else (
                        ((12, -12), (0, -12)) if kind == "E" else
                        ((-12, 12), (0, 12)))
                    assert matrix == expected
                    verdict = "w=v" if not swap else (
                        "w=R^2 T v" if kind == "E" else "w=-R^2 T v")
                records.append({"swap": swap, "sign": sign,
                                "permutation_X": px, "permutation_Y": py,
                                "twelve_w_matrix": matrix,
                                "residual_rows": residuals,
                                "residual_coefficient_gcd": divisor,
                                "gcd_bezout_coefficients": coefficients,
                                "verdict": verdict})
        assert len(records) == (32 if kind == "E" else 8)
        result[kind] = {"base": base, "patterns": records,
                        "gcd_histogram": dict(Counter(
                            rec["residual_coefficient_gcd"] for rec in records))}
    return result


if __name__ == "__main__":
    payload = {"status": "COMPUTED",
               "scope": "complete finite algebraic lift table; separately attacked in composite review",
               "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
               "tables": certificate()}
    path = Path(__file__).resolve().parents[1] / "results/2026-09-30-six-composite-algebra/lift-table.json"
    path.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({kind: {"patterns": len(value["patterns"]),
                            "gcd_histogram": value["gcd_histogram"]}
                      for kind, value in payload["tables"].items()}))
    print(json.dumps({"certificate": str(path),
                      "sha256": sha256(path.read_bytes()).hexdigest()}))
