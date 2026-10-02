"""Independent algebraic checks of the six-point Bloom image.

Counts invariant fibers without constructing chord classes or assuming a
formula. Replays all parameters in direct-enumerator certificates. A separate
additive quadratic-field check uses explicit anchored translation/inversion,
not a scalar or general linear-group quotient. Integer polynomial identities
are checked using a tiny exact coefficient kernel, without symbolic libraries.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations
import hashlib
import json
from math import comb, isqrt
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[1]
NORMALS = ((1, 0), (0, 1), (-1, 1), (1, 1), (-2, 1), (2, 1),
           (-3, 1), (-1, 2), (1, 2), (-3, 2), (-1, 3), (-2, 3))
PX = ((0, 0), (1, 0), (-2, 1), (-2, 2), (0, 2), (-1, 3))
PY = ((0, 0), (1, 0), (2, 1), (-1, 2), (1, 2), (-1, 3))


def prime(p):
    return isinstance(p, int) and not isinstance(p, bool) and p >= 2 and all(
        p % d for d in range(2, isqrt(p) + 1))


def invariant_key(a, b, p):
    return ((a*a - a*b + b*b) % p, (a*b*(a-b))**2 % p)


def allowed(a, b, p):
    return all((u*a + v*b) % p for u, v in NORMALS)


def invariant_fibers(p):
    """Count all parameters by two polynomial values, not by pair images."""
    if not prime(p) or p in (2, 3, 11):
        raise ValueError("requires a prime characteristic other than 2,3,11")
    fibers = Counter()
    for a in range(p):
        for b in range(p):
            if allowed(a, b, p):
                fibers[invariant_key(a, b, p)] += 1
    return fibers


def point_moments(points, p):
    """Rigid invariants from actual endpoint coordinates; require six points."""
    points = tuple(x % p for x in points)
    if len(points) != 6 or len(set(points)) != 6 or p in (2, 3):
        raise ValueError("six distinct points and invertible six required")
    mean = sum(points) * pow(6, -1, p) % p
    values = [(3*(x-mean)) % p for x in points]
    m2, m3, m6 = [sum(pow(x, j, p) for x in values) % p for j in (2, 3, 6)]
    return m2, m3*m3 % p, m6


def key_from_pair(pair, p):
    mx, my = [point_moments(endpoint, p) for endpoint in pair]
    if mx[0] != my[0]:
        raise AssertionError("unequal second moments")
    s = mx[0]*pow(66, -1, p) % p
    c3 = (mx[1]+my[1]-288*s**3) % p
    c6 = (mx[2]+my[2]-47892*s**3) % p
    return s, (118*c6-13*c3)*pow(162, -1, p) % p


def replay_direct(path):
    """Compare every direct fiber to an independently enumerated key fiber.

    Byte-level parameter coverage, injective fiber->key bindings, and sizes
    establish equality of the partitions, not merely of their headline counts.
    Endpoint moments independently bind each saved actual pair to its key.
    """
    started = time.monotonic()
    raw = path.read_bytes()
    direct = json.loads(raw)
    p = direct['summary']['p']
    counts = invariant_fibers(p)
    histogram = dict(sorted(Counter(counts.values()).items()))
    unseen_keys = set(counts)
    visited = bytearray(p*p)
    vertices = Counter()
    for record in direct['fibers']:
        keys = set()
        for a, b in record['parameters']:
            assert 0 <= a < p and 0 <= b < p and allowed(a, b, p)
            index = p*a+b
            assert not visited[index], (p, a, b, "duplicate")
            visited[index] = 1
            keys.add(invariant_key(a, b, p))
        assert len(keys) == 1, (p, "split invariant fiber")
        key = keys.pop()
        assert key in unseen_keys, (p, "duplicate invariant fiber")
        unseen_keys.remove(key)
        assert counts[key] == len(record['parameters'])
        assert key_from_pair(record['pair'], p) == key
        vertices.update(tuple(endpoint) for endpoint in record['pair'])
    assert not unseen_keys and sum(visited) == sum(counts.values())
    assert len(counts) == direct['summary']['pairs']
    if p != 31:
        assert set(vertices.values()) <= {1}
    return {'p': p, 'method': 'collision complement and (s,e_squared) fibers',
            'parameters': p*p, 'admissible_parameters': sum(counts.values()),
            'pairs': len(counts), 'fiber_histogram': histogram,
            'all_direct_parameter_fibers_equal': True,
            'all_saved_endpoint_moments_bound': True,
            'vertex_degree_histogram': dict(sorted(Counter(vertices.values()).items())),
            'direct_file': str(path.relative_to(ROOT)),
            'direct_sha256': hashlib.sha256(raw).hexdigest(),
            'seconds': round(time.monotonic()-started, 6)}


# Tiny polynomial kernel: (i,j)->coefficient of a^i b^j.
def add(*polynomials):
    out = Counter()
    for poly in polynomials:
        for ij, value in poly.items():
            out[ij] += value
    return {ij: value for ij, value in out.items() if value}


def scale(poly, c):
    return {ij: c*value for ij, value in poly.items() if c*value}


def mul(x, y):
    out = Counter()
    for (i, j), a in x.items():
        for (k, l), b in y.items():
            out[i+k, j+l] += a*b
    return {ij: value for ij, value in out.items() if value}


def power(poly, n):
    out = {(0, 0): 1}
    for _ in range(n):
        out = mul(out, poly)
    return out


def linear(u, v, n=1):
    return {(i, n-i): comb(n, i)*u**i*v**(n-i)
            for i in range(n+1) if comb(n, i)*u**i*v**(n-i)}


def symbolic_checks():
    s = {(2, 0): 1, (1, 1): -1, (0, 2): 1}
    e = {(2, 1): 1, (1, 2): -1}
    d = mul(mul(linear(1, 1), linear(2, -1)), linear(1, -2))
    s3, e2, de = power(s, 3), power(e, 2), mul(d, e)
    assert add(power(d, 2), scale(e2, 27)) == scale(s3, 4)
    for points, sign in ((PX, -1), (PY, 1)):
        su = sum(u for u, v in points)
        sv = sum(v for u, v in points)
        assert su % 2 == sv % 2 == 0
        moments = {j: add(*(linear(3*u-su//2, 3*v-sv//2, j)
                           for u, v in points)) for j in (2, 3, 6)}
        assert moments[2] == scale(s, 66)
        assert moments[3] == add(scale(d, 6), scale(e, sign*243))
        assert power(moments[3], 2) == add(scale(s3, 144), scale(e2, 58077),
                                                 scale(de, sign*2916))
        assert moments[6] == add(scale(s3, 23946), scale(e2, 6399),
                                        scale(de, sign*4860))
    directed = []
    for points in (PX, PY):
        directed.append(Counter((x-u, y-v) for x, y in points for u, v in points))
    assert directed[0] == directed[1]
    assert 118*12798-13*116154 == 162
    determinant = 58077*(-4860)-(-2916)*6399
    assert determinant == -2**4*3**12*31
    values = {abs(u*y-v*x) for (u, v), (x, y) in combinations(NORMALS, 2)}
    assert values == {1, 2, 3, 4, 5, 7, 8}
    return {'integer_polynomial_identities': True, 'directed_difference_identity': True,
            'collision_determinants': sorted(values),
            'single_endpoint_determinant': determinant}


class QuadraticField:
    """F_p[t]/(t²−d), elements encoded u+p*v; additive classes only."""
    def __init__(self, p, d):
        if not prime(p) or p == 2 or pow(d % p, (p-1)//2, p) != p-1:
            raise ValueError('odd prime and quadratic nonresidue required')
        self.p, self.d, self.q = p, d % p, p*p

    def add(self, x, y):
        p = self.p
        return (x % p+y % p) % p + p*((x//p+y//p) % p)

    def neg(self, x):
        p = self.p
        return (-(x % p)) % p + p*((-(x//p)) % p)

    def scale(self, x, n):
        p = self.p
        return ((x % p)*n) % p + p*((x//p*n) % p)

    def mul(self, x, y):
        p = self.p
        a, b, c, d = x % p, x//p, y % p, y//p
        return (a*c+self.d*b*d) % p + p*((a*d+b*c) % p)

    def canonical(self, points):
        return min(tuple(sorted(self.add(self.scale(x, sign),
                                         self.scale(anchor, -sign)) for x in points))
                   for sign in (1, -1) for anchor in points)

    def key(self, a, b):
        s = self.add(self.add(self.mul(a, a), self.mul(b, b)),
                     self.scale(self.mul(a, b), -1))
        e = self.mul(self.mul(a, b), self.add(a, self.scale(b, -1)))
        return s, self.mul(e, e)


def quadratic_check(p, d):
    started = time.monotonic()
    field = QuadraticField(p, d)
    if p in (3, 11):
        raise ValueError('outside theorem scope')
    pair_fibers, key_fibers = defaultdict(list), defaultdict(list)
    for a in range(field.q):
        for b in range(field.q):
            x, y = [tuple(field.add(field.scale(a, u), field.scale(b, v))
                          for u, v in points) for points in (PX, PY)]
            support = len(set(x)) == len(set(y)) == 6
            exclusion = all(field.add(field.scale(a, u), field.scale(b, v))
                            for u, v in NORMALS)
            assert support == exclusion
            if not support:
                continue
            xx, yy = field.canonical(x), field.canonical(y)
            assert xx != yy
            pair_fibers[tuple(sorted((xx, yy)))].append((a, b))
            key_fibers[field.key(a, b)].append((a, b))
    assert {tuple(v) for v in pair_fibers.values()} == {
        tuple(v) for v in key_fibers.values()}
    assert set(map(len, pair_fibers.values())) == {12}
    vertices = Counter(endpoint for pair in pair_fibers for endpoint in pair)
    if p != 31:
        assert set(vertices.values()) == {1}
    return {'p': p, 'q': field.q, 'nonresidue': d,
            'group': f'additive (Z/{p}Z)^2',
            'equivalence': 'independent translations/inversions, no scalar quotient',
            'pairs': len(pair_fibers), 'all_pair_key_fibers_equal': True,
            'fiber_histogram': dict(Counter(map(len, pair_fibers.values()))),
            'vertex_degree_histogram': dict(Counter(vertices.values())),
            'seconds': round(time.monotonic()-started, 6)}


def small_prime_census_audit():
    """Replay inherited full payloads; do not re-enumerate missing classes.

    Completeness is inherited from the two original enumerators. This audit
    independently checks every displayed class, ICV, family/edge count and
    exception coefficient, retaining source hashes and explicit trust scope.
    """
    records = []
    for p in (p for p in range(7, 132) if prime(p)):
        candidates = [ROOT/f'results/2026-09-30-six-census/n{p}.json',
                      ROOT/f'results/2026-09-30-six-large-census/n{p}.json']
        path = next(path for path in candidates if path.exists())
        raw = path.read_bytes()
        census = json.loads(raw)
        assert census['methods'] in (
            ['anchored-points-bitcorrelation', 'C-positive-gaps-pairdistances'],
            ['C-gap-pairs', 'C-point-correlations'])
        signatures, classes = set(), set()
        histogram = Counter()
        for family in census['families']:
            signature = tuple(family['icv'])
            assert signature not in signatures
            signatures.add(signature)
            assert len(family['members']) >= 2
            histogram[len(family['members'])] += 1
            for member in family['members']:
                points = tuple(member)
                assert len(points) == len(set(points)) == 6
                assert all(0 <= z < p for z in points)
                anchored = min(tuple(sorted(sign*(z-anchor) % p for z in points))
                               for sign in (1, -1) for anchor in points)
                assert points == anchored and points not in classes
                classes.add(points)
                distances = Counter(min((x-y) % p, (y-x) % p)
                                    for x, y in combinations(points, 2))
                assert tuple(distances[h] for h in range(1, p//2+1)) == signature
        edges = sum(k*(k-1)//2*count for k, count in histogram.items())
        families = sum(histogram.values())
        assert edges == census['summary']['pairs']
        assert families == census['summary']['families']
        base = (p-1)*(p-11)//12 if p >= 13 else 0
        edge_extra = {17: 8, 19: 9, 23: 11, 31: 20}.get(p, 0)
        family_extra = {17: 8, 19: 9, 23: 11, 31: 11}.get(p, 0)
        assert edges == base+edge_extra and families == base+family_extra
        assert dict(histogram) == ({2: 60, 5: 1} if p == 31 else (
                                  {2: families} if families else {}))
        records.append({'p': p, 'pairs': edges, 'families': families,
                        'family_size_histogram': dict(sorted(histogram.items())),
                        'pair_correction': edge_extra, 'family_correction': family_extra,
                        'path': str(path.relative_to(ROOT)),
                        'sha256': hashlib.sha256(raw).hexdigest(),
                        'inherited_methods': census['methods'],
                        'inherited_source_hashes': census.get('source_sha256')})
    return {'scope': 'inherited complete two-method censuses, not a new enumeration',
            'all_displayed_classes_icvs_and_counts_verified': True, 'records': records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--direct', type=Path, default=ROOT/'results/2026-09-30-six-prime-count')
    parser.add_argument('--out', type=Path, default=ROOT/'results/2026-09-30-six-prime-invariants')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    output = {'status': 'COMPUTED', 'symbolic': symbolic_checks(), 'primes': [],
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    paths = sorted(args.direct.glob('p[0-9]*.json'), key=lambda p: int(p.stem[1:]))
    if not paths:
        raise ValueError('no direct certificates found')
    for path in paths:
        report = replay_direct(path)
        output['primes'].append(report)
        (args.out/f'{path.stem}.json').write_text(json.dumps(report, indent=2)+'\n')
        print(json.dumps(report), flush=True)
    output['quadratic_fields'] = [quadratic_check(p, d) for p, d in ((5, 2), (7, 3), (13, 2))]
    output['small_prime_census'] = small_prime_census_audit()
    (args.out/'summary.json').write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps(output['quadratic_fields']), flush=True)


if __name__ == '__main__':
    main()
