"""Exhaustive quotient-DAG cover for one exact real-height stratum.

Builder only: claims require an independent branch/certificate audit.
Restrict every added edge equality to the stated generic height equation;
no modulus or integer-coordinate bound is used. Row-Hermite caching preserves
the integral relation lattice, including torsion.
"""
from __future__ import annotations
import argparse,gzip,json,time
from collections import Counter,deque
from itertools import combinations,permutations,product
from pathlib import Path
from sympy import Matrix
from six_fibers import group_add,group_record,edge_row,canonical_lattice
from six_free_rank import block_certificate,universal_master
ROOT=Path(__file__).resolve().parents[1]
EDGES=tuple(combinations(range(6),2))


def search(heights,max_nodes=10000,progress=None,classify=True,root_matrices=None):
    nodes=[];lookup={};start=time.monotonic();height_vector=list(heights[1:])*2
    def classes(points,torsion):
        out={}
        for edge in EDGES:
            i,j=edge;delta=group_add(points[j],points[i],torsion,-1)
            negative=group_add((0,)*len(delta),delta,torsion,-1);key=min(delta,negative)
            out.setdefault(key,[]).append(edge)
        return out
    def visit(matrix):
        h=canonical_lattice(matrix);key=tuple(map(tuple,h.tolist()))
        if key in lookup:return lookup[key]
        if max_nodes and len(nodes)>=max_nodes:raise RuntimeError('node cap')
        index=len(nodes);lookup[key]=index
        record=group_record(h);node=dict(id=index,**record);nodes.append(node)
        if progress and len(nodes)%100==0:progress(len(nodes),time.monotonic()-start)
        if record['forced_collision']:node['terminal']='collision';return index
        if record['forced_ti']:node['terminal']='ti';return index
        if record['already_homometric']:
            node['terminal']='homometric'
            if classify:
                orders=tuple(record['torsion'])+(0,)*record['free_rank']
                a,b=frozenset(record['a']),frozenset(record['b'])
                node['block']=block_certificate(a,b,orders)
                node['master']=universal_master(a,b,orders) if record['free_rank']>=3 else None
            return index
        aa,bb=classes(record['a'],record['torsion']),classes(record['b'],record['torsion'])
        for k in aa.keys()&bb.keys():
            number=min(len(aa[k]),len(bb[k]));aa[k]=aa[k][number:];bb[k]=bb[k][number:]
        aa={k:v for k,v in aa.items() if v};bb={k:v for k,v in bb.items() if v}
        assert aa and bb
        def allowed(edge):
            i,j=edge;delta=heights[j]-heights[i];out=[]
            for kb,edges in sorted(bb.items()):
                k,l=edges[0]
                for sign in (1,-1):
                    if delta==sign*(heights[l]-heights[k]):out.append((kb,edges[0],sign))
            return out
        options=[]
        for ka,edges in aa.items():
            edge=edges[0];targets=allowed(edge);assert targets
            options.append(((int(heights[edge[0]]==heights[edge[1]]),len(targets),-len(edges),edge),edge,targets))
        _,chosen,targets=min(options)
        node.update(chosen_a=chosen,residual_a=[(k,v) for k,v in sorted(aa.items())],
                    residual_b=[(k,v) for k,v in sorted(bb.items())],branches=[])
        ar=edge_row(chosen,0)
        for kb,edge,sign in targets:
            br=edge_row(edge,1);relation=tuple(x-sign*y for x,y in zip(ar,br))
            assert sum(x*y for x,y in zip(relation,height_vector))==0
            child=visit(h.col_join(Matrix([relation])))
            node['branches'].append(dict(b_edge=edge,sign=sign,child=child))
        return index
    complete=True;error=None;root=None;roots=[]
    try:
        if root_matrices is None:root=visit(Matrix.zeros(0,10))
        else:
            for record in root_matrices:roots.append(dict(orbit_id=record['id'],node=visit(Matrix(record['matrix']))))
    except RuntimeError as exc:complete=False;error=str(exc)
    return dict(status='COMPUTED-UNVALIDATED quotient cover until independent audit',complete=complete,error=error,
                heights=heights,node_cap=max_nodes,root=root,roots=roots,nodes=nodes,seconds=time.monotonic()-start,
                terminal_histogram=dict(Counter(n.get('terminal','branch') for n in nodes)))


