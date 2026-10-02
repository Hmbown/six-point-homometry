"""Recognize reviewed structural moves in exact finitely generated groups."""
from __future__ import annotations
import argparse,json,time
from collections import Counter
from itertools import combinations,product
from pathlib import Path
from six_bloom_cylinders import bloom_certificate

class Group:
 def __init__(self,torsion,dimension):self.torsion=tuple(torsion);self.dimension=dimension;self.zero=(0,)*dimension
 def norm(self,x):return tuple(v%d if i<len(self.torsion) else v for i,(v,d) in enumerate(zip(x,(*self.torsion,*([1]*(self.dimension-len(self.torsion)))))))
 def add(self,a,b):return self.norm(tuple(x+y for x,y in zip(a,b)))
 def neg(self,a):return self.norm(tuple(-x for x in a))
 def sub(self,a,b):return self.add(a,self.neg(b))
 def scale(self,k,a):return self.norm(tuple(k*x for x in a))
 def translate(self,a,t,sign=1):return {self.add(t,self.scale(sign,x)) for x in a}
 def convolution(self,a,b,sign=-1):return Counter(self.add(x,self.scale(sign,y)) for x in a for y in b)
 def shifted(self,p,t):return Counter({self.add(x,t):v for x,v in p.items()})
 def reflected(self,p):return Counter({self.neg(x):v for x,v in p.items()})
 def signed_sum(self,*terms):
  c=Counter()
  for coefficient,p in terms:
   for k,v in p.items():c[k]+=coefficient*v
  return Counter({k:v for k,v in c.items() if v})

def finite_subgroups(g):
 T=[tuple(t)+(0,)*(g.dimension-len(g.torsion)) for t in product(*(range(d) for d in g.torsion))]
 seen={frozenset([g.zero])};todo=list(seen)
 while todo:
  H=todo.pop();yield H
  for t in T:
   if t in H:continue
   coset=set(H);u=t
   while u not in H:
    coset.update(g.add(h,u) for h in H);u=g.add(u,t)
   K=frozenset(coset)
   if K not in seen:seen.add(K);todo.append(K)

