"""Exact one-endpoint singular lift table, independent of paired constraints."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from six_prime_power_lifts import CX, CY, bezout, matching_perms, multiply


def certificate():
    output = {}
    for kind, base in (("E", (1, 0)), ("D", (1, 2))):
        records = []
        for source_name, source, inverse in (
                ("X", CX, ((-4, 4), (-5, 2))),
                ("Y", CY, ((-4, 4), (-2, -1)))):
            for target_name, target in (("X", CX), ("Y", CY)):
                cross = source_name != target_name
                sign = 1 if kind == "E" or not cross else -1
                perms = matching_perms(source, target, base, sign)
                assert len(perms) == (4 if kind == "E" else 2)
                assert not matching_perms(source, target, base, -sign)
                for perm in perms:
                    first_two = tuple(tuple(sign * x for x in target[perm[i]])
                                      for i in (0, 1))
                    matrix = multiply(inverse, first_two)
                    residuals = tuple(tuple(row[j] - 12 * sign * target[perm[i]][j]
                                            for j in range(2))
                                      for i, row in enumerate(multiply(source, matrix)))
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
                        expected = ((12, 0), (0, 12)) if not cross else (
                            ((12, -12), (0, -12)) if kind == "E" else
                            ((-12, 12), (0, 12)))
                        assert matrix == expected
                        verdict = "w=v" if not cross else (
                            "w=R^2 T v" if kind == "E" else "w=-R^2 T v")
                    records.append({"source": source_name, "target": target_name,
                                    "sign": sign, "permutation": perm,
                                    "twelve_w_matrix": matrix,
                                    "residual_rows": residuals,
                                    "residual_coefficient_gcd": divisor,
                                    "gcd_bezout_coefficients": coefficients,
                                    "verdict": verdict})
        assert len(records) == (16 if kind == "E" else 8)
        output[kind] = {"patterns": records,
                        "gcd_histogram": dict(Counter(
                            rec["residual_coefficient_gcd"] for rec in records))}
    return output


if __name__ == "__main__":
    payload = {"status": "COMPUTED",
               "scope": "one-endpoint lift table; prime31 excluded upstream",
               "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
               "tables": certificate()}
    path = Path(__file__).resolve().parents[1] / "results/2026-09-30-six-composite-algebra/endpoint-lift-table.json"
    path.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({kind: {"patterns": len(value["patterns"]),
                            "gcd_histogram": value["gcd_histogram"]}
                      for kind, value in payload["tables"].items()}))
    print(json.dumps({"certificate": str(path),
                      "sha256": sha256(path.read_bytes()).hexdigest()}))
