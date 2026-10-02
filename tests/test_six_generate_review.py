"""Separate executable review: independent sparse certificate arithmetic.

Only driver entry points are imported for generation/replay attacks. No
production canon, correlation, mechanism or saved-edge verifier is used by
the independent checker. It reconstructs canonical classes from gap words.
"""
from collections import Counter
from copy import deepcopy
from itertools import combinations,product
from math import gcd
from pathlib import Path
from random import Random
import hashlib,json,sys,time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import six_generate as driver
SEEDS=(
 (17,(0,1,2,3,8,12),(0,1,2,6,7,9)),
 (19,(0,1,2,3,6,10),(0,1,2,4,5,11)),
 (21,(0,1,2,4,7,14),(0,1,3,7,8,10)),
 (21,(0,1,2,5,6,15),(0,1,2,6,7,10)),
 (21,(0,1,3,7,10,15),(0,1,4,7,14,16)),
 (23,(0,1,2,3,7,17),(0,1,2,4,17,18)),
 (24,(0,1,2,5,7,16),(0,1,2,6,9,11)),
 (27,(0,1,2,3,7,19),(0,1,2,3,8,12)),
 (27,(0,1,2,6,19,22),(0,1,3,17,21,22)),
 (28,(0,1,2,4,12,23),(0,1,3,5,11,12)),
 (30,(0,1,2,6,19,22),(0,1,3,9,13,14)),
 (30,(0,1,3,5,12,25),(0,1,6,9,11,13)),
 (31,(0,1,2,5,11,19),(0,1,2,6,20,23)))


def canonical(points,n):
    a=sorted(x%n for x in points);assert len(set(a))==len(a)
    gaps=tuple((a[(i+1)%len(a)]-a[i])%n for i in range(len(a)))
    words=[w[i:]+w[:i] for w in (gaps,gaps[::-1]) for i in range(len(a))]
    best=min(words);out=[0]
    for x in best[:-1]:out.append(out[-1]+x)
    return tuple(out)


def motion(a,n,sign,shift):
    assert sign in (-1,1)
    return {(sign*x+shift)%n for x in a}


def differences(a,n):return Counter((x-y)%n for x in a for y in a)


def bloom(p,q,n):
    return ({x%n for x in (0,p,q-2*p,2*q-2*p,2*q,3*q-p)},
            {x%n for x in (0,p,q+2*p,2*q-p,2*q+p,3*q-p)})


