# Separate adversarial attack on the two-height theorem TF

30 September 2026. Root reviewer, separately from the builder. Full proof,
producer, certificate enrichment, mechanism recognizer and checker read.
This is an in-house review, not a novelty or external peer-review claim.

**Accepted [PROVED], computer-assisted:** Theorem TF in
`2026-09-30-six-fibers.md`, for all binary cyclic images of two-height
homometric six-pairs, with exactly its stated hypotheses and moves.

The main attacks were as follows.

1. A real projection of a finite cyclic group is trivial, so the hypothesis
   must concern a lift in a finitely generated abelian group. The proof
   explicitly does so. The common height gap is not divided in the group;
   only its positive sign identifies cross edges. The singleton proof
   independently aligns the two actual singleton vertices and compares the
   cross-height coefficient. It is valid for arbitrary torsion.
2. Within-fiber vertex permutations can change the anchored vertex. This
   is still an invertible integral change of the five coordinates on each
   side, obtained by subtracting the new anchor. No forbidden division or
   unit identification occurs. The full independent source/target action
   check covers all40,320 and362,880 cross bijections exactly once through
   their52 and322 orbit representatives.
3. Equality of directed differences is equivalent to equality of unsigned
   edge classes even for order-two differences: each unordered edge gives
   two occurrences at the involutory residue. Repeated and zero classes
   cannot defeat multiplicity cancellation. After subtracting common
   classes, every homometric image must match a chosen remaining A edge to
   at least one remaining B class with one of the two signs. Representatives
   suffice because all edges in one class are already equal up to sign.
4. Adding an equality between remaining classes strictly reduces the
   unmatched occurrence count. Classes may merge, which can only create
   further cancellations. This proves termination independently of the
   cache. Both integral row-lattice inclusions are verified for every
   normalization; using only rational span or one inclusion would have
   been insufficient. The checker reaches every saved node from a root.
5. Universal point collisions persist under every homomorphism and cannot
   produce a six-subset. Universal T/I relations also persist. All118 other
   terminals are checked directly as homometric in their exact presented
   groups, including multiplicities, before applying a mechanism witness.
6. D's group-ring identity remains valid in an arbitrary abelian group.
   On a cyclic image the reviewed nonnegative periodic-weight grammar
   applies. Six distinct endpoints preserve disjointness of the common
   block from the relevant dyads. If a parallelogram step becomes zero,
   the output is congruent, which the theorem explicitly allows.
7. The generalized L3* condition is broader than the older parameterization
   by twice a shift. Its direct identity `P=x^t P*` is sufficient without
   halving t: the new cross terms are simply exchanged. The builder was
   asked to name this explicitly and did so before acceptance. L2, L4,
   and L5 use their exact sufficient cross-distribution conditions.
8. A noncyclic torsion group need not embed in a cyclic target. Exhausting
   all characters into Q/Z is the correct operation: any actual target
   restriction is one of these characters after the canonical embedding
   Z_n into Q/Z. Retain the free coordinates, so no restriction is placed
   on their eventual residues. The36 character quotients exhaust the three
   exceptional groups. Each either forces a collision or has an exact D
   certificate; none is discarded merely for failing a search menu.

The root reviewer reran:

```bash
.venv/bin/python tests/test_six_fibers.py
```

It passes in1.88 seconds:639 quotient nodes,530 signed branches, all118
terminal constructions,36 exceptional torsion characters and309 immutable
reference specializations. The saved normalization witnesses are checked
by multiplication; no normal-form algorithm is used by this checker.
The checker does use SymPy for exact integer matrix multiplication and
determinants; this is an explicit arithmetic dependency, not an independent
small proof kernel. Log: `results/2026-09-30-six-fibers-root-review.log`.

No mathematical defect remains in this branch. The positive-height
decomposition, all orbit actions and every quotient are independent of n.
TF therefore adds a complete structural branch, not a bounded-modulus
observation. It neither proves all six-pairs have two heights nor decides
non-shadow status of an individual output. The larger arbitrary-n problem
still requires the remaining height strata and finite torsion bridge.
