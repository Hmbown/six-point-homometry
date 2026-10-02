"""Exact algebra, shape completeness, and unbounded lift regressions.

Use .venv/bin/python. Independent kernels use pair-difference Counters and
direct mixed differences, rather than the production interval/decomposition
kernels. A separate review script audits the negative shadow certificates.
"""
from collections import Counter
from itertools import combinations, product
from math import gcd
from pathlib import Path
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from sympy import Matrix
from homometry import icv as reference_icv
from six_explore import bloom, bloom_edges, canon
from six_inventory import components, inherited_menu
from six_shell import h6_edges, periodic_decomposition, recover_common, shape_certificate
from six_shadow import (anchored_vector, coprime_kernel_lift, matching_count,
                        matching_matrices, shadow_decision, smith_kernel_lift)


def differences(points, n=None):
    return Counter((x-y) % n if n else x-y for x in points for y in points)


def test_bloom_free_identity():
    x = ((0,0), (1,0), (-2,1), (-2,2), (0,2), (-1,3))
    y = ((0,0), (1,0), (2,1), (-1,2), (1,2), (-1,3))
    def auto(points):
        return Counter((a-c, b-d) for a,b in points for c,d in points)
    assert auto(x) == auto(y)
    for n in (12,17,18,21,24,31,37,60):
        for p,q in product(range(n),repeat=2):
            a,b = bloom(p,q,n)
            if len(a) == len(b) == 6:
                assert differences(a,n) == differences(b,n), (n,p,q)
                assert reference_icv(a,n) == reference_icv(b,n)


def test_dyad_identity_and_decomposition():
    rng = random.Random(20260930)
    for trial in range(400):
        n = rng.randrange(8,61)
        a,b = rng.sample(range(1,n),2)
        r = {0,a,b,(a+b)%n}
        if len(r)!=4:
            continue
        c = rng.sample(sorted(set(range(n))-r),4)
        aa,bb = c+[0,(a+b)%n], c+[a,b]
        w = Counter(c)
        w.update((a+b-x)%n for x in c)
        w.update(r)
        lhs = differences(aa,n)
        lhs.subtract(differences(bb,n))
        rhs = Counter()
        for x,coefficient in w.items():
            for shift,sign in ((-a-b,1),(-b,-1),(-a,-1),(0,1)):
                rhs[(x+shift)%n] += sign*coefficient
        assert all(lhs[x]==rhs[x] for x in range(n))
    # Exhaustive nonnegative inputs, including overlapping subgroups and
    # fixed points. This attacks the integrality/positivity extension of D1.
    for n in range(2,7):
        for w in product(range(3),repeat=n):
            for a,b in product(range(n),repeat=2):
                mixed = all(w[x]-w[(x-a)%n]-w[(x-b)%n]+w[(x-a-b)%n]==0 for x in range(n))
                split = periodic_decomposition(w,a,b)
                assert (split is not None) == mixed, (n,w,a,b)
                if split:
                    u,v=split
                    assert sum(u)+sum(v)==sum(w)


def test_shape_complete_small():
    checked, accepted = 0,0
    for n in range(8,13):
        for a,b in combinations(range(1,n),2):
            r={0,a,b,(a+b)%n}
            if len(r)!=4:
                continue
            for c in combinations(sorted(set(range(n))-r),4):
                aa,bb=c+(0,(a+b)%n),c+(a,b)
                w=[0]*n
                for x in c:
                    w[x]+=1;w[(a+b-x)%n]+=1
                for x in r:
                    w[x]+=1
                equal = differences(aa,n)==differences(bb,n)
                split = periodic_decomposition(w,a,b)
                assert equal == (split is not None), (n,a,b,c)
                if split:
                    assert c in set(recover_common(w,a,b))
                    assert min(n//gcd(a,n),n//gcd(b,n))<=12
                    accepted+=1
                checked+=1
    assert checked>3000 and accepted>100
    for n in (12,18,24,30,36,42,48,54,60):
        edges=h6_edges(n)
        for (x,y),params in edges.items():
            assert reference_icv(x,n)==reference_icv(y,n)
            assert x!=y and x==canon(x,n) and y==canon(y,n)
            assert shape_certificate(x,y,n) is not None
        if n==18:
            for x,y in (((0,1,4,6,10,13),(0,1,4,7,9,13)),
                        ((0,1,3,6,10,12),(0,1,3,7,9,12)),
                        ((0,1,3,9,10,15),(0,1,3,9,12,13))):
                assert (x,y) in edges


def test_exact_lifts_and_caps():
    aa=(0,1,4,10,12,17)
    bb=(0,1,8,11,13,17)
    for n in (257,257**2,257*263):
        matrices=list(matching_matrices(aa,bb,n))
        assert matching_count(aa,bb,n)==len(matrices)==1
        m,_=matrices[0]
        v=anchored_vector(aa,bb,n)
        for lift in (coprime_kernel_lift(m,v,n),smith_kernel_lift(m,v,n)[0]):
            assert lift is not None
            x,y=(0,)+lift[:5],(0,)+lift[5:]
            assert differences(x)==differences(y)
            assert tuple(z%n for z in x)==aa and tuple(z%n for z in y)==bb
        assert shadow_decision(aa,bb,n)["decision"]=="shadow"
    a,b=(0,1,3,8,12,14),(0,1,4,6,12,14)
    d=shadow_decision(a,b,17,limit=3)
    assert d["decision"]=="undecided-capped" and d["checked_matchings"]==3
    assert d["expected_matchings"]==192
    # Antipodal edges allow both signs even with a fixed edge matching.
    a=(0,1,2,3,4,6)
    count=matching_count(a,a,12)
    signs={}
    for index,(m,labels) in enumerate(matching_matrices(a,a,12)):
        assert all(int(x)%12==0 for x in m*Matrix(anchored_vector(a,a,12)))
        for i,j,k,ell,s in labels:
            if (a[j]-a[i])%12==6:
                signs.setdefault((i,j,k,ell),set()).add(s)
        if index>=200:
            break
    assert any(values=={1,-1} for values in signs.values())
    assert count>200


def test_inventory_basics():
    mem=((0,1),(0,2),(0,3))
    assert components(mem,[])==3
    assert components(mem,[(mem[0],mem[1])])==2
    assert components(mem,[(mem[0],mem[1]),(mem[1],mem[2])])==1
    menu=inherited_menu(18)
    pair=((0,1,4,6,10,13),(0,1,4,7,9,13))
    assert pair in menu and menu[pair]["inherited_cZ"]=="0"
    assert not bloom_edges(6)


if __name__=="__main__":
    for test in (test_bloom_free_identity,test_dyad_identity_and_decomposition,
                 test_shape_complete_small,test_exact_lifts_and_caps,test_inventory_basics):
        test()
        print("PASS",test.__name__,flush=True)
