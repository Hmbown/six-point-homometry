"""Fresh literal-enumeration and interruption attacks on inverse_grid.

This independent reviewer file never calls the producer's canonicalization or
correlation helper to construct expected answers.  Full ambient translations
are deliberately enumerated on small grids.
"""
from collections import Counter, defaultdict
from itertools import combinations, product
import copy
import hashlib
import inspect
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import inverse_grid as grid


def literal_bins(points, shape):
    counts = Counter()
    for a in points:
        for b in points:
            counts[tuple((a[i] - b[i]) % shape[i] for i in range(len(shape)))] += 1
    return tuple(sorted(counts.items()))


def ambient_canon(points, shape):
    if not points:
        return ()
    transforms = []
    for offset in product(*(range(n) for n in shape)):
        for sign in (1, -1):
            transforms.append(tuple(sorted(tuple((sign * a[i] + offset[i]) % shape[i]
                                                 for i in range(len(shape)))
                                           for a in points)))
    return min(transforms)


def document(shape, bins):
    return {"schema": grid.INPUT_SCHEMA, "shape": list(shape),
            "pair_counts": [{"shift": list(p), "count": c} for p, c in bins]}


def answers(result):
    return {tuple(tuple(p) for p in row) for row in result["solutions"]}


def all_fibres(shape):
    universe = tuple(product(*(range(n) for n in shape)))
    fibres = defaultdict(set)
    for size in range(len(universe) + 1):
        for arrangement in combinations(universe, size):
            fibres[literal_bins(arrangement, shape)].add(ambient_canon(arrangement, shape))
    return fibres


def integer_turnpike(distances, size):
    """Independent largest-distance branching on the ordinary integer line."""
    diameter = max(distances)
    remaining = distances.copy()
    remaining[diameter] -= 1
    if not remaining[diameter]:
        del remaining[diameter]
    solutions = set()

    def recurse(occupied, unpaid):
        if not unpaid:
            if len(occupied) == size:
                solutions.add(tuple(sorted(occupied)))
            return
        if len(occupied) >= size:
            return
        largest = max(unpaid)
        for candidate in sorted({largest, diameter - largest}):
            if candidate in occupied or not 0 < candidate < diameter:
                continue
            cost = Counter(abs(candidate - old) for old in occupied)
            if any(count > unpaid.get(distance, 0) for distance, count in cost.items()):
                continue
            new_unpaid = unpaid.copy()
            for distance, count in cost.items():
                new_unpaid[distance] -= count
                if not new_unpaid[distance]:
                    del new_unpaid[distance]
            recurse(occupied + (candidate,), new_unpaid)

    recurse((0, diameter), remaining)
    return solutions


