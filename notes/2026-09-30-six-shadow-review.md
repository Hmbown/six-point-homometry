# Independent adversarial review: six-note shadows and dyad grammar

30 September 2026. Fresh mathematical context, separate from the proof builder.
This attack covers `notes/2026-09-30-six-shadow-theorem.md`, §§1–7 including
the subsequently supplied §§6.1–6.2, and the dated shadow/shell certificates.
It does not determine novelty or certify unread literature attributions.

**Final verdict: ACCEPT the mathematical claims in their stated scopes.**
Theorem S, Lemmas S1–S3, the exact signed-matching obstruction, the Bloom
identity and direct-sum exclusion, Equation (D), Lemma D1, Theorem D,
the order-six generator, and Theorem H's three unbounded purely cyclic
families have survived this separate attack. They meet the
in-house **[PROVED]** written-proof/separate-review requirement. No arbitrary-n
classification of all six-pairs, small-prime sharp boundary, factor-menu
completeness, or novelty conclusion follows. The builder must apply any
status changes to the main ledgers; this reviewer has not edited them.

One wording repair was requested and applied during the attack: §6 now
explicitly says that the shell construction alone does not establish that
each output is non-shadow. No mathematical repair remains outstanding.

## Reproduction and independence

Startup: read `README.md`, `RESEARCH_PROGRAM.md`, `PROGRESS.md`,
`CONJECTURES.md`, `LITERATURE.md` and the operating instructions. The current
PROGRESS plan already authorized the separate attack. The immutable startup
suite passed all ten tests under the pinned environment.

```bash
.venv/bin/python tests/run_tests.py
.venv/bin/python tests/test_six_shadow_review.py \
  --out results/2026-09-30-six-shadow-review.json
```

The final review test passed all twelve groups in **6.878 seconds [COMPUTED]**.
Its implementations do not import `six_shadow.py`, `six_shell.py`, or
`six_explore.py`. Signed matching exhaustiveness uses a vertex-edge DFS of
the direct modular equations, rather than permutations of distance buckets.
Determinants use integer Bareiss elimination; ranks use Fraction Gaussian
elimination. Bareiss was itself checked against the Leibniz determinant on
120 matrices of sizes zero through five. Constructive lifts use Cramer's
determinants rather than the builder's adjugate. Smith rejection witnesses
are checked as direct integer row combinations without calling Smith form.
Shape alignments are independently generated from point-pair differences,
rather than all translations. The h=6 generator uses explicit reflection
orbits rather than the builder's coefficient-recovery function.

The trusted `src/homometry.py` supplies additional small-n ICV comparisons.
No protected reference file, `data/` file, ledger, or main proof was edited;
this review creates only its test, attack log, and dated result file. No
commit was made by the reviewer. `command -v lean` returned no executable;
this is an exact-arithmetic and written-proof review, not a formalization.

Reviewed proof SHA256:
`b04076c937b04f8004cd95b3931b741abe5be0b1003489ecad9148f262bf1050`.

Review test SHA256:
`a1bae86abb7208b5488bd8d6dff1cbf5d3bd3eb4bbd78cb62134936f90eef734`.

Review result SHA256:
`61c367743b45713b329a0f05053ba4f0ce32b17cb03879ccf79595629d53bed3`.
Individual source-payload hashes are retained in the result JSON. Later
status-only edits to the proof or payloads need not repeat the mathematics;
changes to statements, matrices, endpoints, or certificates require review.

## Attack 1: signed distance matching and incidence minors

**Targets:** repeated intervals, antipodal signs, dependence on chosen
orientations, and the determinant bound. **Verdict: ACCEPT [PROVED].**

Equality of ICVs gives equal cardinalities of the unordered-edge distance
buckets, including the antipodal bucket. For non-antipodal edges the sign
is forced once orientations are fixed; for antipodal edges both signs must
be enumerated. Keeping labelled vertices and permuting repeated-distance
edges is necessary, and the statement does this.

For S1, a square incidence submatrix has at most two nonzero entries in
each row. A row of size zero or one permits the proposed induction. If
every row has size two, its two entries remain opposite after a row sign
change, so the vector of all ones lies in the right kernel. There is no
missing third case. Further column removal and removal of the anchored
vertex do not invalidate this argument.

As a finite independent check, all **15,504 square subminors** of the
reduced K6 incidence matrix were enumerated: determinants were -1 in 1,840
cases, zero in 10,702, and +1 in 2,962 **[COMPUTED]**. Row permutations and
row sign changes preserve absolute determinants. S2's Laplace expansion
has exactly binomial(r,c) terms, each bounded by one. The constraints
r<=10 and c,r-c<=5 give the stated maximum 252. This is a safe bound;
neither sharpness nor realizability of determinant 251 is claimed.

