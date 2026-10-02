"""Fresh exact structural audit of all low-rank quotient-DAG covers.

Imports no builder, Smith or Hermite implementation. Full fiber permutation
actions independently check cross orbits; integer products check every
normalization in both directions. Mechanism identities are reviewed separately.
"""
from pathlib import Path
from itertools import combinations,permutations,product
from collections import Counter
from math import factorial,prod
import argparse,gzip,hashlib,json,time
from test_six_cylinder_branches_review import mul,det
ROOT=Path(__file__).resolve().parents[1]
EDGES=tuple(combinations(range(6),2))

def read(path):
    with gzip.open(path,'rt') as stream:return json.load(stream)

def edge(e,side):
    i,j=e;row=[0]*10
    if i:row[i-1+5*side]-=1
    if j:row[j-1+5*side]+=1
    return row

def full_vertex_actions(h,edges):
    fibers=[tuple(i for i,x in enumerate(h) if x==v) for v in sorted(set(h))]
    index={e:i for i,e in enumerate(edges)};result=[]
    for choices in product(*(permutations(f) for f in fibers)):
        p=list(range(6))
        for fiber,choice in zip(fibers,choices):
            for i,j in zip(fiber,choice):p[i]=j
        result.append(tuple(index[p[i],p[j]] for i,j in edges))
    return result

def cross_audit(h,cross):
    expected=[]
    for d in sorted({abs(h[j]-h[i]) for i,j in EDGES if h[i]!=h[j]}):
        expected.extend((i,j) if h[i]<h[j] else (j,i) for i,j in EDGES if abs(h[j]-h[i])==d)
    edges=list(map(tuple,cross['edges']));assert edges==expected
    actions=full_vertex_actions(h,edges);counts=Counter(h[j]-h[i] for i,j in edges)
    total=prod(factorial(v) for v in counts.values());covered=set();matrices={}
    for record in cross['records']:
        p=record['permutation'];assert sorted(p)==list(range(len(edges)))
        assert all(h[edges[i][1]]-h[edges[i][0]]==h[edges[j][1]]-h[edges[j][0]] for i,j in enumerate(p))
        orbit={tuple(b[p[a[i]]] for i in range(len(p))) for a in actions for b in actions}
        assert len(orbit)==record['orbit_size'] and not covered.intersection(orbit)
        covered.update(orbit)
        matrix=[]
        for a,b in zip(edges,(edges[j] for j in p)):
            ar,br=edge(a,0),edge(b,1);matrix.append([x-y for x,y in zip(ar,br)])
        assert matrix==record['matrix']
        assert record['id'] not in matrices;matrices[record['id']]=matrix
    assert len(covered)==total==cross['covered']
    assert len(matrices)==cross['orbits']
    return matrices,total

class Group:
    def __init__(self,torsion,dimension):self.t=tuple(torsion);self.zero=(0,)*dimension
    def norm(self,p):return tuple(x%self.t[i] if i<len(self.t) else x for i,x in enumerate(p))
    def sub(self,a,b):return self.norm(tuple(x-y for x,y in zip(a,b)))
    def neg(self,a):return self.norm(tuple(-x for x in a))
    def image(self,pts,sign,shift):return {self.norm(tuple(t+sign*x for t,x in zip(shift,p))) for p in pts}
    def auto(self,pts):return Counter(self.sub(a,b) for a in pts for b in pts)

def node_group(node,h):
    m,u,v=node['matrix'],node['smith_u'],node['smith_v'];d=node['smith_diagonal']
    assert len(v)==10 and all(len(r)==10 for r in v)
    assert len(u)==len(m) and all(len(r)==len(m) for r in u)
    assert abs(det(u))==abs(det(v))==1
    diagonal=[[d[i] if i==j else 0 for j in range(10)] for i in range(len(m))]
    assert mul(mul(u,m),v)==diagonal
    rank=sum(bool(x) for x in d);assert rank==node['rank'] and node['free_rank']==10-rank
    assert all(d[:rank]) and not any(d[rank:])
    indices=[i for i in range(rank) if abs(d[i])>1]+list(range(rank,10))
    torsion=[abs(d[i]) for i in range(rank) if abs(d[i])>1]
    assert torsion==node['torsion']
    g=Group(torsion,len(indices));coords=[g.norm(tuple(row[i] for i in indices)) for row in v]
    aa=[g.zero,*coords[:5]];bb=[g.zero,*coords[5:]]
    assert aa==list(map(tuple,node['a'])) and bb==list(map(tuple,node['b']))
    hv=list(h[1:])*2
    assert all(sum(x*y for x,y in zip(row,hv))==0 for row in m)
    assert (len(set(aa))<6 or len(set(bb))<6)==node['forced_collision']
    assert (g.auto(aa)==g.auto(bb))==node['already_homometric']
    return g,aa,bb

def residual(g,a,b):
    sides=[]
    for pts in (a,b):
        bins={}
        for i,j in EDGES:
            delta=g.sub(pts[j],pts[i]);key=min(delta,g.neg(delta));bins.setdefault(key,[]).append((i,j))
        sides.append(bins)
    aa,bb=sides
    for k in aa.keys()&bb.keys():
        count=min(len(aa[k]),len(bb[k]));aa[k]=aa[k][count:];bb[k]=bb[k][count:]
    return {k:v for k,v in aa.items() if v},{k:v for k,v in bb.items() if v}

