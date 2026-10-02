"""Exact finite presentations for noncongruent free projections of six atoms.

The two real Bloom normal forms have only five exceptional distance slopes.
All compatible real edge matchings, including both signs at distance zero,
are enumerated. Smith certificates describe every possible torsion lift.
"""
from __future__ import annotations
import argparse,hashlib,json,time
from collections import Counter,defaultdict
from fractions import Fraction as F
from itertools import combinations,permutations,product
from math import factorial,prod
from pathlib import Path
from sympy import Matrix,ZZ
from sympy.matrices.normalforms import hermite_normal_form
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp
from six_integer_smt import NORMAL_FORMS,X,Y
EDGES=tuple(combinations(range(6),2))

def difference_forms(points):
 return [(b[0]-a[0],b[1]-a[1]) for a,b in combinations(points,2)]

def critical_slopes(kind):
 forms=difference_forms(NORMAL_FORMS[kind-1][0])
 candidates={F(v[0]-u[0],u[1]-v[1]) for u,v in combinations(forms,2) if u[1]!=v[1]}
 # Include point-collision boundaries even if a zero edge were otherwise unique.
 candidates.update([F(3)] if kind==1 else [F(3,2)])
 return sorted(t for t in candidates if (t>=3 if kind==1 else F(3,2)<=t<2))

def buckets(points,slope):
 out=defaultdict(list)
 for edge,form in zip(EDGES,difference_forms(points)):
  key=form if slope is None else form[0]*slope.denominator+form[1]*slope.numerator
  out[key].append(edge)
 return dict(sorted(out.items()))

def matchings(kind,slope=None):
 a,b=NORMAL_FORMS[kind-1];ba,bb=buckets(a,slope),buckets(b,slope)
 assert {d:len(es) for d,es in ba.items()}=={d:len(es) for d,es in bb.items()}
 groups=list(ba)
 def rec(index,labels):
  if index==len(groups):
   # Fixed A-edge order makes direct independent checking convenient.
   labels=tuple(sorted(labels));rows=[]
   for i,j,k,l,s in labels:
    row=[0]*10
    for vertex,value in ((i,-1),(j,1)):
     if vertex:row[vertex-1]=value
    for vertex,value in ((k,s),(l,-s)):
     if vertex:row[vertex+4]=value
    rows.append(row)
   yield Matrix(rows),labels
   return
  d=groups[index]
  for targets in permutations(bb[d]):
   for signs in product(*[((1,-1) if d==0 else (1,)) for _ in targets]):
    yield from rec(index+1,labels+[(i,j,k,l,s) for (i,j),(k,l),s in zip(ba[d],targets,signs)])
 yield from rec(0,[])

def expected(kind,slope):
 bs=buckets(NORMAL_FORMS[kind-1][0],slope)
 return prod(factorial(len(es))*(2**len(es) if d==0 else 1) for d,es in bs.items())

def presentation(m,labels):
 dd,uu,vv=smith_normal_decomp(DomainMatrix.from_Matrix(m).convert_to(ZZ))
 d,u,v=(x.to_Matrix() for x in (dd,uu,vv))
 assert u*m*v==d
 ds=[int(d[i,i]) for i in range(10)];rank=sum(x!=0 for x in ds)
 ts=[i for i in range(rank) if abs(ds[i])>1];fs=list(range(rank,10))
 pts=[]
 for j in range(10):pts.append([*[int(v[j,i])%abs(ds[i]) for i in ts],*[int(v[j,i]) for i in fs]])
 origin=[0]*(len(ts)+len(fs));a=[origin]+pts[:5];b=[origin]+pts[5:]
 return {'labels':labels,'matrix':m.tolist(),'smith_diagonal':ds,'smith_u':u.tolist(),'smith_v':v.tolist(),'rank':rank,'free_rank':10-rank,'torsion_factors':[abs(ds[i]) for i in ts],'torsion_order':prod(abs(x) for x in ds[:rank]),'a':a,'b':b,'six_distinct_in_presentation':len({tuple(x) for x in a})==len({tuple(x) for x in b})==6,'row_lattice_hnf':hermite_normal_form(m.T).tolist()}

def group_linear(terms,torsion):
 n=len(terms[0][1]);result=[sum(c*v[i] for c,v in terms) for i in range(n)]
 for i,d in enumerate(torsion):result[i]%=d
 return tuple(result)

