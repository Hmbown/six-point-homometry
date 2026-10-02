"""Independent exact controls for the finite Bloom linear matching tables.

Default execution checks every retained witness, all 5,760 endpoint systems
using original 6x4 equation minors, and a benchmark of the independent paired
enumerator. --full checks all 4,147,200 paired systems with a different pivot.
"""
from collections import Counter
from itertools import combinations, permutations
from functools import reduce
from math import gcd
from pathlib import Path
import argparse
import hashlib
import json
import time
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/2026-09-30-six-composite-global-matrix"
X = ((2,-4),(5,-4),(-4,-1),(-4,2),(2,2),(-1,5))
Y = ((-1,-4),(2,-4),(5,-1),(-4,2),(2,2),(-4,5))
P = tuple(permutations(range(6)))


def largepart(value):
    for p in (2,3,5,7):
        while value and value % p == 0:
            value //= p
    return abs(value)


def primepart(value):
    """Remove only primes2 and3 for the final classification scope."""
    for p in (2,3):
        while value and value % p == 0:
            value //= p
    return abs(value)


def det2(a,b):
    return a[0]*b[1] - a[1]*b[0]


def minors(rows):
    return reduce(gcd, (det2(a,b) for a,b in combinations(rows,2)), 0)


def content(rows):
    return reduce(gcd, (z for row in rows for z in row), 0)


