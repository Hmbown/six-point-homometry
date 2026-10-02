"""Symbolic certificates for the three infinite cyclic six-note families.

Verify M*Va=0 and the parameter-independent divisibility obstruction for
every saved matching, without using production Smith computations.
"""
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys

from sympy import Matrix

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from homometry import dihedral_canon
from six_explore import canon
from six_shadow import anchored_vector, matching_matrices
from six_shell import parametric_families


def multiply(matrix,vector):
    return [sum(x*y for x,y in zip(row,vector)) for row in matrix]


def matrix_tuple(m):
    return tuple(tuple(int(x) for x in row) for row in m.tolist())


def distances(s,n):
    return Counter(min((y-x)%n,(x-y)%n) for x,y in combinations(s,2))


def test_symbolic_all_matchings():
    outputs=[]
    for typ in (1,2,3):
        name='n18.json' if typ==1 else f'shell_type{typ}_n18.json'
        d=json.loads((ROOT/'results/2026-09-30-six-shadow'/name).read_text())
        x,y=parametric_families(3,1)[typ-1]
        v3=anchored_vector(x,y,18)
        x4,y4=parametric_families(4,1)[typ-1]
        v4=anchored_vector(x4,y4,24)
        vm=tuple(z-w for z,w in zip(v4,v3))
        va=tuple(z-3*w for z,w in zip(v3,vm))
        seen=set()
        for record in d['certificates']:
            m=record['matrix']
            assert multiply(m,va)==[0]*15
            mm=multiply(m,vm)
            assert all(x%6==0 for x in mm)
            c=record['smith']['row_combination']
            row=[sum(c[i]*m[i][j] for i in range(15)) for j in range(10)]
            assert all(x%6==0 for x in row)
            right=-sum(c[i]*mm[i] for i in range(15))
            assert right%6==0 and (right//6)%6!=0
            assert right//6==record['smith']['value']
            seen.add(matrix_tuple(Matrix(m)))
        expected={matrix_tuple(m) for m,_ in matching_matrices(x,y,18)}
        assert seen==expected and len(seen)==len(d['certificates'])==384
        for mm,aa in ((4,1),(5,2),(10,4),(100,49),(100003,50001)):
            xx,yy=parametric_families(mm,aa)[typ-1]
            assert distances(xx,6*mm)==distances(yy,6*mm)
            assert canon(xx,6*mm)!=canon(yy,6*mm)
            assert {matrix_tuple(m) for m,_ in matching_matrices(xx,yy,6*mm)}==expected
        outputs.append(dict(type=typ,matchings=384,va=va,vm=vm,
                            symbolic_rejections=384,large_parameter_max_n=600018))
    return outputs


def test_inventory_coverage():
    """Check the explained menu-gap edges using the immutable T/I reference.

    This does not recertify discovery of the strict menu; it checks the new
    parametric templates against gap labels independently audited in the
    saved review. The templates need not be distinct under unit action.
    """
    results=[]
    for n in range(12,61,6):
        payload=json.loads((ROOT/f'results/2026-09-30-six-shell/n{n}.json').read_text())
        gap_edges={tuple(sorted((tuple(row['x']),tuple(row['y']))))
                   for row in payload['pairs'] if row['menu_gap']}
        generated=set()
        for a in range(1,(n//6+1)//2):
            for x,y in parametric_families(n//6,a):
                generated.add(tuple(sorted((tuple(dihedral_canon(x,n)),
                                             tuple(dihedral_canon(y,n))))))
        assert generated==gap_edges, (n,len(generated),len(gap_edges))
        results.append(dict(n=n,parametric_menu_gap_edges=len(generated)))
    return results


if __name__=='__main__':
    checks=test_symbolic_all_matchings()
    coverage=test_inventory_coverage()
    (ROOT/'results/2026-09-30-six-parametric-check.json').write_text(json.dumps(dict(
        status='COMPUTED; arbitrary-parameter proof uses symbolic certificates, not finite range',
        checks=checks,coverage=coverage),sort_keys=True)+'\n')
    for row in checks:print('PASS',row,flush=True)
    print('PASS inventory coverage',coverage,flush=True)
