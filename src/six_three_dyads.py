"""Finite three-dyad matching classification with exact label-symmetry orbits."""
from __future__ import annotations
import argparse,gzip,json,time
from collections import Counter
from itertools import combinations,permutations,product
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PAIRS=((0,1),(0,2),(1,2))
P4=tuple(permutations(range(4)));P4_INDEX={p:i for i,p in enumerate(P4)}
P3=tuple(permutations(range(3)));P3_INDEX={p:i for i,p in enumerate(P3)}
N=24**3*48

def encode(parts):
    a,b,c,u=parts
    return ((a*24+b)*24+c)*48+u

def decode(code):
    code,u=divmod(code,48);code,c=divmod(code,24);a,b=divmod(code,24)
    return a,b,c,u

def labels(code):
    c0,c1,c2,u=decode(code);pi=P3[u//8];bits=u%8;out=[]
    for i,j in enumerate(pi):out.append((2*i,2*i+1,2*j,2*j+1,-1 if bits>>i&1 else 1))
    for (i,j),c in zip(PAIRS,(c0,c1,c2)):
        for source,target in enumerate(P4[c]):
            a,b=divmod(source,2);x,y=divmod(target,2)
            out.append((2*i+a,2*j+b,2*i+x,2*j+y,1))
    return tuple(sorted(out))

def parts_from_labels(rows):
    crosses=[[-1]*4 for _ in range(3)];internal=[None]*3;bits=0
    for i,j,k,l,s in rows:
        if i//2==j//2:
            assert k//2==l//2
            internal[i//2]=k//2
            if s==-1:bits|=1<<(i//2)
        else:
            assert (i//2,j//2)==(k//2,l//2) and s==1
            pair=PAIRS.index((i//2,j//2));crosses[pair][2*(i%2)+j%2]=2*(k%2)+l%2
    return tuple(P4_INDEX[tuple(p)] for p in crosses)+(8*P3_INDEX[tuple(internal)]+bits,)

def generators():
    identity=tuple(range(6));out=[]
    for side in ('a','b'):
        for fibre in range(3):
            p=list(identity);i=2*fibre;p[i],p[i+1]=p[i+1],p[i]
            out.append(dict(name=f'{side}_flip_{fibre}',a=p if side=='a' else identity,b=p if side=='b' else identity,swap=False))
    for first in (0,1):
        sigma=list(range(3));sigma[first],sigma[first+1]=sigma[first+1],sigma[first]
        p=tuple(2*sigma[i//2]+i%2 for i in range(6))
        out.append(dict(name=f'fibres_{first}_{first+1}',a=p,b=p,swap=False))
    out.append(dict(name='swap_ab',a=identity,b=identity,swap=True))
    return out

def transform(rows,g):
    out=[]
    for i,j,k,l,s in rows:
        i,j=g['a'][i],g['a'][j];k,l=g['b'][k],g['b'][l]
        if g['swap']:i,j,k,l=k,l,i,j
        if i>j:i,j=j,i;s=-s
        if k>l:k,l=l,k;s=-s
        out.append((i,j,k,l,s))
    return tuple(sorted(out))

def generator_tables():
    result=[]
    for g in generators():
        base=parts_from_labels(transform(labels(0),g));inputs=[];tables=[]
        for output in range(4):
            candidates=[]
            for source,size in enumerate((24,24,24,48)):
                table=[]
                for x in range(size):
                    p=[0]*4;p[source]=x
                    table.append(parts_from_labels(transform(labels(encode(p)),g))[output])
                if len(set(table))>1:candidates.append((source,table))
            assert len(candidates)==1
            source,table=candidates[0];inputs.append(source);tables.append(table)
        assert sorted(inputs)==list(range(4))
        result.append(dict(**g,inputs=inputs,tables=tables))
    # Check simultaneous variations, in addition to all isolated factor values.
    for parts in product(range(0,24,7),range(0,24,7),range(0,24,7),range(0,48,13)):
        for g in result:
            computed=tuple(table[parts[source]] for source,table in zip(g['inputs'],g['tables']))
            assert computed==parts_from_labels(transform(labels(encode(parts)),g))
    return result

def symmetry_orbits(out):
    start=time.monotonic();gens=generator_tables();seen=bytearray(N);orbits=[]
    compact=[(g['inputs'],g['tables']) for g in gens]
    total=0
    for seed in range(N):
        if seen[seed]:continue
        seen[seed]=1;todo=[seed];at=0
        while at<len(todo):
            code=todo[at];at+=1;parts=decode(code)
            for sources,tables in compact:
                a=tables[0][parts[sources[0]]];b=tables[1][parts[sources[1]]]
                c=tables[2][parts[sources[2]]];u=tables[3][parts[sources[3]]]
                target=((a*24+b)*24+c)*48+u
                if not seen[target]:seen[target]=1;todo.append(target)
        orbits.append(dict(index=len(orbits),representative=seed,size=len(todo),members=sorted(todo)))
        total+=len(todo)
        if len(orbits)%200==0:print('orbits',len(orbits),'covered',total,'seconds',round(time.monotonic()-start,2),flush=True)
    assert sum(seen)==N and total==N
    result=dict(status='COMPUTED-UNVALIDATED pending independent symmetry audit',matchings=N,generators=gens,orbits=orbits,seconds=time.monotonic()-start)
    with gzip.open(out/'orbits.json.gz','wt') as f:json.dump(result,f)
    summary=dict(matchings=N,orbits=len(orbits),size_histogram=dict(Counter(o['size'] for o in orbits)),seconds=result['seconds'])
    (out/'orbits-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary,flush=True)
    return result

def group_linear(terms,orders):
    return tuple((sum(c*x[i] for c,x in terms)%d if d else sum(c*x[i] for c,x in terms)) for i,d in enumerate(orders))

def image(points,sign,shift,orders):
    return frozenset(group_linear([(sign,x),(1,shift)],orders) for x in points)

def cross(a,b,orders):
    return Counter(group_linear([(1,x),(-1,y)],orders) for x in a for y in b)

def strict_block(a,b,orders):
    """Find an existing L2/L3/L4/L5 condition, never the tautological L1."""
    zero=(0,)*len(orders)
    for sign in (1,-1):
        for x in a:
            for y in b:
                shift=group_linear([(1,x),(-sign,y)],orders)
                aligned=image(b,sign,shift,orders)
                common=a&aligned;removed=a-aligned;added=aligned-a
                if not removed or not common or len(removed)!=len(added):continue
                cross_before=cross(common,removed,orders)
                cross_after=cross(common,added,orders)
                for local_sign in (1,-1):
                    anchor=min(removed)
                    for target in sorted(added):
                        delta=group_linear([(1,target),(-local_sign,anchor)],orders)
                        if image(removed,local_sign,delta,orders)!=added:continue
                        mechanism=None;extra={}
                        if cross_before==cross_after:mechanism='L2' if local_sign==1 else 'L5'
                        elif local_sign==1 and delta!=zero and group_linear([(2,delta)],orders)==zero:
                            before=cross_before+Counter({group_linear([(-1,k)],orders):v for k,v in cross_before.items()})
                            after=Counter({group_linear([(1,k),(1,delta)],orders):v for k,v in before.items()})
                            if before==after:mechanism='L4'
                        elif local_sign==1:
                            # W=t+V, W+delta=-t+V, and C*V~ symmetric.
                            choices=[]
                            for d,z in zip(orders,delta):
                                choices.append([t for t in range(d) if (2*t+z)%d==0] if d else ([-z//2] if z%2==0 else []))
                            for t in product(*choices):
                                shifted=Counter({group_linear([(1,k),(1,t)],orders):v for k,v in cross_before.items()})
                                reflected=Counter({group_linear([(-1,k)],orders):v for k,v in shifted.items()})
                                if shifted==reflected:mechanism='L3';extra['t']=t;break
                        if mechanism:
                            return dict(mechanism=mechanism,b_sign=sign,b_shift=shift,block_sign=local_sign,block_shift=delta,
                                        common=sorted(common),removed=sorted(removed),added=sorted(added),**extra)
    return None

def classify(report,out):
    from sympy import Matrix,ZZ
    from sympy.polys.matrices import DomainMatrix
    from sympy.polys.matrices.normalforms import smith_normal_decomp
    from six_free_rank import matching_matrix
    path=out/'presentations.jsonl';completed=[]
    if path.exists():completed=[json.loads(x) for x in path.read_text().splitlines() if x]
    counts=Counter(r['classification'] for r in completed)
    weights=Counter()
    for r in completed:weights[r['classification']]+=report['orbits'][r['orbit']]['size']
    start=time.monotonic()
    with path.open('a') as file:
        for orbit in report['orbits'][len(completed):]:
            labs=labels(orbit['representative']);m=matching_matrix(labs)
            dd,uu,vv=smith_normal_decomp(DomainMatrix.from_Matrix(m).convert_to(ZZ))
            d,u,v=(x.to_Matrix() for x in (dd,uu,vv));diag=[int(d[i,i]) for i in range(10)]
            assert u*m*v==d
            keep=[i for i,x in enumerate(diag) if abs(x)!=1];orders=tuple(abs(diag[i]) for i in keep)
            coords=[tuple(int(v[j,i])%abs(diag[i]) if diag[i] else int(v[j,i]) for i in keep) for j in range(10)]
            zero=(0,)*len(orders);aa=(zero,*coords[:5]);bb=(zero,*coords[5:]);a=frozenset(aa);b=frozenset(bb)
            rec=dict(orbit=orbit['index'],representative=orbit['representative'],size=orbit['size'],labels=labs,
                     diagonal=diag,left=u.tolist(),right=v.tolist(),orders=orders,a=aa,b=bb)
            if len(a)<6 or len(b)<6:
                rec['classification']='collision'
                rec['collision']=next((side,i,j) for side,pts in [('a',aa),('b',bb)] for i,j in combinations(range(6),2) if pts[i]==pts[j])
            else:
                ti=None
                for sign in (1,-1):
                    for anchor,y in enumerate(bb):
                        shift=group_linear([(-sign,y)],orders)
                        if image(b,sign,shift,orders)==a:ti=dict(sign=sign,anchor=anchor);break
                    if ti:break
                if ti:rec.update(classification='TI',ti=ti)
                else:
                    cert=strict_block(a,b,orders)
                    rec.update(classification=cert['mechanism'] if cert else 'UNEXPLAINED',block=cert)
            counts[rec['classification']]+=1;weights[rec['classification']]+=orbit['size']
            file.write(json.dumps(rec,default=int)+'\n');file.flush();completed.append(rec)
            if len(completed)%100==0:print('classified',len(completed),dict(counts),'seconds',round(time.monotonic()-start,2),flush=True)
    summary=dict(status='COMPUTED-UNVALIDATED pending independent proof and finite audit',orbits=len(completed),counts=dict(counts),matching_counts=dict(weights),seconds=time.monotonic()-start)
    (out/'classification.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary,flush=True)
    return summary

def cyclic_obstruction(rec):
    orders=rec['orders'];zero=(0,)*len(orders)
    for side in ('a','b'):
        pts=rec[side]
        for pairs in combinations(tuple(combinations(range(6),2)),3):
            differences=[group_linear([(1,pts[j]),(-1,pts[i])],orders) for i,j in pairs]
            if len(set(differences))!=3 or zero in differences:continue
            if any(group_linear([(2,d)],orders)!=zero for d in differences):continue
            if group_linear([(1,differences[0]),(1,differences[1])],orders)==differences[2]:
                return dict(side=side,pairs=pairs,differences=differences,
                            reason='all three nonzero elements of a C2 squared subgroup occur as within-set differences')
    return None

def finish_cyclic(report,out):
    records=[json.loads(x) for x in (out/'presentations.jsonl').read_text().splitlines() if x]
    counts=Counter();weights=Counter()
    for rec in records:
        if rec['classification']=='UNEXPLAINED':
            obstruction=cyclic_obstruction(rec)
            if obstruction:rec.update(classification='cyclic_collision',cyclic_obstruction=obstruction)
        counts[rec['classification']]+=1;weights[rec['classification']]+=rec['size']
    summary=dict(status='COMPUTED-UNVALIDATED pending separate proof attack',orbits=len(records),counts=dict(counts),matching_counts=dict(weights))
    with gzip.open(out/'cyclic-presentations.json.gz','wt') as f:json.dump(records,f)
    (out/'cyclic-classification.json').write_text(json.dumps(summary,indent=2)+'\n')
    print('cyclic',summary,flush=True)
    return summary

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=ROOT/'results/2026-09-30-six-three-dyads');p.add_argument('--classify',action='store_true');args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    if (args.out/'orbits.json.gz').exists():
        with gzip.open(args.out/'orbits.json.gz','rt') as f:report=json.load(f)
    else:report=symmetry_orbits(args.out)
    if args.classify:
        classify(report,args.out)
        finish_cyclic(report,args.out)

if __name__=='__main__':main()
