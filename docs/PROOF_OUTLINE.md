# Condensed statement and proof outline for an independent assessment

This is an **AI-assisted, internally reviewed, computer-assisted proof claim**.
The outline is a map to the proof, not a substitute for checking its certificates.
Historical novelty and external mathematical validation remain unresolved.

## Exact claim

For every positive integer $n$, identify six-element subsets of $\mathbb Z_n$
under translation and reflection. Two such classes have the same directed
autocorrelation

$$r_A(t)=\#\{(a,a')\in A^2:a-a'=t\}$$

**if and only if they are connected by a finite sequence of the explicitly
specified constructions in Theorem G**. Every intermediate set has six
distinct points. This is complete generation of homometry classes, permitting
compositions. Unique representatives and counts of all families are unresolved.

## Eight proof steps

1. **Specify the constructions.** The grammar includes the classical Bloom
   pair below, four block moves with explicit cross-difference identities,
   parallelogram-dyad exchange, half-coset complementation, conditionally
   autocorrelation-preserving unit multiplication, and thirteen fixed cyclic
   templates. The full parameter conditions and template table are in
   [Theorem G, Section 1](../notes/2026-09-30-six-generation.md).

   $$\begin{aligned}
   X&=\{0,p,q-2p,2q-2p,2q,3q-p\},\\
   Y&=\{0,p,q+2p,2q-p,2q+p,3q-p\}.
   \end{aligned}$$

2. **Prove soundness.** Each move preserves $AA^*$ in the integral group
   ring, hence preserves autocorrelation. Compositions preserve it too.
   This proves the “connected implies homometric” direction.

3. **Encode any nontrivial homometric pair universally.** The translation/
   reflection case is already one vertex. Match the fifteen unordered
   edges of $A$ with those of $B$, retaining signs and multiplicities.
   Anchor one vertex on each side. The matching gives an integral
   $15\times10$ relation matrix $M$ and
   $G_M=\mathbb Z^{10}/\operatorname{row}_{\mathbb Z}(M)$.
   The actual pair is an image under $G_M\to\mathbb Z_n$.
   Its free rank is $d=10-\operatorname{rank}_{\mathbb Q}(M)$, with $0\le d\le5$.

4. **Handle $d=0$ by a proved bound.** Incidence-matrix minors bound the
   torsion order by 135. Thus the pair comes from a cyclic subgroup of order
   at most 135. Two independent complete enumerations and explicit connecting
   certificates cover that finite range. Subgroup inflation lifts the paths.
   This bound, rather than a trend in the data, permits arbitrary $n$ here.

5. **Handle noncongruent real projections.** If some map $G_M\to\mathbb R$
   produces a noncongruent pair, the complete six-atom line theorem and an
   integral lifting check put the universal pair into the Bloom construction.
   Repeated projected points are included by the six-atom line theorem
   allowing coincident points with multiplicity.
   This step depends on exact solver encodings and finite presentation checks.

6. **Handle congruent real projections.** Otherwise every real projection
   is congruent. Finitely many possible alignments cover the whole real
   solution space. A vector space cannot be a finite union of proper linear
   subspaces, so one alignment works throughout. This reduces the remaining
   cases to an arrangement of 120 signed-edge relation directions. Integral
   lattices remain intact; rational reduction is used only for heights.

7. **Exhaust the positive-rank branches.** Free ranks $d\ge3$ reduce to
   an explicit block reflection. Free ranks $d=1,2$ use 315 height strata
   and an exact quotient DAG with 10,602 nodes. Matching every uncancelled
   difference with both compatible signs gives exhaustive branching;
   decreasing unmatched multiplicity gives termination. Integral identities
   certify reductions. Terminal cases have construction certificates or a
   complete cyclic torsion-character check, including forced collisions.

8. **Check specialization and conclude.** Verify that the universal
   constructions descend to cyclic images with six distinct endpoints.
   Half-coset complementation needs a separate merger/kernel argument.
   The branches exhaust all $d$ and both projection cases, proving the
   “homometric implies connected” direction for every $n$.

## What to ask the assessing model

Erickson–Jones [Problem 5.2](https://arxiv.org/html/2412.08997v4) asks to extend
their classification and enumeration problem to $k\ge6$. Assess whether this
**complete generating theorem**, if correct and new, is a substantial partial
answer; do not assume it supplies their disjoint classification or enumeration.

Attack the logical cover, the six-atom line theorem and its encoding, the
135 bound, integral versus rational reductions, completeness of the 315
strata and terminal certificates, and specialization under collisions.
Distinguish a sound proof strategy from a verified proof and from novelty.

**Companion result:** Theorem AP classifies the parameter fibres of the
classical Bloom construction for every $n$ and counts its nontrivial
unordered pair edges as $|\Omega_n|/12-2[12\mid n]$. This counts that
construction, not all six-point homometry families.

**Evidence to provide:** [full proof](../notes/2026-09-30-six-generation.md),
[assembled adversarial review](../notes/2026-09-30-six-generation-review.md),
[component proofs and limitations](RESULTS.md), and
[reproduction instructions](REPRODUCING.md). Internal reviews and archived
checks are included; the default verification does not regenerate the whole proof.
