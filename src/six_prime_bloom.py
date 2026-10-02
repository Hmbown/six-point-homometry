"""Direct prime-field enumeration of the classical two-parameter Bloom image.

The counted object is an unordered pair of distinct T/I classes, with T/I
applied independently to each endpoint. Unit multiplication is never quotiented
out. This module enumerates parameters, not arbitrary six-subsets. Its output
retains every parameter in every fiber, and partitions excluded parameters into
support collisions and congruent endpoints. No counting formula is assumed.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations
import hashlib
import json
from math import gcd, isqrt
from pathlib import Path
import time
from typing import Callable, Iterable

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "prime-bloom-direct-v1"
X_COEFFICIENTS = ((0, 0), (1, 0), (-2, 1), (-2, 2), (0, 2), (-1, 3))
Y_COEFFICIENTS = ((0, 0), (1, 0), (2, 1), (-1, 2), (1, 2), (-1, 3))


def is_prime(p: int) -> bool:
    return isinstance(p, int) and not isinstance(p, bool) and p >= 2 and all(
        p % d for d in range(2, isqrt(p) + 1))


def bloom_points(a: int, b: int, p: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Return the six labelled coordinates on each side, including collisions."""
    return (tuple((u * a + v * b) % p for u, v in X_COEFFICIENTS),
            tuple((u * a + v * b) % p for u, v in Y_COEFFICIENTS))


def canonical(points: Iterable[int], n: int) -> tuple[int, ...]:
    """Lexicographic T/I canonical form via the dihedral cyclic-gap necklace.

    Each translation with lexicographically minimal coordinates must place a
    point at zero. Its cyclic gap word is a rotation of the original gap word;
    reflection reverses that word. Lexicographic order on anchored point tuples
    agrees with lexicographic order on gap words through cumulative sums. This
    avoids searching n translations, but performs no additional quotient.
    """
    if n < 1:
        raise ValueError("modulus must be positive")
    pts = tuple(sorted({point % n for point in points}))
    if not pts:
        return ()
    gaps = tuple(pts[i + 1] - pts[i] for i in range(len(pts) - 1)) + (
        pts[0] + n - pts[-1],)
    reverse = gaps[::-1]
    word = min(gaps[i:] + gaps[:i] for i in range(len(gaps)))
    word = min(word, min(reverse[i:] + reverse[:i] for i in range(len(gaps))))
    out = [0]
    for gap in word[:-1]:
        out.append(out[-1] + gap)
    return tuple(out)


def classify_parameter(a: int, b: int, p: int):
    """Return (collision/congruent/admissible, optional unordered pair)."""
    x, y = bloom_points(a, b, p)
    if len(set(x)) != 6 or len(set(y)) != 6:
        return "collision", None
    xx, yy = canonical(x, p), canonical(y, p)
    if xx == yy:
        return "congruent", None
    return "admissible", tuple(sorted((xx, yy)))


def integer_collision_lines() -> list[dict]:
    """Exact integer point-coincidence equations, grouped up to nonzero scale.

    Reducing these equations mod p (including small-characteristic collapse)
    gives all support exclusions. The retained endpoint/point witnesses make
    the equations directly checkable without relying on any proposed formula.
    """
    lines = defaultdict(list)
    for endpoint, coefficients in (("X", X_COEFFICIENTS), ("Y", Y_COEFFICIENTS)):
        for i, j in combinations(range(6), 2):
            u = coefficients[i][0] - coefficients[j][0]
            v = coefficients[i][1] - coefficients[j][1]
            raw = [u, v]
            divisor = gcd(abs(u), abs(v))
            u, v = u // divisor, v // divisor
            if u < 0 or (u == 0 and v < 0):
                u, v = -u, -v
            lines[u, v].append({"endpoint": endpoint, "points": [i, j],
                                "raw_coefficients": raw})
    return [{"coefficients": list(line), "witnesses": witnesses}
            for line, witnesses in sorted(lines.items())]


