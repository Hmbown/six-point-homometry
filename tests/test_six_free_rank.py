"""Independent exhaustive audit of the high-free-rank presentation reduction.

The checker uses exterior minors for rational subspaces, all 720 vertex
permutations for orbit coverage, direct edge-by-edge matching DFS, and
integer row multiplication for discarded cases. It never calls production
span reduction, matching enumeration, Smith decomposition or group canon.
"""
from collections import Counter
from itertools import combinations,permutations
from math import gcd
from pathlib import Path
import json,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from homometry import icv,dihedral_canon
import test_six_shadow_review as independent
EDGES=tuple(combinations(range(6),2))


def normalize(row):
    g=gcd(*row)
    if not g:return ()
    sign=1 if next(x for x in row if x)>0 else -1
    return tuple(sign*x//g for x in row)
def key(rows):
    if not rows:return (0,())
    if len(rows)==1:return (1,normalize(rows[0]))
    a,b=rows;w=normalize(tuple(a[i]*b[j]-a[j]*b[i] for i,j in EDGES))
    return (2,w) if w else (1,normalize(a))
def directions():
    ds=set()
    for prototype in [(1,-1,0,0,0,0),(2,-1,-1,0,0,0),(1,1,-1,-1,0,0)]:
        ds.update(normalize(p) for p in permutations(prototype))
    return ds


def self_matchings(h):
    candidates=[]
    for i,j in EDGES:
        candidates.append([(index,(i,j,k,l,sign)) for index,(k,l) in enumerate(EDGES)
                           for sign in (-1,1) if h[j]-h[i]==sign*(h[l]-h[k])])
    def dfs(depth,used,labels):
        if depth==15:yield tuple(sorted(labels));return
        for index,label in candidates[depth]:
            bit=1<<index
            if not used&bit:yield from dfs(depth+1,used|bit,labels+(label,))
    return dfs(0,0,())


def test_spans_and_orbits():
    saved=json.loads((ROOT/'results/2026-09-30-six-free-rank/spans.json').read_text());ds=directions()
    assert len(ds)==120
    expected={(0,())}|{key([d]) for d in ds}|{key(pair) for pair in combinations(ds,2)}
    assert len(expected)==4176
    covered=set()
    for orbit in saved['orbits']:
        rows=orbit['rows'];local=set()
        for perm in permutations(range(6)):
            local.add(key([[row[i] for i in perm] for row in rows]))
        assert len(local)==orbit['size'] and not covered&local
        covered|=local
        h=orbit['heights'];rank=len(rows)
        assert h[0]==0
        for d in ds:
            belongs=len(independent.rational_pivots(rows+[list(d)]))==rank
            assert (sum(x*y for x,y in zip(d,h))==0)==belongs
        assert len(set(h))>=4
    assert covered==expected and len(saved['orbits'])==25
    return dict(directions=120,rational_spans=4176,permutation_orbits=25)


def relation_matrix(labels):return independent.matching_matrix(labels)
def row_mul(row,m):return [sum(c*m[i][j] for i,c in enumerate(row)) for j in range(10)]
def point(vertex,side):
    return [int(vertex!=0 and j==vertex-1+(5 if side=='b' else 0)) for j in range(10)]
def matmul(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def add(x,y,orders):return tuple((a+b)%d if d else a+b for a,b,d in zip(x,y,orders))
def neg(x,orders):return tuple(-a%d if d else -a for a,d in zip(x,orders))
def sub(x,y,orders):return add(x,neg(y,orders),orders)
def transform(points,sign,shift,orders):return {add(x if sign==1 else neg(x,orders),shift,orders) for x in points}


def test_all_presentations():
    totals=Counter();total_labels=0;row_witnesses=0
    for path in sorted((ROOT/'results/2026-09-30-six-free-rank').glob('orbit*.json')):
        data=json.loads(path.read_text());orbit=data['orbit'];h=orbit['heights']
        labels={}
        for cert in data['discarded']+data['nontrivial']:
            label=tuple(tuple(x) for x in cert['labels']);canonical=tuple(sorted(label));assert canonical not in labels
            labels[canonical]=cert
            m=relation_matrix(label);kind=cert['classification'];totals[kind]+=1
            if kind=='collision':
                relation=[x-y for x,y in zip(point(cert['i'],cert['side']),point(cert['j'],cert['side']))]
                assert cert['i']!=cert['j'] and row_mul(cert['witness'],m)==relation;row_witnesses+=1
            elif kind=='trivial':
                assert sorted(cert['mapping'])==list(range(6))
                for i,j in enumerate(cert['mapping']):
                    relation=[x-cert['sign']*y+cert['sign']*z for x,y,z in zip(point(i,'a'),point(j,'b'),point(cert['anchor'],'b'))]
                    assert row_mul(cert['witnesses'][i],m)==relation;row_witnesses+=1
            else:
                assert kind=='block'
                u,v=cert['left'],cert['right']
                assert abs(independent.determinant(u))==abs(independent.determinant(v))==1
                target=[[int(i==j)*([1]*6+[2,0,0,0])[j] for j in range(10)] for i in range(15)]
                assert matmul(matmul(u,m),v)==target
                assert cert['orders']==[2,0,0,0]
                coordinates=[(row[6]%2,*row[7:10]) for row in v]
                a={(0,0,0,0),*coordinates[:5]};b={(0,0,0,0),*coordinates[5:]}
                assert a==set(map(tuple,cert['a'])) and b==set(map(tuple,cert['b'])) and len(a)==len(b)==6
                master=cert['master'];assert master is not None
                orders=cert['orders'];base,p,q,r,h=(tuple(master[x]) for x in ['base','p','q','r','h'])
                assert h==(1,0,0,0) and abs(independent.determinant([p[1:],q[1:],r[1:]]))==1
                zero=(0,0,0,0);common={zero,p,q,add(sub(p,q,orders),h,orders)}
                aa=common|{r,add(r,h,orders)};s=sub(p,r,orders);bb=common|{s,add(s,h,orders)}
                assert transform(a,1,neg(base,orders),orders)==aa
                aligned=transform(b,master['b_sign'],tuple(master['b_shift']),orders)
                assert transform(aligned,1,neg(base,orders),orders)==bb
                assert all(transform(a,sign,neg(anchor if sign==1 else neg(anchor,orders),orders),orders)!=b for sign in (1,-1) for anchor in a)
        expected=set(self_matchings(orbit['heights']));assert set(labels)==expected
        assert len(expected)==orbit['matching_count']
        total_labels+=len(expected)
    assert dict(totals)=={'trivial':555,'collision':13916,'block':4}
    assert total_labels==14475 and row_witnesses==17246
    return dict(matchings=total_labels,classification=dict(totals),exact_discard_row_witnesses=row_witnesses,
                surviving_unimodular_identities=4,universal_master_certificates=4)


def test_master_identity_and_counterexample():
    orders=(2,0,0,0);zero=(0,0,0,0);h=(1,0,0,0);p=(0,1,0,0);q=(0,0,1,0);r=(0,0,0,1)
    c={zero,p,q,add(sub(p,q,orders),h,orders)}
    a=c|{r,add(r,h,orders)};s=sub(p,r,orders);b=c|{s,add(s,h,orders)}
    def ac(points):return Counter(sub(x,y,orders) for x in points for y in points)
    assert ac(a)==ac(b)
    assert len(a)==len(b)==6
    n=22;aa=(0,1,3,6,13,17);bb=(0,1,3,8,13,19)
    assert icv(aa,n)==icv(bb,n) and dihedral_canon(aa,n)!=dihedral_canon(bb,n)
    return dict(formal_group='C2 x Z^3',directed_formal_differences=36,rank_bound_counterexample_n=22)


def main():
    started=time.monotonic();results={}
    for fn in [test_spans_and_orbits,test_all_presentations,test_master_identity_and_counterexample]:
        results[fn.__name__]=fn();print('PASS',fn.__name__,results[fn.__name__],flush=True)
    results['seconds']=time.monotonic()-started
    (ROOT/'results/2026-09-30-six-free-rank/verification.json').write_text(json.dumps(results,indent=2)+'\n')

if __name__=='__main__':main()
