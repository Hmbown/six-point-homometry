"""Additional independent finite-torsion audit; no long census/replay rerun."""
from collections import Counter,defaultdict,deque
from itertools import combinations
from math import comb,gcd
from pathlib import Path
import hashlib,json,sys,time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from homometry import icv,dihedral_canon

def choose(n,k):return comb(n,k) if 0<=k<=n else 0

def burnside(n):
    rotations=0
    for t in range(n):
        cycles=gcd(n,t);length=n//cycles
        if 6%length==0:rotations+=choose(cycles,6//length)
    reflections=0
    for t in range(n):
        fixed=1 if n%2 else (2 if t%2==0 else 0)
        paired=(n-fixed)//2
        reflections+=sum(choose(fixed,j)*choose(paired,(6-j)//2) for j in range(fixed+1) if (6-j)%2==0)
    assert (rotations+reflections)%(2*n)==0
    return (rotations+reflections)//(2*n)

def primes(n):
    ans=[];p=2
    while p*p<=n:
        if n%p==0:
            ans.append(p)
            while n%p==0:n//=p
        p+=1
    if n>1:ans.append(n)
    return ans

def lift_unit(u,q,n):
    assert n%q==0 and gcd(u,q)==1
    value=u;modulus=q
    for p in primes(n):
        if q%p:
            value+=modulus*((1-value)*pow(modulus,-1,p)%p)
            modulus*=p
    assert value%q==u%q and gcd(value,n)==1
    return value%n

def dyad_decomposition(c,n):
    a=c['a'];b=c['b'];_,sign,shift,mask,_=c['certificate']
    common={x for i,x in enumerate(a) if mask>>i&1};removed=set(a)-common
    target={(sign*x+shift)%n for x in b}-common
    assert len(common)==4 and len(removed)==len(target)==2 and not (removed&target)
    origin=min(removed);alpha,beta=sorted((x-origin)%n for x in target)
    center=(alpha+beta)%n;cc={(x-origin)%n for x in common}
    corners={0,alpha,beta,center};assert len(corners)==4 and not cc&corners
    weight=Counter(cc);weight.update((center-x)%n for x in cc);weight.update(corners)
    assert sum(weight.values())==12
    ga,gb=gcd(n,alpha),gcd(n,beta);g=gcd(ga,gb)
    up={};vp={}
    for component in range(g):
        rows=list(range(component,ga,g));cols=list(range(component,gb,g))
        def value(r,s):
            representative=next(x for x in range(r,n,ga) if x%gb==s)
            return weight[representative]
        minimum=min(value(r,cols[0]) for r in rows)
        for r in rows:up[r]=value(r,cols[0])-minimum
        for s in cols:vp[s]=value(rows[0],s)-up[rows[0]]
    u=[up[x%ga] for x in range(n)];v=[vp[x%gb] for x in range(n)]
    assert min(u)>=0 and min(v)>=0 and all(u[x]+v[x]==weight[x] for x in range(n))
    assert all(u[x]==u[(x+alpha)%n] and v[x]==v[(x+beta)%n] for x in range(n))
    return dict(n=n,steps=[alpha,beta],gcds=[ga,gb],u_mass=sum(u),v_mass=sum(v))

def main():
    start=time.monotonic();source=ROOT/'src/six_large_census.c';source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
    families=pairs=0;labels=Counter();paths=[];sample={};dyads=[];classes={};inputs={}
    for n in range(6,136):
        path=ROOT/f'results/2026-09-30-six-large-census/n{n}.json'
        data=json.loads(path.read_text());inputs[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
        assert data['source_sha256']==source_hash and data['methods']==['C-gap-pairs','C-point-correlations']
        expected=burnside(n);classes[n]=expected
        assert data['summary']['classes']==data['independent']['classes']==expected
        fs=data['families'];family_count=len(fs);pair_count=sum(comb(len(f['members']),2) for f in fs)
        assert family_count==data['summary']['families']==data['independent']['families']
        assert pair_count==data['summary']['pairs']==data['independent']['pairs']
        assert max((len(f['members']) for f in fs),default=0)==data['summary']['largest']==data['independent']['largest']
        families+=family_count;pairs+=pair_count
        if n<12:assert not fs;continue
        path=ROOT/f'results/2026-09-30-six-pair-mechanisms/n{n}.json';report=json.loads(path.read_text())
        inputs[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
        adjacency=defaultdict(dict);local=Counter()
        for c in report['certificates']:
            label=c['label'];a,b=tuple(c['a']),tuple(c['b']);assert b not in adjacency[a]
            adjacency[a][b]=label;adjacency[b][a]=label;local[label]+=1
            if label not in sample:sample[label]=(n,c)
            sample[label+'_last']=(n,c)
            if label=='swap':
                delta=c['certificate'][-1]
                assert (n%2 or delta%2==0)
                h=(-delta*pow(2,-1,n))%n if n%2 else (-delta//2)%n
                assert (2*h+delta)%n==0
        labels.update(local)
        assert {k:v for k,v in report['counts'].items() if k!='gap'}==dict(local)
        gaps=[tuple(map(tuple,pair)) for pair in report['gaps']]
        assert len(gaps)==len(set(gaps))==report['counts'].get('gap',0)
        for a,b in gaps:
            assert b not in adjacency[a]
            todo=deque([a]);previous={a:None}
            while todo and b not in previous:
                x=todo.popleft()
                for y in adjacency[x]:
                    if y not in previous:previous[y]=x;todo.append(y)
            assert b in previous
            chain=[b]
            while previous[chain[-1]] is not None:chain.append(previous[chain[-1]])
            chain.reverse();assert len(chain)>=3
            paths.append(dict(n=n,vertices=chain,labels=[adjacency[x][y] for x,y in zip(chain,chain[1:])]))
        # Check constructive nonnegative D decomposition at every modulus,
        # selecting the first recorded certificate independently of its kernel.
        c=next((c for c in report['certificates'] if c['label']=='dyad'),None)
        if c:dyads.append(dyad_decomposition(c,n))
    replay=json.loads((ROOT/'results/2026-09-30-six-pair-mechanisms-review-135.json').read_text())
    assert families==replay['families']==725132 and pairs==replay['pairs']==728424
    assert dict(labels)==replay['certificate_labels'] and sum(labels.values())==728351
    assert len(paths)==replay['missing_direct_edges']==73 and replay['disconnected_families']==[]
    unit_cases=0
    for q in range(6,136):
        for u in range(1,q):
            if gcd(u,q)!=1:continue
            for scale in (2,4,8,9,25,49,210):
                n=q*scale;ambient=lift_unit(u,q,n)
                assert (ambient*scale-u*scale)%n==0;unit_cases+=1
    inflations=[]
    for key,(q,c) in sample.items():
        if key.endswith('_last'):continue
        for scale in (2,5,11):
            n=q*scale;a=tuple(scale*x for x in c['a']);b=tuple(scale*x for x in c['b'])
            assert len(set(a))==len(set(b))==6
            assert icv(a,n)==icv(b,n) and dihedral_canon(a,n)!=dihedral_canon(b,n)
            inflations.append(dict(mechanism=c['label'],source_modulus=q,target_modulus=n))
    result=dict(status='COMPUTED additional independent finite/inflation audit',moduli=130,classes=classes,families=families,pairs=pairs,
                labels=dict(labels),missing_edge_paths=paths,dyad_decompositions=dyads,unit_lift_cases=unit_cases,inflations=inflations,
                source_sha256=source_hash,input_hashes=inputs,seconds=time.monotonic()-start)
    (ROOT/'results/2026-09-30-six-finite-torsion-review.json').write_text(json.dumps(result,indent=2)+'\n')
    print({k:v for k,v in result.items() if k not in ['classes','missing_edge_paths','dyad_decompositions','inflations','input_hashes']})
    print('D decompositions',len(dyads),'gap paths',len(paths),'inflations',len(inflations))

if __name__=='__main__':main()
