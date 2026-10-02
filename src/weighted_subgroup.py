"""Exact periodic-support controls for real cyclic phase retrieval.

The group/fiber theorems are proved in notes/2026-10-01-weighted-subgroup.md.
This module constructs rational certificates; it is not a general solver.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import time

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]


def autocorrelation(x):
    """Full oriented autocorrelation; real strengths, including lag zero."""
    n = len(x)
    if n == 0:
        raise ValueError("A signal must have positive ambient length")
    return tuple(sum(x[i] * x[(i + d) % n] for i in range(n)) for d in range(n))


def convolve(x, u):
    if len(x) != len(u) or not x:
        raise ValueError("Signals must have the same positive length")
    n = len(x)
    nonzero = [(j, v) for j, v in enumerate(u) if v]
    return tuple(sum(v * x[(i - j) % n] for j, v in nonzero) for i in range(n))


def period_subgroup(n, support):
    if n < 1:
        raise ValueError("Ambient order must be positive")
    s = frozenset(support)
    if not s or any(not isinstance(i, int) or not 0 <= i < n for i in s):
        raise ValueError("Support must be nonempty and contained in the ambient group")
    return tuple(t for t in range(n) if all((i + t) % n in s for i in s))


def folded_difference_set(n, support):
    s = tuple(support)
    period_subgroup(n, s)  # validate
    return tuple(sorted({min((a-b) % n, (b-a) % n) for a in s for b in s}))


def quotient_lift(q, m, residues=(0, 1, 3)):
    if q < 1 or m < 1:
        raise ValueError("Both quotient and subgroup orders must be positive")
    r = tuple(residues)
    if not r or len(set(r)) != len(r) or any(not isinstance(a, int) or not 0 <= a < q for a in r):
        raise ValueError("Residues must be distinct points of the quotient")
    return q*m, tuple(sorted(a+q*j for a in r for j in range(m)))


def distinct_ordered_differences(q, residues):
    r = tuple(residues)
    if len(r) < 3 or len(set(r)) != len(r):
        return False
    d = [(a-b) % q for a in r for b in r if a != b]
    return 0 not in d and len(d) == len(set(d))


def order_three_kernel(t):
    """Classical rational all-pass circle on Z_3, near delta_0 at t=0."""
    t = Fraction(t)
    denominator = 1+3*t*t
    return ((1-t*t)/denominator, 2*t*(t-1)/denominator, 2*t*(t+1)/denominator)


def cayley_kernel(m, t):
    """Rational orthogonal circulant via Cayley transform of P-P^T."""
    if m < 1:
        raise ValueError("Subgroup order must be positive")
    t = sp.Rational(Fraction(t).numerator, Fraction(t).denominator)
    p = sp.zeros(m)
    for j in range(m):
        p[(j+1) % m, j] = 1
    skew = p-p.T
    matrix = (sp.eye(m)+t*skew)*(sp.eye(m)-t*skew).inv()
    return tuple(Fraction(int(matrix[i, 0].p), int(matrix[i, 0].q)) for i in range(m))


def embed_kernel(n, q, kernel):
    if n != q*len(kernel):
        raise ValueError("The kernel order and quotient must multiply to the ambient order")
    result = [Fraction(0)]*n
    for j, value in enumerate(kernel):
        result[q*j] = value
    return tuple(result)


def jacobian(x, support):
    n = len(x)
    return sp.Matrix([[x[(a+d) % n]+x[(a-d) % n] for a in support] for d in range(n//2+1)])


def rigid_squared_distance(x, y):
    n = len(x)
    return min(sum((y[i]-sign*x[(orientation*i+shift) % n])**2 for i in range(n))
               for sign in (-1, 1) for orientation in (-1, 1) for shift in range(n))


def recover_fixed_support(power, q, m, residues=(0, 1, 3)):
    """Reconstruct consistent generic power data modulo subgroup phase units.

    This numerical demonstration chooses the first coset's block transform
    positive at every frequency. Its domain excludes vanishing block Fourier
    coefficients and does not solve unknown-support or inconsistent noisy data.
    """
    residues = tuple(residues)
    if len(power) != q*m or not distinct_ordered_differences(q, residues):
        raise ValueError("Expected a quotient lift with distinct ordered differences")
    a, b, c = residues[:3]
    block = np.empty((len(residues), m), dtype=np.complex128)
    for l in range(m):
        coefficients = np.fft.ifft(np.asarray(power)[l::m])

        def product(i, j):
            return coefficients[(i-j) % q]*np.exp(2j*np.pi*l*(i-j)/(q*m))

        pab, pac, pbc = product(a, b), product(a, c), product(b, c)
        if min(abs(pab), abs(pac), abs(pbc)) == 0:
            raise ValueError("Generic reconstruction excludes zero pair products")
        anchor = np.sqrt(abs(pab)*abs(pac)/abs(pbc))
        block[0, l] = anchor
        for i, residue in enumerate(residues[1:], 1):
            block[i, l] = np.conj(product(a, residue))/anchor
    result = np.zeros(q*m, dtype=np.complex128)
    for i, residue in enumerate(residues):
        result[residue::q] = np.fft.ifft(block[i])
    if np.max(np.abs(result.imag)) > 1e-8:
        raise ValueError("Power data failed the real consistent-signal control")
    return result.real


def subgroup_orbit_distance(x, y, q):
    """Minimum Euclidean distance under the full real H-spectral-unit group."""
    if len(x) != len(y) or len(x) % q:
        raise ValueError("Ambient orders must agree and be divisible by q")
    a = np.fft.fft(np.asarray(x, dtype=float).reshape(-1, q).T, axis=1)
    b = np.fft.fft(np.asarray(y, dtype=float).reshape(-1, q).T, axis=1)
    # At conjugate frequencies optimal phases conjugate; self-conjugate
    # frequencies have real inner products and allow either sign.
    squared = (np.sum(abs(a)**2+abs(b)**2)-2*np.sum(abs(np.sum(a*np.conj(b), axis=0))))/a.shape[1]
    return float(np.sqrt(max(0.0, squared)))


def punctured_certificate():
    """Exact aperiodic Z_35 certificate with a specified real algebraic partner.

    The partner is specified by a quartic isolated root and a rational matrix
    expression. Positivity/nonintrinsicness use exact norm bounds, not decimals.
    """
    q, m = 7, 5
    n, full = quotient_lift(q, m)
    support = tuple(i for i in full if i != 0)
    blocks = {0: (0, 2, 3, 5, 7), 1: (11, 13, 17, 19, 23), 3: (29, 31, 37, 41, 43)}
    x = [sp.Rational(0)]*n
    for residue, block in blocks.items():
        for j, value in enumerate(block):
            x[residue+q*j] = sp.Rational(value)
    t, v, z = sp.symbols("t v z", real=True)
    p = sp.zeros(m)
    for j in range(m):
        p[(j+1) % m, j] = 1
    l1, l2 = p-p.T, p**2-(p**2).T
    skew = t*l1+v*l2
    denominator = sp.factor((sp.eye(m)-skew).det())
    numerator = sp.factor(((sp.eye(m)+skew)*(sp.eye(m)-skew).adjugate()*sp.Matrix(blocks[0]))[0])
    polynomial = sp.Poly(numerator.subs(v, sp.Rational(1, 1000)), t).clear_denoms()[1].primitive()[1]
    intervals = sp.polys.polytools.intervals(polynomial, eps=sp.Rational(1, 10**8))
    chosen = [(interval, multiplicity) for interval, multiplicity in intervals if abs(interval[0]) < sp.Rational(1, 1000) and abs(interval[1]) < sp.Rational(1, 1000)]
    assert len(chosen) == 1 and chosen[0][1] == 1
    root_interval = chosen[0][0]
    norm2 = sum(value**2 for value in x)
    # ||C-I|| <= 4(|t|+|v|) < 8/1000; hence displacement squared < 1.
    displacement_squared_bound = sp.Rational(8, 1000)**2*norm2
    assert displacement_squared_bound < 1
    rigid_separation = min(sum((x[i]-sign*x[(orientation*i+shift) % n])**2 for i in range(n))
                           for sign in (-1, 1) for orientation in (-1, 1) for shift in range(n)
                           if (sign, orientation, shift) != (1, 1, 0))
    assert rigid_separation > 4 and period_subgroup(n, support) == (0,)
    gcds = [sp.gcd(sp.Poly(sum(block[j]*z**j for j in range(m)), z), sp.Poly(z**m-1, z)) for block in blocks.values()]
    assert all(g.degree() == 0 for g in gcds)
    gradient = [sp.diff(numerator, variable).subs({t: 0, v: 0}) for variable in (t, v)]
    tangent = 2*(sp.Rational(-2, 5)*l1+l2)
    tangent_x = [sp.Rational(0)]*n
    for residue, block in blocks.items():
        values = tangent*sp.Matrix(block)
        for j, value in enumerate(values):
            tangent_x[residue+q*j] = value
    assert tangent_x[0] == 0 and any(tangent_x)
    j = jacobian(x, support)
    assert j.rank() == 13 and j*sp.Matrix([tangent_x[i] for i in support]) == sp.zeros(n//2+1, 1)
    return {"status": "COMPUTED", "N": n, "support": list(support), "period_subgroup": [0],
            "folded_distance_classes": list(folded_difference_set(n, support)), "x": list(map(str, x)),
            "cayley_convention": "P[j+1,j]=1; L1=P-P.T; L2=P^2-(P^2).T; C=(I+t L1+v L2)(I-t L1-v L2)^-1",
            "hole_numerator": str(numerator), "denominator": str(denominator), "hole_gradient_at_identity": list(map(str, gradient)),
            "partner_v": "1/1000", "partner_t_polynomial_coefficients": list(map(str, polynomial.all_coeffs())),
            "partner_t_isolating_interval": list(map(str, root_interval)),
            "partner_definition": "Apply C at the uniquely isolated real t root and v=1/1000 to each of the three coset blocks; embed in Z35.",
            "norm_squared_x": str(norm2), "strict_displacement_squared_upper_bound": str(displacement_squared_bound),
            "minimum_nonidentity_intrinsic_squared_separation_of_x": str(rigid_separation),
            "minimum_positive_amplitude_x": "2", "block_spectral_polynomial_gcds": [str(g.as_expr()) for g in gcds],
            "jacobian_shape": list(j.shape), "jacobian_rank": j.rank(), "exact_nonzero_tangent": list(map(str, tangent_x))}


def certificate():
    started = time.perf_counter()
    n, s = quotient_lift(7, 3)
    x = [Fraction(0)]*n
    for i, a in enumerate(s):
        x[a] = Fraction(10+i)
    x = tuple(x)
    u = embed_kernel(n, 7, order_three_kernel(Fraction(1, 10)))
    y = convolve(x, u)
    assert autocorrelation(u) == (Fraction(1),)+(Fraction(0),)*(n-1)
    assert autocorrelation(x) == autocorrelation(y)
    assert all(y[a] > 0 for a in s)
    assert all(y[a] == 0 for a in range(n) if a not in s)
    distance = rigid_squared_distance(x, y)
    assert distance > 0
    z = sp.symbols("z")
    poly = sum(sp.Rational(v.numerator, v.denominator)*z**i for i, v in enumerate(x))
    spectral_gcd = sp.gcd(sp.Poly(poly, z), sp.Poly(z**n-1, z))
    assert spectral_gcd.degree() == 0
    j = jacobian(x, s)
    assert j.rank() == 8
    families = []
    # This is a construction/structure check, not a six-subset census.
    for q in (7, 8, 9, 11, 13, 31):
        assert distinct_ordered_differences(q, (0, 1, 3))
        for m in range(3, 13):
            nn, ss = quotient_lift(q, m)
            h = period_subgroup(nn, ss)
            assert h == tuple(q*i for i in range(m))
            ds = folded_difference_set(nn, ss)
            assert len(ds) == (7*m)//2+1 > len(ss)
            kernel = embed_kernel(nn, q, cayley_kernel(m, Fraction(1, 100)))
            assert autocorrelation(kernel) == (Fraction(1),)+(Fraction(0),)*(nn-1)
            families.append({"q": q, "m": m, "N": nn, "K": len(ss), "folded_differences": len(ds), "fiber_dimension": (m-1)//2})
    return {
        "status": "COMPUTED", "scope": "exact rational construction controls, not a census or priority claim",
        "N": n, "support": list(s), "period_subgroup": list(period_subgroup(n, s)),
        "folded_distances": list(folded_difference_set(n, s)),
        "x": list(map(str, x)), "u": list(map(str, u)), "y": list(map(str, y)),
        "autocorrelation": list(map(str, autocorrelation(x))),
        "minimum_positive_y": str(min(y[a] for a in s)), "minimum_rigid_squared_distance": str(distance),
        "ambient_spectral_polynomial_gcd": str(spectral_gcd.as_expr()),
        "jacobian_shape": list(j.shape), "jacobian_rank": j.rank(),
        "aperiodic_puncture": punctured_certificate(),
        "family_controls": families, "elapsed_seconds": time.perf_counter()-started,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT/"results/2026-10-01-weighted-subgroup/certificate.json")
    args = parser.parse_args()
    result = certificate()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"], "output": str(args.out), "elapsed_seconds": result["elapsed_seconds"], "family_controls": len(result["family_controls"])}))
