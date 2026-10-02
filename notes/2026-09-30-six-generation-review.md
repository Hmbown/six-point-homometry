# Separate whole-argument review of six-note generation

30 September 2026. Final synthesis reviewer: the separate integer/cylinder
review agent. Reviewed full manuscript:
`notes/2026-09-30-six-generation.md`.

**Verdict: accepted [PROVED], in-house, computer-assisted**, after the two
specialization/alignment repairs recorded below. Theorem G establishes
generation of every six-note homometry class in every finite cyclic group
by its explicitly stated grammar, with compositions allowed. No unresolved
branch remains in this argument. This is not a novelty conclusion, an
irredundant normal-form classification, a family-counting theorem, a
higher-cardinality result, or external peer review.

This is a review of the assembled argument as well as its individual
identities. I read the complete synthesis only after it was written. I had
previously independently attacked I/Iw, BF, HR and FT; the remaining LR
builder's mathematical proof and integral cover were attacked separately by
the integer reviewer and the root checker. I authored a separate
three-dyad subcase, but Theorem G does not depend on that subcase: the full
LR cover includes it and has its own separate verification. I did not
silently substitute that self-authored result for an independent review.

## 1. What the theorem actually claims

The vertices are T/I classes of six-element subsets, retaining unit-related
classes as distinct vertices. The edges are B, D, R and L2--L7, with L3*
explicitly the direct cosymmetric identity that does not require dividing
the shift by two. An edge is undirected, and homometry families are the
connected components. This is the generating notion fixed by PQ1.

The manuscript does not assert a single direct construction for every
pair. That stronger statement would not follow from the finite part: 73
finite pair edges lack a saved direct certificate. The proof supplies
actual paths for all 73. Conversely, each stated generator preserves the
autocorrelation, and hence every path stays in one homometry family.
Singleton families cause no problem, and for n<6 the vertex set is empty.

The grammar is explicit. D's conditions are nonnegative periodic weights
and a fixed parallelogram exchange, not an unrestricted test for a
homometric partner. L2--L5 test the cross distribution of a selected block.
L6 is an actual autocorrelation-preserving unit operation, with its
necessary hypothesis stated. R is the fixed thirteen-row table with exact
allowed image orders. These are sufficient generators; minimality and
disjointness of their images are not claimed.

## 2. Exhaustive dichotomy of the original matching presentation

For any input Z-pair, equality of autocorrelations supplies a bijection of
the fifteen unordered edges by classes {g,-g}, with signs. For a
non-involution, an unsigned edge contributes once at g and once at -g;
for an involution it contributes twice at the same value. Thus repeated
and antipodal differences have the correct multiplicities. Neither the
existence of a matching nor the later cancellation step loses those cases.

Independently anchoring the two endpoints produces

    G_M = Z^10 / row_Z(M),  d = 10-rank_Q(M).

The actual coordinates are the image of this presentation. If two vertices
already collided in G_M, their images would collide. If the universal
tuples were T/I, every image would be T/I. Therefore a six-distinct target
Z-pair satisfies the binary, noncongruent universal hypotheses required by
the branch theorems. Either five-column block of M is an oriented reduced
K6 incidence matrix, of rank five, so 0<=d<=5.

All of these ranks belong to the original G_M. Replacing d by the rank of
a later one-dimensional cylinder lift would invalidate the proof's branch
selection. The synthesis explicitly avoids that substitution.

If d=0, reviewed C2 gives a finite image subgroup of order at most 135.
The six distinct points force its order to be at least six, and FT covers
all these groups. If d>0, there either exists a real homomorphism giving
noncongruent projected multisets, or every real projection is congruent.
BF handles the first case, already in G_M, with group-valued Bloom
parameters. Its hypothesis allows repeated projected atoms: replacing Iw
by the distinct-point real theorem would leave a real gap.

In the second case, each possible sign, permutation and translated anchor
gives a homogeneous linear T/I condition on Hom(G_M,R). There are finitely
many choices. A real vector space cannot be a finite union of proper
linear subspaces, so one fixed condition holds throughout. Reanchoring,
relabeling and possibly reflecting B are invertible integer coordinate
changes and make this graph B=A. They do not divide a torsion element or
assume it can be lifted to a half-element.

