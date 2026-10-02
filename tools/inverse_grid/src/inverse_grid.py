"""Exact sparse binary reconstruction on finite periodic grids.

A grid is a product of cyclic groups. Missing displacement bins mean zero,
not unmeasured data. Search is exhaustive when complete=True; limits return
partial results and a resumable state. No floating point or dense grid array.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
from itertools import combinations
import json
from math import prod
from pathlib import Path
import sys
import time
from typing import Callable

Point = tuple[int, ...]
INPUT_SCHEMA = "homometry.grid-input/v1"
RESULT_SCHEMA = "homometry.grid-result/v1"
STATE_SCHEMA = "homometry.grid-checkpoint/v1"


def _integer(value: object) -> bool:
    return type(value) is int


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


_LOADED_SOURCE_DIGEST = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def source_digest() -> str:
    """Identify the source loaded by this process, even if its file is edited."""
    return _LOADED_SOURCE_DIGEST


def displacement(a: Point, b: Point, shape: Point) -> Point:
    return tuple((x-y) % n for x, y, n in zip(a, b, shape))


def point(value: object, shape: Point) -> Point:
    if not isinstance(value, (list, tuple)) or len(value) != len(shape):
        raise ValueError("Each coordinate must match the grid dimension.")
    if any(not _integer(x) or not 0 <= x < n for x, n in zip(value, shape)):
        raise ValueError("Coordinates must be integers in their canonical grid range.")
    return tuple(value)


def canonical(points: tuple[Point, ...], shape: Point) -> tuple[Point, ...]:
    """Translation/global-inversion orbit; no extra rotations or multipliers."""
    if not points:
        return ()
    return min(tuple(sorted(tuple((sign*(x-y)) % n for x, y, n in zip(a, anchor, shape))
                            for a in points))
               for anchor in points for sign in (1, -1))


def correlation(points: tuple[Point, ...], shape: Point) -> Counter:
    return Counter(displacement(a, b, shape) for a in points for b in points)


@dataclass(frozen=True)
class Problem:
    shape: Point
    bins: tuple[tuple[Point, int], ...]

    @property
    def counts(self) -> dict[Point, int]:
        return dict(self.bins)

    @property
    def zero(self) -> Point:
        return (0,) * len(self.shape)

    @property
    def cardinality(self) -> int:
        return self.counts.get(self.zero, 0)

    def document(self) -> dict:
        return {"schema": INPUT_SCHEMA, "shape": list(self.shape),
                "pair_counts": [{"shift": list(p), "count": c} for p, c in self.bins]}

    @property
    def fingerprint(self) -> str:
        return _digest(self.document())

    @classmethod
    def read(cls, data: dict) -> "Problem":
        if not isinstance(data, dict) or data.get("schema") != INPUT_SCHEMA:
            raise ValueError("Expected a homometry.grid-input/v1 object.")
        shape = data.get("shape")
        if not isinstance(shape, list) or not shape or any(not _integer(n) or n < 1 for n in shape):
            raise ValueError("Shape must be a nonempty list of positive integers.")
        shape = tuple(shape)
        rows = data.get("pair_counts")
        if not isinstance(rows, list):
            raise ValueError("pair_counts must be a list of displacement/count records.")
        counts = {}
        seen = set()
        for row in rows:
            if not isinstance(row, dict) or set(row) != {"shift", "count"}:
                raise ValueError("A pair-count record needs exactly shift and count.")
            p = point(row["shift"], shape)
            c = row["count"]
            if p in seen or not _integer(c) or c < 0:
                raise ValueError("Displacements must be unique and counts nonnegative integers.")
            seen.add(p)
            if c:
                counts[p] = c
        zero = (0,) * len(shape)
        k = counts.get(zero, 0)
        if k > prod(shape) or sum(counts.values()) != k*k:
            raise ValueError("Binary pair counts require C(0)=k and total mass k squared.")
        for p, c in counts.items():
            negative = displacement(zero, p, shape)
            if c > k or counts.get(negative, 0) != c:
                raise ValueError("Binary pair counts require inversion symmetry and counts at most k.")
            if p != zero and p == negative and c % 2:
                raise ValueError("A nonzero self-inverse displacement has an even directed count.")
        return cls(shape, tuple(sorted(counts.items())))

    @classmethod
    def from_points(cls, shape: list[int], values: list[list[int]]) -> "Problem":
        if not isinstance(shape, list) or not shape or any(not _integer(n) or n < 1 for n in shape):
            raise ValueError("Shape must be a nonempty list of positive integers.")
        shape_tuple = tuple(shape)
        points = tuple(point(p, shape_tuple) for p in values)
        if len(set(points)) != len(points):
            raise ValueError("Binary arrangements require distinct occupied sites.")
        counts = correlation(points, shape_tuple)
        return cls.read({"schema": INPUT_SCHEMA, "shape": shape,
                         "pair_counts": [{"shift": list(p), "count": c}
                                         for p, c in sorted(counts.items())]})


def _residual(prefix: tuple[Point, ...], problem: Problem) -> dict[Point, int] | None:
    residual = {p: c for p, c in problem.bins if p != problem.zero}
    for p, c in correlation(prefix, problem.shape).items():
        if p == problem.zero:
            continue
        if c > residual.get(p, 0):
            return None
        residual[p] -= c
        if not residual[p]:
            del residual[p]
    return residual


def _cost(p: Point, prefix: tuple[Point, ...], shape: Point) -> Counter:
    costs = Counter()
    for a in prefix:
        costs[displacement(p, a, shape)] += 1
        costs[displacement(a, p, shape)] += 1
    return costs


def _capacity(prefix: tuple[Point, ...], candidates: tuple[Point, ...],
              shape: Point) -> Counter:
    """Optimistic capacity using ALL candidates, including mutually incompatible ones."""
    capacity = Counter()
    for p in candidates:
        capacity.update(_cost(p, prefix, shape))
    for a, b in combinations(candidates, 2):
        capacity[displacement(a, b, shape)] += 1
        capacity[displacement(b, a, shape)] += 1
    return capacity


def _state(problem: Problem, stack: list, solutions: set, stats: dict) -> dict:
    payload = {"schema": STATE_SCHEMA, "input_sha256": problem.fingerprint,
               "solver_sha256": source_digest(), "stack": [[list(p) for p in row] for row in stack],
               "solutions": [[list(p) for p in row] for row in sorted(solutions)], "stats": stats}
    return {**payload, "state_sha256": _digest(payload)}


def _restore(problem: Problem, saved: dict) -> tuple[list, set, dict]:
    if not isinstance(saved, dict):
        raise ValueError("Checkpoint must be an object.")
    payload = {k: v for k, v in saved.items() if k != "state_sha256"}
    if saved.get("state_sha256") != _digest(payload):
        raise ValueError("Checkpoint checksum mismatch.")
    if (saved.get("schema") != STATE_SCHEMA or saved.get("input_sha256") != problem.fingerprint
            or saved.get("solver_sha256") != source_digest()):
        raise ValueError("Checkpoint belongs to a different target or solver revision.")
    stack = [tuple(point(p, problem.shape) for p in row) for row in saved["stack"]]
    solutions = {tuple(point(p, problem.shape) for p in row) for row in saved["solutions"]}
    if len(stack) != len(set(stack)) or len(solutions) != len(saved["solutions"]):
        raise ValueError("Checkpoint has duplicate states or solutions.")
    for prefix in stack:
        if (len(prefix) > problem.cardinality or tuple(sorted(set(prefix))) != prefix
                or (prefix and prefix[0] != problem.zero) or _residual(prefix, problem) is None):
            raise ValueError("Checkpoint has an invalid partial arrangement.")
        if problem.cardinality and not prefix:
            raise ValueError("Nonempty targets must have an anchored checkpoint.")
    for solution in solutions:
        if (len(solution) != problem.cardinality or canonical(solution, problem.shape) != solution
                or correlation(solution, problem.shape) != problem.counts):
            raise ValueError("Checkpoint has an invalid solution.")
    stats = saved["stats"]
    required = {"nodes", "budget_rejections", "candidate_prunes", "capacity_prunes", "matching_leaves"}
    if not isinstance(stats, dict) or set(stats) != required or any(not _integer(v) or v < 0 for v in stats.values()):
        raise ValueError("Checkpoint counters must be nonnegative integers.")
    return stack, solutions, dict(stats)


def _expand_node(prefix: tuple[Point, ...], problem: Problem, support: tuple[Point, ...]):
    """Prepare a node expansion without changing the saved search frontier."""
    changes = dict(nodes=1, budget_rejections=0, candidate_prunes=0,
                   capacity_prunes=0, matching_leaves=0)
    residual = _residual(prefix, problem)
    if residual is None:
        changes["budget_rejections"] += 1
        return [], None, changes
    needed = problem.cardinality-len(prefix)
    if not needed:
        solution = canonical(prefix, problem.shape) if not residual else None
        changes["matching_leaves"] = int(solution is not None)
        return [], solution, changes
    candidates = []
    for p in support:
        if p <= prefix[-1]:
            continue
        costs = _cost(p, prefix, problem.shape)
        if all(c <= residual.get(delta, 0) for delta, c in costs.items()):
            candidates.append(p)
        else:
            changes["budget_rejections"] += 1
    if len(candidates) < needed:
        changes["candidate_prunes"] += 1
        return [], None, changes
    # A safe optional prune. Large supports skip it; completeness is unchanged.
    if len(candidates) <= 48:
        capacity = _capacity(prefix, tuple(candidates), problem.shape)
        if any(c > capacity.get(delta, 0) for delta, c in residual.items()):
            changes["capacity_prunes"] += 1
            return [], None, changes
    # Only the first len(candidates)-needed+1 can start a completion.
    children = [prefix+(p,) for p in reversed(candidates[:len(candidates)-needed+1])]
    return children, None, changes


def solve(problem: Problem, *, max_nodes: int | None = None, timeout: float | None = None,
          max_solutions: int | None = None, resume: dict | None = None,
          progress: Callable[[dict], None] | None = None) -> dict:
    """Recover every binary translation/inversion class, or honestly stop early.

    Time limits are checked between nodes. Checkpoints detect accidental edits
    and bind the target/source; they are trusted search states, not adversarial
    completeness proofs. Fresh replay is the completeness verification route.
    """
    if max_nodes is not None and (not _integer(max_nodes) or max_nodes < 0):
        raise ValueError("max_nodes must be a nonnegative integer.")
    if timeout is not None and (not isinstance(timeout, (int, float)) or isinstance(timeout, bool)
                                or timeout < 0 or timeout != timeout or timeout == float("inf")):
        raise ValueError("timeout must be finite and nonnegative.")
    if max_solutions is not None and (not _integer(max_solutions) or max_solutions < 1):
        raise ValueError("max_solutions must be a positive integer.")
    if resume is None:
        stack = [(problem.zero,)] if problem.cardinality else [()]
        solutions = set()
        stats = dict(nodes=0, budget_rejections=0, candidate_prunes=0, capacity_prunes=0, matching_leaves=0)
    else:
        stack, solutions, stats = _restore(problem, resume)
    starting_nodes = stats["nodes"]
    support = tuple(p for p, c in problem.bins if p != problem.zero)
    started = time.monotonic()
    last_progress = started
    reason = "exhausted"
    active_prefix = None
    active_base = 0
    active_stats = None
    try:
        while stack:
            elapsed = time.monotonic()-started
            if max_nodes is not None and stats["nodes"]-starting_nodes >= max_nodes:
                reason = "node_limit"; break
            if timeout is not None and elapsed >= timeout:
                reason = "time_limit"; break
            if max_solutions is not None and len(solutions) >= max_solutions:
                reason = "solution_limit"; break
            if progress and time.monotonic()-last_progress >= 1:
                progress({"nodes": stats["nodes"], "pending": len(stack), "solutions": len(solutions),
                          "seconds": elapsed})
                last_progress = time.monotonic()
            # Keep the current branch until its full expansion has committed.
            active_stats = dict(stats)
            active_base = len(stack)-1
            active_prefix = stack[-1]
            children, solution, changes = _expand_node(active_prefix, problem, support)
            stack[active_base:] = children
            if solution is not None:
                solutions.add(solution)
            for key, change in changes.items():
                stats[key] += change
            active_prefix = None
    except KeyboardInterrupt:
        if active_prefix is not None:
            # Replay the whole active node. An already-added valid solution is
            # harmless because solutions are a set; unfinished work is retained.
            stack[active_base:] = [active_prefix]
            stats = active_stats
        reason = "interrupted"
    complete = not stack
    if complete:
        reason = "exhausted"
    return {"schema": RESULT_SCHEMA, "input": problem.document(), "input_sha256": problem.fingerprint,
            "solver_sha256": source_digest(), "equivalence": "translation_and_global_inversion",
            "cardinality": problem.cardinality, "grid_sites": prod(problem.shape),
            "complete": complete, "termination": reason,
            "solutions": [[list(p) for p in row] for row in sorted(solutions)],
            "stats": {**stats, "nodes_this_run": stats["nodes"]-starting_nodes,
                      "seconds_this_run": time.monotonic()-started,
                      "initial_support_candidates": len(support)},
            "checkpoint": _state(problem, stack, solutions, stats)}


def verify_result(result: dict, *, recompute: bool = False, max_nodes: int | None = None,
                  timeout: float | None = None) -> dict:
    """Check each arrangement; optionally fresh-replay the completeness assertion."""
    if not isinstance(result, dict) or result.get("schema") != RESULT_SCHEMA:
        raise ValueError("Expected a homometry.grid-result/v1 object.")
    problem = Problem.read(result["input"])
    if (result.get("input_sha256") != problem.fingerprint or result.get("cardinality") != problem.cardinality
            or result.get("grid_sites") != prod(problem.shape)
            or result.get("equivalence") != "translation_and_global_inversion"
            or type(result.get("complete")) is not bool
            or result.get("termination") not in {"exhausted", "node_limit", "time_limit",
                                                "solution_limit", "interrupted"}
            or result["complete"] != (result.get("termination") == "exhausted")):
        raise ValueError("Result metadata does not match its input.")
    solutions = []
    for row in result["solutions"]:
        pts = tuple(point(p, problem.shape) for p in row)
        if (len(pts) != problem.cardinality or len(set(pts)) != len(pts)
                or canonical(pts, problem.shape) != pts or correlation(pts, problem.shape) != problem.counts):
            raise ValueError("Invalid or noncanonical reconstructed arrangement.")
        solutions.append(pts)
    if solutions != sorted(set(solutions)):
        raise ValueError("Solutions must be ordered without duplicates.")
    verified = False
    replay = None
    if recompute:
        replay = solve(problem, max_nodes=max_nodes, timeout=timeout)
        expected = {tuple(tuple(p) for p in row) for row in replay["solutions"]}
        if not set(solutions) <= expected and replay["complete"]:
            raise ValueError("Fresh replay disagrees with listed solutions.")
        if result["complete"] and replay["complete"]:
            if set(solutions) != expected:
                raise ValueError("Claimed complete result omitted arrangements.")
            verified = True
    return {"solutions_valid": True, "classes": len(solutions),
            "completeness_verified_by_fresh_replay": verified,
            "replay_complete": replay["complete"] if replay else None}


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name+".tmp")
    temporary.write_text(json.dumps(data, indent=2)+"\n")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    make = commands.add_parser("target", help="Make exact pair counts from occupied points.")
    make.add_argument("--shape", required=True, help="Comma-separated grid periods.")
    make.add_argument("--points", required=True, help="Semicolon-separated points; coordinates use commas.")
    make.add_argument("--out", type=Path, required=True)
    recover = commands.add_parser("solve", help="Recover all compatible binary arrangements.")
    recover.add_argument("--input", type=Path, required=True)
    recover.add_argument("--out", type=Path, required=True)
    recover.add_argument("--checkpoint", type=Path)
    recover.add_argument("--resume", type=Path)
    recover.add_argument("--max-nodes", type=int, default=1_000_000)
    recover.add_argument("--timeout", type=float, default=60.0)
    recover.add_argument("--max-solutions", type=int)
    verify = commands.add_parser("verify", help="Check results; fresh replay can check completeness.")
    verify.add_argument("--input", type=Path, required=True)
    verify.add_argument("--recompute", action="store_true")
    verify.add_argument("--max-nodes", type=int, default=1_000_000)
    verify.add_argument("--timeout", type=float, default=60.0)
    args = parser.parse_args()
    try:
        if args.command == "target":
            shape = [int(x) for x in args.shape.split(",")]
            values = [[int(x) for x in row.split(",")] for row in args.points.split(";") if row]
            problem = Problem.from_points(shape, values)
            _write(args.out, problem.document())
            print(json.dumps({"cardinality": problem.cardinality, "pair_bins": len(problem.bins)}))
        elif args.command == "solve":
            problem = Problem.read(json.loads(args.input.read_text()))
            saved = json.loads(args.resume.read_text()) if args.resume else None
            result = solve(problem, max_nodes=args.max_nodes, timeout=args.timeout,
                           max_solutions=args.max_solutions, resume=saved,
                           progress=lambda p: print(json.dumps(p), file=sys.stderr, flush=True))
            _write(args.out, result)
            if args.checkpoint:
                _write(args.checkpoint, result["checkpoint"])
            print(json.dumps({"complete": result["complete"], "termination": result["termination"],
                              "classes": len(result["solutions"]), "nodes": result["stats"]["nodes"],
                              "seconds": result["stats"]["seconds_this_run"]}))
        else:
            print(json.dumps(verify_result(json.loads(args.input.read_text()), recompute=args.recompute,
                                           max_nodes=args.max_nodes, timeout=args.timeout)))
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError) as error:
        print(str(error), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
