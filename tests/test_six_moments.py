"""Independent direct-root controls for the exploratory Newton elimination.

These tests verify exact identities, not completeness of the moment method.
Elementary symmetric functions and moments are constructed directly from
roots, avoiding the production recurrence. Repeated roots are retained.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import prod
from pathlib import Path
import json,sys,time
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from six_moments import power_sums,difference_moment,derive


def elementary(roots):
    return [sum(prod(subset) for subset in combinations(roots,j))
            for j in range(1,len(roots)+1)]


def centered(roots):
    mean=sum(roots)/Fraction(len(roots))
    return [Fraction(x)-mean for x in roots]


def bloom(p,q):
    return ([0,p,q-2*p,2*q-2*p,2*q,3*q-p],
            [0,p,q+2*p,2*q-p,2*q+p,3*q-p])


def main():
    start=time.monotonic()
    fixtures=[(0,),(-3,2),(1,1,1),(-7,-1,0,2),
              (-9,-3,-1,0,4,8),(0,1,3,3,7,8),
              (Fraction(-7,3),Fraction(1,2),0,Fraction(2,3),5,5)]
    checks=0
    for roots in fixtures:
        roots=list(map(Fraction,roots));sums=power_sums(elementary(roots),30)
        for j in range(31):
            assert sums[j]==sum(x**j for x in roots),(roots,j)
            assert difference_moment(sums,j)==sum((x-y)**j for x in roots for y in roots),(roots,j)
            checks+=2
    # Symbolic two-root checks make the j>k recurrence branch observable.
    x,y=sp.symbols('x y');sums=power_sums([x+y,x*y],9)
    for j in range(10):assert sp.expand(sums[j]-x**j-y**j)==0

    result=derive(20)
    # Compare regenerated exact expressions with the preserved exploration.
    saved=json.loads((ROOT/'results/2026-09-30-six-moments-explore.json').read_text())
    for field,value in result.items():
        if isinstance(value,dict):
            assert {str(k) for k in value}==set(saved[field])
            for k,expression in value.items():assert sp.expand(expression-sp.sympify(saved[field][str(k)]))==0
        else:assert sp.expand(value-sp.sympify(saved[field]))==0

    s,t,u,v,w,T,V,W,d=sp.symbols('s t u v w T V W d')
    parameters=[(1,6),(2,7),(3,-2),(1,3),(1,2),(0,1),
                (Fraction(1,2),Fraction(5,3))]
    nontrivial_d=0;repeated_support=0
    for p,q in parameters:
        a,b=bloom(p,q)
        assert Counter(x-y for x in a for y in a)==Counter(x-y for x in b for y in b)
        repeated_support+=len(set(a))<6 or len(set(b))<6
        ea,eb=elementary(centered(a)),elementary(centered(b))
        assert ea[0]==eb[0]==0 and ea[1]==eb[1] and ea[3]==eb[3]
        delta=eb[2]**2-ea[2]**2;nontrivial_d+=bool(delta)
        substitution=dict(zip((s,t,u,v,w),ea[1:]))
        substitution.update({T:eb[2],V:eb[4],W:eb[5],d:delta})
        assert eb[5]==ea[5]-2*delta
        assert result['b'].subs(substitution)==eb[2]*eb[4]
        assert result['c'].subs(substitution)==eb[4]**2
        assert result['relation'].subs(substitution)==0
        for eq in result['equations'].values():assert eq.subs(substitution)==0
        for eq in result['reduced'].values():assert eq.subs(substitution)==0
    assert nontrivial_d and repeated_support
    # Negative control: unchanged cardinality alone does not equalize moments.
    a=(0,1,4,10,12,17);wrong=(0,1,8,11,13,18)
    pa=power_sums(elementary(a),2);pb=power_sums(elementary(wrong),2)
    assert difference_moment(pa,2)!=difference_moment(pb,2)
    print(dict(status='PASS exact exploratory identity controls; no completeness claim',
               direct_root_checks=checks,symbolic_checks=10,bloom_controls=len(parameters),
               repeated_support_controls=repeated_support,nonzero_elimination_parameter=nontrivial_d,
               seconds=round(time.monotonic()-start,3)))

if __name__=='__main__':main()
