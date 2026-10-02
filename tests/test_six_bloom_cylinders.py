"""Production smoke/soundness tests; exhaustive attack is separate."""
from pathlib import Path
import sys,json
from collections import Counter
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from six_bloom_cylinders import critical_slopes,expected,group_linear
from six_integer_smt import X,Y
from homometry import icv

def main():
 assert critical_slopes(1)==[F(3),F(4),F(5)]
 assert critical_slopes(2)==[F(3,2),F(5,3)]
 assert sum(expected(k,s) for k in (1,2) for s in [None,*critical_slopes(k)])==282
 d=json.loads(Path('results/2026-09-30-six-bloom-cylinders.json').read_text())
 count=0
 for row in d['presentations']:
  r=row['presentation']
  if not r['six_distinct_in_presentation']:continue
  c=r['bloom_certificate'];p,q=c['p'],c['q'];mod=r['torsion_factors']
  def lin(*terms):return group_linear(terms,mod)
  xx=Counter(lin((1,c['shift_x']),(u,p),(v,q)) for u,v in X)
  yy=Counter(lin((1,c['shift_y']),(c['sign_y']*u,p),(c['sign_y']*v,q)) for u,v in Y)
  sides={'a':r['a'],'b':r['b']}
  assert xx==Counter(map(tuple,sides[c['x_side']]))
  assert yy==Counter(map(tuple,sides['b' if c['x_side']=='a' else 'a']))
  count+=1
 assert count==19
 # Nonzero order-two parameter, checked against immutable cyclic ICV.
 tested=0
 for n in range(12,81,2):
  h=n//2
  for g in range(1,n):
   a=tuple(x%n for x in [0,g,3*g,3*g+h,7*g,8*g+h]);b=tuple(x%n for x in [0,2*g+h,4*g+h,7*g,7*g+h,8*g+h])
   if len(set(a))==len(set(b))==6:
    assert icv(a,n)==icv(b,n);tested+=1
 print('PASS slopes/count,19 exact group Bloom certificates,reference cyclic instances',tested)
if __name__=='__main__':main()
