# Fresh attack of the all-modulus classical Bloom image

> Mathematics-only export. Nonmathematical media passages were omitted;
> mathematical arguments and acceptance boundaries are retained. Copy provenance
> and upstream/export hashes are in `docs/EXPORT_MANIFEST.json`.

Started and completed 1 October 2026. **Accepted separate fresh attack**
of the all-modulus support formula and pair-fibre theorem AP, for their
written classical-family scopes. Finite replay results are **[COMPUTED]**.
This is a separate adversarial review, limited to the classical six-point
parametrization; it does not review a new all-cardinality theorem or claim
historical priority.

## Review plan

1. Reconstruct all raw labelled-point collision kernels from the literal
   endpoint formulas, retaining nonunit scales at even moduli.
2. Independently enumerate paired matchings using the first two raw Y
   differences as a unit pivot, and single-endpoint systems by original
   integer-matrix minors without elimination.
3. Attack the written arbitrary-n inference, including translation,
   point bijections, Smith factors, CRT gluing, freeness and shared partners.
4. Log explicit failures or the exact accepted scope and frozen digests.
   The finite tables should take seconds; no subset census is planned.

## Startup and independent observations

The pinned-environment startup command `.venv/bin/python tests/run_tests.py`
passed all ten groups. The reference implementation, test runner and data
were not edited. The old centered proof uses division by 12, and its
coprime-to-6 hypothesis is essential to that elimination; it cannot be
extended by merely reducing the same residual table at 2 or 3.

The independent literal raw rows are

\[
 P_X=((0,0),(1,0),(-2,1),(-2,2),(0,2),(-1,3)),
 \quad P_Y=((0,0),(1,0),(2,1),(-1,2),(1,2),(-1,3)).
\]

Subtracting every pair of rows gives the same collision catalogue at
both endpoints. The directions `(1,0)`, `(0,1)` and `(1,-1)` occur at
scales 1 and 2, and the other nine primitive directions occur only at
scale 1. Their unions therefore give the exact twelve excluded kernels

\[
 2a=0,\;2b=0,\;2(a-b)=0,\quad
 a+b=0,\;2a\pm b=0,\;3a-b=0,\;a\pm2b=0,
 \;3a-2b=0,\;a-3b=0,\;2a-3b=0.
\]

This is an all-modulus condition. Replacing the first three equations by
their primitive forms would admit colliding six-point lists when n is
even. No factor 3 occurs among the raw difference scales.

Removing a translation from a matching by subtracting its index-0
equation is valid over every ring. The first two remaining raw X rows
form `[[1,0],[-2,1]]`; the raw Y rows form `[[1,0],[2,1]]`.
Both determinants equal 1. Thus an exact denominator-free elimination
is available; it is not a formal reuse of the centered table.

## Independent finite reconstruction

The independently written evidence script is
`src/six_bloom_primary_review.py`.
It imports only `src/homometry.py` for literal finite T/I and ICV controls;
it does not import either author's new support or matching functions.
It uses the pinned Python 3.12.12 / NumPy 2.5.3 environment, whose five
temporary-elision guards passed before the full calculation.

The complete paired replay used **the first two Y differences** as its
unit pivot, while the author's calculation uses X. It enumerated all
4,147,200 cases, including both endpoint assignments, both independent
signs and every pair of label permutations. Its exact partition is
12 rank-zero, 864 rank-one and 4,146,324 rank-two systems. Every one of
the 15 rank-one `(direction,content)` and 17 rank-two `(content,D)`
histogram entries agrees with the author's full certificate. All twelve
zero matrices are exactly G, each once; the endpoint swap agrees with
its T exponent. My pivot's largest absolute residual entry/minor is
24/110, safely within exact signed int64 arithmetic.

The independent single-endpoint check used the original translated
**5×4 matrices without elimination**. All 3×3 and 4×4 minors were
calculated by signed permutation expansion, with exact integer gcds.
Every original system contains a unit 2×2 minor. Its rank partition
is 24/432/5304 for ranks 2/3/4; its complete third/fourth-minor-gcd
histogram agrees with the author's residual table. This is an additional
control of the elimination, including its nonunit torsion information;
it is not an acceptance of a new endpoint-graph classification.