## Attack 2: constructive lifting and the large-prime theorem

**Targets:** rectangular matrices, dependent unused rows, composite moduli,
negative determinants, full rank, and exact reduction. **Verdict: ACCEPT
[PROVED].**

The chosen r rows have rank r and therefore span the entire rational row
space. Their exact zero equations imply the exact zero equations for every
other row, even if the spanning coefficients are rational. The adjugate
construction is integral, and reducing its pivot coordinates gives
delta*v_P. Multiplying the entire vector by a modular inverse of delta
restores the required residues. The free coordinates are not reduced
incorrectly or solved only over Q. Rank zero is covered separately; a
rank-ten matrix with a coprime minor simply permits only v=0 modulo n.

Because 252 is composite, every prime dividing any nonzero determinant
of absolute value at most 252 is at most 251. Hence all prime factors of n
greater than 251 make the chosen minor coprime to n. The argument uses no
assumption that n itself is prime or bounded.

Independent Cramer lifts passed four generic cases and **32 modular Bloom
cases**: eight each for n=257, 263, 257*263=67,591, and 257²=66,049
**[COMPUTED]**. Selected minors included negative determinants and absolute
values through seven; ranks were eight or nine. Every lift was checked by
exact kernel equations, the prescribed residues, six distinct integer
coordinates on each side, and equality of the full integer directed
difference counters. Some coordinates exceeded 29 billion; the proof
correctly places no short-lift bound on them.

Restoring the separate anchors recovers the original residues. Distinct
residues guarantee distinct lifted points. An integer translation or
reflection would reduce to the same modular rigid motion, so T/I-distinct
modular inputs have nontrivial integer lifts. No integer classification is
needed for this implication.

## Attack 3: exact obstruction and misleading partial rejections

**Targets:** necessity, repeated distances, a single failed matching, and
the sufficiency-versus-necessity of the coprime-minor condition.
**Verdict: ACCEPT [PROVED].**

An integer kernel vector gives exactly matched signed integer differences,
and hence absolute differences. Conversely, an integer homometric lift
gives a bijection of equal absolute distances even when lengths repeat;
orienting those edges gives an allowed modular signed matching after the
actual lifted anchors are subtracted. Thus the stated quantifier over at
least one matching is exact.

The equation z=v+n*y gives M*y=-M*v/n, whose right side is integral.
For D=U*M*V, taking y=V*q converts this to D*q=U*(-M*v/n); nonzero diagonal
divisibility and zero-row vanishing are both necessary and sufficient.
The matrix-transform direction is correct.

Two deliberately hostile examples were retained **[COMPUTED]**:

* A=B={0,1,2,3,4,6} in Z12 has an obvious integer lift. Match identical
  edges but negate only the antipodal edge {0,6}. This valid modular
  matching has rank six; the other equations force corresponding anchored
  coordinates equal, while the negated edge forces both six-coordinates
  to zero over Z. That matching cannot lift residue six. The all-positive
  matching does lift. Therefore one failed matching cannot prove non-shadow.
* M=[2,3], n=6 has integer kernel vector (3,-2), although neither rank-one
  minor is coprime to six. The stronger certificate is sufficient, not
  necessary; the proof never asserts the false converse.

## Attack 4: Bloom identity and 2-by-3 direct-sum exclusion

**Targets:** incorrect parameters, specialization collisions, a hidden
integer classification assumption, and nontrivial factor flips.
**Verdict: ACCEPT [PROVED].**

The exact Bloom identity was checked in the free abelian group on p,q.
For an explicit readable certificate, orient each formal unordered edge
so its q coefficient is positive, or, when zero, its p coefficient is
positive. Both six-point lists have each of the following fifteen vectors
exactly once:

```text
(1,0), (2,0),
(-3,1), (-2,1), (-1,1), (0,1), (1,1), (2,1),
(-3,2), (-2,2), (-1,2), (0,2), (1,2),
(-2,3), (-1,3).
```

Their full directed difference tables therefore consist of these vectors,
their negatives, and coefficient six at the origin: 31 support terms.
Arbitrary substitution preserves this identity. Only after checking that
each modular list has six distinct residues may the polynomial be regarded
as a six-subset indicator. Arbitrary integer lifts of p,q keep the six
coordinates distinct under that same modular distinctness condition.
Completeness for repeated-distance integer sets is correctly withheld.