Substitution of this graph into M describes exactly its real kernel, and
the A-coordinate projection is injective there. Consequently the
substituted-row span has rank 5-d, not merely a rank bound. Each nonzero
row direction is a difference of oriented K6 edges. Normalizing only for
this rational-space calculation gives 120 directions, with counts
15 for (1,-1), 60 for (2,-1,-1), and 45 for (1,1,-1,-1), modulo sign and
coordinate permutation. I independently regenerated these from all pairs
of the thirty oriented edges; the exact counts agree.

HR covers d=3,4,5, using all spans of rank at most two. LR covers d=1,2,
using spans of ranks four and three. Thus no possible free dimension and
neither real-projection case is omitted. There is no unproved assumption
that some chosen cyclic pair must possess a favorable matching: any
compatible matching enters this exhaustive split.

## 3. Integral lattices, height restrictions and cyclic characters

Dividing content is legitimate for enumerating the rational height
arrangement only. Replacing the actual relation lattice by its saturation
would erase torsion and lose valid mechanisms. The branch proofs retain
integral rows, and every cached normalization in LR carries two integer
lattice inclusions. Smith coordinates are justified by explicit UMV=D
identities and unimodular matrices, rather than by trusting a returned list
of invariant factors.

The height vectors used in the finite strata are exact certificates of
genericity: each of the 120 directions vanishes exactly when forced by the
span. This records all relevant signed-edge coincidences and repeated
heights. It does not require a numerical separation tolerance, and the
heights are not inserted as additional integral relations.

The LR cancellation argument concerns an original full matching
presentation that factors through a weaker node and still has the chosen
real-height homomorphism. Equal universal classes remain equal in that
presentation. After cancelling equal multiplicities, a chosen residual
A occurrence must equal some residual B occurrence up to sign, and its
real heights must agree. Both signs are included when compatible. The
original presentation therefore factors through a listed child. Adding
the equality strictly decreases residual multiplicity; quotienting cannot
destroy any already cancelled equalities. Universal collisions and T/I
relations are hereditary and safe to discard.

This argument would be false if applied to arbitrary homometric images of
an unrelated weak cross root in Z_n: such an image need not retain a real
height map. The manuscript makes the correct assertion about the original
lift. A terminal may have more free parameters than the original matching;
its universally checked identity still transfers through the factor map.

For the nine exceptional terminal groups, the finite character enumeration
is exhaustive for all cyclic targets. If T has exponent E, every map
T->Z_n has cyclic image C_q with q dividing E and n. Identifying that image
with a subgroup of C_E gives one of the enumerated characters with the
same kernel. The factorization uses its actual image C_q, not all of C_E;
requiring E|n would incorrectly omit targets. Free coordinates are left
arbitrary. All sixty characters have a checked disposition: forty-four
forced collisions and sixteen explicit constructions. There is no
remaining noncyclic torsion case to extrapolate.

## 4. Repairs found at the interfaces

### 4.1 L7 under a possibly noninjective ambient projection

Transporting a group-ring identity proves homometry, but need not by
itself preserve the named combinatorial construction. A material omission
in the early branch prose was that occupied cosets of H can merge even
when each six-point endpoint remains injective. The integer reviewer and I
independently raised this objection. The following lemma is now in LR and
in Section 2 of the synthesis.

Suppose A,B are complementary halves of 12/h occupied cosets of a cyclic
H of order h in {2,4,6,12}. Under a homomorphism injective on each endpoint,
let k be the kernel size on H. A half-coset's h/2 points must fit into a
coset of size h/k, so k<=2. If k=2, both halves fill the same image coset
and the endpoint images are equal. A non-T/I image therefore preserves H.

