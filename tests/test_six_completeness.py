"""Independent arithmetic checks for the six-note cylinder reduction."""
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from sympy import Matrix
from homometry import icv, dihedral_canon
from six_completeness import cylinder_certificate, graph_minor_bound, overlap_energy


def bareiss(matrix):
    a = [list(row) for row in matrix]
    sign, previous = 1, 1
    for k in range(len(a)-1):
        pivot = next((i for i in range(k,len(a)) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k],a[pivot] = a[pivot],a[k]
            sign = -sign
        value = a[k][k]
        for i in range(k+1,len(a)):
            for j in range(k+1,len(a)):
                numerator = value*a[i][j] - a[i][k]*a[k][j]
                assert numerator % previous == 0
                a[i][j] = numerator // previous
            a[i][k] = 0
        previous = value
    return sign*a[-1][-1]


def test_graph_bound():
    # Independent of production's tree subsets: Kirchhoff's determinant.
    edges = list(combinations(range(6),2))
    hist = Counter()
    for chosen in combinations(edges,10):
        lap = [[0]*6 for _ in range(6)]
        for a,b in chosen:
            lap[a][a] += 1
            lap[b][b] += 1
            lap[a][b] -= 1
            lap[b][a] -= 1
        hist[bareiss([row[:5] for row in lap[:5]])] += 1
    actual = graph_minor_bound()
    assert dict(hist) == actual['histogram']
    assert sum(hist.values()) == 3003
    assert max(hist) == 135 and hist[135] == 60
    return dict(actual, independent_method='Kirchhoff cofactor and exact Bareiss determinant')


def cylinder_differences(points,q):
    return Counter((x-u,(t-v)%q) for x,t in points for u,v in points)


def check_certificate(c):
    n,q = c['n'],c['q']
    m,d,u,v = map(Matrix, [c['matrix'],c['smith_d'],c['smith_u'],c['smith_v']])
    assert u*m*v == d
    assert abs(int(u.det())) == abs(int(v.det())) == 1
    assert n % q == 0 and 1 <= q <= 135
    assert c['torsion_order'] % q == 0
    aa,bb = c['cylinder_a'],c['cylinder_b']
    assert len(set(map(tuple,aa))) == len(set(map(tuple,bb))) == 6
    assert cylinder_differences(aa,q) == cylinder_differences(bb,q)
    projected_a = tuple((x+n//q*t)%n for x,t in aa)
    projected_b = tuple((x+n//q*t)%n for x,t in bb)
    assert projected_a == tuple(c['a']) and projected_b == tuple(c['b'])
    assert icv(projected_a,n) == icv(projected_b,n)
    assert dihedral_canon(projected_a,n) != dihedral_canon(projected_b,n)


def test_cylinders():
    cases = [
        (18,(0,1,4,6,10,13),(0,1,4,7,9,13)),
        (21,(0,1,3,7,10,15),(0,1,4,7,14,16)),
        (37,(0,1,4,10,12,17),(0,1,8,11,13,17)),
    ]
    reports=[]
    for n,a,b in cases:
        for index in ((0,) if n==37 else (0,1,3)):
            c=cylinder_certificate(a,b,n,index)
            check_certificate(c)
            reports.append(dict(n=n,q=c['q'],rank=c['rank'],index=index))
    # Test anchoring and ordinary inflation without relying on normal forms.
    for scale in (2,7,1009):
        n=18*scale
        a=tuple((scale*x+5)%n for x in cases[0][1])
        b=tuple((scale*x+9)%n for x in cases[0][2])
        c=cylinder_certificate(a,b,n)
        check_certificate(c)
        reports.append(dict(n=n,q=c['q'],rank=c['rank'],translated=True))
    assert reports[0]['q']==6
    assert reports[3]['q']==21
    assert reports[6]['q']==1
    return reports


def test_overlap_reduction():
    hist=Counter(); energy_hist=Counter(); forced=0; total=0
    for n in range(12,61):
        families=json.loads((ROOT/f'results/2026-09-30-six-census/n{n}.json').read_text())['families']
        for family in families:
            for a,b in combinations(family['members'],2):
                r=overlap_energy(a,b,n)
                # Independent membership intersections over shifts/orientations.
                aset=set(a)
                overlaps=[len(aset & {(s*x+t)%n for x in b})
                          for s in (1,-1) for t in range(n)]
                assert max(overlaps)==r['max_ti_overlap']
                if r['forced_three_common_notes']:
                    assert r['max_translation_overlap']>=3
                    forced+=1
                else:
                    # Energy <=72 forces at most one repeated non-antipodal ICV bin,
                    # multiplicities <=2, and at most one antipodal pair.
                    iv=list(icv(a,n))
                    ordinary=iv[:-1] if n%2==0 else iv
                    assert max(ordinary,default=0)<=2
                    assert sum(c==2 for c in ordinary)<=1
                    if n%2==0:
                        assert iv[-1]<=1
                hist[max(overlaps)]+=1;energy_hist[r['energy']]+=1;total+=1
    assert total==32106
    assert hist=={3:3130,4:25197,5:3779}
    return dict(pairs=total,max_ti_overlap_histogram=dict(hist),
                energy_forced_three_common=forced,energy_histogram=dict(energy_hist),
                independent_overlap_method='all 2n rigid alignments by set intersection')


if __name__=='__main__':
    start=time.monotonic()
    result=dict(graph_bound=test_graph_bound(),cylinders=test_cylinders(),
                overlap=test_overlap_reduction())
    result['seconds']=round(time.monotonic()-start,3)
    result['status']='COMPUTED: independent exact checks passed; mathematical review pending'
    dest=ROOT/'results/2026-09-30-six-completeness-tests.json'
    dest.write_text(json.dumps(result,sort_keys=True)+'\n')
    print('PASS graph determinant bound, cylinder certificates, overlap reduction')
    print(result['overlap'])
    print('seconds',result['seconds'])
