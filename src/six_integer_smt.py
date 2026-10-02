"""Exact QF_LRA reduction for real six-point homometry (research certificate).

No numerical bounds on coordinates: scale common diameter to one.  The
finite Bloom plane union is derived from all ordering chambers of q/p.
External z3 is used only as an exact SMT solver; no default Python/NumPy.
"""
from __future__ import annotations
import argparse, gzip, hashlib, json, subprocess, time
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

X=((0,0),(1,0),(-2,1),(-2,2),(0,2),(-1,3))
Y=((0,0),(1,0),(2,1),(-1,2),(1,2),(-1,3))
NORMAL_FORMS=(
    (((0,0),(-2,1),(0,1),(-3,2),(-2,3),(-1,3)),
     ((0,0),(-1,1),(1,1),(1,2),(-2,3),(-1,3))),
    (((0,0),(-1,1),(1,1),(-2,3),(-1,3),(1,2)),
     ((0,0),(1,0),(-1,2),(2,1),(-1,3),(1,2))),
)

def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def val(a,r): return a[0]+a[1]*r

def bloom_templates():
    """Every p != 0 chamber; p<0 absorbed by simultaneous reflection."""
    cuts=sorted({F(b[0]-a[0],a[1]-b[1]) for pts in (X,Y)
                 for a,b in combinations(pts,2) if a[1]!=b[1]})
    samples=[cuts[0]-1,*cuts, cuts[-1]+1]
    samples.extend((a+b)/2 for a,b in zip(cuts,cuts[1:]))
    out=set()
    for r in samples:
        if any(len({val(a,r) for a in pts})<6 for pts in (X,Y)): continue
        pts=[]
        for seed in (X,Y):
            s=sorted(seed,key=lambda a: val(a,r)); pts.append(tuple(sub(a,s[0]) for a in s))
        for ra in (False,True):
            for rb in (False,True):
                pair=[]
                for s,rev in zip(pts,(ra,rb)):
                    pair.append(tuple(sub(s[-1],a) for a in s[::-1]) if rev else s)
                out.add(tuple(pair)); out.add(tuple(pair[::-1]))
    return sorted(out),cuts

def smt_num(n):
    if isinstance(n,F):
        if n.denominator!=1:return f'(/ {smt_num(n.numerator)} {n.denominator})'
        n=n.numerator
    return str(n) if n>=0 else f'(- {-n})'
def linear(coeffs,variables):
    terms=[]
    for c,v in zip(coeffs,variables):
        if c:terms.append(v if c==1 else f'(* {smt_num(c)} {v})')
    return '0' if not terms else terms[0] if len(terms)==1 else '(+ '+' '.join(terms)+')'
def smt_and(x): return '(and '+' '.join(x)+')'
def smt_or(x): return '(or '+' '.join(x)+')'

def plane_constraints(pair):
    coeffs=pair[0][1:]+pair[1][1:]
    var=['a1','a2','a3','r','1','b1','b2','b3','r','1']
    ij=next((i,j) for i,j in combinations(range(10),2)
            if coeffs[i][0]*coeffs[j][1]-coeffs[i][1]*coeffs[j][0])
    i,j=ij; a,b=coeffs[i]; c,d=coeffs[j]; det=a*d-b*c
    # det*p=d*z_i-b*z_j; det*q=-c*z_i+a*z_j
    out=[]
    for (u,v),w in zip(coeffs,var):
        out.append(f'(= {linear((det,),[w])} {linear((u*d-v*c,-u*b+v*a),(var[i],var[j]))})')
    return smt_and(out)

