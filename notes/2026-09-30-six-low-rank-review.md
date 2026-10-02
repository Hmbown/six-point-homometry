# Separate adversarial review of the low-rank completeness reduction

30 September 2026. Reviewer: integer/Bloom/fiber agent, separately from the
low-rank DAG builder. No novelty claim.

**Final verdict: ACCEPT [PROVED], computer-assisted, for Statement LR.**
The full argument in `notes/2026-09-30-six-free-dag.md` includes the
halfcoset specialization repair below. Every terminal mechanism and cyclic
character reduction passes independent exact verification. The root agent's
complete orbit/root/branch/lattice audit also passes all 315 strata. This
review establishes the stated low-rank branch; it does not claim the
assembled arbitrary-n theorem independently of its other reviewed branches.

## 1. Scope and the free-height reduction

The object being classified is a universal signed matching presentation,
not a chosen arrangement of points on a finite circle. Its free quotient
admits real homomorphisms. Under LR's hypothesis the entire real solution
space is contained in one fixed labelled T/I graph. Reanchoring, relabelling,
and reflecting B make this graph B=A by an invertible integer coordinate
change. No rational division is needed for this normalization.

Substituting B=A in all matching equations then describes exactly the
solution space: any solution after substitution is a solution of M, and by
hypothesis all solutions of M already lie on that graph. The projection to
A's five anchored coordinates is injective. Thus free dimensions 1 and 2
correspond exactly to substituted-row ranks 4 and 3.

Every substituted row is the difference of two oriented complete-graph
edges. Its nonzero projective directions have the three stated support
patterns, giving 15+60+45=120 directions. Dividing a row's content here is
allowed only for enumerating its *rational height subspace*. It is not
applied to the integer matching relations. This distinction is necessary:
rationally saturating those relations would erase the torsion mechanisms.

Every rank-r span has a basis of direction rows; remove the last basis
row, apply a permutation taking the previous span to its saved
representative, and observe that the direction set is permutation
invariant. This proves the inductive orbit-growth procedure exhaustive.
The exterior-coordinate checker verifies 43,770 rank-three spans in 104
orbits and 116,401 rank-four spans in 211 orbits, independently of the
builder's row-reduction representation.

A rational height vector outside the finitely many unforced hyperplanes
exists; clearing denominators gives an integer vector. Checking all 120
directions on that vector is enough: every relevant equality of signed
edge differences, including repeated heights, is represented among those
directions. Its numerical magnitudes and signs do not create an additional
assumption about generic configurations.

The preceding reduction applies only after obtaining one fixed T/I graph.
That hypothesis comes from the separately reviewed weighted-real/Bloom
projection dichotomy and finite-union argument. LR does not independently
prove that dichotomy, the high-free-rank theorem, or the rank-zero torsion
bound. These dependencies must remain explicit in the assembled theorem.

## 2. Cross-edge matching and the cancellation lemma

For a fixed height vector, orient nonzero-height edges upwards. Occurrence
bijections within equal positive-height bins give all compatible cross
matchings. Within-height label permutations on A and B act independently
and preserve the whole completion problem. If an anchor moves, subtracting
the new anchor is an invertible integer change of generators. Consequently
these symmetries do not identify different cyclic chord classes or impose a
unit-multiplication equivalence.

Equal *unsigned* group-difference classes may be cancelled with
multiplicity. For a non-involution, one unsigned edge contributes one to
each directed difference; for an involution (including zero) it contributes
two to the one directed value. Thus equality of unsigned occurrence
multisets is exactly equivalent to equality of directed autocorrelations,
including all multiplicities. The diagonal contributes six zeros on both
sides and cancels separately.

I specifically attacked whether cancelling universal classes could destroy
a particular compatible matching. It cannot: after passage to the original
full universal presentation, the cancelled contributions remain equal, so
the remaining multisets are still equal. The chosen residual A occurrence
therefore has some residual B occurrence equal up to sign. The original
presentation retains its height homomorphism, so this equality obeys the
height restriction. Any representative of an already equal B class works,
with the appropriate sign. Each branch adds a genuine new equality and
cancels at least one more residual unsigned occurrence; the residual count
strictly decreases, initially at most fifteen.

