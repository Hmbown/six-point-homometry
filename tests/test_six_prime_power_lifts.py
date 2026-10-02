"""Independent coupled-equation and reflection controls for the ring proof."""
from collections import Counter
from hashlib import sha256
from itertools import permutations, product
import json
from math import gcd
from pathlib import Path
import sys
import unittest

import sympy as S
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import six_composite_auxiliary as aux

RAW = (S.Matrix([[0, 0], [1, 0], [-2, 1], [-2, 2], [0, 2], [-1, 3]]),
       S.Matrix([[0, 0], [1, 0], [2, 1], [-1, 2], [1, 2], [-1, 3]]))
C = tuple(S.Matrix([[3*M[j, i] - sum(M[:, i])/2 for i in range(2)]
                    for j in range(6)]) for M in RAW)
OUT = ROOT / 'results/2026-09-30-six-composite-algebra'


def options(source, target, base, sign):
    left, right = tuple(source*S.Matrix(base)), tuple(target*S.Matrix(base))
    return [p for p in permutations(range(6)) if left == tuple(sign*right[i] for i in p)]


class LiftTests(unittest.TestCase):
    def check_record(self, record, source, targets, base, paired):
        inverse = source[:2, :].inv()
        matrix = 12*inverse*targets[0][:2, :]
        h = source*matrix - 12*targets[0]
        if paired:
            h = h.col_join(C[1]*matrix - 12*targets[1])
        divisor = 0
        for row in h.tolist():
            self.assertEqual(row[0], 0 if base == (1, 0) else -2*row[1])
            divisor = gcd(divisor, int(row[1]))
        self.assertEqual(record['twelve_w_matrix'], matrix.tolist())
        self.assertEqual(record['residual_rows'], h.tolist())
        self.assertEqual(record['residual_coefficient_gcd'], divisor)
        self.assertEqual(sum(x*int(h[i, 1]) for i, x in
                             enumerate(record['gcd_bezout_coefficients'])), divisor)

    def test_complete_paired_systems(self):
        payload = json.loads((OUT/'lift-table.json').read_text())
        self.assertEqual(payload['source_sha256'], sha256(
            (ROOT/'src/six_prime_power_lifts.py').read_bytes()).hexdigest())
        for kind, base in (('E', (1, 0)), ('D', (1, 2))):
            saved = payload['tables'][kind]['patterns']
            covered, smiths = set(), Counter()
            for swap in (0, 1):
                sign = 1 if kind == 'E' or not swap else -1
                u = (C[swap], C[1-swap])
                opts = [options(C[e], u[e], base, sign) for e in (0, 1)]
                self.assertTrue(all(not options(C[e], u[e], base, -sign) for e in (0, 1)))
                for px, py in product(*opts):
                    key = swap, px, py
                    self.assertNotIn(key, covered)
                    covered.add(key)
                    found = [r for r in saved if r['swap'] == swap and
                             tuple(r['permutation_X']) == px and tuple(r['permutation_Y']) == py]
                    self.assertEqual(len(found), 1)
                    targets = [sign*S.Matrix([u[e].tolist()[i] for i in p])
                               for e, p in enumerate((px, py))]
                    self.check_record(found[0], C[0], targets, base, True)
                    equations = C[0].row_join(-targets[0]).col_join(C[1].row_join(-targets[1]))
                    d = smith_normal_form(equations, domain=S.ZZ)
                    smiths[tuple(abs(int(d[i, i])) for i in range(4))] += 1
            self.assertEqual(len(covered), len(saved))
            expected = ({(1, 3, 3, 0): 24, (1, 3, 6, 0): 6, (1, 3, 0, 0): 2}
                        if kind == 'E' else {(1, 3, 3, 0): 6, (1, 3, 0, 0): 2})
            self.assertEqual(smiths, expected)

    def test_complete_single_endpoint_systems(self):
        payload = json.loads((OUT/'endpoint-lift-table.json').read_text())
        self.assertEqual(payload['source_sha256'], sha256(
            (ROOT/'src/six_prime_power_endpoint_lifts.py').read_bytes()).hexdigest())
        for kind, base in (('E', (1, 0)), ('D', (1, 2))):
            saved = payload['tables'][kind]['patterns']
            covered = set()
            for left, right in product((0, 1), repeat=2):
                sign = 1 if kind == 'E' or left == right else -1
                self.assertFalse(options(C[left], C[right], base, -sign))
                for perm in options(C[left], C[right], base, sign):
                    key = left, right, perm
                    self.assertNotIn(key, covered)
                    covered.add(key)
                    found = [r for r in saved if r['source'] == 'XY'[left] and
                             r['target'] == 'XY'[right] and tuple(r['permutation']) == perm]
                    self.assertEqual(len(found), 1)
                    target = sign*S.Matrix([C[right].tolist()[i] for i in perm])
                    self.check_record(found[0], C[left], [target], base, False)
            self.assertEqual(len(covered), len(saved))
            self.assertEqual(Counter(r['residual_coefficient_gcd'] for r in saved),
                             {0: 4, 18: 8, 36: 4} if kind == 'E' else {0: 4, 9: 2, 36: 2})

    def test_actual_reflection_cosets_and_complete_catalog(self):
        for endpoint in (0, 1):
            catalog = aux.reflection_certificate()['XY'[endpoint]]
            self.assertEqual(len(catalog), 15)
            for record in catalog:
                rows = S.Matrix([tuple(C[endpoint][i, h]+C[endpoint][j, h]
                                       for h in range(2)) for i, j in record['pairs']])
                snf = smith_normal_form(rows, domain=S.ZZ)
                self.assertEqual(abs(int(snf[0, 0]*snf[1, 1])), record['minor_gcd'])
                self.assertNotEqual(snf[1, 1], 0)
            cosets = []
            rho = tuple(aux.formal_permutations()['rho_'+'XY'[endpoint]])
            for p, slope in ((13, (10, 4)[endpoint]), (19, (8, 12)[endpoint])):
                values = tuple(int(x) % p for x in C[endpoint]*S.Matrix([1, slope]))
                self.assertEqual(len(set(values)), 6)
                chi = tuple(values.index(-x % p) for x in values)
                self.assertEqual(aux.parity(chi), -1)
                coset, power = set(), tuple(range(6))
                for _ in range(3):
                    coset.add(tuple(chi[i] for i in power))
                    power = tuple(power[i] for i in rho)
                self.assertEqual(len(coset), 3)
                cosets.append(coset)
            self.assertFalse(cosets[0] & cosets[1])


if __name__ == '__main__':
    unittest.main(verbosity=2)
