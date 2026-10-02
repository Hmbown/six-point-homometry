"""Independent small-grid enumeration and operational controls for inverse_grid."""
from collections import Counter, defaultdict
from itertools import combinations, product
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
from inverse_grid import Problem, canonical, solve, verify_result
sys.path.insert(0, str(ROOT.parents[1]/"src"))
from homometry import bracelets, dihedral_canon, icv


def literal_counts(pts, shape):
    # Separate literal coordinate arithmetic; no inverse-grid helper.
    bins = Counter()
    for a in pts:
        for b in pts:
            bins[tuple((a[i]-b[i]) % shape[i] for i in range(len(shape)))] += 1
    return tuple(sorted(bins.items()))


def literal_canon(pts, shape):
    # ALL ambient translations, rather than the producer's occupied-site anchors.
    if not pts:
        return ()
    return min(tuple(sorted(tuple((sign*a[i]+shift[i]) % shape[i] for i in range(len(shape)))
                            for a in pts))
               for shift in product(*(range(n) for n in shape)) for sign in (1, -1))


def input_document(shape, bins):
    return {"schema": "homometry.grid-input/v1", "shape": list(shape),
            "pair_counts": [{"shift": list(p), "count": c} for p, c in bins]}


def recovered(result):
    return {tuple(tuple(p) for p in row) for row in result["solutions"]}


