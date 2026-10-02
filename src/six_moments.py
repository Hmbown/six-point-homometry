"""Exact centered six-point moment elimination (exploratory, not a proof status).

All coefficients are rational integers. This script derives identities;
its interpretation in finite characteristic must list denominator factors.
"""
from math import comb
from pathlib import Path
import json
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]


def power_sums(e,maximum=30):
    k=len(e)
    p=[sp.Integer(k)]
    for j in range(1,maximum+1):
        value=0
        for i in range(1,min(j-1,k)+1):
            value+=(-1)**(i-1)*e[i-1]*p[j-i]
        if j<=k:
            value+=(-1)**(j-1)*j*e[j-1]
        else:
            value+=(-1)**(k-1)*e[k-1]*p[j-k] if k>=j else 0
        p.append(sp.expand(value))
    return p


def difference_moment(p,j):
    return sp.expand(sum((-1)**i*comb(j,i)*p[j-i]*p[i] for i in range(j+1)))


def derive(maximum=20):
    s,t,u,v,w,T,V,W,d=sp.symbols('s t u v w T V W d')
    p=power_sums([0,s,t,u,v,w],maximum)
    equations={j:sp.factor(difference_moment(p,j).xreplace({t:T,v:V,w:W})-
                           difference_moment(p,j)) for j in range(6,maximum+1,2)}
    substitutions={W:w-2*d,T**2:t**2+d}
    rows={}
    for j,eq in equations.items():
        poly=sp.Poly(sp.expand(eq.subs(W,w-2*d)),T,V)
        transformed=0
        for (i,k),coef in poly.terms():
            assert (i+k)%2==0
            term=coef*(t*t+d)**(i//2)
            if i%2:
                term*=sp.Symbol('b')
                k-=1
            term*=sp.Symbol('c')**(k//2)
            transformed+=term
        rows[j]=sp.factor(transformed)
    b,c=sp.symbols('b c')
    solve_b=sp.solve(rows[8],b)[0]
    solve_c=sp.solve(rows[10].subs(b,solve_b),c)[0]
    reduced={j:sp.factor(value.subs({b:solve_b,c:solve_c})) for j,value in rows.items()}
    relation=sp.factor(solve_b**2-(t*t+d)*solve_c)
    return dict(equations=equations,b=solve_b,c=solve_c,relation=relation,reduced=reduced)


if __name__=='__main__':
    result=derive()
    path=ROOT/'results/2026-09-30-six-moments-explore.json'
    payload={key:{str(k):str(v) for k,v in value.items()} if isinstance(value,dict) else str(value)
             for key,value in result.items()}
    path.write_text(json.dumps(payload,indent=2)+'\n')
    for key,value in payload.items():print(key,value,flush=True)
