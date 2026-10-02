"""Separate exact review of all terminal mechanisms in the low-rank cover.

No builder, recognizer, SymPy, or normal-form implementation is imported.
The orbit/root/branch cover is reviewed separately by the root agent.
"""
from collections import Counter
from itertools import combinations,product
from math import gcd,lcm
from pathlib import Path
import gzip,hashlib,json,sys,time
from test_six_cylinder_branches_review import linear,autocorrelation
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'results/2026-09-30-six-free-dag-all';OUT=ROOT/'results/2026-09-30-six-low-rank-review'
X=((0,0),(1,0),(-2,1),(-2,2),(0,2),(-1,3))
Y=((0,0),(1,0),(2,1),(-1,2),(1,2),(-1,3))

def translate(S,sign,t,orders):return {linear([(sign,x),(1,t)],orders) for x in S}
def shift(P,t,orders):return Counter({linear([(1,x),(1,t)],orders):v for x,v in P.items()})
def star(P,orders):return Counter({linear([(-1,x)],orders):v for x,v in P.items()})
def convolve(A,B,sign,orders):return Counter(linear([(1,x),(sign,y)],orders) for x in A for y in B)

def mechanism(rec,cert):
 orders=tuple(rec['torsion'])+(0,)*(len(rec['a'][0])-len(rec['torsion']));a=set(map(tuple,rec['a']));b=set(map(tuple,rec['b']));zero=(0,)*len(orders)
 assert len(a)==len(b)==6 and autocorrelation(a,orders)==autocorrelation(b,orders)
 kind=cert['type']
 if kind=='Bloom':
  c=cert['certificate'];p,q=c['p'],c['q'];sx,sy=c['shift_x'],c['shift_y'];sign=c['sign_y']
  xx=Counter(linear([(1,sx),(u,p),(v,q)],orders) for u,v in X)
  yy=Counter(linear([(1,sy),(sign*u,p),(sign*v,q)],orders) for u,v in Y)
  assert sign in (-1,1) and c['x_side'] in ('a','b')
  assert (xx,yy)==((Counter(a),Counter(b)) if c['x_side']=='a' else (Counter(b),Counter(a)))
  return kind
 bb=translate(b,cert['alignment_sign'],cert['alignment_shift'],orders);assert cert['alignment_sign'] in (-1,1)
 if kind=='D-dyad':
  C=set(map(tuple,cert['common']));anchor=cert['anchor'];s,t=cert['steps'];center=linear([(1,s),(1,t)],orders)
  assert len(C)==4 and C.isdisjoint((zero,center)) and C.isdisjoint((tuple(s),tuple(t)))
  assert zero!=center and tuple(s)!=tuple(t)
  assert translate(C|{zero,center},1,anchor,orders)==a
  assert translate(C|{tuple(s),tuple(t)},1,anchor,orders)==bb
  W=Counter(C)+Counter(linear([(1,center),(-1,x)],orders) for x in C)+Counter((zero,tuple(s),tuple(t),center))
  assert sum(W.values())==12
  mixed=Counter()
  for coefficient,P in ((1,W),(-1,shift(W,s,orders)),(-1,shift(W,t,orders)),(1,shift(W,center,orders))):
   for x,v in P.items():mixed[x]+=coefficient*v
  assert all(v==0 for v in mixed.values())
  return kind
 U=set(map(tuple,cert['fixed']));V=set(map(tuple,cert['moving']));t=cert['move']
 assert U and V and U.isdisjoint(V) and U|V==a
 P=convolve(U,V,-1,orders);Ps=star(P,orders)
 if kind=='L2-translate':assert shift(P,t,orders)==P
 elif kind=='L3star-cosymmetric':assert shift(P,linear([(-1,t)],orders),orders)==Ps
 elif kind=='L4-halfturn':assert linear([(2,t)],orders)==zero and shift(P+Ps,t,orders)==P+Ps
 elif kind=='L5-reflect':assert P==shift(convolve(U,V,1,orders),linear([(-1,t)],orders),orders)
 else:raise AssertionError(kind)
 moved=translate(V,-1 if kind=='L5-reflect' else 1,t,orders)
 assert U.isdisjoint(moved) and U|moved==bb
 return kind

