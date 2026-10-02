"""Independent arrangement/CRT counts and exact direct-fiber bindings.

No point canonicalizer or direct enumerator is imported. Inclusion-exclusion
counts odd-modulus support parameters by exact two-column Smith factors.
For the proved regular CRT domain, classify by twelve formal parameter maps.
The full-domain fiber assertion is a checked observation, not a theorem here.
"""
from collections import Counter
from itertools import combinations
from math import gcd
from pathlib import Path
import argparse
import gzip
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parents[1]
LINES = ((1, 0), (0, 1), (-1, 1), (1, 1), (-2, 1), (2, 1),
         (-3, 1), (-1, 2), (1, 2), (-3, 2), (-1, 3), (-2, 3))


def factors(n):
    if not isinstance(n, int) or isinstance(n, bool) or n < 2:
        raise ValueError('integer modulus at least two required')
    out, p = [], 2
    while p*p <= n:
        k = 0
        while n % p == 0:
            n //= p
            k += 1
        if k:
            out.append((p, k))
        p += 1
    if n > 1:
        out.append((n, 1))
    return out


def arrangement_weights():
    # Every normal is primitive. For rank two, first Smith factor is one
    # and second is the gcd of all 2x2 minors. Its kernel has gcd(n,d) points.
    out = Counter()
    for size in range(2, len(LINES)+1):
        for subset in combinations(LINES, size):
            determinant_gcd = 0
            for (a, b), (c, d) in combinations(subset, 2):
                determinant_gcd = gcd(determinant_gcd, abs(a*d-b*c))
            assert determinant_gcd
            out[determinant_gcd] += (-1)**size
    return dict(sorted(out.items()))


def support_count(n):
    if n < 3 or n % 2 == 0:
        raise ValueError('primitive collision normals are valid here only at odd moduli')
    return n*n-12*n+sum(weight*gcd(n, d) for d, weight in arrangement_weights().items())


def support_admissible(a, b, n):
    return all((u*a+v*b) % n for u, v in LINES)


def orbit(a, b, n):
    # Independent root-triple permutation representation, not R/T matrices.
    from itertools import permutations
    triple = (a, -b, b-a)
    return {(sign*x % n)*n+(-sign*y) % n
            for x, y, z in permutations(triple) for sign in (1, -1)}


def faithful(a, b, prime_factors):
    return all(support_admissible(a, b, p) for p, k in prime_factors)


def regular(a, b, n, prime_factors):
    e, d = a*b*(a-b), (a+b)*(2*a-b)*(a-2*b)
    return gcd(e*d, n) == 1 and all(support_admissible(a, b, p**k)
                                   for p, k in prime_factors)


def local_supports(a, b, prime_factors):
    return all(support_admissible(a, b, p**k) for p, k in prime_factors)


def local_support_parameter_count(n):
    ff = factors(n)
    if any(p < 13 for p, k in ff):
        raise ValueError('local support theorem requires prime divisors at least13')
    result = 1
    for p, k in ff:
        result *= (p**k-1)*(p**k-11)
    return result


def regular_parameter_count(n):
    ff = factors(n)
    if any(p < 13 for p, k in ff):
        raise ValueError('the regular CRT theorem requires all prime divisors at least13')
    result = 1
    for p, k in ff:
        result *= p**(2*k-2)*(p-1)*(p-5)-6*p**(k-1)*(p-1)
    return result


def faithful_parameter_count(n):
    ff = factors(n)
    if any(p < 13 for p, k in ff):
        raise ValueError('the faithful theorem requires all prime divisors at least13')
    result = 1
    for p, k in ff:
        result *= p**(2*k-2)*(p-1)*(p-11)
    return result


def audit(path):
    start = time.monotonic()
    path = path.resolve()
    raw = path.read_bytes()
    result = json.loads(gzip.decompress(raw))
    n = result['summary']['n']
    ff = factors(n)
    if n % 2 == 0:
        raise ValueError('this arithmetic replay concerns odd moduli')
    seen = bytearray(n*n)
    histogram = Counter()
    counts = Counter()
    for category, codes in result['excluded_parameter_codes'].items():
        for code in codes:
            assert 0 <= code < n*n and not seen[code]
            seen[code] = 1
            a, b = divmod(code, n)
            assert support_admissible(a, b, n) == (category != 'collision')
            counts[category] += 1
    for record in result['fibers']:
        codes = record['parameter_codes']
        assert codes
        a, b = divmod(codes[0], n)
        assert set(codes) == orbit(a, b, n)
        histogram[len(codes)] += 1
        for code in codes:
            assert 0 <= code < n*n and not seen[code]
            seen[code] = 1
            x, y = divmod(code, n)
            assert support_admissible(x, y, n)
        counts['admissible'] += len(codes)
        if faithful(a, b, ff):
            counts['faithful_pairs'] += 1
            counts['faithful_parameters'] += len(codes)
        if regular(a, b, n, ff):
            counts['regular_pairs'] += 1
            counts['regular_parameters'] += len(codes)
        if local_supports(a, b, ff):
            counts['local_support_pairs'] += 1
            counts['local_support_parameters'] += len(codes)
    assert all(seen)
    assert counts['admissible']+counts['congruent'] == support_count(n)
    assert counts['admissible'] == result['summary']['admissible_parameters']
    assert sum(histogram.values()) == result['summary']['pairs']
    assert counts['faithful_pairs'] == result['summary']['unit_separated_pairs']
    if all(p >= 13 for p, k in ff):
        assert counts['regular_parameters'] == regular_parameter_count(n)
        assert counts['faithful_parameters'] == faithful_parameter_count(n)
        assert counts['local_support_parameters'] == local_support_parameter_count(n)
        assert set(histogram) == {12}
        assert counts['regular_parameters'] == 12*counts['regular_pairs']
        assert counts['faithful_parameters'] == 12*counts['faithful_pairs']
        assert counts['local_support_parameters'] == 12*counts['local_support_pairs']
    return {'n': n, 'factors': ff, 'counts': dict(counts),
            'fiber_histogram': dict(histogram), 'all_parameter_locations_verified': True,
            'all_direct_fibers_equal_root_permutation_orbits': True,
            'arrangement_support_count': support_count(n),
            'regular_theorem_applies': all(p >= 13 for p, k in ff),
            'full_fiber_status': 'COMPUTED; global full-domain theorem not assumed',
            'direct_path': str(path.relative_to(ROOT)),
            'direct_sha256': hashlib.sha256(raw).hexdigest(),
            'seconds': round(time.monotonic()-start, 6)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--direct', type=Path, default=ROOT/'results/2026-09-30-six-composite-count')
    parser.add_argument('--out', type=Path, default=ROOT/'results/2026-09-30-six-composite-arithmetic')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    output = {'status': 'COMPUTED', 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'arrangement_smith_weights': arrangement_weights(), 'moduli': []}
    for path in sorted(args.direct.glob('n*.json.gz'), key=lambda p: int(p.name.split('.')[0][1:])):
        report = audit(path)
        output['moduli'].append(report)
        (args.out/f'n{report["n"]}.json').write_text(json.dumps(report, indent=2)+'\n')
        print(json.dumps(report), flush=True)
    if not output['moduli']:
        raise ValueError('no direct certificates found')
    (args.out/'summary.json').write_text(json.dumps(output, indent=2)+'\n')


if __name__ == '__main__':
    main()
