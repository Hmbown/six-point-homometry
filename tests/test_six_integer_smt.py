"""Non-vacuity and exact formula checks for the integer completeness reduction."""
import sys,subprocess,json
from fractions import Fraction as F
from itertools import combinations
from collections import Counter
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from six_integer_smt import X,Y,NORMAL_FORMS,val,bloom_templates,encode
from homometry import icv,dihedral_canon

def canon(v):
    v=sorted(v);v=tuple(x-v[0] for x in v)
    return min(v,tuple(v[-1]-x for x in v[::-1]))
def oriented(v):
    v=sorted(v);v=tuple(F(x-v[0],v[-1]-v[0]) for x in v)
    return v if v[-2]>=1-v[1] else tuple(1-x for x in v[::-1])
def member(a,b):
    z=a[1:]+b[1:]
    for pair in bloom_templates()[0]:
        coeffs=pair[0][1:]+pair[1][1:]
        i,j=next((i,j) for i,j in combinations(range(10),2) if coeffs[i][0]*coeffs[j][1]-coeffs[i][1]*coeffs[j][0])
        u,v=coeffs[i];w,t=coeffs[j];det=u*t-v*w
        p=(t*z[i]-v*z[j])/det;q=(-w*z[i]+u*z[j])/det
        if all(c*p+d*q==e for (c,d),e in zip(coeffs,z)):return True
    return False

def solver(text):
    p=subprocess.run(['z3','-in'],input=text,text=True,capture_output=True,check=True)
    return p.stdout.splitlines()[0]
def fixed(text,a,b):
    a,b=sorted((oriented(a),oriented(b)))
    vals=dict(zip(['a1','a2','a3','r'],a[1:5]));vals.update(zip(['b1','b2','b3'],b[1:4]))
    assert a[4]==b[4]
    eq=[]
    for k,v in vals.items():eq.append(f'(assert (= {k} (/ {v.numerator} {v.denominator})))')
    return text.replace('(check-sat)','\n'.join(eq)+'\n(check-sat)')

def test_chambers():
    templates,cuts=bloom_templates();assert len(templates)==96
    seen=0
    for p in range(-12,13):
      for q in range(-24,25):
        if p==0:continue
        a=tuple(sorted(c*p+d*q for c,d in X));b=tuple(sorted(c*p+d*q for c,d in Y))
        if len(set(a))<6 or len(set(b))<6:continue
        a=oriented(a);b=oriented(b)
        assert member(a,b);seen+=1
    print('PASS chamber coverage',seen)

def test_formal_soundness():
    for pair in NORMAL_FORMS:
        differences=[]
        for pts in pair:
            differences.append(Counter((b[0]-a[0],b[1]-a[1]) for a,b in combinations(pts,2)))
        assert differences[0]==differences[1]
    cases=0
    for p in range(1,9):
      for q in range(1,50):
        for index,pair in enumerate(NORMAL_FORMS):
          if not (q>3*p if index==0 else 3*p<2*q<4*p):continue
          a,b=[tuple(u*p+v*q for u,v in pts) for pts in pair]
          assert all(x<y for pts in (a,b) for x,y in zip(pts,pts[1:]))
          assert Counter(y-x for x,y in combinations(a,2))==Counter(y-x for x,y in combinations(b,2))
          n=2*max(a[-1],b[-1])+1
          assert icv(a,n)==icv(b,n)
          assert dihedral_canon(a,n)!=dihedral_canon(b,n)
          cases+=1
    print("PASS formal identity and immutable reference",cases)

def test_controls():
    text,_=encode(timeout_ms=15000,exclude_bloom=False)
    assert solver(text)=='sat'
    for a,b in [((0,1,4,10,12,17),(0,1,8,11,13,17)),((0,1,2,6,8,11),(0,1,6,7,9,11))]:
        assert solver(fixed(text,a,b))=='sat'
        excluding,_=encode(timeout_ms=15000)
        assert solver(fixed(excluding,a,b))=='unsat'
    no_distance,_=encode(timeout_ms=15000,homometry=False)
    assert solver(no_distance)=='sat'  # Bloom exclusion is not the whole domain.
    assert solver(fixed(text,(0,1,4,10,12,17),(0,1,8,10,13,17)))=='unsat'
    print('PASS satisfiable and unsatisfiable controls')

if __name__=='__main__':
    test_chambers();test_formal_soundness();test_controls()