def encode(mode='count', timeout_ms=60000, exclude_bloom=True, proof=False, homometry=True, normal_forms=True):
    lines=(['(set-option :produce-proofs true)'] if proof else [])+['(set-logic QF_LRA)',f'(set-option :timeout {timeout_ms})']
    var=['a1','a2','a3','r','b1','b2','b3']
    lines += [f'(declare-fun {v} () Real)' for v in var]
    A=['0','a1','a2','a3','r','1'];B=['0','b1','b2','b3','r','1']
    for pts in (A,B):
        lines += [f'(assert (< {a} {b}))' for a,b in zip(pts,pts[1:])]
        lines += [f'(assert (>= r (- 1 {pts[1]})))']
    # Pair order removes swapping; reflection exclusion is separate.
    lex=[]
    for i in range(1,4):lex.append(smt_and([f'(= {A[j]} {B[j]})' for j in range(1,i)]+[f'(< {A[i]} {B[i]})']))
    lines += ['(assert '+smt_or(lex)+')']
    lines += ['(assert (not '+smt_and([f'(= {A[i]} (- 1 {B[5-i]}))' for i in range(1,5)])+'))']
    da=[f'(- {A[j]} {A[i]})' for i,j in combinations(range(6),2)]
    db=[f'(- {B[j]} {B[i]})' for i,j in combinations(range(6),2)]
    for lab,ds in [('a',da),('b',db)]:
        for i,d in enumerate(ds):lines += [f'(define-fun {lab}d{i} () Real {d})']
    da=[f'ad{i}' for i in range(15)]; db=[f'bd{i}' for i in range(15)]
    if not homometry:
        pass
    elif mode=='count':
        for d in da:
            lhs='(+ '+' '.join(f'(ite (= {d} {x}) 1 0)' for x in da)+')'
            rhs='(+ '+' '.join(f'(ite (= {d} {x}) 1 0)' for x in db)+')'
            lines += [f'(assert (= {lhs} {rhs}))']
    elif mode=='sorting':
        for lab,ds in [('a',da),('b',db)]:
            s=[];c=0
            for d in ds:
                carry=d; new=[]
                for old in s:
                    lo=f'{lab}lo{c}';hi=f'{lab}hi{c}';c+=1
                    lines += [f'(define-fun {lo} () Real (ite (<= {old} {carry}) {old} {carry}))',f'(define-fun {hi} () Real (ite (<= {old} {carry}) {carry} {old}))']
                    new.append(lo);carry=hi
                s=new+[carry]
            if lab=='a':left=s
            else:lines += [f'(assert (= {a} {b}))' for a,b in zip(left,s)]
    else:raise ValueError(mode)
    templates,cuts=bloom_templates()
    if exclude_bloom:
        for pair in NORMAL_FORMS if normal_forms else templates:lines += ['(assert (not '+plane_constraints(pair)+'))']
    lines+=['(check-sat)', '(get-proof)' if proof else '(get-info :all-statistics)']
    return '\n'.join(lines)+'\n', {'mode':mode,'bloom_order_templates':len(templates),'excluded_planes':2 if normal_forms else len(templates),'cuts':[str(x) for x in cuts]}

def main():
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['count','sorting'],default='count');p.add_argument('--timeout',type=int,default=60);p.add_argument('--out',default='results/2026-09-30-six-integer-smt');p.add_argument('--generate-only',action='store_true');p.add_argument('--proof',action='store_true');a=p.parse_args()
    base=Path(a.out);base.mkdir(parents=True,exist_ok=True)
    text,meta=encode(a.mode,1000*a.timeout,proof=a.proof);path=base/(a.mode+'.smt2');path.write_text(text)
    meta['status']='GENERATED'
    meta['input_sha256']=hashlib.sha256(text.encode()).hexdigest()
    meta['z3_version']=subprocess.check_output(['z3','--version'],text=True).strip()
    if not a.generate_only:
        t=time.monotonic();r=subprocess.run(['z3','-smt2',str(path)],text=True,capture_output=True);meta.update(seconds=time.monotonic()-t,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,status='EXPERIMENTAL-SOLVER-RESULT')
    if a.proof and not a.generate_only:
        proof_path=base/(a.mode+'.proof.gz')
        with gzip.open(proof_path,'wt') as f:f.write(meta['stdout'])
        meta['proof_path']=str(proof_path)
        meta['stdout']=meta['stdout'].splitlines()[0]
    (base/(a.mode+'.json')).write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta,indent=2))
if __name__=='__main__':main()
