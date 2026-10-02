# Fresh adversarial review of the field/prime Bloom theorem

30 September 2026. **Review verdict: ACCEPT Theorems A–C for their stated
scope; ACCEPT D–E with their expressly retained dependencies.** This is a
separate in-house adversarial reread, not external specialist review, novelty
establishment or proof-assistant verification. The author owns status promotion.
The controls below are **[COMPUTED]** supporting checks; the argument for A–C
is the written algebraic proof, not extrapolation from those checks.

## 1. Review independence and accepted bytes

I read `AGENTS.md`, the program's definitions/status rules and the full
`notes/2026-09-30-six-prime-theorem.md` first. I did not assume its theorems
or use an author's summary as mathematical evidence. I attacked the main
proof and independently expanded its equations before reading
`notes/2026-09-30-six-prime-symmetries.md`. I subsequently read both new
implementations and their complete test sources. The author then added E;
I separately checked its finite-count interface. Only this review file was
written by this reviewer; protected reference files, data, ledgers, code,
other authors' notes and concurrent outputs were not changed.

Accepted final frozen E-inclusive proof source:

```
notes/2026-09-30-six-prime-theorem.md
SHA256 673d22305ac9a75eff85ec6506405dfb0692c5c51a70a80114db25bc2356289e
```

The mathematical-body digest is SHA256
`eef83cfea29a3283846bf8fcb98ca82964975cf49ab291238daa06405cc9ba1f`,
of the exact UTF-8 substring starting at `## 1. Definitions and statements`
and ending immediately before `## 7. Verification, prior art and remaining scope`.
This includes A–E and all their written proofs. The final source changed
only status, opening dependency wording and the evidence/reproduction
section from the accepted E-inclusive source with SHA256
`5eafaccc3c961241fddc8d3ed3150194373acb3f7cd386e4fa7fbb22f0a40fbe`;
the mathematical-body digest is unchanged. The earlier A–D source,
also accepted before E was added, had SHA256
`3dafe11863520b9e18161f9f9ac6d7ef9c80185239a0b11b0c005f4189b102c8`.

Other reviewed source hashes:

| Source | SHA256 |
|---|---|
| `notes/2026-09-30-six-prime-symmetries.md` | `56763e210e2645c06951675f75136d8235d8d941eb473e58d8906208f2c72bab` |
| `src/six_prime_bloom.py` | `243efb65973a53e9e4a54fc272d450c32ff5c10a3ae1258b8e29bfbc8b79fef5` |
| `src/six_bloom_invariants.py` | `7e60e878e8955846c4e601310e48c96bfa86817c69a84e2f7ad70b7452dde59d` |
| `tests/test_six_prime_bloom.py` | `1716cb8ebe1601970d1ff12ec3bbb6515cdb04b54d15317eb8d006af594b0098` |
| `tests/test_six_bloom_invariants.py` | `8a9abec2c1eb330163cdd2f98e8e1d8d578e7501b37354d18bfaf29718f9ed0d` |

The auxiliary note was subsequently promoted by its author using only
review/status wording changes. The reviewed pre-status digest above is
retained; its current status-only derivative has SHA256
`74d0f8f5c866cd16f2dac1fbf0859d7a6b45234108bc20177e8bf4a52d1f828b`.

## 2. Mathematical attacks and their outcomes

1. **Homometry versus multiplicity/collision issues.** I recomputed the
   coefficient-space directed differences, obtaining equality of the full
   36-entry counters, including six diagonal zero entries. On the specified
   support-admissible locus the lists represent sets, so the integer identity
   really gives the directed autocorrelations. It requires no ordering of K
   and permits repeated nonzero distances. It therefore applies to arbitrary
   fields in the stated scope, not just prime cyclic fields.

2. **Exact support locus.** Every within-endpoint difference yields one of
   the twelve primitive normals; their discarded integer common factors are
   only invertible factors of two. Independent exact determinant computation
   gives `{1,2,3,4,5,7,8}`. There is no omitted support exclusion. In
   characteristics 5 and 7 the reduced normals give exactly six and eight
   distinct lines. They cover the prime-field projective line but not all
   extension-field directions. Consequently the nonempty extension-field
   cases must not be discarded merely because F5 and F7 themselves have
   no admissible parameter. In characteristic 11 the twelve slopes cover
   F11's projective line, but that observation licenses no extension-field
   theorem in characteristic 11.

