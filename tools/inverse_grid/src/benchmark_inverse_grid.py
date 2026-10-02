"""Bounded, reproducible sparse-grid reconstruction examples; standard library only."""
from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import random

from inverse_grid import Problem, canonical, solve, source_digest, verify_result


def literal_counts(points, shape):
    """Separate literal arithmetic, without the solver's correlation helper."""
    return Counter(tuple((a[i]-b[i]) % shape[i] for i in range(len(shape)))
                   for a in points for b in points)


def reference_classes(points, n):
    """Exhaust all raw subsets on a small circle, with all ambient symmetries."""
    target = literal_counts(points, (n,))
    found = set()
    for row in combinations(range(n), len(points)):
        candidate = tuple((x,) for x in row)
        if literal_counts(candidate, (n,)) != target:
            continue
        found.add(min(tuple(sorted(((sign*x+shift) % n,) for x in row))
                      for shift in range(n) for sign in (1, -1)))
    return found


def cases():
    bloom = [[x] for x in (0, 1, 4, 10, 12, 17)]
    rng = random.Random(20261001)
    return [
        ("tetrachord-12", [12], [[x] for x in (0, 1, 4, 6)], "independent_raw_subsets"),
        ("eight-sites-16", [16], [[x] for x in (0, 1, 2, 4, 7, 8, 9, 13)], "independent_raw_subsets"),
        ("bloom-billion", [1_000_000_007], bloom, "two_explicit_classes_plus_bounded_tests"),
        ("bloom-three-dimensions", [1_000_000_007, 1_000_000_009, 1_000_000_021],
         [[p[0], 0, 0] for p in bloom], "two_explicit_classes_plus_bounded_tests"),
        ("ten-sites-billion", [1_000_000_007], [[x] for x in sorted(rng.sample(range(100000), 10))],
         "per_solution_validity_and_source_inclusion"),
        ("twelve-sites-three-dimensions", [1_000_000_007, 1_000_000_009, 1_000_000_021],
         [[rng.randrange(100000) for _ in range(3)] for _ in range(12)],
         "per_solution_validity_and_source_inclusion"),
        ("limit-demonstration", [31], [[x] for x in sorted(rng.sample(range(31), 15))],
         "per_solution_validity_only_for_partial_search"),
    ]


def run_case(name, shape, points, validation, out, max_nodes, timeout):
    problem = Problem.from_points(shape, points)
    # The final case deliberately demonstrates an honest partial result.
    limit = min(max_nodes, 100) if name == "limit-demonstration" else max_nodes
    result = solve(problem, max_nodes=limit, timeout=timeout)
    verify_result(result)
    actual = {tuple(tuple(p) for p in row) for row in result["solutions"]}
    target = literal_counts(points, shape)
    if any(literal_counts(row, shape) != target for row in actual):
        raise AssertionError("Independent literal counts reject a returned arrangement.")
    if result["complete"] and canonical(tuple(tuple(p) for p in points), tuple(shape)) not in actual:
        raise AssertionError("A complete search omitted its known source arrangement.")
    expected = None
    if validation == "independent_raw_subsets":
        expected = reference_classes(points, shape[0])
    elif validation == "two_explicit_classes_plus_bounded_tests":
        expected = {canonical(tuple((x,)+(0,)*(len(shape)-1) for x in row), tuple(shape))
                    for row in ((0, 1, 4, 10, 12, 17), (0, 1, 8, 11, 13, 17))}
    if expected is not None and (not actual <= expected or (result["complete"] and actual != expected)):
        raise AssertionError("Returned classes disagree with independent/explicit controls.")
    directory = out/name
    directory.mkdir(parents=True, exist_ok=True)
    for filename, content in (("input.json", problem.document()), ("result.json", result),
                              ("checkpoint.json", result["checkpoint"])):
        (directory/filename).write_text(json.dumps(content, indent=2)+"\n")
    return {"name": name, "shape": shape, "cardinality": problem.cardinality,
            "grid_sites": result["grid_sites"], "complete": result["complete"],
            "termination": result["termination"], "classes_found": len(actual),
            "validation": validation, "stats": result["stats"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-nodes", type=int, default=100_000)
    parser.add_argument("--timeout", type=float, default=5)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    summaries = []
    for case in cases():
        summary = run_case(*case, args.out, args.max_nodes, args.timeout)
        summaries.append(summary)
        print(json.dumps(summary), flush=True)
        (args.out/"summary.json").write_text(json.dumps({
            "solver_sha256": source_digest(), "seed": 20261001,
            "max_nodes_per_case": args.max_nodes, "soft_seconds_per_case": args.timeout,
            "cases": summaries,
            "scope": "Local measurements; no efficient worst-case bound or independent large-grid classification."
        }, indent=2)+"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
