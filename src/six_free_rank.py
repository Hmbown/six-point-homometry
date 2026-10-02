"""Exact high-free-rank matching exploration via codimension-two height spans.

This module does not assume the false bound free rank <=2. The rank-three
C2 example is retained as a regression obstruction. Generic real projections
with rank>=3 must be TI conditional on the separately reviewed weighted-line
classification; this module enumerates the TI projection cases.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict,deque
from itertools import combinations,permutations,product
from math import factorial,gcd
from pathlib import Path
import gzip,json,time

ROOT=Path(__file__).resolve().parents[1]
EDGES=tuple(combinations(range(6),2))


def primitive(row):
    row=tuple(row);g=gcd(*row)
    if not g:return ()
    s=1 if next(x for x in row if x)>0 else -1
    return tuple(s*x//g for x in row)


def canonical_span(rows):
    """Unique primitive row-scaled rational RREF, for rank at most two."""
    rows=[primitive(row) for row in rows if any(row)]
    if not rows:return ()
    a=rows[0];p=next(i for i,x in enumerate(a) if x)
    if len(rows)==1:return (a,)
    b=primitive(tuple(a[p]*y-rows[1][p]*x for x,y in zip(a,rows[1])))
    if not b:return (a,)
    q=next(i for i,x in enumerate(b) if x)
    a=primitive(tuple(b[q]*x-a[q]*y for x,y in zip(a,b)))
    return tuple(sorted((a,b),key=lambda row:next(i for i,x in enumerate(row) if x)))


def extend_span(rows,vector):
    """Adjoin a row to any primitive integer-scaled rational RREF."""
    v=primitive(vector)
    if not v:return tuple(rows)
    for row in rows:
        p=next(i for i,x in enumerate(row) if x)
        if v[p]:v=primitive(tuple(row[p]*x-v[p]*y for x,y in zip(v,row)))
        if not v:return tuple(rows)
    q=next(i for i,x in enumerate(v) if x)
    result=[]
    for row in rows:
        result.append(primitive(tuple(v[q]*x-row[q]*y for x,y in zip(row,v))) if row[q] else tuple(row))
    result.append(v)
    return tuple(sorted(result,key=lambda row:next(i for i,x in enumerate(row) if x)))


def general_span(rows):
    """Canonical rational span in six coordinates, with arbitrary row rank."""
    out=()
    for row in rows:out=extend_span(out,row)
    return out


def next_span_orbits(previous_orbits,rank):
    """All rank-r S6 orbits, by extending representatives of rank r-1.

    Every orbit occurs because the direction set is S6-invariant. The
    candidate set need not itself be closed under all permutations.
    """
    ds=directions();candidates={extend_span(tuple(map(tuple,row['rows'])),d)
                             for row in previous_orbits if len(row['rows'])==rank-1 for d in ds}
    candidates={rows for rows in candidates if len(rows)==rank}
    original_count=len(candidates);result=[];perms=list(permutations(range(6)))
    started=time.monotonic()
    while candidates:
        representative=min(candidates);orbit=set()
        for perm in perms:
            orbit.add(general_span([tuple(row[i] for i in perm) for row in representative]))
        candidates-=orbit
        result.append(dict(rows=min(orbit),size=len(orbit)))
        if len(result)%10==0:print('rank',rank,'orbits',len(result),'unclassified candidates',len(candidates),'seconds',round(time.monotonic()-started,2),flush=True)
    return dict(rank=rank,extension_candidates=original_count,orbits=result,
                spans=sum(row['size'] for row in result),seconds=time.monotonic()-started)


def directions():
    roots=[]
    for i in range(6):
        for j in range(6):
            if i!=j:roots.append(tuple(int(k==i)-int(k==j) for k in range(6)))
    return tuple(sorted({primitive(tuple(x-y for x,y in zip(a,b)))
                        for a in roots for b in roots if a!=b}))


def height_spans():
    ds=directions();spans={()}|{(d,) for d in ds}
    spans|={canonical_span(pair) for pair in combinations(ds,2)}
    unseen=set(spans);orbits=[]
    while unseen:
        seed=min(unseen,key=lambda rows:(len(rows),rows));orbit={seed};todo=[seed]
        while todo:
            rows=todo.pop()
            for i in range(5):
                swapped=[]
                for row in rows:
                    other=list(row);other[i],other[i+1]=other[i+1],other[i];swapped.append(other)
                target=canonical_span(swapped)
                assert target in spans
                if target not in orbit:orbit.add(target);todo.append(target)
        unseen-=orbit;orbits.append(dict(rows=seed,size=len(orbit)))
    return ds,spans,orbits


def generic_heights(rows,ds):
    anchored=general_span([row[1:] for row in rows]);pivots=[next(i for i,x in enumerate(row) if x) for row in anchored]
    free=[j for j in range(5) if j not in pivots]
    # Membership for rank two uses elimination of one candidate, not rank-three RREF.
    def member(d):
        v=list(d)
        for row in rows:
            p=next(i for i,x in enumerate(row) if x)
            v=[row[p]*x-v[p]*y for x,y in zip(v,row)]
        return not any(v)
    for base in range(2,100):
        scale=1
        for row in anchored:scale*=next(x for x in row if x)
        vals=[0]*5
        for i,j in enumerate(free):vals[j]=scale*base**i
        for row,p in zip(anchored,pivots):
            numerator=-sum(row[j]*vals[j] for j in free)
            assert numerator%row[p]==0;vals[p]=numerator//row[p]
        h=(0,*vals)
        if all((sum(x*y for x,y in zip(d,h))==0)==member(d) for d in ds):return h
    raise RuntimeError('no generic integer specialization found')


def isolated_singleton(h):
    """A universally translating star: each incident length identifies one fiber.

    No other edge may share that absolute length, except edges from the same
    singleton to points of exactly the same height (not the reflected height).
    """
    buckets=defaultdict(list)
    for i,j in EDGES:buckets[abs(h[j]-h[i])].append((i,j))
    for center in range(6):
        if h.count(h[center])!=1:continue
        valid=True
        for other in range(6):
            if other==center:continue
            d=abs(h[other]-h[center])
            for edge in buckets[d]:
                if center not in edge:
                    valid=False;break
                target=edge[1] if edge[0]==center else edge[0]
                if h[target]!=h[other]:valid=False;break
            if not valid:break
        if valid:return center
    return None


def line_matching_count(h):
    counts=Counter(abs(h[j]-h[i]) for i,j in EDGES)
    total=1
    for distance,count in counts.items():total*=factorial(count)*(2**count if distance==0 else 1)
    return total,dict(sorted(counts.items()))


def line_matchings(h):
    buckets=defaultdict(list)
    for edge in EDGES:
        i,j=edge;buckets[abs(h[j]-h[i])].append(edge)
    distances=sorted(buckets)
    def rec(index,labels):
        if index==len(distances):yield labels;return
        d=distances[index];edges=buckets[d]
        for targets in permutations(edges):
            signs=product((-1,1),repeat=len(edges)) if d==0 else [tuple(1 if (h[j]-h[i])==(h[l]-h[k]) else -1 for (i,j),(k,l) in zip(edges,targets))]
            for ss in signs:
                block=tuple((i,j,k,l,s) for (i,j),(k,l),s in zip(edges,targets,ss))
                yield from rec(index+1,labels+block)
    return rec(0,())


def benchmark():
    started=time.monotonic();ds,spans,orbits=height_spans();rows=[]
    for i,orbit in enumerate(orbits):
        h=generic_heights(orbit['rows'],ds);count,buckets=line_matching_count(h)
        row=dict(index=i,**orbit,heights=h,matching_count=count,distance_multiplicities=list(buckets.values()),distinct_heights=len(set(h)))
        rows.append(row)
    return dict(status='EXPLORATORY until independent span and matching completeness audit',directions=len(ds),spans=len(spans),orbits=rows,
                total_orbit_matchings=sum(row['matching_count'] for row in rows),seconds=time.monotonic()-started)


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=ROOT/'results/2026-09-30-six-free-rank');p.add_argument('--classify',action='store_true');p.add_argument('--growth',action='store_true');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    report=benchmark();(a.out/'spans.json').write_text(json.dumps(report,indent=2)+'\n')
    print({k:v for k,v in report.items() if k!='orbits'},flush=True)
    for row in report['orbits']:print(row,flush=True)
    if a.classify:print(classify_presentations(a.out),flush=True)
    if a.growth:growth_benchmark(a.out)



def matching_matrix(labels):
    from sympy import Matrix
    out=[]
    for i,j,k,l,s in labels:
        row=[0]*10
        if i:row[i-1]-=1
        if j:row[j-1]+=1
        if k:row[k+4]+=s
        if l:row[l+4]-=s
        out.append(row)
    return Matrix(out)


def group_add(a,b,orders):
    return tuple((x+y)%d if d else x+y for x,y,d in zip(a,b,orders))
def group_neg(a,orders):return tuple(-x%d if d else -x for x,d in zip(a,orders))
def group_sub(a,b,orders):return group_add(a,group_neg(b,orders),orders)
def group_image(points,sign,shift,orders):
    return frozenset(group_add(x if sign==1 else group_neg(x,orders),shift,orders) for x in points)
def group_canon(points,orders):
    return min(tuple(sorted(group_image(points,sign,group_neg(anchor if sign==1 else group_neg(anchor,orders),orders),orders)))
               for anchor in points for sign in (1,-1))


def block_certificate(a,b,orders):
    """Find an exact aligned block reflection/translation in the universal group."""
    best=None
    for sign in (1,-1):
        for x in a:
            for y in b:
                shift=group_sub(x,y if sign==1 else group_neg(y,orders),orders)
                image=group_image(b,sign,shift,orders)
                removed=a-image;added=image-a
                if not removed or len(removed)!=len(added):continue
                if best is not None and len(removed)>=best['moved']:continue
                for local_sign in (1,-1):
                    anchor=next(iter(removed))
                    for target in added:
                        local_shift=group_sub(target,anchor if local_sign==1 else group_neg(anchor,orders),orders)
                        if group_image(removed,local_sign,local_shift,orders)==added:
                            best=dict(moved=len(removed),b_sign=sign,b_shift=shift,
                                      block_sign=local_sign,block_shift=local_shift,
                                      common=sorted(a&image),removed=sorted(removed),added=sorted(added))
    return best


def master_certificate(common,removed,added,orders):
    """Identify C={0,p,q,p-q+h} and antipodal reflected dyads exactly."""
    zero=(0,)*len(orders);common=list(map(tuple,common));removed=list(map(tuple,removed));added=frozenset(map(tuple,added))
    if len(common)!=4 or len(removed)!=2:return None
    h=group_sub(removed[1],removed[0],orders)
    if h==zero or group_add(h,h,orders)!=zero:return None
    for base,partner in permutations(common,2):
        center=group_add(base,partner,orders)
        if group_image(removed,-1,center,orders)!=added:continue
        rest=[x for x in common if x not in (base,partner)]
        p=group_sub(partner,base,orders);q=group_sub(rest[0],base,orders)
        target=group_add(group_sub(p,q,orders),h,orders)
        if group_sub(rest[1],base,orders)!=target:continue
        r=group_sub(removed[0],base,orders)
        return dict(base=base,p=p,q=q,r=r,h=h)
    return None


def universal_master(a,b,orders):
    for sign in (1,-1):
        for x in a:
            for y in b:
                shift=group_sub(x,y if sign==1 else group_neg(y,orders),orders)
                image=group_image(b,sign,shift,orders)
                cert=master_certificate(a&image,a-image,image-a,orders)
                if cert is not None:return dict(b_sign=sign,b_shift=shift,**cert)
    return None


def classify_presentations(out,progress_every=1000,orbit_records=None,resume=False,compressed=False):
    from sympy import ZZ
    from sympy.polys.matrices import DomainMatrix
    from sympy.polys.matrices.normalforms import smith_normal_decomp
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    report=benchmark() if orbit_records is None else {'orbits':orbit_records};records=[];totals=Counter();start=time.monotonic()
    for orbit in report['orbits']:
        target=out/f'orbit{orbit["index"]:02}.json'
        if compressed:target=target.with_suffix('.json.gz')
        if resume and target.exists():
            with (gzip.open(target,'rt') if compressed else target.open()) as handle:record=json.load(handle)
            totals.update(record['counts']);records.append(record);continue
        h=orbit['heights'];counts=Counter();interesting=[];discards=[]
        for index,labels in enumerate(line_matchings(h)):
            m=matching_matrix(labels)
            dd,uu,vv=smith_normal_decomp(DomainMatrix.from_Matrix(m).convert_to(ZZ))
            d,u,v=dd.to_Matrix(),uu.to_Matrix(),vv.to_Matrix()
            diag=[abs(int(d[j,j])) for j in range(10)]
            keep=[j for j,x in enumerate(diag) if x!=1];orders=tuple(diag[j] for j in keep)
            zero=(0,)*len(orders)
            coords=[tuple(int(v[i,j])%diag[j] if diag[j] else int(v[i,j]) for j in keep) for i in range(10)]
            a=frozenset([zero]+coords[:5]);b=frozenset([zero]+coords[5:])
            def row_witness(relation):
                transformed=[sum(relation[i]*int(v[i,j]) for i in range(10)) for j in range(10)]
                qs=[]
                for j,value in enumerate(transformed):
                    divisor=int(d[j,j])
                    assert value%divisor==0 if divisor else value==0
                    qs.append(value//divisor if divisor else 0)
                witness=[sum(qs[i]*int(u[i,j]) for i in range(10)) for j in range(15)]
                assert all(sum(witness[i]*int(m[i,j]) for i in range(15))==relation[j] for j in range(10))
                return witness
            zero_raw=(0,)*10
            units=[tuple(int(i==j) for j in range(10)) for i in range(10)]
            raw_a=[zero_raw]+units[:5];raw_b=[zero_raw]+units[5:]
            point_a=[zero]+coords[:5];point_b=[zero]+coords[5:]
            if len(a)<6 or len(b)<6:
                classification='collision'
                side,ii,jj=next((side,ii,jj) for side,pts in [('a',point_a),('b',point_b)] for ii,jj in combinations(range(6),2) if pts[ii]==pts[jj])
                raw=raw_a if side=='a' else raw_b
                relation=[x-y for x,y in zip(raw[ii],raw[jj])]
                discards.append(dict(index=index,labels=labels,classification=classification,
                                     side=side,i=ii,j=jj,witness=row_witness(relation)))
            elif group_canon(a,orders)==group_canon(b,orders):
                classification='trivial'
                sign,anchor=next((sign,k) for sign in (1,-1) for k in range(6)
                                 if group_image(b,sign,group_neg(point_b[k] if sign==1 else group_neg(point_b[k],orders),orders),orders)==a)
                shift=group_neg(point_b[anchor] if sign==1 else group_neg(point_b[anchor],orders),orders)
                image=[group_add(x if sign==1 else group_neg(x,orders),shift,orders) for x in point_b]
                mapping=[image.index(x) for x in point_a]
                witnesses=[]
                for i,j in enumerate(mapping):
                    relation=[x-sign*y+sign*z for x,y,z in zip(raw_a[i],raw_b[j],raw_b[anchor])]
                    witnesses.append(row_witness(relation))
                discards.append(dict(index=index,labels=labels,classification=classification,
                                     sign=sign,anchor=anchor,mapping=mapping,witnesses=witnesses))
            else:
                cert=block_certificate(a,b,orders)
                classification='block' if cert else 'UNEXPLAINED'
                master=universal_master(a,b,orders)
                interesting.append(dict(index=index,labels=labels,diagonal=diag,
                                        left=[[int(x) for x in row] for row in u.tolist()],
                                        right=[[int(x) for x in row] for row in v.tolist()],
                                        orders=orders,a=sorted(a),b=sorted(b),block=cert,master=master,
                                        classification=classification))
            counts[classification]+=1;totals[classification]+=1
            if sum(totals.values())%progress_every==0:print('presentations',sum(totals.values()),dict(totals),'seconds',round(time.monotonic()-start,2),flush=True)
        assert sum(counts.values())==orbit['matching_count']
        record=dict(orbit=orbit,counts=dict(counts),nontrivial=interesting,discarded=discards)
        records.append(record)
        if compressed:
            with gzip.open(target,'wt') as handle:json.dump(record,handle);handle.write('\n')
        else:target.write_text(json.dumps(record)+'\n')
        print('orbit',orbit['index'],dict(counts),round(time.monotonic()-start,2),flush=True)
    summary=dict(status='COMPUTED-UNVALIDATED until independent exhaustive audit and proof review',counts=dict(totals),orbits=len(records),seconds=time.monotonic()-start)
    (out/'presentations.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary


def growth_benchmark(out):
    """Benchmark the remaining TI projection strata without expanding matchings."""
    out=Path(out);previous=benchmark()['orbits'];ds=directions()
    for rank in (3,4):
        data=next_span_orbits(previous,rank);counts=[]
        for i,row in enumerate(data['orbits']):
            h=generic_heights(row['rows'],ds);number,buckets=line_matching_count(h)
            row.update(index=i,heights=h,matching_count=number,
                       height_multiplicities=sorted(Counter(h).values()),
                       distance_multiplicities=list(buckets.values()))
            counts.append(number)
        data.update(total_matchings=sum(counts),max_matchings=max(counts),
                    under100k=sum(c for c in counts if c<=100000),
                    orbits_under100k=sum(c<=100000 for c in counts))
        (out/f'rank{rank}-orbits.json').write_text(json.dumps(data,indent=2)+'\n')
        print({k:v for k,v in data.items() if k!='orbits'},'orbit_count',len(data['orbits']),flush=True)
        previous=data['orbits']


if __name__=='__main__':main()
