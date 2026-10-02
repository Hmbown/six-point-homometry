"""Verify saved low-height certificates without normal-form calculations."""
from __future__ import annotations
import json,sys,time
from collections import Counter
from itertools import combinations,permutations,product
from math import factorial,gcd,lcm
from pathlib import Path
from sympy import Matrix,zeros
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from homometry import icv
BASE=ROOT/'results/2026-09-30-six-fibers'

class G:
 def __init__(self,t,n):self.t=tuple(t);self.n=n;self.zero=(0,)*n
 def norm(self,p):return tuple(x%self.t[i] if i<len(self.t) else x for i,x in enumerate(p))
 def add(self,a,b):return self.norm(tuple(x+y for x,y in zip(a,b)))
 def neg(self,a):return self.norm(tuple(-x for x in a))
 def mul(self,k,a):return self.norm(tuple(k*x for x in a))
 def sub(self,a,b):return self.add(a,self.neg(b))
 def shift(self,S,t,sign=1):return {self.add(t,self.mul(sign,x)) for x in S}
 def conv(self,A,B,sign=-1):return Counter(self.add(x,self.mul(sign,y)) for x in A for y in B)
 def shiftp(self,P,t):return Counter({self.add(x,t):v for x,v in P.items()})
 def star(self,P):return Counter({self.neg(x):v for x,v in P.items()})
 def signed(self,*terms):
  out=Counter()
  for c,P in terms:
   for x,v in P.items():out[x]+=c*v
  return {x:v for x,v in out.items() if v}

def smith(record):
 m=Matrix(record['matrix']);u=Matrix(record['smith_u']);v=Matrix(record['smith_v']);d=zeros(*m.shape)
 for i,x in enumerate(record['smith_diagonal']):d[i,i]=x
 assert u*m*v==d and abs(u.det())==abs(v.det())==1
 rank=sum(x!=0 for x in record['smith_diagonal']);assert rank==record['rank']
 idx=[i for i in range(rank) if abs(d[i,i])>1]+list(range(rank,10))
 torsion=[abs(int(d[i,i])) for i in range(rank) if abs(d[i,i])>1];assert torsion==record['torsion']
 g=G(torsion,len(idx));points=[g.norm(tuple(int(v[j,i]) for i in idx)) for j in range(10)]
 assert [g.zero,*points[:5]]==list(map(tuple,record['a']))
 assert [g.zero,*points[5:]]==list(map(tuple,record['b']))
 return g

def edge(i,j,side):
 x=[0]*10
 if i:x[i-1+side*5]-=1
 if j:x[j-1+side*5]+=1
 return x

def cross_matrix(r,s,p):
 rows=[]
 for i,k in enumerate(p):
  a,b=divmod(i,s);c,d=divmod(k,s)
  rows.append([x-y for x,y in zip(edge(a,b+r,0),edge(c,d+r,1))])
 return Matrix(rows)

def full_actions(r,s):
 for a in permutations(range(r)):
  for b in permutations(range(s)):yield tuple(a[i]*s+b[j] for i in range(r) for j in range(s))

def audit_cross(profile):
 r,s=profile;doc=json.loads((BASE/f'{r}-{s}-cross.json').read_text());seen=set();actions=list(full_actions(r,s))
 for rec in doc['records']:
  p=rec['permutation'];orbit={tuple(b[p[a[i]]] for i in range(r*s)) for a in actions for b in actions}
  assert len(orbit)==rec['orbit_size'] and not seen.intersection(orbit);seen.update(orbit)
  assert Matrix(rec['matrix'])==cross_matrix(r,s,p);smith(rec)
 assert len(seen)==factorial(r*s)==doc['covered_permutations']
 return doc

def residual(node,r):
 g=G(node['torsion'],len(node['a'][0]));internal=list(combinations(range(r),2))+list(combinations(range(r,6),2));sides=[]
 for side in ('a','b'):
  P=list(map(tuple,node[side]));classes={}
  for i,j in internal:
   v=g.sub(P[j],P[i]);v=min(v,g.neg(v));classes.setdefault(v,[]).append((i,j))
  sides.append(classes)
 aa,bb=sides
 for v in aa.keys()&bb.keys():
  k=min(len(aa[v]),len(bb[v]));aa[v]=aa[v][k:];bb[v]=bb[v][k:]
 return {k:v for k,v in aa.items() if v},{k:v for k,v in bb.items() if v}

def audit_dag(profile,cross):
 r,s=profile;doc=json.loads((BASE/f'{r}-{s}-certified.json').read_text());assert doc['complete'];nodes=doc['nodes'];seen=set()
 for root in doc['roots']:
  original=Matrix(cross['records'][root['orbit_id']]['matrix']);target=Matrix(nodes[root['node']]['matrix'])
  assert Matrix(root['cross_to_root'])*target==original
  assert Matrix(root['root_to_cross'])*original==target
 assert {x['orbit_id'] for x in doc['roots']}==set(range(len(cross['records'])))
 def visit(i):
  if i in seen:return
  seen.add(i);n=nodes[i];assert n['id']==i;g=smith(n);a=set(map(tuple,n['a']));b=set(map(tuple,n['b']))
  collision=len(a)<6 or len(b)<6;assert collision==n['forced_collision']
  hom=g.conv(a,a)==g.conv(b,b) if not collision else g.conv(n['a'],n['a'])==g.conv(n['b'],n['b'])
  assert hom==n['already_homometric']
  if n.get('terminal')=='collision':assert collision;return
  if n.get('terminal')=='ti':
   t=n['forced_ti'];assert g.shift(a,tuple(t['shift']),t['sign'])==b;return
  if n.get('terminal')=='homometric':assert hom and len(a)==len(b)==6;return
  aa,bb=residual(n,r);assert aa and bb
  saved=lambda x:{tuple(k):list(map(tuple,v)) for k,v in x}
  assert saved(n['residual_a'])==aa and saved(n['residual_b'])==bb
  ae=tuple(n['chosen_a']);assert any(ae in v for v in aa.values())
  wanted={(v[0],sign) for v in bb.values() for sign in (1,-1)}
  assert {(tuple(br['b_edge']),br['sign']) for br in n['branches']}==wanted
  ar=edge(*ae,0)
  for branch in n['branches']:
   br=edge(*branch['b_edge'],1);relation=[x-branch['sign']*y for x,y in zip(ar,br)]
   extension=Matrix(n['matrix']+[relation]);child=nodes[branch['child']];cm=Matrix(child['matrix'])
   assert Matrix(branch['extension_to_child'])*cm==extension
   assert Matrix(branch['child_to_extension'])*extension==cm
   ca,cb=residual(child,r);assert sum(map(len,ca.values()))<sum(map(len,aa.values()))
   visit(branch['child'])
 for root in doc['roots']:visit(root['node'])
 assert seen==set(range(len(nodes)))
 return doc

