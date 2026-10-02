"""Exploratory universal six-point quotient DAG from oriented star orbits.

A capped run proves no completeness. A complete run still needs independent
branch/lattice verification and structural classification of every terminal.
"""
from pathlib import Path
from itertools import combinations,product
from collections import Counter,deque
import argparse,gzip,json,time
from sympy import Matrix
from six_fibers import group_record,canonical_lattice,group_add,edge_row
ROOT=Path(__file__).resolve().parents[1]
EDGES=tuple(combinations(range(6),2))
ARCS=tuple((a,b) for a,b in EDGES for a,b in ((a,b),(b,a)))

def stars():
    allstars={tuple(sorted(2*e+s for e,s in zip(edges,signs)))
              for edges in combinations(range(15),5) for signs in product((0,1),repeat=5)}
    actions=[]
    for k in range(5):
        permutation=list(range(6));permutation[k],permutation[k+1]=permutation[k+1],permutation[k]
        actions.append(tuple(ARCS.index((permutation[a],permutation[b])) for a,b in ARCS))
    actions.append(tuple(i^1 for i in range(30)))
    unseen=set(allstars);orbits=[]
    while unseen:
        rep=min(unseen);orbit={rep};todo=[rep]
        while todo:
            star=todo.pop()
            for action in actions:
                other=tuple(sorted(action[x] for x in star))
                if other not in orbit:orbit.add(other);todo.append(other)
        assert orbit<=allstars;unseen-=orbit;orbits.append(dict(star=rep,size=len(orbit)))
    return orbits

def root_matrix(star):
    rows=[]
    for i,arc in enumerate(star):
        a,b=ARCS[arc];r=[0]*10
        if b:r[b-1]+=1
        if a:r[a-1]-=1
        r[5+i]-=1;rows.append(r)
    return Matrix(rows)

def search(orbits,limit,seconds,out):
    start=time.monotonic();nodes=[];seen={};roots=[]
    def visit(m):
        h=canonical_lattice(m);key=tuple(map(tuple,h.tolist()))
        if key in seen:return seen[key]
        if len(nodes)>=limit or time.monotonic()-start>seconds:raise TimeoutError('benchmark bound')
        index=len(nodes);seen[key]=index;record=group_record(h);node=dict(id=index,**record);nodes.append(node)
        if len(nodes)%1000==0:print('nodes',len(nodes),'seconds',round(time.monotonic()-start,2),'roots',len(roots),flush=True)
        if record['forced_collision']:node['terminal']='collision';return index
        if record['forced_ti']:node['terminal']='ti';return index
        if record['already_homometric']:node['terminal']='homometric';return index
        def classes(points):
            bins={}
            for e in EDGES:
                i,j=e;d=group_add(points[j],points[i],record['torsion'],-1)
                neg=group_add((0,)*len(d),d,record['torsion'],-1)
                bins.setdefault(min(d,neg),[]).append(e)
            return bins
        a,b=classes(record['a']),classes(record['b'])
        for key in a.keys()&b.keys():
            count=min(len(a[key]),len(b[key]));a[key]=a[key][count:];b[key]=b[key][count:]
        a={k:v for k,v in a.items() if v};b={k:v for k,v in b.items() if v}
        assert a and b
        ka=min(a,key=lambda k:(-len(a[k]),k));chosen=a[ka][0];ar=edge_row(chosen,0)
        node['chosen_a']=chosen;node['branches']=[]
        for kb,edges in sorted(b.items()):
            edge=edges[0];br=edge_row(edge,1)
            for sign in (1,-1):
                relation=[x-sign*y for x,y in zip(ar,br)]
                child=visit(h.col_join(Matrix([relation])))
                node['branches'].append(dict(b_edge=edge,sign=sign,child=child))
        node['branches_complete']=True
        return index
    complete=True;error=None
    try:
        for i,orbit in enumerate(orbits):
            roots.append(dict(orbit=i,node=visit(root_matrix(orbit['star']))))
            print('root',i,'nodes',len(nodes),'seconds',round(time.monotonic()-start,2),flush=True)
    except TimeoutError as exc:complete=False;error=str(exc)
    hist=Counter(x.get('terminal','branch') for x in nodes)
    report=dict(complete=complete,error=error,roots=roots,orbits=orbits,nodes=nodes,seconds=time.monotonic()-start,
                counts=dict(hist),status='EXPLORATORY; not reviewed or structurally classified')
    with gzip.open(out/'dag.json.gz','wt') as stream:json.dump(report,stream,default=int)
    summary={k:v for k,v in report.items() if k not in ('nodes','orbits','roots')};summary['completed_roots']=len(roots);summary['nodes']=len(nodes)
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');return summary

def main():
    p=argparse.ArgumentParser();p.add_argument('--max-nodes',type=int,default=5000);p.add_argument('--seconds',type=int,default=60)
    p.add_argument('--out',type=Path,default=ROOT/'results/2026-09-30-six-star-quotient');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    orbits=stars();assert len(orbits)==107 and sum(x['size'] for x in orbits)==96096
    (a.out/'stars.json').write_text(json.dumps(orbits)+'\n');print('stars',len(orbits),'raw',sum(x['size'] for x in orbits),flush=True)
    print(search(orbits,a.max_nodes,a.seconds,a.out),flush=True)

if __name__=='__main__':main()
