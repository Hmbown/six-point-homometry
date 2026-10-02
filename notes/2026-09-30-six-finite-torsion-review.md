# Separate review of the bounded finite-torsion bridge

30 September 2026. Separate adversarial review by the six-integer reviewer.
**Accepted [PROVED], in-house, computer-assisted**, for the finite generating
table at 6 <= q <= 135 and its ordinary inflations. Together with reviewed
Corollary C2, this closes the rank-ten matching branch for arbitrary n.
It does not close positive-free-rank branches. No novelty claim.

Plan: audit both complete census traversals and exact signature packing;
check T/I representative coverage against independent Burnside counts;
attack the D, L2--L7 and generator certificate semantics; inspect the
completed all-edge replay and independently construct paths for missing
direct edges; prove each generator survives C2's ordinary inflation,
including the ambient-unit CRT step. Reuse the completed long replay.

## 1. Statement and dependencies

The reviewed manuscript is `notes/2026-09-30-six-finite-torsion.md`.
Its claim is graph connectivity by Bloom, rigid templates R, dyad grammar
D, and L2--L7, rather than a claim that every pair has one direct move.
That is the generating notion in PQ1. The proof depends on the previously
reviewed identities for these generators, on D1 and Theorem D in
`notes/2026-09-30-six-shadow-theorem.md` (attack in
`notes/2026-09-30-six-shadow-review.md`), and on C2 in
`notes/2026-09-30-six-completeness.md` (attack in
`notes/2026-09-30-six-cylinder-templates-review.md`). The finite table itself
does not require the new real-line classification.

I inspected both census implementations, the producer and full independent
certificate checker, the completed reports and replay log. I did not
duplicate the completed 728,351-certificate replay. Additional independent
checks are implemented in `tests/test_six_finite_torsion_review.py`, with
results and input hashes in
`results/2026-09-30-six-finite-torsion-review.json`.

## 2. Completeness and exactness of the census

**Gap traversal.** Every six-subset has six positive cyclic gaps summing
to n. A lexicographically minimal dihedral gap word begins with a minimum
gap g, where g <= floor(n/6). Enumerating all remaining gaps >= g and then
requiring minimality among all rotations and reversed rotations therefore
retains every T/I class. A repeated minimum or a stabilizer causes no
duplicate: a numerical gap word is enumerated once. Lexicographic gap and
anchored cumulative-point comparison agree, since their first difference
occurs at the same cumulative coordinate. Reversal together with all
rotations supplies every inverted anchored representative.

**Point traversal.** Every T/I class has a sorted representative containing
zero, and the code enumerates all five remaining increasing coordinates.
Any canonical rigid image can be anchored at one of the six points;
the twelve images obtained from both signs and six anchors suffice.
Comparing sorted tuples retains precisely one numerical canonical tuple,
including when the set has a nontrivial stabilizer. No unit equivalence is
taken in either traversal.

**Interval signatures.** Pair mode counts the fifteen unordered minimum
cyclic distances. Correlation mode counts memberships of x+d for each
d <= n/2. The latter counts an antipodal unordered pair twice, so its
2d=n entry is divided by two. Away from that entry each unordered pair
contributes exactly once to its minimum distance. Thus the two kernels
compute the same ICV by distinct procedures.

The packed representation is exact: eight one-byte sorted distances in
one 64-bit word and seven in another. At n <= 255 every distance is at
most 127. The five nonzero point coordinates each fit one byte. Shifts
are performed after unsigned conversion; the largest shift is 56.
Sorting by both full signature words may use a different order than
lexicographic distance order, but equality and grouping are unaffected.
There is no probabilistic hash equality. Record counts and payload sizes
through 135 fit the types and allocations used. Shared packing and sorting
remain ordinary executable-code dependencies, with their semantics checked
here rather than treated as an independent third enumeration.

