"""Independent exact review of high-rank and Bloom cylinder branches.

No imports of builder modules, SymPy, or Smith/Hermite normal-form routines.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, permutations
from math import factorial, gcd, prod
from pathlib import Path
import argparse, hashlib, json, sys, time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from homometry import icv,dihedral_canon
EDGES=tuple(combinations(range(6),2))
ZERO=(0,)*10
UNITS=tuple(tuple(int(i==j) for j in range(10)) for i in range(10))
RAW_A=(ZERO,*UNITS[:5]); RAW_B=(ZERO,*UNITS[5:])
FORMS=(
 (((0,0),(-2,1),(0,1),(-3,2),(-2,3),(-1,3)),((0,0),(-1,1),(1,1),(1,2),(-2,3),(-1,3))),
 (((0,0),(-1,1),(1,1),(-2,3),(-1,3),(1,2)),((0,0),(1,0),(-1,2),(2,1),(-1,3),(1,2))))
X=((0,0),(1,0),(-2,1),(-2,2),(0,2),(-1,3))
Y=((0,0),(1,0),(2,1),(-1,2),(1,2),(-1,3))

def mul(a,b):
    assert a and b and len(a[0])==len(b)
    assert all(type(x) is int for row in [*a,*b] for x in row)
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

def det(a):
    a=[list(row) for row in a]; n=len(a); sign=1; previous=1
    assert all(len(row)==n for row in a)
    for k in range(n-1):
        p=next((i for i in range(k,n) if a[i][k]),None)
        if p is None:return 0
        if p!=k:a[k],a[p]=a[p],a[k];sign=-sign
        pivot=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                value=pivot*a[i][j]-a[i][k]*a[k][j]
                assert value%previous==0
                a[i][j]=value//previous
            a[i][k]=0
        previous=pivot
    return sign*a[-1][-1]

def rref(rows):
    a=[list(map(Q,row)) for row in rows if any(row)]
    if not a:return ()
    lead=0
    for col in range(len(a[0])):
        pivot=next((i for i in range(lead,len(a)) if a[i][col]),None)
        if pivot is None:continue
        a[lead],a[pivot]=a[pivot],a[lead]
        v=a[lead][col];a[lead]=[x/v for x in a[lead]]
        for i in range(len(a)):
            if i!=lead:
                v=a[i][col];a[i]=[x-v*y for x,y in zip(a[i],a[lead])]
        lead+=1
        if lead==len(a):break
    return tuple(tuple(row) for row in a[:lead])

def prim(row):
    d=gcd(*row); sign=1 if next(x for x in row if x)>0 else -1
    return tuple(sign*x//d for x in row)

def directions():
    result=set()
    # The three possible support patterns of a difference of signed edges.
    for i,j in combinations(range(6),2):
        v=[0]*6;v[i]=1;v[j]=-1;result.add(prim(v))
    for triple in combinations(range(6),3):
        for middle in triple:
            v=[0]*6
            for i in triple:v[i]=-2 if i==middle else 1
            result.add(prim(v))
    for four in combinations(range(6),4):
        for plus in combinations(four,2):
            v=[0]*6
            for i in four:v[i]=1 if i in plus else -1
            result.add(prim(v))
    return sorted(result)

def signed_matchings(aa,bb):
    """Independent edge-by-edge DFS, with a used-edge bitmask."""
    def difference(x,y):
        return tuple(v-u for u,v in zip(x,y)) if isinstance(x,tuple) else y-x
    def times(s,x):return tuple(s*t for t in x) if isinstance(x,tuple) else s*x
    da=[difference(aa[i],aa[j]) for i,j in EDGES]
    db=[difference(bb[i],bb[j]) for i,j in EDGES]
    options=[[(j,s) for j,v in enumerate(db) for s in (-1,1) if u==times(s,v)] for u in da]
    def dfs(i,used,labels):
        if i==15:yield tuple(labels);return
        u,v=EDGES[i]
        for target,s in options[i]:
            if not (used>>target)&1:
                k,l=EDGES[target]
                yield from dfs(i+1,used|(1<<target),labels+[(u,v,k,l,s)])
    return dfs(0,0,[])

def matrix(labels):
    assert sorted((i,j) for i,j,k,l,s in labels)==list(EDGES)
    assert sorted((k,l) for i,j,k,l,s in labels)==list(EDGES)
    assert all(s in (-1,1) for i,j,k,l,s in labels)
    return [[RAW_A[j][v]-RAW_A[i][v]-s*RAW_B[l][v]+s*RAW_B[k][v] for v in range(10)] for i,j,k,l,s in labels]

def verify_diagonal(m,u,v,diagonal,absolute=False):
    assert len(u)==15 and len(v)==10
    assert abs(det(u))==abs(det(v))==1
    d=mul(mul(u,m),v)
    for i in range(15):
        for j in range(10):
            expected=diagonal[i] if i==j else 0
            assert (abs(d[i][j]) if absolute else d[i][j])==expected
    return d

def linear(terms,orders):
    ans=[sum(c*v[i] for c,v in terms) for i in range(len(orders))]
    return tuple(x%d if d else x for x,d in zip(ans,orders))

def coordinates(v,diag):
    keep=[i for i,x in enumerate(diag) if abs(x)!=1]
    orders=tuple(abs(diag[i]) for i in keep)
    points=[tuple(row[i]%abs(diag[i]) if diag[i] else row[i] for i in keep) for row in v]
    origin=(0,)*len(orders)
    return orders,(origin,*points[:5]),(origin,*points[5:])

def autocorrelation(points,orders):
    return Counter(linear([(1,a),(-1,b)],orders) for a in points for b in points)

def orbit_audit(base):
    start=time.monotonic(); saved=json.loads((base/'spans.json').read_text())
    ds=directions();assert len(ds)==120
    flats={()}|{rref([d]) for d in ds}|{rref(pair) for pair in combinations(ds,2)}
    assert len(flats)==saved['spans']==4176
    unseen=set(flats);orbit_union=set();counts=Counter();certificates=0;survivors=[]
    for orbit in saved['orbits']:
        rows=orbit['rows'];h=orbit['heights'];key=rref(rows)
        permuted={rref([[row[j] for j in p] for row in rows]) for p in permutations(range(6))}
        assert len(permuted)==orbit['size'] and permuted<=flats
        assert not (permuted&orbit_union)
        orbit_union|=permuted;unseen-=permuted
        assert len(key)<=2 and h[0]==0
        for d in ds:
            assert (sum(x*y for x,y in zip(d,h))==0)==(len(rref([*rows,d]))==len(key))
        record=json.loads((base/f'orbit{orbit["index"]:02}.json').read_text())
        records=record['discarded']+record['nontrivial']
        actual={tuple(sorted(map(tuple,z['labels']))) for z in records}
        expected=set(signed_matchings(h,h))
        assert actual==expected and len(actual)==len(records)==orbit['matching_count']
        hist=Counter(abs(h[j]-h[i]) for i,j in EDGES)
        assert len(actual)==prod(factorial(n)*(2**n if d==0 else 1) for d,n in hist.items())
        orbit_counts=Counter()
        for rec in records:
            m=matrix(rec['labels']);kind=rec['classification'];counts[kind]+=1;orbit_counts[kind]+=1
            if kind=='collision':
                raw=RAW_A if rec['side']=='a' else RAW_B
                assert rec['i']!=rec['j']
                target=[x-y for x,y in zip(raw[rec['i']],raw[rec['j']])]
                assert mul([rec['witness']],m)==[target];certificates+=1
            elif kind=='trivial':
                s=rec['sign'];anchor=rec['anchor'];mapping=rec['mapping']
                assert s in (-1,1) and sorted(mapping)==list(range(6))
                target=[[x-s*y+s*z for x,y,z in zip(RAW_A[i],RAW_B[j],RAW_B[anchor])] for i,j in enumerate(mapping)]
                assert mul(rec['witnesses'],m)==target;certificates+=6
            else:
                assert kind=='block'
                d=verify_diagonal(m,rec['left'],rec['right'],rec['diagonal'],absolute=True)
                orders,a,b=coordinates(rec['right'],rec['diagonal'])
                assert orders==tuple(rec['orders'])==(2,0,0,0)
                assert set(a)==set(map(tuple,rec['a'])) and set(b)==set(map(tuple,rec['b']))
                assert len(set(a))==len(set(b))==6
                assert autocorrelation(a,orders)==autocorrelation(b,orders)
                bc=rec['block']
                image={linear([(bc['b_sign'],x),(1,bc['b_shift'])],orders) for x in b}
                assert set(a)&image==set(map(tuple,bc['common']))
                assert set(a)-image==set(map(tuple,bc['removed']))
                assert image-set(a)==set(map(tuple,bc['added']))
                assert {linear([(bc['block_sign'],x),(1,bc['block_shift'])],orders) for x in bc['removed']}==set(map(tuple,bc['added']))
                mc=rec['master'];p,q,r,h0=[mc[k] for k in ('p','q','r','h')];zero=(0,)*len(orders)
                assert tuple(h0)!=zero and linear([(2,h0)],orders)==zero
                assert abs(det([p[1:],q[1:],r[1:]]))==1
                common=[zero,tuple(p),tuple(q),linear([(1,p),(-1,q),(1,h0)],orders)]
                left=common+[tuple(r),linear([(1,r),(1,h0)],orders)]
                right=common+[linear([(1,p),(-1,r)],orders),linear([(1,p),(-1,r),(1,h0)],orders)]
                assert {linear([(1,mc['base']),(1,x)],orders) for x in left}==set(a)
                assert {linear([(1,mc['base']),(1,x)],orders) for x in right}=={linear([(mc['b_sign'],x),(1,mc['b_shift'])],orders) for x in b}
                survivors.append(dict(orbit=orbit['index'],index=rec['index'],orders=orders,moved=bc['moved']))
        assert dict(orbit_counts)==record['counts']
    assert not unseen and len(orbit_union)==len(flats)
    assert dict(counts)==json.loads((base/'presentations.json').read_text())['counts']
    # Prove the formal master identity in C2 x Z3 by exact coefficient counting.
    orders=(2,0,0,0);h=(1,0,0,0);p=(0,1,0,0);q=(0,0,1,0);r=(0,0,0,1)
    c=[(0,0,0,0),p,q,linear([(1,p),(-1,q),(1,h)],orders)]
    a=c+[r,linear([(1,r),(1,h)],orders)]
    b=c+[linear([(1,p),(-1,r)],orders),linear([(1,p),(-1,r),(1,h)],orders)]
    assert autocorrelation(a,orders)==autocorrelation(b,orders)
    actual_a=(0,1,3,6,13,17);actual_b=(0,1,3,8,13,19)
    assert icv(actual_a,22)==icv(actual_b,22)
    assert dihedral_canon(actual_a,22)!=dihedral_canon(actual_b,22)
    return dict(directions=len(ds),flats=len(flats),orbits=len(saved['orbits']),matchings=sum(counts.values()),counts=dict(counts),row_identities=certificates,survivors=survivors,formal_master_identity=True,seconds=time.monotonic()-start)

def bloom_audit(path):
    start=time.monotonic();saved=json.loads(path.read_text());presentations={x['id']:x['presentation'] for x in saved['presentations']}
    collision=0;torsion=Counter();identities=0;case_results=[]
    for uid,rec in presentations.items():
        m=matrix(rec['labels']);assert m==rec['matrix']
        d=verify_diagonal(m,rec['smith_u'],rec['smith_v'],rec['smith_diagonal'])
        orders,a,b=coordinates(rec['smith_v'],rec['smith_diagonal'])
        assert list(a)==list(map(tuple,rec['a'])) and list(b)==list(map(tuple,rec['b']))
        distinct=len(set(a))==len(set(b))==6
        assert distinct==rec['six_distinct_in_presentation']
        rank=sum(x!=0 for x in rec['smith_diagonal']);assert rank==rec['rank'] and 10-rank==rec['free_rank']
        assert [x for x in orders if x]==rec['torsion_factors']
        if not distinct:collision+=1;continue
        cert=rec['bloom_certificate'];p,q=cert['p'],cert['q'];s=cert['sign_y']
        assert s in (-1,1)
        xx=[linear([(1,cert['shift_x']),(u,p),(v,q)],orders) for u,v in X]
        yy=[linear([(1,cert['shift_y']),(s*u,p),(s*v,q)],orders) for u,v in Y]
        left,right=(a,b) if cert['x_side']=='a' else (b,a)
        assert Counter(xx)==Counter(left) and Counter(yy)==Counter(right)
        torsion[(rec['free_rank'],tuple(rec['torsion_factors']))]+=1
    # Distinct representatives really are distinct labelled integer lattices.
    # Witness inequality by an original row with nonzero class in the other's
    # certified quotient; no HNF routine or HNF metadata is trusted.
    distinct_lattice_pairs=0
    for i,j in combinations(presentations,2):
        def not_contained(i,j):
            left=presentations[i];right=presentations[j]
            transformed=mul(left['matrix'],right['smith_v'])
            return any((value%d!=0 if d else value!=0) for row in transformed for value,d in zip(row,right['smith_diagonal']))
        assert not_contained(i,j) or not_contained(j,i)
        distinct_lattice_pairs+=1
    for kind,forms in enumerate(FORMS,1):
        da=[tuple(y-x for x,y in zip(forms[0][i],forms[0][j])) for i,j in EDGES]
        db=[tuple(y-x for x,y in zip(forms[1][i],forms[1][j])) for i,j in EDGES]
        assert Counter(da)==Counter(db)
        assert len(set(da))==15
        critical=set()
        for x,y in combinations(da,2):
            c=x[0]-y[0];d=x[1]-y[1]
            if d:critical.add(Q(-c,d))
        # Zero distances are also checked, without relying on duplicated forms.
        critical|={Q(-c,d) for c,d in da if d}
        critical={t for t in critical if (t>=3 if kind==1 else Q(3,2)<=t<2)}
        cases=[x for x in saved['cases'] if x['kind']==kind]
        assert {x['slope'] for x in cases}=={'None'}|set(map(str,critical))
        for case in cases:
            slope=None if case['slope']=='None' else Q(case['slope'])
            if slope is None:a,b=forms
            else:a,b=[tuple(Q(x)+y*slope for x,y in pts) for pts in forms]
            expected=set(signed_matchings(a,b))
            actual={tuple(sorted(map(tuple,r['labels']))) for r in case['matching_records']}
            assert expected==actual and len(actual)==len(case['matching_records'])==case['expected_matchings']
            assert case['matching_presentation_ids']==[x['presentation_id'] for x in case['matching_records']]
            for rec in case['matching_records']:
                m=matrix(rec['labels']);representative=presentations[rec['presentation_id']]['matrix']
                assert mul(rec['representative_from_matching'],m)==representative
                assert mul(rec['matching_from_representative'],representative)==m
                identities+=30
            case_results.append(dict(kind=kind,slope=case['slope'],matchings=len(actual)))
    assert sum(x['matchings'] for x in case_results)==saved['total_matchings']==282
    assert len(presentations)==saved['unique_labelled_row_lattices']==21
    return dict(cases=case_results,matchings=282,presentations=21,distinct_lattice_pairs=distinct_lattice_pairs,collision_presentations=collision,bloom_presentations=21-collision,histogram=[dict(free_rank=k[0],torsion=k[1],count=v) for k,v in sorted(torsion.items())],row_identities=identities,seconds=time.monotonic()-start)

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='results/2026-09-30-six-cylinder-branches-review.json');args=p.parse_args()
    report={'status':'COMPUTED independent exact certificate audit'}
    report['high_free_rank']=orbit_audit(ROOT/'results/2026-09-30-six-free-rank')
    print('PASS high-free-rank',report['high_free_rank'],flush=True)
    report['bloom']=bloom_audit(ROOT/'results/2026-09-30-six-bloom-cylinders.json')
    print('PASS Bloom cylinders',report['bloom'],flush=True)
    report['inputs']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'src/six_free_rank.py',ROOT/'src/six_bloom_cylinders.py',ROOT/'results/2026-09-30-six-bloom-cylinders.json',*sorted((ROOT/'results/2026-09-30-six-free-rank').glob('*.json'))]}
    Path(args.out).write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
