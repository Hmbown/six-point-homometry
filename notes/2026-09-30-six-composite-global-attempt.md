# Full composite Bloom image: weighted local lists and a small gluing table

Started30 September2026; completed1 October2026. **[PROVED], in-house, with exact finite lift/permutation certificates;
accepted by the separate fresh review in
`notes/2026-09-30-six-composite-global-review.md`.** This is a bounded attempt at the remaining global-support
gap. The previously accepted partial checkpoint is not edited. This note
uses its exact40-pattern paired and24-pattern endpoint lift certificates,
then checks the previously discarded collision branches and constructs
an independent small gluing certificate. No novelty claim is made.

Plan: extend local separation from sets to six-labelled multisets;
classify possible label permutations when a CRT projection has repeated
entries; prove that one fixed global matching forces a common G-element.
Success is a written arbitrary-modulus theorem with an auditable finite
coefficient table, not sampled agreement. The coefficient table is small
(219 paired patterns and57 patterns per endpoint); expected compute is
under one second. The actual certificate completes in that range.

## 1. Proposed theorem and precise scope

Let n be a positive integer whose prime divisors are all at least13.
For v=(a,b) in(Z/n)² use the classical ordered lists

\[
 X_v=(0,a,b-2a,2b-2a,2b,3b-a),\qquad
 Y_v=(0,a,b+2a,2b-a,2b+a,3b-a).
\]

Let Ω_n consist of parameters for which these lists are six-element
sets modulo n. Their reductions in a CRT factor may have repeated
entries. A pair means an unordered pair of independent translation/
inversion classes. General units are not quotiented out. Define

\[
 R=\begin{pmatrix}0&-1\\1&-1\end{pmatrix},\quad
 T=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
 G=\{\lambda R^iT^j:\lambda=\pm1,\ i=0,1,2,\ j=0,1\}.
\]

**Theorem GLOBAL [PROVED].** Every v∈Ω_n gives a homometric pair
of different rigid classes. Every fiber of the unordered pair map is
exactly one free G-orbit. Hence the full Bloom image has

\[
 B(n)=\frac{(n-1)(n-11)}{12}
\]

unordered pair edges. If31 does not divide n, every Bloom endpoint has a
unique Bloom partner, and the number of nontrivial Bloom families also
equals B(n); each has size two. If31 divides n, unique partner fails by
inflating the accepted characteristic31 example. Pair classification and
the pair-edge count have no31 exception.

This theorem concerns the Bloom image. It neither counts all six-point
homometric pairs nor removes purely cyclic constructions or overlaps
with the complete generation grammar. The n221 mixed-sign moment example
is retained: equal(s,e²) remains insufficient globally. Actual point
permutations supply the missing compatibility.

## 2. Weighted local separation, including actual collisions

A weighted list is the six labelled entries with their multiplicities.
Rigid equivalence means equality after one sign and shift as multisets;
equivalently, some label permutation matches the six entries. Centering
is valid because6 is a unit in every ring here. Its two coefficient
matrices are

\[
 C_X=((2,-4),(5,-4),(-4,-1),(-4,2),(2,2),(-1,5)),
\]
\[
 C_Y=((-1,-4),(2,-4),(5,-1),(-4,2),(2,2),(-4,5)).
\]

For any list the centered coordinates are3(x−μ). Let
s=a²−ab+b²,e=ab(a−b),d=(a+b)(2a−b)(a−2b). All moment identities from
the accepted prime and local notes are integer polynomial identities,
so remain valid for weighted lists:

\[
 m_2(X)=m_2(Y)=66s,\quad m_3(X)=6d-243e,\quad m_3(Y)=6d+243e,
\]
\[
 118C_6-13C_3=162e^2,\qquad d^2+27e^2=4s^3.
\]

Here C_3,C_6 are the pair-moment combinations defined in the accepted
field/local notes. These recover s,e² from any weighted pair equality.
Over F_p the cubic(z−a)(z+b)(z−b+a)=z³−sz−e therefore gives w∈Gv
for **every** parameter, including e=0,d=0 and v=0. Equality of cubic
root multisets over a field does not need distinct roots.

Over Z/p^k, divide both parameters by p whenever v≡0 modulo p. Field
alignment forces w≡0 too; the matching translations are divisible by p
because zero is a label and every target label is divisible by p. This
reduces to a smaller modulus, preserving the weighted-list equality.
For primitive parameters, if e,d are units the unit-separated cubic
proof from the local note applies without a support-size assumption.
Otherwise one normalizes to E:b≡0 or D:b≡2a, with a a unit, and aligns
w≡v modulo p as in the accepted local proof.