def direct(a,b,n,c):
    a,b=set(a),set(b);label=c['label'];assert len(a)==len(b)==6
    assert differences(a,n)==differences(b,n)
    if label=='Bloom':
        x,y=bloom(c['p'],c['q'],n)
        x=motion(x,n,1,c['x_shift']);y=motion(y,n,c['y_sign'],c['y_shift'])
        assert c['x_side'] in ('a','b') and (x,y)==((a,b) if c['x_side']=='a' else (b,a));return
    if label=='R':
        assert type(c['seed']) is int and 1<=c['seed']<=len(SEEDS)
        q,x,y=SEEDS[c['seed']-1];t=c['parameter'];assert q*t%n==0
        assert sorted((canonical([t*z%n for z in x],n),canonical([t*z%n for z in y],n)))==sorted((canonical(a,n),canonical(b,n)));return
    bb=motion(b,n,c['b_sign'],c['b_shift'])
    if label=='L7':
        h=c['order'];assert h in (2,4,6,12) and n%h==0
        step=n//h;cosets={x%step for x in a};whole={x+j*step for x in cosets for j in range(h)}
        assert all(sum(y%step==x for y in a)==h//2 for x in cosets)
        assert whole-a==bb;return
    if label=='D':
        common=set(c['common']);s,t=c['steps'];center=(s+t)%n
        assert len(common)==4 and len(common|{0,center})==len(common|{s,t})==6
        assert motion(common|{0,center},n,1,c['anchor'])==a
        assert motion(common|{s,t},n,1,c['anchor'])==bb
        weight=Counter(common);weight.update((center-x)%n for x in common);weight.update((0,s,t,center))
        assert sorted(weight.items())==list(map(tuple,c['weight']))
        defect=Counter()
        for x,v in weight.items():
            for shift,sign in ((0,1),(s,-1),(t,-1),(s+t,1)):defect[(x+shift)%n]+=sign*v
        assert all(v==0 for v in defect.values());return
    fixed=set(c['fixed']);moving=a-fixed;assert fixed and moving and fixed<=a&bb
    t=c['move'];local_sign=-1 if label=='L5' else 1
    assert fixed|motion(moving,n,local_sign,t)==bb
    assert not fixed&motion(moving,n,local_sign,t)
    original=Counter((u-w)%n for u in fixed for w in moving)
    changed=Counter((u-local_sign*w-t)%n for u in fixed for w in moving)
    reverse=Counter((w-u)%n for u in fixed for w in moving)
    if label=='L2':assert changed==original
    elif label=='L3*':assert changed==reverse
    elif label=='L4':
        assert 2*t%n==0
        assert changed+Counter((t+w-u)%n for u in fixed for w in moving)==original+reverse
    elif label=='L5':assert changed==original
    else:raise AssertionError(label)


def saved(c,n):
    a,b=tuple(c['a']),tuple(c['b']);label=c['label']
    assert len(a)==len(b)==6 and a!=b and canonical(a,n)==a and canonical(b,n)==b
    assert differences(a,n)==differences(b,n)
    if label=='Bloom':
        x,y=bloom(*c['parameters'],n);assert sorted((canonical(x,n),canonical(y,n)))==[a,b]
    elif label=='R':direct(a,b,n,dict(label='R',seed=c['parameters'][0],parameter=c['parameters'][1]))
    elif label=='unit':
        u=c['u'];assert gcd(n,u)==1 and canonical([u*x%n for x in a],n)==b
        assert differences(a,n)==differences([u*x%n for x in a],n)
    elif label=='halfcoset':
        h=c['h'];assert h in (2,4,6,12) and n%h==0;step=n//h
        residues={x%step for x in a};whole={r+j*step for r in residues for j in range(h)}
        assert all(sum(x%step==r for x in a)==h//2 for r in residues)
        assert canonical(whole-set(a),n)==b
    else:
        number,sign,t,mask,v=c['certificate'];names={1:'translate',2:'swap',3:'halfturn',4:'reflect',5:'dyad'}
        assert names.get(number)==label and type(mask) is int and 0<mask<64
        fixed={x for i,x in enumerate(a) if mask>>i&1};bb=motion(b,n,sign,t)
        if label=='dyad':
            assert fixed==set(a)&bb and len(fixed)==4
            left=set(a)-fixed;right=bb-fixed;assert len(left)==len(right)==2 and (sum(left)-sum(right))%n==0
        else:
            if label=='swap':assert n%2 or v%2==0
            if label=='halfturn':assert n%2==0 and v==n//2
            direct(a,b,n,dict(label={'translate':'L2','swap':'L3*','halfturn':'L4','reflect':'L5'}[label],b_sign=sign,b_shift=t,fixed=sorted(fixed),move=v))
    return a,b


def portable(c):
    assert c['schema']=='six-generation-v1';n=c['n'];assert type(n) is int and n>=6
    inputs=[]
    for side in ('a','b'):
        raw=c['input_'+side];assert len(raw)==6 and all(type(x) is int for x in raw)
        points={x%n for x in raw};assert len(points)==6
        endpoint=tuple(c[side]);assert canonical(points,n)==endpoint
        w=c['input_alignment_'+side];assert motion(points,n,w['sign'],w['shift'])==set(endpoint)
        inputs.append(endpoint)
    a,b=inputs;assert differences(a,n)==differences(b,n)
    scale=gcd(n,*a,*b);q=n//scale;assert c['ordinary_support']==dict(modulus=q,scale=scale)
    if c['route']=='TI':assert a==b;vertices=[a]
    elif c['route']=='direct':direct(a,b,n,c['certificate']);vertices=[a,b]
    else:
        assert c['route']=='finite_path';path=c['path'];assert path['modulus']==q and q<=135
        points=list(map(tuple,path['vertices']));assert len(points)==len(path['edges'])+1
        assert points[0]==tuple(x//scale for x in a) and points[-1]==tuple(x//scale for x in b)
        for x,y,edge in zip(points,points[1:],path['edges']):assert set(saved(edge,q))=={x,y}
        vertices=[tuple(scale*x for x in v) for v in points]
    if 'vertices' in c:assert list(map(tuple,c['vertices']))==vertices
    return vertices


def reject(call):
    try:call()
    except (ValueError,AssertionError,KeyError,TypeError,IndexError):return
    raise AssertionError('malicious certificate accepted')


def brute_block_exists(a,b,n):
    """All 2n rigid alignments and all63 A masks, independent of discovery."""
    a,b=set(a),set(b);ordered=sorted(a)
    for sign in (-1,1):
        for shift in range(n):
            bb=motion(b,n,sign,shift)
            for mask in range(1,63):
                fixed={x for i,x in enumerate(ordered) if mask>>i&1}
                if not fixed<=bb:continue
                moving=a-fixed;other=bb-fixed
                for local_sign in (-1,1):
                    for delta in range(n):
                        if motion(moving,n,local_sign,delta)!=other:continue
                        p=Counter((u-w)%n for u in fixed for w in moving)
                        changed=Counter((u-local_sign*w-delta)%n for u in fixed for w in moving)
                        if changed==p:return True
                        if local_sign==1:
                            if changed==Counter((w-u)%n for u in fixed for w in moving):return True
                            if 2*delta%n==0 and changed+Counter((delta+w-u)%n for u in fixed for w in moving)==p+Counter((w-u)%n for u in fixed for w in moving):return True
    return False


def main():
    started=time.monotonic();rng=Random(6302026);out=ROOT/'results/2026-09-30-six-generate-review';out.mkdir(exist_ok=True)
    # Independently validate our gap-word canon against the protected reference.
    from homometry import dihedral_canon
    for n in range(6,22):
        for _ in range(20):
            a=rng.sample(range(n),6);assert canonical(a,n)==dihedral_canon(a,n)
    supplied=ROOT/'results/2026-09-30-six-generate'
    paths=json.loads((supplied/'all-73-finite-paths.json').read_text());labels=Counter()
    for cert in paths:
        assert portable(cert)==driver.replay(cert)
        for edge in cert['path']['edges']:labels[edge['label']]+=1
    large_cases=0
    for path in supplied.glob('*.json'):
        data=json.loads(path.read_text())
        if isinstance(data,dict) and data.get('schema')=='six-generation-v1':
            assert portable(data)==driver.replay(data);large_cases+=1
    # Exercise every legacy edge label independently and reject altered labels.
    representatives={}
    for n in range(12,136):
        report=json.loads((ROOT/f'results/2026-09-30-six-pair-mechanisms/n{n}.json').read_text())
        for edge in report['certificates']:representatives.setdefault(edge['label'],(n,edge))
        if len(representatives)==9:break
    for n,edge in representatives.values():
        assert saved(edge,n)==driver.verify_saved(edge,n)
        bad=deepcopy(edge);bad['label']='not-a-mechanism';reject(lambda:driver.verify_saved(bad,n))
    # Regression for the reviewed bug: the halfcoset partner is DISJOINT
    # from A, so alignments constructed by forcing an intersection miss it.
    a=(0,1,3,4,9,11);b=(0,1,3,9,11,12)
    c=driver.generate(16,a,b);assert c['certificate']['label']=='L7';portable(c)
    a=(0,100003,1,200007,3,200009);n=400012;step=n//4
    b={r+j*step for r in {x%step for x in a} for j in range(4)}-set(a)
    c=driver.generate(n,a,b);assert c['certificate']['label']=='L7';portable(c)
    # Exhaustive independent small-ring block-search comparison. Disable
    # earlier mechanisms only during discovery, leaving the verifier intact.
    block_pairs=[]
    for n in range(12,19):
        report=json.loads((ROOT/f'results/2026-09-30-six-pair-mechanisms/n{n}.json').read_text())
        for edge in report['certificates']:
            block_pairs.append((n,edge['a'],edge['b']))
            if len(block_pairs)==40:break
        if len(block_pairs)==40:break
    originals={k:getattr(driver,k) for k in ('bloom_certificate','dyad_certificate','halfcoset_certificate')}
    try:
        for k in originals:setattr(driver,k,lambda *args:None)
        for n,a,b in block_pairs:
            exists=brute_block_exists(a,b,n);c=driver.direct_certificate(a,b,n)
            if exists:assert c is not None,(n,a,b)
            if c:
                direct(a,b,n,c)
                if c['label']!='R':assert exists
    finally:
        for k,v in originals.items():setattr(driver,k,v)
    # Cover all six-distinct Bloom instances in several small rings, all
    # swapped sides and independently reflected input endpoints.
    bloom_count=0
    for n in (12,13,17,22,31,47,1000000007):
        parameters=product(range(n),repeat=2) if n<50 else [(1234567,98765431),(1,6),(-3,13)]
        for p,q in parameters:
            a,b=bloom(p,q,n)
            if len(a)!=6 or len(b)!=6 or canonical(a,n)==canonical(b,n):continue
            a=motion(a,n,-1,7);b=motion(b,n,1,11)
            if bloom_count%2:a,b=b,a
            c=driver.bloom_certificate(a,b,n);assert c is not None,(n,p,q)
            direct(a,b,n,c);bloom_count+=1
    # Sample every formal low-rank terminal in large targets. This attacks
    # driver specialization independently of finite-modulus census data.
    atlas=json.loads((ROOT/'results/2026-09-30-six-free-mechanisms/atlas.json').read_text())
    projected=0;nontrivial=0;large_support=0;skips=0;routes=Counter();direct_examples={}
    for record in atlas['records']:
        options=record.get('cyclic_quotients',[record])
        for option in options:
            if option['certificate']['label'] in ('collision','ti'):continue
            orders=option['orders'];torsion=[d for d in orders if d]
            modulus=1000003
            for d in torsion:modulus=modulus*d//gcd(modulus,d)
            for _ in range(2):
                coefficients=[modulus//d*rng.randrange(d) if d else rng.randrange(modulus) for d in orders]
                images=[{sum(c*x for c,x in zip(coefficients,p))%modulus for p in option[side]} for side in ('a','b')]
                if any(len(a)!=6 for a in images):skips+=1;continue
                projected+=1
                if canonical(images[0],modulus)==canonical(images[1],modulus):continue
                nontrivial+=1;cert=driver.generate(modulus,*images)
                assert portable(cert)==driver.replay(cert)
                large_support+=cert['ordinary_support']['modulus']>135
                routes[(cert['route'],cert.get('certificate',{}).get('label'))]+=1
                if cert['route']=='direct':direct_examples.setdefault(cert['certificate']['label'],cert)
    assert nontrivial>300 and large_support>300
    # Force every saved finite path through the public fallback after ordinary
    # inflation with independent endpoint translations and reflections.
    for index,old in enumerate(paths):
        q=old['n'];a,b=old['a'],old['b'];scale=1009
        cert=driver.generate(q*scale,[scale*x+3 for x in a],[-scale*x+17 for x in b],True)
        assert cert['route']=='finite_path' and portable(cert)==driver.replay(cert)
    # Replay must depend on embedded finite edges, not discovery or disk tables.
    cert=deepcopy(paths[0]);originals={k:getattr(driver,k) for k in ('finite_graph','finite_path','direct_certificate','bloom_certificate')}
    try:
        for k in originals:setattr(driver,k,lambda *args:(_ for _ in ()).throw(AssertionError('replay used discovery')))
        assert driver.replay(cert)==portable(cert)
    finally:
        for k,v in originals.items():setattr(driver,k,v)
    bads=[]
    for field,value in [('schema','forged-v1'),('n',True),('route','imaginary')]:
        bad=deepcopy(cert);bad[field]=value;bads.append(bad)
    bad=deepcopy(cert);bad['ordinary_support']['scale']+=1;bads.append(bad)
    bad=deepcopy(cert);bad['input_alignment_a']['sign']=0;bads.append(bad)
    bad=deepcopy(cert);bad['path']['modulus']+=1;bads.append(bad)
    bad=deepcopy(cert);bad['path']['vertices'][0][1]+=1;bads.append(bad)
    bad=deepcopy(cert);bad['path']['edges'][0]['label']='unit';bad['path']['edges'][0]['u']=0;bads.append(bad)
    bad=deepcopy(cert);bad['input_a'][0]=bad['input_a'][1];bads.append(bad)
    bad=deepcopy(cert);bad['vertices'][0][1]+=1;bads.append(bad)
    bad=deepcopy(cert);bad['input_alignment_a']['shift']=float(bad['input_alignment_a']['shift']);bads.append(bad)
    bad=deepcopy(cert);bad['path']['edges'][0]['unexpected_bool']=True;bads.append(bad)
    for bad in bads:reject(lambda:driver.replay(bad))
    direct_tampers=0
    for label,example in direct_examples.items():
        bad=json.loads(json.dumps(example));c=bad['certificate']
        if label=='Bloom':c['y_sign']=0
        elif label=='D':c['weight'][0][1]+=1
        elif label=='L7':c['order']=3
        else:c['fixed']=[]
        reject(lambda:driver.replay(bad));direct_tampers+=1
    reject(lambda:driver.generate(17,(0,1,2,3,4,5),(0,1,2,3,4,6)))
    result=dict(status='PASS independent executable/certificate audit',portable_saved_paths=len(paths),large_saved_cases=large_cases,
                legacy_labels=sorted(representatives),exhaustive_block_pair_controls=len(block_pairs),halfcoset_regression_controls=2,bloom_parameter_controls=bloom_count,projected_valid_pairs=projected,
                projected_nontrivial_pairs=nontrivial,projected_support_above135=large_support,projection_collisions_skipped=skips,
                generated_routes=[dict(route=k[0],label=k[1],count=v) for k,v in routes.items()],
                malicious_rejections=len(bads)+len(representatives)+direct_tampers,nonhomometric_input_rejections=1,seconds=round(time.monotonic()-started,3),
                source_sha256=hashlib.sha256((ROOT/'src/six_generate.py').read_bytes()).hexdigest())
    (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(result,flush=True)

if __name__=='__main__':main()