def equivalence(source,target,witness):
    forward,reverse=witness['to_canonical'],witness['from_canonical']
    assert all(type(x) is int for rows in (forward,reverse) for row in rows for x in row)
    assert mul(forward,source)==target and mul(reverse,target)==source

def dag_audit(h,data,matrices):
    assert data['complete'] and data['normalizations_certified'] and not data['error']
    nodes=data['nodes'];seen=set();cache={};branches=0;identities=0;terminals=Counter()
    assert len({r['orbit_id'] for r in data['roots']})==len(data['roots'])==len(matrices)
    assert {r['orbit_id'] for r in data['roots']}==set(matrices)
    for root in data['roots']:
        equivalence(matrices[root['orbit_id']],nodes[root['node']]['matrix'],root['row_lattice']);identities+=2
    def visit(i):
        nonlocal branches,identities
        if i in seen:return
        seen.add(i);node=nodes[i];assert node['id']==i
        g,a,b=node_group(node,h);aa,bb=residual(g,a,b);cache[i]=sum(map(len,aa.values()))
        kind=node.get('terminal')
        if kind:
            terminals[kind]+=1
            if kind=='collision':assert node['forced_collision']
            elif kind=='ti':
                t=node['forced_ti'];assert g.image(a,t['sign'],tuple(t['shift']))==set(b)
            elif kind=='homometric':assert not aa and not bb and len(set(a))==len(set(b))==6
            else:raise AssertionError(kind)
            return
        assert aa and bb and not node['forced_collision']
        decode=lambda x:{tuple(k):list(map(tuple,v)) for k,v in x}
        assert decode(node['residual_a'])==aa and decode(node['residual_b'])==bb
        chosen=tuple(node['chosen_a']);assert any(chosen in edges for edges in aa.values())
        delta=h[chosen[1]]-h[chosen[0]]
        expected={(edges[0],s) for edges in bb.values() for s in (1,-1) if delta==s*(h[edges[0][1]]-h[edges[0][0]])}
        assert expected and {(tuple(x['b_edge']),x['sign']) for x in node['branches']}==expected
        assert len(node['branches'])==len(expected)
        ar=edge(chosen,0)
        for branch in node['branches']:
            br=edge(branch['b_edge'],1);row=[x-branch['sign']*y for x,y in zip(ar,br)]
            child=branch['child'];assert 0<=child<len(nodes)
            equivalence(node['matrix']+[row],nodes[child]['matrix'],branch['row_lattice']);identities+=2
            visit(child);assert cache[child]<cache[i];branches+=1
    for root in data['roots']:visit(root['node'])
    assert seen==set(range(len(nodes)))
    return dict(nodes=len(nodes),roots=len(data['roots']),branches=branches,lattice_inclusions=identities,terminals=dict(terminals))

def main():
    p=argparse.ArgumentParser();p.add_argument('--resume',action='store_true');p.add_argument('--require-complete',action='store_true')
    p.add_argument('--base',type=Path,default=ROOT/'results/2026-09-30-six-free-dag-all')
    p.add_argument('--out',type=Path,default=ROOT/'results/2026-09-30-six-free-dag-review');args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    strata=[]
    for rank in (3,4):
        saved=json.loads((ROOT/f'results/2026-09-30-six-free-rank/rank{rank}-orbits.json').read_text())
        strata.extend((rank,r['index'],r['heights']) for r in saved['orbits'])
    reports=[];start=time.monotonic()
    for rank,index,h in strata:
        stem=f'rank{rank}-orbit{index:03}';dp=args.base/f'{stem}.json.gz';cp=args.base/f'{stem}-cross.json.gz';dest=args.out/f'{stem}.json'
        hashes=[hashlib.sha256(path.read_bytes()).hexdigest() for path in (dp,cp)]
        if args.resume and dest.exists():
            old=json.loads(dest.read_text())
            if old['hashes']==hashes:reports.append(old);continue
        data=read(dp)
        if not data.get('normalizations_certified'):
            print(stem,'awaiting exact normalization witnesses',flush=True);break
        assert data['heights']==h
        matrices,total=cross_audit(h,read(cp));result=dag_audit(h,data,matrices)
        report=dict(rank=rank,orbit=index,cross_bijections=total,hashes=hashes,**result)
        dest.write_text(json.dumps(report,sort_keys=True)+'\n');reports.append(report)
        print(stem,result,'elapsed',round(time.monotonic()-start,2),flush=True)
    summary=dict(complete=len(reports)==len(strata),strata=len(reports),expected_strata=len(strata),seconds=time.monotonic()-start,
                 totals={k:sum(r[k] for r in reports) for k in ('cross_bijections','roots','nodes','branches','lattice_inclusions')},
                 status='Independent structural cover audit only; terminal mechanism proof audited separately')
    (args.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary,flush=True)
    if args.require_complete:assert summary['complete']

if __name__=='__main__':main()