def cross_orbits(heights,progress=None):
    """Exact nonzero-edge bijection orbits under independent fiber relabelling."""
    buckets={}
    for i,j in EDGES:
        if heights[i]==heights[j]:continue
        edge=(i,j) if heights[i]<heights[j] else (j,i)
        buckets.setdefault(abs(heights[j]-heights[i]),[]).append(edge)
    edges=tuple(edge for d in sorted(buckets) for edge in buckets[d]);lookup={edge:i for i,edge in enumerate(edges)}
    slices=[];start=0
    for d in sorted(buckets):
        size=len(buckets[d]);slices.append(tuple(range(start,start+size)));start+=size
    fibers={}
    for i,h in enumerate(heights):fibers.setdefault(h,[]).append(i)
    actions=[]
    for fiber in fibers.values():
        for u,v in zip(fiber,fiber[1:]):
            perm=list(range(6));perm[u],perm[v]=perm[v],perm[u]
            actions.append(tuple(lookup[(perm[i],perm[j])] for i,j in edges))
    seen=set();records=[];started=time.monotonic()
    for blocks in product(*(permutations(part) for part in slices)):
        p=tuple(x for block in blocks for x in block)
        if p in seen:continue
        todo=[p];seen.add(p);size=0
        while todo:
            x=todo.pop();size+=1
            for action in actions:
                for y in (tuple(x[i] for i in action),tuple(action[i] for i in x)):
                    if y not in seen:seen.add(y);todo.append(y)
        labels=tuple((*edge,*edges[target],1) for edge,target in zip(edges,p))
        rows=[]
        for i,j,k,l,sign in labels:
            ar=edge_row((i,j),0);br=edge_row((k,l),1);rows.append([x-y for x,y in zip(ar,br)])
        records.append(dict(id=len(records),permutation=p,orbit_size=size,labels=labels,matrix=rows))
        if progress and len(records)%100==0:progress(len(records),len(seen),time.monotonic()-started)
    return dict(heights=heights,edges=edges,actions=actions,covered=len(seen),orbits=len(records),records=records,seconds=time.monotonic()-started)


def main():
    p=argparse.ArgumentParser();p.add_argument('--rank',type=int,choices=[3,4],default=4);p.add_argument('--orbit',type=int,default=173)
    p.add_argument('--cross-orbits',action='store_true');p.add_argument('--max-nodes',type=int,default=10000);p.add_argument('--out',type=Path,default=ROOT/'results/2026-09-30-six-free-dag')
    a=p.parse_args();data=json.loads((ROOT/f'results/2026-09-30-six-free-rank/rank{a.rank}-orbits.json').read_text())
    orbit=data['orbits'][a.orbit];a.out.mkdir(parents=True,exist_ok=True)
    cross=None
    if a.cross_orbits:
        cross=cross_orbits(orbit['heights'],lambda count,covered,seconds:print('cross orbits',count,'covered',covered,'seconds',round(seconds,2),flush=True))
        with gzip.open(a.out/f'rank{a.rank}-orbit{a.orbit:03}-cross.json.gz','wt') as f:json.dump(cross,f,default=int);f.write('\n')
        print('cross complete',cross['orbits'],cross['covered'],flush=True)
    result=search(orbit['heights'],a.max_nodes,lambda count,seconds:print('nodes',count,'seconds',round(seconds,2),flush=True),root_matrices=cross['records'] if cross else None)
    result['orbit']=orbit;result['rank']=a.rank
    with gzip.open(a.out/f'rank{a.rank}-orbit{a.orbit:03}.json.gz','wt') as f:json.dump(result,f,default=int);f.write('\n')
    print({k:v for k,v in result.items() if k not in ('nodes','orbit')},flush=True)

if __name__=='__main__':main()
