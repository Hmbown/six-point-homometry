# General six-note generation in every cyclic group

30 September 2026. **[PROVED], in-house, computer-assisted**, after the
separate whole-argument attack in `2026-09-30-six-generation-review.md`.
This is a computer-assisted generation
result for cardinality six, with explicit finite certificates. It is not
an irredundant classification or a counting formula. Novelty is withheld;
a second primary-literature search is complete, with explicit access and
priority gaps recorded in `2026-09-30-six-literature-second.md` and its
independent companion. No matching published theorem was located;
absence from these searches is not proof of originality.

## 1. Theorem G: scope and explicit generating grammar

For every positive integer n, form a graph whose vertices are the T/I
classes of six-element subsets of Z_n. Join two different vertices when
representatives are related by one of the constructions below. Each
construction is reversible as an edge. Then **the connected components
are exactly the homometry classes**: two six-note sets have the same
interval multiset if and only if their vertices are connected.

All coordinates below are in Z_n, unless an integer lift is explicitly
specified. Every endpoint must have six distinct points. Independent
translations, global inversions and interchange of endpoints are allowed.
Discard endpoints in the same T/I class when listing Z-relations.
Multiplication by a unit is a move with a stated hypothesis, never an
extra equivalence between vertices.

Write a finite set also for its indicator in Z[Z_n], write x^s for a
translation and F* for reflection of every exponent of F. For a disjoint
partition A=U+W with |U|+|W|=6, put P=UW*. The four block moves are:

| Label | Endpoint B | Parameter condition |
|---|---|---|
| L2 periodic translation | U+x^s W | x^s P=P |
| L3* cosymmetric translation | U+x^s W | x^(-s)P=P* |
| L4 halfturn translation | U+x^s W | 2s=0 and x^s(P+P*)=P+P* |
| L5 block reflection | U+x^c W* | UW*=x^(-c)UW |

Require the new moving block to be disjoint from U. These are identities
of small cross-difference distributions, not unrestricted spectral units.
They provide finite parameter tests for blocks of at most five notes. The
older halved-shift L3 is included in L3*; no halving hypothesis is silently
used in the new version.

The remaining generators are:

**B: classical integer-factor/Bloom construction.** For arbitrary p,q,

    X={0,p,q-2p,2q-2p,2q,3q-p},
    Y={0,p,q+2p,2q-p,2q+p,3q-p}.

Its signed Laurent-factor identity is given in the shadow proof, Section5.
Every admissible modular image has an integer homometric lift. Conversely,
Theorem I proves every integer six-pair belongs to this construction,
including repeated-distance pairs.

**D: parallelogram-dyad grammar.** Choose a,b with four distinct corners
R={0,a,b,a+b}. Let rho(t)=a+b-t. Choose nonnegative integer weights U0,V0,
constant respectively on <a>- and <b>-cosets, with total mass12. Put
K=U0+V0. Require rho(K)=K, K=1 on R, K in {0,1,2} off R, and K in {0,2}
at rho-fixed points off R. On each two-point rho-orbit outside R choose
neither point if K=0, either point if K=1, and both if K=2; at a fixed
point choose it exactly when K=2. These choices make a four-set C. Output

    X=C union {0,a+b},       Y=C union {a,b}.

The finite mass constraint is
12=ord(a) sum_(a-orbits)U0 + ord(b) sum_(b-orbits)V0.
Thus at least one of ord(a),ord(b) is at most12. Theorem D proves this
parameterization is both necessary and sufficient for this exchange
shape. It allows nonunit steps and supplies actual nonnegative periodic
weights, rather than asking for an unrestricted homometry test.

**L7: half-per-coset complementation.** Choose a subgroup H of even order
h in {2,4,6,12}, choose 12/h distinct H-cosets and choose h/2 points of
each. Their union is A. Let S be the union of the selected full cosets and
put B=S minus A. The h=12, n=12 case is classical hexachord complementation.

**L6: autocorrelation-preserving unit.** For gcd(u,n)=1, put B=uA, requiring
r_A(ut)=r_A(t) for all t, where r_A(t)=#{(a,a') in A²:a-a'=t}.
This explicit multiplier condition is indispensable. L6 is needed only
in the bounded finite part of the completeness proof below; an arbitrary
unit does not preserve an interval vector and does not identify T/I classes.

