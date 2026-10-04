# Exact binary reconstruction on any finite periodic grid

1 October 2026. PQ1/PQ3, constructive algorithm for arbitrary cardinality.

**Status: [PROVED], in-house.** The full proof and repaired implementation
were accepted in the separate adversarial review named below; eleven
independent review groups pass. This is not external peer review. No novelty
is claimed for exhaustive reconstruction, correlation identities, anchoring,
or branch pruning. Implementation: `tools/inverse_grid/src/inverse_grid.py`; original tests:
`tools/inverse_grid/tests/test_inverse_grid.py`; separate attack: `tools/inverse_grid/tests/test_inverse_grid_review.py`
and `docs/general_matching/INVERSE_GRID_REVIEW.md`.

## Input, output, and scope

Let `G = C_(n_1) × ... × C_(n_D)`, with positive integer periods. Coordinates
use their canonical ranges and lexicographic order. The input is a sparse
function `C:G -> Z_(>=0)`. Omitted displacement bins mean **zero**, not
unmeasured data. A solution is a subset `A` satisfying

    C(t) = #{(a,b) in A × A : a-b=t}.

Thus pairs are directed, diagonals are included, and `k=C(0)` is the unknown
set's cardinality. Equalities here concern ordinary integer multiplicities.
They are not equalities only modulo a positive-characteristic coefficient
field. The solver uses exact integers and does not reconstruct fractional
occupancies, weights, noisy counts, or continuous positions.

Solutions are returned once per orbit `A -> u+A` and `A -> u-A`. No other
rotation, coordinate permutation, multiplier, or group automorphism is
quotiented out. The output describes **every** class when `complete=true`,
and only the classes found so far when `complete=false`.

Input checks require `k<=|G|`, total mass `k²`, `C(t)=C(-t)`, `C(t)<=k`, and
even `C(t)` at every nonzero element of order two. These are necessary:
mass counts all ordered pairs, inversion swaps their order, fixing the first
endpoint allows at most k pairs at a shift, and reversing a pair at an
order-two shift is a fixed-point-free involution. They are not sufficient;
an accepted input can have zero realizations, which a complete search reports.

## Theorem IG

For every such grid and accepted sparse input, an uninterrupted fresh call
to `solve` without limiting parameters terminates. Its output is exactly
the set of binary solutions modulo translation and global inversion. All
listed solutions from a limited call are valid. A correctly saved, unedited
checkpoint can be resumed without losing any unfinished branch.

Here and below, termination is a mathematical assertion about finite search.
It does not assert that arbitrary inputs are practical to exhaust on given
hardware. A process kill before a checkpoint is saved is not a graceful
interruption; a further interrupt during recovery is also outside the
single-interruption recovery guarantee. Recovery applies to interrupts
caught in `solve`'s search loop; interrupts during initial validation,
restore, result construction, or external serialization can raise without
producing a new saved result. Those interruptions are not evidence of a
completed search.

### 1. Anchor and sparse support

If k>0, translating any solution by minus one of its occupied points gives
an equally correlated solution containing zero. Every other point p of this
anchored solution contributes the pair `(p,0)`, so `C(p)>0`. Let

    S={t != 0 : C(t)>0}, s=|S|.

All anchored solutions are `{0}` plus a `(k-1)`-subset of S. Since every
positive off-diagonal bin contributes at least one unit and the off-diagonal
mass is `k²-k`, `s<=k(k-1)`. This removes any need to allocate |G| cells.
For k=0, mass zero gives the unique empty solution.

### 2. Residual budgets and candidate pruning

For a partial ordered set P containing zero, define the off-diagonal residual
`R_P(t)=C(t)-#{(a,b) in P² : a!=b, a-b=t}` for nonzero t. A negative residual
rules out all completions, because adding occupied points cannot remove pairs.

Appending p adds, for every a in P, both shifts p-a and a-p. These are
counted with multiplicity even when the two shifts coincide. The procedure
`_cost` computes precisely this counter. A candidate is admissible only if
its entire cost is at most the residual in every bin. Any point belonging
to a completion must pass this necessary test.

Only candidates larger than the last prefix point are considered. Every
anchored subset has a unique increasing ordering, so this removes duplicate
ordered traversals without removing any anchored subset.