3. **Group and accidental stabilizers.** I checked all matrix relations and
   closure, the twelve distinct matrices, all six endpoint transport rows,
   and distinctness also after reduction in characteristics 5 and 7. The
   translations on the two endpoints genuinely differ where stated. Rotation
   fixed-space determinants use only 1 or 3; negation needs only invertible
   2. Every remaining involution's fixed line is a forbidden support line.
   Thus there is no exceptional admissible stabilizer in any allowed field.

4. **Independent endpoint translations/inversions and interchange.** A
   translated six-set has centroid mu+t because 6 is invertible. The centered
   coordinates therefore do not change. Negation changes an odd moment's
   sign; squaring m3 removes it. The even moments are invariant, and sums of
   endpoint invariants survive interchange. These are invariants of the exact
   quotient specified in the statement, with each endpoint transformed
   independently. No shared translation or shared inversion is assumed.

5. **Moment algebra and exceptional characteristics.** SymPy expansion from
   the original, uncentered coordinates independently checks m2, both m3
   identities, both individual m6 identities, d²+27e²=4s³, the squared-m3
   coefficients and the cubic factorization. The elimination identity
   `118 C6 - 13 C3 = 162 e²` is exact over Z. Its denominators use only
   66 and 162, so the scope excludes precisely 2,3,11 at this step. A single
   coefficient would fail at 79 or 239; the combined identity does not.
   Explicit checks and exhaustive prime fibers at both exceptional primes
   pass. Nothing divides by s: admissible isotropic parameters are included.

6. **Reconstruction from roots, including degeneracy.** Equality of e²
   gives e(w)=e(v) or -e(v) over a field; replacing w by -w corrects the
   latter without changing s. The resulting factorizations of
   z³-sz-e have the same root multiset by uniqueness of factorization, even
   if a root repeats. The ordered roots are (a,-b,b-a), R cycles them and
   -T transposes the first two, realizing every permutation. The first two
   roots recover the parameter vector. This proves orbit separation over
   every allowed field, not merely over an algebraic closure or an ordered
   field. In fact d is nonzero on Omega, so its cubic discriminant d² is
   nonzero there; the proof did not need that stronger observation.

7. **Nontriviality and a hidden unit quotient.** Both e and d have their
   factors among the collision equations, so they are nonzero on Omega.
   The squared-third-moment difference -5832de is therefore nonzero in
   every allowed characteristic. Each pair's endpoints are different rigid
   classes. Orbit reconstruction uses only the twelve matrices, not all
   field scalars. A general scalar can occasionally land in the same
   twelve-orbit, but there is no quotient by its full multiplicative group.
   The independent direct enumeration anchors only translations and ±1;
   the test's p19 multiplication-by-2 control retains two different pairs.

8. **Finite-field count.** Different K-lines through zero meet only at zero
   and each has q-1 nonzero elements. Base-field slopes do not acquire
   identifications in an extension. Thus the excluded count is exactly
   1+d_p(q-1), with d5=6, d7=8 and d_p=12 for p>=13. Freeness and exact
   orbit separation permit division by twelve, giving B's three cases.
   The two independent custom-extension computations agree at q25,49,169.
   Neither A nor B claims classification of all six-set homometry in those
   noncyclic additive groups.

9. **Unique partner and the boundary at 31.** Squaring the cubic moment
   and expanding the individual sixth moment gives precisely the displayed
   2-by-2 system. Its exact determinant is -263594736=-2^4*3^12*31. For
   a Y endpoint the second unknown is -de; the first unknown remains e².
   Thus it need not be known which side the endpoint occupies, nor need
   s be nonzero. A shared rigid class recovers the same s,e², hence the
   same pair by A. At 31 I checked all four transport identities for the
   two parameters, distinctness of the three rigid classes by full anchored
   translation/reflection, and all fifteen cyclic distances occurring once.
   The invariants really are (s,e²)=(0,2) and (0,8). This disproves the
   extension of C to characteristic 31; it does not impair A or B there.
   The witness also persists under embedding F31 into an extension, since
   a translation identifying two nonempty base-field sets lies in the base
   field. No positive uniqueness claim is made for such extensions.

10. **Auxiliary formal-symmetry argument.** Only after the first attack I
    recomputed its centroids/covariance, the 8/33 versus 14/33 split, and
    all six inner-triangle permutations for P->P and P->Q. Exactly the
    stated three maps in each list preserve the outer triple. Its inverses
    and conjugation explain the other two directions. The small-characteristic
    scope of this auxiliary argument uses only invertible 2,3,11, as
    claimed. Formal planar completeness alone would not have excluded
    projected accidents; the main proof correctly supplies the separate
    moment-and-root argument.

