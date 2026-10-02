"""Weighted-six boundary identity, exact finite multiset check, SMT control."""
import sys,subprocess
from pathlib import Path
from itertools import combinations,combinations_with_replacement
from collections import Counter,defaultdict
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from six_integer_smt import encode,NORMAL_FORMS
sys.path.insert(0,str(Path(__file__).resolve().parent))
from test_six_integer_smt import canon,oriented,member,solver,fixed

def weighted_text(exclude=True):
 s,_=encode(timeout_ms=20000,exclude_bloom=exclude)
 for pts in [('0','a1','a2','a3','r','1'),('0','b1','b2','b3','r','1')]:
  for x,y in zip(pts,pts[1:]):s=s.replace(f'(assert (< {x} {y}))',f'(assert (<= {x} {y}))')
 return s

def main():
 a=(0,1,3,3,7,8);b=(0,2,4,7,7,8)
 assert Counter(y-x for x,y in combinations(a,2))==Counter(y-x for x,y in combinations(b,2))
 assert len(set(a))==len(set(b))==5
 assert solver(fixed(weighted_text(False),a,b))=='sat'
 assert solver(fixed(weighted_text(),a,b))=='unsat'
 assert solver(weighted_text())=='unsat'
 cases=0
 for L in range(1,15):
  table=defaultdict(set)
  for middle in combinations_with_replacement(range(L+1),4):
   a=(0,*middle,L);a=canon(a)
   table[tuple(sorted(y-x for x,y in combinations(a,2)))].add(a)
  for g in table.values():
   for a,b in combinations(g,2):
    assert member(oriented(a),oriented(b))
    assert len(set(a))>=5 and len(set(b))>=5
    if len(set(a))<6 or len(set(b))<6:
     def primitive(v):
      from math import gcd
      from functools import reduce
      d=reduce(gcd,v);return canon(tuple(x//d for x in v))
     assert set((primitive(a),primitive(b)))=={canon((0,1,3,3,7,8)),canon((0,2,4,7,7,8))}
    cases+=1
 print('PASS weighted boundary, SMT nonvacuity, and exact integer multiset cases',cases)
if __name__=='__main__':main()
