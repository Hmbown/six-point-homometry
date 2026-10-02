# Separate adversarial review: three independent dyad fibers

30 September 2026. Reviewer: the integer/Bloom/fiber agent, separately
from the three-dyad builder. This review does not claim novelty.

**Verdict: ACCEPT [PROVED], computer-assisted, for the exact scope of
Theorem T in `notes/2026-09-30-six-three-dyads.md`.** Every genuine cyclic
six-set image of the three-independent-height dyad branch is generated
by L2 or L4. The remaining two noncyclic universal configurations cannot
produce cyclic six-sets. No arithmetic-progression-height or other
multiplicity branch is implicitly included in this verdict.

The reviewer read the entire proof, the builder, its checker, and the
checker's imported integer arithmetic/quotient routines. The complete
663,552-case orbit checker was rerun from the saved certificates. The
reviewer then wrote additional independent controls for the intended
height maps and the complete cyclic-character obstruction. No builder
or reference code was changed during this attack.

## Attack 1: existence and scope of compatible signed matchings

A homometric pair in an abelian group has equal unordered-edge
multiplicities in classes {d,-d}. This follows from equality of directed
multiplicities; an involution contributes twice per unordered edge on
both sides. Thus a signed occurrence bijection exists even when distances
repeat or have order two. Diagonal terms contribute six zeros on both
sides and cancel. These facts justify using fifteen unordered edges.

The height assumption is stronger than merely three distinct real
heights: the two differences u,v are independent over Q. Therefore the
unsigned classes of u,v,v-u are nonzero and distinct. Each contains four
cross-edge occurrences on either side, and the zero-height bucket has
three internal occurrences. With the same fiber labels the cross signs
are forced positive. The internal signs must remain free; the builder
retains all eight possibilities. The exact count is consequently
24^3*6*8=663,552, without a numerical-height or modulus bound.

A possible failure would have been silently using only one internal
sign at an involution. No such omission occurs. Another would have been
extending the claim to arithmetic-progression heights, where buckets
merge. The note explicitly excludes that scope. The independently
written extra control verifies both prescribed free-height vectors on
every relation of every representative: 2,990 height-map checks pass.

## Attack 2: orbit reduction and anchor changes

The allowed transformations are six independent within-fiber swaps,
one common S3 permutation of fibers, and pair interchange. All are
relabellings/reanchoring of the same configurations. Moving vertex zero
requires subtracting the new anchor, which is an invertible integer
change of the five anchored coordinates; no division or unit action is
introduced. Reversing an endpoint order changes only a relation-row
sign. Pair interchange inverts a signed edge equality and is valid for
both signs.

The builder uses small generator tables. The checker does not rely on
those tables: it explicitly applies all 768 vertex transformations to
each saved representative, recomputes the matching code, and compares
the full resulting set to the saved orbit. It also verifies disjointness,
minimum representatives, and that all integer codes 0,...,663551 occur
exactly once. The matching-code encoding is injective on the three S4
bijections and the signed S3 internal bijection. The checker's matrix
constructor separately confirms that all fifteen source and target
edges occur exactly once and that every sign is +/-1.

This audit passes: **1,495 orbits covering 663,552 cases**. A hidden
missing orbit, an accidental affine quotient, or an invalid shortcut in
the builder's generator tables would fail these exact set comparisons.

## Attack 3: universal groups and non-saturated integer lattices

Replacing integer relations by their rational span would erase precisely
the torsion relevant to this problem. The stored certificates retain
integer U,V and signed D, and the checker verifies UMV=D and
|det U|=|det V|=1 using integer multiplication and Bareiss determinants.
It imports neither SymPy nor the builder nor a normal-form routine.
The row-coordinate convention is correct: old generator e_j is the j-th
row of V in the diagonal quotient. Zero diagonals are free coordinates;
nonunit diagonal entries are retained as torsion, not discarded.

All 1,495 certificates pass. Each universal tuple has at least the two
required free directions. Cases with additional free directions are
legitimate: the original height projection need not be the whole free
quotient. The collision, rigid-motion, and mechanism statements are
checked in the full universal group before specialization.

## Attack 4: all dispositions and their image behavior

The counts reproduced by the checker are:

| disposition | orbits | signed matchings |
|---|---:|---:|
| forced collision | 1,378 | 649,504 |
| universal T/I | 97 | 12,288 |
| L4 | 15 | 1,344 |
| L2 | 3 | 160 |
| cyclic collision from C2 squared | 2 | 256 |
| total | 1,495 | 663,552 |

For each collision, two distinct vertex labels are certified equal.
For each T/I case, the exact sign and anchor map the whole point sets.
These are hereditary conclusions under every homomorphism, so pruning
cannot lose a binary nontrivial cyclic image.

For each L2/L4 case, the checker reconstructs the aligned common block,
removed block, added block, and the translating element. L2 checks
invariance of the cross-distribution under that translation. L4 checks
that the translating element is nonzero and killed by two, and that the
combined cross-distribution is invariant. These are the stated
structural conditions, not an invocation of full autocorrelation as the
mechanism. Expanding the two cross terms independently confirms both
identities. Internal block autocorrelation is translation invariant.

All identities survive a group homomorphism. The six-distinct-points
condition on both target sets ensures that their polynomial sums still
represent binary sets, with the required disjoint blocks. Further T/I
collapse in an image is allowed and does not invalidate generation.

## Attack 5: the two C2-squared obstructions

The three displayed differences f,e,e+f are all nonzero and distinct
involutions. A cyclic group has at most one nonzero involution, so every
homomorphism of C2 squared to it kills at least one of those differences.
Because each is the difference of two A vertices, every cyclic image
collides. This reasoning excludes only cyclic six-set realizations;
the actual noncyclic homometric configurations remain valid.

The checker verifies the three differences, their orders, and the sum
relation exactly in each universal group. As a separate hostile control,
the reviewer enumerated all four torsion characters for each of the two
C2 squared groups while retaining both free coordinates. All eight
characters force a within-tuple collision. Independent free-coordinate
choices cannot rescue such a collision.

## Reproduction and trust boundary

```
.venv/bin/python tests/test_six_three_dyads.py
.venv/bin/python tests/test_six_three_dyads_review.py
```

The complete checker rerun is logged at
`results/2026-09-30-six-three-dyads-review-rerun.log`; it completed in
5.38 seconds. Exact hashes and counts are in
`results/2026-09-30-six-three-dyads/verification.json`.
The additional checks and their immutable-reference specialization count
are recorded in `results/2026-09-30-six-three-dyads/adversarial-controls.json`
and `results/2026-09-30-six-three-dyads-adversarial-controls.log`.

This is a finite computer-assisted proof with exact integer certificates
and independently written checking logic. It is not a Lean proof or a
standalone proof-kernel artifact. Its trust boundary includes ordinary
Python integer arithmetic and the audited verifier. The protected
reference was used only for cyclic specialization controls, not for
universal completeness. No mathematical repair was required by this
review. The theorem's scope remains one complete branch of the ongoing
six-note classification.
