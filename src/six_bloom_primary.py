"""Exact uncentered labelled matching for the classical six-point Bloom family.

The first three labels give a unimodular pivot. No division by 2, 3 or n
occurs. This is a finite universal matching certificate, not a subset census.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import permutations
import json
from math import gcd
from pathlib import Path
import time

import numpy as np

X = np.array(((0, 0), (1, 0), (-2, 1), (-2, 2), (0, 2), (-1, 3)), dtype=np.int64)
Y = np.array(((0, 0), (1, 0), (2, 1), (-1, 2), (1, 2), (-1, 3)), dtype=np.int64)
PERMS = np.array(tuple(permutations(range(6))), dtype=np.int64)


def eliminated(source: np.ndarray, target: np.ndarray, sign: int, perm: np.ndarray) -> np.ndarray:
    """Solve source(w)=sign*target(v)[perm]+translation from labels 0,1,2."""
    delta = sign * (target[perm[1:3]] - target[perm[0]])
    # source row1 is a; source row2 is b +/- 2a.
    return np.array((delta[0], delta[1] - source[2, 0] * delta[0]), dtype=np.int64)


def residual(source: np.ndarray, target: np.ndarray, sign: int, perm: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    return source[3:] @ matrix - sign * (target[perm[3:]] - target[perm[0]])


def invariants(rows: np.ndarray) -> tuple[int, int]:
    content = 0
    minor = 0
    for a, b in rows.tolist():
        content = gcd(content, gcd(a, b))
    for i, (a, b) in enumerate(rows.tolist()):
        for c, d in rows[:i].tolist():
            minor = gcd(minor, a*d-b*c)
    return content, minor


def primitive(row: np.ndarray) -> tuple[int, int]:
    a, b = map(int, row)
    content = gcd(a, b)
    a, b = a // content, b // content
    return (a, b) if a > 0 or a == 0 and b > 0 else (-a, -b)


def group() -> tuple[np.ndarray, ...]:
    eye = np.eye(2, dtype=np.int64)
    r = np.array(((0, -1), (1, -1)), dtype=np.int64)
    t = np.array(((0, 1), (1, 0)), dtype=np.int64)
    answer = []
    power = eye
    for i in range(3):
        for j in range(2):
            for sign in (1, -1):
                answer.append(sign * (power @ (t if j else eye)))
        power = power @ r
    return tuple(answer)


def point_lists(a: int, b: int, n: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    return (tuple(int(value) % n for value in X @ (a, b)),
            tuple(int(value) % n for value in Y @ (a, b)))


def gap_canon(values: tuple[int, ...], n: int) -> tuple[int, ...]:
    """Independent gap-word implementation; only actual six-element sets."""
    ordered = sorted(values)
    gaps = tuple((ordered[(i+1) % 6]-ordered[i]) % n for i in range(6))
    words = [word[i:]+word[:i] for word in (gaps, gaps[::-1]) for i in range(6)]
    best = min(words)
    points = [0]
    for gap in best[:5]:
        points.append(points[-1] + gap)
    # A minimal gap word need not give the smallest point tuple. The returned
    # tuple is an unambiguous class key; convert separately for comparison.
    return tuple(points)


def small_image(n: int, reference: bool = False) -> dict:
    """Every parameter; retains all admissible and congruent image fibres."""
    if reference:
        from homometry import dihedral_canon as canonical
    else:
        canonical = gap_canon
    fibers = defaultdict(list)
    actual = congruent = 0
    for a in range(n):
        for b in range(n):
            x, y = point_lists(a, b, n)
            if len(set(x)) != 6 or len(set(y)) != 6:
                continue
            actual += 1
            cx, cy = canonical(x, n), canonical(y, n)
            pair = tuple(sorted((cx, cy)))
            congruent += cx == cy
            fibers[pair].append((a, b))
    def orbit(a, b):
        return {tuple(int(value) % n for value in g @ (a, b)) for g in group()}
    entries = []
    for pair, parameters in sorted(fibers.items()):
        unseen = set(parameters)
        orbits = []
        while unseen:
            v = min(unseen)
            found = orbit(*v)
            if not found <= unseen:
                raise AssertionError('formal group fails to preserve image')
            orbits.append(sorted(found))
            unseen -= found
        entries.append(dict(pair=[list(endpoint) for endpoint in pair], congruent=pair[0] == pair[1],
                            parameters=parameters, G_orbits=orbits))
    return dict(n=n, candidates=n*n, actual_parameters=actual, congruent_parameters=congruent,
                nontrivial_pair_count=sum(not entry['congruent'] for entry in entries),
                fiber_histogram=dict(Counter(len(entry['parameters']) for entry in entries)),
                free_G=all(len(orbit(*v)) == 12 for entry in entries for v in entry['parameters']),
                entries=entries)


def even_endpoint_controls(first: int = 9, last: int = 128) -> dict:
    """Immutable-reference certificates for the symbolic even-family lemma."""
    from homometry import dihedral_canon, icv
    entries = []
    for m in range(first, last+1):
        if m < 9:
            raise ValueError('the proved family requires m >= 9')
        n = 2*m
        v, w = (m+3, 1), (-3, m-2)
        xv, yv = point_lists(*v, n)
        xw, yw = point_lists(*w, n)
        classes = [dihedral_canon(endpoint, n) for endpoint in (xv, yv, xw, yw)]
        if not all(len(set(endpoint)) == 6 for endpoint in (xv, yv, xw, yw)):
            raise AssertionError('support collision')
        if classes[1] != classes[2] or len(set(classes)) != 3:
            raise AssertionError('shared endpoint or distinctness fails')
        if not icv(xv, n) == icv(yv, n) == icv(yw, n):
            raise AssertionError('reference homometry fails')
        entries.append(dict(n=n, v=v, w=w, point_sets=[sorted(endpoint) for endpoint in (xv, yv, xw, yw)],
                            endpoint_classes=classes, icv=icv(xv, n)))
    return dict(schema='six-bloom-even-shared-endpoint-v1', status='COMPUTED', complete=True,
                range=[2*first, 2*last], steps=2, controls=len(entries), entries=entries)


def pair_table(limit: int = 4_147_200) -> dict:
    """Batched NumPy gcds; all entries/minors exact signed 64-bit integers."""
    begin = time.monotonic()
    counts = Counter()
    rank1 = Counter()
    rank2 = Counter()
    zeros = []
    witnesses = {}
    maximum_entry = maximum_minor = processed = 0
    for swap in (0, 1):
        ux, uy = (Y, X) if swap else (X, Y)
        y_delta = uy[PERMS[:, 1:]] - uy[PERMS[:, 0, None]]
        for sx in (1, -1):
            for sy in (1, -1):
                for px in PERMS:
                    if processed >= limit:
                        break
                    m = eliminated(X, ux, sx, px)
                    hx = residual(X, ux, sx, px, m)
                    remaining = min(720, limit - processed)
                    hy = (Y[1:] @ m)[None, :, :] - sy * y_delta[:remaining]
                    h = np.concatenate((np.broadcast_to(hx, (remaining, 3, 2)), hy), axis=1)
                    content = np.gcd.reduce(np.abs(h), axis=(1, 2))
                    minors = np.stack([h[:, i, 0]*h[:, j, 1]-h[:, i, 1]*h[:, j, 0]
                                       for i in range(8) for j in range(i)], axis=1)
                    determinant = np.gcd.reduce(np.abs(minors), axis=1)
                    maximum_entry = max(maximum_entry, int(np.max(np.abs(h))))
                    maximum_minor = max(maximum_minor, int(np.max(np.abs(minors))))
                    kinds = np.where(content == 0, 0, np.where(determinant == 0, 1, 2))
                    for kind, count in zip(*np.unique(kinds, return_counts=True)):
                        counts[int(kind)] += int(count)
                    for iy in np.where(kinds == 0)[0]:
                        zeros.append(dict(swap=swap, sx=sx, sy=sy, px=px.tolist(), py=PERMS[iy].tolist(), M=m.tolist()))
                    for iy in np.where(kinds == 1)[0]:
                        direction = primitive(next(row for row in h[iy] if np.any(row)))
                        key = direction + (int(content[iy]),)
                        rank1[key] += 1
                        witnesses.setdefault(('rank1', key), dict(swap=swap, sx=sx, sy=sy, px=px.tolist(), py=PERMS[iy].tolist(), M=m.tolist(), H=h[iy].tolist()))
                    keys, multiplicities = np.unique(np.stack((content[kinds == 2], determinant[kinds == 2]), axis=1), axis=0, return_counts=True)
                    for key, multiplicity in zip(keys.tolist(), multiplicities.tolist()):
                        rank2[tuple(key)] += multiplicity
                        if ('rank2', tuple(key)) not in witnesses:
                            iy = np.where((content == key[0]) & (determinant == key[1]))[0][0]
                            witnesses['rank2', tuple(key)] = dict(swap=swap, sx=sx, sy=sy, px=px.tolist(), py=PERMS[iy].tolist(), M=m.tolist(), H=h[iy].tolist())
                    processed += remaining
                if processed >= limit:
                    break
            if processed >= limit:
                break
        if processed >= limit:
            break
    return dict(schema='six-bloom-uncentered-pair-v1', status='COMPUTED', processed=processed,
                complete=processed == 4_147_200, elapsed_seconds=time.monotonic()-begin,
                maximum_entry=maximum_entry, maximum_minor=maximum_minor,
                ranks=dict(counts), rank0=zeros,
                rank1=[dict(direction=list(k[:2]), content=k[2], count=v, witness=witnesses['rank1', k]) for k, v in sorted(rank1.items())],
                rank2=[dict(content=k[0], minor_gcd=k[1], count=v, witness=witnesses['rank2', k]) for k, v in sorted(rank2.items())])


def endpoint_table() -> dict:
    counts = Counter()
    rank1 = Counter()
    rank2 = Counter()
    zeros = []
    cases = []
    for source_index, source in enumerate((X, Y)):
        for target_index, target in enumerate((X, Y)):
            for sign in (1, -1):
                for perm in PERMS:
                    m = eliminated(source, target, sign, perm)
                    h = residual(source, target, sign, perm, m)
                    c, d = invariants(h)
                    case = dict(source=source_index, target=target_index, sign=sign, permutation=perm.tolist(), M=m.tolist(), H=h.tolist(), content=c, minor_gcd=d)
                    kind = 0 if c == 0 else 1 if d == 0 else 2
                    counts[kind] += 1
                    if kind == 0:
                        zeros.append(case)
                    elif kind == 1:
                        direction = primitive(next(row for row in h if np.any(row)))
                        rank1[direction + (c,)] += 1
                        cases.append(case)
                    else:
                        rank2[c, d] += 1
                        if d > 1:
                            cases.append(case)
    return dict(schema='six-bloom-uncentered-endpoint-v1', status='COMPUTED', complete=True, processed=5760, ranks=dict(counts), rank0=zeros,
                rank1=[dict(direction=list(k[:2]), content=k[2], count=v) for k, v in sorted(rank1.items())],
                rank2=[dict(content=k[0], minor_gcd=k[1], count=v) for k, v in sorted(rank2.items())], cases=cases)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=4_147_200)
    parser.add_argument('--endpoint', action='store_true')
    parser.add_argument('--images', type=int, nargs='+')
    parser.add_argument('--reference', action='store_true')
    parser.add_argument('--even-endpoints', type=int, nargs=2, metavar=('FIRST_M', 'LAST_M'))
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = (even_endpoint_controls(*args.even_endpoints) if args.even_endpoints else
              dict(schema='six-bloom-primary-images-v1', status='COMPUTED', complete=True,
                   reference=args.reference, images=[small_image(n, args.reference) for n in args.images])
              if args.images else endpoint_table() if args.endpoint else pair_table(args.limit))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps({key: result[key] for key in ('schema', 'processed', 'complete', 'ranks') if key in result}, sort_keys=True))


if __name__ == '__main__':
    main()
