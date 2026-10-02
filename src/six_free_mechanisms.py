"""Exact sufficient mechanisms for formal six-sets in Z^r plus finite torsion.

This is an atlas builder, not an independent certificate verifier.  In contrast
to the exploratory broad block recognizer, each label below has an explicit
sufficient group-ring condition. Unrecognized pairs remain explicit templates.
"""
from __future__ import annotations
import argparse,gzip,json,time
from collections import Counter
from itertools import combinations,product
from math import gcd,lcm
from pathlib import Path
from six_free_rank import group_add,group_neg,group_sub,group_image,group_canon
ROOT=Path(__file__).resolve().parents[1]


def scale(x,n,orders):return tuple((n*a)%d if d else n*a for a,d in zip(x,orders))
def autocorrelation(a,orders):return Counter(group_sub(x,y,orders) for x in a for y in a)
def counter_shift(c,s,orders):return Counter({group_add(x,s,orders):v for x,v in c.items()})
def counter_reflect(c,orders):return Counter({group_neg(x,orders):v for x,v in c.items()})
def align(a,b,orders):
    """Return all rigid images of B meeting A, with exact alignment witnesses."""
    seen=set()
    for sign in (1,-1):
        for x in sorted(a):
            for y in sorted(b):
                shift=group_sub(x,scale(y,sign,orders),orders)
                image=group_image(b,sign,shift,orders)
                if image in seen:continue
                seen.add(image);yield image,sign,shift


def ti_certificate(a,b,orders):
    for image,sign,shift in align(a,b,orders):
        if image==a:return dict(label='ti',b_sign=sign,b_shift=shift)
    return None


def bloom_certificate(a,b,orders):
    zero=(0,)*len(orders)
    for anchor in sorted(a):
        aa=group_image(a,1,group_neg(anchor,orders),orders)
        for p in aa-{zero}:
            for x in aa-{zero,p}:
                q=group_add(x,scale(p,2,orders),orders)
                def z(i,j):return group_add(scale(p,i,orders),scale(q,j,orders),orders)
                first=frozenset((zero,p,z(-2,1),z(-2,2),z(0,2),z(-1,3)))
                if first!=aa:continue
                second=frozenset((zero,p,z(2,1),z(-1,2),z(1,2),z(-1,3)))
                c=ti_certificate(second,b,orders)
                if c:return dict(label='Bloom',anchor=anchor,p=p,q=q,b_sign=c['b_sign'],b_shift=c['b_shift'])
    return None


