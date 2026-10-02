"""Independent exact R5 proof audit; never imports the author's implementation.

Build directed correlation from a full 21-coordinate grid, rather than the
author's folded edge rows. Reproduce the real-branch algebra, and check
the same-support critical direction and Fourier nonvanishing separately.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path

import sympy as sp

N = 21
A = (0, 1, 3, 7, 10, 15)
B = (0, 1, 4, 7, 14, 16)
DIRECTION = (1, -1, 1, -1, -1, 1)


def directed_correlation(support, weights, n=N):
    grid = [sp.Integer(0)] * n
    for location, weight in zip(support, weights, strict=True):
        grid[location] = weight
    return [
        sp.expand(sum(grid[j] * grid[(j + d) % n] for j in range(n)))
        for d in range(n)
    ]


def _trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def _remainder(numerator, denominator):
    """Own rational polynomial division, coefficients in ascending order."""
    remainder = _trim(numerator)
    denominator = _trim(denominator)
    if denominator == [0]:
        raise ZeroDivisionError
    while remainder != [0] and len(remainder) >= len(denominator):
        shift = len(remainder) - len(denominator)
        multiple = remainder[-1] / denominator[-1]
        for j, value in enumerate(denominator):
            remainder[j + shift] -= multiple * value
        remainder = _trim(remainder)
    return remainder


def rational_gcd(p, q):
    p, q = [Fraction(x) for x in p], [Fraction(x) for x in q]
    while q != [0]:
        p, q = q, _remainder(p, q)
    return [value / p[-1] for value in p]


def audit():
    r, s, k, t = sp.symbols("r s k t", real=True)
    x, y, z = sp.symbols("x y z", real=True, nonzero=True)
    a = sp.symbols("a0:6", real=True, nonzero=True)
    b = sp.symbols("b0:6", real=True)
    raw = [sp.factor(p - q) for p, q in zip(
        directed_correlation(A, a), directed_correlation(B, b), strict=True
    )]

    # Six singleton correlations force five B coordinates nonzero. This
    # explicitly does not divide by b3, which may initially be zero.
    singleton_rows = (1, 2, 4, 5, 8, 10)
    singleton_expected = (
        a[0]*a[1]-b[0]*b[1], a[1]*a[2]-b[4]*b[5],
        a[2]*a[3]-b[0]*b[2], a[4]*a[5]-b[0]*b[5],
        a[3]*a[5]-b[1]*b[4], a[0]*a[4]-b[2]*b[4],
    )
    singleton_ok = all(sp.expand(raw[d] - expected) == 0
                       for d, expected in zip(singleton_rows, singleton_expected))
    b0 = b[0]
    substitutions = {b[1]:a[0]*a[1]/b0, b[2]:a[2]*a[3]/b0,
                     b[5]:a[4]*a[5]/b0, b[4]:a[1]*a[2]*b0/(a[4]*a[5])}
    singleton_constraints = [sp.factor(raw[d].subs(substitutions)) for d in (8,10)]

    # Re-derive the qh=1 step over the reals in the written review. Given
    # that step, generate and independently compare the three double rows.
    general_a = (r*x, z, r*y, x, y, r*z)
    general_b = (s, r*x*z/s, r*x*y/s, t, s, r*y*z/s)
    general = [sp.factor(p-q) for p,q in zip(
        directed_correlation(A,general_a), directed_correlation(B,general_b),strict=True)]
    double_rows = [sp.factor(general[d]/product)
                   for d,product in ((3,x*y),(6,x*z),(9,y*z))]
    double_differences = [sp.factor(double_rows[0]-double_rows[j]) for j in (1,2)]
    double_ok = (
        sp.simplify(double_differences[0]+r**2*z*(x-y)/s**2)==0
        and sp.simplify(double_differences[1]-r**2*x*(y-z)/s**2)==0
    )

    normalized = [sp.factor(p-q) for p,q in zip(
        directed_correlation(A,(r,1,r,1,1,r)),
        directed_correlation(B,(s,k,k,t,s,k)),strict=True)]
    sk_equation = normalized[1]
    double_equation = normalized[3]
    triple_equation = normalized[7]
    norm_equation = normalized[0]
    triple_substituted = sp.factor(triple_equation.subs(
        {s:r/k,t:(r*r+1-k*k)/k}, simultaneous=True)*k*k/r)
    k_squared = sp.solve(triple_substituted,k**2)[0]
    norm_times_k_squared = sp.factor(norm_equation.subs(
        {s:r/k,t:(r*r+1-k*k)/k}, simultaneous=True)*k*k)
    eliminant = sp.factor(norm_times_k_squared.subs(k**2,k_squared))
    expected_eliminant = sp.Rational(9,25)*(r-1)**2*(r*r+3*r+1)
    classification_algebra_ok = (
        sp.expand(sk_equation-(r-s*k))==0
        and sp.expand(double_equation-(r*r+1-k*k-k*t))==0
        and sp.expand(triple_equation-(3*r-s*s-2*s*t))==0
        and sp.expand(k_squared-(2*r*r+r+2)/5)==0
        and sp.expand(eliminant-expected_eliminant)==0
    )

    branch_checks = []
    for root in (sp.Integer(1),(-3+sp.sqrt(5))/2,(-3-sp.sqrt(5))/2):
        for epsilon in (1,-1):
            if root == 1:
                aw = (1,)*6
                bw = (epsilon,)*6
            else:
                aw = (root,1,root,1,1,root)
                bw = tuple(epsilon*sp.sqrt(-root)*entry for entry in (-1,1,1,2,-1,1))
            residual = [sp.simplify(p-q) for p,q in zip(
                directed_correlation(A,aw),directed_correlation(B,bw),strict=True)]
            branch_checks.append({"r":str(root),"epsilon":epsilon,
                                  "all_21_equal":all(value==0 for value in residual),
                                  "all_b_nonzero":all(sp.simplify(value)!=0 for value in bw)})

    ones = (1,)*6
    c0 = directed_correlation(A,ones)
    cv = directed_correlation(A,DIRECTION)
    plus = directed_correlation(A,tuple(1+t*v for v in DIRECTION))
    minus = directed_correlation(A,tuple(1-t*v for v in DIRECTION))
    plus_minus_ok = all(sp.expand(p-q)==0 for p,q in zip(plus,minus,strict=True))
    quadratic_ok = all(sp.expand(p-c-t*t*v)==0
                       for p,c,v in zip(plus,c0,cv,strict=True))
    normalized_difference = [sp.factor((p/(6*(1+t*t)))-c/6)
                             for p,c in zip(plus,c0,strict=True)]
    scaling_ok = all(sp.simplify(d-t*t*(v-c)/(6*(1+t*t)))==0
                    for d,v,c in zip(normalized_difference,cv,c0,strict=True))
    scaling_nonzero = any(v != c for v,c in zip(cv,c0,strict=True))
    stabilizers = [(sign,shift) for sign in (1,-1) for shift in range(N)
                   if {(sign*point+shift)%N for point in A}==set(A)]

    X=sp.symbols("X")
    support_polynomial=sum(X**point for point in A)
    line_polynomial=sum((1+t*v)*X**point for point,v in zip(A,DIRECTION,strict=True))
    line_factor=(1+X**3+X**15)*((1+t)+(1-t)*X**7)
    line_factor_ok=sp.rem(line_polynomial-line_factor,X**21-1,X)==0
    cyclotomic_remainders={str(d):str(sp.rem(support_polynomial,sp.cyclotomic_poly(d,X),X))
                           for d in (1,3,7,21)}
    cyclotomic_coprime = all(sp.gcd(support_polynomial,sp.cyclotomic_poly(d,X))==1
                            for d in (1,3,7,21))
    raw_p=[int(i in A) for i in range(max(A)+1)]
    raw_q=[-1]+[0]*(N-1)+[1]
    own_gcd=rational_gcd(raw_p,raw_q)
    checks={"six_singleton_rows":singleton_ok,"double_rows_force_equal_xyz":double_ok,
            "independent_eliminant":classification_algebra_ok,
            "six_real_signed_branches":all(v["all_21_equal"] and v["all_b_nonzero"]
                                           for v in branch_checks),
            "same_support_plus_minus":plus_minus_ok,"quadratic_expansion":quadratic_ok,
            "normalized_change_exact_order_two":scaling_ok and scaling_nonzero,
            "trivial_dihedral_stabilizer":stabilizers==[(1,0)],
            "fourier_nonzero_cyclotomic":cyclotomic_coprime,
            "fourier_nonzero_own_euclid":own_gcd==[Fraction(1)],
            "same_support_line_factorization":line_factor_ok}
    return {"scope":"R5 global prescribed-support real classification and same-support instability only",
            "n":N,"A":A,"B":B,"checks":checks,
            "raw_directed_equations_0_to_10":[str(v) for v in raw[:11]],
            "remaining_singleton_constraints":[str(v) for v in singleton_constraints],
            "double_differences":[str(v) for v in double_differences],
            "normalized_equations":[str(v) for v in normalized[:11]],
            "k_squared":str(k_squared),"norm_times_k_squared":str(norm_times_k_squared),
            "eliminant":str(eliminant),"branches":branch_checks,
            "c_equal_strength_0_to_10":c0[:11],"c_direction_0_to_10":cv[:11],
            "normalized_correlation_change":[str(v) for v in normalized_difference[:11]],
            "stabilizers":stabilizers,"cyclotomic_remainders":cyclotomic_remainders,
            "line_factorization_mod_X21_minus_1":str(line_factor),
            "own_rational_gcd":[str(v) for v in own_gcd]}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,default=Path(__file__).resolve().parents[1]/
                        "results/2026-10-01-weighted-six-review")
    args=parser.parse_args()
    report=audit()
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"independent-audit.json").write_text(json.dumps(report,indent=2,default=str)+"\n")
    lines=[f"{'PASS' if ok else 'FAIL'} {name}" for name,ok in report["checks"].items()]
    (args.out/"verification.txt").write_text("\n".join(lines)+"\n")
    print("\n".join(lines))
    if not all(report["checks"].values()):
        raise SystemExit(1)


if __name__=="__main__":
    main()