**R: thirteen fixed cyclic templates.** For a row (q,X,Y) in the following
table, choose t with qt=0 and output tX,tY. Require order(t) in the last
column, which is exactly the condition for six distinct, T/I-distinct
outputs. These include torsion images and ordinary subgroup inflations.

| q | X | Y | allowed order(t) |
|---:|---|---|---|
|17|0,1,2,3,8,12|0,1,2,6,7,9|17|
|19|0,1,2,3,6,10|0,1,2,4,5,11|19|
|21|0,1,2,4,7,14|0,1,3,7,8,10|21|
|21|0,1,2,5,6,15|0,1,2,6,7,10|21|
|21|0,1,3,7,10,15|0,1,4,7,14,16|21|
|23|0,1,2,3,7,17|0,1,2,4,17,18|23|
|24|0,1,2,5,7,16|0,1,2,6,9,11|12,24|
|27|0,1,2,3,7,19|0,1,2,3,8,12|27|
|27|0,1,2,6,19,22|0,1,3,17,21,22|27|
|28|0,1,2,4,12,23|0,1,3,5,11,12|14,28|
|30|0,1,2,6,19,22|0,1,3,9,13,14|15,30|
|30|0,1,3,5,12,25|0,1,6,9,11,13|15,30|
|31|0,1,2,5,11,19|0,1,2,6,20,23|31|

Theorem R gives all536 exact universal matching certificates for these
seeds. The table is part of this sufficient generating grammar; neither
its minimality nor independence from the other generators is asserted.

## 2. Soundness and specialization

For each block move, AA*=UU*+WW*+P+P*. Moving W preserves its own
autocorrelation. For a translation the new cross sum is x^(-s)P+x^s P*.
L2 leaves its summands unchanged, L3* exchanges them, and L4 leaves the
sum unchanged. For L5, the new first cross term is x^(-c)UW; its equality
to P and the involuted equality prove the claim. For B, the formal signed
factor identity proves equality in every abelian group. For D,

    XX*-YY*=x^(-a-b)(1-x^a)(1-x^b)[C+x^(a+b)C*+(1+x^a)(1+x^b)],

and the bracket is K=U0+V0, annihilated by the displayed product.
For L7, the half-coset condition gives SA*+AS*=SS*, so
(S-A)(S-A)*=AA*. L6 simply permutes the equal autocorrelation coefficients.
R follows from its exact formal matching identities. Therefore every edge
and every composition preserves homometry.

Universal block identities survive any group homomorphism. Endpoint
injectivity preserves their disjoint fixed/moving partitions. A nonzero
halfturn either stays order2 or becomes zero, the latter giving an equal
endpoint. For D, if images of the two distinct equal-sum dyads share a
point, they share both, so the output is equal; every nontrivial image
retains four distinct corners and the cyclic periodic-weight grammar.
Bloom formulas also specialize directly.

**The L7 projection issue requires a separate lemma.** Let a universal
half-coset pair have six points on each side, and let a homomorphism be
injective on each endpoint. If its kernel on H has size k, then h/2
points in each source coset must fit in h/k positions, so k<=2. For k=2,
both complementary halves fill the same image coset and the endpoints
are equal. Thus a non-T/I image preserves H's order. At most two occupied
source cosets can merge, by the same cardinality argument. A merged pair
produces one full common image coset. When h=2 all other singleton halves
are exchanged by the same order2 translation, which fixes full cosets;
the entire endpoints are translates. When h=4 there are three source
cosets, so a merger leaves one dyad; every dyad in C4 has its complementary
dyad as a translate by an H element, which again fixes the full common
coset. When h=6 a merger leaves equal full cosets; h=12 has only one
source coset. Consequently every non-T/I six-image preserves the occupied
cosets distinctly and is a literal L7 construction. This prevents an
unjustified claim that all coset descriptions automatically transport.

## 3. Universal signed matching: the exhaustive dichotomy

Take any homometric six-subsets A,B in Z_n. Match their fifteen unordered
edges in equal unoriented difference classes, with a sign on each matched
edge. Repeated and antipodal differences are included with multiplicity.
Anchor each endpoint independently. This yields a15-by10 integer matrix M
and the finitely generated group

    G_M=Z^10 / row_Z(M).