No mathematical flaw, counterexample to the stated A–C, or missing quotient
identification was found. A small editorial correction was sent to the
author: after adding E, the introduction's singular “final total-count
corollary” should name both total-count corollaries and E's finite census.
It does not affect the proof and is corrected in the accepted final source.

## 3. Exact scope and dependency attack on D–E

D is conditional on the inherited large-prime result. I read its exact
statement and proof interface in `notes/2026-09-30-six-paper.tex`,
lines 1629–1650: every prime divisor of n must exceed 131; the universal
torsion order is at most 135; the least possible such prime is 137; the
torsion image consequently vanishes; an integer functional gives faithful
within-endpoint lifts; the line/shadow obligation then gives Bloom. At a
prime p>131 this covers every nontrivial six-set pair. Since p!=31, C
then makes every nontrivial family an edge, and B gives its count. I did
**not** re-review or re-run G, its universal torsion bound, UNSAT solvers,
finite matching certificates or complete census. Their exact qualification
and trusted dependencies remain part of D.

E adds inherited complete six-only censuses at the finitely many primes
through 131. I independently reread the payloads at all 27 primes from
13 through 131, recomputed every member's ICV and reference T/I canonical
form, checked member uniqueness/disjointness and unique family ICVs,
formed every unordered edge, and checked all Bloom edges are present.
Where both small and large census payloads exist, the family sets agree.
Their ordering differs at p13; an initial order-sensitive comparison was
replaced by the correct comparison of ICV-keyed family sets. This was a
review-check issue, not a missing family or a theorem repair.

The correction formulas agree at all 27 primes. The exceptional rows are:

| p | B(p) | total unordered pairs | maximal families | family sizes |
|---:|---:|---:|---:|---|
| 17 | 8 | 16 | 16 | all 2 |
| 19 | 12 | 21 | 21 | all 2 |
| 23 | 22 | 33 | 33 | all 2 |
| 31 | 50 | 70 | 61 | sixty 2, one 5 |

At p31, 60+binomial(5,2)=70 explains why the pair and family corrections
are different. Every other prime 13..131 has B(p) pairs/families, all of
size two. Complete fresh immutable-reference enumerations at p7 and p11
have no nontrivial six-family; primes below six cannot support a six-set.
For p>131, D supplies the infinite range. E is therefore accepted with
finite-census completeness explicitly inherited; a payload audit is not
a new proof that no family was omitted by the original enumeration.

Chosen exceptional census file hashes (the replay below reports all 27):

```
results/2026-09-30-six-census/n17.json 7dea6238f3225f0a9512063eaa27d05cec647b497ce741b0da45e4bd37bd2f7a
results/2026-09-30-six-census/n19.json 3d0e7e7264f37405ef2c7e0d5bbf05014906f17b943bad377e551020e02e947b
results/2026-09-30-six-census/n23.json c96634a2074c3d72c12e16f1b2f10ae668269643b0afff6677da9d1090a43f50
results/2026-09-30-six-census/n31.json a52768b6bc6234054a271dbaf2d71b74d262037b3a9b77684e88fa1bee90634d
results/2026-09-30-six-large-census/n131.json ebc01205598d3307c11d6ba1b63865a3d3db6966d67dd854fec128f267b832fc
```

## 4. Code, tests and independent controls

Commands executed from `.`:

```text
.venv/bin/python tests/run_tests.py
.venv/bin/python tests/test_env.py
.venv/bin/python tests/test_six_prime_bloom.py
.venv/bin/python tests/test_six_bloom_invariants.py
```

Results: immutable reference 10/10, pinned environment 5/5, direct-enumerator
tests 6/6, invariant tests 8/8 with no skip. The added eighth test freshly
executes the small-prime payload audit; I read its implementation and test
before rerunning the final eight-test source. The environment was Python
3.12.12 with NumPy 2.5.3. The last test independently checked the completed
50-prime replay report; the review did not rerun the entire 50-prime job.

I inspected `results/2026-09-30-six-prime-invariants/summary.json`, SHA256
`abe274ca0c69933881a3c0515e53e4fce8c763f9831f8c0c2b5edd69214d42d8`.
Its embedded source hash agrees with the reviewed invariant source. It
reports every prime 13..251 and 1009, exact equality of the full direct
parameter partitions with the separately enumerated invariant partitions,
and actual endpoint moments bound to the corresponding invariant keys.
Selected independently checked numbers are p79:442, p239:4522,
p1009:83832; all fibers have twelve parameters. At 31 the report has
50 Bloom edges, ninety degree-one vertices and five degree-two vertices.
The extension reports are q25:40, q49:168 and q169:2212. The final report
also adds the explicit small-prime census payload audit, with all inherited
file and method/source hashes. The earlier 50-prime/field report without
that addition had SHA256
`14c8c747ac59ee99266a3fa737c8972b499407f2855005e6fe928285541a722c`.

