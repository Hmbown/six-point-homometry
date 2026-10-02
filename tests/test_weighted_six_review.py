"""Checks the separate R5 reviewer with an independent pairwise correlation."""

from fractions import Fraction
from pathlib import Path
import sys

import sympy as sp

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
import weighted_six_review as review
from homometry import icv


def pairwise_correlation(support,weights,n):
    result=[sp.Integer(0)]*n
    for p,u in zip(support,weights,strict=True):
        for q,v in zip(support,weights,strict=True):
            result[(q-p)%n]+=u*v
    return [sp.expand(value) for value in result]


def test_independent_directed_models():
    weights=sp.symbols("w0:6")
    for support in (review.A,review.B):
        assert review.directed_correlation(support,weights)==pairwise_correlation(support,weights,21)
    assert icv(review.A,21)==icv(review.B,21)


def test_classification_and_zeros():
    report=review.audit()
    assert all(report["checks"].values()),report["checks"]
    assert len(report["branches"])==6
    assert all(branch["all_b_nonzero"] for branch in report["branches"])
    # The real algebra must be attacked separately from complex cube roots.
    r=sp.symbols("r",real=True)
    assert sp.discriminant(2*r*r+r+2,r)==-15
    assert sp.solve(r*r+3*r+1,r)==[(-3-sp.sqrt(5))/2,(-3+sp.sqrt(5))/2]
    assert (-3+sp.sqrt(5))/2<0


def test_positive_same_support_exact():
    for t in (Fraction(1,7),Fraction(-3,8)):
        plus=tuple(1+t*v for v in review.DIRECTION)
        minus=tuple(1-t*v for v in review.DIRECTION)
        assert min(plus)>0 and min(minus)>0 and plus!=minus
        assert pairwise_correlation(review.A,plus,21)==pairwise_correlation(review.A,minus,21)
    report=review.audit()
    assert report["c_equal_strength_0_to_10"]==[6,1,1,2,1,1,2,3,1,2,1]
    assert report["c_direction_0_to_10"]==[6,-1,-1,2,-1,-1,2,-3,-1,2,-1]


def test_own_exact_fourier_gcd():
    assert review.rational_gcd([1,0,1],[-1,0,0,1])==[Fraction(1)]
    assert review.rational_gcd([-1,0,1],[-1,0,0,1])==[Fraction(-1),Fraction(1)]
    p=[int(i in review.A) for i in range(16)]
    q=[-1]+[0]*20+[1]
    assert review.rational_gcd(p,q)==[Fraction(1)]


if __name__=="__main__":
    for test in (test_independent_directed_models,test_classification_and_zeros,
                 test_positive_same_support_exact,test_own_exact_fourier_gcd):
        test()
        print("PASS",test.__name__)
