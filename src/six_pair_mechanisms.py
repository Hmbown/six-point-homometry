"""Targeted L2--L7 and dyad-shape certificates without a 64-bit modulus cap.

Discovery is independent of the old bitset partner menu. Every accepted edge
has a concrete partition/alignment and an exact sufficient algebraic condition.
This module does not assert these mechanisms are complete.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter
from math import gcd
import argparse,json,time
import numpy as np
from numba import njit
ROOT=Path(__file__).resolve().parents[1]
LABELS=('none','translate','swap','halfturn','reflect','dyad','halfcoset','unit')

@njit(cache=True)
def block_certificate(a,b,n):
    aa=np.zeros(n,np.int64)
    for x in a:aa[x]=1
    # Most matches use the whole common block. Enumerate all subblocks as
    # well: moving a block can leave some of its points in the intersection.
    for sign in (1,-1):
        for shift in range(n):
            bb=np.zeros(n,np.int64)
            for x in b:bb[(sign*x+shift)%n]=1
            shared=0
            for i in range(6):
                if bb[a[i]]:shared|=1<<i
            sub=shared
            while sub:
                u=np.empty(6,np.int64);w=np.empty(6,np.int64);wp=np.empty(6,np.int64)
                nu=0;nw=0;ny=0
                for i in range(6):
                    if sub>>i&1:u[nu]=a[i];nu+=1
                    else:w[nw]=a[i];nw+=1
                for y in range(n):
                    if not bb[y]:continue
                    keep=True
                    for j in range(nu):
                        if u[j]==y:keep=False
                    if keep:wp[ny]=y;ny+=1
                if nw==0:sub=(sub-1)&shared;continue
                # D: maximal common four points and equal dyad sums.
                if nu==4 and sub==shared and (w[0]+w[1]-wp[0]-wp[1])%n==0:
                    return (5,sign,shift,sub,0)
                p=np.zeros(n,np.int64);r=np.zeros(n,np.int64)
                for i in range(nu):
                    for j in range(nw):
                        p[(u[i]-w[j])%n]+=1;r[(u[i]+w[j])%n]+=1
                for k in range(nw):
                    v=(wp[k]-w[0])%n;ok=True
                    for j in range(nw):
                        y=(w[j]+v)%n;found=False
                        for t in range(nw):
                            if wp[t]==y:found=True
                        if not found:ok=False;break
                    if ok:
                        periodic=True;swap=True;half=n%2==0 and v==n//2
                        for g in range(n):
                            if p[g]!=p[(g+v)%n]:periodic=False
                            if p[(g+v)%n]!=p[-g%n]:swap=False
                            if half and p[g]+p[-g%n]!=p[(g+v)%n]+p[(-g-v)%n]:half=False
                        if periodic:return (1,sign,shift,sub,v)
                        if swap and (n%2==1 or v%2==0):return (2,sign,shift,sub,v)
                        if half:return (3,sign,shift,sub,v)
                    s=(wp[k]+w[0])%n;ok=True
                    for j in range(nw):
                        y=(s-w[j])%n;found=False
                        for t in range(nw):
                            if wp[t]==y:found=True
                        if not found:ok=False;break
                    if ok:
                        condition=True
                        for g in range(n):
                            if p[g]!=r[(g+s)%n]:condition=False;break
                        if condition:return (4,sign,shift,sub,s)
                sub=(sub-1)&shared
    return (0,0,0,0,0)

def verify_block(a,b,n,c):
    """Pure integer/Counter verifier; imports no discovery kernel helpers."""
    label,sign,shift,sub,v=map(int,c)
    assert label in range(1,6)
    u={x for i,x in enumerate(a) if sub>>i&1};w=set(a)-u
    image={(sign*x+shift)%n for x in b};assert u<=image
    wp=image-u
    p=Counter((x-y)%n for x in u for y in w)
    if label==5:
        from six_shell import shape_certificate
        assert len(u)==4 and len(w)==len(wp)==2 and (sum(w)-sum(wp))%n==0
        assert shape_certificate(a,b,n) is not None
    elif label==4:
        assert wp=={(v-x)%n for x in w}
        r=Counter((x+y)%n for x in u for y in w)
        assert all(p[g]==r[(g+v)%n] for g in range(n))
    else:
        assert wp=={(x+v)%n for x in w}
        if label==1:assert all(p[g]==p[(g+v)%n] for g in range(n))
        if label==2:assert (n%2 or v%2==0) and all(p[(g+v)%n]==p[-g%n] for g in range(n))
        if label==3:assert n%2==0 and v==n//2 and all(p[g]+p[-g%n]==p[(g+v)%n]+p[(-g-v)%n] for g in range(n))
    return True

def quick_certificate(a,b,n):
    from six_explore import canon,icv
    if len(set(a))!=6 or len(set(b))!=6 or icv(a,n)!=icv(b,n):
        raise ValueError('targeted recognition requires a homometric pair of six-subsets')
    # Cheap subgroup complement before partition work.
    for h in (2,4,6,12):
        if n%h:continue
        step=n//h;counts=Counter(x%step for x in a)
        if all(c==h//2 for c in counts.values()):
            other={c+step*j for c in counts for j in range(h)}-set(a)
            if canon(other,n)==b:return dict(label='halfcoset',h=h)
    c=block_certificate(np.array(a,dtype=np.int64),np.array(b,dtype=np.int64),n)
    if c[0]:
        verify_block(a,b,n,c)
        return dict(label=LABELS[c[0]],certificate=list(map(int,c)))
    for u in range(2,n):
        if gcd(u,n)==1 and canon((u*x for x in a),n)==b:
            auto=Counter((x-y)%n for x in a for y in a)
            assert all(auto[g]==auto[(u*g)%n] for g in range(n))
            return dict(label='unit',u=u)
    return None

def main():
    p=argparse.ArgumentParser();p.add_argument('--nmin',type=int,default=12);p.add_argument('--nmax',type=int,default=135)
    p.add_argument('--resume',action='store_true');p.add_argument('--out',type=Path,default=ROOT/'results/2026-09-30-six-pair-mechanisms')
    args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    from six_explore import bloom_edges
    from six_templates import SEEDS
    from six_explore import canon
    for n in range(args.nmin,args.nmax+1):
        dest=args.out/f'n{n}.json'
        if args.resume and dest.exists():continue
        source=ROOT/f'results/2026-09-30-six-large-census/n{n}.json'
        if not source.exists():source=ROOT/f'results/2026-09-30-six-census/n{n}.json'
        if not source.exists():print(f'n={n} awaiting census',flush=True);break
        started=time.monotonic();families=json.loads(source.read_text())['families'];blooms=bloom_edges(n)
        rigid={}
        for index,(q,x,y) in enumerate(SEEDS):
            for t in range(n):
                if q*t%n:continue
                aa,bb=canon((z*t for z in x),n),canon((z*t for z in y),n)
                if len(aa)==len(bb)==6 and aa!=bb:rigid[tuple(sorted((aa,bb)))]=(index+1,t)
        counts=Counter();gaps=[];certificates=[]
        for f in families:
            members=sorted(tuple(x) for x in f['members'])
            for a,b in combinations(members,2):
                pair=a,b
                if pair in blooms:c=dict(label='Bloom',parameters=blooms[pair])
                elif pair in rigid:c=dict(label='R',parameters=rigid[pair])
                else:c=quick_certificate(a,b,n)
                if c is None:gaps.append(pair);counts['gap']+=1
                else:counts[c['label']]+=1;certificates.append(dict(a=a,b=b,**c))
        # Connectivity, rather than direct coverage of every pair edge, is
        # the move grammar's criterion. Keep missing edges for audit.
        known={tuple(sorted((tuple(c['a']),tuple(c['b'])))) for c in certificates}
        disconnected=[]
        for f in families:
            members=list(map(tuple,f['members']));seen={members[0]}
            while True:
                more=seen|{y for x in seen for y in members if tuple(sorted((x,y))) in known}
                if more==seen:break
                seen=more
            if len(seen)!=len(members):disconnected.append(members)
        report=dict(n=n,counts=dict(counts),gaps=gaps,disconnected_families=disconnected,certificates=certificates,seconds=round(time.monotonic()-started,3),status='COMPUTED exact certificates; selected mechanism coverage only')
        temp=dest.with_suffix('.tmp');temp.write_text(json.dumps(report,sort_keys=True)+'\n');temp.replace(dest)
        print(n,dict(counts),report['seconds'],flush=True)

if __name__=='__main__':main()
