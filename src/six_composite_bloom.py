"""Direct cyclic-ring Bloom parameter enumeration, with exact singular fibres.

Every (a,b) in Z_n^2 is evaluated as labelled points.  The enumerator does
not use moments, CRT orbit identifications or a counting formula to group
images.  Rigid equivalence is independent translation/reflection on the two
endpoints, followed by endpoint interchange.  General units are not quotiented.
Compressed certificates retain every parameter, including excluded ones.
"""
from __future__ import annotations

import argparse
from array import array
from collections import Counter, defaultdict
from dataclasses import dataclass
import gzip
import hashlib
import json
from pathlib import Path
import pickle
import time
from typing import Callable, Iterable

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "composite-bloom-direct-v1"
Pair = tuple[tuple[int, ...], tuple[int, ...]]


def factors(n: int) -> tuple[tuple[int, int], ...]:
    """Prime factorization by trial division; validate before allocating."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 2:
        raise ValueError("modulus must be an integer at least two")
    remainder, divisor, result = n, 2, []
    while divisor * divisor <= remainder:
        exponent = 0
        while remainder % divisor == 0:
            remainder //= divisor
            exponent += 1
        if exponent:
            result.append((divisor, exponent))
        divisor += 1
    if remainder > 1:
        result.append((remainder, 1))
    return tuple(result)


def points(a: int, b: int, n: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Explicit labelled formulas; no import from the prime implementation."""
    return ((0, a % n, (b - 2*a) % n, (2*b - 2*a) % n,
             2*b % n, (3*b - a) % n),
            (0, a % n, (b + 2*a) % n, (2*b - a) % n,
             (2*b + a) % n, (3*b - a) % n))


def canonical(values: Iterable[int], n: int) -> tuple[int, ...]:
    """Direct anchored point comparison, pruning only by the second point.

    A minimal translate contains zero, and its next point is the smallest
    cyclic gap.  Evaluate all ties in both orientations.  Unlike a gap-word
    canonicalizer, the compared objects here are actual anchored point tuples.
    """
    if n < 1:
        raise ValueError("modulus must be positive")
    ordered = tuple(sorted({x % n for x in values}))
    if len(ordered) < 2:
        return (0,) if ordered else ()
    gaps = tuple(ordered[(i+1) % len(ordered)] - ordered[i]
                 if i+1 < len(ordered) else ordered[0] + n - ordered[i]
                 for i in range(len(ordered)))
    smallest = min(gaps)
    candidates = []
    for i, gap in enumerate(gaps):
        if gap == smallest:
            anchor = ordered[i]
            candidates.append(tuple(sorted((x-anchor) % n for x in ordered)))
            anchor = ordered[(i+1) % len(ordered)]
            candidates.append(tuple(sorted((anchor-x) % n for x in ordered)))
    return min(candidates)


def classify(a: int, b: int, n: int) -> tuple[str, Pair | None]:
    x, y = points(a, b, n)
    if len(set(x)) < 6 or len(set(y)) < 6:
        return "collision", None
    xx, yy = canonical(x, n), canonical(y, n)
    if xx == yy:
        return "congruent", None
    return "admissible", (xx, yy) if xx < yy else (yy, xx)


def parameter_orbit(a: int, b: int, n: int) -> set[int]:
    """The twelve formal parameter symmetries, used only after grouping images."""
    six = ((a, b), (-b, a-b), (b-a, -a),
           (b, a), (-a, b-a), (a-b, -b))
    return {(sign*x % n)*n + sign*y % n
            for x, y in six for sign in (1, -1)}


def local_support_profile(a: int, b: int, primes: tuple[int, ...]):
    """Unordered endpoint support sizes at each residue field."""
    return tuple(tuple(sorted((len(set(x)), len(set(y)))))
                 for p in primes for x, y in (points(a, b, p),))


def is_unit_separated(profile) -> bool:
    return all(sizes == (6, 6) for sizes in profile)


@dataclass
class Enumeration:
    n: int
    counts: Counter
    fibers: dict[Pair, array]
    excluded: dict[str, array]
    local_counts: Counter
    next_row: int = 0
    seconds: float = 0.0