Its twelve formal vertices have equal difference multisets by construction.
The input coordinates define a homomorphism G_M -> Z_n. They force six
separate vertices on each side; universal T/I would also imply target T/I.
Hence for a genuine input Z-pair the universal configurations are binary
and non-T/I.

Write d=10-rank_Q(M). Since either five-column block is a reduced K6
incidence matrix, 0<=d<=5. All ranks in what follows refer to this original
presentation, not to a chosen one-dimensional cylinder image.

### 3.1 d=0: bounded finite torsion, then inflation

Theorem C bounds the torsion order of G_M by135. The maximal-rank minor
bound follows from incidence total unimodularity; for rank10 the bound is
the maximum number of spanning trees of a ten-edge K6 subgraph. All3003
labelled subgraphs were independently counted in two ways, with maximum135.
The input map therefore has a cyclic image of order q<=135. Since six
points remain distinct, q>=6. Both independently anchored sets are in this
subgroup and are ordinary inflations from Z_q.

Theorem FT exhausts all these finite q by two independently implemented
six-subset enumerations. Every finite homometry family is connected by
B,D,R,L2,L3,L4,L5,L6,L7, using explicit independently replayed certificates.
All generators lift through the injective subgroup embedding. For L6 a
unit modulo q lifts to a unit modulo n: retain its residue modulo q and
set it to1 modulo each prime dividing n but not q, using CRT. Thus the
whole path lifts. A T/I relation between nonempty subsets of the subgroup
has its translation in that subgroup, so distinct T/I vertices remain
distinct after inflation. This proves the d=0 branch for every n.

### 3.2 d>0 with a noncongruent real projection: Bloom

If a homomorphism G_M -> R sends the two vertex multisets to non-T/I
multisets, Theorem BF shows the pair already has the group-valued Bloom
formula in G_M. Its image in Z_n is B. BF uses the complete weighted
six-atom line theorem Iw; projections are allowed to have repeated points.
Its five exceptional slopes and two generic patterns have282 signed
matchings, reducing to21 integral presentations. Nineteen are Bloom and
two force forbidden collisions. No real-parameter sampling is used.

### 3.3 All real projections congruent: one fixed height graph

There are only finitely many anchored signs, vertex permutations and
translated-anchor choices that can express a real T/I congruence of the
two six-atom lists. Each choice defines a linear subspace of
Hom(G_M,R). By hypothesis their union is the whole space. A real vector
space cannot be a finite union of proper linear subspaces. Thus one fixed
choice holds for every real solution. Relabel, reflect and reanchor B
accordingly; every real solution now has labelled B=A.

Substitute this graph into the matching equations. The resulting rational
relations among six A heights are spanned by differences of signed edges.
After removing content and sign the possible projective directions are
exactly the120 permutations of

    (1,-1,0,0,0,0), (2,-1,-1,0,0,0), (1,1,-1,-1,0,0).

Their span S has rank5-d in the five-dimensional space modulo translation.
Only this rational height arrangement is normalized in this way. All
actual group presentations and quotient relations retain integral row
lattices, including their torsion.

If d>=3, Theorem HR exhausts spans of ranks0,1,2 and every compatible
matching. The only nontrivial outcome is the explicit order2 family

    C={0,p,q,p-q+h}, A=C union {r,r+h},
    B=C union {p-r,p-r+h}, 2h=0.

For the table's precise L5 identity, first reflect the whole second set:
`p-B={r,r+h} union (p-C)`. Now the fixed block is `U={r,r+h}`, the
moving block is `W=C`, and c=p. Writing P0=x^p and H0=x^h, direct expansion
gives `(C-P0 C*)(1+H0)=0`; hence `UW*=P0^(-1)UW`, as required.
Reflecting the dyad while keeping C fixed would preserve the total cross
sum but would not generally meet L5's stronger first-cross-term condition.
The displayed global alignment supplies that condition. Parameters are
arbitrary, subject to six-point distinctness.

If d=1 or2, Theorem LR exhausts the remaining rank4 or rank3 spans:
116,401 or43,770 rational flats, in211 or104 S6 orbits. A certified generic
integer height vector in each flat's orthogonal complement records exactly
its forced signed-edge coincidences. Complete nonzero-edge matching
orbits seed a quotient tree/DAG. At each node cancel already equal
unsigned difference classes; any remaining A class must match some
remaining B class with one of both compatible signs in the original
presentation. Branch on every such equality. The unmatched multiplicity
strictly decreases. Two-way integral row identities certify every cached
normalization. Thus every original presentation factors through a terminal.
This reasoning uses the real heights of G_M, never a nonexistent nonzero
map from the final finite cyclic target to R.