The direct implementation enumerates every a,b, excludes support collisions
from actual lists, and retains full fibers. Its gap-word canonicalizer
performs exactly cyclic T/I; its tests compare it with the immutable
reference on all small subsets and all relevant parameter controls. The
invariant implementation independently uses collision normals and polynomial
keys; it never obtains its prime counts by constructing chord classes.
Its tiny integer coefficient kernel was cross-checked here with SymPy.
Its quadratic-field canonicalizer anchors only ±1 and translations.

`replay_direct` is a complementary invariant/moment partition audit,
not a standalone verifier against arbitrary corrupted endpoints: it does
not itself reevaluate every saved parameter's raw point sets. That binding
is supplied by the separately passing direct-artifact test, which checks
every parameter against the saved actual pair. I rely on both checks
together when describing the saved computational evidence. This does not
create a dependency for the algebraic A–C proof.

My own independent controls, reproduced below, use explicit original
coordinates, anchored endpoint rigid motions and separate arithmetic.
All p² parameters were checked at p2,3,5,7,11,13,17,19,31,79,239; exact
pair fibers equal invariant fibers and generated twelve-orbits. For
p13,17,19,31,79,239 the counts are 2,8,12,50,442,4522. At p31 the
maximum Bloom vertex degree is two; at the other tested allowed primes
it is one. Admissible s=0 parameters were explicitly encountered at
p13 (24), p19 (36), p31 (60), p79 (156).

Independent quadratic arithmetic used F5[t]/(t²-2), F7[t]/(t²-3),
F13[t]/(t²-2), verified nonresidue status and that every nonzero element
satisfies x^(q-1)=1. It checked every pair fiber, support-normal equivalence,
orbit size, complete moment extraction and single-endpoint e² recovery.
Counts are 40,168,2212 and isotropic parameter counts are 48,0,336.
The original field-control command had a missing space in a Python `else`
expression and stopped before executing; the corrected command passes.
No mathematical change resulted from that syntax correction.

## 5. Reproduction of the review's independent checks

Each following Python block is a self-contained review check. Their exact
extraction command below was executed after saving this note; every symbolic,
prime, quadratic-field and finite-census assertion passed. Run them all
without writing a helper file using exactly:

```text
.venv/bin/python - <<'PY'
from pathlib import Path
import re
text = Path('notes/2026-09-30-six-prime-review.md').read_text()
for code in re.findall(r'```python\n(.*?)\n```', text, re.S):
    exec(compile(code, '<prime-review-control>', 'exec'), {})
PY
```

