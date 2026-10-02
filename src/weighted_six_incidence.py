"""Exact weighted incidence certificates for thirteen fixed cyclic six-pairs.

The competitors in this module have prescribed supports.  Binary homometry
does not enumerate all supports of possible weighted competitors.  No global
standard-coordinate sparse phase-retrieval conjecture is claimed here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path
import time

from sympy import Matrix, Poly, eye, sqrt, symbols, factor, zeros, gcdex, ilcm

ROOT = Path(__file__).resolve().parents[1]
# Copy the published-in-repo seed coordinates, rather than depend on its
# matching enumerator or unweighted mechanism classifications.
SEEDS = (
    (17, (0, 1, 2, 3, 8, 12), (0, 1, 2, 6, 7, 9)),
    (19, (0, 1, 2, 3, 6, 10), (0, 1, 2, 4, 5, 11)),
    (21, (0, 1, 2, 4, 7, 14), (0, 1, 3, 7, 8, 10)),
    (21, (0, 1, 2, 5, 6, 15), (0, 1, 2, 6, 7, 10)),
    (21, (0, 1, 3, 7, 10, 15), (0, 1, 4, 7, 14, 16)),
    (23, (0, 1, 2, 3, 7, 17), (0, 1, 2, 4, 17, 18)),
    (24, (0, 1, 2, 5, 7, 16), (0, 1, 2, 6, 9, 11)),
    (27, (0, 1, 2, 3, 7, 19), (0, 1, 2, 3, 8, 12)),
    (27, (0, 1, 2, 6, 19, 22), (0, 1, 3, 17, 21, 22)),
    (28, (0, 1, 2, 4, 12, 23), (0, 1, 3, 5, 11, 12)),
    (30, (0, 1, 2, 6, 19, 22), (0, 1, 3, 9, 13, 14)),
    (30, (0, 1, 3, 5, 12, 25), (0, 1, 6, 9, 11, 13)),
    (31, (0, 1, 2, 5, 11, 19), (0, 1, 2, 6, 20, 23)),
)


def quadratic_matrices(support, n):
    """H_d such that q_d(w)=w^T H_d w/2.

    q_0 is squared norm; other q_d count unordered weighted pairs.  Directed
    autocorrelation is q_d except at a nonzero antipodal class, where it is
    2*q_d.  The row scaling is invertible, so the exact fibres coincide.
    """
    if n <= 0 or len(set(support)) != len(support):
        raise ValueError("require a positive modulus and distinct coordinates")
    if any(x < 0 or x >= n for x in support):
        raise ValueError("coordinates must lie in the cyclic grid")
    k = len(support)
    rows = [2 * eye(k)] + [zeros(k, k) for _ in range(n // 2)]
    for i, j in combinations(range(k), 2):
        d = abs(support[i] - support[j])
        d = min(d, n - d)
        rows[d][i, j] += 1
        rows[d][j, i] += 1
    return rows


def weighted_coefficients(support, n, weights):
    w = Matrix(weights)
    if len(weights) != len(support):
        raise ValueError("one weight per support coordinate is required")
    return Matrix([(w.T * h * w)[0] / 2 for h in quadratic_matrices(support, n)])


def incidence_data(n, a, b):
    ha, hb = quadratic_matrices(a, n), quadratic_matrices(b, n)
    one = Matrix([1] * 6)
    ja, jb = Matrix.vstack(*[(h * one).T for h in ha]), Matrix.vstack(*[(h * one).T for h in hb])
    j = ja.row_join(-jb)
    h = [Matrix.diag(x, -y) for x, y in zip(ha, hb)]
    normalized = j.col_join(Matrix([[1] * 12]))
    null = normalized.nullspace()
    tangent = Matrix.hstack(*null) if null else zeros(12, 0)
    left = j.T.nullspace()
    projected = []
    for ell in left:
        form = sum((ell[d] * h[d] / 2 for d in range(len(h))), zeros(12, 12))
        projected.append(tangent.T * form * tangent)
    return dict(ha=ha, hb=hb, ja=ja, jb=jb, j=j, h=h,
                tangent=tangent, left=left, projected=projected)


def enc_matrix(m):
    return [[str(x) for x in row] for row in m.tolist()]


def rank_minor(m):
    cols = list(m.rref()[1])
    rows = list(m[:, cols].T.rref()[1])
    minor = m.extract(rows, cols)
    return dict(rows=rows, columns=cols, determinant=str(minor.det()))


def benchmark_real_branches():
    """One representative per sign-independent real projective type.

    Multiply A by any u != 0 and B independently by +/-u.  The competitor
    may initially be supported on a subset of B: the equations force all six
    B weights nonzero when all six A weights are nonzero.
    """
    out = [dict(r=1, a=[1] * 6, b=[1] * 6)]
    for r in [(-3 + sqrt(5)) / 2, (-3 - sqrt(5)) / 2]:
        k = sqrt(-r)
        out.append(dict(r=r, a=[r, 1, r, 1, 1, r], b=[-k, k, k, 2*k, -k, k]))
    return out


def benchmark_elimination():
    r = symbols("r", real=True)
    k2 = (2*r*r + r + 2) / 5
    # d=7 and the doubled rows imply these expressions.
    t_times_k = (3*r*r - r + 3) / 5
    norm_difference = factor(3*(r*r + 1) - (2*r*r/k2 + 3*k2 + t_times_k**2/k2))
    return dict(variable="r", k_squared=str(k2), t_times_k=str(t_times_k),
                norm_difference=str(norm_difference),
                eliminant_coefficients=[9, 9, -36, 9, 9],
                eliminant_factored="9*(r - 1)**2*(r**2 + 3*r + 1)",
                denominator="5*(2*r**2 + r + 2)")


def benchmark_fourier_certificate():
    """Integer Bezout identity: U*P_A+V*(x^21-1)=12.

    Consequently the equal-strength benchmark A has no Fourier zero.
    """
    x = symbols("x")
    p = sum(x**i for i in SEEDS[4][1])
    u, v, g = gcdex(p, x**21-1, x)
    assert g == 1
    den = ilcm(*[q.q for q in Poly(u, x).all_coeffs()+Poly(v, x).all_coeffs()])
    u, v = Poly(u*den, x), Poly(v*den, x)
    return dict(coefficient_order="ascending", modulus=21, constant=int(den),
                u=[int(u.nth(i)) for i in range(u.degree()+1)],
                v=[int(v.nth(i)) for i in range(v.degree()+1)])


def build_certificates():
    records = []
    for index, (n, a, b) in enumerate(SEEDS, 1):
        data = incidence_data(n, a, b)
        tangent = data["tangent"]
        if index == 2:
            local = "two real analytic curves after fixing common scale"
        elif index == 7:
            local = "exact affine line after fixing common scale"
        else:
            local = "isolated after fixing common scale"
        records.append(dict(seed=f"R{index}", n=n, a=a, b=b,
                            active_rows=[d for d, h in enumerate(data["h"]) if h != zeros(12, 12)],
                            rank_a=data["ja"].rank(), rank_b=data["jb"].rank(),
                            rank_incidence=data["j"].rank(),
                            normalized_tangent_dimension=tangent.cols,
                            jacobian=enc_matrix(data["j"]),
                            rank_minor=rank_minor(data["j"]),
                            normalized_tangent=enc_matrix(tangent),
                            left_null=[enc_matrix(x) for x in data["left"]],
                            quadratic_obstructions=[enc_matrix(x) for x in data["projected"]],
                            candidate_local_real_classification=local))
    n, a, b = SEEDS[4]
    branches = []
    for row in benchmark_real_branches():
        aa, bb = row["a"], row["b"]
        branches.append(dict(r=str(row["r"]), a=list(map(str, aa)), b=list(map(str, bb)),
                             coefficients_a=list(map(str, weighted_coefficients(a, n, aa))),
                             coefficients_b=list(map(str, weighted_coefficients(b, n, bb)))))
    return dict(status="COMPUTED; W21 and R5 reviewed; other template-local conclusions pending separate review",
                scope="13 prescribed pairs, nonzero real strengths; no arbitrary-support classification",
                normalization="sum of the twelve amplitudes = 12, near the all-ones point",
                seeds=records, benchmark_real_projective_branches=branches,
                benchmark_elimination=benchmark_elimination(),
                benchmark_fourier_bezout=benchmark_fourier_certificate())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "results/2026-10-01-weighted-six-incidence")
    args = parser.parse_args()
    start = time.monotonic()
    payload = build_certificates()
    args.out.mkdir(parents=True, exist_ok=True)
    target = args.out / "certificates.json"
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    summary = dict(status=payload["status"], seconds=round(time.monotonic()-start, 3),
                   sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                   seeds=13, locally_isolated=[x["seed"] for x in payload["seeds"]
                                                if x["candidate_local_real_classification"].startswith("isolated")],
                   benchmark_positive_projective_types=1, benchmark_real_projective_types=3)
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
