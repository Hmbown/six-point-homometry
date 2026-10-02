"""Six-note inventory certificates checked against the immutable reference."""
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from homometry import dihedral_canon as canonical, icv
from six_explore import bloom, bloom_edges
from six_inventory import components, inherited_menu


def test_bloom_identity():
    x=((0,0),(1,0),(-2,1),(-2,2),(0,2),(-1,3))
    y=((0,0),(1,0),(2,1),(-1,2),(1,2),(-1,3))
    assert Counter((a-c,b-d) for a,b in x for c,d in x)==Counter((a-c,b-d) for a,b in y for c,d in y)
    for n in (12,17,18,21,24,31,32):
        census=json.loads((ROOT/f"results/2026-09-30-six-census/n{n}.json").read_text())
        pairs={pair for f in census['families'] for pair in combinations([tuple(a) for a in f['members']],2)}
        for (a,b),(p,q) in bloom_edges(n).items():
            assert (a,b) in pairs and tuple(sorted(bloom(p,q,n)))==(a,b)
            assert icv(a,n)==icv(b,n) and canonical(a,n)==a and canonical(b,n)==b


def test_inventory_payloads():
    for n in range(12,61):
        census=json.loads((ROOT/f"results/2026-09-30-six-census/n{n}.json").read_text())
        inventory=json.loads((ROOT/f"results/2026-09-30-six-inventory/n{n}.json").read_text())
        expected={tuple(tuple(a) for a in f['members']):f['icv'] for f in census['families']}
        assert len(inventory['families'])==len(expected)
        for f in inventory['families']:
            members=tuple(tuple(a) for a in f['members'])
            assert expected[members]==f['icv']
            strict=set()
            for e in f['strict_edges']:
                a,b=tuple(e['a']),tuple(e['b'])
                assert a in members and b in members and a!=b
                assert icv(a,n)==icv(b,n)==tuple(f['icv'])
                assert e['labels']
                strict.add((a,b))
            bloom_set=set()
            for e in f['bloom_edges']:
                a,b=tuple(e['a']),tuple(e['b'])
                assert tuple(sorted(bloom(e['p'],e['q'],n)))==(a,b)
                bloom_set.add((a,b))
            assert components(members,strict)==f['strict_components']
            assert components(members,strict|bloom_set)==f['combined_components']
    pair=((0,1,4,6,10,13),(0,1,4,7,9,13))
    assert inherited_menu(18)[pair]['inherited_cZ']=='0'
    assert components(((0,1),(0,2),(0,3)),[])==3


if __name__=='__main__':
    test_bloom_identity();print('PASS Bloom identity and modular certificates against reference',flush=True)
    test_inventory_payloads();print('PASS six-note inventory endpoint certificates n=12..60',flush=True)
