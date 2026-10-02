"""Smoke and independent-control checks for the bounded benchmark driver."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"src"))
from benchmark_inverse_grid import cases, run_case


class BenchmarkControls(unittest.TestCase):
    def test_small_control_and_saved_input(self):
        with tempfile.TemporaryDirectory() as temporary:
            out = Path(temporary)
            summary = run_case(*cases()[0], out, 10000, 5)
            self.assertTrue(summary["complete"])
            self.assertEqual(summary["classes_found"], 2)
            self.assertEqual(json.loads((out/"tetrachord-12/input.json").read_text())["shape"], [12])
            result = json.loads((out/"tetrachord-12/result.json").read_text())
            state = json.loads((out/"tetrachord-12/checkpoint.json").read_text())
            self.assertEqual(result["checkpoint"], state)

    def test_limit_and_fixed_inputs(self):
        self.assertEqual(cases(), cases())
        with tempfile.TemporaryDirectory() as temporary:
            summary = run_case(*cases()[-1], Path(temporary), 0, 5)
            self.assertFalse(summary["complete"])
            self.assertEqual(summary["termination"], "node_limit")
            self.assertEqual(summary["classes_found"], 0)


if __name__ == "__main__":
    unittest.main()