def halfcoset_certificate(a,b,orders):
    torsion=[d for d in orders if d];r=len(orders)-len(torsion)
    seen=set();zero=(0,)*len(orders)
    for part in product(*(range(d) for d in torsion)):
        h=tuple(part)+(0,)*r
        order=lcm(*(d//gcd(x,d) for x,d in zip(part,torsion))) if torsion else 1
        if order not in (2,4,6,12):continue
        subgroup=frozenset(scale(h,i,orders) for i in range(order))
        if subgroup in seen:continue
        seen.add(subgroup);cosets={min(group_add(x,y,orders) for y in subgroup) for x in a}
        union=set()
        for anchor in cosets:
            coset={group_add(anchor,y,orders) for y in subgroup}
            if len(a&coset)!=order//2:break
            union.update(coset)
        else:
            other=frozenset(union-a);c=ti_certificate(other,b,orders)
            if c:return dict(label='halfcoset',generator=h,order=order,b_sign=c['b_sign'],b_shift=c['b_shift'])
    return None


def strict_block_certificate(a,b,orders):
    zero=(0,)*len(orders)
    for image,sign,shift in align(a,b,orders):
        common=sorted(a&image)
        for mask in range((1<<len(common))-1,0,-1):
            u=frozenset(x for i,x in enumerate(common) if mask>>i&1)
            w=a-u;wp=image-u
            if not w:continue
            p=Counter(group_sub(x,y,orders) for x in u for y in w)
            reflected=counter_reflect(p,orders);r=Counter(group_add(x,y,orders) for x in u for y in w)
            anchor=min(w)
            for target in sorted(wp):
                v=group_sub(target,anchor,orders)
                if group_image(w,1,v,orders)==wp:
                    if counter_shift(p,v,orders)==p:label='translate'
                    elif counter_shift(p,group_neg(v,orders),orders)==reflected:label='cosymmetric_translate'
                    elif v!=zero and scale(v,2,orders)==zero and counter_shift(p+reflected,v,orders)==p+reflected:label='halfturn'
                    else:label=None
                    if label:return dict(label=label,b_sign=sign,b_shift=shift,common=sorted(u),move=v)
                v=group_add(target,anchor,orders)
                if group_image(w,-1,v,orders)==wp and p==counter_shift(r,group_neg(v,orders),orders):
                    return dict(label='reflect',b_sign=sign,b_shift=shift,common=sorted(u),move=v)
    return None


def dyad_certificate(a,b,orders):
    """The reviewed D parallelogram exchange with its exact kernel condition."""
    zero=(0,)*len(orders)
    for image,sign,shift in align(a,b,orders):
        common=a&image;removed=a-image;added=image-a
        if len(common)!=4 or len(removed)!=2 or len(added)!=2:continue
        x,y=sorted(removed);u,v=sorted(added)
        if group_add(x,y,orders)!=group_add(u,v,orders):continue
        c=frozenset(group_sub(z,x,orders) for z in common)
        s=group_sub(u,x,orders);t=group_sub(v,x,orders);center=group_add(s,t,orders)
        w=Counter(c)+Counter(group_sub(center,z,orders) for z in c)+Counter((zero,s,t,center))
        coefficients=Counter()
        for factor,term in ((1,w),(-1,counter_shift(w,s,orders)),(-1,counter_shift(w,t,orders)),(1,counter_shift(w,center,orders))):
            for z,count in term.items():coefficients[z]+=factor*count
        if any(coefficients.values()):continue
        return dict(label='dyad',b_sign=sign,b_shift=shift,anchor=x,common=sorted(c),steps=[s,t])
    return None


def classify(a,b,orders):
    a,b=frozenset(map(tuple,a)),frozenset(map(tuple,b));orders=tuple(orders)
    if len(a)!=6 or len(b)!=6:return dict(label='collision')
    assert autocorrelation(a,orders)==autocorrelation(b,orders)
    for method in (ti_certificate,halfcoset_certificate,bloom_certificate,strict_block_certificate,dyad_certificate):
        c=method(a,b,orders)
        if c:return c
    return dict(label='template')


def cyclic_quotients(a,b,torsion,free_rank):
    """Every character of finite torsion, restricted to its actual cyclic image.

    Each finite-image character into any cyclic group factors through one of
    these maps. Free generators remain unrestricted; no distinct T/I classes
    in a target cyclic group are identified by this enumeration.
    """
    exponent=lcm(*torsion) if torsion else 1;nt=len(torsion)
    for labels in product(*(range(d) for d in torsion)):
        coefficients=tuple(exponent//d*j for d,j in zip(torsion,labels))
        divisor=gcd(exponent,*coefficients);order=exponent//divisor
        def project(x):
            t=sum(c*y for c,y in zip(coefficients,x[:nt]))//divisor%order
            return ((t,) if order>1 else ())+tuple(x[nt:])
        aa,bb=tuple(map(project,a)),tuple(map(project,b));orders=((order,) if order>1 else ())+(0,)*free_rank
        yield dict(character=labels,coefficients=coefficients,exponent=exponent,image_order=order,
                   a=aa,b=bb,orders=orders,certificate=classify(aa,bb,orders))


def main():
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,default=ROOT/'results/2026-09-30-six-free-dag-all')
    p.add_argument('--out',type=Path,default=ROOT/'results/2026-09-30-six-free-mechanisms');p.add_argument('--resume',action='store_true');args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    summary=json.loads((args.base/'summary.json').read_text());started=time.monotonic();hist=Counter();qh=Counter();records=[]
    for stratum in summary['strata']:
        stem=f'rank{stratum["rank"]}-orbit{stratum["orbit"]:03}';dest=args.out/f'{stem}.json'
        if args.resume and dest.exists():data=json.loads(dest.read_text())
        else:
            with gzip.open(args.base/f'{stem}.json.gz','rt') as f:dag=json.load(f)
            data=[]
            for node in dag['nodes']:
                if node.get('terminal')!='homometric':continue
                orders=tuple(node['torsion'])+(0,)*node['free_rank']
                cert=classify(node['a'],node['b'],orders)
                record=dict(node=node['id'],orders=orders,a=node['a'],b=node['b'],certificate=cert)
                if cert['label']=='template':record['cyclic_quotients']=list(cyclic_quotients(node['a'],node['b'],node['torsion'],node['free_rank']))
                data.append(record)
            dest.write_text(json.dumps(data,sort_keys=True)+'\n')
        for record in data:
            hist[record['certificate']['label']]+=1
            for q in record.get('cyclic_quotients',[]):qh[q['certificate']['label']]+=1
            records.append(dict(stratum=stem,**record))
        print(stem,dict(hist),dict(qh),'seconds',round(time.monotonic()-started,2),flush=True)
    report=dict(status='COMPUTED-UNVALIDATED exact group mechanisms and cyclic-image templates',terminal_count=len(records),histogram=dict(hist),cyclic_quotient_histogram=dict(qh),records=records,seconds=time.monotonic()-started)
    (args.out/'atlas.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print({k:v for k,v in report.items() if k!='records'},flush=True)

if __name__=='__main__':main()
