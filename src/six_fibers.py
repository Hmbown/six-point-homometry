"""Low-support cylinder fibers: exact cross-edge orbit reduction."""
from __future__ import annotations
import argparse,json,time
from collections import Counter,deque
from itertools import permutations,combinations
from math import factorial,prod
from pathlib import Path
from sympy import Matrix,ZZ
from sympy.matrices.normalforms import hermite_normal_form
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp

def edge_actions(r,s):
 n=r*s;out=[]
 for i in range(r-1):
  out.append(tuple((i+1)*s+j if k==i else i*s+j if k==i+1 else k*s+j for k in range(r) for j in range(s)))
 for j in range(s-1):
  out.append(tuple(i*s+(j+1 if l==j else j if l==j+1 else l) for i in range(r) for l in range(s)))
 return out

def cross_orbits(r,s):
 """All double orbits under within-fiber source/target vertex relabelling.

 Adjacent row/column transpositions generate the full allowed product of
 symmetric groups.  No group-unit quotient or chord-class identification.
 """
 actions=edge_actions(r,s);seen=set()
 for p in permutations(range(r*s)):
  if p in seen:continue
  todo=deque([p]);seen.add(p);size=0
  while todo:
   x=todo.popleft();size+=1
   for a in actions:
    for y in (tuple(x[i] for i in a),tuple(a[i] for i in x)):
     if y not in seen:seen.add(y);todo.append(y)
  yield p,size
 assert len(seen)==factorial(r*s)

def cross_matrix(r,s,p):
 rows=[]
 for e,f in enumerate(p):
  i,j=divmod(e,s);k,l=divmod(f,s);j+=r;l+=r
  row=[0]*10
  for a,v in ((i,-1),(j,1)):
   if a:row[a-1]+=v
  for a,v in ((k,1),(l,-1)):
   if a:row[a+4]+=v
  rows.append(row)
 return Matrix(rows)

def group_add(a,b,torsion,sign=1):
 out=[x+sign*y for x,y in zip(a,b)]
 for i,d in enumerate(torsion):out[i]%=d
 return tuple(out)

def group_record(m):
 dd,uu,vv=smith_normal_decomp(DomainMatrix.from_Matrix(m).convert_to(ZZ))
 d,u,v=(x.to_Matrix() for x in (dd,uu,vv));assert u*m*v==d
 diag=[int(d[i,i]) for i in range(min(m.shape))];rank=sum(x!=0 for x in diag)
 torsion=[abs(x) for x in diag[:rank] if abs(x)>1];indices=[i for i in range(rank) if abs(diag[i])>1]+list(range(rank,10))
 points=[]
 for j in range(10):
  point=[int(v[j,i]) for i in indices]
  for i,mod in enumerate(torsion):point[i]%=mod
  points.append(tuple(point))
 zero=(0,)*len(indices);a=(zero,*points[:5]);b=(zero,*points[5:])
 collision=len(set(a))<6 or len(set(b))<6
 congruence=None
 for sign in (1,-1):
  for shift in b:
   if {group_add(shift,x,torsion,sign) for x in a}==set(b):congruence={'sign':sign,'shift':shift};break
  if congruence:break
 da=Counter(group_add(x,y,torsion,-1) for x in a for y in a)
 db=Counter(group_add(x,y,torsion,-1) for x in b for y in b)
 return {'matrix':m.tolist(),'smith_u':u.tolist(),'smith_v':v.tolist(),'smith_diagonal':diag,'rank':rank,'free_rank':10-rank,'torsion':torsion,'a':a,'b':b,'forced_collision':collision,'forced_ti':congruence,'already_homometric':da==db}

def edge_row(edge,side):
 i,j=edge;row=[0]*10
 for a,v in ((i,-1),(j,1)):
  if a:row[a-1+5*side]+=v
 return tuple(row)

def canonical_lattice(m):
 return hermite_normal_form(m.T).T

