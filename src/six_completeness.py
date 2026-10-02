"""Bounded cyclic-cylinder reduction for six-note homometry.

The graph exhaustion bounds every signed K6 matching minor by 135.
A Smith certificate then realizes any given pair in Z x C_q, q <= 135.
This is a structural reduction, not a list of all six-note mechanisms.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import reduce
from itertools import combinations
import json
from math import gcd
from pathlib import Path

from sympy import Matrix, ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp

from six_shadow import EDGES, anchored_vector, matching_matrices, validate_pair

ROOT = Path(__file__).resolve().parents[1]


def tree_masks():
    """All labelled K6 spanning trees, by acyclicity of five edges."""
    result = []
    for selected in combinations(range(15), 5):
        parent = list(range(6))

        def find(v):
            while parent[v] != v:
                v = parent[v]
            return v

        for edge in selected:
            a, b = map(find, EDGES[edge])
            if a == b:
                break
            parent[a] = b
        else:
            result.append(sum(1 << edge for edge in selected))
    return tuple(result)


def graph_minor_bound():
    """Exhaust all 3003 ten-edge subsets; no graph-isomorphism reduction."""
    trees = tree_masks()
    counts = Counter()
    maximum, example = 0, None
    for selected in combinations(range(15), 10):
        graph = sum(1 << edge for edge in selected)
        number = sum(graph & tree == tree for tree in trees)
        counts[number] += 1
        if number > maximum:
            maximum, example = number, [EDGES[i] for i in selected]
    return dict(vertices=6, graph_edges=10, labelled_graphs=sum(counts.values()),
                complete_graph_trees=len(trees), maximum=maximum,
                maximizer_count=counts[maximum], maximizing_graph=example,
                histogram=dict(sorted(counts.items())),
                method="edge subsets and union-find acyclicity; no symmetry quotient")


def cylinder_certificate(a, b, n, matching_index=0):
    """Construct a homometric pair in Z x C_q mapping to the given pair.

    The output contains D,U,V with U M V=D, so the construction can be
    checked by matrix multiplication without trusting the Smith algorithm.
    The index chooses a compatible edge matching, not an optimization of q.
    """
    a, b = validate_pair(a, b, n)
    if matching_index < 0:
        raise ValueError("negative matching index")
    for index, (m, labels) in enumerate(matching_matrices(a, b, n)):
        if index == matching_index:
            break
    else:
        raise ValueError("matching index outside enumeration")
    v = Matrix(anchored_vector(a, b, n))
    d0, u0, v0 = smith_normal_decomp(DomainMatrix.from_Matrix(m).convert_to(ZZ))
    d, u, transform = (x.to_Matrix() for x in (d0, u0, v0))
    assert u * m * transform == d
    diagonal = [int(d[i, i]) for i in range(10)]
    rank = sum(x != 0 for x in diagonal)
    assert all(x != 0 for x in diagonal[:rank])
    w = [int(x) % n for x in transform.inv() * v]
    step = reduce(gcd, [n] + w[:rank])
    q = n // step
    torsion_order = 1
    for divisor in diagonal[:rank]:
        torsion_order *= abs(divisor)
    assert torsion_order <= 135 and torsion_order % q == 0
    torsion = [x // step for x in w[:rank]]
    cylinder = []
    for i in range(10):
        z = sum(int(transform[i, j]) * w[j] for j in range(rank, 10))
        t = sum(int(transform[i, j]) * torsion[j] for j in range(rank)) % q
        cylinder.append((z, t))
    # Restore each independent anchor by adding it to the integer coordinate.
    ca = [(a[0], 0)] + [(z+a[0], t) for z, t in cylinder[:5]]
    cb = [(b[0], 0)] + [(z+b[0], t) for z, t in cylinder[5:]]
    return dict(n=n, a=a, b=b, q=q, rank=rank, free_rank=10-rank,
                torsion_order=torsion_order, cylinder_a=ca, cylinder_b=cb,
                projection_step=step, matching_index=matching_index,
                matrix=m.tolist(), labels=labels, smith_d=d.tolist(),
                smith_u=u.tolist(), smith_v=transform.tolist(),
                smith_diagonal=diagonal, generator_images=w)


def overlap_energy(a, b, n):
    """Exact diagnostic for the universal three-common-note reduction."""
    a, b = validate_pair(a, b, n)
    auto = Counter((x-y) % n for x in a for y in a)
    cross = Counter((x-y) % n for x in a for y in b)
    cross_inversion = Counter((x+y) % n for x in a for y in b)
    energy = sum(count * count for count in auto.values())
    assert energy == sum(count * count for count in cross.values())
    return dict(energy=energy, excess_over_distinct_differences=energy-66,
                max_translation_overlap=max(cross.values()),
                max_ti_overlap=max(max(cross.values()), max(cross_inversion.values())),
                forced_three_common_notes=energy > 72)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    examples = [
        (18, (0,1,4,6,10,13), (0,1,4,7,9,13)),
        (21, (0,1,3,7,10,15), (0,1,4,7,14,16)),
        (37, (0,1,4,10,12,17), (0,1,8,11,13,17)),
    ]
    payload = dict(status="COMPUTED-UNVALIDATED until independent test/review",
                   graph_bound=graph_minor_bound(),
                   cylinder_examples=[cylinder_certificate(a,b,n) for n,a,b in examples])
    # SymPy matrix entries need conversion when serializing certificates.
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, sort_keys=True, default=int) + "\n")
    print(payload["graph_bound"])
    print([(r["n"],r["q"],r["free_rank"]) for r in payload["cylinder_examples"]])


if __name__ == "__main__":
    main()