```python
# REVIEW-CHECK: exact symbolic expansion and transport identities
from collections import Counter
from itertools import combinations
from math import gcd
import sympy as sp
a,b,z=sp.symbols('a b z')
P=[(0,0),(1,0),(-2,1),(-2,2),(0,2),(-1,3)]
Q=[(0,0),(1,0),(2,1),(-1,2),(1,2),(-1,3)]
x=[u*a+v*b for u,v in P];y=[u*a+v*b for u,v in Q]
s=a*a-a*b+b*b;e=a*b*(a-b);d=(a+b)*(2*a-b)*(a-2*b)
assert Counter((u-u2,v-v2) for u,v in P for u2,v2 in P)==Counter((u-u2,v-v2) for u,v in Q for u2,v2 in Q)
assert sp.expand(d*d+27*e*e-4*s**3)==0
assert sp.expand((z-a)*(z+b)*(z-b+a)-(z**3-s*z-e))==0
for C,sg in [(x,-1),(y,1)]:
    cen=[3*c-sum(C)/2 for c in C]
    assert sp.expand(sum(c**2 for c in cen)-66*s)==0
    assert sp.expand(sum(c**3 for c in cen)-(6*d+sg*243*e))==0
    assert sp.expand(sum(c**6 for c in cen)-(23946*s**3+6399*e*e+sg*4860*d*e))==0
c3=(6*d-243*e)**2+(6*d+243*e)**2-288*s**3
c6=2*(23946*s**3+6399*e*e)-47892*s**3
assert sp.expand(118*c6-13*c3-162*e*e)==0
assert sp.Matrix([[58077,-2916],[6399,-4860]]).det()==-2**4*3**12*31
I=sp.eye(2);R=sp.Matrix([[0,-1],[1,-1]]);T=sp.Matrix([[0,1],[1,0]])
ms=[I,R,R**2,T,R*T,R**2*T];G=ms+[-M for M in ms]
assert len(set(tuple(M) for M in G))==12
assert all(any(U*V==W for W in G) for U in G for V in G)
trs=[(x,0,y,0),(x,2*a-2*b,y,a-3*b),(x,-2*b,y,-2*a-b),(y,a-2*b,x,2*a-b),(y,-a,x,-a),(y,-a-2*b,x,a-3*b)]
for M,(X,t,Y,u) in zip(ms,trs):
    aa,bb=M*sp.Matrix([a,b])
    xx=[sp.expand(c.subs({a:aa,b:bb},simultaneous=True)) for c in x]
    yy=[sp.expand(c.subs({a:aa,b:bb},simultaneous=True)) for c in y]
    assert Counter(xx)==Counter(sp.expand(c+t) for c in X)
    assert Counter(yy)==Counter(sp.expand(c+u) for c in Y)
norms=set()
for C in [P,Q]:
    for v,w in combinations(C,2):
        u,t=v[0]-w[0],v[1]-w[1];g=gcd(abs(u),abs(t));u//=g;t//=g
        if u<0 or(u==0 and t<0):u=-u;t=-t
        norms.add((u,t))
assert len(norms)==12
assert {abs(u[0]*v[1]-u[1]*v[0]) for u,v in combinations(norms,2)}=={1,2,3,4,5,7,8}
print('PASS independent exact symbolic control')
```

```python
# REVIEW-CHECK: all raw prime parameters, independent anchored rigid quotient
from collections import Counter,defaultdict
P=((0,0),(1,0),(-2,1),(-2,2),(0,2),(-1,3))
Q=((0,0),(1,0),(2,1),(-1,2),(1,2),(-1,3))
for p in (2,3,5,7,11,13,17,19,31,79,239):
    def points(a,b,C):return tuple((u*a+v*b)%p for u,v in C)
    def rigid(A):return min(tuple(sorted((sg*(x-t))%p for x in A)) for sg in(-1,1) for t in A)
    def orbit(a,b):
        out=set();todo=[(a,b)]
        while todo:
            v=todo.pop()
            if v in out:continue
            out.add(v);a0,b0=v
            todo.extend([((-b0)%p,(a0-b0)%p),(b0,a0),((-a0)%p,(-b0)%p)])
        return out
    fibers=defaultdict(set);invs=defaultdict(set);degree=defaultdict(set);isotropic=0
    for a in range(p):
        for b in range(p):
            X,Y=points(a,b,P),points(a,b,Q)
            if len(set(X))<6 or len(set(Y))<6:continue
            pair=tuple(sorted((rigid(X),rigid(Y))));assert pair[0]!=pair[1]
            fibers[pair].add((a,b));s=(a*a-a*b+b*b)%p;e2=(a*b*(a-b))**2%p
            invs[s,e2].add((a,b));isotropic+=s==0
            degree[pair[0]].add(pair);degree[pair[1]].add(pair)
    assert all(len(V)==12 and V==orbit(*next(iter(V))) for V in fibers.values())
    assert {frozenset(V) for V in fibers.values()}=={frozenset(V) for V in invs.values()}
    assert len(fibers)==(0 if p<13 else(p-1)*(p-11)//12)
    if p>=13 and p!=31:assert max(map(len,degree.values()),default=0)==1
    if p==31:
        A=(0,1,3,8,12,18);B=(0,1,3,10,14,26);C=(0,1,4,10,12,17)
        X,Y=points(2,12,P),points(2,12,Q);W,Z=points(8,17,P),points(8,17,Q)
        assert set(A)=={(3-t)%p for t in Y}==set(W)
        assert set(B)=={(3-t)%p for t in X};assert set(C)=={(12-t)%p for t in Z}
        assert len({rigid(A),rigid(B),rigid(C)})==3
        for E in(A,B,C):assert Counter(min((x-y)%p,(y-x)%p) for i,x in enumerate(E) for y in E[i+1:])==Counter(range(1,16))
    print('PASS prime',p,'pairs',len(fibers),'isotropic',isotropic,'max degree',max(map(len,degree.values()),default=0))
```

