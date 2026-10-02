# Separate executable six-note generator review

30 September 2026. **ACCEPT [PROVED implementation correspondence], within
the already reviewed theorem G and its fixed certificate tables.** This
review checks that the executable driver implements the stated exhaustive
candidate mechanisms and that portable certificates can be checked
independently. It does not repeat the mathematical proof of G.

Reviewed implementation: `src/six_generate.py`; builder controls:
`tests/test_six_generate.py`; independent review:
`tests/test_six_generate_review.py`. The exact final source SHA256 is
recorded in `results/2026-09-30-six-generate-review/verification.json`.

## 1. Material discovery bug found and repaired

The original L7 branch compared its required partner S-A against a list of
rigid images of B constructed by mapping one B point onto a point of A.
Every image in that list intersects A; S-A is disjoint from A. Thus the
L7 discovery branch was unreachable. Other mechanisms happened to explain
the original examples, so the original tests did not expose it.

The builder repaired this with `halfcoset_certificate`: compute the
complement, select one of its points, and align each of the six B points
to it for each sign. These twelve candidates cover every possible rigid
alignment to the complement. The independent regressions now exercise
actual L7 discovery at n=16 and n=400012, including a case with a genuinely
free coset-location parameter. Both return L7 and independently verify.
The fix does not change theorem G or its proof data.

## 2. Completeness of the sparse candidate searches

**Bloom without an n² loop.** Consider a six-distinct specialization of
the standard Bloom pair. In its X endpoint, the points corresponding to
0, p, and q-2p are necessarily distinct. Enumerating the120 ordered triples
of one endpoint therefore includes its translated copies of those three
points. The recovery formulas p=u-anchor and q=v-anchor+2p reconstruct
the correct modular parameters. A global reflection of X is absorbed by
negating p and q. The algorithm tries each endpoint as X. Because Y contains
zero, any translated/reflected Y copy sends zero to a point of the other
endpoint; six target translations for each sign cover it. Thus the search
is complete for Bloom even if parameters wrap around the cyclic target,
without enumerating all n² parameter choices.

**Rigid block alignments and masks.** Any nontrivial L2/L3*/L4/L5 instance
has a nonempty fixed block U; if U were empty the whole pair would already
be T/I. Choose a point of U in A and its preimage in B. The driver's
6×6×2 alignment list includes that rigid image. Enumerating every nonempty
subset of the entire intersection includes U, even when the moving block
also has points in the intersection. Enumerating targets for one fixed
anchor of the moving block recovers every possible translation or
reflection. The tested sufficient identities retain the separate legacy
L3 halving condition in old certificates, while new L3* uses its reviewed
direct cross-term identity without that restriction.

For D, a genuine aligned exchange has four common points and disjoint
remaining dyads with equal sums. Any shared point between those dyads
would force equality of the second points as well; that case is trivial.
Thus using the maximal common four-set in the D recognizer loses no
nontrivial D specialization. The explicit mixed-difference condition is
checked with sparse integer coefficients.

For L7, the cyclic group has a unique subgroup of each possible order
2,4,6,12. Exact residue counts and the repaired twelve-candidate
complement alignment cover it. The six-note L7 specialization lemma in
the reviewed theorem ensures that a non-T/I specialization remains literal
L7, rather than merely preserving its polynomial identity.

For a fixed R seed of modulus q, the solutions of qt=0 modulo n are
exactly t=j·n/gcd(n,q). At most31 values are tried for each saved seed.
Separate endpoint canonicalizations and an unordered-pair comparison cover
orientations and swapped endpoints. These are generator parameters; they
do not silently identify different T/I chord classes under unit action.

## 3. Finite support quotient and composition fallback

The independently canonicalized endpoints both contain zero. If
g=gcd(n,A,B), all their points lie in the subgroup g Z_n, of order q=n/g.
Dividing the coordinates by g gives their ordinary support quotient.
Independent translations/reflections preserve this generated subgroup of
within-set differences. Canonicalization commutes with the injective
scaling from Z_q into Z_n, and introduces no extra T/I identifications.

Theorem G guarantees a direct recognized mechanism for its positive-rank
branches. In the rank-zero branch, the ordinary support order is at most
135. The saved finite graph has a path between the quotient endpoints;
breadth-first search finds one. Each edge is replayed with its original
schema, including unit autocorrelation conditions, and the vertices are
scaled back injectively by g. Thus an indirect finite relation is returned
as an actual composition of six-note classes. The same CRT unit-extension
argument reviewed in theorem FT justifies the interpretation of inflated
unit edges; replay also checks their exact source equality independently.

Missing tables or an unexplained validated pair produce
`GenerationInvariantError`, not an assertion that the pair is nonhomometric.
Nonhomometry and within-endpoint repeated points are rejected at input.
The generator relies on the fixed reviewed finite tables for discovery;
a portable result embeds the selected edge records and needs no table
access for replay.

## 4. Independent certificate replay and adversarial controls

The review checker imports no production canonicalization, correlation,
mechanism, direct-certificate verifier or saved-edge verifier. It computes
canonical classes from cyclic gap words, independently checks the full
directed difference multiset, and reconstructs each sufficient group-ring
condition with its own sparse arithmetic. Its gap-word canon is first
checked against the immutable reference on320 controls.

The independent tests pass:

* all73 saved composition paths, plus independent ordinary inflations of
  all73 with separately translated/reflected endpoints;
* nine saved large-modulus portable examples and all nine legacy edge
  schemas (Bloom, R, unit, halfcoset and the five block labels);
* 2,583 valid nontrivial Bloom parameter controls in selected small rings
  and a large prime, including swapped and independently reflected inputs;
* forty small-ring comparisons with an exhaustive independent search over
  all2n rigid alignments, all fixed-block masks, and all local motions;
* 537 nontrivial specializations of formal terminal templates whose
  ordinary support exceeds135, all independently certified. There were
  560 endpoint-injective projections total;694 other trials collided and
  were recorded as skipped, not counted as coverage evidence;
* actual L7 discovery at16 and400012;
* 27 malformed/tampered certificate rejections and a nonhomometric-input
  rejection. Attacks include false schemas/routes, changed support or
  alignments, forged finite edge labels, zero unit multipliers, altered
  dyad coefficients, empty fixed blocks, illegal halfcoset order, false
  advertised paths, duplicate input points, and floating/bool data.

The large formal projections are implementation controls, not an
extrapolation establishing arbitrary-n completeness. That conclusion
comes from theorem G and the candidate-coverage argument above.

Replay is tested with finite-table access and discovery routines replaced
by exceptions; it still validates the embedded path. A saved certificate's
top-level `vertices` field is now checked against the recomputed path when
present, following this review's tampering observation. Recursive
exact-data validation rejects floats and booleans before arithmetic.
Unknown/invalid certificates fail closed, sometimes with a structural
exception rather than a normalized friendly message; this is a CLI
presentation limitation, not a false acceptance.

## Reproduction and trust boundary

```
.venv/bin/python tests/test_six_generate.py
.venv/bin/python tests/test_six_generate_review.py
```

Review output: `results/2026-09-30-six-generate-review/verification.json`;
log: `results/2026-09-30-six-generate-review.log`. The implementation uses
exact Python integers. It invokes the immutable reference for moduli at
most4096 and sparse interval/canonical calculations for larger moduli.
There is no search over all cardinalities or an n² Bloom parameter menu.
The finite proof tables must accompany generation; the selected embedded
certificates suffice for portable replay. No novelty assertion follows
from this executable review.