As a third check on canonical-class coverage, I independently evaluated
Burnside's formula at all 130 moduli from 6 through 135. For rotation t,
put d=gcd(n,t), L=n/d: the number of fixed six-subsets is C(d,6/L) when
L divides six, and zero otherwise. For reflection x -> t-x, let f be its
number of fixed points (one for odd n; zero or two for even n). Its fixed
six-subsets number

    sum_j C(f,j) C((n-f)/2,(6-j)/2),

with inadmissible or nonintegral terms omitted. Dividing the sum over
all 2n group elements by 2n matches both census class counts at every n.
This does not alone verify the family partition, but is independent of
both representative-selection routines. Their complete family agreement,
the immutable-reference regressions and endpoint checks, and exact
signature reasoning jointly establish the claimed finite census.

All 130 checkpoints identify the currently audited C source hash
`7a227e2d6aabd0f4fa99fe370f962269a5cba936fcddfb55e6a2e7029e88ecf6`.
The prior reference checks cover 6..22 directly, inherited full agreement
through 24, previous independent census agreement at 12..60, and explicit
31..33 and 63..65 representation-boundary regressions. The source hash
ties the larger checkpoints to the inspected implementation; it is not
itself a correctness proof.

## 3. Are the recorded moves actual generators?

Write P=C*~W for the cross-correlation of a fixed block and moving block.
The replay reconstructs the aligned endpoint sets, block disjointness and
the exact Counter identities. The following potential gaps were checked.

* L2 checks that P is invariant under the recorded translation. L4 checks
  invariance of P+~P under the recorded nonzero half-turn. L5 checks the
  precise cross-correlation equality for W -> s-W. These are the sufficient
  group-ring identities of the corresponding generators, not merely an
  endpoint-ICV check.
* L3 uses tau_(-d)P=~P. To express the original co-symmetric swap, take h
  with 2h=-d. Then tau_h P is symmetric and the two blocks are h+V and
  -h+V. Such h exists automatically for odd n, and exactly when d is even
  for even n. The producer's parity guard is necessary and correct. The
  additional checker reconstructs h for every saved swap certificate.
* L7 tests subgroup orders 2,4,6,12. This is exhaustive for a six-set with
  half occupancy in every occupied subgroup coset: if the subgroup has
  order h and there are m occupied cosets, mh/2=6, so h is even and divides
  twelve. Exact half occupancy and coset-complement equality are checked.
* L6 records a genuine unit and verifies that it fixes the autocorrelation.
  A general unit action alone would not establish homometry; that missing
  condition is not a defect here because the replay explicitly checks it.
* Bloom and R certificates reconstruct their formula outputs, including
  R's torsion relation, and match the displayed endpoints after rigid
  normalization. Their previously proved formal identities apply.

**D requires more than finding equal-sum dyads.** Its replay has two removed
and two added points of equal sum, outside a common four-set. The four
corners are distinct: two equal-sum two-element sets sharing one point
coincide, which here would give identical aligned sets and hence identical
canonical endpoints. Those endpoints are different T/I classes. After
anchoring, the dyads are {0,a+b} and {a,b}.

The weight vector W=C+rho(C)+1_R is a nonnegative integer vector of mass
twelve, with the exact reflection and corner properties in Theorem D.
The replay checks (1-x^a)(1-x^b)W=0. Reviewed D1 then produces nonnegative
integer a-periodic and b-periodic weights, so this is indeed a certificate
of the parametric grammar D. As an extra check I explicitly constructed
such decompositions for a saved D certificate at every modulus containing
one: 82 decompositions. For each component of <a,b>, I intersected the
a-orbit and b-orbit partitions, subtracted the minimum in a fixed column,
and verified integrality, nonnegativity, periodicity and reconstruction.
These examples supplement D1's proof; they do not replace its universal
argument.

The discovery procedures need not be complete recognizers of all possible
individual moves. Their sufficient certificates and connectivity of each
entire finite family are enough for the stated finite-generation theorem.

## 4. Whole-table replay and compositions