def mechanism(record):
 a=set(map(tuple,record['a']));b=set(map(tuple,record['b']));g=Group(record['torsion'],len(next(iter(a))))
 bloom=bloom_certificate({'a':list(a),'b':list(b),'torsion_factors':record['torsion']})
 if bloom:return {'type':'Bloom','certificate':bloom}
 alignments={}
 for sign in (1,-1):
  for x in a:
   for y in b:
    shift=g.sub(x,g.scale(sign,y));bb=frozenset(g.translate(b,shift,sign));alignments.setdefault(bb,(sign,shift))
 for bb,(sign,shift) in alignments.items():
  common=a&bb;left=a-bb;right=bb-a
  if len(common)==4 and len(left)==len(right)==2:
   x,y=sorted(left);u,v=sorted(right)
   if g.add(x,y)==g.add(u,v):
    c={g.sub(z,x) for z in common};sa=g.sub(u,x);sb=g.sub(v,x);center=g.add(sa,sb)
    w=Counter(c)+Counter(g.sub(center,z) for z in c)+Counter([g.zero,sa,sb,center])
    annih=g.signed_sum((1,w),(-1,g.shifted(w,sa)),(-1,g.shifted(w,sb)),(1,g.shifted(w,center)))
    assert not annih
    return {'type':'D-dyad','alignment_sign':sign,'alignment_shift':shift,'anchor':x,'common':sorted(c),'steps':[sa,sb]}
 # Half-per-coset complementation, including all finite subgroup shapes.
 for H in finite_subgroups(g):
  if len(H)<2 or len(H)%2 or len(H)>12:continue
  support={g.add(x,h) for x in a for h in H}
  if len(support)!=12:continue
  if any(len({g.add(x,h) for h in H}&a)!=len(H)//2 for x in a):continue
  partner=frozenset(support-a)
  if partner in alignments:
   sign,shift=alignments[partner]
   return {'type':'L7-halfcoset','subgroup':sorted(H),'alignment_sign':sign,'alignment_shift':shift}
 for bb,(asign,ashift) in alignments.items():
  common=sorted(a&bb)
  for size in range(1,len(common)+1):
   for uu in combinations(common,size):
    u=set(uu);w=a-u;z=set(bb)-u
    if not w or len(w)!=len(z):continue
    x=min(w)
    cross=g.convolution(u,w);back=g.reflected(cross)
    for y in z:
     delta=g.sub(y,x)
     if g.translate(w,delta)==z:
      if g.shifted(cross,delta)==cross:kind='L2-translate'
      elif cross==g.shifted(back,delta):kind='L3star-cosymmetric'
      elif g.scale(2,delta)==g.zero and g.shifted(cross+back,delta)==cross+back:kind='L4-halfturn'
      else:kind=None
      if kind:return {'type':kind,'alignment_sign':asign,'alignment_shift':ashift,'fixed':sorted(u),'moving':sorted(w),'move':delta}
     delta=g.add(y,x)
     if g.translate(w,delta,-1)==z:
      if cross==g.shifted(g.convolution(u,w,1),g.neg(delta)):
       return {'type':'L5-reflect','alignment_sign':asign,'alignment_shift':ashift,'fixed':sorted(u),'moving':sorted(w),'move':delta}
 return None

def main():
 p=argparse.ArgumentParser();p.add_argument('--out');p.add_argument('--cyclic',action='store_true');a=p.parse_args();result=[];start=time.monotonic()
 for profile in ('4-2','3-3'):
  source=Path(f'results/2026-09-30-six-fibers/{profile}-quotients.json');d=json.loads(source.read_text())
  for node in d['nodes']:
   if node.get('terminal')!='homometric':continue
   cert=mechanism(node);row={'profile':profile,'node':node['id'],'mechanism':cert}
   if cert is None and a.cyclic:row['cyclic_cover']=cyclic_cover(node)
   result.append(row)
  subset=[r for r in result if r['profile']==profile];print(profile,Counter(r['mechanism']['type'] if r['mechanism'] else 'gap' for r in subset),flush=True)
 Path(a.out or ('results/2026-09-30-six-fibers/mechanisms-cyclic.json' if a.cyclic else 'results/2026-09-30-six-fibers/mechanisms.json')).write_text(json.dumps({'status':'COMPUTED-UNVALIDATED','rows':result,'seconds':time.monotonic()-start})+'\n');print('seconds',time.monotonic()-start,flush=True)


def cyclic_character_quotients(record):
 """All maps from finite torsion to a cyclic group, modulo image scaling.

 Every map into any cyclic group has the same kernel as one of these
 characters T -> Q/Z.  The free coordinates are retained independently.
 """
 from math import lcm,gcd
 t=tuple(record['torsion']);exponent=lcm(*t) if t else 1
 for character in product(*(range(d) for d in t)):
  coefficients=tuple(k*(exponent//d) for k,d in zip(character,t))
  common=gcd(exponent,*coefficients);order=exponent//common
  def project(p):
   residue=sum(k*x for k,x in zip(coefficients,p))%exponent
   return ((residue//common,) if order>1 else ())+tuple(p[len(t):])
  a=tuple(project(p) for p in record['a']);b=tuple(project(p) for p in record['b'])
  q={'torsion':[order] if order>1 else [],'a':a,'b':b,'character':character,'image_order':order}
  for name,points in (('a',a),('b',b)):
   for i,j in combinations(range(6),2):
    if points[i]==points[j]:q['collision']={'side':name,'indices':[i,j]};break
   if 'collision' in q:break
  if 'collision' not in q:
   g=Group(q['torsion'],len(a[0]))
   for sign in (1,-1):
    for shift in b:
     if g.translate(a,shift,sign)==set(b):q['ti']={'sign':sign,'shift':shift};break
    if 'ti' in q:break
  yield q


def cyclic_cover(record):
 result=[]
 for quotient in cyclic_character_quotients(record):
  if 'collision' not in quotient and 'ti' not in quotient:quotient['mechanism']=mechanism(quotient)
  result.append(quotient)
 return result

if __name__=='__main__':main()