The accepted paired lift table retains all32 E and8 D patterns. In E its
nonzero residual gcd forces b=0 exactly; in D it forces b=2a exactly.
Those cases were previously excluded because the local supports had to
be six-element. For the weighted extension, inspect the elimination
matrix M in12w=Mv. Every E table entry satisfies
M(1,0)=12(1,0), and every D entry satisfies M(1,2)=12(1,2). Thus the
collision branches instead give **w=v exactly**. The zero-residual
branches give I or±R²T as before. All branches lie in G, proving:

**Weighted local lemma WL [PROVED].** In Z/p^k, p≥13, two unordered rigid
pairs of six-labelled Bloom lists are equal exactly when their parameters
are in the same G-orbit. No distinct-support assumption is needed.

The24 one-endpoint lift patterns have the identical matrix-on-base
property. Therefore, if p≠31, the accepted invertible single-endpoint
moment matrix and the same induction show that sharing **one weighted
endpoint** already puts the local parameters in the same G-orbit.
These conclusions do not assert freeness on weighted collision strata.

The new certificate explicitly checks all64 inherited M-on-base
identities. Its source hashes bind those inherited coefficient tables.

## 3. Weighted symmetries and complete local collision partitions

A nonzero translation cannot stabilize a weighted six-label list over
Z/p^k: each point orbit has order at least p≥13, and invariant positive
multiplicities would give total mass at least13. Thus a fixed sign has
one transport shift, and the only ambiguity in its point permutation
comes from equal labels or a reflection.

Divide any nonzero parameter by its maximal common p-power. This changes
the effective ring but preserves label equalities and rigid symmetry.
For a primitive parameter at most one of the twelve primitive collision
forms can vanish modulo p, since all determinants between different
forms are units. Consequently an **actual** collision in the effective
ring lies on exactly one of the following twelve rational directions:

\[
 (0,1),(1,0),(1,1),(1,-1),(1,2),(1,-2),
 (1,3),(2,1),(2,-1),(2,3),(3,1),(3,2).
\]

The first three directions are the e=0 lines. Each endpoint then has
two equal pairs and its positive label automorphism group has order4.
On each other line each endpoint has one equal pair, giving a positive
automorphism group of order2. There are no further actual coincidences:
a second collision form would have unit determinant with the first and
force the primitive parameter to be zero. Thus these label partitions
are exactly the rational coefficient partitions, for every p^k here.
If no actual collision occurs, the positive label group is the identity.

Two weighted endpoints can be simultaneously reflection-symmetric only
for the zero parameter. Indeed divide to a primitive parameter; both
reflections would give m_3(X)=m_3(Y)=0, hence e=d=0 modulo p. The six
e/d lines have pairwise unit determinants and this forces the primitive
parameter to vanish modulo p, a contradiction.

For later parity and one-endpoint gluing, the full weighted reflection
catalog is needed. If the primitive reduction lies on e=0 or d=0, its
two third moments reduce respectively to12a³ or±486a³ after normalization,
so neither endpoint reflects. Otherwise e,d are units. A direct integer
expansion gives

\[
 m_5(X)=15s(38d-567e),\qquad m_5(Y)=15s(38d+567e).
\]

If X reflects, m_3(X)=m_5(X)=0. Then d=81e/2 and m_5(X)=14580se;
the constants and e are units, so s=0. Substitution into
d²+27e²=4s³ gives6669e²/4=0, with6669=3³·13·19. A primitive reflection
therefore occurs only in an effective ring F13 or F19, never at an
effective prime power of exponent≥2. The Y calculation is identical
with the signs reversed. Their isotropic slopes are4,10 at13 and8,12
at19, all outside the twelve collision lines. Thus every reflected
weighted endpoint has six distinct entries and is an inflation of the
previously audited F13/F19 reflection.

The corresponding label involutions are

\[
 \chi_{X,13}=(2,4,0,5,1,3),\quad
 \chi_{X,19}=(1,0,3,2,5,4),
\]
\[
 \chi_{Y,13}=(3,2,1,0,5,4),\quad
 \chi_{Y,19}=(1,0,4,5,2,3).
\]

They each have three transpositions and odd parity. In particular **an
actually colliding nonzero weighted endpoint never reflects**.

