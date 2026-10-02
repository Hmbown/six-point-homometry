"""Exact algebra and independent reference tests for Bloom orbit invariants."""
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
import six_bloom_invariants as inv
from homometry import dihedral_canon, icv


class BloomInvariantTests(unittest.TestCase):
    def test_integer_identities(self):
        report = inv.symbolic_checks()
        self.assertEqual(report['single_endpoint_determinant'], -263594736)

    def test_parameter_partition_against_immutable_reference(self):
        for p in (5, 7, 13, 17, 19, 23, 31, 37, 41, 43):
            by_pair, by_key = {}, {}
            for a in range(p):
                for b in range(p):
                    x = tuple(sorted({0, a, (b-2*a) % p, (2*b-2*a) % p,
                                      (2*b) % p, (3*b-a) % p}))
                    y = tuple(sorted({0, a, (b+2*a) % p, (2*b-a) % p,
                                      (2*b+a) % p, (3*b-a) % p}))
                    self.assertEqual(inv.allowed(a, b, p), len(x) == len(y) == 6)
                    if len(x) != 6 or len(y) != 6:
                        continue
                    pair = tuple(sorted((dihedral_canon(x, p), dihedral_canon(y, p))))
                    self.assertNotEqual(*pair)
                    self.assertEqual(icv(x, p), icv(y, p))
                    key = inv.invariant_key(a, b, p)
                    self.assertEqual(inv.key_from_pair(pair, p), key)
                    by_pair.setdefault(pair, []).append((a, b))
                    by_key.setdefault(key, []).append((a, b))
            self.assertEqual({tuple(v) for v in by_pair.values()},
                             {tuple(v) for v in by_key.values()})
            self.assertEqual(Counter({k: len(v) for k, v in by_key.items()}),
                             inv.invariant_fibers(p))

    def test_exceptional_coefficients_and_isotropic_parameters(self):
        # One moment coefficient can vanish at79/239; Bezout extraction still works.
        self.assertEqual(12798 % 79, 0)
        self.assertEqual(116154 % 239, 0)
        for p in (79, 239):
            x = tuple((u+6*v) % p for u, v in inv.PX)
            y = tuple((u+6*v) % p for u, v in inv.PY)
            self.assertEqual(inv.key_from_pair((x, y), p), inv.invariant_key(1, 6, p))
        self.assertEqual(inv.invariant_key(1, 6, 31)[0], 0)
        self.assertTrue(inv.allowed(1, 6, 31))

    def test_genuine_characteristic31_shared_endpoint(self):
        p = 31
        a_class = (0, 1, 3, 8, 12, 18)
        b_class = (0, 1, 3, 10, 14, 26)
        c_class = (0, 1, 4, 10, 12, 17)
        x1, y1 = [tuple((u*2+v*12) % p for u, v in points)
                  for points in (inv.PX, inv.PY)]
        x2, y2 = [tuple((u*8+v*17) % p for u, v in points)
                  for points in (inv.PX, inv.PY)]
        self.assertEqual(tuple(sorted((3-z) % p for z in y1)), a_class)
        self.assertEqual(tuple(sorted((3-z) % p for z in x1)), b_class)
        self.assertEqual(tuple(sorted(x2)), a_class)
        self.assertEqual(tuple(sorted((12-z) % p for z in y2)), c_class)
        self.assertEqual(len({dihedral_canon(s, p) for s in
                              (a_class, b_class, c_class)}), 3)
        for s in (a_class, b_class, c_class):
            self.assertEqual(icv(s, p), (1,)*15)
        self.assertEqual(inv.invariant_key(2, 12, p), (0, 2))
        self.assertEqual(inv.invariant_key(8, 17, p), (0, 8))

    def test_quadratic_fields_and_additive_quotient(self):
        for p, d, expected in ((5, 2, 40), (7, 3, 168)):
            f = inv.QuadraticField(p, d)
            for x in range(f.q):
                self.assertEqual(f.add(x, f.neg(x)), 0)
                self.assertEqual(f.scale(x, p), 0)
                if x:
                    self.assertTrue(any(f.mul(x, y) == 1 for y in range(1, f.q)))
            report = inv.quadratic_check(p, d)
            self.assertEqual(report['pairs'], expected)
            self.assertEqual(report['vertex_degree_histogram'], {1: 2*expected})
        f = inv.QuadraticField(5, 2)
        points = (0, 1, 5, 7, 10, 23)
        for anchor in range(25):
            self.assertEqual(f.canonical(points),
                             f.canonical(tuple(f.add(x, anchor) for x in points)))
        self.assertEqual(f.canonical(points), f.canonical(tuple(f.neg(x) for x in points)))
        self.assertNotEqual(f.canonical(points),
                            f.canonical(tuple(f.scale(x, 2) for x in points)))

    def test_input_scope(self):
        for p in (2, 3, 11, 15, True, -1):
            with self.assertRaises(ValueError):
                inv.invariant_fibers(p)
        for p, d in ((5, 1), (7, 2), (9, 2), (2, 1)):
            with self.assertRaises(ValueError):
                inv.QuadraticField(p, d)
        with self.assertRaises(ValueError):
            inv.point_moments((0, 1, 2, 3, 4, 4), 13)

    def test_small_prime_finite_dependencies(self):
        audit = inv.small_prime_census_audit()
        self.assertTrue(audit['all_displayed_classes_icvs_and_counts_verified'])
        records = {record['p']: record for record in audit['records']}
        self.assertEqual((records[31]['pairs'], records[31]['families']), (70, 61))
        self.assertEqual(records[31]['family_size_histogram'], {2: 60, 5: 1})
        self.assertEqual((records[17]['pairs'], records[19]['pairs']), (16, 21))

    def test_saved_independent_replays(self):
        summary_path = ROOT/'results/2026-09-30-six-prime-invariants/summary.json'
        if not summary_path.exists():
            self.skipTest('independent replay not yet generated')
        report = json.loads(summary_path.read_text())
        primes = [record['p'] for record in report['primes']]
        self.assertEqual(primes, [p for p in range(13, 252) if inv.prime(p)]+[1009])
        for record in report['primes']:
            self.assertTrue(record['all_direct_parameter_fibers_equal'])
            self.assertTrue(record['all_saved_endpoint_moments_bound'])
            self.assertEqual(record['pairs'], (record['p']-1)*(record['p']-11)//12)
        self.assertEqual([(r['q'], r['pairs']) for r in report['quadratic_fields']],
                         [(25, 40), (49, 168), (169, 2212)])


if __name__ == '__main__':
    unittest.main(verbosity=2)