class ReconstructionTests(unittest.TestCase):
    def test_every_small_target_by_literal_enumeration(self):
        targets = raw = 0
        for shape in [(n,) for n in range(1, 11)] + [(3, 3), (2, 4), (2, 2, 3)]:
            universe = list(product(*(range(n) for n in shape)))
            groups = defaultdict(set)
            for k in range(len(universe)+1):
                for pts in combinations(universe, k):
                    groups[literal_counts(pts, shape)].add(literal_canon(pts, shape))
                    raw += 1
            for bins, expected in groups.items():
                problem = Problem.read(input_document(shape, bins))
                result = solve(problem)
                self.assertTrue(result["complete"], shape)
                self.assertEqual(recovered(result), expected, (shape, bins))
                self.assertTrue(verify_result(result)["solutions_valid"])
                targets += 1
        print("Independent literal targets", targets, "raw arrangements", raw)

    def test_all_reference_fibres(self):
        checked = 0
        for n in range(4, 15):
            for k in range(n+1):
                groups = defaultdict(list)
                for pts in bracelets(n, k):
                    groups[icv(pts, n)].append(pts)
                for expected in groups.values():
                    problem = Problem.from_points([n], [[x] for x in expected[0]])
                    result = solve(problem)
                    self.assertTrue(result["complete"])
                    actual = {tuple(p[0] for p in row) for row in recovered(result)}
                    self.assertEqual(actual, set(expected), (n, k))
                    # This independently exercises canonicalization for each returned class.
                    self.assertTrue(all(dihedral_canon(p, n) == p for p in actual))
                    checked += 1
        print("Immutable reference fibres", checked)

    def test_large_modulus_and_three_dimensions(self):
        points = [0, 1, 4, 10, 12, 17]
        for shape, values in [
            ([1_000_000_007], [[x] for x in points]),
            ([1_000_000_007, 1_000_000_009, 1_000_000_021], [[x, 0, 0] for x in points]),
        ]:
            result = solve(Problem.from_points(shape, values), max_nodes=100_000)
            self.assertTrue(result["complete"])
            expected = [
                points, [0, 1, 8, 11, 13, 17],
            ]
            expected = {canonical(tuple((x,)+(0,)*(len(shape)-1) for x in p), tuple(shape))
                        for p in expected}
            self.assertEqual(recovered(result), expected)
            self.assertLessEqual(result["stats"]["initial_support_candidates"], 30)

    def test_antipodal_counts_and_known_ambiguity(self):
        pts = [[0], [1], [4], [6]]
        problem = Problem.from_points([12], pts)
        self.assertEqual(problem.counts[(6,)], 2)
        result = solve(problem)
        self.assertEqual(recovered(result), {((0,), (1,), (3,), (7,)), ((0,), (1,), (4,), (6,))})

    def test_resume_limits_and_source_binding(self):
        problem = Problem.from_points([12], [[0], [1], [4], [6]])
        full = solve(problem)
        partial = solve(problem, max_nodes=0)
        self.assertFalse(partial["complete"])
        self.assertEqual(partial["termination"], "node_limit")
        calls = 0
        while not partial["complete"]:
            partial = solve(problem, max_nodes=2, resume=partial["checkpoint"])
            calls += 1
            self.assertLess(calls, 1000)
        self.assertEqual(recovered(partial), recovered(full))
        self.assertEqual(partial["stats"]["nodes"], full["stats"]["nodes"])
        stopped = solve(problem, timeout=0)
        self.assertFalse(stopped["complete"])
        limited = solve(problem, max_solutions=1)
        self.assertFalse(limited["complete"])
        self.assertEqual(limited["termination"], "solution_limit")
        self.assertEqual(recovered(solve(problem, resume=limited["checkpoint"])), recovered(full))
        bad = copy.deepcopy(stopped["checkpoint"])
        bad["stack"] = []
        with self.assertRaises(ValueError):
            solve(problem, resume=bad)
        other = Problem.from_points([13], [[0], [1], [4], [6]])
        with self.assertRaises(ValueError):
            solve(other, resume=stopped["checkpoint"])

    def test_unrealizable_but_consistent_input(self):
        # Enumerate all symmetric, nonnegative necessary-condition targets on Z5;
        # locate an unachievable one independently, rather than tune a made-up case.
        realized = {literal_counts(p, (5,)) for p in combinations([(x,) for x in range(5)], 3)}
        invalid = None
        for a in range(4):
            b = 3-a
            bins = tuple(sorted([((0,), 3)] + [((p,), c) for p, c in [(1,a),(4,a),(2,b),(3,b)] if c]))
            if bins not in realized:
                invalid = bins; break
        self.assertIsNotNone(invalid)
        result = solve(Problem.read(input_document((5,), invalid)))
        self.assertTrue(result["complete"])
        self.assertEqual(result["solutions"], [])

    def test_malformed_and_tampered_results(self):
        good = Problem.from_points([12], [[0], [1], [4], [6]]).document()
        bads = []
        bad = copy.deepcopy(good); bad["shape"] = [True]; bads.append(bad)
        bad = copy.deepcopy(good); bad["pair_counts"].append(bad["pair_counts"][0]); bads.append(bad)
        bad = copy.deepcopy(good); bad["pair_counts"][0]["count"] = True; bads.append(bad)
        bad = copy.deepcopy(good); bad["pair_counts"][0]["shift"] = [12]; bads.append(bad)
        bad = copy.deepcopy(good); bad["pair_counts"][0]["count"] -= 1; bads.append(bad)
        for bad in bads:
            with self.assertRaises(ValueError):
                Problem.read(bad)
        with self.assertRaises(ValueError):
            Problem.from_points([5], [[0], [0]])
        problem = Problem.read(good)
        for kwargs in [{"max_nodes": -1}, {"timeout": float("nan")}, {"max_solutions": 0}]:
            with self.assertRaises(ValueError):
                solve(problem, **kwargs)
        result = solve(problem)
        broken = copy.deepcopy(result)
        broken["solutions"][0][1] = [2]
        with self.assertRaises(ValueError):
            verify_result(broken)
        missing = copy.deepcopy(result)
        missing["solutions"] = missing["solutions"][:1]
        self.assertTrue(verify_result(missing)["solutions_valid"])
        self.assertFalse(verify_result(missing)["completeness_verified_by_fresh_replay"])
        with self.assertRaises(ValueError):
            verify_result(missing, recompute=True)
        self.assertTrue(verify_result(result, recompute=True)["completeness_verified_by_fresh_replay"])
        self.assertFalse(verify_result(result, recompute=True, max_nodes=0)["completeness_verified_by_fresh_replay"])

    def test_cli_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            script = str(ROOT/"src/inverse_grid.py")
            commands = [
                ["target", "--shape", "12", "--points", "0;1;4;6", "--out", str(base/"input.json")],
                ["solve", "--input", str(base/"input.json"), "--out", str(base/"partial.json"),
                 "--checkpoint", str(base/"state.json"), "--max-nodes", "1"],
                ["solve", "--input", str(base/"input.json"), "--out", str(base/"full.json"),
                 "--resume", str(base/"state.json")],
                ["verify", "--input", str(base/"full.json"), "--recompute"],
            ]
            for command in commands:
                run = subprocess.run([sys.executable, "-S", script, *command], text=True, capture_output=True)
                self.assertEqual(run.returncode, 0, run.stderr)
            self.assertFalse(json.loads((base/"partial.json").read_text())["complete"])
            self.assertTrue(json.loads((base/"full.json").read_text())["complete"])


if __name__ == "__main__":
    unittest.main()