def enumerate_composite(n: int, progress: Callable[[str], None] | None = None,
                        checkpoint: Path | None = None, resume: bool = False,
                        checkpoint_seconds: float = 20.0) -> Enumeration:
    """Evaluate n^2 labelled parameters; no symmetry reduction precedes grouping.

    Optional resumable gzip/pickle checkpoints are local implementation state,
    bound to this source digest.  Final public certificates are gzip JSON.
    Parameter codes a*n+b retain exact values with four bytes each internally.
    """
    prime_factors = factors(n)
    if n*n > 10_000_000:
        raise ValueError("parameter cap is ten million; benchmark before increasing")
    primes = tuple(p for p, _ in prime_factors)
    local_tables = {p: tuple(local_support_profile(a, b, (p,))[0]
                            for a in range(p) for b in range(p)) for p in primes}
    source_digest = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result = Enumeration(n, Counter(), {},
                         {"collision": array("I"), "congruent": array("I")}, Counter())
    if resume and checkpoint is not None and checkpoint.exists():
        with gzip.open(checkpoint, "rb") as stream:
            saved = pickle.load(stream)
        if saved["schema"] != SCHEMA or saved["source_sha256"] != source_digest:
            raise ValueError("checkpoint schema/source digest differs")
        result = saved["enumeration"]
        if result.n != n:
            raise ValueError("checkpoint modulus differs")
    started = time.monotonic()
    previous_seconds = result.seconds
    last_log = last_checkpoint = started
    for a in range(result.next_row, n):
        residues = tuple((a % p)*p for p in primes)
        for b in range(n):
            category, pair = classify(a, b, n)
            result.counts[category] += 1
            profile = tuple(local_tables[p][base + b % p]
                            for p, base in zip(primes, residues))
            result.local_counts[(profile, category)] += 1
            code = a*n + b
            if pair is None:
                result.excluded[category].append(code)
            else:
                fiber = result.fibers.get(pair)
                if fiber is None:
                    result.fibers[pair] = array("I", [code])
                else:
                    fiber.append(code)
        result.next_row = a+1
        now = time.monotonic()
        result.seconds = previous_seconds + now-started
        if progress and (now-last_log >= 5.0 or a+1 == n):
            progress(f"n={n} rows={a+1}/{n} pairs={len(result.fibers)} "
                     f"seconds={result.seconds:.3f}")
            last_log = now
        if checkpoint is not None and now-last_checkpoint >= checkpoint_seconds and a+1 < n:
            temporary = checkpoint.with_suffix(checkpoint.suffix + ".tmp")
            with gzip.open(temporary, "wb", compresslevel=1) as stream:
                pickle.dump({"schema": SCHEMA, "source_sha256": source_digest,
                             "enumeration": result}, stream, protocol=5)
            temporary.replace(checkpoint)
            last_checkpoint = time.monotonic()
            if progress:
                progress(f"n={n} checkpoint_row={a+1} bytes={checkpoint.stat().st_size}")
    assert sum(result.counts.values()) == n*n
    assert sum(map(len, result.fibers.values())) == result.counts["admissible"]
    return result


def graph_summary(pairs: Iterable[Pair]) -> dict:
    """Connected components of actual Bloom edges; no ICV-family claim."""
    ids, parent, degree = {}, array("I"), array("I")

    def find(index):
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    edges = 0
    for pair in pairs:
        ends = []
        for endpoint in pair:
            index = ids.get(endpoint)
            if index is None:
                index = len(parent)
                ids[endpoint] = index
                parent.append(index)
                degree.append(0)
            degree[index] += 1
            ends.append(index)
        parent[find(ends[0])] = find(ends[1])
        edges += 1
    sizes = Counter(find(i) for i in range(len(parent)))
    shared = [(endpoint, degree[index]) for endpoint, index in ids.items()
              if degree[index] > 1]
    return {"edges": edges, "endpoint_classes": len(ids),
            "degree_histogram": dict(sorted(Counter(degree).items())),
            "component_size_histogram": dict(sorted(Counter(sizes.values()).items())),
            "components": len(sizes), "shared_endpoint_classes": len(shared),
            "maximum_degree": max(degree, default=0),
            "shared_endpoint_examples": [{"endpoint": endpoint, "degree": d}
                                         for endpoint, d in sorted(shared)[:10]]}