For A=P+Q with P={u,v}, -P=P-(u+v). Thus flipping P translates A, while
P-Q=(u+v)-A is a reflection of A. A 0/1 direct sum has multiplicative
cardinality, so nontrivial cardinality-six factors have sizes two and three.
Singleton factors cause only translations/reflections. This works equally
in Z and Z_n and does not exclude signed or canceling factors. Exhaustive
normalized modular products for n=6..14 gave **1,854 collision-free products**
and no nontrivial direct-sum output **[COMPUTED]**.

## Attack 5: dyad identity, unit steps, and non-unit failure

**Targets:** the sign/monomial in (D), the kernel claim, nonnegative mass,
and whether the unit hypothesis can be silently dropped.
**Verdict: ACCEPT [PROVED].**

Equation (D) was independently expanded in a free abelian group on
a,b,c1,c2,c3,c4; both sides have the same 36 signed support terms.
The factor is x^(-a-b), and the reflected common part is x^(a+b)*C~;
neither sign is reversed.

For gcd(a,n)=1, 1-x^a vanishes only at the trivial character. That character
is already a zero of 1-x^b, so multiplying the factors adds no zero
characters. The invertible DFT makes their kernels equal over C and hence
on integer vectors. Periodicity along a b-orbit of length h and integer
coefficients imply mass twelve is divisible by h. Repeated coefficients
or intersecting reflected common sets do not invalidate the mass count.

All **56,396 admissible shapes for n=8..14** were independently checked;
**1,876 are homometric [COMPUTED]**. Direct autocorrelation equality agreed
with the mixed-difference equation in every case. The unit-step iff
b-periodicity held whenever the unit hypothesis applied.

A counterexample to dropping that hypothesis is retained: in Z8, a=4,
b=1, C={2,3,6,7}, the sets {0,2,3,5,6,7}/{1,2,3,4,6,7} are homometric,
but W=(1,1,2,2,1,1,2,2) is not b-periodic **[COMPUTED]**. This example
need not be T/I-distinct to refute the unrestricted kernel equivalence.

## Attack 6: D1 and complete grammar for the displayed shape

**Targets:** integer/nonnegative decomposition, incomplete coset grids,
zero steps, fixed points of reflection, and hidden alignment assumptions.
**Verdict: ACCEPT [PROVED].**

The DFT proves that the complex kernel of the product is the sum of the
two periodic subspaces; taking real parts is valid because W is real.
In each <a,b>-coset, an <a>-coset and a <b>-coset intersect because
<a>+<b>=<a,b>. Thus there are no missing cells in the stated grid.
The cell values are additive. Subtracting the minimum in an anchor column
and putting it into the column component produces nonnegative integers;
V_j is exactly min_i w_ij. This does not assume an integral Fourier split
or round a real split to integers.

Summing complete orbits gives (M). If h_a>12, any positive U orbit alone
would have mass greater than twelve, so U=0. At least one order is at most
twelve because W has positive mass and U,V are nonnegative. The statement
does not incorrectly infer that both orders divide twelve in the general
case.

As an additional edge-case attack, all **33,897 choices** of n=1..6,
a,b in Z_n, and coefficients W(x) in {0,1,2} were checked against direct
mixed differences. Exactly **11,493 admit the required decomposition**,
and existence agrees with the kernel condition in every case **[COMPUTED]**.
This includes a=0, b=0, coincident steps, singleton groups, and zero mass.

Theorem D's reflection conditions are exact. Corners have coefficient one;
outside corners a two-point orbit with coefficient zero, one, or two
admits respectively neither, either one, or both points of C. At a fixed
point only coefficients zero and two are possible. The mass condition
then forces |C|=(12-4)/2=4. These conditions recover every binary C of
the original shape, including repeated intervals and non-unit steps.
They do not merely select a convenient subclass of the displayed shape.

Keeping A fixed during relative-alignment recognition loses no cases:
apply the inverse of A's rigid motion to both aligned sets. A four-point
intersection and equality of the two swapped-point sums are preserved
by the common translation/reflection. Theorem D expressly withholds
completeness of which arbitrary six-pairs can be so aligned.

## Attack 7: order-six shell, fixed points, and displayed examples

**Targets:** collisions, orbit count, lack of a unit step, nontriviality,
and the claimed translated endpoints. **Verdict: ACCEPT [PROVED].**

With a outside H=<b>, S has twelve points and the four corners are distinct.
Reflection exchanges H and a+H, so in fact it cannot have a fixed point
in S. Its restriction to S minus the four corners has four two-point
orbits. Selecting one point from each gives C+rho(C)=1_(S minus R), and
therefore W=1_S. Periodicity directly proves homometry without gcd(a,n)=1.
The T/I filter remains necessary: there are trivial raw outputs.