The whole independent audit took 2.831 seconds. Its saved exact output is
`results/2026-10-01-six-primary-review/independent-audit.json`.
An initial audit import used nonexistent reference function names;
replacing those names by the actual `dihedral_canon` and `icv` aliases
resolved that programming error before any audit calculation ran.
No mathematical counterexample or numeric failure was suppressed.

## Attack of the all-modulus support proof

Freshly read `notes/2026-10-01-six-bloom-support.md`,
`src/six_bloom_support.py` and `tests/test_six_bloom_support.py`.
The raw collision catalogue above agrees with the displayed twelve
kernels. Every two distinct raw normals have a nonzero determinant,
and the maximum absolute determinant is 8. If a vector is in both
kernels, the integer adjugate identity annihilates it by that determinant.
Its additive order therefore divides an integer from 1 through 8.
For a nonzero vector in multiple kernels, the only possible orders are
2 through 8. This step retains orders 6 and 8 and makes no prime-only
or primitive-direction simplification.

For m dividing n, the map `u → (n/m)u` identifies Z/m injectively with
the subgroup of Z/n killed by m. In two coordinates its exact-order-m
vectors are precisely `gcd(a,b,m)=1`. A raw linear equation holds before
embedding iff it holds after embedding. Consequently the membership
number r of any such vector is independent of the ambient n, with no
local collision-direction gluing assumption.

The independently rebuilt complete exact-order membership histograms
are:

|m|r: number of vectors|Overcount|
|---:|---|---:|
|2|6:3|15|
|3|3:8|16|
|4|1:6, 4:6|18|
|5|1:12, 3:12|24|
|6|1:12, 2:12|12|
|7|1:36, 3:12|24|
|8|1:36, 2:12|12|

The three doubled kernel sizes are `n gcd(n,2)`; the other nine have
size n by Bézout. The origin's overcount is 11. Subtracting all the
displayed `r−1` overcounts from the sum of kernel sizes yields precisely
the claimed support formula for all n, including n below six.
Literal point construction independently agrees at every n from 1
through 100. The author's distinct 4096-subset Smith inclusion–exclusion
method and its 840-residue regression are retained as separate evidence.
All five support regression groups passed in this review's own invocation.

**Decision:** the support proof and formula are accepted for every
positive modulus. It counts parameter supports, including congruent
endpoints; it does not alone count Z-pairs.

## Attack of pair-fibre theorem AP

Freshly read `notes/2026-10-01-six-bloom-primary.md`,
`src/six_bloom_primary.py` and `tests/test_six_bloom_primary.py`.
The label-zero subtraction removes the two translations independently.
The unit pivots prove an equivalence of the original equations and
`w=Mv, Hv=0` over every Z/n. An actual equality of six-point sets supplies
global point bijections, even if a CRT projection has repeated points.
No locally unique matching, parity or CRT gluing is assumed.

The rank-one rows are multiples of one primitive normal ℓ. Their
entry gcd c gives the exact equation `c ℓ(v)=0` by Bézout; c is 1 or
2. Content 2 occurs only on a, b and a−b, whose **actual** forbidden
collision equations are doubled. Thus every rank-one paired system
is impossible on Ω_n, without cancelling 2 modulo even n.

For rank two, the gcd-of-minors adjugate argument gives `Dv=0`, and
the integer relation `w=Mv` puts both parameters in the same subgroup
`K_gcd(n,D)`. The finite D list is complete by the independent replay.
There is no hidden possibility of a higher 2/3 power or a mixed CRT
combination: all relevant d divide one of
`1,2,3,4,5,6,7,8,9,12,13,16,19`.

Subgroup embedding preserves actual support. Any rigid transport
between supported sets has its translation in that subgroup, since a
matched target point minus its signed source is in it. Hence rigid
equivalence descends, and inflation introduces no new rigid equivalence.
My independently constructed raw finite images at **all divisors** of
the D list, canonicalized by the immutable reference, give:

