# Reply for an independent assessment

Yes—the intended main claim covers **every modulus by a mathematical
reduction to finite checks**, rather than extrapolating a census. Please
assess the exact claim below. It is AI-assisted working research with written
proofs and separate internal attacks; correctness and novelty still require
independent specialist assessment.

**Theorem G (claimed, internally reviewed, computer-assisted).** For every
positive integer $n$, let the vertices be the translation/reflection classes
of six-element subsets of $\mathbb Z_n$. Add the edges specified by the
generating grammar. Then two vertices have equal autocorrelation if and
only if they belong to the same connected component. Every intermediate
vertex is a six-element set. Multiplication by a general unit is not an
additional equivalence relation.

The grammar contains the classical Bloom construction, four block
translation/reflection moves with explicit cross-difference identities,
parallelogram-dyad exchange, half-coset complementation, unit multiplication
subject to autocorrelation invariance, and thirteen fixed cyclic templates.
The [full statement](../notes/2026-09-30-six-generation.md) gives every
formula, parameter condition and template; the list is allowed to overlap.

The proof architecture is:

1. Prove every generator preserves $AA^*$ in the integral group ring.
   Consequently every connecting path is sound.
2. Take an arbitrary nontrivial six-point homometric pair. Match its fifteen
   unordered edges with signs and multiplicities, including repeated and
   antipodal differences. After anchoring the two sets, obtain a
   $15\times10$ integer matrix $M$ and the universal group
   $G_M=\mathbb Z^{10}/\operatorname{row}_{\mathbb Z}(M)$.
   The input pair is an image of this group in $\mathbb Z_n$.
3. Split by the original group's free rank
   $d=10-\operatorname{rank}_{\mathbb Q}M$, which lies in $0,\ldots,5$.
   If $d=0$, a proved incidence-minor bound gives torsion order at most 135.
   Thus the pair comes from a cyclic subgroup of bounded order. Two
   independent complete enumerations and explicit paths cover that range;
   subgroup inflation transports those paths to every ambient modulus.
4. For $d>0$, if a real projection is noncongruent, the six-atom line theorem
   and exact integral lifting certificates give the Bloom construction.
   Coincident projected atoms are included with multiplicity. This branch
   depends on audited exact solver encodings, not numerical sampling.
5. If all real projections are congruent, a finite-union-of-subspaces
   argument gives one fixed alignment. Reduce the possible rational height
   relations to an arrangement of 120 signed-edge directions while retaining
   the original integral relation lattices and their torsion.
6. Exhaust the remaining branches: $d\ge3$ gives an explicit block move;
   $d=1,2$ uses 315 height strata and a certified 10,602-node quotient DAG.
   Every compatible residual matching is branched on, decreasing unmatched
   multiplicity proves termination, and exact integral identities justify
   each reduction. Terminal cases have construction certificates or complete
   cyclic torsion-character checks, including forced collisions.
7. Check specialization carefully. Injectivity on the six-point endpoints
   and the separate half-coset kernel/merger lemma control degeneracies.
   These branches exhaust the arbitrary input pair and establish completeness.

This is a statement about **whole connected homometry families**, so families
with more than two rigid classes are included. The finite package contains
725,132 nontrivial families and 728,424 pair edges through 135; 73 edges are
covered by saved composed paths rather than saved direct certificates.
Those numbers belong to the bounded branch, not a proposed
formula for all moduli.

The companion theorem AP classifies the parameter fibres of the classical
Bloom construction for every $n$, with count
$B(n)=|\Omega_n|/12-2[12\mid n]$. It counts that construction's pair edges,
not all six-point families. Here $\Omega_n$ is the set of parameters making
both Bloom endpoints six distinct points.

We therefore **do not claim a complete solution of Erickson–Jones Problem
5.2**, whose underlying problem asks for classification and enumeration.
The precise assessment requested is whether G's completeness argument is
sound, whether this explicit construction/path theorem already appears in
the literature, and—if sound and new—how substantial that structural advance
is. Please inspect the line-solver encoding, the 135 bound, completeness of
the height/DAG cover, integral reductions and specialization before treating
this outline as an established theorem.

**Files:** [full G proof](../notes/2026-09-30-six-generation.md),
[assembled attack](../notes/2026-09-30-six-generation-review.md),
[component/result map](RESULTS.md), [condensed outline](PROOF_OUTLINE.md),
[reproduction guide](REPRODUCING.md), and [attribution](REFERENCES.md).
The separate proofs, reviews and computational certificates are packaged.
The fresh standalone verification passed 18 commands; that run does not
regenerate every exhaustive enumeration, structural stratum or solver proof.