def characters(rec,cover):
 torsion=rec['torsion'];exponent=lcm(*torsion);expected=set(product(*(range(d) for d in torsion)))
 assert len(cover)==len(expected) and {tuple(q['character']) for q in cover}==expected
 hist=Counter()
 for q in cover:
  coefficients=[k*(exponent//d) for k,d in zip(q['character'],torsion)];common=gcd(exponent,*coefficients);order=exponent//common
  assert q['image_order']==order and q['torsion']==([order] if order>1 else [])
  for side in ('a','b'):
   image=[(([sum(k*x for k,x in zip(coefficients,p))%exponent//common] if order>1 else [])+p[len(torsion):]) for p in rec[side]]
   assert image==q[side]
  if 'collision' in q:
   c=q['collision'];i,j=c['indices'];assert c['side'] in ('a','b') and i!=j and q[c['side']][i]==q[c['side']][j];hist['collision']+=1
  elif 'ti' in q:
   c=q['ti'];orders=tuple(q['torsion'])+(0,)*(len(q['a'][0])-len(q['torsion']))
   assert translate(q['a'],c['sign'],c['shift'],orders)==set(map(tuple,q['b']));hist['ti']+=1
  else:hist[mechanism(q,q['mechanism'])]+=1
 return hist

def builder_mechanism(row):
 orders=tuple(row['orders']);a=set(map(tuple,row['a']));b=set(map(tuple,row['b']));c=row['certificate'];kind=c['label']
 if kind=='collision':assert len(a)<6 or len(b)<6;return kind
 if kind=='ti':assert translate(b,c['b_sign'],c['b_shift'],orders)==a;return kind
 assert len(a)==len(b)==6 and autocorrelation(a,orders)==autocorrelation(b,orders)
 rec={'a':row['a'],'b':row['b'],'torsion':[d for d in orders if d]}
 if kind=='halfcoset':
  h=c['generator'];d=c['order'];zero=(0,)*len(orders)
  H={linear([(i,h)],orders) for i in range(d)}
  assert d in (2,4,6,12) and len(H)==d and linear([(d,h)],orders)==zero
  whole={linear([(1,x),(1,t)],orders) for x in a for t in H}
  assert len(whole)==12
  for x in a:assert len(translate(H,1,x,orders)&a)==d//2
  assert translate(b,c['b_sign'],c['b_shift'],orders)==whole-a
  return kind
 if kind=='Bloom':
  cert={'type':'Bloom','certificate':{'x_side':'a','p':c['p'],'q':c['q'],'shift_x':c['anchor'],'shift_y':linear([(-c['b_sign'],c['b_shift'])],orders),'sign_y':c['b_sign']}}
 else:
  names={'dyad':'D-dyad','translate':'L2-translate','cosymmetric_translate':'L3star-cosymmetric','halfturn':'L4-halfturn','reflect':'L5-reflect'}
  cert={'type':names[kind],'alignment_sign':c['b_sign'],'alignment_shift':c['b_shift']}
  if kind=='dyad':cert.update(anchor=c['anchor'],common=c['common'],steps=c['steps'])
  else:
   U=set(map(tuple,c['common']));cert.update(fixed=c['common'],moving=sorted(a-U),move=c['move'])
 mechanism(rec,cert)
 return kind


def builder_atlas(expected):
 path=ROOT/'results/2026-09-30-six-free-mechanisms/atlas.json';atlas=json.loads(path.read_text());keyed={}
 for r in atlas['records']:
  left,right=r['stratum'].split('-orbit');key=(int(left[4:]),int(right),r['node']);assert key not in keyed;keyed[key]=r
 assert set(keyed)==set(expected)
 hist=Counter();qh=Counter()
 for key,rec in expected.items():
  row=keyed[key];assert row['a']==rec['a'] and row['b']==rec['b'] and row['orders']==rec['torsion']+[0]*rec['free_rank']
  if row['certificate']['label']!='template':hist[builder_mechanism(row)]+=1;continue
  hist['template']+=1;T=rec['torsion'];e=lcm(*T);cover=row['cyclic_quotients']
  wanted=set(product(*(range(d) for d in T)))
  assert len(cover)==len(wanted) and {tuple(q['character']) for q in cover}==wanted
  for q in cover:
   coefficients=[k*(e//d) for k,d in zip(q['character'],T)];common=gcd(e,*coefficients);order=e//common
   assert q['coefficients']==coefficients and q['exponent']==e and q['image_order']==order
   assert q['orders']==([order] if order>1 else [])+[0]*rec['free_rank']
   for side in ('a','b'):
    image=[(([sum(k*x for k,x in zip(coefficients,p))%e//common] if order>1 else [])+p[len(T):]) for p in rec[side]]
    assert image==q[side]
   qh[builder_mechanism(q)]+=1
 assert dict(hist)==atlas['histogram'] and dict(qh)==atlas['cyclic_quotient_histogram']
 return {'direct':dict(hist),'characters':dict(qh),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}


def halfcoset_degeneration_controls():
 # Enumerate every half-subset for loss-of-order tests.  Enumerate every
 # possible merger partition (blocks of size<=2) and half-subset choice
 # for the six-note occupied-coset cases; integer coset labels remain distinct.
 def partitions(items):
  if not items:yield [];return
  first,*tail=items
  for rest in partitions(tail):yield [(first,)]+rest
  for j,other in enumerate(tail):
   for rest in partitions(tail[:j]+tail[j+1:]):yield [(first,other)]+rest
 losses=mergers=0
 for m in (2,4,6,12):
  half=list(map(set,combinations(range(m),m//2)));allH=set(range(m))
  for multiplier in range(m):
   if gcd(multiplier,m)==1:continue
   for A in half:
    B=allH-A;aa={multiplier*x%m for x in A};bb={multiplier*x%m for x in B}
    if len(aa)==len(bb)==m//2:assert aa==bb;losses+=1
  k=12//m
  if k==1:continue
  for partition in partitions(list(range(k))):
   if len(partition)==k:continue
   for choices in product(half,repeat=k):
    aa=set();bb=set()
    for target,cluster in enumerate(partition):
     for source in cluster:
      aa.update((target,x) for x in choices[source]);bb.update((target,x) for x in allH-choices[source])
    if len(aa)==len(bb)==6:
     assert any({(c,(x+t)%m) for c,x in aa}==bb for t in range(m));mergers+=1
 return {'loss_of_subgroup_order_cases':losses,'occupied_coset_merger_cases':mergers,'outcome':'all injective endpoint degenerations are globally T/I'}


def main():
 start=time.monotonic();path=OUT/'exploratory-mechanisms.json';report=json.loads(path.read_text());saved={(r['rank'],r['orbit'],r['node']):r for r in report['rows']};assert len(saved)==len(report['rows'])
 summary=json.loads((BASE/'summary.json').read_text());expected={};group_counter=Counter()
 for s in summary['strata']:
  with gzip.open(BASE/f'rank{s["rank"]}-orbit{s["orbit"]:03}.json.gz','rt') as f:dag=json.load(f)
  assert dag['complete']
  for node in dag['nodes']:
   if node.get('terminal')=='homometric':expected[(s['rank'],s['orbit'],node['id'])]=node
 assert set(saved)==set(expected) and len(expected)==620
 hist=Counter();qh=Counter()
 for key,rec in expected.items():
  row=saved[key]
  if row['mechanism']:hist[mechanism(rec,row['mechanism'])]+=1
  else:hist['cyclic-character-cover']+=1;qh.update(characters(rec,row['cyclic_cover']))
 assert hist==Counter({'D-dyad':481,'L5-reflect':71,'L3star-cosymmetric':24,'L4-halfturn':20,'Bloom':14,'L2-translate':1,'cyclic-character-cover':9})
 assert qh==Counter({'collision':44,'D-dyad':16})
 report['status']='VERIFIED exact sufficient group identities and exhaustive cyclic-character covers'
 final=OUT/'mechanism-certificates.json';final.write_text(json.dumps(report,sort_keys=True)+'\n')
 result={'status':'COMPUTED separate exact mechanism audit passed; completeness cover audited separately','strata':len(summary['strata']),'terminals':len(expected),'direct':dict(hist),'cyclic_characters':dict(qh),'seconds':time.monotonic()-start,'certificate_sha256':hashlib.sha256(final.read_bytes()).hexdigest(),'independent_builder_atlas':builder_atlas(expected),'halfcoset_degenerations':halfcoset_degeneration_controls()}
 (OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(result,flush=True)
if __name__=='__main__':main()
