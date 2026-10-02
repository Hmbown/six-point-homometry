"""Independent exterior-coordinate audit of rank-three/four orbit growth."""
from itertools import combinations,permutations
from collections import Counter
from math import factorial,gcd
from pathlib import Path
import json,sys,time
import test_six_shadow_review as independent
from test_six_free_rank import directions,normalize
ROOT=Path(__file__).resolve().parents[1]


def exterior(rows):
    r=len(rows)
    return normalize(tuple(independent.determinant([[row[j] for j in columns] for row in rows])
                           for columns in combinations(range(6),r)))

def actions(rank):
    subsets=list(combinations(range(6),rank));lookup={s:i for i,s in enumerate(subsets)};out=[]
    for perm in permutations(range(6)):
        mapping=[]
        for s in subsets:
            values=[perm[i] for i in s];inversions=sum(values[i]>values[j] for i in range(rank) for j in range(i+1,rank))
            mapping.append((lookup[tuple(sorted(values))],(-1)**inversions))
        out.append(mapping)
    return out

def act(vector,action):
    v=tuple(vector[i]*sign for i,sign in action)
    if next(x for x in v if x)<0:v=tuple(-x for x in v)
    return v


def main():
    base=ROOT/'results/2026-09-30-six-free-rank';previous=json.loads((base/'spans.json').read_text())['orbits'];result={};started=time.monotonic()
    for rank in (3,4):
        saved=json.loads((base/f'rank{rank}-orbits.json').read_text());covered=set();maps=actions(rank)
        for orbit in saved['orbits']:
            seed=exterior(orbit['rows']);assert seed
            group={act(seed,a) for a in maps}
            assert len(group)==orbit['size'] and not group&covered;covered|=group
            h=orbit['heights'];assert not any(sum(x*y for x,y in zip(row,h)) for row in orbit['rows'])
            counts=Counter(abs(h[j]-h[i]) for i,j in combinations(range(6),2))
            number=1
            for distance,count in counts.items():number*=factorial(count)*(2**count if distance==0 else 1)
            assert number==orbit['matching_count']
            assert sorted(Counter(h).values())==orbit['height_multiplicities']
            for d in directions():
                belongs=len(independent.rational_pivots(orbit['rows']+[list(d)]))==rank
                assert (sum(x*y for x,y in zip(d,h))==0)==belongs
        candidates={exterior(row['rows']+[list(d)]) for row in previous if len(row['rows'])==rank-1 for d in directions()}
        candidates.discard(())
        assert candidates<=covered and len(candidates)==saved['extension_candidates']
        # Every stored orbit must meet the exhaustive extension list.
        for orbit in saved['orbits']:
            seed=exterior(orbit['rows']);assert any(act(seed,a) in candidates for a in maps)
        assert len(covered)==saved['spans']
        total=sum(r['matching_count'] for r in saved['orbits']);assert total==saved['total_matchings']
        result[rank]=dict(spans=len(covered),orbits=len(saved['orbits']),total_matchings=total,
                          largest=max(r['matching_count'] for r in saved['orbits']))
        print('PASS',rank,result[rank],flush=True);previous=saved['orbits']
    result['seconds']=time.monotonic()-started
    (base/'growth-verification.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
