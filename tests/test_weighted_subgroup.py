"""Exact and independently formed small controls for subgroup mechanisms."""
import sys
from fractions import Fraction as F
from pathlib import Path
import unittest

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"src"))
import weighted_subgroup as w
from homometry import icv


class SubgroupTests(unittest.TestCase):
    def test_validation_and_periods(self):
        with self.assertRaises(ValueError):
            w.period_subgroup(7, ())
        with self.assertRaises(ValueError):
            w.period_subgroup(7, (7,))
        n, s = w.quotient_lift(7, 3)
        self.assertEqual(w.period_subgroup(n, s), (0, 7, 14))
        self.assertTrue(w.distinct_ordered_differences(7, (0, 1, 3)))
        self.assertFalse(w.distinct_ordered_differences(6, (0, 1, 3)))

    def test_exact_allpass_cayley(self):
        for m in range(1, 10):
            u = w.cayley_kernel(m, F(1, 7))
            self.assertEqual(w.autocorrelation(u), (F(1),)+(F(0),)*(m-1))
            self.assertEqual(sum(u), 1)
        for t in (F(0), F(1, 10), F(-2, 3), F(1)):
            self.assertEqual(w.autocorrelation(w.order_three_kernel(t)), (F(1), F(0), F(0)))

    def test_positive_exact_nonintrinsic_pair(self):
        n, s = w.quotient_lift(7, 3)
        x = tuple(F(10+s.index(i)) if i in s else F(0) for i in range(n))
        u = w.embed_kernel(n, 7, w.order_three_kernel(F(1, 10)))
        y = w.convolve(x, u)
        self.assertEqual(w.autocorrelation(x), w.autocorrelation(y))
        self.assertEqual(tuple(i for i, v in enumerate(y) if v), s)
        self.assertGreater(min(y[i] for i in s), 0)
        self.assertGreater(w.rigid_squared_distance(x, y), 0)
        self.assertEqual(w.jacobian(x, s).rank(), 8)
        # Separate ambient complex FFT controls the exact rational result.
        fx = np.fft.fft(np.array(x, dtype=float))
        fy = np.fft.fft(np.array(y, dtype=float))
        np.testing.assert_allclose(abs(fx)**2, abs(fy)**2, atol=1e-9, rtol=1e-12)

    def test_reference_binary_autocorrelation_convention(self):
        for n, s in ((12, (0, 1, 4, 6)), (21, (0, 1, 3, 7, 10, 15))):
            x = tuple(int(i in s) for i in range(n))
            a = w.autocorrelation(x)
            reference = icv(s, n)
            for d in range(1, n//2+1):
                self.assertEqual(a[d], (2 if 2*d == n else 1)*int(reference[d-1]))

    def test_universal_support_preservation_criterion(self):
        # Independently use each standard basis vector: no cancellation can hide a shift.
        for n, s in ((7, (0, 1, 3)), w.quotient_lift(7, 3), w.quotient_lift(8, 4)):
            for t in range(n):
                maps_space = all((a+t) % n in s for a in s)
                self.assertEqual(maps_space, t in w.period_subgroup(n, s))

    def test_constructive_reconstruction_and_stability(self):
        rng = np.random.default_rng(210107)
        for q in (7, 8, 9):
            for m in range(3, 10):
                n, s = w.quotient_lift(q, m)
                x = np.zeros(n)
                y = np.zeros(n)
                x[list(s)] = rng.uniform(1, 3, len(s))
                y[list(s)] = x[list(s)]+rng.normal(0, .01, len(s))
                px, py = abs(np.fft.fft(x))**2, abs(np.fft.fft(y))**2
                recovered = w.recover_fixed_support(px, q, m)
                np.testing.assert_allclose(abs(np.fft.fft(recovered))**2, px, atol=1e-9, rtol=1e-10)
                self.assertLess(w.subgroup_orbit_distance(x, recovered, q), 1e-6)
                blocks = np.array([np.fft.fft(v[r::q]) for v in (x, y) for r in (0, 1, 3)])
                delta, maximum = np.min(abs(blocks)), np.max(abs(blocks))
                l0 = (2*maximum**2/delta**2+maximum**4/delta**4)/(2*delta)
                bound = np.sqrt(3/n)*max(l0, 1/delta+maximum**2*l0/delta**2)*np.linalg.norm(px-py)
                self.assertLessEqual(w.subgroup_orbit_distance(x, y, q), bound)
        with self.assertRaises(ValueError):
            w.recover_fixed_support(np.zeros(21), 7, 3)

    def test_aperiodic_exact_algebraic_certificate(self):
        certificate = w.punctured_certificate()
        self.assertEqual(certificate["period_subgroup"], [0])
        self.assertEqual(len(certificate["support"]), 14)
        self.assertEqual(len(certificate["folded_distance_classes"]), 18)
        self.assertEqual(certificate["jacobian_rank"], 13)
        self.assertLess(F(certificate["strict_displacement_squared_upper_bound"]), 1)
        self.assertEqual(certificate["hole_gradient_at_identity"], ["10", "4"])


if __name__ == "__main__":
    unittest.main()
