"""Boundary, exact arithmetic and reference controls for all-modulus support."""
from math import gcd
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
import six_bloom_support as s
from homometry import icv


class SupportTests(unittest.TestCase):
    def test_unscaled_collision_catalogue(self):
        raw = set(s.KERNELS) | {(0, 1), (1, 0), (1, -1)}
        self.assertEqual(set(s.raw_normals(s.X)), raw)
        self.assertEqual(set(s.raw_normals(s.Y)), raw)
        # The old primitive-only rule loses actual order-two collisions.
        self.assertFalse(s.support_admissible(8, 1, 16))
        self.assertFalse(s.point_support_admissible(8, 1, 16))

    def test_all_possible_overlap_orders(self):
        actual = s.primitive_order_table()
        self.assertEqual({m: row["overcount"] for m, row in actual.items()}, s.OVERCOUNTS)
        self.assertEqual(actual[6]["histogram"], {1: 12, 2: 12})
        self.assertEqual(actual[8]["histogram"], {1: 36, 2: 12})

    def test_smith_formula_every_residue_in_period(self):
        for n in range(1, 841):
            self.assertEqual(s.support_count(n), s.smith_count(n), n)
        for n in (1680, 2197, 10**12+39, 2**40*3**12*5*7):
            self.assertEqual(s.support_count(n), s.smith_count(n))
        for n in range(1, 150, 2):
            self.assertEqual(s.support_count(n), n*n-12*n+11+16*(n % 3 == 0)+
                             24*(n % 5 == 0)+24*(n % 7 == 0))

    def test_actual_supports_and_immutable_homometry(self):
        for n in range(1, 49):
            count = 0
            for a in range(n):
                for b in range(n):
                    literal = s.point_support_admissible(a, b, n)
                    self.assertEqual(literal, s.support_admissible(a, b, n), (n, a, b))
                    count += literal
                    if literal:
                        x = tuple(sorted({(u*a+v*b) % n for u, v in s.X}))
                        y = tuple(sorted({(u*a+v*b) % n for u, v in s.Y}))
                        self.assertEqual(icv(x, n), icv(y, n))
            self.assertEqual(count, s.support_count(n), n)
        self.assertEqual(s.support_count(12), 36)
        self.assertEqual(s.support_count(24), 300)
        self.assertEqual(s.support_count(637), 398160)

    def test_input_validation_and_tiny_empty_domains(self):
        for n in (0, -1, True, 2.5):
            with self.assertRaises(ValueError):
                s.support_count(n)
        for n in range(1, 10):
            self.assertEqual(s.support_count(n), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
