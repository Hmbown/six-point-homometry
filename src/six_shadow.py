"""Exact integer-shadow decision by signed distance matchings for six-subsets.

A capped run is explicitly undecided.  Full-rank matrices reject a matching
because their integer kernel is zero; rank-deficient matrices use an exact
Smith decomposition.  No bound is imposed on integer lift coordinates.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations, permutations, product
import hashlib
import json
from math import factorial, gcd
from pathlib import Path
import time

from sympy import Matrix, ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp


ROOT = Path(__file__).resolve().parents[1]
EDGES = tuple(combinations(range(6), 2))


def validate_pair(a, b, n):
    if n < 6 or len(a) != 6 or len(b) != 6:
        raise ValueError("expected two six-subsets in Z_n")
    a, b = tuple(sorted(x % n for x in a)), tuple(sorted(x % n for x in b))
    if len(set(a)) != 6 or len(set(b)) != 6:
        raise ValueError("colliding residues")
    if distance_buckets(a, n).keys() != distance_buckets(b, n).keys():
        raise ValueError("different cyclic interval contents")
    if {d: len(v) for d, v in distance_buckets(a, n).items()} != {
            d: len(v) for d, v in distance_buckets(b, n).items()}:
        raise ValueError("different cyclic interval contents")
    return a, b


def distance_buckets(a, n):
    buckets = defaultdict(list)
    for edge in EDGES:
        i, j = edge
        delta = (a[j] - a[i]) % n
        buckets[min(delta, n - delta)].append(edge)
    return dict(sorted(buckets.items()))


def matching_count(a, b, n):
    a, b = validate_pair(a, b, n)
    total = 1
    for d, edges in distance_buckets(a, n).items():
        total *= factorial(len(edges))
        if 2 * d == n:
            total *= 2 ** len(edges)
    return total


def anchored_vector(a, b, n):
    return tuple((x - a[0]) % n for x in a[1:]) + tuple(
        (x - b[0]) % n for x in b[1:])


def matching_matrices(a, b, n):
    """Enumerate every compatible bijection and every antipodal sign choice.

    Row order is increasing distance, then lexicographic A edge.  This fixes
    labelled vertices; repeated distances permute B edges rather than merging
    them.  Each certificate has the target edge and sign for every row.
    """
    a, b = validate_pair(a, b, n)
    ba, bb = distance_buckets(a, n), distance_buckets(b, n)
    distances = list(ba)

    def blocks(index, rows, labels):
        if index == len(distances):
            yield Matrix(rows), tuple(labels)
            return
        d = distances[index]
        for targets in permutations(bb[d]):
            sign_choices = []
            for (i, j), (k, ell) in zip(ba[d], targets):
                da, db = (a[j] - a[i]) % n, (b[ell] - b[k]) % n
                sign_choices.append(tuple(s for s in (1, -1) if (da - s * db) % n == 0))
            for signs in product(*sign_choices):
                new_rows, new_labels = [], []
                for (i, j), (k, ell), sign in zip(ba[d], targets, signs):
                    row = [0] * 10
                    for vertex, value in ((i, -1), (j, 1)):
                        if vertex:
                            row[vertex - 1] = value
                    for vertex, value in ((k, sign), (ell, -sign)):
                        if vertex:
                            row[vertex + 4] = value
                    new_rows.append(row)
                    new_labels.append((i, j, k, ell, sign))
                yield from blocks(index + 1, rows + new_rows, labels + new_labels)

    yield from blocks(0, [], [])


def maximal_minor(m):
    """Choose an exact nonzero rank-sized minor, with a reproducible certificate."""
    _, columns = m.rref()
    if not columns:
        return (), (), 1
    _, rows = m[:, list(columns)].T.rref()
    delta = int(m.extract(rows, columns).det())
    assert delta != 0
    return tuple(rows), tuple(columns), delta


def coprime_kernel_lift(m, v, n):
    """Construct Lemma S3's lift, or None if the chosen minor is not coprime."""
    v = Matrix(v)
    if any(int(x) % n for x in m * v):
        raise ValueError("input does not satisfy matching modulo n")
    rows, columns, delta = maximal_minor(m)
    if gcd(delta, n) != 1:
        return None
    if not columns:
        return tuple(int(x) for x in v)
    free = [j for j in range(m.cols) if j not in columns]
    z = Matrix.zeros(m.cols, 1)
    f = v[free, :]
    for j in free:
        z[j] = delta * v[j]
    pivot = -m.extract(rows, columns).adjugate() * m.extract(rows, free) * f
    for j, value in zip(columns, pivot):
        z[j] = value
    z *= pow(delta, -1, n)
    assert m * z == Matrix.zeros(m.rows, 1)
    assert all((int(z[j]) - int(v[j])) % n == 0 for j in range(m.cols))
    return tuple(int(x) for x in z)


