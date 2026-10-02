"""Adversarial extra controls for the three-dyad branch.

The full 663552-case coverage audit is tests/test_six_three_dyads.py.
This separate test checks the intended free-height maps, all torsion
characters of the two obstruction groups, and immutable-reference images.
"""
from collections import Counter
from itertools import product
from math import lcm
from pathlib import Path
import gzip,json,sys,time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from homometry import icv
BASE=ROOT/'results/2026-09-30-six-three-dyads'

def main():
 start=time.monotonic()
 with gzip.open(BASE/'cyclic-presentations.json.gz','rt') as f:records=json.load(f)
 checks=0;collisions=0;binary_by_orbit=Counter()
 for r in records:
  # Every relation annihilates both independent, labelled free-height maps.
  for height in ((0,0,1,1,0,0),(0,0,0,0,1,1)):
   for i,j,k,l,s in r['labels']:assert height[j]-height[i]==s*(height[l]-height[k])
  if r['classification']=='cyclic_collision':
   assert r['orders']==[2,2,0,0]
   # All four maps C2^2 -> Q/Z, retaining BOTH free coordinates.
   for c in product(range(2),repeat=2):
    aa=[((c[0]*p[0]+c[1]*p[1])%2,*p[2:]) for p in r['a']]
    bb=[((c[0]*p[0]+c[1]*p[1])%2,*p[2:]) for p in r['b']]
    assert len(set(aa))<6 or len(set(bb))<6;collisions+=1
  if r['classification'] not in ('L2','L4'):continue
  orders=r['orders'];T=[d for d in orders if d];exponent=lcm(*T);free=orders.count(0)
  # Enumerate each torsion character at several cyclic embedding sizes,
  # with reproducible free-coordinate maps (these are controls, not proof).
  for size in (3,5,7):
   n=exponent*size
   for chars in product(*(range(d) for d in T)):
    for seed in range(12):
     co=[c*(n//d) for c,d in zip(chars,T)]+[(seed+2)**(j+1)+j for j in range(free)]
     a=sorted({sum(x*y for x,y in zip(p,co))%n for p in r['a']});b=sorted({sum(x*y for x,y in zip(p,co))%n for p in r['b']})
     if len(a)==len(b)==6:
      assert icv(a,n)==icv(b,n);checks+=1;binary_by_orbit[r['orbit']]+=1
 assert len(records)==1495 and collisions==8 and checks>100
 result={'status':'COMPUTED separate adversarial controls passed','height_map_checks':2*len(records),'cyclic_obstruction_characters':collisions,'immutable_reference_specializations':checks,'mechanism_orbits_with_binary_controls':len(binary_by_orbit),'seconds':time.monotonic()-start}
 (BASE/'adversarial-controls.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
if __name__=='__main__':main()
