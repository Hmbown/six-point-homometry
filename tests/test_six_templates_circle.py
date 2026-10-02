"""Controls for experimental rational-circle plane discovery, not completeness."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from homometry import icv,dihedral_canon
from six_templates_circle import encode,exclude,num,parse_sexpr,rational,VARS
import test_six_shadow_review as independent


def gap_canon(a,n):
    a=sorted(a);g=[a[i+1]-a[i] for i in range(5)]+[n+a[0]-a[-1]]
    return min(tuple(x[i:]+x[:i]) for x in [g,g[::-1]] for i in range(6))


def test_gap_canon():
    count=0
    for n in range(6,15):
        for a in combinations(range(n),6):
            c=dihedral_canon(a,n)
            expected=tuple([c[i+1]-c[i] for i in range(5)]+[n-c[-1]])
            assert gap_canon(a,n)==expected;count+=1
    print('PASS gap canonicalization',count)


def test_saved_planes_and_models():
    for directory in ('2026-09-30-six-templates-circle','2026-09-30-six-templates-circle-unseeded'):
        planes=json.loads((ROOT/'results'/directory/'planes.json').read_text())
        for cert in planes:
            q=cert['n'];a,b=cert['a'],cert['b'];vector=[F(x,q) for x in a[1:]+b[1:]]
            assert icv(a,q)==icv(b,q)
            m=independent.matching_matrix(cert['labels'])
            k=independent.matvec(m,vector);assert all(x.denominator==1 for x in k)
            augmented=[row+[int(rhs)] for row,rhs in zip(m,k)]
            rows=cert['rows']
            assert len(independent.rational_pivots(augmented))==len(rows)==cert['rank']
            assert len(independent.rational_pivots(augmented+rows))==len(rows)
            assert all(sum(c*x for c,x in zip(row[:10],vector))==row[10] for row in rows)
        print('PASS affine plane row spans',directory,len(planes))
    models=json.loads((ROOT/'results/2026-09-30-six-templates-circle-unseeded/models.json').read_text())
    for model in models:
        q=model['n'];a,b=model['a'],model['b']
        assert icv(a,q)==icv(b,q) and dihedral_canon(a,q)!=dihedral_canon(b,q)
        assert tuple(a)==dihedral_canon(a,q) and tuple(b)==dihedral_canon(b,q)
    print('PASS rational models',len(models))


def test_solver_controls():
    samples=[(12,[0,1,2,3,6,8],[0,1,2,4,6,7],'sat'),
             (12,[0,1,2,3,6,8],[0,1,2,3,6,8],'unsat'),
             (17,[0,1,2,3,8,12],[0,1,2,6,7,9],'sat')]
    count=0
    for mode in ['folded','direct']:
        for n,a,b,expected in samples:
            script=encode(10,mode)+'\n'.join(f'(assert (= {v} {num(F(x,n))}))' for v,x in zip(VARS,a[1:]+b[1:]))+'\n(check-sat)\n'
            r=subprocess.run(['z3','-in','-smt2'],input=script,text=True,capture_output=True,timeout=12)
            assert r.returncode==0 and r.stdout.strip()==expected,(r.stdout,r.stderr)
            count+=1
    parsed=parse_sexpr('((a1 (/ 1.0 7.0)) (a2 (- (/ 2 3))))')
    assert dict((k,rational(v)) for k,v in parsed)=={'a1':F(1,7),'a2':F(-2,3)}
    print('PASS exact solver controls',count)

if __name__=='__main__':
    test_gap_canon();test_saved_planes_and_models();test_solver_controls()
