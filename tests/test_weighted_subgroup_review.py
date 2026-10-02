"""Meaningful independent controls for a subgroup-preserving ambiguity."""
from fractions import Fraction as Q
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import weighted_subgroup_review as r


class WeightedSubgroupReviewTests(unittest.TestCase):
    def test_original_folded_distance_and_sparsity_conditions(self):
        for m in range(3,25):
            n,s=r.support(m)
            self.assertEqual(r.folded_differences(n,s),tuple(range(n//2+1)))
            self.assertGreater(len(r.folded_differences(n,s)),len(s))
            self.assertLessEqual(len(s),n//2)
            self.assertEqual(r.periods(n,s),tuple(range(0,n,7)))

    def test_exact_symbolic_all_pass_family(self):
        self.assertEqual(r.symbolic_kernel_identity(),['0','0','0'])
        for t in (Q(0),Q(1,100),Q(-1,17),Q(1,6),Q(2)):
            u=r.rational_kernel(t)
            self.assertEqual(r.autocorrelation(u),(Q(1),Q(0),Q(0)))

    def test_positive_exact_witness_outside_rigid_orbit(self):
        n,s,x,u,y=r.witness()
        self.assertEqual(tuple(i for i,v in enumerate(y) if v),s)
        self.assertTrue(all(y[i]>0 for i in s))
        self.assertEqual(r.autocorrelation(x),r.autocorrelation(y))
        self.assertGreater(r.rigid_squared_distance(x,y),0)

    def test_ambient_fourier_and_even_odd_subgroup_controls(self):
        for m in (3,4,5,6,7,8,12):
            result=r.ambient_phase_control(m)
            self.assertGreater(result['minimum_amplitude'],0)
            self.assertLess(result['outside_support_error'],2e-14)
            self.assertLess(result['power_error'],2e-10)

    def test_exact_jacobian_obstruction_and_no_ambient_fourier_zeros(self):
        result=r.audit()
        self.assertEqual(result['jacobian_rank'],8)
        self.assertEqual(result['spectral_polynomial_gcd'],'1')
        self.assertGreater(Q(result['minimum_rigid_squared_distance']),0)

    def test_full_pairproduct_blocks_and_exact_generic_rank(self):
        for q in (7,8,9):
            for m in (3,4,5,8):
                result=r.exact_rank_control(q,m)
                self.assertEqual(result['jacobian_rank'],3*m-(m-1)//2)
                self.assertEqual(result['tangent_rank'],(m-1)//2)
                self.assertLess(result['frequency_block_error'],1e-9)
        for m in (3,4):
            result=r.exact_rank_control(13,m,(0,1,3,9))
            self.assertEqual(result['jacobian_rank'],4*m-(m-1)//2)

    def test_aperiodic_deleted_support_and_exact_restricted_rank(self):
        for q in (7,8,9):
            for m in (5,6,9,10):
                result=r.punctured_rank_control(q,m)
                self.assertEqual(result['periods'],[0])
                self.assertEqual(result['jacobian_rank'],3*m-(m-1)//2)
                self.assertEqual(result['hole_tangent_rank'],(m-1)//2-1)
                self.assertGreater(result['folded_difference_count'],result['K'])
        certificate=r.independent_puncture_certificate()
        self.assertEqual(certificate['interval_root_count'],1)
        self.assertEqual(certificate['jacobian_rank'],13)
        self.assertLess(Q(certificate['strict_displacement_squared_bound']),1)
        self.assertEqual(certificate['minimum_nonidentity_intrinsic_squared_separation'],502)

    def test_stability_reconstruction_with_fixed_nonzero_anchor(self):
        for q in (7,8,9):
            for m in (3,4,5,8,9):
                result=r.stability_control(q,m)
                self.assertEqual(result['fixed_untwisted_anchor'],3)
                self.assertLess(result['pairproduct_error'],2e-10)
                self.assertLessEqual(result['orbit_distance'],result['recovery_bound'])


if __name__=='__main__':unittest.main(verbosity=2)
