"""Executable arbitrary-n six-note homometry certificates.

Direct sparse group identities first; otherwise an exact saved finite-family
path in the ordinary support quotient, followed by ordinary inflation.
No failure of recognition is reported as nonhomometry. Run --help for usage.
"""
from __future__ import annotations
import argparse,json
from collections import Counter,defaultdict,deque
from functools import lru_cache
from itertools import combinations,permutations
from math import gcd
from pathlib import Path
from homometry import icv as reference_icv,dihedral_canon as reference_canon

ROOT=Path(__file__).resolve().parents[1]
REFERENCE_LIMIT=4096
BLOOM_X=((0,0),(1,0),(-2,1),(-2,2),(0,2),(-1,3))
BLOOM_Y=((0,0),(1,0),(2,1),(-1,2),(1,2),(-1,3))

class GenerationInvariantError(RuntimeError):
 """A validated homometric pair was not covered by the proved implementation."""

def require(ok,message):
 if not ok:raise ValueError(message)

def canon_witness(points,n):
 points=tuple(points)
 image,sign,shift=min((tuple(sorted((s*(x-anchor))%n for x in points)),s,(-s*anchor)%n) for s in (1,-1) for anchor in points)
 return image,{'sign':sign,'shift':shift}

def canon(points,n):return canon_witness(points,n)[0]
def move(points,n,sign=1,shift=0):return {(sign*x+shift)%n for x in points}
def interval_counter(points,n):return Counter(min((y-x)%n,(x-y)%n) for x,y in combinations(points,2))
def correlation(a,b,n,sign=-1):return Counter((x+sign*y)%n for x in a for y in b)
def shifted(p,t,n):return Counter({(x+t)%n:v for x,v in p.items()})
def reflected(p,n):return Counter({(-x)%n:v for x,v in p.items()})

def normalize_input(n,points):
 require(type(n) is int and n>=6,'n must be an integer at least 6')
 points=tuple(points);require(len(points)==6 and all(type(x) is int for x in points),'each endpoint must contain exactly six integers')
 out=tuple(sorted(x%n for x in points));require(len(set(out))==6,'an endpoint has a repeated pitch class')
 return out

def validated_inputs(n,a,b):
 a,b=normalize_input(n,a),normalize_input(n,b)
 require(interval_counter(a,n)==interval_counter(b,n),'endpoints are not homometric')
 ca,wa=canon_witness(a,n);cb,wb=canon_witness(b,n)
 if n<=REFERENCE_LIMIT:
  require(reference_icv(a,n)==reference_icv(b,n),'immutable ICV validation disagrees')
  require(reference_canon(a,n)==ca and reference_canon(b,n)==cb,'immutable T/I validation disagrees')
 return a,b,ca,cb,wa,wb

def alignments(a,b,n):
 seen=set()
 for sign in (1,-1):
  for x in sorted(a):
   for y in sorted(b):
    t=(x-sign*y)%n;bb=frozenset(move(b,n,sign,t))
    if bb not in seen:seen.add(bb);yield bb,sign,t

def bloom_certificate(a,b,n):
 for side,source,target in (('a',a,b),('b',b,a)):
  for anchor,u,v in permutations(sorted(source),3):
   p=(u-anchor)%n;q=(v-anchor+2*p)%n
   X={(anchor+i*p+j*q)%n for i,j in BLOOM_X}
   if X!=source:continue
   Y={(i*p+j*q)%n for i,j in BLOOM_Y}
   for sign in (1,-1):
    for t in sorted(target):
     if move(Y,n,sign,t)==target:return {'label':'Bloom','x_side':side,'p':p,'q':q,'x_shift':anchor,'y_sign':sign,'y_shift':t}
 return None

