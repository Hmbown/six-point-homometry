"""Independent orbit coverage and honest bounded-run controls for exploration."""
from pathlib import Path
from itertools import permutations,combinations,product
import json,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from six_star_quotient import stars,search

def check():
    data=stars();covered=set()
    for row in data:
        # Reconstruct the action as actual ordered vertex pairs, with all
        # 720 vertex permutations, rather than production adjacent swaps.
        edges=list(combinations(range(6),2));seed=[]
        for k in row['star']:
            e=edges[k//2];seed.append(e[::-1] if k%2 else e)
        orbit=set()
        for p in permutations(range(6)):
            for sign in (1,-1):
                image=tuple(sorted((p[a],p[b]) if sign==1 else (p[b],p[a]) for a,b in seed));orbit.add(image)
        assert len(orbit)==row['size'] and not (orbit&covered)
        covered|=orbit
    raw=set()
    for edges in combinations(list(combinations(range(6),2)),5):
        for signs in product((0,1),repeat=5):raw.add(tuple(sorted(e[::-1] if s else e for e,s in zip(edges,signs))))
    assert covered==raw and len(data)==107 and len(raw)==96096
    with tempfile.TemporaryDirectory(prefix='six-star-test-') as d:
        result=search(data[:1],10,10,Path(d));assert result['complete'] and result['completed_roots']==1
        result=search(data[:7],100,10,Path(d));assert not result['complete'] and result['nodes']==100
    print('PASS independent107-star/96096 coverage and bounded-completeness controls')

if __name__=='__main__':check()