def enumerate_prime(p: int, progress: Callable[[str], None] | None = None) -> dict:
    """Enumerate all p^2 parameters and retain exact fibers of admissible pairs."""
    if not is_prime(p):
        raise ValueError(f"expected a prime modulus, got {p!r}")
    started = time.monotonic()
    counts = Counter()
    fibers = defaultdict(list)
    # Projective-direction checks describe exclusions, never identify pairs.
    directions = defaultdict(list)
    for a, b in [(0, 1)] + [(1, b) for b in range(p)]:
        category, _ = classify_parameter(a, b, p)
        directions[category].append([a, b])
    interval = max(1, p // 10)
    for a in range(p):
        for b in range(p):
            category, pair = classify_parameter(a, b, p)
            counts[category] += 1
            if pair is not None:
                fibers[pair].append((a, b))
        if progress and ((a + 1) % interval == 0 or a + 1 == p):
            progress(f"p={p} rows={a + 1}/{p} pairs={len(fibers)} "
                     f"seconds={time.monotonic() - started:.3f}")
    histogram = Counter(map(len, fibers.values()))
    # This consistency check follows only from homogeneity of the labelled
    # coordinates and invariance of rigid congruence under multiplication.
    assert sum(counts.values()) == p * p
    assert counts["collision"] == 1 + (p - 1) * len(directions["collision"])
    assert counts["congruent"] == (p - 1) * len(directions["congruent"])
    assert counts["admissible"] == (p - 1) * len(directions["admissible"])
    assert sum(size * count for size, count in histogram.items()) == counts["admissible"]
    records = [{"pair": [list(x), list(y)], "parameters": [list(v) for v in params]}
               for (x, y), params in sorted(fibers.items())]
    return {
        "schema": SCHEMA,
        "status": "COMPUTED",
        "method": "all prime-field parameters; cyclic-gap T/I canonicalization",
        "equivalence": "unordered endpoint pair; independent translation/reflection; no unit quotient",
        "summary": {
            "p": p, "parameters": p * p,
            "collision_parameters": counts["collision"],
            "six_distinct_parameters": p * p - counts["collision"],
            "congruent_parameters": counts["congruent"],
            "admissible_parameters": counts["admissible"],
            "pairs": len(fibers),
            "fiber_histogram": dict(sorted(histogram.items())),
            "non12_fibers": sum(count for size, count in histogram.items() if size != 12),
            "proposed_count_numerator": (p - 1) * (p - 11),
            "proposed_count_denominator": 12,
            "seconds": round(time.monotonic() - started, 6),
        },
        "exclusion_directions": {name: directions[name] for name in
                                 ("collision", "congruent", "admissible")},
        "integer_collision_lines": integer_collision_lines(),
        "fibers": records,
    }


def pairs_from_result(result: dict) -> set:
    return {tuple(tuple(endpoint) for endpoint in rec["pair"]) for rec in result["fibers"]}


def reference_parameter_pairs(p: int) -> dict:
    """Independent slow parameter image using immutable homometry.py.

    The reference checks all 2p rigid images directly, rather than using gap
    necklaces. The explicit coordinate formulas avoid calling bloom_points.
    """
    from homometry import dihedral_canon, icv
    pairs = defaultdict(list)
    for a in range(p):
        for b in range(p):
            x = tuple(sorted({0, a, (b - 2 * a) % p, (2 * b - 2 * a) % p,
                              2 * b % p, (3 * b - a) % p}))
            y = tuple(sorted({0, a, (b + 2 * a) % p, (2 * b - a) % p,
                              (2 * b + a) % p, (3 * b - a) % p}))
            if len(x) != 6 or len(y) != 6:
                continue
            xx, yy = dihedral_canon(x, p), dihedral_canon(y, p)
            if xx != yy:
                assert icv(xx, p) == icv(yy, p)
                pairs[tuple(sorted((xx, yy)))].append((a, b))
    return dict(pairs)


def compare_saved_census(result: dict) -> dict | None:
    """Verify membership in complete saved six-set census, if one exists."""
    p = result["summary"]["p"]
    candidates = [ROOT / f"results/2026-09-30-six-census/n{p}.json",
                  ROOT / f"results/2026-09-30-six-large-census/n{p}.json"]
    path = next((path for path in candidates if path.exists()), None)
    if path is None:
        return None
    raw = path.read_bytes()
    census = json.loads(raw)
    all_pairs = {tuple(sorted((tuple(a), tuple(b))))
                 for family in census["families"]
                 for a, b in combinations(family["members"], 2)}
    pairs = pairs_from_result(result)
    missing = pairs - all_pairs
    if missing:
        raise AssertionError(f"p={p}: Bloom pairs absent from saved census: {sorted(missing)[:2]}")
    return {"path": str(path.relative_to(ROOT)),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "source_methods": census.get("methods"),
            "all_bloom_pairs_present": True,
            "total_census_pairs": len(all_pairs),
            "census_pairs_outside_bloom": len(all_pairs - pairs),
            "census_non_bloom_pairs": [[list(a), list(b)] for a, b in sorted(all_pairs - pairs)]}


def parse_primes(values: list[str]) -> list[int]:
    out = set()
    for value in values:
        for piece in value.split(","):
            if ".." in piece:
                lo, hi = map(int, piece.split(".."))
                out.update(p for p in range(lo, hi + 1) if is_prime(p))
            else:
                p = int(piece)
                if not is_prime(p):
                    raise ValueError(f"expected a prime modulus, got {p}")
                out.add(p)
    if not out:
        raise ValueError("no primes requested")
    return sorted(out)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primes", nargs="+", default=["13..43"],
                        help="primes, comma lists or inclusive prime ranges such as 13..131")
    parser.add_argument("--out", type=Path,
                        default=ROOT / "results/2026-09-30-six-prime-count")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--reference-max", type=int, default=19)
    args = parser.parse_args()
    primes = parse_primes(args.primes)
    args.out.mkdir(parents=True, exist_ok=True)
    source_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    summaries = []
    log_path = args.out / "enumeration.log"
    with log_path.open("a") as log:
        def progress(message: str) -> None:
            print(message, flush=True)
            log.write(message + "\n")
            log.flush()
        for p in primes:
            path = args.out / f"p{p}.json"
            if args.resume and path.exists():
                result = json.loads(path.read_text())
                if result.get("schema") != SCHEMA or result.get("source_sha256") != source_hash:
                    raise ValueError(f"checkpoint schema/source mismatch: {path}")
                summaries.append(result["summary"])
                progress(f"p={p} resumed validated source checkpoint")
                continue
            progress(f"p={p} start exact parameter candidates={p*p}")
            result = enumerate_prime(p, progress)
            result["source_sha256"] = source_hash
            if p <= args.reference_max:
                expected = reference_parameter_pairs(p)
                actual = {tuple(tuple(x) for x in rec["pair"]):
                          [tuple(v) for v in rec["parameters"]] for rec in result["fibers"]}
                assert actual == expected, p
                result["reference_parameter_image"] = True
            else:
                result["reference_parameter_image"] = False
            result["saved_census_comparison"] = compare_saved_census(result)
            temp = path.with_suffix(".tmp")
            temp.write_text(json.dumps(result, sort_keys=True) + "\n")
            temp.replace(path)
            summaries.append(result["summary"])
            progress(json.dumps(result["summary"], sort_keys=True))
    (args.out / "summary.json").write_text(json.dumps({"schema": SCHEMA, "summaries": summaries},
                                                     indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
