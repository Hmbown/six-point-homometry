# Fresh inverse-grid adversarial review, 1 October 2026

Scope: `tools/inverse_grid/src/inverse_grid.py`, `tools/inverse_grid/tests/test_inverse_grid.py`, and the author's
written proof in `docs/general_matching/INVERSE_GRID.md`, read in full. This is a
separate fresh-context attack; no reference source or data was modified.
The root agent had run the ten immutable baseline tests and was already
running the new author suite; this reviewer did not duplicate those runs.

## Current disposition

**[PROVED], in-house Theorem IG accepted after repair.** The full written
proof establishes exact finite exhaustive reconstruction in its stated
binary/discrete/exact-input scope. The fresh reviewer finds no remaining
mathematical or operational completeness blocker. This is not a novelty,
efficiency, compact-grammar or external-validation claim. Eleven independent
reviewer test groups pass after the two repairs below, in 3.826 seconds.

**[COMPUTED]** Independent literal enumeration agrees with the solver on
557 target fibres from all 9,538 binary arrangements on
`(1,1,1)`, `(1,3,1,2)`, `(2,2,2)`, `(2,5)`, `(3,4)`, and `(1,2,3,2)`.
Every ambient translation and simultaneous global inversion was explicitly
enumerated to obtain the expected representative; the solver's correlation
and canonicalization helpers were not used to construct expected answers.
This supplies bounded independent evidence, not an unbounded computational
completeness claim.

**[COMPUTED]** A second sweep checks every necessary-condition target on
`Z_2 x Z_3` for every cardinality. All 31 agree; 18 have no binary realization.
Their absence is proved only by independent literal exhaustive enumeration
at this finite grid, not by the algebraic necessary conditions alone.

**[COMPUTED]** One-node checkpoint/resume runs reproduce fresh search answers
and counters for empty, singleton, full-grid and genuinely ambiguous targets.
A product example on `Z_7 x Z_7` verifies that separate axis reflections
remain distinct classes: quotienting permits only simultaneous global
inversion, not coordinatewise signs, rotations or coordinate permutations.

**Initial blocking defect, now repaired:** the initial interruption handler lost
an active search subtree if `KeyboardInterrupt` arrives after `stack.pop()`
but before its children or solution are committed. Interrupting `_residual`
at the initial node returned `complete=True`, `termination="exhausted"`, no
solutions, and an empty checkpoint for the all-interval Z_12 tetrachord
target, whose fresh search has two classes. The repaired solver prepares
expansion locally with the parent still on the frontier, then commits the
frontier, valid solution and counters, with rollback until the final marker.
Deterministic regressions pass for `_residual`, `_cost`, `_capacity`, leaf
canonicalization, interruption at every DFS node and interruption at six
commit boundaries, including partially updated counters and an already
inserted solution. All resumed answers and five cumulative counters exactly
match the uninterrupted search. Interruptions during checkpoint serialization
or validation can still raise before a saved result exists; the recovery
guarantee concerns interrupts caught within the search loop.

**Initial provenance defect, now repaired:** the initial `source_digest()` read
the current disk file, although a resident imported module continues
executing its already loaded functions after that file changes. An old-code
run could therefore stamp a new-code digest. The repaired solver captures
the loaded-source identity at import. A disposable-copy test edits only its
temporary file after import, verifies that the resident solver retains its
original identity and resumes correctly, and verifies that a fresh process
loading the changed source rejects the original checkpoint.

**[COMPUTED]** The 8-mark target `(0,1,4,9,15,22,32,34)` in `Z_1000003`
has 56 nonzero support candidates, exercising the branch that skips initial
capacity pruning. Its entire output agrees with a separate largest-distance
integer turnpike algorithm. The small-diameter unwrapping argument below
justifies this independent method for this cyclic target. The check has one
translation/global-inversion class and completes below 10,000 nodes.

## Mathematical attack

The following independent arguments, together with the full author proof and
repaired operational implementation, support acceptance of Theorem IG.

1. **Anchoring and support restriction.** Every nonempty solution can be
   translated so that an occupied point is the zero vector. Each other
   occupied point `p` then contributes to the directed bin `C(p)` through
   `(p,0)`, so `p` must belong to the nonzero target support. This works in
   any product of positive-order cyclic groups, including order-one axes.

2. **Canonicalization by occupied anchors.** In canonical coordinate ranges,
   the zero vector is the least possible point. Every nonempty orbit has a
   translate containing zero, and therefore its lexicographically least
   sorted representative contains zero. Any translation/inversion image
   containing zero is obtained by subtracting an occupied anchor and
   multiplying all coordinates by the same sign. Consequently occupied-site
   anchors cover every possible lexicographic orbit minimum even in multiple
   dimensions. Ambient translations provide an independent computational
   attack on precisely this claim.

3. **Pair-count budget and order-two directions.** Extending a distinct-site
   prefix by `p` adds exactly the two directed differences `(p,a)` and
   `(a,p)` for every previous point `a`. At a nonzero self-inverse difference
   these coincide and must contribute two units to one bin. `_cost()` counts
   them twice; it does not collapse antipodal pairs to one unit. Any true
   completion has nonnegative remaining budgets at every prefix.

