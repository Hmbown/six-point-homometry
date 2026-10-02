"""Domain-boundary witness: CRT sign changes defeat field moment separation."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from homometry import dihedral_canon, icv


def main():
    n, t = 221, 118
    assert t % 13 == 1 and t % 17 == 16 and t*t % n == 1
    assert t not in (1, n-1)
    records = json.loads((ROOT/'results/2026-09-30-six-prime-invariants/'
                         'composite-obstruction.json').read_text())['records']
    pairs, keys = [], []
    for record in records:
        a, b = record['parameter']
        x = tuple(sorted({0, a, (b-2*a) % n, (2*b-2*a) % n, 2*b % n, (3*b-a) % n}))
        y = tuple(sorted({0, a, (b+2*a) % n, (2*b-a) % n, (2*b+a) % n, (3*b-a) % n}))
        assert len(x) == len(y) == 6 and list(x) == record['X'] and list(y) == record['Y']
        pair = tuple(sorted((dihedral_canon(x, n), dihedral_canon(y, n))))
        assert pair[0] != pair[1] and icv(x, n) == icv(y, n)
        assert [list(endpoint) for endpoint in pair] == record['canonical_pair']
        key = ((a*a-a*b+b*b) % n, (a*b*(a-b))**2 % n)
        assert list(key) == record['invariants']
        pairs.append(pair)
        keys.append(key)
    assert keys[0] == keys[1] == (13, 144) and pairs[0] != pairs[1]
    assert (t*records[0]['parameter'][0] % n,
            t*records[0]['parameter'][1] % n) == tuple(records[1]['parameter'])
    maxima = []
    for record in records:
        maxima.append({max([b-a for a, b in zip(points, points[1:])]+
                           [points[0]+n-points[-1]]) for points in (record['X'], record['Y'])})
    assert maxima == [{210}, {73, 75}]
    # Every even centered power and square of an odd centered power survives
    # this CRT multiplier, but the actual pair classes above differ.
    for x, y in zip((records[0]['X'], records[0]['Y']),
                    (records[1]['X'], records[1]['Y'])):
        cx = [(6*z-sum(x)) % n for z in x]
        cy = [(6*z-sum(y)) % n for z in y]
        for exponent in range(2, 21):
            mx, my = sum(pow(z, exponent, n) for z in cx) % n, sum(
                pow(z, exponent, n) for z in cy) % n
            assert (mx if exponent % 2 == 0 else mx*mx % n) == (
                    my if exponent % 2 == 0 else my*my % n)
    print('PASS CRT domain-boundary certificate, independent classes/ICVs/gaps/moments')


if __name__ == '__main__':
    main()