def summarize(result: Enumeration) -> dict:
    """Audit exact fibres against G and describe every residue support stratum."""
    n = result.n
    prime_factors = factors(n)
    primes = tuple(p for p, _ in prime_factors)
    histogram, orbit_histogram, orbit_sizes = Counter(), Counter(), Counter()
    unit_histogram, unit_orbits = Counter(), Counter()
    strata = defaultdict(lambda: {"parameter_counts": Counter(), "pairs": 0,
                                 "fiber_histogram": Counter(), "G_orbit_histogram": Counter()})
    for (profile, category), count in result.local_counts.items():
        strata[profile]["parameter_counts"][category] = count
    unit_pairs = []
    exceptional = []
    for pair, codes in result.fibers.items():
        a, b = divmod(codes[0], n)
        profile = local_support_profile(a, b, primes)
        # Local support sizes are invariant under rigid equivalence/interchange.
        assert all(local_support_profile(*divmod(code, n), primes) == profile for code in codes)
        remaining, orbits = set(codes), 0
        while remaining:
            code = min(remaining)
            orbit = parameter_orbit(*divmod(code, n), n)
            assert orbit <= remaining, (n, code, orbit - remaining)
            remaining.difference_update(orbit)
            orbit_sizes[len(orbit)] += 1
            orbits += 1
        histogram[len(codes)] += 1
        orbit_histogram[orbits] += 1
        strata[profile]["pairs"] += 1
        strata[profile]["fiber_histogram"][len(codes)] += 1
        strata[profile]["G_orbit_histogram"][orbits] += 1
        if is_unit_separated(profile):
            unit_pairs.append(pair)
            unit_histogram[len(codes)] += 1
            unit_orbits[orbits] += 1
        if len(codes) != 12 or orbits != 1:
            exceptional.append({"pair": pair, "parameter_codes": codes,
                                "G_orbits": orbits, "local_support_sizes": profile})
    unit_parameters = sum(size*count for size, count in unit_histogram.items())
    candidate = None
    if all(p >= 13 for p in primes):
        numerator = 1
        for p, exponent in prime_factors:
            numerator *= p**(2*exponent-2)*(p-1)*(p-11)
        candidate = {"numerator": numerator, "denominator": 12,
                     "integral": numerator % 12 == 0,
                     "matches": 12*len(unit_pairs) == numerator}
    return {"n": n, "prime_factorization": prime_factors, "parameters": n*n,
            "collision_parameters": result.counts["collision"],
            "congruent_parameters": result.counts["congruent"],
            "admissible_parameters": result.counts["admissible"],
            "pairs": len(result.fibers), "fiber_histogram": dict(sorted(histogram.items())),
            "G_orbits_per_fiber_histogram": dict(sorted(orbit_histogram.items())),
            "G_orbit_size_histogram": dict(sorted(orbit_sizes.items())),
            "non12_fibers": sum(count for size, count in histogram.items() if size != 12),
            "fibers_not_single_G_orbits": sum(count for size, count in orbit_histogram.items() if size != 1),
            "unit_separated_parameters": unit_parameters, "unit_separated_pairs": len(unit_pairs),
            "unit_separated_fiber_histogram": dict(sorted(unit_histogram.items())),
            "unit_separated_G_orbits_per_fiber_histogram": dict(sorted(unit_orbits.items())),
            "unit_separated_candidate": candidate,
            "full_graph": graph_summary(result.fibers),
            "unit_separated_graph": graph_summary(unit_pairs),
            "local_support_strata": [{"support_sizes": profile, **values}
                                     for profile, values in sorted(strata.items())],
            "exceptional_fibers": exceptional, "enumeration_seconds": round(result.seconds, 6)}


def reference_parameter_pairs(n: int) -> dict[Pair, list[int]]:
    """Full independent image using the immutable reference and explicit formulas."""
    from homometry import dihedral_canon, icv
    fibers = defaultdict(list)
    for a in range(n):
        for b in range(n):
            x = tuple(sorted({0, a, (b-2*a) % n, (2*b-2*a) % n, 2*b % n, (3*b-a) % n}))
            y = tuple(sorted({0, a, (b+2*a) % n, (2*b-a) % n, (2*b+a) % n, (3*b-a) % n}))
            if len(x) != 6 or len(y) != 6:
                continue
            xx, yy = dihedral_canon(x, n), dihedral_canon(y, n)
            assert icv(xx, n) == icv(yy, n)
            if xx != yy:
                fibers[tuple(sorted((xx, yy)))].append(a*n+b)
    return dict(fibers)