def primitive(row):
    divisor = gcd(*row)
    u,v = (z//divisor for z in row)
    return (-u,-v) if u < 0 or (u == 0 and v < 0) else (u,v)


def group():
    r = np.array(((0,-1),(1,-1)),dtype=np.int64)
    t = np.array(((0,1),(1,0)),dtype=np.int64)
    return {tuple(map(tuple, sign*np.linalg.matrix_power(r,i) @
                      (t if j else np.eye(2,dtype=np.int64))))
            for sign in (1,-1) for i in range(3) for j in range(2)}


def collision_lines():
    return {primitive((a[0]-b[0],a[1]-b[1])) for pts in (X,Y)
            for a,b in combinations(pts,2)}


def replay(w):
    ux,uy = (Y,X) if w["swap"] else (X,Y)
    target = [[w["sx"]*z for z in ux[i]] for i in w["px"]]
    # Solve the first two X equations directly by Cramer's rule.
    m = ((-4*target[0][0]+4*target[1][0],
          -4*target[0][1]+4*target[1][1]),
         (-5*target[0][0]+2*target[1][0],
          -5*target[0][1]+2*target[1][1]))
    h=[]
    for source,endpoint,sign,permutation,start in (
            (X,ux,w["sx"],w["px"],2), (Y,uy,w["sy"],w["py"],0)):
        for i in range(start,6):
            h.append(tuple(source[i][0]*m[0][j]+source[i][1]*m[1][j]-
                           12*sign*endpoint[permutation[i]][j] for j in range(2)))
    assert tuple(map(tuple,w["M"])) == m
    assert tuple(map(tuple,w["H"])) == tuple(h)
    return m,h


def test_paired_retained_witnesses():
    # Independent centering from original Bloom coordinates, componentwise:
    # C=3(point-mean), so 2C=6point-sum(six labelled points).
    originals=(((0,0),(1,0),(-2,1),(-2,2),(0,2),(-1,3)),
               ((0,0),(1,0),(2,1),(-1,2),(1,2),(-1,3)))
    for original,centered in zip(originals,(X,Y)):
        totals=tuple(sum(row[j] for row in original) for j in range(2))
        assert tuple(tuple(6*row[j]-totals[j] for j in range(2)) for row in original) == tuple(tuple(2*z for z in row) for row in centered)
    data=json.loads((OUT/"matching-certificate.json").read_text())
    assert data["complete"] and data["processed"] == 2*4*720**2
    gs=group()
    assert {tuple(tuple(z//12 for z in row) for row in rec["witness"]["M"])
            for rec in data["rank0"]} == gs
    assert len(data["rank0"]) == 12
    for rec in data["rank0"]:
        m,h=replay(rec["witness"])
        assert content(h) == 0
        assert all(z%12==0 for row in m for z in row)
        swap=rec["witness"]["swap"]
        r=np.array(((0,-1),(1,-1)),dtype=np.int64)
        t=np.array(((0,1),(1,0)),dtype=np.int64)
        expected={tuple(map(tuple, sign*np.linalg.matrix_power(r,i) @
                       (t if swap else np.eye(2,dtype=np.int64))))
                  for sign in (1,-1) for i in range(3)}
        assert tuple(tuple(z//12 for z in row) for row in m) in expected
    for rec in data["rank1"]:
        _,h=replay(rec["witness"])
        assert content(h) == rec["content"] and minors(h) == 0
        assert tuple(rec["direction"]) in collision_lines()
        assert largepart(rec["content"]) == 1
        assert {primitive(row) for row in h if row != (0,0)} == {tuple(rec["direction"])}
    for rec in data["rank2"]:
        _,h=replay(rec["witness"])
        assert content(h) == rec["content"] and minors(h) == rec["minor_gcd"]
        assert largepart(rec["content"]) == 1
        assert largepart(rec["minor_gcd"]) in (1,13,19)
        assert primepart(rec["minor_gcd"]) in (1,5,7,13,19)
    assert sum(r["count"] for r in data["rank1"]) == 864
    assert sum(r["count"] for r in data["rank2"]) == 4146324
    assert data["rank2_large_count"] == len(data["exceptional_cases"]) == 48
    assert data["uncontained_count"] == 0
    for rec in data["exceptional_cases"]:
        m,h=replay(rec["witness"])
        g=tuple(map(tuple,rec["g"]))
        assert g in gs
        augmented=h+[tuple(m[i][j]-12*g[i][j] for j in range(2)) for i in range(2)]
        assert minors(augmented) == rec["enlarged_minor_gcd"]
        assert largepart(minors(augmented)) == largepart(minors(h))


def independent_paired(limit=None):
    """All permutations, using the first two Y equations as the pivot.

    This does not call or reconstruct the C++ X-pivot routine. Each Y matching
    is a scalar control and all 720 X matchings are handled in one exact int64
    batch. The entry bound is <500; determinant bound is <500,000, safely int64.
    """
    started=time.monotonic()
    x=np.array(X,dtype=np.int64); y=np.array(Y,dtype=np.int64)
    perms=np.array(P,dtype=np.int64)
    hist=Counter(); r1=Counter();r2=Counter();processed=0
    pairs=np.array(tuple(combinations(range(10),2)))
    for swap in (0,1):
        ux,uy=(y,x) if swap else (x,y)
        for sx in (1,-1):
            for sy in (1,-1):
                for py in P:
                    target=sy*uy[np.array(py)]
                    # 12*Y[:2]^-1 = ((-4,4),(-2,-1)).
                    m=np.array(((-4*target[0]+4*target[1]),
                                (-2*target[0]-target[1])))
                    hx=np.einsum('ij,jk->ik',x,m)[None,:,:]-12*sx*ux[perms]
                    hy=(np.einsum('ij,jk->ik',y[2:],m)-12*target[2:])
                    h=np.concatenate((hx,np.broadcast_to(hy,(720,4,2))),axis=1)
                    c=np.gcd.reduce(h.reshape(720,20),axis=1)
                    a,b=h[:,pairs[:,0]],h[:,pairs[:,1]]
                    d=np.gcd.reduce(a[:,:,0]*b[:,:,1]-a[:,:,1]*b[:,:,0],axis=1)
                    rank=np.where(c==0,0,np.where(d==0,1,2))
                    hist.update(map(int,rank))
                    for i in np.flatnonzero(rank==1):
                        r1[(primitive(next(tuple(map(int,r)) for r in h[i] if np.any(r))),int(c[i]))]+=1
                    c2,d2=c[rank==2],d[rank==2]
                    r2.update(zip(map(int,c2),map(int,d2)))
                    processed+=720
                    if limit is not None and processed>=limit:
                        return processed,hist,r1,r2,time.monotonic()-started
    return processed,hist,r1,r2,time.monotonic()-started


def determinant(rows):
    """Permutation expansion, independent of elimination and numpy."""
    total=0
    for p in permutations(range(len(rows))):
        term=(-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
        for i,j in enumerate(p):
            term*=rows[i][j]
        total+=term
    return total


def independent_endpoints():
    """Original six equations in four unknowns; use all 4x4 minors.

    The first two source columns have rank2 at every allowed prime. A nonzero
    fourth determinantal divisor means residual rank2, and its large-prime part
    equals that of the elimination table because12 is an allowed-ring unit.
    """
    count=Counter();large=Counter();coprime6=Counter();started=time.monotonic()
    for source in (X,Y):
        for target in (X,Y):
            for sign in (1,-1):
                for p in P:
                    q=[tuple(source[i])+tuple(-sign*z for z in target[p[i]]) for i in range(6)]
                    d4=reduce(gcd,(determinant([q[i] for i in inds])
                                   for inds in combinations(range(6),4)),0)
                    if d4:
                        count[2]+=1;large[largepart(d4)]+=1;coprime6[primepart(d4)]+=1
                    else:
                        d3=reduce(gcd,(determinant([[q[i][j] for j in cols] for i in inds])
                             for inds in combinations(range(6),3) for cols in combinations(range(4),3)),0)
                        count[1 if d3 else 0]+=1
    assert count == Counter({0:24,1:432,2:5304}),count
    assert large == Counter({1:4920,11:288,13:24,19:24,31:48}),large
    assert coprime6 == Counter({1:4632,5:144,7:144,11:288,13:24,19:24,31:48}),coprime6
    return {"method":"original 6x4 equations; permutation-expansion 4x4 and 3x3 minors",
            "processed":sum(count.values()),"ranks":dict(count),"rank2_largepart":dict(large),
            "rank2_coprime6_part":dict(coprime6),
            "seconds":round(time.monotonic()-started,6)}


def test_endpoint_table():
    data=json.loads((OUT/"endpoint-certificate.json").read_text())
    assert data["processed"] == 5760 and data["complete"]
    assert data["rank0_count"] == 24 and data["rank1_count"] == 432
    assert sum(r["count"] for r in data["rank2"]) == 5304
    for rec in data["rank2"]:
        assert primepart(rec["content"]) == 1
        assert primepart(rec["minor_gcd"]) in (1,5,7,11,13,19,31)
    for key in ("rank0","rank1_cases","exceptional_cases"):
        for rec in data[key]:
            source,target=(X,Y)[rec["source"]],(X,Y)[rec["target"]]
            m=rec["M"];p=rec["permutation"];sign=rec["sign"]
            for i in (0,1):
                assert [sum(source[i][k]*m[k][j] for k in range(2)) for j in range(2)] == [12*sign*z for z in target[p[i]]]
            h=[tuple(sum(source[i][k]*m[k][j] for k in range(2))-12*sign*target[p[i]][j] for j in range(2)) for i in range(2,6)]
            assert h == list(map(tuple,rec["H"]))
            assert content(h) == rec["content"] and minors(h) == rec["minor_gcd"]
            if key=="rank0":
                assert tuple(tuple(z//12 for z in row) for row in m) in group()
            if key=="rank1_cases":
                assert largepart(content(h)) == 1
                assert primitive(next(r for r in h if r!=(0,0))) in collision_lines()
            if key=="exceptional_cases":
                assert largepart(minors(h)) in (11,13,19,31)


def test_exceptional_systems_against_reference():
    """Replay every exceptional actual-support solution in its residue field.

    Canonicalization and ICV come directly from the immutable reference. This
    checks both elimination orientations and the declared endpoint assignment,
    including reflected solutions and the characteristic31 partner exception.
    """
    sys.path.insert(0,str(ROOT/"src"))
    from homometry import dihedral_canon,icv
    paired=json.loads((OUT/"matching-certificate.json").read_text())
    endpoints=json.loads((OUT/"endpoint-certificate.json").read_text())
    originals=(((0,0),(1,0),(-2,1),(-2,2),(0,2),(-1,3)),
               ((0,0),(1,0),(2,1),(-1,2),(1,2),(-1,3)))
    refs={}
    for p in (5,7,11,13,19,31):
        refs[p]={}
        for a in range(p):
            for b in range(p):
                sets=[tuple(sorted({(u*a+v*b)%p for u,v in side})) for side in originals]
                if any(len(side)!=6 for side in sets):
                    continue
                c=tuple(dihedral_canon(side,p) for side in sets)
                assert c[0]!=c[1] and icv(c[0],p)==icv(c[1],p)
                refs[p][(a,b)]=c
    assert all(refs[p] == {} for p in (5,7,11)), "no actual six-element Bloom parameter at5/7/11"
    for p,expected in ((7,8),(11,12)):
        projective={next((1,(v*pow(u,-1,p))%p) if u%p else (0,1)
                         for u,v in (line,)) for line in collision_lines()}
        assert len(projective)==expected==p+1
    exercised=Counter()
    for case in paired["exceptional_cases"]:
        w=case["witness"];p=largepart(minors(w["H"]));inv=pow(12,-1,p)
        for v,c in refs[p].items():
            if any(sum(row[j]*v[j] for j in range(2))%p for row in w["H"]):
                continue
            mapped=tuple(inv*sum(row[j]*v[j] for j in range(2))%p for row in w["M"])
            other=refs[p][mapped]
            assert c == (other[::-1] if w["swap"] else other)
            exercised[("paired",p)]+=1
    for case in endpoints["exceptional_cases"]:
        p=largepart(case["minor_gcd"]);inv=pow(12,-1,p)
        for v,c in refs[p].items():
            if any(sum(row[j]*v[j] for j in range(2))%p for row in case["H"]):
                continue
            mapped=tuple(inv*sum(row[j]*v[j] for j in range(2))%p for row in case["M"])
            other=refs[p][mapped]
            assert other[case["source"]] == c[case["target"]]
            exercised[("endpoint",p)]+=1
    assert set(exercised)=={("paired",13),("paired",19),("endpoint",13),("endpoint",19),("endpoint",31)}
    # Reconstruct the entire order31 Bloom graph using only reference classes.
    edges={tuple(sorted(pair)) for pair in refs[31].values()}
    adjacency={}
    for a,b in edges:
        adjacency.setdefault(a,set()).add(b);adjacency.setdefault(b,set()).add(a)
    components=[];remaining=set(adjacency)
    while remaining:
        todo=[min(remaining)];component=set()
        while todo:
            vertex=todo.pop()
            if vertex in component:
                continue
            component.add(vertex);todo.extend(adjacency[vertex]-component)
        remaining-=component;components.append(component)
    assert Counter(map(len,components))==Counter({2:45,5:1})
    cycle=next(c for c in components if len(c)==5)
    assert all(len(adjacency[v])==2 for v in cycle)
    inherited=json.loads((ROOT/"results/2026-09-30-six-prime-count/p31.json").read_text())
    assert edges=={tuple(tuple(side) for side in r["pair"]) for r in inherited["fibers"]}
    certificate={"status":"COMPUTED","p":31,"method":"all actual-support field parameters; immutable reference T/I canonicalization",
                 "pairs":len(edges),"components":{"2":45,"5":1},"cycle_classes":[list(v) for v in sorted(cycle)],
                 "cycle_edges":[[list(a),list(b)] for a,b in sorted(edges) if a in cycle]}
    (OUT/"field31-graph.json").write_text(json.dumps(certificate,indent=2)+"\n")


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--full",action="store_true");args=parser.parse_args()
    test_paired_retained_witnesses();test_endpoint_table();test_exceptional_systems_against_reference()
    endpoints=independent_endpoints()
    if args.full:
        processed,hist,r1,r2,seconds=independent_paired()
        assert processed == 4147200 and hist == Counter({0:12,1:864,2:4146324})
        data=json.loads((OUT/"matching-certificate.json").read_text())
        assert Counter({(tuple(r["direction"]),r["content"]):r["count"] for r in data["rank1"]}) == r1
        assert Counter({(r["content"],r["minor_gcd"]):r["count"] for r in data["rank2"]}) == r2
        result={"status":"COMPUTED","method":"independent exact int64 enumeration with Y pivot",
                "processed":processed,"ranks":dict(hist),"rank1_classes":len(r1),"rank2_classes":len(r2),
                "seconds":round(seconds,6),"independent_endpoints":endpoints,
                "paired_sha256":hashlib.sha256((OUT/"matching-certificate.json").read_bytes()).hexdigest(),
                "endpoint_sha256":hashlib.sha256((OUT/"endpoint-certificate.json").read_bytes()).hexdigest()}
        (OUT/"independent-audit.json").write_text(json.dumps(result,indent=2)+"\n")
        print(json.dumps(result,indent=2))
    else:
        processed,hist,_,_,_=independent_paired(7200)
        assert processed==7200 and sum(hist.values())==7200
        print("Matching-table witness, independent endpoint-minor and Y-pivot benchmark tests passed.")


if __name__=="__main__":
    main()