def quotient_search(r,s,orbit_records,max_nodes=2000,progress=None):
 nodes=[];lookup={};roots=[];start=time.monotonic();internal=tuple(combinations(range(r),2))+tuple(combinations(range(r,6),2))
 def visit(matrix):
  h=canonical_lattice(matrix);key=tuple(map(tuple,h.tolist()))
  if key in lookup:return lookup[key]
  if max_nodes and len(nodes)>=max_nodes:raise RuntimeError('node cap')
  index=len(nodes);lookup[key]=index;record=group_record(h);node={'id':index,**record};nodes.append(node)
  if len(nodes)%100==0 and progress:progress(len(nodes),time.monotonic()-start)
  if record['forced_collision']:node['terminal']='collision';return index
  if record['forced_ti']:node['terminal']='ti';return index
  if record['already_homometric']:node['terminal']='homometric';return index
  a,b=record['a'],record['b'];torsion=record['torsion']
  def classes(points):
   out={}
   for edge in internal:
    i,j=edge;delta=group_add(points[j],points[i],torsion,-1)
    neg=group_add((0,)*len(delta),delta,torsion,-1);k=min(delta,neg)
    out.setdefault(k,[]).append(edge)
   return out
  aa,bb=classes(a),classes(b)
  for k in aa.keys()&bb.keys():
   count=min(len(aa[k]),len(bb[k]));aa[k]=aa[k][count:];bb[k]=bb[k][count:]
  aa={k:v for k,v in aa.items() if v};bb={k:v for k,v in bb.items() if v}
  assert aa and bb
  ka=min(aa,key=lambda k:(-len(aa[k]),k));chosen=aa[ka][0];ar=edge_row(chosen,0)
  node['chosen_a']=chosen;node['residual_a']=[(k,v) for k,v in sorted(aa.items())];node['residual_b']=[(k,v) for k,v in sorted(bb.items())];node['branches']=[]
  for kb,edges in sorted(bb.items()):
   edge=edges[0];br=edge_row(edge,1)
   for sign in (1,-1):
    rel=tuple(x-sign*y for x,y in zip(ar,br))
    child=visit(h.col_join(Matrix([rel])))
    node['branches'].append({'b_edge':edge,'sign':sign,'child':child})
  return index
 complete=True;error=None
 try:
  for row in orbit_records:roots.append({'orbit_id':row['id'],'node':visit(Matrix(row['matrix']))})
 except RuntimeError as exc:complete=False;error=str(exc)
 return {'complete':complete,'error':error,'node_cap':max_nodes,'profile':[r,s],'roots':roots,'nodes':nodes,'seconds':time.monotonic()-start,'terminal_histogram':dict(Counter(x.get('terminal','branch') for x in nodes))}

def main():
 p=argparse.ArgumentParser();p.add_argument('--profile',choices=['4,2','3,3','5,1'],default='4,2');p.add_argument('--out',default='results/2026-09-30-six-fibers');p.add_argument('--quotients',action='store_true');p.add_argument('--max-nodes',type=int,default=2000);a=p.parse_args();r,s=map(int,a.profile.split(','));rows=[];start=time.monotonic()
 for i,(permutation,size) in enumerate(cross_orbits(r,s)):
  g=group_record(cross_matrix(r,s,permutation));rows.append({'id':i,'permutation':permutation,'orbit_size':size,**g})
  if i%20==0:print('orbits',i+1,'covered',sum(x['orbit_size'] for x in rows),'seconds',time.monotonic()-start,flush=True)
 hist=Counter((x['free_rank'],tuple(x['torsion']),x['forced_collision'],bool(x['forced_ti']),x['already_homometric']) for x in rows)
 result={'status':'COMPUTED-UNVALIDATED','profile':[r,s],'raw_cross_permutations':factorial(r*s),'orbit_count':len(rows),'covered_permutations':sum(x['orbit_size'] for x in rows),'histogram':[(list(k),v) for k,v in hist.items()],'records':rows,'seconds':time.monotonic()-start}
 base=Path(a.out);base.mkdir(parents=True,exist_ok=True);(base/f'{r}-{s}-cross.json').write_text(json.dumps(result,default=int)+'\n');print({k:v for k,v in result.items() if k!='records'},flush=True)
 if a.quotients:
  q=quotient_search(r,s,rows,a.max_nodes,lambda count,seconds:print('quotient nodes',count,'seconds',seconds,flush=True))
  (base/f'{r}-{s}-quotients.json').write_text(json.dumps(q,default=int)+'\n')
  print({k:v for k,v in q.items() if k not in ('roots','nodes')},flush=True)
if __name__=='__main__':main()