def smith_kernel_lift(m, v, n):
    """Solve z=v+n*y, Mz=0 over Z; returns lift and an exact decision record."""
    v = Matrix(v)
    mv = m * v
    if any(int(x) % n for x in mv):
        raise ValueError("input does not satisfy matching modulo n")
    rhs = -mv / n
    dm = DomainMatrix.from_Matrix(m).convert_to(ZZ)
    dd, uu, vv = smith_normal_decomp(dm)
    d, u, transform = dd.to_Matrix(), uu.to_Matrix(), vv.to_Matrix()
    assert u * m * transform == d
    transformed = u * rhs
    q = Matrix.zeros(m.cols, 1)
    diagonal = [int(d[i, i]) for i in range(min(m.shape))]
    for i in range(m.rows):
        divisor = int(d[i, i]) if i < m.cols else 0
        value = int(transformed[i])
        if (divisor and value % divisor) or (not divisor and value):
            # This row is an integer combination of matching equations giving
            # an unsatisfiable divisibility (or zero-row) condition.
            return None, dict(diagonal=diagonal, failed_row=i, divisor=divisor,
                              value=value, row_combination=[int(x) for x in u[i, :]])
        if divisor:
            q[i] = value // divisor
    z = v + n * transform * q
    assert m * z == Matrix.zeros(m.rows, 1)
    assert all((int(z[j]) - int(v[j])) % n == 0 for j in range(m.cols))
    return tuple(int(x) for x in z), dict(diagonal=diagonal)


def integer_distances(a):
    return Counter(abs(x - y) for x, y in combinations(a, 2))


def shadow_decision(a, b, n, limit=None, save_matrices=True, progress=None):
    a, b = validate_pair(a, b, n)
    expected = matching_count(a, b, n)
    v = anchored_vector(a, b, n)
    records = []
    ranks = Counter()
    start = time.monotonic()
    for number, (m, labels) in enumerate(matching_matrices(a, b, n), 1):
        if limit is not None and number > limit:
            break
        rows, columns, delta = maximal_minor(m)
        rank = len(columns)
        assert abs(delta) <= 252, (rank, delta)
        ranks[rank] += 1
        record = dict(labels=labels, rank=rank, minor_rows=rows,
                      minor_columns=columns, determinant=delta)
        if save_matrices:
            record["matrix"] = [[int(x) for x in row] for row in m.tolist()]
        if rank == 10:
            lift = None
            record["rejection"] = "full column rank: integer kernel is zero"
        else:
            lift, smith = smith_kernel_lift(m, v, n)
            record["smith"] = smith
        records.append(record)
        if lift is not None:
            la = tuple([a[0]] + [x + a[0] for x in lift[:5]])
            lb = tuple([b[0]] + [x + b[0] for x in lift[5:]])
            assert len(set(la)) == len(set(lb)) == 6
            assert integer_distances(la) == integer_distances(lb)
            assert tuple(x % n for x in la) == a and tuple(x % n for x in lb) == b
            return dict(n=n, a=a, b=b, decision="shadow", expected_matchings=expected,
                        checked_matchings=len(records), ranks=dict(ranks),
                        lift_a=la, lift_b=lb, certificates=records,
                        seconds=round(time.monotonic() - start, 3))
        if progress and number % 100 == 0:
            progress(number, expected, dict(ranks))
    exhausted = len(records) == expected
    return dict(n=n, a=a, b=b, decision="purely-cyclic" if exhausted else "undecided-capped",
                expected_matchings=expected, checked_matchings=len(records), ranks=dict(ranks),
                certificates=records, seconds=round(time.monotonic() - start, 3))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--a", required=True, help="comma-separated residues")
    parser.add_argument("--b", required=True, help="comma-separated residues")
    parser.add_argument("--limit", type=int, default=100000)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    a, b = (tuple(map(int, s.split(","))) for s in (args.a, args.b))
    count = matching_count(a, b, args.n)
    print(f"expected matchings={count}; cap={args.limit}; exact 15x10 arithmetic", flush=True)
    result = shadow_decision(a, b, args.n, args.limit,
                             progress=lambda i, total, ranks: print(i, total, ranks, flush=True))
    result["status"] = "COMPUTED-UNVALIDATED until independent certificate audit"
    result["source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    temp = args.out.with_suffix(".tmp")
    temp.write_text(json.dumps(result, sort_keys=True) + "\n")
    temp.replace(args.out)
    print({k: v for k, v in result.items() if k != "certificates"}, flush=True)


if __name__ == "__main__":
    main()
