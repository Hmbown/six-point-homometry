"""Exploratory exact circle SMT with learned signed-matching affine planes.

A SAT model is a discovery point, never a completeness claim. UNSAT is only
meaningful together with a reviewed encoding and independently verified plane
certificates. Each learned plane Mv=k is globally homometric on the circle.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from functools import reduce
from itertools import combinations
import hashlib,json,math,subprocess,time
from pathlib import Path
import re
from sympy import Matrix
from six_shadow import matching_matrices, matching_count

ROOT=Path(__file__).resolve().parents[1]
VARS=[f'{letter}{i}' for letter in 'ab' for i in range(1,6)]

def num(x):
    x=F(x)
    if x<0:return f'(- {num(-x)})'
    return str(x.numerator) if x.denominator==1 else f'(/ {x.numerator} {x.denominator})'
def land(xs):return '(and '+' '.join(xs)+')'
def lor(xs):return '(or '+' '.join(xs)+')'
def lex(a,b,strict=False):
    rows=[land([f'(= {a[j]} {b[j]})' for j in range(i)]+[f'(< {a[i]} {b[i]})']) for i in range(len(a))]
    if not strict:rows.append(land([f'(= {x} {y})' for x,y in zip(a,b)]))
    return lor(rows)
def linear(row):
    terms=[v if c==1 else f'(* {num(c)} {v})' for c,v in zip(row,VARS) if c]
    return '0' if not terms else terms[0] if len(terms)==1 else '(+ '+' '.join(terms)+')'

def encode(timeout=10, mode="folded"):
    if mode not in ("folded", "direct"):raise ValueError(mode)
    lines=['(set-logic QF_LRA)','(set-option :produce-models true)',f'(set-option :timeout {timeout*1000})']
    lines += [f'(declare-fun {v} () Real)' for v in VARS]
    sets=[['0']+VARS[:5],['0']+VARS[5:]];gaps=[]
    for points in sets:
        lines += [f'(assert (< {x} {y}))' for x,y in zip(points,points[1:])]+[f'(assert (< {points[-1]} 1))']
        gap=[f'(- {points[j+1]} {points[j]})' for j in range(5)]+[f'(- 1 {points[-1]})'];gaps.append(gap)
        for order in [gap,list(reversed(gap))]:
            for shift in range(6):
                other=order[shift:]+order[:shift]
                if other!=gap:lines.append('(assert '+lex(gap,other)+')')
    lines.append('(assert '+lex(gaps[0],gaps[1],True)+')')
    for label,points in zip('ab',sets):
        for i,(j,k) in enumerate(combinations(range(6),2)):
            delta=f'(- {points[k]} {points[j]})'
            expression=f'(ite (<= {delta} (/ 1 2)) {delta} (- 1 {delta}))' if mode=='folded' else delta
            lines.append(f'(define-fun {label}d{i} () Real {expression})')
    da=[f'ad{i}' for i in range(15)];db=[f'bd{i}' for i in range(15)]
    for d in da:
        def condition(x):return f'(= {d} {x})' if mode=='folded' else f'(or (= {d} {x}) (= (+ {d} {x}) 1))'
        lhs='(+ '+' '.join(f'(ite {condition(x)} 1 0)' for x in da)+')'
        rhs='(+ '+' '.join(f'(ite {condition(x)} 1 0)' for x in db)+')'
        lines.append(f'(assert (= {lhs} {rhs}))')
    return '\n'.join(lines)+'\n'

def rational(value):
    if isinstance(value,str):return F(value)
    if value[0]=='-':return -rational(value[1])
    if value[0]=='/':return rational(value[1])/rational(value[2])
    raise ValueError(value)
def parse_sexpr(text):
    tokens=re.findall(r'\(|\)|[^\s()]+',text);it=iter(tokens)
    def item(token):
        if token!='(':return token
        out=[]
        for t in it:
            if t==')':return out
            out.append(item(t))
        raise ValueError('unterminated')
    return item(next(it))

def plane(m,vector):
    k=m*Matrix(vector)
    assert all(x.q==1 for x in k)
    augmented=m.row_join(k);rref,_=augmented.rref()
    rows=[]
    for r in rref.tolist():
        if not any(r):continue
        den=math.lcm(*(int(x.q) for x in r))
        row=tuple(int(x*den) for x in r);g=math.gcd(*row)
        row=tuple(x//g for x in row)
        if next(x for x in row if x)<0:row=tuple(-x for x in row)
        rows.append(row)
    return tuple(rows)
def exclude(rows):
    return '(assert (not '+land([f'(= {linear(r[:10])} {num(r[10])})' for r in rows])+'))'

def first_planes(nmin,nmax):
    found={}
    for n in range(nmin,nmax+1):
        data=json.loads((ROOT/f'results/2026-09-30-six-census/n{n}.json').read_text())
        for family in data['families']:
            for a,b in combinations(family['members'],2):
                # Existing canonical point tuples equal lex-min gap tuples.
                m,labels=next(matching_matrices(a,b,n))
                v=[F(x,n) for x in a[1:]+b[1:]]
                rows=plane(m,v)
                found.setdefault(rows,dict(n=n,a=a,b=b,labels=labels,rank=len(rows)))
    return found

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=ROOT/'results/2026-09-30-six-templates-circle')
    p.add_argument('--preload',type=int,default=24);p.add_argument('--iterations',type=int,default=10);p.add_argument('--timeout',type=int,default=15)
    p.add_argument('--mode',choices=['folded','direct'],default='folded')
    p.add_argument('--matching-cap',type=int,default=100);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    started=time.monotonic();known=first_planes(12,a.preload) if a.preload>=12 else {}
    print('preloaded',len(known),'seconds',round(time.monotonic()-started,2),flush=True)
    source=encode(a.timeout,a.mode)+'\n'.join(exclude(rows) for rows in known)+'\n'
    (a.out/'initial.smt2').write_text(source+'(check-sat)\n')
    process=subprocess.Popen(['z3','-in','-smt2'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1)
    process.stdin.write(source);process.stdin.flush();models=[]
    for iteration in range(a.iterations):
        tick=time.monotonic();process.stdin.write('(check-sat)\n');process.stdin.flush()
        status=process.stdout.readline().strip()
        print('iteration',iteration,status,'seconds',round(time.monotonic()-tick,2),flush=True)
        if status!='sat':break
        process.stdin.write('(get-value ('+' '.join(VARS)+'))\n');process.stdin.flush()
        text=''
        while not text or text.count('(')>text.count(')'):text+=process.stdout.readline()
        values=dict(parse_sexpr(text));v=[rational(values[x]) for x in VARS];n=math.lcm(*(x.denominator for x in v))
        aa=[0]+[int(n*x) for x in v[:5]];bb=[0]+[int(n*x) for x in v[5:]]
        new=[];count=matching_count(aa,bb,n)
        for index,(m,labels) in enumerate(matching_matrices(aa,bb,n)):
            if index>=a.matching_cap:break
            rows=plane(m,v)
            if rows not in known:
                known[rows]=dict(n=n,a=aa,b=bb,labels=labels,rank=len(rows))
                new.append(rows)
        model=dict(n=n,a=aa,b=bb,matchings=count,learned=len(new),min_rank=min(map(len,new)),iteration=iteration)
        models.append(model);print(model,flush=True)
        for rows in new:process.stdin.write(exclude(rows)+'\n')
        process.stdin.flush()
        (a.out/'models.json').write_text(json.dumps(models,indent=2)+'\n')
    process.stdin.write('(exit)\n');process.stdin.flush();process.wait(timeout=5)
    all_planes=[dict(rows=rows,**cert) for rows,cert in known.items()]
    (a.out/'planes.json').write_text(json.dumps(all_planes)+'\n')
    final=encode(a.timeout,a.mode)+'\n'.join(exclude(rows) for rows in known)+'\n(check-sat)\n'
    (a.out/'final.smt2').write_text(final)
    report=dict(status=status,last_query_status=status,final_formula_checked=(status!='sat'),mode=a.mode,preload_max=a.preload,plane_count=len(known),models=models,seconds=time.monotonic()-started,
                warning='Exploratory solver result; no reviewed classification conclusion.',source_sha256=hashlib.sha256(final.encode()).hexdigest())
    (a.out/'summary.json').write_text(json.dumps(report,indent=2)+'\n');print(report,flush=True)

if __name__=='__main__':main()