The315 strata have10,602 nodes, with620 homometric terminals. Every one
has a B,D,L2,L3*,L4,L5,L7 certificate, or reduces to such a certificate
or a forced collision under every cyclic torsion character. Precisely nine
terminals require this last step: all60 characters give44 collisions and16
constructions. Every map of a finite abelian torsion group to Z_n factors
through one enumerated character's actual cyclic image; its order divides
n, even when the full torsion exponent does not. Free coordinates remain
arbitrary. Section2 ensures a nontrivial cyclic specialization is still
one of the listed generators.

These branches exhaust d=0,1,2,3,4,5 and both real-projection cases. Together
with soundness they prove G. The separate audits of each finite certificate
package and this assembled proof are complete and accepted. No extension of a numerical
trend to arbitrary n is made.

## 4. What is and is not settled

G gives a complete structural generating grammar for all six-note cyclic
homometry, allowing compositions. It does not assert that every pair is one
direct move, that the list is minimal, or that each family has a unique
normal form. It does not solve the higher-cardinality program or supply a
closed counting formula for six-note families.

Integer shadows are decided exactly by modular Bloom membership (I).
Purely cyclic means outside that complete image; the label of a cyclic
construction alone does not prove this. Faithful R images and the earlier
H families have separate exact non-shadow proofs. A cyclic integral factor
flip is not automatically an integer shadow. The21-EDO benchmark remains
both the rigid R5 example and the previously explained complement-conjugate,
cyclic factor-flip and difference-set exchange example. Inflation and
unit action do not erase T/I class distinctions.

The six-only finite validation range is6..135, with725,132 nontrivial
families and728,424 pair edges at12..135. Of these728,351 have saved direct
certificates; all73 remaining edges have explicit paths. These finite
numbers support FT, whose rank bound is proved. The arbitrary-n theorem
also requires BF, HR and LR; it is not supplied by the census alone.

Trust boundaries remain explicit: exact integer certificate checkers,
C/Python runtime and independently audited exact solver encodings for Iw.
This is an in-house computer-assisted proof, not a Lean-kernel proof or
external peer-reviewed result. A human specialist should review the logical
cover, line-solver encoding and certificate checkers before publication.
No novelty claim follows from the theorem or from unsuccessful searches.

## 5. Proof and reproduction map

All commands use the pinned environment in this checkout.

| Component | Full proof | Separate attack / principal verification |
|---|---|---|
| I/Iw and shadow iff Bloom | six-integer-theorem.md | six-integer-review.md |
| D, H and original shadow bound | six-shadow-theorem.md | six-shadow-review.md |
| C/C2 bounded finite branch | six-completeness.md | six-cylinder-templates-review.md |
| R thirteen rigid templates | six-templates.md | six-cylinder-templates-review.md |
| BF and HR | six-bloom-cylinders.md; six-free-rank.md | six-cylinder-branches-review.md |
| FT finite generating paths | six-finite-torsion.md | six-finite-torsion-review.md |
| LR positive low free rank | six-free-dag.md | six-low-rank-review.md |
| G assembled arbitrary-n statement | this note | six-generation-review.md |

Every filename in this table has prefix `notes/2026-09-30-`.

```bash
.venv/bin/python tests/test_env.py
.venv/bin/python tests/run_tests.py
.venv/bin/python tests/test_six_cylinder_branches_review.py
.venv/bin/python tests/test_six_free_rank_growth.py
.venv/bin/python tests/test_six_free_dag_review.py --resume --require-complete
.venv/bin/python tests/test_six_low_rank_mechanisms_review.py
.venv/bin/python tests/test_six_finite_torsion_review.py
```

Complete regeneration commands and longer line-solver/census replays are
in the component proofs. The root structural audit checks all315 strata,
4,822,240 cross-bijections,328,473 roots,974 branch edges and658,894 integral
lattice-inclusion identities. Its resume files are bound to input SHA256
hashes. The independent terminal checker imports no builder, recognizer,
Smith or Hermite routine. The finite table has two complete traversals,
independent Burnside class counts and direct immutable-reference regressions.
