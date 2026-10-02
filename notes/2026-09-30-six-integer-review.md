# Fresh adversarial review: real/integer six-point classification

30 September 2026. Reviewer: separate fresh-context agent from the builder.
No novelty claim and no new literature dependency.

## Verdict and scope

**[PROVED], computer-assisted, in-house:** Theorem I and its integer-parameter
conclusion in `notes/2026-09-30-six-integer-theorem.md` pass this adversarial
review. All noncongruent real six-point homometric pairs, including repeated
distances, have exactly one of the two stated normalized forms. The statement
is not conditional on a coordinate, denominator, or diameter bound.

**[PROVED], with the same computational qualification:** Theorem Iw passes
for noncongruent multisets of total multiplicity six. Its only support-collision
case, up to the stated rigid motions and common scaling, is

    {0,1,3,3,7,8} / {0,2,4,7,7,8}.

**[PROVED], dependent on I:** for a cyclic six-note Z-pair, membership in the
complete modular Bloom image is equivalent to being an integer shadow.

These conclusions trust exact SMT solvers and their arithmetic/proof checking.
The original encoding was checked using Z3 and cvc5; this review supplies a
different encoding and cvc5 run, with eager internal proof checking and saved
proofs. There is no Lean proof or separately executed small proof kernel.
Human mathematical review is appropriate before public presentation.

**Scope warning required by the mathematics:** Iw excludes congruent line
multisets. Distinct cyclic/cylinder configurations can project to equal or
reflected line multisets, including multisets with at most four support
positions. Iw does not remove or classify that branch. No complete cyclic
six-note classification follows from this review alone.

## Plan and startup

The parent recorded the full-six continuation plan in `PROGRESS.md` before
this assigned review. The reviewer read README, RESEARCH_PROGRAM, PROGRESS,
CONJECTURES and LITERATURE in the prescribed order, then ran the pinned
immutable startup suite: all ten tests passed.

Review plan: independently derive the normalization and multiplicity semantics;
attack the explicit parameter planes and degeneracies; build a separate
unbounded exact model; compare against an exhaustive integer search; inspect
the full written proof and its saved evidence. Initial compute estimate was
seconds for diameter 40 and up to 60 seconds per solver attempt. No shared
ledgers, protected files, builder code, or inherited jobs were changed.

## 1. Normalization, equivalence and repeated distances

Let the increasing list be `0=a0 <= a1 <= ... <= a5=L`, with strict
inequalities for Theorem I. For every edge other than `(0,5)`, either its
right endpoint is at most a4, or its left endpoint is at least a1.
Consequently the largest remaining distance after deleting one occurrence
of L is exactly `max(a4,L-a1)`. This argument still works if there are
additional diameter occurrences, repeated interior coordinates, or ties.

Reflection exchanges those two endpoint distances. Independent reflection
of A and B therefore gives the common a4=b4=r. This is a choice of rigid
motion for each member of a homometric pair, and is legitimate. Neither a
strict choice nor uniqueness of the choice is assumed in the reduction.

The resulting coordinates have the same first, penultimate and last values.
If the sets are not equal, lexicographic order of the first three interior
coordinates orders the pair. Reflection congruence is exactly the equality
of A with the reversed complement of B; the builder excludes every component
of this equality together. Translation congruence was already reduced to
literal equality by setting both minima to zero. There are no further line
isometries to exclude.

The builder's count encoding queries each A-edge value, with one term per
edge occurrence. Equal multiplicities at every A-support value use all 15
occurrences in B, so B cannot contain a new value. This is a valid exact
multiset equality test even when distances repeat. In the weighted case,
zero distances remain in the 15 occurrences. Directed autocorrelation has
twice these off-diagonal zero occurrences plus six diagonal occurrences;
thus the weighted interpretation is consistent.

## 2. Plane exclusions, parameter conditions and uniqueness

The builder's Cramer-rule equations describe the full span of its two
coefficient columns: the pivot determinant is a nonzero integer constant,
and each output row is imposed. Repeated r and diameter coordinates are
substituted in the appropriate positions. No parameter quantifier is
silently dropped. This excludes exactly the stated planes, rather than a
larger affine set.

