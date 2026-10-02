"""Independent certificate audit for the thirteen rigid cyclic templates.

The matrix and matching checker is the prior fresh-context review's exact
implementation; it imports none of the production six-point mechanisms.
Coverage is checked by graph reachability rather than production union-find.
"""
from __future__ import annotations
from collections import Counter
from itertools import combinations
import json
from math import gcd
from pathlib import Path
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from homometry import icv as reference_icv, dihedral_canon
import test_six_shadow_review as independent
from six_templates import SEEDS, transported_pair, seed_edges


def matmul(a,b):
    bt=list(zip(*b))
    return [[sum(x*y for x,y in zip(row,col)) for col in bt] for row in a]


def test_all_presentations():
    saved=json.loads((ROOT/'results/2026-09-30-six-templates/smith.json').read_text())
    total=0
    for seed,(q,a,b) in zip(saved['seeds'],SEEDS):
        assert (seed['q'],tuple(seed['a']),tuple(seed['b']))==(q,a,b)
        expected={tuple(sorted(labels)) for labels in independent.independent_matchings(a,b,q)}
        got=set()
        for cert in seed['certificates']:
            labels=tuple(tuple(row) for row in cert['labels'])
            got.add(tuple(sorted(labels)))
            m=independent.matching_matrix(labels)
            assert m==cert['matrix']
            u,v=cert['left'],cert['right']
            assert abs(independent.determinant(u))==abs(independent.determinant(v))==1
            target=[[int(i==j)*(q if i==9 else 1) for j in range(10)] for i in range(15)]
            assert matmul(matmul(u,m),v)==target
            w=[row[9] for row in v]
            assert w==cert['generator']
            scalar=cert['normalizing_scalar']
            vector=list(a[1:])+list(b[1:])
            assert [x*scalar%q for x in w]==vector
            assert gcd(w[0],q)==1
            assert independent.rational_pivots(m)==tuple(range(10))
        assert got==expected and len(got)==len(seed['certificates'])
        assert len(got)==seed['matchings']
        total+=len(got)
    assert total==saved['total_matchings']==536
    return dict(seeds=len(saved['seeds']),exact_matchings=total,
                unimodular_matrix_identities=total)


def test_transports_and_projections():
    checks=0
    for i,(q,a,b) in enumerate(SEEDS):
        for n in range(1,151):
            independent_edges=set()
            for t in range(n):
                if q*t%n:continue
                aa,bb={t*x%n for x in a},{t*x%n for x in b}
                expected=None
                if len(aa)==len(bb)==6:
                    assert reference_icv(aa,n)==reference_icv(bb,n)
                    ca,cb=dihedral_canon(aa,n),dihedral_canon(bb,n)
                    if ca!=cb:expected=tuple(sorted((ca,cb)))
                assert transported_pair(i,n,t)==expected
                checks+=1
            # Faithful inflation transports pure cyclicity, with no coordinate cap.
        valid=[d for d in range(1,q+1) if q%d==0 and transported_pair(i,d,1)]
        saved=json.loads((ROOT/'results/2026-09-30-six-templates/smith.json').read_text())
        assert valid==saved['seeds'][i]['nontrivial_image_orders']
    return dict(reference_transport_checks=checks,max_n=150)


def test_residual_coverage():
    saved=json.loads((ROOT/'results/2026-09-30-six-templates/inventory.json').read_text())
    total=0;counts=[];seed_hits=Counter()
    for n in range(12,61):
        inventory=json.loads((ROOT/f'results/2026-09-30-six-inventory/n{n}.json').read_text())
        shell=json.loads((ROOT/f'results/2026-09-30-six-shell/n{n}.json').read_text())
        shape={frozenset((tuple(e['x']),tuple(e['y']))) for e in shell['pairs']}
        forward={}
        for i,(q,a,b) in enumerate(SEEDS,1):
            for t in range(n):
                if q*t%n:continue
                aa,bb={t*x%n for x in a},{t*x%n for x in b}
                if len(aa)!=6 or len(bb)!=6:continue
                pair=tuple(sorted((dihedral_canon(aa,n),dihedral_canon(bb,n))))
                if pair[0]!=pair[1]:forward.setdefault(pair,set()).add(i)
        assert set(forward)==set(seed_edges(n))
        gaps=[]
        for family in inventory['families']:
            mm=list(map(tuple,family['members']));adj={a:set() for a in mm}
            pairs={frozenset((tuple(e['a']),tuple(e['b']))) for e in family['strict_edges']+family['bloom_edges']}
            pairs|={frozenset((a,b)) for a,b in combinations(mm,2) if frozenset((a,b)) in shape}
            for a,b in map(tuple,pairs):adj[a].add(b);adj[b].add(a)
            def reach(a):
                found={a};todo=[a]
                while todo:
                    x=todo.pop()
                    for y in adj[x]-found:found.add(y);todo.append(y)
                return found
            for a,b in combinations(mm,2):
                if b not in reach(a):
                    gaps.append((a,b));assert (a,b) in forward
                    for i in forward[a,b]:seed_hits[i]+=1
            for a,b in combinations(mm,2):
                if (a,b) in forward:adj[a].add(b);adj[b].add(a)
            assert reach(mm[0])==set(mm)
        row=next(row for row in saved['by_n'] if row['n']==n)
        assert gaps==[(tuple(e['a']),tuple(e['b'])) for e in row['gaps']]
        assert row['remaining_families']==0 and row['residual_pairs']==len(gaps)
        total+=len(gaps)
        if gaps:counts.append([n,len(gaps)])
    assert len(saved['groups'])==13
    assert {(r['q'],tuple(r['a']),tuple(r['b'])) for r in saved['groups']}==set(SEEDS)
    assert sum(len(x['occurrences']) for x in saved['groups'])==total==186
    return dict(nmin=12,nmax=60,residual_pairs=total,seed_groups=13,
                by_n=counts,seed_hits=dict(sorted(seed_hits.items())),remaining_families=0,
                limitation='Coverage relative to inherited strict/Bloom/dyad labels; does not independently redo strict discovery.')


def main():
    started=time.monotonic();results={}
    for fn in (test_all_presentations,test_transports_and_projections,test_residual_coverage):
        results[fn.__name__]=fn();print('PASS',fn.__name__,results[fn.__name__],flush=True)
    results['seconds']=round(time.monotonic()-started,3)
    (ROOT/'results/2026-09-30-six-templates/verification.json').write_text(json.dumps(results,sort_keys=True,indent=2)+'\n')

if __name__=='__main__':main()
