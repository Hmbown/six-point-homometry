"""Independent geometric and kernel controls for composite arrangement counts."""
from collections import Counter
from itertools import combinations
from math import gcd
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
import six_composite_arithmetic as a
from homometry import dihedral_canon, icv


class ArithmeticTests(unittest.TestCase):
    def test_exact_smith_kernel_counts(self):
        self.assertEqual(a.arrangement_weights(), {1: -16, 2: 3, 3: 8, 4: 3, 5: 6, 7: 4, 8: 3})
        for n in (5, 7, 9, 13, 15, 21, 25):
            for rows in combinations(a.LINES, 2):
                (u, v), (x, y) = rows
                expected = gcd(n, abs(u*y-v*x))
                actual = sum(all((r*aa+s*bb) % n == 0 for r, s in rows)
                             for aa in range(n) for bb in range(n))
                self.assertEqual(actual, expected)

    def test_support_count_against_actual_six_lists(self):
        for n in range(3, 122, 2):
            count = 0
            for aa in range(n):
                for bb in range(n):
                    x = {0, aa, (bb-2*aa) % n, (2*bb-2*aa) % n, 2*bb % n, (3*bb-aa) % n}
                    y = {0, aa, (bb+2*aa) % n, (2*bb-aa) % n, (2*bb+aa) % n, (3*bb-aa) % n}
                    self.assertEqual(a.support_admissible(aa, bb, n), len(x) == len(y) == 6)
                    count += len(x) == len(y) == 6
            self.assertEqual(count, a.support_count(n))
            self.assertEqual(count, n*n-12*n+11+16*(n % 3 == 0)+
                             24*(n % 5 == 0)+24*(n % 7 == 0))

    def test_domains_reference_and_normal_forms(self):
        # A separate actual-point reference builds each of these domain images.
        for n in (13, 17, 19, 31, 169, 221):
            ff = a.factors(n)
            counts = Counter()
            fibers = {}
            for aa in range(n):
                for bb in range(n):
                    if not a.regular(aa, bb, n, ff):
                        continue
                    xx = tuple(sorted({0, aa, (bb-2*aa) % n, (2*bb-2*aa) % n, 2*bb % n, (3*bb-aa) % n}))
                    yy = tuple(sorted({0, aa, (bb+2*aa) % n, (2*bb-aa) % n, (2*bb+aa) % n, (3*bb-aa) % n}))
                    pair = tuple(sorted((dihedral_canon(xx, n), dihedral_canon(yy, n))))
                    self.assertNotEqual(*pair)
                    self.assertEqual(icv(xx, n), icv(yy, n))
                    fibers.setdefault(pair, set()).add(aa*n+bb)
                    counts['regular'] += 1
                    counts['faithful'] += a.faithful(aa, bb, ff)
            self.assertEqual(counts['regular'], a.regular_parameter_count(n))
            self.assertEqual(counts['faithful'], a.faithful_parameter_count(n))
            for values in fibers.values():
                first = min(values)
                self.assertEqual(values, a.orbit(*divmod(first, n), n))
                self.assertEqual(len(values), 12)

    def test_input_scope(self):
        for n in (2, 12, 20):
            with self.assertRaises(ValueError):
                a.support_count(n)
        for n in (25, 49, 121, 637):
            with self.assertRaises(ValueError):
                a.regular_parameter_count(n)
        self.assertEqual(a.support_count(637), 398160)
        self.assertEqual(a.support_count(2197), 4800456)
        self.assertEqual(a.local_support_parameter_count(2197)//12, 400038)
        self.assertEqual(a.local_support_parameter_count(221)//12, 192)
        self.assertTrue(a.support_admissible(1, 104, 221))
        self.assertFalse(a.local_supports(1, 104, a.factors(221)))

    def test_relative_certificate_path(self):
        relative = Path('results/2026-09-30-six-composite-count/n169.json.gz')
        absolute = ROOT/relative
        expected, actual = a.audit(absolute), a.audit(relative)
        for record in (expected, actual):
            record.pop('seconds')
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main(verbosity=2)