I independently checked the formal coefficient multisets of all 15 positive
differences in each ordered normal form. They agree identically. The gap
inequalities in the proof are correct; the early draft's I.1 B-gap typo was
corrected before the final review. Its first-gap and reflected-first-gap
arguments establish noncongruence throughout both parameter chambers.

In the strict case, the last gap is smaller than the first gap of both
sets in either form. Thus the reflection normalization is unique. The
first gap of A is smaller than that of B, fixing pair order. The normalized
A2 coordinate lies in `(1/3,3/8)` for I.1 and `(3/5,5/8)` for I.2, so the
two planes have no admissible common point. The displayed coordinate
formulas recover p and q uniquely. The final proof includes this argument.

After undoing diameter scaling, I.1 gives `p=A5-A4`, `q=A2`; I.2 gives
`p=A4-A3`, `q=A1+p`. These are integer differences/sums for integer sets.
The use of diameter one inside the solver does not imply that the final
integer parameters are normalized fractions.

For weak gaps, I.1 allows p>=0 and q>=3p. The p=0 case makes the lists equal,
so noncongruence requires p>0. I.2 allows p>=0 and 3p/2<=q<=2p;
p=0 contradicts positive diameter and q=2p makes the lists equal.
Only q=3p in I.1 and q=3p/2 in I.2 create support collisions. The two
boundary descriptions are related by reflecting A, so the weighted theorem
correctly says "one of" rather than claiming unique normalized type.

## 3. Independent unbounded encoding

`tests/test_six_integer_review.py` imports none of the builder's classification
or SMT modules. It uses five consecutive gaps per set,

    (x0,x1,x2,x3,t), (y0,y1,y2,y3,t),

with each sum equal to one, and `x0>=t`, `y0>=t`. Strict or weak gap
positivity gives the two domains. Lexicographic gap order is equivalent to
lexicographic coordinate order at the first differing gap. Reflection is
reversal of the gap list.

The three edge occurrences `(0,4),(0,5),(4,5)` have common distances
`1-t,1,t`. They can be cancelled from both multisets even when their values
also occur elsewhere. Each of the twelve remaining A-edge occurrences
chooses a B-edge occurrence of equal distance using Boolean variables.
Every A row chooses at least one column, and a column is chosen by at most
one row. With twelve rows and columns this is a bijection. Thus repeated
values are handled by matching distinct occurrences; no collision-free
assumption or builder multiplicity-count expression is used.

The excluded planes are expressed directly in gaps, independently of the
builder's Cramer routine. For I.1 these equations are

    x1=2t, x2=x0-t, x3=x0+3t,
    y0=x0+t, y1=2t, y2=x0+2t, y3=x0-t.

For I.2 they are

    x1=2x3, x2=2x0-x3, t=x3-x0,
    y0=x3, y1=2x0, y2=2x3-x0, y3=2x0-x3.

Substituting `p=t,q=x0+2t` or `p=x3,q=x0+x3` proves exact correspondence
with the theorem. The positivity/domain restrictions imply precisely its
open or closed parameter conditions.

The strict model needs no matching symmetry reduction. For the weighted
run, equal-valued A occurrences are required to match B indices in increasing
order. This preserves existence: within each common distance value, sort
the A indices and B indices and pair them in order. Auxiliary real index
variables are forced by selected Boolean edges to their literal integer
indices; no integrality assumption is needed.

**[COMPUTED]** cvc5 1.4.1 returned UNSAT for both independent encodings,
with `produce-proofs=true`, `check-proofs=true`, `proof-check=eager`:

| Domain | Time including proof export | Uncompressed proof bytes |
|---|---:|---:|
| Strict six-point sets | 4.841 s | 10,881,375 |
| Weak six-atom multisets, ordered equal occurrences | 10.900 s | 24,459,075 |

Native printed proofs end in false and contain no rule whose printed name
includes `trust`; the rule inventory is saved. This inspection is not an
independent validation of every inference. Exact solver implementations
remain part of the trusted computation.

## 4. Controls, finite attack and shadow corollary