With H preserved, at most two occupied source cosets can merge, since
their disjoint A-halves must fit into h positions. A merged pair gives a
full common image coset. For h=2, all remaining singleton halves exchange
under the same nonzero H translation, which also fixes every full common
coset; the whole pair is a translate. For h=4, only three source cosets
exist. A merger leaves one complementary dyad; every dyad in C4 translates
to its complement, and that translation fixes the full common coset.
For h=6, a merger exhausts the two cosets and gives equality. For h=12,
there is only one coset. Thus every non-T/I six-image preserves both H's
order and the distinct occupied cosets and remains literal L7.

This is a complete elementary degeneration argument, not merely a
sampled control. The separate LR review additionally checks 150
loss-of-order and 1,448 coset-merger cases. No new mechanism was needed.

### 4.2 The precise HR alignment needed for L5

For the high-rank family, put

    C=1+P+Q+P Q^(-1) H,  W=R(1+H),  H^2=1.

The displayed endpoints are A=C+W and B=C+P W*. Their autocorrelations
agree because (C-P C*)(1+H)=0. However, keeping C fixed and reflecting W
does not generally satisfy the synthesis table's stronger L5 condition
`C W*=P^(-1) C W`: one side contains R^(-1), the other R. A bare assertion
that this displayed dyad motion is exactly that L5 certificate would be
insufficient.

Reflect the entire second endpoint first: B'=P B*=W+P C*. Now the fixed
block is U=W, the moving block is C, and the reflection parameter is p.
Multiplying (C-P C*)(1+H)=0 by R gives

    U C* = P^(-1) U C,

which is precisely L5. Independent global reflection is explicitly
allowed on endpoints. I requested this alignment be written out and
verified that it is now present in Section 3.3 of the synthesis.

An independent Counter expansion in Z^3 direct-sum C2 confirms the full
autocorrelation identity, rejects the unaligned stronger condition, and
confirms the aligned L5 condition. The controls, together with the
independent 120-direction count, are saved in
`results/2026-09-30-six-generation-review-controls.json`.

### 4.3 The other specializations

Endpoint injectivity preserves each block's within-endpoint partition.
The L2, L3*, L4 and L5 identities therefore descend directly. If an L4
shift becomes zero the endpoints coincide, which is discarded. Bloom
coordinates descend as integer-linear formulas.

For D, the common four-set remains distinct and disjoint from every corner
that appears on either side. If the two equal-sum dyads acquire a common
point, they coincide completely, giving equal endpoints. Any nontrivial
image retains four distinct corners, and reviewed D1 in the cyclic target
supplies the required nonnegative periodic weights. This establishes actual
membership in D's parameter grammar, beyond an endpoint homometry check.

L3* must retain its asterisk or its explicit generalized description:
`x^(-s)P=P*` is sound without a solution of 2t=-s. The synthesis does not
replace it silently by the older, more restrictive halved-shift L3.

## 5. The finite branch really lifts generating paths

For d=0, C2 bounds the universal finite order and hence the actual cyclic
image order q by 135. No primitivity of the displayed sets is assumed.
Independently anchoring both endpoints places them in the same image
subgroup. FT covers all q=6..135, including nonprimitive pairs there.

The embedding i:Z_q->Z_n, i(x)=(n/q)x, is injective on the whole finite
group, not just the endpoint sets. It preserves all group-ring identities,
subgroup cosets, complements, disjointness and periodic weight functions,
so all finite paths lift edge by edge without the L7 degeneration problem.

For a finite L6 unit u, impose u'=u modulo q and u'=1 modulo each prime
dividing n but not q. CRT applies; primes already dividing q do not divide
u', and all other primes dividing n are excluded by construction. Therefore
u' is an ambient unit and acts on the subgroup exactly as u. It preserves
the inflated autocorrelation, including its zero coefficients outside the
subgroup. No prime-power lifting condition is missing.

Finally, if nonempty subsets of the subgroup are ambiently T/I equivalent,
their translation belongs to the subgroup: compare any matched pair of
points. Thus distinct finite T/I vertices remain distinct after inflation.
Separate initial anchors add only allowed rigid motions. This proves
composition, not merely preservation of isolated edges.

