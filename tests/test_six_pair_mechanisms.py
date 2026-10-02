"""Independent replay of endpoint, group-ring and connectivity certificates."""
from pathlib import Path
from collections import Counter
from itertools import combinations
import argparse,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from homometry import icv,dihedral_canon

def check(c,n):
    a=tuple(c['a']);b=tuple(c['b']);label=c['label']
    assert len(a)==len(b)==6 and a!=b and icv(a,n)==icv(b,n)
    assert dihedral_canon(a,n)==a and dihedral_canon(b,n)==b
    if label=='Bloom':
        p,q=c['parameters'];x=(0,p,q-2*p,2*q-2*p,2*q,3*q-p);y=(0,p,q+2*p,2*q-p,2*q+p,3*q-p)
        assert sorted((dihedral_canon(x,n),dihedral_canon(y,n)))==[a,b]
    elif label=='R':
        from six_templates import SEEDS
        index,t=c['parameters'];q,x,y=SEEDS[index-1];assert q*t%n==0
        assert sorted((dihedral_canon([v*t%n for v in x],n),dihedral_canon([v*t%n for v in y],n)))==[a,b]
    elif label=='unit':
        from math import gcd
        u=c['u'];assert gcd(u,n)==1 and dihedral_canon([u*x%n for x in a],n)==b
        auto=Counter((x-y)%n for x in a for y in a)
        assert auto==Counter({u*x%n:v for x,v in auto.items()})
    elif label=='halfcoset':
        h=c['h'];assert n%h==0;step=n//h;counts=Counter(x%step for x in a)
        assert all(v==h//2 for v in counts.values())
        other=tuple(sorted({x+step*j for x in counts for j in range(h)}-set(a)))
        assert len(other)==6 and dihedral_canon(other,n)==b
    else:
        _,sign,shift,mask,t=c['certificate']
        u=[x for i,x in enumerate(a) if mask>>i&1];w=[x for x in a if x not in u]
        image={(sign*x+shift)%n for x in b};assert set(u)<=image;v=image-set(u)
        left=Counter((x-y)%n for x in u for y in w)
        if label=='dyad':
            assert len(u)==4 and len(w)==len(v)==2 and (sum(w)-sum(v))%n==0
            # A kernel certificate for D, constructed directly from the
            # four common points and the parallelogram corners.
            anchor=w[0];aa,bb=sorted((x-anchor)%n for x in v)
            common=[(x-anchor)%n for x in u];weight=Counter(common)
            weight.update((aa+bb-x)%n for x in common);weight.update([0,aa,bb,(aa+bb)%n])
            assert sum(weight.values())==12
            assert all(weight[g]-weight[(g-aa)%n]-weight[(g-bb)%n]+weight[(g-aa-bb)%n]==0 for g in range(n))
        elif label=='reflect':
            assert {(t-x)%n for x in w}==v
            right=Counter((x+y-t)%n for x in u for y in w);assert left==right
        else:
            assert {(x+t)%n for x in w}==v
            if label=='translate':assert left==Counter({(x+t)%n:k for x,k in left.items()})
            elif label=='swap':
                assert n%2 or t%2==0
                assert Counter({(x-t)%n:k for x,k in left.items()})==Counter({-x%n:k for x,k in left.items()})
            elif label=='halfturn':
                assert 2*t==n
                total=left+Counter({-x%n:k for x,k in left.items()})
                assert total==Counter({(x+t)%n:k for x,k in total.items()})
            else:raise AssertionError(label)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--nmax',type=int,default=135);args=parser.parse_args()
    labels=Counter();families_count=0;pair_count=0;missing_edges=0;disconnected=[]
    for n in range(12,args.nmax+1):
        path=ROOT/f'results/2026-09-30-six-pair-mechanisms/n{n}.json'
        if not path.exists():raise RuntimeError(f'missing checkpoint {n}')
        report=json.loads(path.read_text());source=ROOT/f'results/2026-09-30-six-large-census/n{n}.json'
        if not source.exists():source=ROOT/f'results/2026-09-30-six-census/n{n}.json'
        families=json.loads(source.read_text())['families']
        allpairs={tuple(sorted(map(tuple,pair))) for f in families for pair in combinations(f['members'],2)}
        certs={}
        for c in report['certificates']:
            check(c,n);key=tuple(sorted((tuple(c['a']),tuple(c['b']))));assert key in allpairs and key not in certs
            certs[key]=c;labels[c['label']]+=1
        gaps={tuple(map(tuple,pair)) for pair in report['gaps']}
        assert not (set(certs)&gaps) and set(certs)|gaps==allpairs
        # Independent union-find; production uses reachability expansion.
        for f in families:
            mem=list(map(tuple,f['members']));parent={x:x for x in mem}
            def root(x):
                while parent[x]!=x:x=parent[x]
                return x
            for a,b in combinations(mem,2):
                if (a,b) in certs:parent[root(a)]=root(b)
            if len({root(x) for x in mem})!=1:disconnected.append(dict(n=n,members=mem))
        families_count+=len(families);pair_count+=len(allpairs);missing_edges+=len(gaps)
    from six_pair_mechanisms import quick_certificate
    try:quick_certificate((0,1,2,3,4,5),(0,1,2,3,4,6),17)
    except ValueError:pass
    else:raise AssertionError('nonhomometric negative control accepted')
    result=dict(nmin=12,nmax=args.nmax,families=families_count,pairs=pair_count,missing_direct_edges=missing_edges,
                certificate_labels=dict(labels),disconnected_families=disconnected,status='COMPUTED independent certificate replay and connectivity')
    (ROOT/f'results/2026-09-30-six-pair-mechanisms-review-{args.nmax}.json').write_text(json.dumps(result,indent=2)+'\n')
    assert not disconnected,disconnected[:3]
    print(result)

if __name__=='__main__':main()