The independent model accepts the diameter-17 collision-free example and
diameter-11 repeated-distance example before plane exclusion, and rejects
both afterward. It admits points outside the planes when homometry is
removed and rejects a fixed nonhomometric perturbation. Separate weighted
controls accept the five-support boundary pair before exclusion and reject
it afterward. Eight translation/reflection/swap controls pass.

**[COMPUTED]** exhaustive integer line enumeration through diameter 40 visits
330,144 translation/reflection classes and finds 39 noncongruent pairs,
including eight pairs with repeated distances. Every pair fits exactly one
normal form. The class count independently equals Burnside's expression

    sum_(L=5..40) (binom(L-1,4)+binom(floor((L-1)/2),2))/2.

An independent parameter loop generates exactly the same 39 pairs. For
every enumerated pair, immutable `homometry.icv` agrees at modulus `2L+1`,
where all positive line distances remain their own interval classes.

**[COMPUTED]** weak integer enumeration through diameter 20 visits 26,817
reflection classes and finds nine pairs, two with support collisions
(diameters 8 and 16). All have at least five support positions and the
colliding pairs are exactly the stated boundary shape. Burnside counting
checks the class total, and a separate closed-parameter loop produces the
identical pair set. These finite searches are attacks and controls, not
the proof of unbounded completeness.

The classical Bloom coefficient lists have identical formal directed
autocorrelations, checked separately. I.1 is `(3q-p)-Y,(3q-p)-X`;
I.2 is `(3q-p)-X,Y`, as unordered coefficient lists. Both substitutions
were checked exactly. Integer lifts of a cyclic Z-pair cannot be line
congruent, since line congruence reduces to cyclic congruence. Applying I
to shadow lifts therefore yields integer Bloom parameters. Conversely,
an admissible modular Bloom pair has six distinct residues in each member,
so every integer parameter lift has six distinct integer terms. The
formal autocorrelation identity proves their line homometry. This verifies
both directions of the shadow decision corollary, including arbitrary
modular parameter representatives.

## 5. Reproduction, artifacts and failures

The pinned cvc5 wheel is an isolated dependency at `/tmp/babbitt-six-cvc5`,
version 1.4.1; it is not part of the checked-in source environment. It can
be restored using the builder's documented isolated install command.

```bash
.venv/bin/python tests/run_tests.py
.venv/bin/python tests/test_six_integer_review.py --timeout 60
.venv/bin/python tests/test_six_integer_review.py --weighted --order-matches --out results/2026-09-30-six-integer-weighted-review-ordered --timeout 60
```

Strict artifacts are in `results/2026-09-30-six-integer-review/`;
weighted artifacts are in
`results/2026-09-30-six-integer-weighted-review-ordered/`.
Each has the complete SMT input, compressed native cvc5 proof and result
metadata. `artifact-audit.json` checks proof/input hashes and inventories
rules. `final-exact-checks.json` records the final formal/finite checks and
hashes of the reviewed proof/source files. Regeneration of both saved SMT
inputs from the final reviewer script is byte-for-byte identical.

Strict input SHA256:
`83b1adbd474d376eb6f02ab6e3b826e96db419f325c4ba75804f6b47013f2b00`.
Weighted input SHA256:
`e8a9bcf7c94c9f3c8c352b92ea8a22a48872cd723463a6d2bdbe61740cbccb30`.

Failures retained honestly:

1. The first strict run reached proof export, but the wrapper expected text
   while cvc5 returned bytes. No result was promoted from that failed wrapper.
   Decoding the proof and rerunning produced the saved successful result.
2. The initial weak Boolean model without equal-occurrence ordering ran
   beyond 160 seconds despite a 60-second per-query option. It was terminated;
   its input remains in `six-integer-weighted-review/`. It produced no saved
   solver verdict and is not evidence either way. The justified occurrence
   ordering produced the successful independent weak certificate above.
3. The builder's separate sorting-network timeout is recorded in its proof
   note. This review makes no completeness inference from that timeout.

No protected reference/data files were edited. No literature novelty search
was performed by this reviewer; the existing logged literature scope and
access gaps remain in force. This verdict accepts a computer-assisted
classification in the stated line/multiset scope, not a claim of novelty.
