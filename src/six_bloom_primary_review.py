#!/usr/bin/env python3
"""Fresh review evidence; literal raw coordinates, Y pivot, no author imports."""
import argparse
from collections import Counter, defaultdict
from itertools import combinations, permutations, product
import json
from math import gcd
from pathlib import Path
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from homometry import dihedral_canon as canonical_ti, icv as interval_vector

X = np.array(((0, 0), (1, 0), (-2, 1), (-2, 2), (0, 2), (-1, 3)), dtype=np.int64)
Y = np.array(((0, 0), (1, 0), (2, 1), (-1, 2), (1, 2), (-1, 3)), dtype=np.int64)
PERMS = np.array(list(permutations(range(6))), dtype=np.int64)
K = ((2, 0), (0, 2), (2, -2), (1, 1), (2, -1), (2, 1),
     (3, -1), (1, -2), (1, 2), (3, -2), (1, -3), (2, -3))


def raw_collisions():
    tables = {}
    for label, P in [('X', X), ('Y', Y)]:
        table = defaultdict(list)
        for i, j in combinations(range(6), 2):
            r = tuple(map(int, P[j] - P[i]))
            g = gcd(*r)
            q = tuple(t // g for t in r)
            if q[0] < 0 or (q[0] == 0 and q[1] < 0):
                q = tuple(-t for t in q)
            table[q].append((g, i, j, r))
        tables[label] = table
    assert {q: sorted({r[0] for r in v}) for q, v in tables['X'].items()} == {
        q: sorted({r[0] for r in v}) for q, v in tables['Y'].items()}
    normals = []
    for q, entries in sorted(tables['X'].items()):
        scales = sorted({e[0] for e in entries})
        assert scales in ([1], [1, 2])
        normals.append({'normal': q, 'scales': scales, 'X': entries, 'Y': tables['Y'][q]})
    return normals


def support_count():
    assert max(abs(a*d-b*c) for (a,b),(c,d) in combinations(K, 2)) == 8
    assert all(a*d-b*c for (a,b),(c,d) in combinations(K, 2))
    order_tables = []
    corrections = {}
    for m in range(2, 9):
        h = Counter()
        for a, b in product(range(m), repeat=2):
            if gcd(gcd(a,b),m) != 1:
                continue
            r = sum((u*a+v*b) % m == 0 for u,v in K)
            h[r] += 1
        corr = sum((r-1)*c for r,c in h.items() if r >= 2)
        corrections[m] = corr
        order_tables.append({'order': m, 'membership_histogram': dict(sorted(h.items())),
                             'overcount': corr})
    assert corrections == {2:15,3:16,4:18,5:24,6:12,7:24,8:12}
    checked = []
    for n in range(1, 101):
        literal = 0
        for a,b in product(range(n), repeat=2):
            x = {(u*a+v*b)%n for u,v in X.tolist()}
            y = {(u*a+v*b)%n for u,v in Y.tolist()}
            literal += len(x) == len(y) == 6
        formula = n*n-(9+3*gcd(n,2))*n+11 + sum(c for m,c in corrections.items() if n%m==0)
        assert literal == formula, (n, literal, formula)
        checked.append({'n':n,'support':literal})
    return {'order_tables':order_tables,'literal_checks':checked}


def paired_y_pivot(limit_groups=None):
    """Every paired system: eliminate w from first two Y differences."""
    hist = Counter()
    h1 = Counter()
    h2 = Counter()
    zeros = []
    bounds = [0,0]
    groups = 0
    for swap,sx,sy in product(range(2), (1,-1), (1,-1)):
        UX, UY = (Y,X) if swap else (X,Y)
        yd = UY[PERMS] - UY[PERMS[:,0]][:,None,:]
        # w_a = sy*yd_1*v, w_b = sy*(yd_2-2*yd_1)*v.
        M = sy*np.stack((yd[:,1,:], yd[:,2,:]-2*yd[:,1,:]),axis=1)
        xd = UX[PERMS] - UX[PERMS[:,0]][:,None,:]
        # axes: py, px, residual row, source parameter coordinate.
        HX = np.einsum('ij,pjk->pik',X[1:],M)[:,None,:,:] - sx*xd[None,:,1:,:]
        HY = np.einsum('ij,pjk->pik',Y[3:],M) - sy*yd[:,3:,:]
        H = np.concatenate((HX,np.broadcast_to(HY[:,None,:,:],(720,720,3,2))),axis=2)
        c = np.gcd.reduce(np.abs(H).reshape(720,720,-1),axis=2)
        D = np.zeros((720,720),dtype=np.int64)
        bounds[0] = max(bounds[0],int(np.abs(H).max()))
        for i,j in combinations(range(8),2):
            minor = H[:,:,i,0]*H[:,:,j,1]-H[:,:,i,1]*H[:,:,j,0]
            bounds[1] = max(bounds[1],int(np.abs(minor).max()))
            D = np.gcd(D,np.abs(minor))
        z = c == 0
        r1 = (c != 0)&(D == 0)
        r2 = D != 0
        hist.update({0:int(z.sum()),1:int(r1.sum()),2:int(r2.sum())})
        for py,px in np.argwhere(z):
            zeros.append({'swap':swap,'sx':sx,'sy':sy,'px':PERMS[px].tolist(),
                          'py':PERMS[py].tolist(),'M':M[py].tolist()})
        for py,px in np.argwhere(r1):
            rows = H[py,px]
            rr = next(r for r in rows if np.any(r))
            g = gcd(int(rr[0]),int(rr[1]))
            q = tuple(int(t)//g for t in rr)
            if q[0]<0 or (q[0]==0 and q[1]<0): q=tuple(-t for t in q)
            h1[(q[0],q[1],int(c[py,px]))] += 1
        pairs,freq = np.unique(np.stack((c[r2],D[r2]),axis=1),axis=0,return_counts=True)
        h2.update({tuple(map(int,q)):int(n) for q,n in zip(pairs,freq)})
        groups += 1
        print('Y-pivot group',groups,'processed',sum(hist.values()),flush=True)
        if limit_groups and groups >= limit_groups: break
    return {'processed':sum(hist.values()),'ranks':dict(hist),
            'rank0':zeros,'rank1':[{'direction':[a,b],'content':c,'count':v} for (a,b,c),v in sorted(h1.items())],
            'rank2':[{'content':c,'minor_gcd':d,'count':v} for (c,d),v in sorted(h2.items())],
            'max_entry':bounds[0],'max_minor':bounds[1]}


def original_endpoint_minors():
    """No elimination: all5×4 original translated equations, exact expanded minors."""
    matrices = []
    for S,U,s in product((X,Y),(X,Y),(1,-1)):
        d = U[PERMS]-U[PERMS[:,0]][:,None,:]
        A = np.concatenate((np.broadcast_to(S[None,1:,:],(720,5,2)),-s*d[:,1:,:]),axis=2)
        matrices.append(A)
    A = np.concatenate(matrices,axis=0)
    minor_gcds = {}
    for k in (3,4):
        D = np.zeros(5760,dtype=np.int64)
        for rr in combinations(range(5),k):
            for cc in combinations(range(4),k):
                B = A[:,rr,:][:,:,cc]
                v = np.zeros(5760,dtype=np.int64)
                for p in permutations(range(k)):
                    parity = sum(p[i]>p[j] for i in range(k) for j in range(i+1,k))%2
                    term = np.ones(5760,dtype=np.int64)
                    for i in range(k): term *= B[:,i,p[i]]
                    v += (-1 if parity else 1)*term
                D = np.gcd(D,np.abs(v))
        minor_gcds[k] = D
    c = minor_gcds[3]
    D = minor_gcds[4]
    hist = Counter()
    h1 = Counter()
    h2 = Counter()
    for u,v in zip(c,D):
        if u==v==0: hist[2]+=1
        elif v==0: hist[3]+=1;h1[int(u)]+=1
        else: hist[4]+=1;h2[(int(u),int(v))]+=1
    return {'processed':5760,'original_matrix_ranks':dict(hist),
            'rank3_third_minor_gcd':dict(h1),
            'rank4':[{'third_minor_gcd':c,'fourth_minor_gcd':d,'count':v} for (c,d),v in sorted(h2.items())]}


def small_images():
    R = np.array(((0,-1),(1,-1)),dtype=np.int64)
    T = np.array(((0,1),(1,0)),dtype=np.int64)
    eye = np.eye(2,dtype=np.int64)
    group = [sgn*(np.linalg.matrix_power(R,i) @ (T if j else eye))
             for sgn,i,j in product((1,-1),range(3),range(2))]
    answer=[]
    for n in sorted({d for D in (1,2,3,4,5,6,7,8,9,12,13,16,19) for d in range(1,D+1) if D%d==0}):
        fibers=defaultdict(list)
        congruent=[]
        vertices=defaultdict(set)
        orders=Counter()
        for a,b in product(range(n),repeat=2):
            x={(int(u)*a+int(v)*b)%n for u,v in X}
            y={(int(u)*a+int(v)*b)%n for u,v in Y}
            if len(x)!=6 or len(y)!=6:continue
            assert interval_vector(x,n)==interval_vector(y,n)
            cx=canonical_ti(x,n);cy=canonical_ti(y,n)
            key=tuple(sorted((cx,cy)))
            fibers[key].append((a,b))
            if cx==cy:congruent.append((a,b))
            else:vertices[cx].add(cy);vertices[cy].add(cx)
            orbit={tuple(map(int,g @ np.array((a,b)))) for g in group}
            assert len({(u%n,v%n) for u,v in orbit})==12
            orders[n//gcd(gcd(a,b),n)]+=1
        answer.append({'n':n,'support':sum(map(len,fibers.values())),
                       'parameter_orders':dict(orders),'congruent_parameters':congruent,
                       'fiber_size_histogram':dict(Counter(map(len,fibers.values()))),
                       'fiber_count':len(fibers),'nontrivial_edges':len(fibers)-bool(congruent),
                       'max_graph_degree':max(map(len,vertices.values()),default=0),
                       'exceptional_fibers':[{'classes':key,'parameters':v} for key,v in fibers.items() if len(v)!=12 or key[0]==key[1]]})
    return answer


def even_controls():
    """Fresh literal/reference replay of the displayed even-modulus family."""
    answer=[]
    for m in range(9,129):
        n=2*m
        v=(m+3,1);w=(-3,m-2)
        x,y=[{(int(u)*v[0]+int(t)*v[1])%n for u,t in P} for P in (X,Y)]
        xx,yy=[{(int(u)*w[0]+int(t)*w[1])%n for u,t in P} for P in (X,Y)]
        assert x=={0,2,2*m-5,2*m-4,m,m+3}
        assert y=={0,7,m-1,m,m+3,m+5}
        assert xx=={0,2,2*m-4,2*m-3,m-3,m+4}
        assert yy=={0,m-8,m-3,2*m-7,2*m-3,2*m-1}
        assert all(len(s)==6 for s in (x,y,xx,yy))
        assert xx=={(t-(m+3))%n for t in y}
        assert gcd(gcd(*v),n)==gcd(gcd(*w),n)==1
        assert all(z%n!=(-3)%n for z in (1,-1,m+3,-m-3,m+2,-m-2))
        classes=[canonical_ti(s,n) for s in (x,y,xx,yy)]
        assert classes[1]==classes[2] and len(set(classes))==3
        assert len({interval_vector(s,n) for s in (x,y,xx,yy)})==1
        answer.append({'n':n,'v':v,'w':w,'supports':[sorted(s) for s in (x,y,xx,yy)],
                       'classes':classes,'icv':interval_vector(x,n)})
    return answer


def main():
    start=time.monotonic()
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',default=str(ROOT/'results/2026-10-01-six-primary-review/independent-audit.json'))
    parser.add_argument('--benchmark',action='store_true')
    args=parser.parse_args()
    if args.benchmark:
        print(json.dumps(paired_y_pivot(1)));return
    result={'status':'COMPUTED','python':sys.version,'numpy':np.__version__,
            'raw_collision_catalogue':raw_collisions(),'support':support_count(),
            'paired':paired_y_pivot(),'endpoint_original_minors':original_endpoint_minors(),
            'small_images':small_images(),'even_endpoints':even_controls()}
    result['seconds']=time.monotonic()-start
    Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
    print('DONE',result['seconds'],'seconds',args.out)


if __name__=='__main__': main()