4. **Candidate restriction and truncation.** Every member of any true
   completion individually passes the current prefix budget check. With
   `m` sorted passing candidates and `r` sites still needed, a completion's
   least remaining point has index at most `m-r` (zero-based), because at
   least `r` candidates must remain from that index onwards. It therefore
   belongs to `candidates[:m-r+1]`. Sorted extension enumerates each anchored
   subset along one unique path; truncation cannot remove that path.

5. **Optimistic capacity.** For a completion contained in the candidate set,
   its residual pairs are a submultiset of all prefix/candidate pairs and
   all unordered candidate/candidate pairs counted in both directions.
   Counting incompatible candidates together can only overestimate capacity.
   If any target residual exceeds that capacity, no completion exists.
   Omitting this optional prune for large supports changes cost, not coverage.

6. **Leaves and exhaustion.** A leaf is accepted only with cardinality `k`
   and zero remaining nonzero bins; its `k` distinct sites also give the
   required zero bin `C(0)=k`. Thus accepted solutions are sound. Finite
   strictly increasing prefixes exhaust the candidate support, and the
   preceding arguments preserve every valid completion path, so ordinary
   uninterrupted exhaustion covers every translation/global-inversion class.
   The initial interruption bug was operationally separate; its repair now
   preserves the active subtree until a full node has committed.

7. **Boundary cases.** For `k=0`, nonnegative total mass zero forces all bins
   zero, and the empty arrangement is the sole class. For `k=1`, only the
   zero bin remains and the origin singleton represents the sole class.
   Full-grid targets and order-one factors fall within the same argument.
   Necessary-condition inputs can nevertheless be unrealizable, in which
   case honest exhaustive output is an empty list of classes.

8. **Independent sparse-large-grid reduction.** Suppose a 1D target is
   obtained from an integer set of diameter D, with period n>3D. Every point
   of an anchored cyclic solution has an integer representative in `[-D,D]`,
   because its difference from zero must be supported. If the unwrapped
   span exceeded D, it would lie in `(D,2D]`, which cannot be congruent to
   any supported shift in `[-D,D]` when n>3D. Therefore every solution
   unwraps to an integer set of span at most D. A positive target count at D
   forces span exactly D. Translate the minimum to zero; then both 0 and D
   are occupied. In the independent turnpike recursion, the largest unpaid
   distance is either the greatest unplaced point's distance from 0, or the
   least unplaced point's distance from D. Any unplaced-to-unplaced distance
   is no larger, so branching at x=d or x=D-d preserves every completion.
   This supplies a different exhaustive algorithm for the 8-mark fixture.

## Checkpoint and verification limits

The checksum detects accidental corruption and binds a trusted search state
to an input and solver revision. It does not attest that pending subtrees
were faithfully preserved. A caller can erase the pending stack, recompute
the public checksum, and obtain a formally valid resumed result with a
false completeness assertion. This is an explicit documented trust boundary,
not a newly asserted adversarial checkpoint certificate. A reviewer fixture
demonstrates it; ordinary solution validation correctly reports no completeness
verification, and a fresh complete replay rejects the false claim.

Time limits are checked between nodes; a node can overrun the requested
wall-time bound. Dense support and large cardinality can still make search
exponential. Sparse dependence on support avoids allocation proportional
to huge ambient grid volume, but does not establish polynomial-time or
practical all-cardinality recovery. No novelty claim is made.

## Reproduction

Initial independent non-interruption checks:

```sh
.venv/bin/python -S -m unittest tests.test_inverse_grid_review.IndependentGridAttack.test_every_target_with_order_two_and_degenerate_axes tests.test_inverse_grid_review.IndependentGridAttack.test_necessary_condition_targets_including_unrealizable tests.test_inverse_grid_review.IndependentGridAttack.test_resume_one_node_everywhere tests.test_inverse_grid_review.IndependentGridAttack.test_self_consistent_checkpoint_is_trusted_not_completeness_proof
.venv/bin/python -S -m unittest tests.test_inverse_grid_review.IndependentGridAttack.test_every_target_with_order_two_and_degenerate_axes tests.test_inverse_grid_review.IndependentGridAttack.test_global_inversion_does_not_collapse_separate_axis_reflections
```

The expanded fibre sweep and global-inversion fixture passed in 3.125 seconds
of unittest wall time. All initial bounded jobs remained below the assigned
20-CPU-second review budget. Full reviewer-suite reproduction after repair:

```sh
.venv/bin/python -S tools/inverse_grid/tests/test_inverse_grid_review.py
```

Final full reviewer command passed all eleven test groups in 3.826 seconds.
Root author/reference commands were not duplicated by the reviewer. No
commit, push, reference source edit or raw-data edit was performed.

Accepted snapshot SHA-256 identities:

```text
12a378c6f7a64ba7d85846771495a9e9ef96b562aee585eb482cdd1a345eda92  tools/inverse_grid/src/inverse_grid.py
9604a8da10f1e7a0507676190cab1fd77133a202b50eff0be9756add3db14ee5  tools/inverse_grid/tests/test_inverse_grid.py
c9e210693cc97e3a540437bdd429041ea0f2aabe5da300e069aa7d66957b3759  tools/inverse_grid/tests/test_inverse_grid_review.py
82f11a0687ce91d4dff38178b69fb03f551d15e1496db590d0a7a1bef92d8d3d  docs/general_matching/INVERSE_GRID.md
```

The proof snapshot still carries its author's pending status; a subsequent
status-only promotion does not change the accepted mathematical content.