```python
# REVIEW-CHECK: independently implemented quadratic arithmetic and all moments
from collections import defaultdict
from functools import reduce
P=((0,0),(1,0),(-2,1),(-2,2),(0,2),(-1,3));Q=((0,0),(1,0),(2,1),(-1,2),(1,2),(-1,3))
N=((1,0),(0,1),(-1,1),(1,1),(-2,1),(2,1),(-3,1),(-1,2),(1,2),(-3,2),(-1,3),(-2,3))
for p,n in ((5,2),(7,3),(13,2)):
    q=p*p;assert all(x*x%p!=n for x in range(p))
    def add(x,y):return (x%p+y%p)%p+p*((x//p+y//p)%p)
    def neg(x):return (-x%p)+p*(-(x//p)%p)
    def sub(x,y):return add(x,neg(y))
    def mul(x,y):return (x%p*(y%p)+n*(x//p)*(y//p))%p+p*((x%p*(y//p)+(x//p)*(y%p))%p)
    def scl(k,x):return mul(k%p,x)
    def power(x,k):
        a=1
        while k:
            if k&1:a=mul(a,x)
            x=mul(x,x);k//=2
        return a
    def total(E):return reduce(add,E,0)
    assert all(power(x,q-1)==1 for x in range(1,q))
    def pts(a,b,C):return tuple(add(scl(u,a),scl(v,b)) for u,v in C)
    def rigid(E):return min(tuple(sorted(scl(sg,sub(x,t)) for x in E)) for sg in(-1,1) for t in E)
    def moments(E):
        half=scl(pow(2,-1,p),total(E));Z=[sub(scl(3,x),half) for x in E]
        return tuple(total(power(x,j) for x in Z) for j in(2,3,6))
    def orbit(a,b):
        out=set();todo=[(a,b)]
        while todo:
            a0,b0=todo.pop()
            if(a0,b0) in out:continue
            out.add((a0,b0));todo.extend([(neg(b0),sub(a0,b0)),(b0,a0),(neg(a0),neg(b0))])
        return out
    fibers=defaultdict(set);invs=defaultdict(set);degree=defaultdict(set);isotropic=0
    for a in range(q):
        for b in range(q):
            X,Y=pts(a,b,P),pts(a,b,Q);collision=len(set(X))<6 or len(set(Y))<6
            assert collision==any(add(scl(u,a),scl(v,b))==0 for u,v in N)
            if collision:continue
            pair=tuple(sorted((rigid(X),rigid(Y))));assert pair[0]!=pair[1]
            s=add(sub(mul(a,a),mul(a,b)),mul(b,b));e=mul(mul(a,b),sub(a,b));e2=mul(e,e);s3=power(s,3)
            fibers[pair].add((a,b));invs[s,e2].add((a,b));degree[pair[0]].add(pair);degree[pair[1]].add(pair);isotropic+=s==0
            mx,my=moments(X),moments(Y);assert mx[0]==my[0]==scl(66,s)
            C3=sub(add(power(mx[1],2),power(my[1],2)),scl(288,s3));C6=sub(add(mx[2],my[2]),scl(47892,s3))
            assert sub(scl(118,C6),scl(13,C3))==scl(162,e2)
            det=(-2**4*3**12*31)%p
            for M in(mx,my):
                H3=sub(power(M[1],2),scl(144,s3));H6=sub(M[2],scl(23946,s3))
                assert scl(pow(det,-1,p),add(scl(-4860,H3),scl(2916,H6)))==e2
    assert all(len(V)==12 and V==orbit(*next(iter(V))) for V in fibers.values())
    assert {frozenset(V) for V in fibers.values()}=={frozenset(V) for V in invs.values()}
    assert len(fibers)==(q-1)*(q-(p if p in(5,7) else 11))//12
    assert max(map(len,degree.values()))==1
    print('PASS quadratic field',q,'pairs',len(fibers),'isotropic',isotropic)
```

