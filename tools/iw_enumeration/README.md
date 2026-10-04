# A second, solver-free derivation of Theorem Iw

Author: Hunter Bown, with AI assistance. Added 4 October 2026.

**Theorem Iw** (`notes/2026-09-30-six-integer-theorem.md`, Section 6): two
real multisets of total multiplicity six with equal autocorrelation that are
not congruent by translation or reflection form a Bloom pair, with repeated
atoms allowed. The archived proof is an SMT unsatisfiability certificate
(Z3 and cvc5 on one encoding; cvc5 with proof checking on an independently
written encoding). A solver certificate is only as good as its encoding, so
the theorem is re-derived here by a different method with no solver, no
floating point and no third-party library: an exhaustive branch-and-bound
over sorted orders with exact rational arithmetic.

The theorem matters for Theorem G because branch BF of the completeness
proof feeds a real projection of the universal pair into Iw.

## Method

Normalize both configurations to `0 = a_0 <= a_1 <= ... <= a_5 = 1` and
`0 = b_0 <= ... <= b_5 = 1`. Weak inequalities allow coincident atoms, so
this is the multiset statement. Equal autocorrelation of two multisets of
the same mass is the same as equality of the two multisets of fifteen
interval lengths `a_j - a_i`, `b_j - b_i` (`i < j`), zeros included.

Two multisets of fifteen numbers are equal exactly when, after sorting each,
they agree position by position. Lengths are monotone under interval
inclusion, so among tied lengths one can always sort a sub-interval before
an interval containing it. The search therefore chooses, for `k = 1..15`,
the k-th smallest A-interval and the k-th smallest B-interval, each from the
*inclusion-minimal* unplaced intervals, and adds

- the equality `d_A(e_k) = d_B(f_k)`,
- the order inequality `d_A(e_k) >= d_A(e_{k-1})`, and
- `d_A(e_k) <= d_A(m)` and `d_A(e_k) <= d_B(m')` for every minimal unplaced
  interval `m, m'` (so `e_k` really is the k-th smallest).

Every homometric pair is reached by some branch (completeness of the
branching). A branch is cut when its linear system is infeasible, decided by
an exact two-phase simplex over `Fraction`. A branch is closed as **good**
when its explicit equalities alone already force the configuration into a
*target*: one of the Bloom lines or the congruent locus. Every surviving
leaf is a polyhedron whose affine hull (explicit plus implicit equalities,
the latter found by exact LP maximization of each slack) must lie in one
target; a convex set inside a finite union of affine subspaces lies in one
of them, so this is the right test. A leaf failing it would be printed as a
counterexample.

Targets. The congruent locus is `b = a` or `b = reflect(a)`. The Bloom lines
are generated from the formula `X = {0,p,q-2p,2q-2p,2q,3q-p}`,
`Y = {0,p,q+2p,2q-p,2q+p,3q-p}`: within each slope chamber the sorted,
min-shifted coordinates are linear in `(p,q)`, so the normalized pairs form
an affine line; all chambers, both signs of `p`, both reflections and the
interchange give 16 distinct lines, which agrees with the 16 planes found
in the original proof's chamber analysis.

Symmetry breaking adds three linear inequalities, each justified by a
symmetry preserving the others: reflect A so `a_1 + a_4 <= 1`, reflect B
likewise, swap so `a_1 <= b_1`. Two inclusion-minimal candidates that are
already provably equal under the current equalities yield identical leaf
systems, so only the first is branched on.

## Controls

- Four points: every branch closes as congruent (161 nodes). The
  classical statement that four-point multisets are determined up to
  congruence is recovered.
- Five points: every branch closes as congruent (30,499 nodes, about one
  minute on 13 processes). Five-atom multisets have no non-congruent
  homometric partner, with repeated atoms allowed.
- `tests/test_iw_enumeration.py`: exact simplex against vertex enumeration,
  the 16 Bloom lines, membership of known Bloom pairs including the
  repeated-atom pair `{0,1,3,3,7,8}/{0,2,4,7,7,8}`, detection of implicit
  equalities, and the four-point run.

## Result for six points

See the section appended below after the run, and
`evidence/summary-6.json` / `evidence/log-6.txt` for the raw record.

## Running

```sh
.venv/bin/python tools/iw_enumeration/iw_sorted_order_enumeration.py --points 6 --jobs 12
.venv/bin/python tools/iw_enumeration/tests/test_iw_enumeration.py
```

Standard library only. The six-point run is the long one; the first-level
branches run in separate processes and a summary is written to `evidence/`.

## Trust boundary

This derivation shares no code, encoding or solver with the SMT proof. What
the two have in common is the statement and the Bloom formula. Remaining
trust: Python's `fractions` module, the correctness of this program's
simplex and rank routines (unit-tested above), and the two prose arguments
(branching completeness; the convex-set-in-a-finite-union step) stated in
the method section.