def dyad_certificate(a,bb,n,sign,shift):
 C=a&bb;left=a-bb;right=bb-a
 if len(C)!=4 or len(left)!=2 or len(right)!=2 or (sum(left)-sum(right))%n:return None
 anchor=min(left);s,t=sorted((x-anchor)%n for x in right);common=sorted((x-anchor)%n for x in C);center=(s+t)%n
 W=Counter(common)+Counter((center-x)%n for x in common)+Counter((0,s,t,center));delta=Counter()
 for c,P in ((1,W),(-1,shifted(W,s,n)),(-1,shifted(W,t,n)),(1,shifted(W,center,n))):
  for x,v in P.items():delta[x]+=c*v
 if any(delta.values()):return None
 return {'label':'D','b_sign':sign,'b_shift':shift,'anchor':anchor,'common':common,'steps':[s,t],'weight':sorted(W.items())}

def halfcoset_certificate(a,b,n):
 """Align B to the DISJOINT coset complement, not to a point of A."""
 a,b=set(a),set(b)
 for order in (2,4,6,12):
  if n%order:continue
  step=n//order;counts=Counter(x%step for x in a)
  if not all(v==order//2 for v in counts.values()):continue
  other={r+j*step for r in counts for j in range(order)}-a
  if len(other)!=6:continue
  anchor=min(other)
  for sign in (1,-1):
   for source in sorted(b):
    t=(anchor-sign*source)%n
    if move(b,n,sign,t)==other:return {'label':'L7','order':order,'b_sign':sign,'b_shift':t}
 return None


def direct_certificate(a,b,n):
 """Search all sufficient direct cases with work bounded by six-point size.

 No subgroup enumeration of size n, n-entry vectors, or n-by-n parameter
 menu occurs here. Recognition completeness follows from the reviewed
 positive-rank branches; the finite branch has a separate path fallback.
 """
 a,b=set(a),set(b)
 c=bloom_certificate(a,b,n)
 if c:return c
 align=list(alignments(a,b,n))
 for bb,sign,t in align:
  c=dyad_certificate(a,bb,n,sign,t)
  if c:return c
 c=halfcoset_certificate(a,b,n)
 if c:return c
 for bb,sign,t in align:
  common=sorted(a&bb)
  for size in range(len(common),0,-1):
   for fixed in combinations(common,size):
    U=set(fixed);V=a-U;Vp=set(bb)-U
    if not V:continue
    P=correlation(U,V,n);Ps=reflected(P,n);anchor=min(V)
    for target in sorted(Vp):
     delta=(target-anchor)%n
     if move(V,n,1,delta)==Vp:
      if shifted(P,delta,n)==P:label='L2'
      elif shifted(P,-delta,n)==Ps:label='L3*'
      elif 2*delta%n==0 and shifted(P+Ps,delta,n)==P+Ps:label='L4'
      else:label=None
      if label:return {'label':label,'b_sign':sign,'b_shift':t,'fixed':sorted(U),'move':delta}
     delta=(target+anchor)%n
     if move(V,n,-1,delta)==Vp and P==shifted(correlation(U,V,n,1),-delta,n):
      return {'label':'L5','b_sign':sign,'b_shift':t,'fixed':sorted(U),'move':delta}
 # Fixed torsion seeds have at most gcd(q,n)<=31 admissible parameters.
 from six_templates import SEEDS
 for index,(q,x,y) in enumerate(SEEDS,1):
  step=n//gcd(n,q)
  for t in range(0,n,step):
   xx={t*z%n for z in x};yy={t*z%n for z in y}
   if len(xx)==len(yy)==6 and sorted((canon(xx,n),canon(yy,n)))==sorted((tuple(sorted(a)),tuple(sorted(b)))):
    return {'label':'R','seed':index,'parameter':t}
 return None

def verify_direct(a,b,n,c):
 """Replay sufficient identities; no discovery search or saved table needed."""
 a,b=set(a),set(b);label=c['label'];require(len(a)==len(b)==6,'certificate endpoints are not six-subsets')
 if label=='Bloom':
  p,q=c['p'],c['q'];X={(c['x_shift']+i*p+j*q)%n for i,j in BLOOM_X};Y={(c['y_shift']+c['y_sign']*(i*p+j*q))%n for i,j in BLOOM_Y}
  require(c['y_sign'] in (-1,1) and c['x_side'] in ('a','b'),'invalid Bloom orientation')
  require((X,Y)==((a,b) if c['x_side']=='a' else (b,a)),'Bloom endpoint mismatch');return
 if label=='R':
  from six_templates import SEEDS
  require(type(c['seed']) is int and 1<=c['seed']<=len(SEEDS),'invalid rigid seed index')
  q,x,y=SEEDS[c['seed']-1];t=c['parameter'];require(q*t%n==0,'seed torsion condition failed')
  xx={t*z%n for z in x};yy={t*z%n for z in y}
  require(len(xx)==len(yy)==6 and sorted((canon(xx,n),canon(yy,n)))==sorted((canon(a,n),canon(b,n))),'seed endpoint mismatch');return
 sign,shift=c['b_sign'],c['b_shift'];require(sign in (-1,1),'invalid rigid sign');bb=move(b,n,sign,shift)
 if label=='D':
  C=set(c['common']);s,t=c['steps'];center=(s+t)%n;origin=c['anchor']
  require(len(C)==4 and len(C|{0,center})==len(C|{s,t})==6,'invalid dyad disjointness')
  require(move(C|{0,center},n,1,origin)==a and move(C|{s,t},n,1,origin)==bb,'dyad endpoint mismatch')
  W=Counter(C)+Counter((center-x)%n for x in C)+Counter((0,s,t,center));require(sorted(W.items())==list(map(tuple,c['weight'])),'dyad weight mismatch')
  delta=Counter()
  for coefficient,P in ((1,W),(-1,shifted(W,s,n)),(-1,shifted(W,t,n)),(1,shifted(W,center,n))):
   for x,v in P.items():delta[x]+=coefficient*v
  require(not any(delta.values()),'dyad mixed-difference condition failed');return
 if label=='L7':
  h=c['order'];require(h in (2,4,6,12) and n%h==0,'invalid halfcoset subgroup');step=n//h;counts=Counter(x%step for x in a)
  require(all(v==h//2 for v in counts.values()),'halfcoset balance failed')
  require({r+j*step for r in counts for j in range(h)}-a==bb,'halfcoset endpoint mismatch');return
 U=set(c['fixed']);V=a-U;require(U and V and U<=a and U<=bb,'invalid fixed block');Vp=bb-U;t=c['move'];P=correlation(U,V,n);Ps=reflected(P,n)
 require(move(V,n,-1 if label=='L5' else 1,t)==Vp,'moving block endpoint mismatch')
 if label=='L2':require(shifted(P,t,n)==P,'L2 periodicity failed')
 elif label=='L3*':require(shifted(P,-t,n)==Ps,'L3* cosymmetry failed')
 elif label=='L4':require(2*t%n==0 and shifted(P+Ps,t,n)==P+Ps,'L4 condition failed')
 elif label=='L5':require(P==shifted(correlation(U,V,n,1),-t,n),'L5 condition failed')
 else:raise ValueError(f'unknown direct certificate label {label}')

@lru_cache(maxsize=2)
def finite_graph(q):
 path=ROOT/f'results/2026-09-30-six-pair-mechanisms/n{q}.json'
 if not path.exists():raise GenerationInvariantError(f'missing proved finite certificate table: {path}')
 report=json.loads(path.read_text());adj=defaultdict(list)
 for c in report['certificates']:
  a,b=tuple(c['a']),tuple(c['b']);adj[a].append((b,c));adj[b].append((a,c))
 return adj

def finite_path(a,b,q):
 graph=finite_graph(q);todo=deque([a]);previous={a:None}
 while todo and b not in previous:
  x=todo.popleft()
  for y,c in graph.get(x,[]):
   if y not in previous:previous[y]=(x,c);todo.append(y)
 if b not in previous:raise GenerationInvariantError(f'proved finite table has no path for validated pair in Z_{q}')
 vertices=[b];edges=[]
 while previous[vertices[-1]] is not None:
  x,c=previous[vertices[-1]];edges.append(c);vertices.append(x)
 return {'modulus':q,'vertices':list(reversed(vertices)),'edges':list(reversed(edges))}

def verify_saved(c,q):
 """Replay the immutable FT schema, preserving its original label semantics."""
 a,b=tuple(c['a']),tuple(c['b']);label=c['label']
 require(len(set(a))==len(set(b))==6 and a!=b and canon(a,q)==a and canon(b,q)==b,'invalid finite endpoint')
 if label=='Bloom':
  p,t=c['parameters'];x={(i*p+j*t)%q for i,j in BLOOM_X};y={(i*p+j*t)%q for i,j in BLOOM_Y}
  require(len(x)==len(y)==6 and sorted((canon(x,q),canon(y,q)))==[a,b],'finite Bloom mismatch')
 elif label=='R':
  index,t=c['parameters'];verify_direct(a,b,q,{'label':'R','seed':index,'parameter':t})
 elif label=='unit':
  u=c['u'];require(gcd(u,q)==1 and canon((u*x%q for x in a),q)==b,'finite unit mismatch');P=correlation(a,a,q)
  require(P==Counter({u*x%q:v for x,v in P.items()}),'finite unit autocorrelation mismatch')
 elif label=='halfcoset':
  h=c['h'];require(h in (2,4,6,12) and q%h==0,'invalid finite subgroup');step=q//h;counts=Counter(x%step for x in a)
  require(all(v==h//2 for v in counts.values()),'finite halfcoset balance failed');partner={r+j*step for r in counts for j in range(h)}-set(a)
  require(len(partner)==6 and canon(partner,q)==b,'finite halfcoset endpoint mismatch')
 else:
  number,sign,t,mask,v=c['certificate'];labels={1:'translate',2:'swap',3:'halfturn',4:'reflect',5:'dyad'}
  require(labels.get(number)==label and type(mask) is int and 0<mask<64,'finite block label or mask mismatch');U={x for i,x in enumerate(a) if mask>>i&1};bb=move(b,q,sign,t)
  if label=='dyad':
   direct=dyad_certificate(set(a),bb,q,sign,t);require(direct is not None and U==set(a)&bb,'finite dyad mismatch');verify_direct(a,b,q,direct)
  else:
   if label=='swap':require(q%2==1 or v%2==0,'legacy L3 halving condition failed')
   if label=='halfturn':require(q%2==0 and v==q//2,'legacy L4 halfturn condition failed')
   verify_direct(a,b,q,{'label':{'translate':'L2','swap':'L3*','halfturn':'L4','reflect':'L5'}[label],'b_sign':sign,'b_shift':t,'fixed':sorted(U),'move':v})
 require(interval_counter(a,q)==interval_counter(b,q),'finite endpoint homometry mismatch')
 return a,b

def generate(n,a,b,prefer_finite=False):
 a,b,ca,cb,wa,wb=validated_inputs(n,a,b);g=gcd(n,*ca,*cb);q=n//g
 result={'schema':'six-generation-v1','n':n,'input_a':a,'input_b':b,'a':ca,'b':cb,'input_alignment_a':wa,'input_alignment_b':wb,'ordinary_support':{'modulus':q,'scale':g},'validation':'immutable-reference' if n<=REFERENCE_LIMIT else 'exact-sparse-intervals-and-anchored-TI'}
 if ca==cb:result.update(route='TI',certificate=None)
 elif prefer_finite and q<=135:result.update(route='finite_path',path=finite_path(tuple(x//g for x in ca),tuple(x//g for x in cb),q))
 else:
  c=direct_certificate(ca,cb,n)
  if c:result.update(route='direct',certificate=c)
  elif q<=135:result.update(route='finite_path',path=finite_path(tuple(x//g for x in ca),tuple(x//g for x in cb),q))
  else:raise GenerationInvariantError(f'validated homometric pair in Z_{n} with ordinary support {q} lacks its required direct certificate; this is an implementation/proof invariant failure, not a nonhomometry decision')
 result['vertices']=replay(result)
 return result

def exact_certificate_data(value):
 """Portable certificates contain integer arithmetic, never float inputs."""
 if value is None or type(value) in (int,str):return True
 if isinstance(value,(list,tuple)):return all(exact_certificate_data(x) for x in value)
 if isinstance(value,dict):return all(type(k) is str and exact_certificate_data(v) for k,v in value.items())
 return False

def checked_vertices(c,vertices):
 if 'vertices' in c:require(list(map(tuple,c['vertices']))==vertices,'advertised path vertices differ from executable certificate')
 return vertices

def replay(c):
 """Check a portable certificate and return its actual ambient T/I path.

 The finite edge records are embedded in c, so replay does not load the
 finite tables. Independent endpoint rigid alignments recover the exact
 input sets; returned intermediate vertices preserve T/I classes.
 """
 require(exact_certificate_data(c),'certificate contains noninteger arithmetic data')
 require(c.get('schema')=='six-generation-v1','unsupported certificate schema');n=c['n'];a=tuple(c['a']);b=tuple(c['b'])
 aa,bb,ca,cb,wa,wb=validated_inputs(n,c['input_a'],c['input_b'])
 require(ca==a and cb==b,'canonical endpoint mismatch')
 for name,points,target in (('a',aa,a),('b',bb,b)):
  w=c['input_alignment_'+name];require(w['sign'] in (-1,1) and tuple(sorted(move(points,n,w['sign'],w['shift'])))==target,'input alignment mismatch')
 g=gcd(n,*a,*b);q=n//g;require(c['ordinary_support']=={'modulus':q,'scale':g},'ordinary support mismatch')
 if c['route']=='TI':require(a==b,'false T/I certificate');return checked_vertices(c,[a])
 if c['route']=='direct':verify_direct(a,b,n,c['certificate']);return checked_vertices(c,[a,b])
 require(c['route']=='finite_path','unknown certificate route');path=c['path'];require(path['modulus']==q and q<=135,'invalid finite support modulus')
 vertices=list(map(tuple,path['vertices']));require(vertices and len(vertices)==len(path['edges'])+1,'invalid path length')
 require(vertices[0]==tuple(x//g for x in a) and vertices[-1]==tuple(x//g for x in b),'finite path endpoint mismatch')
 for x,y,edge in zip(vertices,vertices[1:],path['edges']):require(set(verify_saved(edge,q))=={x,y},'finite path edge mismatch')
 return checked_vertices(c,[tuple(g*x for x in v) for v in vertices])

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('n',type=int,nargs='?');p.add_argument('a',nargs='?',help='six comma-separated integers');p.add_argument('b',nargs='?',help='six comma-separated integers');p.add_argument('--replay',type=Path,help='verify an existing portable JSON certificate');p.add_argument('--prefer-finite',action='store_true',help='use the saved finite-family path whenever the ordinary support is at most135');p.add_argument('--out',type=Path)
 args=p.parse_args()
 if args.replay:
  r={'verified':True,'vertices':replay(json.loads(args.replay.read_text()))}
 else:
  if args.n is None or args.a is None or args.b is None:p.error('provide n, A, B, or --replay CERTIFICATE.json')
  r=generate(args.n,map(int,args.a.split(',')),map(int,args.b.split(',')),args.prefer_finite)
 text=json.dumps(r,indent=2)+'\n'
 if args.out:args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(text)
 else:print(text,end='')
if __name__=='__main__':main()