|d|Admissible parameters|Congruent parameters|Nontrivial edges|Fibre sizes|
|---:|---:|---:|---:|---|
|1,2,3,4,5,6,7,8,9|0|0|0|—|
|12|36|12|1|12 congruent; 24 nontrivial|
|13|24|0|2|12|
|16|72|0|6|12|
|19|144|0|12|12|

The literal n12 anomalous parameters/classes are retained in my output.
They contain `(1,5)` on the sole congruent fibre and `(1,4),(3,7)` on
the sole merged fibre, with exactly the classes stated in AP. All have
exact additive order 12. Consequently their inflations exist exactly
when 12 divides n. No partner can lie outside K_12: formal G partners
stay there, and a rank-two system containing an order-12 parameter
requires 12 to divide D; the displayed D list then forces D=12.

The full rank-zero systems give actual integer affine point identities
for all G elements. Thus they preserve Ω and Φ at every modulus.
I separately checked that their endpoint assignments equal the stated
T exponents. The freeness argument is valid without any cancellation:
the six reflection equations force respectively a=b, a=0, b=0,
a=−b, a=2b or b=2a, each forbidden by a raw support condition.
The nonidentity positive rotations force coordinates into a subgroup
of order at most three. The two negative rotations have unimodular
fixed-vector matrices, and negation forces `2a=2b=0`.
None can fix a six-point parameter.

Endpoint congruence and its inverse indeed form a swapped matching with
`w=v`. The formal swapped cases are precisely the six reflections,
which cannot fix a parameter in Ω. The other ranks have already been
excluded or reduced to the complete finite table. This proves that
the sole congruent orbit is `G(h,5h)` at `h=n/12`.

Since the complete symbolic difference-coefficient multisets agree
up to signs, homometry holds over every ring; cyclic distance reduction
preserves that identity when both lists are actual sets. The author's
new identity/transport/certificate/finite-control/primary-control tests
passed all five groups in this review's own invocation. The gap-word
class key need not equal the smallest point representative, but its
class partition is the correct invariant; the tests compare every
finite fibre and G-orbit partition against the full reference.

**Decision:** AP is accepted as an in-house computer-assisted proof,
including the free size-12 orbits, the single congruent orbit, the single
24-parameter nontrivial fibre when 12 divides n, and the edge count
`B(n)=|Ω_n|/12−2[12|n]`. No mathematical gap or counterexample was found.
The ordinary subgroup inflation and exact finite table, rather than
a bounded large-n census, justify the arbitrary-n conclusion.

## Separate attack of the infinite even shared-endpoint family

The author's later §5 addition is explicitly separate from AP. I
independently expanded the four raw lists for `n=2m`,
`v=(m+3,1)`, `w=(-3,m−2)`. They agree exactly with the displayed
residue sets. At m≥9 every listed value is in range and the four
supports are distinct internally. The matching permutation from X_w
to Y_v is `(1,5,2,4,3,0)`, with translation `−(m+3)`.
Reconstructing its raw unit-pivot elimination gives exactly the stated
matrix M and residual rows `(-2,6),(-4,12),(-6,18)`.
Thus the identity uses the actual surviving half-period condition
`2(a−3b)=0`, without claiming `a−3b=0`.

Parameter v has full order n because b=1. A common divisor of the
coordinates of w and n must divide 3; if it were 3 then it would divide
both m and m−2, impossible. Parameter w also has full order n.
Since n≥18, neither parameter is in any of AP's three order-12
exceptional orbits. The only possible first coordinates in Gv are
`±1, ±(m+3), ±(m+2)`, none equal to −3 modulo 2m when m≥9.
Therefore AP implies distinct nontrivial pair edges sharing an endpoint,
and hence at least three distinct Bloom vertices in one component.