The completed independent reconstruction report is
`results/2026-09-30-six-pair-mechanisms-review-135.json`, with completion
output in `results/2026-09-30-six-pair-mechanisms-tests135.log`.
It verifies every recorded move using integer Counters and the immutable
reference, verifies that certificates and missing edges partition each
family's complete pair set without duplicates, and uses union-find rather
than the producer's reachability routine.

| Quantity | Checked total |
|---|---:|
| Nontrivial families | 725,132 |
| Unordered pairs within those families | 728,424 |
| Direct certificates | 728,351 |
| Pairs without a direct certificate | 73 |
| Disconnected families | 0 |

The 728,351 certificates have labels D 398,642; L3 222,262; Bloom 59,211;
L7 18,018; L5 16,432; L4 13,101; R 561; L2 79; L6 45. At 6..11 there is
no nontrivial family. The largest family has five T/I classes.

The additional checker independently recounts the reports and uses BFS to
construct an explicit path, with intermediate vertices and move labels,
for each of the 73 absent direct edges. All paths use at least two
certified edges. They are saved in the additional review output. Thus
there is no inference from a high percentage of directly covered pairs
to full generation: every remaining pair has an actual composition.

## 5. Ordinary inflation, including ambient units

Reviewed C2 says that a rank-ten compatible signed matching has finite
universal presentation with torsion order bounded by 135, and the actual
anchored cyclic image lies in a subgroup H of order q <= 135. Since each
endpoint has six distinct points, q >= 6. Identify H with Z_q via the
injective embedding i(x)=(n/q)x in Z_n.

Injectivity transfers all group-ring identities, binary distinctness,
disjointness, subgroup-periodic weight vectors and occupied-coset
complements. Therefore Bloom, R, D and L2--L5/L7 paths embed edge by edge.
For L3 its witnessing h embeds as well; the ambient parity condition does
not introduce a new obstruction. Separate initial anchors are rigid
translations and do not change the relevant T/I classes.

For L6, given u coprime to q, choose u' congruent to u modulo q and
congruent to one modulo each prime p dividing n but not q. These moduli
are pairwise coprime, so CRT applies. No prime dividing q divides u';
none of the other primes dividing n does either. Hence gcd(u',n)=1.
Prime-power congruences are unnecessary for coprimality. Multiplication
by u' acts on H exactly as multiplication by u, preserves H and its
complement, and fixes the inflated autocorrelation. This is a valid
ambient L6 move. The additional test checks 38,920 such unit lifts over
q=6..135 and several multipliers with new prime factors.

Inflation also preserves the distinction of T/I classes. If nonempty
A,B subset H satisfy B=epsilon A+t in Z_n, select a matched point from
each side. Then t belongs to H, and the same equivalence already holds
inside H. Thus an embedded generating path does not lose a required
vertex by merging classes. As finite controls, one certificate from each
of the nine mechanism labels was inflated by 2,5,11; all 27 endpoint pairs
retain six distinct points, equal immutable-reference ICVs and T/I
inequivalence.

These arguments establish the claimed arbitrary-n rank-ten consequence.
They do not turn a census through 135 into an unrestricted arbitrary-n
classification: a pair whose compatible presentations have positive free
rank remains subject to the separate cylinder-branch analysis.

## 6. Reproduction, decision and limitations

Additional review command:

```bash
.venv/bin/python tests/test_six_finite_torsion_review.py
```

It passed in 4.37 seconds, checking all 130 class counts, aggregate table
contents, all 73 paths, all saved swap parity witnesses, 82 constructive
D decompositions, 38,920 unit lifts and 27 inflation controls. Its report
records hashes of the census and certificate inputs. The longer complete
certificate replay had already passed and was inspected, not rerun.

No mathematical repair was required. The manuscript can replace its
pending-review wording with the accepted finite-generation theorem and
C2 consequence, while retaining the positive-free-rank limitation.
This remains a computer-assisted proof relying on the stated finite
enumeration, exact checked certificates and previously reviewed algebra.
There is no Lean or small-kernel formal verification of the whole pipeline,
and no novelty conclusion.