def audit_move(record,c):
 a=set(map(tuple,record['a']));b=set(map(tuple,record['b']));g=G(record['torsion'],len(next(iter(a))))
 assert g.conv(a,a)==g.conv(b,b);bb=g.shift(b,tuple(c['alignment_shift']),c['alignment_sign']);kind=c['type']
 if kind=='D-dyad':
  C=set(map(tuple,c['common']));x=tuple(c['anchor']);s,t=map(tuple,c['steps']);center=g.add(s,t)
  assert g.shift(C|{g.zero,center},x)==a and g.shift(C|{s,t},x)==bb
  W=Counter(C)+Counter(g.sub(center,z) for z in C)+Counter((g.zero,s,t,center))
  assert not g.signed((1,W),(-1,g.shiftp(W,s)),(-1,g.shiftp(W,t)),(1,g.shiftp(W,center)))
  return
 U=set(map(tuple,c['fixed']));V=set(map(tuple,c['moving']));t=tuple(c['move']);P=g.conv(U,V);Ps=g.star(P)
 assert U.isdisjoint(V) and U|V==a
 if kind=='L2-translate':assert g.shiftp(P,t)==P
 elif kind=='L3star-cosymmetric':assert P==g.shiftp(Ps,t)
 elif kind=='L4-halfturn':assert g.mul(2,t)==g.zero and g.shiftp(P+Ps,t)==P+Ps
 elif kind=='L5-reflect':assert P==g.shiftp(g.conv(U,V,1),g.neg(t))
 else:raise AssertionError(kind)
 assert U|g.shift(V,t,-1 if kind=='L5-reflect' else 1)==bb

def audit_cyclic_cover(record,cover):
 T=record['torsion'];exponent=lcm(*T) if T else 1
 assert {tuple(c['character']) for c in cover}==set(product(*(range(d) for d in T)))
 for c in cover:
  coeff=[k*(exponent//d) for k,d in zip(c['character'],T)];scale=gcd(exponent,*coeff);q=exponent//scale
  assert c['image_order']==q and c['torsion']==([q] if q>1 else [])
  for side in ('a','b'):
   expected=[(([sum(t*k for t,k in zip(p,coeff))%exponent//scale] if q>1 else [])+p[len(T):]) for p in record[side]]
   assert c[side]==expected
  if 'collision' in c:
   w=c['collision'];i,j=w['indices'];assert i!=j and c[w['side']][i]==c[w['side']][j]
  elif 'ti' in c:
   g=G(c['torsion'],len(c['a'][0]));assert g.shift(map(tuple,c['a']),tuple(c['ti']['shift']),c['ti']['sign'])==set(map(tuple,c['b']))
  else:assert c['mechanism'];audit_move(c,c['mechanism'])

def audit_mechanisms(dags):
 doc=json.loads((BASE/'mechanisms-cyclic.json').read_text());expected={(name,n['id']) for name,d in dags.items() for n in d['nodes'] if n.get('terminal')=='homometric'}
 assert {(r['profile'],r['node']) for r in doc['rows']}==expected
 for row in doc['rows']:
  n=dags[row['profile']]['nodes'][row['node']]
  if row['mechanism']:audit_move(n,row['mechanism'])
  else:audit_cyclic_cover(n,row['cyclic_cover'])
 return len(doc['rows'])

def reference_specializations(dags):
 checks=0
 for doc in dags.values():
  for n in doc['nodes']:
   if n.get('terminal')!='homometric':continue
   T=n['torsion'];e=lcm(*T) if T else 1
   for factor in (3,5):
    modulus=e*factor
    for seed in range(6):
     co=[(modulus//d)*(seed+i+1) for i,d in enumerate(T)]+[(seed+2)**(i+1) for i in range(n['free_rank'])]
     a=sorted({sum(x*y for x,y in zip(p,co))%modulus for p in n['a']});b=sorted({sum(x*y for x,y in zip(p,co))%modulus for p in n['b']})
     if len(a)==len(b)==6:assert icv(a,modulus)==icv(b,modulus);checks+=1
 assert checks>100
 return checks

def main():
 started=time.monotonic();dags={}
 for profile in ((4,2),(3,3)):
  cross=audit_cross(profile);name='-'.join(map(str,profile));dags[name]=audit_dag(profile,cross);print(name,'orbit and quotient certificates verified',flush=True)
 print('mechanisms',audit_mechanisms(dags),'reference specializations',reference_specializations(dags),'seconds',time.monotonic()-started,flush=True)
if __name__=='__main__':main()
