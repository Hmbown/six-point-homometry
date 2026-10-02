"""Reference and bit-boundary checks for the extended six-only census."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from six_large_census import run
from homometry import z_families,dihedral_canon,icv

for n in range(6,23):
    a,ast,_=run(n,'gap');b,bst,_=run(n,'point')
    reference=sorted(sorted(tuple(s) for s in f) for f in z_families(n,sizes=[6]).values())
    assert a==b==reference,n
    assert ast['classes']==bst['classes'],n
for n in (31,32,33,60,63,64,65):
    a,ast,_=run(n,'gap');b,bst,_=run(n,'point')
    assert a==b and ast['classes']==bst['classes'],n
    for family in a:
        assert len({icv(s,n) for s in family})==1
        assert all(s==dihedral_canon(s,n) for s in family)
print('PASS two six-only traversals, immutable reference6..22, and boundaries31..33/63..65')
