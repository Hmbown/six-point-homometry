"""Tests for the universal uncentered Bloom matching and finite controls."""
from __future__ import annotations

from collections import Counter
import json
from math import gcd
from pathlib import Path
import sys
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from homometry import dihedral_canon, icv
from six_bloom_primary import (PERMS, X, Y, eliminated, group, invariants,
                               point_lists, residual, small_image)


class PrimaryMatchingTests(unittest.TestCase):
    def test_integer_homometry_identity(self):
        def forms(rows):
            answer = []
            for i in range(6):
                for j in range(i):
                    a, b = map(int, rows[i] - rows[j])
                    answer.append((a, b) if a > 0 or a == 0 and b > 0 else (-a, -b))
            return sorted(answer)
        self.assertEqual(forms(X), forms(Y))
        for n in range(6, 33):
            for a in range(n):
                for b in range(n):
                    x, y = point_lists(a, b, n)
                    if len(set(x)) == len(set(y)) == 6:
                        self.assertEqual(icv(x, n), icv(y, n))

    def test_unimodular_equivalence_in_even_and_three_primary_rings(self):
        # These tests include repeated labels and zero divisors; they compare
        # every original equation after the recovered anchor translation.
        for source in (X, Y):
            for target in (X, Y):
                for sign in (1, -1):
                    for index in range(0, 720, 7):
                        perm = PERMS[index]
                        matrix = eliminated(source, target, sign, perm)
                        h = residual(source, target, sign, perm, matrix)
                        for n in (2, 3, 4, 6, 8, 9, 12, 16, 27):
                            v = np.array(((index+1) % n, (3*index+2) % n), dtype=np.int64)
                            w = matrix @ v % n
                            translation = -sign * (target[perm[0]] @ v) % n
                            equations = (source @ w - sign * (target[perm] @ v) - translation) % n
                            self.assertTrue(np.all(equations[:3] == 0))
                            self.assertEqual(np.all(equations == 0), np.all(h @ v % n == 0))

    def test_complete_universal_certificate_acceptance(self):
        path = ROOT / 'results/2026-10-01-six-bloom-primary/pair-certificate.json'
        certificate = json.loads(path.read_text())
        self.assertTrue(certificate['complete'])
        self.assertEqual(certificate['processed'], 4_147_200)
        self.assertEqual(certificate['ranks'], {'0': 12, '1': 864, '2': 4_146_324})
        self.assertEqual(sum(entry['count'] for entry in certificate['rank1']), 864)
        self.assertEqual(sum(entry['count'] for entry in certificate['rank2']), 4_146_324)
        self.assertEqual({tuple(sum(entry['M'], [])) for entry in certificate['rank0']},
                         {tuple(map(int, g.flatten())) for g in group()})
        expected_D = {1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 16, 19}
        self.assertEqual({entry['minor_gcd'] for entry in certificate['rank2']}, expected_D)
        doubled = {(0, 1), (1, 0), (1, -1)}
        for entry in certificate['rank1']:
            self.assertIn(entry['content'], (1, 2))
            if entry['content'] == 2:
                self.assertIn(tuple(entry['direction']), doubled)
        for entry in certificate['rank1'] + certificate['rank2']:
            witness = entry['witness']
            ux, uy = (Y, X) if witness['swap'] else (X, Y)
            px, py = map(np.array, (witness['px'], witness['py']))
            m = eliminated(X, ux, witness['sx'], px)
            self.assertEqual(m.tolist(), witness['M'])
            hx = residual(X, ux, witness['sx'], px, m)
            hy = Y[1:] @ m - witness['sy'] * (uy[py[1:]] - uy[py[0]])
            h = np.concatenate((hx, hy))
            self.assertEqual(h.tolist(), witness['H'])
            content, determinant = invariants(h)
            self.assertEqual(content, entry['content'])
            self.assertEqual(determinant, entry.get('minor_gcd', 0))

    def test_all_reduced_moduli_agree_with_immutable_reference(self):
        moduli = (1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 16, 19)
        for n in moduli:
            gap = small_image(n)
            reference = small_image(n, reference=True)
            for key in ('actual_parameters', 'congruent_parameters', 'nontrivial_pair_count', 'free_G'):
                self.assertEqual(gap[key], reference[key], (n, key))
            def partitions(image):
                return sorted((entry['congruent'], sorted(entry['parameters']),
                               sorted(sorted(orbit) for orbit in entry['G_orbits']))
                              for entry in image['entries'])
            self.assertEqual(partitions(gap), partitions(reference), n)
            self.assertTrue(gap['free_G'])
            if n not in (12, 13, 16, 19):
                self.assertEqual(gap['actual_parameters'], 0)

    def test_twelve_exception_and_larger_primary_controls(self):
        for n in (12, 24, 27, 32, 36, 48, 60, 96):
            image = small_image(n)
            delta = int(n % 12 == 0)
            self.assertEqual(image['congruent_parameters'], 12*delta)
            self.assertEqual(image['nontrivial_pair_count'], image['actual_parameters']//12-2*delta)
            self.assertTrue(image['free_G'])
            exceptional = [entry for entry in image['entries'] if not entry['congruent'] and len(entry['parameters']) != 12]
            self.assertEqual(len(exceptional), delta)
            if delta:
                entry = exceptional[0]
                self.assertEqual(len(entry['parameters']), 24)
                h = n // 12
                expected = {tuple(int(x) % n for x in g @ v)
                            for v in ((h, 4*h), (3*h, 7*h)) for g in group()}
                self.assertEqual(set(map(tuple, entry['parameters'])), expected)

    def test_explicit_even_shared_partner_family(self):
        for m in range(9, 129):
            n = 2*m
            v = (m+3, 1)
            w = (-3, m-2)
            xv, yv = point_lists(*v, n)
            xw, yw = point_lists(*w, n)
            for endpoint in (xv, yv, xw, yw):
                self.assertEqual(len(set(endpoint)), 6)
            self.assertEqual(set(xw), {(point-m-3) % n for point in yv})
            self.assertNotIn(tuple(point % n for point in w),
                             {tuple(int(point) % n for point in g @ v) for g in group()})
            # Immutable reference independently verifies three different
            # endpoint classes rather than only parameter separation.
            cx, shared, cy = (dihedral_canon(xv, n), dihedral_canon(yv, n),
                              dihedral_canon(yw, n))
            self.assertEqual(dihedral_canon(xw, n), shared)
            self.assertEqual(len({cx, shared, cy}), 3)
            self.assertEqual(icv(xv, n), icv(yw, n))


if __name__ == '__main__':
    unittest.main(verbosity=2)