def reference_controls(result: Enumeration, full_max: int = 43) -> dict:
    """Full parameter reference below the stated bound, representative controls above."""
    from homometry import dihedral_canon, icv
    if result.n <= full_max:
        actual = {pair: list(codes) for pair, codes in result.fibers.items()}
        expected = reference_parameter_pairs(result.n)
        assert actual == expected
        return {"method": "immutable dihedral_canon and icv; full parameter image",
                "full": True, "parameters": result.n**2, "pairs": len(expected)}
    pairs = sorted(result.fibers)
    selected = pairs[::max(1, len(pairs)//24)] if pairs else []
    for pair in selected:
        assert all(dihedral_canon(endpoint, result.n) == endpoint for endpoint in pair)
        assert icv(pair[0], result.n) == icv(pair[1], result.n)
    return {"method": "immutable dihedral_canon and icv; spread-out endpoints",
            "full": False, "pairs": len(selected)}


def json_default(value):
    if isinstance(value, array):
        return list(value)
    raise TypeError(type(value).__name__)


def save_certificate(result: Enumeration, summary: dict, path: Path, reference: dict):
    """Stream exact public JSON without expanding all parameter arrays at once."""
    metadata = {"schema": SCHEMA, "status": "COMPUTED",
                "scope": "Bloom parameter image only, not a census of six-subsets",
                "method": "all n^2 labelled point parameters; anchored rigid canonicalization",
                "equivalence": "unordered endpoint pair; independent translation/reflection; no unit quotient",
                "parameter_encoding": "code=a*n+b, a=code//n, b=code%n",
                "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "reference_sha256": hashlib.sha256((ROOT/"src/homometry.py").read_bytes()).hexdigest(),
                "summary": summary, "reference_controls": reference,
                "excluded_parameter_codes": result.excluded}
    temporary = path.with_suffix(path.suffix + ".tmp")
    with gzip.open(temporary, "wt", compresslevel=5) as stream:
        header = json.dumps(metadata, separators=(",", ":"), default=json_default)
        stream.write(header[:-1] + ',"fibers":[')
        primes = tuple(p for p, _ in factors(result.n))
        for index, pair in enumerate(sorted(result.fibers)):
            codes = result.fibers[pair]
            record = {"pair": pair, "parameter_codes": codes,
                      "local_support_sizes": local_support_profile(*divmod(codes[0], result.n), primes)}
            if index:
                stream.write(",")
            stream.write(json.dumps(record, separators=(",", ":"), default=json_default))
        stream.write("]}")
    temporary.replace(path)


def read_certificate(path: Path) -> dict:
    with gzip.open(path, "rt") as stream:
        return json.load(stream)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--moduli", nargs="+", type=int, default=[169, 221, 289])
    parser.add_argument("--out", type=Path, default=ROOT/"results/2026-09-30-six-composite-count")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--reference-max", type=int, default=43)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    source_digest = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    summaries = []
    with (args.out/"enumeration.log").open("a") as log:
        def progress(message):
            print(message, flush=True)
            log.write(message+"\n")
            log.flush()
        for n in args.moduli:
            path = args.out/f"n{n}.json.gz"
            checkpoint = args.out/f"n{n}.checkpoint.gz"
            if args.resume and path.exists():
                saved = read_certificate(path)
                if saved["source_sha256"] != source_digest:
                    raise ValueError(f"saved n{n} source digest differs")
                summaries.append(saved["summary"])
                progress(f"n={n} completed certificate reused")
                continue
            result = enumerate_composite(n, progress, checkpoint, args.resume)
            summary = summarize(result)
            reference = reference_controls(result, args.reference_max)
            save_certificate(result, summary, path, reference)
            if checkpoint.exists():
                checkpoint.unlink()
            summaries.append(summary)
            progress(f"n={n} complete pairs={summary['pairs']} "
                     f"unit_pairs={summary['unit_separated_pairs']} "
                     f"non12={summary['non12_fibers']} "
                     f"nonG={summary['fibers_not_single_G_orbits']} "
                     f"shared_endpoints={summary['full_graph']['shared_endpoint_classes']} "
                     f"certificate_bytes={path.stat().st_size}")
            del result
    combined = {"schema": SCHEMA, "status": "COMPUTED", "source_sha256": source_digest,
                "summaries": summaries}
    (args.out/"summary.json").write_text(json.dumps(combined, indent=2, default=json_default)+"\n")


if __name__ == "__main__":
    main()