```python
# REVIEW-CHECK: finite corollary payloads, without asserting a new census
from pathlib import Path
from itertools import combinations
from math import isqrt
from collections import Counter
import json,hashlib,sys
sys.path.insert(0,'src')
from homometry import icv,dihedral_canon,z_families
for p in(7,11):assert not z_families(p,sizes=[6])
primes=[p for p in range(13,132) if all(p%d for d in range(2,isqrt(p)+1))]
def normalized(F):return {tuple(f['icv']):tuple(sorted(tuple(x) for x in f['members'])) for f in F}
for p in primes:
    candidates=[Path(f'results/2026-09-30-six-census/n{p}.json'),Path(f'results/2026-09-30-six-large-census/n{p}.json')]
    path=next(x for x in candidates if x.exists());raw=path.read_bytes();data=json.loads(raw)
    edges=set();members_seen=set();hist=Counter();keys=set()
    for family in data['families']:
        members=[tuple(x) for x in family['members']];hist[len(members)]+=1
        assert len(members)==len(set(members))>=2
        assert all(len(x)==len(set(x))==6 for x in members)
        assert all(tuple(family['icv'])==icv(x,p) for x in members)
        assert all(x==dihedral_canon(x,p) for x in members)
        assert not(members_seen&set(members));members_seen.update(members)
        key=tuple(family['icv']);assert key not in keys;keys.add(key)
        edges.update(tuple(sorted(x)) for x in combinations(members,2))
    bloom=json.loads(Path(f'results/2026-09-30-six-prime-count/p{p}.json').read_bytes())
    bpairs={tuple(tuple(E) for E in r['pair']) for r in bloom['fibers']};assert bpairs<=edges
    base=(p-1)*(p-11)//12;assert len(bpairs)==base
    ep={17:8,19:9,23:11,31:20}.get(p,0);ef={17:8,19:9,23:11,31:11}.get(p,0)
    assert len(edges)==base+ep and len(data['families'])==base+ef
    assert hist==({2:60,5:1} if p==31 else{2:base+ef})
    for alternate in candidates:
        if alternate.exists():assert normalized(json.loads(alternate.read_text())['families'])==normalized(data['families'])
    print('PASS finite payload',p,'pairs',len(edges),'families',len(data['families']),'SHA256',hashlib.sha256(raw).hexdigest())
```

## 6. Remaining limitations

No external literature priority assertion was reviewed or established here;
novelty remains unestablished. I did not read the cited classical papers
anew, and the mathematical acceptance above does not depend on an unread
classification theorem. A–C are for the explicitly specified Bloom image
under independent rigid motions, not arbitrary finite abelian groups,
general scalar equivalence, every cardinality, composite cyclic counts or
extension fields of characteristic 2,3,11. C also excludes characteristic
31. D–E retain their computer-assisted completeness dependencies. No new
Lean formalization, external mathematician review, public archival,
submission or outreach was performed. A human specialist should examine
the algebraic argument, the inherited completeness obligations and the
historical-priority scope before public sharing.

## 7. Standalone paper comparison

I subsequently read the complete
`notes/2026-09-30-six-prime-paper.tex` source and compared its mathematical
statements and proofs with the accepted A–E source above. **Review verdict:
ACCEPT its mathematical presentation and dependency wording.** The final
accepted paper source has SHA256
`8a2bfba946f9a03c4625060b33c0b18cfed0d1c34f4e1f9846d984cee3ae4d39`.
The first accepted presentation, before a precision-only wording edit in
E's proof and presentation-only theorem-counter/path-wrapping changes,
had SHA256
`69644536e1cc5e391ac0042ee030970c633e187d6bc9018f0f8d9fc2050dda1c`.

The comparison checks the exact original coordinates and all moment
coefficients, cubic sign/permutation reconstruction, twelve free symmetries,
field characteristic scope, independent endpoint rigid motions, scalar
quotient exclusion, isotropic parameters and the exceptions 79,239,31.
The paper's 31 witness includes the raw endpoints, correct transports,
distinct gap multisets and the limitation that this three-class witness
alone does not establish the complete five-class census family.

Its D input correctly retains the line solver and bounded torsion
certificate, and its E assumes the inherited full six-only census through
135, a stronger finite input than the needed prime payloads through 131.
It distinguishes Bloom counts, unordered pair-edge counts and maximal
families. It does not turn the parameter checks at 1009 or the noncyclic
extension fields into full six-subset completeness. I suggested replacing
the unqualified phrase “no six-subsets below 7” with “Primes below 7
support no six-subsets”; the final source incorporates this precision edit.
The author also changed the displayed theorem/corollary counters to A–E
and made file paths breakable; these do not affect content. No substantive mathematical drift
or unsupported theorem status was found.

This comparison did not redo the paper agent's native compilation, PDF
export/render inspection, metadata or bibliographic primary-source audit.
The paper's additional bibliographic prose is outside this mathematical
comparison and must retain the separate literature audit. This acceptance
does not strengthen external review, novelty or publication status.

## 8. Composite boundary witness: separate accepted computational audit