class IndependentGridAttack(unittest.TestCase):
    def test_every_target_with_order_two_and_degenerate_axes(self):
        checked = 0
        for shape in [(1, 1, 1), (1, 3, 1, 2), (2, 2, 2), (2, 5),
                      (3, 4), (1, 2, 3, 2)]:
            for bins, expected in all_fibres(shape).items():
                result = grid.solve(grid.Problem.read(document(shape, bins)))
                self.assertTrue(result["complete"], (shape, bins))
                self.assertEqual(answers(result), expected, (shape, bins))
                checked += 1
        print("Review independently enumerated target fibres:", checked)

    def test_necessary_condition_targets_including_unrealizable(self):
        shape = (2, 3)
        realized = all_fibres(shape)
        missing = 0
        checked = 0
        # Five nonzero shifts: one order-two bin and two sign pairs.  Enumerate
        # every necessary-condition target for every possible cardinality.
        for k in range(7):
            for doubled, first, second in product(range(k // 2 + 1), range(k + 1), range(k + 1)):
                if 2 * (doubled + first + second) != k * (k - 1):
                    continue
                rows = [((0, 0), k), ((1, 0), 2 * doubled),
                        ((0, 1), first), ((0, 2), first),
                        ((1, 1), second), ((1, 2), second)]
                bins = tuple(sorted((p, c) for p, c in rows if c))
                result = grid.solve(grid.Problem.read(document(shape, bins)))
                expected = realized.get(bins, set())
                self.assertTrue(result["complete"])
                self.assertEqual(answers(result), expected, bins)
                missing += not bool(expected)
                checked += 1
        self.assertGreater(missing, 0)
        print("Review necessary-condition targets/unrealizable:", checked, missing)

    def test_resume_one_node_everywhere(self):
        # Includes full occupation, singleton, empty, and a true ambiguous case.
        fixtures = [((2, 2, 2), []), ((2, 2, 2), [[1, 1, 1]]),
                    ((2, 2), [list(p) for p in product(range(2), repeat=2)]),
                    ((12,), [[0], [1], [4], [6]])]
        for shape, points in fixtures:
            problem = grid.Problem.from_points(list(shape), points)
            whole = grid.solve(problem)
            partial = grid.solve(problem, max_nodes=0)
            runs = 0
            while not partial["complete"]:
                partial = grid.solve(problem, max_nodes=1, resume=partial["checkpoint"])
                runs += 1
                self.assertLess(runs, 1000)
            self.assertEqual(answers(partial), answers(whole))
            self.assertEqual(partial["stats"]["nodes"], whole["stats"]["nodes"])

    def test_global_inversion_does_not_collapse_separate_axis_reflections(self):
        shape = (7, 7)
        factor = (0, 1, 3)
        arrangement = tuple(product(factor, factor))
        one_axis_reflected = tuple(((-a) % 7, b) for a, b in arrangement)
        # Product sets retain their pair counts under either factor reflection,
        # but the requested quotient permits only simultaneous global inversion.
        self.assertEqual(literal_bins(arrangement, shape), literal_bins(one_axis_reflected, shape))
        expected = ambient_canon(arrangement, shape)
        other = ambient_canon(one_axis_reflected, shape)
        self.assertNotEqual(expected, other)
        self.assertEqual(grid.canonical(arrangement, shape), expected)
        self.assertEqual(grid.canonical(one_axis_reflected, shape), other)

    def test_sparse_huge_grid_when_initial_capacity_prune_is_skipped(self):
        marks = (0, 1, 4, 9, 15, 22, 32, 34)
        period = 1_000_003
        distances = Counter(abs(a - b) for a, b in combinations(marks, 2))
        integer_answers = integer_turnpike(distances, len(marks))
        self.assertTrue(integer_answers)
        # For n>3D, each anchored point has a representative in [-D,D].
        # Any pair spanning more than D cannot wrap to a supported shift, so
        # all cyclic solutions unwrap to integer solutions of diameter D.
        self.assertGreater(period, 3 * max(distances))
        bins = literal_bins(tuple((x,) for x in marks), (period,))
        offsets = {0} | {p[0] for p, count in bins}
        expected = set()
        for integer_answer in integer_answers:
            # Enumerate every target-support translation, rather than use
            # occupied-anchor canonicalization or a producer helper.
            orbit = []
            for offset in offsets:
                for sign in (1, -1):
                    translated = tuple(sorted(((sign * x + offset) % period,)
                                               for x in integer_answer))
                    if (0,) in translated:
                        orbit.append(translated)
            expected.add(min(orbit))
        result = grid.solve(grid.Problem.read(document((period,), bins)), max_nodes=10_000)
        self.assertTrue(result["complete"])
        self.assertEqual(result["stats"]["initial_support_candidates"], 56)
        self.assertEqual(answers(result), expected)

    def test_interruption_keeps_current_subtree(self):
        problem = grid.Problem.from_points([12], [[0], [1], [4], [6]])
        whole = grid.solve(problem)
        # Simulate the exact instant after the active prefix was removed from
        # the pending stack.  The active subtree must remain resumable.
        with patch.object(grid, "_residual", side_effect=KeyboardInterrupt):
            partial = grid.solve(problem)
        self.assertFalse(partial["complete"], "Interrupted active node was mistaken for exhaustion")
        self.assertEqual(partial["termination"], "interrupted")
        resumed = grid.solve(problem, resume=partial["checkpoint"])
        self.assertEqual(answers(resumed), answers(whole))

    def test_interruption_during_child_generation_and_leaf(self):
        problem = grid.Problem.from_points([12], [[0], [1], [4], [6]])
        whole = grid.solve(problem)
        for helper in ["_cost", "_capacity", "canonical"]:
            with self.subTest(helper=helper):
                with patch.object(grid, helper, side_effect=KeyboardInterrupt):
                    partial = grid.solve(problem)
                self.assertFalse(partial["complete"])
                self.assertEqual(partial["termination"], "interrupted")
                resumed = grid.solve(problem, resume=partial["checkpoint"])
                self.assertEqual(answers(resumed), answers(whole))

    def test_interruption_at_each_dfs_node_preserves_exact_search_counters(self):
        problem = grid.Problem.from_points([12], [[0], [1], [4], [6]])
        whole = grid.solve(problem)
        original = grid._residual
        for stop_at in range(1, whole["stats"]["nodes"] + 1):
            calls = 0

            def interrupt_one(prefix, target):
                nonlocal calls
                calls += 1
                if calls == stop_at:
                    raise KeyboardInterrupt
                return original(prefix, target)

            with patch.object(grid, "_residual", side_effect=interrupt_one):
                partial = grid.solve(problem)
            self.assertFalse(partial["complete"], stop_at)
            resumed = grid.solve(problem, resume=partial["checkpoint"])
            self.assertEqual(answers(resumed), answers(whole), stop_at)
            for counter in ["nodes", "budget_rejections", "candidate_prunes", "capacity_prunes", "matching_leaves"]:
                self.assertEqual(resumed["stats"][counter], whole["stats"][counter], (stop_at, counter))

    def test_interruptions_at_frontier_commit_boundaries(self):
        problem = grid.Problem.from_points([12], [[0], [1], [4], [6]])
        whole = grid.solve(problem)
        lines, first_line = inspect.getsourcelines(grid.solve)
        cases = [
            ("stack[active_base:] = children", 1, False),
            ("if solution is not None:", 1, False),
            ("solutions.add(solution)", 1, True),
            ("for key, change in changes.items():", 1, True),
            ("stats[key] += change", 3, False),
            ("active_prefix = None", 1, True),
        ]
        for statement, occurrence, leaf_only in cases:
            # The last match distinguishes the commit marker from initialization.
            location = max(first_line + i for i, line in enumerate(lines)
                           if line.strip() == statement)
            calls = 0
            fired = False

            def trace(frame, event, arg):
                nonlocal calls, fired
                if (frame.f_code is grid.solve.__code__ and event == "line"
                        and frame.f_lineno == location
                        and (not leaf_only or frame.f_locals.get("solution") is not None)):
                    calls += 1
                    if calls == occurrence:
                        fired = True
                        raise KeyboardInterrupt
                return trace

            previous = sys.gettrace()
            try:
                sys.settrace(trace)
                partial = grid.solve(problem)
            finally:
                sys.settrace(previous)
            self.assertTrue(fired, statement)
            self.assertFalse(partial["complete"], statement)
            self.assertEqual(partial["termination"], "interrupted")
            resumed = grid.solve(problem, resume=partial["checkpoint"])
            self.assertEqual(answers(resumed), answers(whole), statement)
            for counter in ["nodes", "budget_rejections", "candidate_prunes", "capacity_prunes", "matching_leaves"]:
                self.assertEqual(resumed["stats"][counter], whole["stats"][counter], (statement, counter))

    def test_self_consistent_checkpoint_is_trusted_not_completeness_proof(self):
        problem = grid.Problem.from_points([12], [[0], [1], [4], [6]])
        checkpoint = copy.deepcopy(grid.solve(problem, max_nodes=0)["checkpoint"])
        checkpoint["stack"] = []
        payload = {k: v for k, v in checkpoint.items() if k != "state_sha256"}
        checkpoint["state_sha256"] = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        forged = grid.solve(problem, resume=checkpoint)
        self.assertTrue(forged["complete"])
        self.assertEqual(forged["solutions"], [])
        # This behavior is documented: checksums detect accidental corruption;
        # a fresh complete search, not a self-consistent checkpoint, proves coverage.
        self.assertFalse(grid.verify_result(forged)["completeness_verified_by_fresh_replay"])
        with self.assertRaises(ValueError):
            grid.verify_result(forged, recompute=True)

    def test_source_identity_survives_later_disk_edit(self):
        # A resident Python module keeps executing its loaded code when the
        # source on disk changes.  It must not stamp results with the new file's
        # identity.  Work only in a disposable copy, never edit the real solver.
        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory) / "inverse_grid.py"
            copied.write_bytes((ROOT / "src" / "inverse_grid.py").read_bytes())
            script = """
import hashlib, json, pathlib, subprocess, sys
sys.path.insert(0, sys.argv[1])
import inverse_grid as g
initial = g.source_digest()
problem = g.Problem.from_points([12], [[0], [1], [4], [6]])
partial = g.solve(problem, max_nodes=0)
source = pathlib.Path(g.__file__)
source.write_bytes(source.read_bytes() + b'\\n# Later disk edit in isolated test.\\n')
assert hashlib.sha256(source.read_bytes()).hexdigest() != initial
assert g.source_digest() == initial, 'Loaded solver incorrectly assumed new disk identity'
resumed = g.solve(problem, resume=partial['checkpoint'])
assert resumed['complete'] and len(resumed['solutions']) == 2
assert resumed['solver_sha256'] == initial
target = source.with_name('target.json'); target.write_text(json.dumps(problem.document()))
state = source.with_name('checkpoint.json'); state.write_text(json.dumps(partial['checkpoint']))
fresh = subprocess.run([sys.executable, '-S', str(source), 'solve', '--input', str(target),
                        '--resume', str(state), '--out', str(source.with_name('output.json'))],
                       capture_output=True, text=True, timeout=3)
assert fresh.returncode == 2 and 'different target or solver revision' in fresh.stderr
print(json.dumps({'loaded_source_bound': True}))
"""
            run = subprocess.run([sys.executable, "-S", "-c", script, directory],
                                 text=True, capture_output=True, timeout=5)
            self.assertEqual(run.returncode, 0, run.stderr)


if __name__ == "__main__":
    unittest.main()