All **2,880 parameter/reflection choices** for n=12,18,24,30,36 passed
exact autocorrelation checks; 2,520 raw outputs are T/I-distinct, counted
with parameter multiplicity, and 1,152 small-n outputs also agree with
the reference ICV **[COMPUTED]**. These are test-case counts, not counts
of distinct classes. The n18 displayed A,B require common translation
by six; the n24 displayed A,B require common translation by eight.
Both endpoint pairs, ICVs, and T/I distinctions are independently verified.
The n18 example has a 2/4 H-coset distribution, so the half-per-coset
hypothesis mentioned in §6 indeed fails for it.

The initial phrase separating the shell mechanism "from integer shadows"
could have suggested disjointness of mechanisms without a proof. The
builder applied the requested explicit sentence: construction alone does
not establish that each output is non-shadow. This repair is accepted.

## Attack 8: exhaustive non-shadow certificates

**Verdict: ACCEPT the six named purely-cyclic decisions [COMPUTED].**

Every signed matching is generated by the independent direct-equation DFS.
Supplied certificates contain each matching exactly once, with no
duplicate-padding or omitted antipodal sign. Every matrix is reconstructed
from its labels, every modular equation is checked, every stored rank is
independently eliminated, and every selected minor is independently
evaluated and checked against its sharper binomial(r,c) bound.

| n | A | B | All matchings | Rank(s) | Minor determinants |
|---|---|---|---:|---|---|
| 17 | {0,1,3,8,12,14} | {0,1,4,6,12,14} | 192 | 10 | +/-17 |
| 18 | {0,1,4,6,10,13} | {0,1,4,7,9,13} | 384 | 9 | +/-6 |
| 19 | {0,1,4,6,12,15} | {0,1,4,7,9,15} | 96 | 10 | +/-19 |
| 21 | {0,1,3,7,10,15} | {0,1,4,7,14,16} | 48 | 10 | +/-21 |
| 23 | {0,2,4,6,11,14} | {0,2,4,8,11,13} | 48 | 10 | +/-23 |
| 31 | {0,2,4,7,16,25} | {0,2,4,9,12,18} | 4 | 10 | +/-31 |

In rank ten the integer kernel is zero and cannot lift the nonzero anchored
coordinate vector. In every n18 certificate the stored integer row
combination produces coefficients divisible by six, but a right side
not divisible by six. For example, the first row combination gives
coefficients (0,0,0,0,0,0,0,-6,-6,6) and right side one, requiring
6*(-y_7-y_8+y_9)=1. This is an exact impossibility witness independent of
Smith form. All 384 such witnesses pass. Thus rank deficiency is not
mistaken for liftability, and none of these conclusions rests on a cap
or on one convenient matching.

## Attack 9: shell certificates and coverage through sixty

**Verdict: ACCEPT the new shell evidence [COMPUTED], relative to the
supplied census and saved menu labels.**

Every dated shell payload for n=12..60 was independently checked. The
**22,921 certificates** have valid distinct endpoints, exact rigid
alignments, four distinct corners, binary common sets of size four,
the correct W, nonnegative integer U,V, the stated periodicities and
orders, mass twelve, and exact reflection conditions. Independent
point-pair alignment searches of **all 32,106 inventory pairs** reproduce
exactly the supplied shape pairs, so this checks omissions as well as
positive soundness. All supplied family ICVs are recomputed; through n24
they also agree with the reference ICV.

The independent reflection-orbit generator reproduces every distinct h6
edge through sixty, with none missing from the shape inventory. Each
stored h6 witness is independently checked against its subgroup, cosets,
reflection, and canonical endpoints. Every saved menu-gap shape pair is
h6-generated. The named counts agree:

| n | Saved strict+Bloom gap pairs | Dyad/h6 gap pairs generated |
|---|---:|---:|
| 18 | 3 | 3 |
| 24 | 7 | 3 |
| 30 | 14 | 6 |
| 36 | 6 | 6 |
| 42 | 22 | 9 |
| 48 | 13 | 9 |
| 54 | 30 | 12 |
| 60 | 20 | 12 |

All saved disconnected families have two members, so their family-gap
labels also label their unique missing pair; this is explicitly checked.
The audit does not independently recompute the older strict-menu moves or
upgrade their legacy completeness/coverage status. These gap counts remain
relative to those saved labels, not proofs of all-menu sporadic families.
The census itself is supplied by the two earlier census methods; this
review is not a third exhaustive enumeration of every six-subset.

## Attack 10: three unbounded purely cyclic parameter families

