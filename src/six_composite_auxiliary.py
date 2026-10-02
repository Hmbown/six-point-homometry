"""Auxiliary exact certificates; does not infer a theorem from finite counts."""
from collections import Counter, defaultdict
from functools import reduce
from hashlib import sha256
from itertools import combinations
import json
from math import gcd
from pathlib import Path
import sys
from time import monotonic

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import homometry

P = ((0, 0), (1, 0), (-2, 1), (-2, 2), (0, 2), (-1, 3))
Q = ((0, 0), (1, 0), (2, 1), (-1, 2), (1, 2), (-1, 3))
CX = ((2, -4), (5, -4), (-4, -1), (-4, 2), (2, 2), (-1, 5))
CY = ((-1, -4), (2, -4), (5, -1), (-4, 2), (2, 2), (-4, 5))
R = ((0, -1), (1, -1))
T = ((0, 1), (1, 0))


def mat_rows(rows, matrix):
    return tuple(tuple(sum(r[h] * matrix[h][j] for h in range(2))
                       for j in range(2)) for r in rows)


def parity(perm):
    return (-1) ** sum(perm[i] > perm[j] for i in range(6)
                      for j in range(i + 1, 6))


def formal_permutations():
    out = {}
    for name, rows, matrix, target in (
            ("rho_X", CX, R, CX), ("rho_Y", CY, R, CY),
            ("tau_X", CX, T, CY), ("tau_Y", CY, T, CX)):
        perm = tuple(target.index(row) for row in mat_rows(rows, matrix))
        assert parity(perm) == 1
        out[name] = list(perm)
    return out


def matchings(xs):
    if not xs:
        yield ()
        return
    a = xs[0]
    for b in xs[1:]:
        for tail in matchings(tuple(x for x in xs[1:] if x != b)):
            yield ((a, b),) + tail


def reflection_certificate():
    out = {}
    for name, coordinates in (("X", CX), ("Y", CY)):
        records = []
        for pairs in matchings(tuple(range(6))):
            rows = [tuple(coordinates[a][j] + coordinates[b][j]
                          for j in range(2)) for a, b in pairs]
            minors = [a[0] * b[1] - a[1] * b[0]
                      for a, b in combinations(rows, 2)]
            divisor = abs(reduce(gcd, minors, 0))
            assert divisor != 0
            records.append({"pairs": pairs, "sum_rows": rows,
                            "minors": minors, "minor_gcd": divisor})
        assert len(records) == 15
        out[name] = records
    return out


def image(rows, a, b, n):
    return tuple((x * a + y * b) % n for x, y in rows)


def anchored_canon(points, n):
    # Independent of the direct enumerator's cyclic-gap necklaces.
    return min(tuple(sorted(epsilon * (point - anchor) % n
                            for point in points))
               for epsilon in (1, -1) for anchor in points)


def orbit(v, n):
    a, b = v
    positives = ((a, b), (-b, a - b), (b - a, -a),
                 (b, a), (-a, b - a), (a - b, -b))
    return {(epsilon * x % n, epsilon * y % n)
            for x, y in positives for epsilon in (1, -1)}


def domain(a, b, n, factors, mode):
    if mode == "full":
        return True
    if mode == "faithful":
        return all(len(set(image(P, a, b, p))) == 6 and
                   len(set(image(Q, a, b, p))) == 6 for p, k in factors)
    e = a * b * (a - b)
    d = (a + b) * (2 * a - b) * (a - 2 * b)
    return gcd(e * d, n) == 1 and all(
        len(set(image(P, a, b, p ** k))) == 6 and
        len(set(image(Q, a, b, p ** k))) == 6 for p, k in factors)


def enumerate_domain(n, factors, mode):
    started = monotonic()
    fibers = defaultdict(list)
    congruent = []
    for a in range(n):
        for b in range(n):
            if not domain(a, b, n, factors, mode):
                continue
            x, y = image(P, a, b, n), image(Q, a, b, n)
            if len(set(x)) != 6 or len(set(y)) != 6:
                continue
            cx, cy = anchored_canon(x, n), anchored_canon(y, n)
            if cx == cy:
                congruent.append((a, b))
            else:
                fibers[tuple(sorted((cx, cy)))].append((a, b))
    records = []
    for pair, parameters in sorted(fibers.items()):
        assert set(parameters) == orbit(parameters[0], n)
        assert len(parameters) == 12
        for endpoint in pair:
            assert homometry.dihedral_canon(endpoint, n) == endpoint
        assert homometry.icv(pair[0], n) == homometry.icv(pair[1], n)
        records.append({"pair": pair, "parameters": parameters})
    assert not congruent
    return {"n": n, "factors": factors, "domain": mode,
            "parameters": sum(map(len, fibers.values())),
            "pairs": len(fibers), "congruent": congruent,
            "fiber_histogram": dict(Counter(map(len, fibers.values()))),
            "every_fiber_exactly_G": True,
            "reference_all_saved_endpoint_canons_and_icv": True,
            "seconds": round(monotonic() - started, 6), "fibers": records}


def main():
    output = {"status": "COMPUTED",
              "scope": "finite support controls and exact formal/reflection data; separate proof review",
              "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "reference_sha256": sha256((ROOT / "src/homometry.py").read_bytes()).hexdigest(),
              "formal_permutations": formal_permutations(),
              "reflection_matchings": reflection_certificate(),
              "partitions": []}
    for n, factors, mode in ((169, ((13, 2),), "full"),
                             (169, ((13, 2),), "faithful"),
                             (169, ((13, 2),), "regular"),
                             (221, ((13, 1), (17, 1)), "faithful")):
        record = enumerate_domain(n, factors, mode)
        output["partitions"].append(record)
        print(json.dumps({key: value for key, value in record.items()
                          if key != "fibers"}), flush=True)
    target = Path(__file__).resolve().parents[1] / "results/2026-09-30-six-composite-algebra/certificate.json"
    target.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"certificate": str(target),
                      "sha256": sha256(target.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()