If h=k-|P| additional points are needed, fewer than h admissible candidates
means no completion. If candidates are `p_1<...<p_l`, a first new point
`p_i` with `i>l-h+1` has fewer than h-1 admissible successors. Admissibility
can only shrink when the prefix grows: its residual decreases and each
candidate's cost increases. Hence branching only over the first l-h+1
candidates is safe.

### 3. Optimistic capacity pruning

For each shift t, `_capacity` counts all directed pairs involving at least
one admissible candidate, among the union of the prefix and **all** admissible
candidates. Prefix-prefix pairs are excluded because they have already been
paid from the residual. Every completion uses a subset of these candidates,
so every new directed pair is included in this capacity. If some residual
count exceeds capacity, no completion can pay that count. Counting mutually
incompatible candidates together only increases this upper bound and
therefore cannot wrongly prune a completion. The implementation skips this
optional calculation when there are more than 48 candidates.

### 4. Leaves, equivalence, and exhaustiveness

At a leaf of k distinct points, zero residual means all off-diagonal counts
match. The diagonal count is k automatically, so all counts match exactly.
Conversely any true completion survives every necessary prune above, reaches
its leaf in increasing order, and is accepted.

`canonical` examines all 2k arrangements obtained by subtracting an occupied
anchor and choosing global sign ±1, sorts each, and selects the minimum.
Every translate or inverted translate that contains zero has exactly this
form. Since the lexicographically minimal arrangement contains zero (any
occupied anchor can be moved there), this gives exactly one representative
per required orbit. The empty arrangement is canonical by definition.

The finite depth-first traversal partitions the remaining choices into
children according to their first new point. Each prefix is processed once
in an uninterrupted run, and the finite frontier is eventually exhausted.
These facts prove both soundness and completeness.

### 5. Limits and graceful interruption

Node, time, and solution limits are checked between nodes. A nonempty
frontier means `complete=false`. Time is a soft limit: one node, final
serialization, or checkpoint validation can run beyond the supplied time.
The solution limit counts equivalence classes, and does not certify that
no other class exists. There is no hard memory ceiling.

The active prefix remains on the frontier while its expansion is prepared
in local variables. Only after expansion is ready does the solver replace
the parent by its children, add an optional valid solution, and update
counters. A completion marker is set last. If a single `KeyboardInterrupt`
arrives before that marker, the frontier tail is restored to the parent
and pre-node counters are restored. A valid solution already inserted can
remain because deduplication makes reprocessing harmless. Thus an unfinished
active subtree cannot be lost, nor can an interrupted last branch falsely
be reported as exhausted. Between-node interruption leaves the frontier
unchanged. An interrupt after the completion marker leaves committed work.

## Verification and trust boundary

Checkpoint checksums detect accidental edits, and target and loaded-source
identities prevent routine cross-input or cross-revision resumes. They are
not cryptographic certificates that all earlier branches were searched.
Someone able to edit a checkpoint and recompute its checksum can delete
frontier entries or solutions. Resumable completeness assumes the checkpoint
was produced by the trusted solver and was not deliberately altered.

The source digest is captured at module load, rather than reread after an
on-disk edit during execution. This is source identity in the normal trusted
Python loading environment, not signed executable attestation.

`verify_result` independently checks each listed solution's exact counts,
canonical form, and metadata. That establishes solution validity only.
With `--recompute`, a new search starts at the root; completeness is verified
by replay only if both the claimed result and the fresh run are complete
and have exactly the same classes. Replay uses the same algorithm, so it
is not a second independent mathematical method. Independent enumeration
and immutable-reference tests supply separate bounded controls.

## Cost and practical meaning

For k>0, a coarse bound on visited nodes is
`sum_(j=0)^(k-1) binomial(s,j)`. Arithmetic uses O(log n_i)-bit coordinates;
candidate and optional capacity work are polynomial per node, but the total
search is exponential in cardinality in the worst case. The depth-first
frontier stores polynomially many prefixes (at most O(ks), each length at
most k), while storing every answer can itself be large. Nothing here
proves an efficient general classification or a compact all-k grammar.

This is an exact inverse interface with general input types, explicit
equivalence, progress, limits, resumability, and replay. It is useful for
sparse periodic binary configurations even when the ambient grid is large.
Whether it is useful for a particular larger input is measured, not inferred
from the cardinality-independent theorem.