**Targets:** incorrect shell translations, parameter-dependent extra
matchings, hidden unit or coprimality restrictions, exceptional T/I
equivalences, and an unjustified extrapolation from n18.
**Verdict: ACCEPT Theorem H [PROVED], with its finite computer-assisted
certificate dependency explicitly retained.**

Each displayed six-tuple is strictly sorted, consists of distinct points,
and lies in [0,6m) when 0<a<m/2. The translated common sets in the proof
are correct: subtracting 2m in types 1 and 2 gives the stated C' and
corners {0,a,m,a+m}; subtracting 5m in type 3 gives C'={m,a+m,2m,4m}
and corners {0,5m,a+5m,a+4m}. Their stated reflections partition the
same twelve-point two-coset shell. Independently, all three formal
autocorrelation identities were checked in Z times Z6, with a the free
coordinate and m of formal order six. This is a universal substitution
certificate, not a sample assertion of homometry.

The written gap-word arguments are valid. Types 1 and 2 have a unique
smallest gap a; aligning it leaves differing third entries, and reversal
leaves differing second entries. Type 3 has a unique largest gap 2m;
after aligning it, X's second entry is a and Y's is m, while reversing
X gives second entry m-a. These inequalities are strict. No division by
a unit, gcd(a,m)=1 assumption, or numerical genericity is needed.

The stable-matching lemma survives the main attack. Every edge difference
has a-coefficient -1, zero, or one; the displayed vertex order is constant.
Folding it gives exactly one of the nine stated bins. Their strict order
follows from 0<2a<m, so bins cannot merge anywhere inside this chamber.
Only the 3m bin is antipodal. Both signs there remain included. A residue
matching at any chamber parameter therefore has exactly the same labelled
edges and signs as at the prototype; there are no additional exceptional
matchings at special rational values of a/m. The excluded boundary
a=m/2 would merge bins and is not licensed by this proof.

The independent check additionally compared all **450 edge/edge/sign
compatibilities per type** with their formal coefficient condition
delta_a=0, delta_m divisible by six. This exactly agrees with the prototype
modular compatibility graph. Each edge's folded coefficient pair was
checked against the nine-bin list. The resulting independent DFS confirms
**384 signed matchings for each type**, and the two additional prototype
files `shell_type2_n18.json` and `shell_type3_n18.json` pass the same full
rank/minor/row-witness audit as type 1. All three prototypes have rank nine
for every matching.

For every one of the **1,152 matrices**, the independently reconstructed
matrix annihilates the stated v_a exactly, M*v_m has every entry divisible
by six, the supplied integer row combination has every coefficient of
c*M divisible by six, and -c*M*v_m/6 is not divisible by six. The ten
coefficient vectors in the proof agree with the formulas. Witness
remainders are:

| Type | Remainder one modulo six | Remainder five modulo six |
|---|---:|---:|
| 1 | 144 | 240 |
| 2 | 96 | 288 |
| 3 | 0 | 384 |

These are exact symbolic row identities **[COMPUTED]**, not floating point
Smith data. For arbitrary parameter values, M*(a*v_a+m*v_m)/(6m) is exactly
M*v_m/6. Hence the same impossible integer congruence rejects every
matching for every allowed a,m. The exact-obstruction theorem then excludes
all integer homometric lifts, including lifts with arbitrary coordinates
or a different integer point order. Labelling points by residue order
does not assume that the lifted integer coordinates are sorted.

As supplementary checks, each type was evaluated at **603 parameter
choices**: every allowed integer a for m=3..50, plus large-modulus and
inflated cases with m=1,000,003 or 1,000,008. All points, strict bins,
autocorrelations, and dihedral gap-word distinctions pass **[COMPUTED]**.
The universal non-shadow proof is the invariant-matching and exact-row
argument above, not extrapolation from these samples. Parameters with
gcd(a,m)>1 remain covered; dividing by that gcd describes ordinary
inflation without altering the obstruction. The theorem does not assert
that every h6 output is non-shadow or that the three templates exhaust
six-note relations.

## Remaining review boundaries

No mathematical defect remains in the reviewed statements. Key limitations
are retained explicitly: Theorem S gives a sufficient small-prime support
bound, not its sharp value; Theorem D is complete only for the displayed
parallelogram-dyad shape; no all-six-note grammar or repeated-distance
integer classification is claimed. The selected non-shadow pairs and
three unbounded templates do not
classify all non-shadow pairs. New six-only evidence cannot repair the
inherited single-method all-cardinality n38..40 census, the old factor
support cap, or the global kappa definition defect. Literature novelty
searches and unread primary attributions remain the builder's separate
responsibility; a human mathematician should review these results before
public sharing.
