"""Independent finite checker: full symmetry group, exact quotient identities.

Does not import the three-dyad builder, SymPy, or normal-form routines.
"""
from collections import Counter
from itertools import combinations,permutations,product
from pathlib import Path
import argparse,gzip,hashlib,json,time
from test_six_cylinder_branches_review import matrix,mul,det,coordinates,linear,autocorrelation

ROOT=Path(__file__).resolve().parents[1]
PERMS=tuple(permutations(range(4)));INDEX={p:i for i,p in enumerate(PERMS)}
P3=tuple(permutations(range(3)));I3={p:i for i,p in enumerate(P3)}
PAIRS=((0,1),(0,2),(1,2))

def code(rows):
    cs=[[-1]*4 for _ in range(3)];pi=[-1]*3;sbits=0
    for i,j,k,l,s in rows:
        if i//2==j//2:
            assert k//2==l//2
            pi[i//2]=k//2
            if s<0:sbits|=1<<(i//2)
        else:
            assert (i//2,j//2)==(k//2,l//2) and s==1
            cs[PAIRS.index((i//2,j//2))][2*(i%2)+j%2]=2*(k%2)+l%2
    a,b,c=(INDEX[tuple(x)] for x in cs)
    return ((a*24+b)*24+c)*48+8*I3[tuple(pi)]+sbits

def full_group():
    ans=[]
    for sigma in permutations(range(3)):
        for fa,fb in product(range(8),repeat=2):
            pa=tuple(2*sigma[i//2]+(i%2 ^ (fa>>(i//2)&1)) for i in range(6))
            pb=tuple(2*sigma[i//2]+(i%2 ^ (fb>>(i//2)&1)) for i in range(6))
            ans.extend([(pa,pb,False),(pa,pb,True)])
    assert len(set(ans))==768
    return ans

def transformed_code(labels,pa,pb,swap):
    out=[]
    for i,j,k,l,s in labels:
        ai,aj=pa[i],pa[j];bk,bl=pb[k],pb[l]
        if swap:ai,aj,bk,bl=bk,bl,ai,aj
        if ai>aj:ai,aj=aj,ai;s=-s
        if bk>bl:bk,bl=bl,bk;s=-s
        out.append((ai,aj,bk,bl,s))
    return code(out)

def run(base):
    start=time.monotonic()
    with gzip.open(base/'orbits.json.gz','rt') as f:orbits=json.load(f)['orbits']
    with gzip.open(base/'cyclic-presentations.json.gz','rt') as f:records=json.load(f)
    assert len(records)==len(orbits)==1495
    group=full_group();seen=bytearray(663552);counts=Counter();weights=Counter();survivors=[]
    for index,(orbit,rec) in enumerate(zip(orbits,records)):
        labels=rec['labels'];assert code(labels)==orbit['representative']==rec['representative']
        assert rec['orbit']==orbit['index']==index
        actual={transformed_code(labels,*g) for g in group}
        assert actual==set(orbit['members']) and len(actual)==orbit['size']==rec['size']
        assert min(actual)==orbit['representative']
        for x in actual:assert not seen[x];seen[x]=1
        m=matrix(labels);u,v=rec['left'],rec['right'];diag=rec['diagonal']
        assert abs(det(u))==abs(det(v))==1
        d=mul(mul(u,m),v)
        assert d==[[diag[i] if i==j else 0 for j in range(10)] for i in range(15)]
        orders,a,b=coordinates(v,diag)
        assert orders==tuple(rec['orders']) and orders.count(0)>=2
        assert a==tuple(map(tuple,rec['a'])) and b==tuple(map(tuple,rec['b']))
        kind=rec['classification'];counts[kind]+=1;weights[kind]+=rec['size']
        if kind=='collision':
            side,i,j=rec['collision'];pts=a if side=='a' else b
            assert i!=j and pts[i]==pts[j]
        else:
            assert len(set(a))==len(set(b))==6
            assert autocorrelation(a,orders)==autocorrelation(b,orders)
            if kind=='TI':
                s=rec['ti']['sign'];anchor=b[rec['ti']['anchor']]
                assert set(a)=={linear([(s,x),(-s,anchor)],orders) for x in b}
            elif kind=='cyclic_collision':
                obs=rec['cyclic_obstruction'];pts=a if obs['side']=='a' else b
                ds=[linear([(1,pts[j]),(-1,pts[i])],orders) for i,j in obs['pairs']]
                zero=(0,)*len(orders)
                assert ds==list(map(tuple,obs['differences'])) and len(set(ds))==3 and zero not in ds
                assert all(linear([(2,x)],orders)==zero for x in ds)
                assert linear([(1,ds[0]),(1,ds[1])],orders)==ds[2]
            else:
                assert kind in ('L2','L4')
                cert=rec['block'];s=cert['b_sign'];shift=cert['b_shift']
                aligned={linear([(s,x),(1,shift)],orders) for x in b}
                common=set(a)&aligned;removed=set(a)-aligned;added=aligned-set(a)
                assert common==set(map(tuple,cert['common'])) and removed==set(map(tuple,cert['removed'])) and added==set(map(tuple,cert['added']))
                delta=cert['block_shift'];assert cert['block_sign']==1
                assert added=={linear([(1,x),(1,delta)],orders) for x in removed}
                cross=Counter(linear([(1,x),(-1,y)],orders) for x in common for y in removed)
                if kind=='L2':
                    assert cross==Counter(linear([(1,x),(-1,y)],orders) for x in common for y in added)
                else:
                    assert tuple(delta)!=(0,)*len(orders) and linear([(2,delta)],orders)==(0,)*len(orders)
                    total=cross+Counter({linear([(-1,x)],orders):n for x,n in cross.items()})
                    shifted=Counter({linear([(1,x),(1,delta)],orders):n for x,n in total.items()})
                    assert total==shifted
                survivors.append(dict(orbit=index,orders=orders,mechanism=kind,moved=len(removed)))
        if (index+1)%300==0:print('checked',index+1,'seconds',round(time.monotonic()-start,2),flush=True)
    assert sum(seen)==663552
    saved=json.loads((base/'cyclic-classification.json').read_text())
    assert dict(counts)==saved['counts'] and dict(weights)==saved['matching_counts']
    return dict(status='COMPUTED independent checker; proof attack still required',orbits=1495,matchings=663552,full_symmetry_group=768,counts=dict(counts),matching_counts=dict(weights),survivors=survivors,seconds=time.monotonic()-start)

def main():
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,default=ROOT/'results/2026-09-30-six-three-dyads');args=p.parse_args()
    result=run(args.base)
    result['sha256']={str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in [args.base/'orbits.json.gz',args.base/'cyclic-presentations.json.gz',ROOT/'src/six_three_dyads.py',Path(__file__)]}
    (args.base/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(result,flush=True)

if __name__=='__main__':main()