This reasoning deliberately takes place in the original homometric lift.
It would be invalid to claim that every homometric cyclic image of a weaker
cross-edge root must preserve the chosen height bins: a finite cyclic group
has no nonzero homomorphism to R. LR makes the correct assertion about the
original matching presentation and subsequently transports the terminal
identities to the cyclic target.

A universal collision is hereditary under every homomorphism. Universal
T/I congruence is hereditary too. Stopping at either cannot discard a
binary nontrivial target. A terminal with universal homometry may have more
free directions than the original full matching, because it is a weaker
presentation. That causes no problem: the original factors through it,
and the terminal identities are checked on its entire larger group.

## 3. Integral normalization and coverage evidence

The certified identities C M_source=H_child and C' H_child=M_source prove
equality of the integer relation lattices, in both directions. Checking
only rational spans or only one inclusion would be insufficient. The Smith
identities UMV=D with unimodular U,V then give the full universal quotient,
including its finite torsion. Rows of V are the correct coordinates of the
old vertex generators in the diagonal quotient.

The root agent independently checked the complete cross-orbit cover,
root coverage, residual class counts, every allowed signed branch, both
integer lattice inclusions, and terminal dispositions. Its completed
result is recorded in `results/2026-09-30-six-free-dag-review/summary.json`,
with source SHA hashes in the 315 per-stratum audit files. I additionally
read that checker and confirmed its correspondence to the coverage lemma. The supplied
cover has 315 strata, 328,473 cross-orbit roots, and 10,602 nodes, comprising
7,429 T/I, 2,207 collision, 620 homometric, and 346 branch nodes. These are
certificate counts, not a finite-n census extrapolated to arbitrary n.
The independent audit verifies all 4,822,240 cross bijections, 328,473
roots, 974 signed branches, and 658,894 two-way integer lattice-inclusion
identities. Every node is reachable and every branch strictly reduces the
residual occurrence count.

## 4. Independent terminal mechanism audit

The builder's broad exploratory `block_certificate` only certifies that a
removed block has a rigid image. This alone is not one of the strict
mechanisms. I did not use that label as a proof. Instead, a separate checker
reconstructs and tests each of the sufficient group-ring conditions in the
final atlas, importing no builder, recognizer, SymPy, or normal-form code.

For P=UW*, the checks and hand expansions are:

- L2: x^sP=P, which preserves both cross terms.
- L3*: x^(-s)P=P*, which exchanges the two cross terms. The name must remain
  L3* or explicitly generalized L3; division of s by two is not assumed.
- L4: 2s=0 and x^s(P+P*)=P+P*, preserving their sum.
- L5: UW*=x^(-c)UW for W'=x^cW*, preserving the first cross term and hence
  its involution.
- D: explicit four-point common set and parallelogram dyads, with the
  reviewed mixed-difference condition on a nonnegative weight of mass 12.
- Bloom: the exact six displayed integer-linear expressions in p,q, with
  independent rigid-motion certificates.
- L7: a cyclic subgroup of the stated exact order, exactly half occupation
  in every occupied coset, and the aligned partner equal to the complement
  in their union. The specialization issue is repaired in Section 5.

The checker confirms set distinctness, all partitions and alignments, and
all these exact coefficient identities. The builder atlas gives 271 L4,
135 L3*, 114 L7, 53 L5, 16 L2, 14 Bloom, 8 D, and nine presentations requiring
finite-character reduction. All pass.

As a separate discovery cross-check I applied another recognizer with a
different priority and obtained 481 D, 71 L5, 24 L3*, 20 L4, 14 Bloom, 1 L2,
and the same nine remaining presentations. The independent checker verifies
this entire alternative certificate set as well. The distribution is not
canonical, and neither discovery count substitutes for exact checking.

## 5. A repaired specialization gap: L7 degenerations

A material gap in the initial prose was the suggestion that preserving six
distinct points in each endpoint automatically preserves literal halfcoset
complementation. Distinct occupied cosets can merge across endpoints while
each endpoint remains injective. The issue was independently noticed by
this reviewer and the final whole-argument reviewer. The following small
lemma repairs it without adding a mechanism.