**[COMPUTED], accepted boundary witness.** I read the appended obstruction
in `notes/2026-09-30-six-next.md`, its standalone test and exact certificate,
then ran `.venv/bin/python tests/test_six_prime_boundary.py` successfully.
Independent canonicalization using all 442 translation/sign images per
endpoint reproduces both saved unordered pairs; full directed difference
counters verify homometry within each row and different endpoint classes.
Actual scaled centered moments `(m2,m3²,m6)` reproduce `[195,220,65]`
for X and `[195,26,110]` for Y in both rows. The parameter keys are
both `(13,144)`, but the largest cyclic gaps are `210,210` versus `75,73`;
this excludes every cross-row rigid endpoint identification.

The infinite moment claim follows from algebra, rather than the test's
finite exponent range 2..20: 6 is invertible modulo 221, so multiplying
every point by t multiplies its centered coordinate by t and its jth
moment by t^j. Here t=118 has t²=1 and t is neither global +1 nor -1.
Consequently every even moment and every squared odd moment is preserved.
Locally t is +1 modulo 13 and -1 modulo 17. Explicitly e(v)=209 and
e(w)=131, which are not global negatives or equals, while
`(131-209)(131+209)=0 mod221` with both factors nonzero. The field's
integral-domain sign step therefore genuinely fails; these local signs
cannot be replaced by global T/I inversion.

The two rows are not mutually homometric: their directed distance-1
counts are respectively two and zero. The source correctly claims only
internal homometry of each row and equality of the stated moments, not
cross-row homometry or any composite counting theorem. This does not
change the accepted A–E, root proof, paper or main implementation scope.

Audited hashes:

```
notes/2026-09-30-six-next.md 8c8793590c9f9590160e53c8471efb23a5367179e4ccde7cc5ce77848d28f1dd
tests/test_six_prime_boundary.py b7f4fc8b3a2dc243828c932c1fb3851e3c7afcdad286e84260d33503d8561945
results/2026-09-30-six-prime-invariants/composite-obstruction.json b8e386e8d8f44b86be0e251e4dbdfc5f9c6943753d83c690b1fecdbdda85cb13
```

This additional independent block uses all translations rather than
anchoring only at points. It is also runnable by the extraction command
in Section 5 and was executed after being saved here.

```python
# REVIEW-CHECK: separate composite-domain obstruction
from collections import Counter
from pathlib import Path
import json
n,t=221,118
rows=json.loads(Path('results/2026-09-30-six-prime-invariants/composite-obstruction.json').read_text())['records']
canonical=lambda A:min(tuple(sorted((sign*x+shift)%n for x in A)) for sign in(-1,1) for shift in range(n))
directed=lambda A:Counter((x-y)%n for x in A for y in A)
keys=[];pairs=[];moments=[]
for row in rows:
    a,b=row['parameter'];X=tuple(sorted({0,a,(b-2*a)%n,(2*b-2*a)%n,2*b%n,(3*b-a)%n}));Y=tuple(sorted({0,a,(b+2*a)%n,(2*b-a)%n,(2*b+a)%n,(3*b-a)%n}))
    assert len(X)==len(Y)==6 and list(X)==row['X'] and list(Y)==row['Y']
    assert directed(X)==directed(Y)
    pair=tuple(sorted((canonical(X),canonical(Y))));assert pair[0]!=pair[1] and [list(E) for E in pair]==row['canonical_pair'];pairs.append(pair)
    s=(a*a-a*b+b*b)%n;e=a*b*(a-b)%n;keys.append((s,e*e%n));assert [s,e*e%n]==row['invariants']
    out=[]
    for A in(X,Y):
        mu=sum(A)*pow(6,-1,n)%n;Z=[3*(x-mu)%n for x in A]
        M=[sum(pow(x,j,n) for x in Z)%n for j in(2,3,6)];out.append([M[0],M[1]*M[1]%n,M[2]])
    assert out==row['endpoint_moments'];moments.append(out)
assert keys[0]==keys[1]==(13,144) and pairs[0]!=pairs[1] and moments[0]==moments[1]
assert t*t%n==1 and t%13==1 and t%17==-1%17 and t not in(1,n-1)
assert tuple(t*x%n for x in rows[0]['parameter'])==tuple(rows[1]['parameter'])
assert 131 not in(209,-209%n) and (131-209)*(131+209)%n==0
assert [directed(row['X'])[1] for row in rows]==[2,0]
print('PASS independent composite classes, internal homometry, centered moments and CRT obstruction')
```