Weighted X,Y classes can coincide only on the e/d actual-collision
directions (or at zero). This follows either from the paired swapped
lift table with w=v, or from the accepted actual-support theorem together
with the unit m_3-square difference on the remaining collision lines.
On normalized E:b=0, S=R²T fixes v and interchanges endpoints; on
normalized D:b=2a, S=−R²T does so. Conjugation handles the other e/d
directions. Hence whenever the two local endpoint classes coincide, a
stabilizer permits one to choose the local G-representative with either
endpoint assignment. This will make its assignment agree with the
chosen global matching.

## 4. The small exact permutation table

The formal centered rotation permutations are

\[
 \rho_X=(3,2,5,4,0,1),\qquad
 \rho_Y=(5,3,0,4,1,2).
\]

They are even products of two3-cycles. T's fixed endpoint-exchange
permutations are even5-cycles. Normalize a global endpoint assignment
to be nonswapped by applying T to w if necessary. For a local
G-element λR^i, a **positive** actual matching differs from the formal
permutation only by a positive automorphism of the target weighted list.

For each of the twelve directions L, let H_X(L),H_Y(L) be its exact
positive label groups from §3. Collect all paired permutations

\[
 (h_X\circ\rho_X^i,\ h_Y\circ\rho_Y^i),\quad
 i=0,1,2,\ h_X\in H_X(L),\ h_Y\in H_Y(L).
\]

Composition here means target-index composition, matching the explicit
row convention in the certificate. The complete table has:

| Table | Distinct patterns | Witness multiplicity | Rotation ambiguity |
|---|---:|---|---:|
| paired endpoints |219|216 patterns have one(i,L); three have12 witnesses|0|
| X alone |57|54 have one(i,L); three have12 witnesses|0|
| Y alone |57|54 have one(i,L); three have12 witnesses|0|

The three patterns with twelve witnesses are exactly the formal rotation
permutations, one per i, occurring on every line with identity label
automorphisms. Thus the noncollision case is already included. Every
pattern determines **one rotation index i**, even if its collision line
is unknown. This is the critical finite gluing lemma. All permutations,
all witnesses and all line groups are retained; it is not a count-only
check or a finite-modulus experiment.

For one-endpoint gluing the negative/reflected patterns are
χ_(X,13)∘ρ_X^i andχ_(X,19)∘ρ_X^i (and the analogous Y patterns).
Each triple has three distinct members. The two triples are disjoint,
and all six members are disjoint from the57 positive patterns, separately
for X and Y. The certificate compares their full arrays, not parity
alone; repeated-label permutations can have odd parity.

## 5. Global pair gluing

Suppose v,w∈Ω_n give the same unordered pair. Choose its global endpoint
assignment, signs ε_X,ε_Y and label permutations π_X,π_Y. They exist
because the global supports are six-element. Apply T to w if necessary
so the global assignment is nonswapped; this exchanges the endpoint sign
labels while preserving their equal/opposite relation, and composes the
label permutations with fixed formal permutations.
Centering removes shifts and produces one fixed permutation per endpoint
in every CRT factor, even where local entries repeat.

WL gives w∈Gv in each prime-power factor. If its local endpoints are
different weighted classes, the G assignment must be nonswapped. If
they coincide, §3's parameter stabilizer changes the representative to
nonswapped without changing w. Thus choose in each factor

\[
 w=\lambda_qR^{i_q}v.
\]

Factors with v=0 have w=0 and impose no condition on the eventual global
G-element. There is at least one nonzero factor, since v∈Ω_n.

If ε_X=ε_Y=ε, every nonzero factor has λ_q=ε: otherwise both actual
endpoint matches differ from their formal equations by reflection,
contradicting §3's no-simultaneous-reflection statement. Both matches are
therefore positive. If local supports have actual collisions, their
fixed pair(π_X,π_Y) belongs to the219 table for that local line and i_q.
If no collision occurs it is the corresponding formal pattern, also
in that table. By its unique rotation index all i_q equal a single i.
Zero factors are compatible with the same choice. CRT gives w=εR^iv.

If ε_X≠ε_Y, in every nonzero factor exactly one endpoint reflects.
Section3 shows both local supports are then six-element, inflated from
F13 or F19. Thus the ordinary parity comparison is valid: all formal
permutations are even, an actual negative match differs by a three-
transposition reflection, and an actual positive match is exactly formal.
In particular sgn(π_X)=ε_Xλ_q, so λ_q is one common λ. One of the two
global endpoint signs equals λ; its matching is formal in every nonzero
factor. Its three formal rotation permutations are distinct, so again
all i_q coincide. CRT gives w=λR^iv. Restore the optional T to recover
the original endpoint assignment and obtain w∈Gv.