def bloom_certificate(presentation):
 """Exhibit raw Bloom parameters and separate rigid motions in the group.

 The search has exactly 2*6*5*4 candidate (anchor,p,q) choices: the raw X
 coordinates 0,p,q-2p are three distinct points whenever X has six points.
 Completeness of this certificate search is not needed for the theorem;
 each returned identity is checked directly.
 """
 torsion=presentation['torsion_factors'];a=tuple(map(tuple,presentation['a']));b=tuple(map(tuple,presentation['b']))
 lin=lambda *terms:group_linear(terms,torsion)
 for side,source,target in [('a',a,b),('b',b,a)]:
  for i,j,k in permutations(range(6),3):
   anchor=source[i];p=lin((1,source[j]),(-1,anchor));q=lin((1,source[k]),(-1,anchor),(2,p))
   xx=[lin((1,anchor),(u,p),(v,q)) for u,v in X]
   if Counter(xx)!=Counter(source):continue
   for sign in (1,-1):
    for shift in target:
     yy=[lin((1,shift),(sign*u,p),(sign*v,q)) for u,v in Y]
     if Counter(yy)==Counter(target):
      return {'x_side':side,'p':p,'q':q,'shift_x':anchor,'shift_y':shift,'sign_y':sign}
 return None

def row_coefficients(rows,basis_presentation):
 """Express integer rows in the row lattice certified by a Smith transform."""
 u=Matrix(basis_presentation['smith_u']);v=Matrix(basis_presentation['smith_v']);ds=basis_presentation['smith_diagonal']
 transformed=rows*v;coefficients=Matrix.zeros(rows.rows,15)
 for j in range(10):
  if ds[j]:
   assert all(int(x)%ds[j]==0 for x in transformed[:,j])
   for i in range(rows.rows):coefficients[i,j]=transformed[i,j]/ds[j]
  else:assert all(x==0 for x in transformed[:,j])
 result=coefficients*u
 assert result*Matrix(basis_presentation['matrix'])==rows
 return result.tolist()

def run():
 out=[];unique={};start=time.monotonic()
 for kind in (1,2):
  for slope in [None,*critical_slopes(kind)]:
   t=time.monotonic();records=[];matching_records=[]
   for m,labels in matchings(kind,slope):
    rec=presentation(m,labels);key=tuple(tuple(row) for row in rec['row_lattice_hnf'])
    if key not in unique:
     if rec['six_distinct_in_presentation']:
      rec['bloom_certificate']=bloom_certificate(rec)
      assert rec['bloom_certificate'] is not None, ('not Bloom',kind,slope,rec)
     unique[key]={'id':len(unique),'presentation':rec,'occurrences':[]}
    uid=unique[key]['id'];unique[key]['occurrences'].append({'kind':kind,'slope':str(slope),'matching_index':len(records)})
    matching_records.append({'presentation_id':uid,'labels':labels,'representative_from_matching':row_coefficients(Matrix(unique[key]['presentation']['matrix']),rec),'matching_from_representative':row_coefficients(m,unique[key]['presentation'])})
    records.append(uid)
   assert len(records)==expected(kind,slope)
   summary=Counter((unique[k]['presentation']['free_rank'],tuple(unique[k]['presentation']['torsion_factors']),unique[k]['presentation']['six_distinct_in_presentation']) for k in unique if any(o['kind']==kind and o['slope']==str(slope) for o in unique[k]['occurrences']))
   row={'kind':kind,'slope':str(slope),'expected_matchings':expected(kind,slope),'matching_presentation_ids':records,'matching_records':matching_records,'seconds':time.monotonic()-t,'unique_presentation_histogram':[(list(k),v) for k,v in summary.items()]}
   out.append(row);print('kind',kind,'slope',slope,'matchings',len(records),'seconds',row['seconds'],'histogram',row['unique_presentation_histogram'],flush=True)
 return {'status':'COMPUTED-UNVALIDATED until separate audit','scope':'noncongruent free projection, conditional on real six-atom theorem','cases':out,'presentations':list(unique.values()),'total_matchings':sum(len(x['matching_presentation_ids']) for x in out),'unique_labelled_row_lattices':len(unique),'seconds':time.monotonic()-start,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',default='results/2026-09-30-six-bloom-cylinders.json');a=p.parse_args();result=run();Path(a.out).write_text(json.dumps(result,sort_keys=True,default=int)+'\n');print('total',result['total_matchings'],'unique',result['unique_labelled_row_lattices'],'seconds',result['seconds'],flush=True)
if __name__=='__main__':main()