**Decision:** the displayed all-even `n≥18` family is accepted, dependent
on AP for its two-edge distinction. This is a constructive lower bound,
not an all-modulus endpoint-graph classification. My literal raw-point
and immutable-reference replay independently checked all 120 even
moduli from 18 through 256, retaining the four supports, shared classes
and interval vectors in the review output. All six primary regression
groups, including the new family test, passed on a fresh invocation.

At the parent's instruction, the review auditor was moved into
`src/six_bloom_primary_review.py` to follow the project layout. Its ROOT
and default output paths were updated, the even-family control was
added, and the whole independent universal replay was rerun. Every
paired and endpoint invariant histogram still agrees; the final full
run including the new controls took 2.793 seconds. Only the explicitly
assigned new auditor, review note and review result files were edited.

## Commands, evidence and frozen boundary

```bash
.venv/bin/python tests/run_tests.py
.venv/bin/python tests/test_env.py
.venv/bin/python src/six_bloom_primary_review.py --benchmark
.venv/bin/python src/six_bloom_primary_review.py
.venv/bin/python tests/test_six_bloom_support.py
.venv/bin/python tests/test_six_bloom_primary.py
```

The independent script writes only its own review output. A subsequent
read-only comparison checked every saved paired histogram against the
author's table and checked the original endpoint-minor table against
every saved endpoint histogram. All agreed. Reviewed source, tests,
proof drafts, finite certificates, immutable reference and independent
script/output digests are frozen in
`results/2026-10-01-six-primary-review/reviewed-digests.json`.

The accepted support draft SHA256 is
`28d3f3a034a4ca09149c4a817a9eb0defa322e26894b4d9a271fb42da2aa55aa`;
the accepted AP draft SHA256 is
`2f2f30c5f393d8f605061758b4a7e69a75159486c63322091c6eff67da9aa1a9`.
These are pre-status-promotion digests. Later mathematical edits require
a fresh review; explicit status promotion does not change the accepted
scope. No other agent's source, test, certificate or note was modified;
no staging or commit was performed by this reviewer.

## Honest limitations and human review

These proofs classify and count the classical Bloom image. They do not
give a minimal normal form or disjoint counts for every cyclic mechanism,
settle the all-modulus shared-endpoint graph, or determine every full
homometry family's size. The single-endpoint table has surviving even
rank-one phenomena and is explicitly outside AP's conclusion. The
general generating grammar retains its separate earlier dependencies.
No claim about other cardinalities, priority, novelty, peer review or
external human validation is made. A human specialist should inspect
the completeness of the labelled matching encoding, exact finite tables
and subgroup descent before public sharing.

## Final status promotion and regression freeze

Freshly read the final proof notes after the parent promoted their status
and linked this attack. The AP note now has SHA256
`5b1756eebfda020fe7952dabf0380b29e2b485c29c7746675df1cfb06f8cd7ba`;
the support note has SHA256
`b9c173920d4aad0c7d0599a464feeac0d2eab7666dc3676059a3c2a0534f2da0`.
Reversing precisely the introductory status text, AP theorem label and
attack-footer text recovers both accepted pre-promotion SHA256 digests
byte for byte. The attempted draft copies were made during promotion,
so their exact pre-promotion text was restored by this verified reversal.
The restored copies are retained as `accepted-six-bloom-{support,primary}-draft.md`
inside this review's result directory. No mathematical body changed.

Read and independently invoked the parent's new
`tests/test_six_bloom_primary_review.py`; all five groups passed. It
compares the independent raw nonunit catalogue, finite image partitions,
all universal saved histogram entries, a 518,400-case opposite-pivot
slice, and the 120 even shared-endpoint controls. Its saved parent log is
`results/2026-10-01-six-primary-review/regression-tests.log`.
All previously reviewed mathematical source/test/certificate/independent-evidence
digests remain unchanged. Final mathematical note hashes, regression/log and
restored draft copies are recorded in
`results/2026-10-01-six-primary-review/final-review-digests.json`.
The inherited digest receipt also names a media snapshot outside this extraction;
that separate content/export review is omitted here.