Conversely every G-element preserves the unordered pair by the integer
coefficient identities. The proof retains the endpoint assignment: a
swapped global identification produces an element λR^iT rather than a
nonswapped element. If X_v,Y_v were globally congruent, it would give a
swapped identification with w=v. Hence a nonidentity reflection-type
G-element would fix v; each such fixed line is an actual collision line,
contradicting Ω_n. The endpoints are therefore different.

G acts freely on Ω_n: its six reflection-type fixed lines are collision
lines; the other nonidentity fixed-vector matrices have determinants
1,3 or4, all units modulo n, forcing v=0. The twelve collision kernels
have n points each and meet pairwise only at zero, since their normal
determinants have prime divisors only2,3,5,7. Consequently
|Ω_n|=n²−1−12(n−1)=(n−1)(n−11). Divide by the now-proved free global
orbit size12 to obtain the pair-edge formula.

## 6. Full global unique partner outside31

Assume31 does not divide n and two global Bloom pairs share an endpoint.
Normalize it by T to be X_v and X_w. Weighted one-endpoint local
separation in §2 puts w∈Gv in every factor, even if its list entries
repeat. As in §5, choose a nonswapped representative λ_qR^(i_q): the
matched local endpoint determines the assignment when classes differ,
and a stabilizer corrects it when they coincide.

Let ε,π be the sign and fixed label permutation of the global shared
endpoint matching. In a nonzero local factor, if λ_q=ε its actual
permutation belongs to the57 positive patterns from §4. If λ_q=−ε,
the endpoint reflects, so its permutation belongs to one of the two
negative triples at13 or19. These three sets of full permutation arrays
are pairwise disjoint. The fixed global π cannot mix these alternatives.

If all nonzero factors are positive, the57 table supplies one common
rotation index and CRT gives w∈Gv. If all are negative, every nonzero
factor has the same prime13 or19 because the negative triples are
disjoint. There is only one CRT factor for each prime. Its triple also
fixes i, and every other factor has v=w=0. One common G-element again
works globally. Thus sharing any endpoint gives the same global pair.
Every Bloom family has exactly two classes, with B(n) families.

The31 exception is real at every allowed modulus divisible by31. Let
t=n/31. Multiply the accepted characteristic31 shared-endpoint example
by t; the injection Z31→Zn preserves the six distinct points, homometry,
and the two different partner classes. Any rigid transport between its
inflated supports has shift in the subgroup, since zero is a support
point, and would descend to a rigid transport in Z31. The distinct
original classes remain distinct. Hence some endpoint has two Bloom
partners at every such n. No family-count formula is inferred at these
moduli; the pair-edge formula remains valid.

## 7. Exact evidence and trust boundary

Reproduce the new coefficient certificate:

```bash
.venv/bin/python src/six_composite_weighted_gluing.py
.venv/bin/python tests/test_six_composite_weighted_gluing.py
```

It regenerates the219 paired patterns, both57-pattern endpoint tables,
all line automorphisms, the disjoint reflected triples, both m_5 integer
identities and the64 weighted extensions of the inherited lift matrices.
The saved certificate is
`results/2026-09-30-six-composite-global-attempt/certificate.json`, SHA256
`ceeea3aff49a49f0edcaf284cf3a744355a8d855d618b466049178ce43641865`.
Every claim about finite table coverage has full witnesses. No large-n
sampling is used to establish completeness.

**[COMPUTED]** The new six regression groups pass6/6. They independently
generate label automorphisms by equal-coordinate blocks, compare every
219/57 table witness, verify actual prime-power collision partitions,
distinguish near-collisions modulo p from actual collisions modulo p²,
derive the reflected label permutations from actual field point lists,
and check the integer moment and64 weighted lift extensions. They do not
replace the fresh whole-proof attack. Source lives in
`src/six_composite_weighted_gluing.py`, tests in
`tests/test_six_composite_weighted_gluing.py`; output stays in the dated
result directory.

The proof depends on elementary ring algebra, the accepted
integer moment/formal G identities, the40/24 exact lift certificates and
the219/57 exact label table. The fresh independent attack checked the
weighted normalization, assignment-stabilizer choice, zero CRT factors,
the distinction between actual collisions and mod-p collisions, and the
full coverage of positive/negative label patterns. The full written attack accepts the stated scope and every table
acceptance condition. The separate4,147,200-case full coefficient
matrix enumeration is an independent alternative; this proof does not
assume its counts or its Smith reductions.
