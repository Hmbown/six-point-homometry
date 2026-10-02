"""Exact support counts for the classical six-point family at every modulus.

This counts parameters with two six-element supports, including congruent
endpoints. It does not itself count homometric pair classes. The elementary
overlap argument and the independently computed Smith inclusion-exclusion
formula are deliberately separate implementations.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from math import gcd
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[1]
X = ((0, 0), (1, 0), (-2, 1), (-2, 2), (0, 2), (-1, 3))
Y = ((0, 0), (1, 0), (2, 1), (-1, 2), (1, 2), (-1, 3))
# Three doubled normals subsume their primitive occurrences. The remaining
# normals have no omitted nonunit factor.
KERNELS = ((0, 2), (1, -3), (1, -2), (2, -2), (1, 1), (1, 2),
           (2, -3), (2, -1), (2, 0), (2, 1), (3, -2), (3, -1))
OVERCOUNTS = {2: 15, 3: 16, 4: 18, 5: 24, 6: 12, 7: 24, 8: 12}


def modulus(n: int) -> int:
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("positive integer modulus required")
    return n


def support_count(n: int) -> int:
    """All support-admissible parameter locations, not pair classes."""
    modulus(n)
    return (n*n - (9 + 3*gcd(n, 2))*n + 11 +
            sum(c for m, c in OVERCOUNTS.items() if n % m == 0))


def support_admissible(a: int, b: int, n: int) -> bool:
    modulus(n)
    return all((u*a + v*b) % n != 0 for u, v in KERNELS)


def point_support_admissible(a: int, b: int, n: int) -> bool:
    """A separate actual-point implementation for the audit."""
    modulus(n)
    return all(len({(u*a + v*b) % n for u, v in rows}) == 6
               for rows in (X, Y))


def raw_normals(rows):
    result = set()
    for (u, v), (x, y) in combinations(rows, 2):
        a, b = u-x, v-y
        if a < 0 or (a == 0 and b < 0):
            a, b = -a, -b
        result.add((a, b))
    return tuple(sorted(result))


def primitive_order_table():
    """All exact-order m coordinates for every possible overlap order."""
    result = {}
    for m in range(2, 9):
        histogram = Counter()
        multiple = []
        for a in range(m):
            for b in range(m):
                if gcd(gcd(a, b), m) != 1:
                    continue
                memberships = [i for i, (u, v) in enumerate(KERNELS)
                               if (u*a + v*b) % m == 0]
                histogram[len(memberships)] += 1
                if len(memberships) >= 2:
                    multiple.append({"parameter": [a, b], "kernels": memberships})
        overcount = sum((r-1)*c for r, c in histogram.items() if r >= 2)
        result[m] = {"histogram": dict(sorted(histogram.items())),
                     "overcount": overcount, "multiple_memberships": multiple}
    return result


@lru_cache(maxsize=1)
def smith_weights():
    """Independent 4096-subset kernel count, retaining nonprimitive rows."""
    weights = Counter()
    for size in range(1, len(KERNELS)+1):
        for subset in combinations(KERNELS, size):
            content = 0
            for a, b in subset:
                content = gcd(content, gcd(a, b))
            minors = 0
            for (a, b), (c, d) in combinations(subset, 2):
                minors = gcd(minors, abs(a*d-b*c))
            rank = 1 if minors == 0 else 2
            second = 0 if minors == 0 else minors // content
            weights[rank, content, second] += (-1)**size
    return dict(sorted((k, c) for k, c in weights.items() if c))


def smith_count(n: int) -> int:
    modulus(n)
    result = n*n
    for (rank, first, second), weight in smith_weights().items():
        result += weight*gcd(n, first)*(n if rank == 1 else gcd(n, second))
    return result


def audit(nmax: int):
    started = time.monotonic()
    if not 1 <= nmax <= 256:
        raise ValueError("direct parameter audit bound must lie in 1..256")
    order_table = primitive_order_table()
    assert {m: r["overcount"] for m, r in order_table.items()} == OVERCOUNTS
    assert raw_normals(X) == raw_normals(Y)
    expected_raw = set(KERNELS) | {(0, 1), (1, 0), (1, -1)}
    assert set(raw_normals(X)) == expected_raw
    rows = []
    for n in range(1, nmax+1):
        count = 0
        for a in range(n):
            for b in range(n):
                literal = point_support_admissible(a, b, n)
                assert literal == support_admissible(a, b, n), (n, a, b)
                count += literal
        assert count == support_count(n) == smith_count(n), (n, count)
        rows.append({"n": n, "candidate_parameters": n*n, "six_support_parameters": count})
        if n % 25 == 0:
            print(f"audited n=1..{n} seconds={time.monotonic()-started:.3f}", flush=True)
    return {"schema": "six-bloom-all-modulus-support-v1", "status": "COMPUTED",
            "scope": "parameter supports; congruence and pair fibers not assumed",
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "kernels": KERNELS, "raw_normals_X": raw_normals(X),
            "raw_normals_Y": raw_normals(Y), "order_table": order_table,
            "smith_weights": [{"rank": rank, "first": first, "second": second,
                               "coefficient": c}
                              for (rank, first, second), c in smith_weights().items()],
            "parameters_audited": sum(r["candidate_parameters"] for r in rows),
            "direct_moduli": rows, "seconds": round(time.monotonic()-started, 6)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nmax", type=int, default=135)
    parser.add_argument("--out", type=Path, default=ROOT/"results/2026-10-01-six-bloom-support")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    result = audit(args.nmax)
    path = args.out/"certificate.json"
    path.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: result[k] for k in ("schema", "parameters_audited", "seconds")}))


if __name__ == "__main__":
    main()