The independent finite attack verifies census completeness and exact
packing, the generator semantics, all completed replay totals, independent
Burnside counts at all 130 moduli, and actual paths for the 73 absent direct
edges. This final review does not repeat that expensive replay or treat the
finite cutoff by itself as an arbitrary-n proof.

## 6. Finite evidence and dependency gate

The previously reviewed components and the newly complete LR package have
the following exact coverage boundaries:

| Component | Checked finite cover relevant to G |
|---|---|
| I/Iw | Independent strict and weighted real SMT encodings, exact UNSAT proof checking, separate finite controls |
| BF | 282 signed real-compatible matchings, 21 integral presentations, 19 Bloom and two forced-collision cases |
| HR | 120 directions, 4,176 rank-at-most-two spans, 25 orbits, all 14,475 signed matchings, four explicit survivors |
| C2 | All 3,003 ten-edge K6 subgraphs; maximum spanning-tree bound 135 |
| R | All 536 matching certificates and exact allowed image orders for the thirteen displayed seeds |
| FT | 725,132 families and 728,424 pair edges through 135; 728,351 direct certificates; 73 path closures; zero disconnected families |
| LR cover | 315 strata, 4,822,240 cross bijections, 328,473 roots, 10,602 nodes, 974 branch edges, 658,894 integral inclusion identities |
| LR terminal atlas | All 620 homometric terminals; nine require all 60 finite characters, giving 44 collisions and 16 constructions |

The LR structural report is
`results/2026-09-30-six-free-dag-review/summary.json`; it records completion
at all 315 expected strata. The independent mechanism report is
`results/2026-09-30-six-low-rank-review/verification.json`. It checks both
the builder's atlas and the independently discovered alternative atlas,
with their hashes, using exact group arithmetic without importing the
builder, recognizer, Smith or Hermite code. Different priorities give
different mechanism counts but the same complete cover; those distributions
are not asserted canonical.

The final separate LR mathematical review is
`notes/2026-09-30-six-low-rank-review.md`. It now accepts LR after the full
structural check and L7 repair. FT and its arbitrary-n rank-ten consequence
were separately accepted in
`notes/2026-09-30-six-finite-torsion-review.md`. The remaining component proof
and attack references are accurately listed in the synthesis's proof map.
No pending mathematical subcase or truncated computational artifact is
being used as a complete cover.

For the critical Iw dependency, I reread the independent review and
refreshed the hashes of both gap/bijection SMT inputs and both decompressed
proofs against their accepted metadata. Both match. Their saved cvc5 1.4.1
results are UNSAT with eager internal proof checking; the proof sizes are
10,881,375 and 24,459,075 bytes. These encodings use occurrence bijections
in consecutive gaps, independently of the builder's edge-value counts.
The refresh is recorded in the synthesis control report. I did not rerun
the solver or claim an independent external proof-kernel check at this
stage. The independent-encoding and solver-trust wording of the synthesis
is accurate with that qualification.

## 7. Final decision and trust boundary

The initial interface objections were resolved by written arguments and
checked algebra: literal L7 survives every nontrivial six-point projection,
and HR satisfies the exact named L5 condition after a specified allowed
alignment. The original-presentation rank split, weighted projection
dichotomy, integral quotient cover, cyclic character factorization and
finite-path inflation now join without a gap found in this attack.

Theorem G may therefore be marked **[PROVED], computer-assisted** under the
program's in-house definition. This relies on the written arguments,
audited exact C/Python computations, finite integer certificates, and the
independently encoded exact solver results for Iw. I did not rerun every
component computation during this synthesis review. There is no complete
Lean or standalone-small-kernel formalization, and this acceptance is not
external peer review. A human specialist should inspect the logical cover,
the line-solver encodings and the finite verifiers before publication.

The theorem settles six-note PQ1 generation with compositions. It does not
settle the entire research program, unique normal forms, minimal generators,
or counting formulas. A separate executable recognition driver, if added,
requires its own tests and is not a dependency of this proof. Historical
priority and novelty remain entirely separate questions.