**Six-note halfcoset degeneration lemma.** Let A occupy half of each of
k=12/m distinct cosets of a cyclic subgroup H of order m in {2,4,6,12};
let B be the complementary halves. Under any homomorphism for which each
endpoint image still has six points, either the image pair is globally T/I,
or H retains order m, all occupied cosets remain distinct, and the image
pair is literally the same L7 construction.

To prove this, put K=image(H) and d=|ker(f restricted to H)|. Each old
halfcoset has m/2 points and maps injectively into a K-coset, so d<=2. If
d=2, each half fills that entire K-coset on both sides; the endpoints
therefore have equal images. Thus a nontrivial image has d=1.

When H maps injectively, at most two occupied old cosets can merge into
one K-coset, since their A-halves are disjoint in the injective endpoint.
If two merge, their two A-halves fill the K-coset; the B-halves fill it too.
Thus merged cosets become common full K-cosets. If m=2, every residual
single-point half moves to its complement by the unique nonzero element of
K; common full cosets are fixed by it, so the entire pair is a translate.
If m=4, there were only three occupied cosets. A merger leaves one residual
dyad. Every dyad in C4 has a translated complementary dyad: opposite dyads
translate by a generator, adjacent dyads by the involution. That same
translation fixes the common full K-coset, so the whole pair is T/I.
For m=6 a merger exhausts the two occupied cosets and gives equality.
For m=12 there was only one coset, so merging is impossible. This proves
the lemma.

The checker additionally enumerates every half-subset in the four possible
subgroups, every loss-of-order map that preserves a half, and every possible
occupied-coset merger partition with six distinct endpoints. All 150 loss-of-order cases and 1,448 occupied-coset merger cases
retaining injective endpoints are globally T/I. These finite controls support the elementary
case proof; they are not its logical substitute. The other mechanisms'
identities and within-endpoint disjoint partitions descend directly.

## 6. Exhaustive finite torsion characters

For T=direct-sum C_(d_i), every homomorphism into any cyclic group has the
same kernel as a character T->Q/Z of the displayed form sum k_i t_i/d_i.
Enumerating all product d_i choices is therefore exhaustive. Let
E=lcm(d_i) and g=gcd(E,c_1,...,c_k). Dividing the character values by g gives
the actual image C_(E/g); the free coordinates remain separate. This
actual-image step is essential: one must not assume C_E embeds in the
eventual target when E does not divide n.

The checker independently verifies every character label, coefficient,
image order, projected coordinate, and its disposition. Seven C2-squared
presentations each have four characters that force vertex collisions. The
two C2 x C8 presentations each have sixteen characters, eight forcing
collisions and eight admitting L7. Thus all 60 characters give 44 collisions
and 16 exact L7 certificates, with no residual case. The alternative
certificate set verifies D for all the same sixteen survivors. No bound
on n is introduced by this argument.

## Reproduction and completed gate

```
.venv/bin/python tests/test_six_free_rank_growth.py
.venv/bin/python tests/test_six_free_dag_review.py --resume --require-complete
.venv/bin/python tests/test_six_low_rank_mechanisms_review.py
```

The terminal audit is recorded in
`results/2026-09-30-six-low-rank-review/verification.json` and
`results/2026-09-30-six-low-rank-mechanisms-review.log`. It validates both
`results/2026-09-30-six-free-mechanisms/atlas.json` and the alternative
`results/2026-09-30-six-low-rank-review/mechanism-certificates.json`.
Both certificate hashes are saved with the verification. The exact
orbit/root/branch coverage audit is the root agent's separate artifact.

Trust remains ordinary exact Python integer arithmetic and audited finite
verifier code. This is not a Lean/standalone-kernel formalization. A completed
mathematical proof plus all finite audits is required for [PROVED] status.
Those gates are now complete: the height-growth, integral DAG coverage,
strict mechanism, full torsion-character, and L7-degeneration checks all
pass. The L7 repair is incorporated in the builder note. No unresolved
branch or mathematical objection remains within Statement LR's scope.
