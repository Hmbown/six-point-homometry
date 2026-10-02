# Six-note shadows and the bounded torsion obstruction

Codex, 30 September 2026. PQ1/P3, cardinality six. **[PROVED], in-house:
full written proof and separate fresh-context adversarial review completed.
No novelty claimed.** Theorem H's non-shadow part is computer-assisted,
with every finite certificate independently checked. The attack and its
limits are logged in [the separate review](2026-09-30-six-shadow-review.md).
This is a partial structural result, not an arbitrary-n six-note classification.

## 1. Statement

**Theorem S (bounded torsion).** Let A and B be homometric six-subsets of
Z_n. If every prime divisor of n is greater than 251, there are homometric
six-subsets A', B' of Z whose reductions modulo n are exactly A and B.
If A and B are T/I distinct, A' and B' are distinct up to integer translation
and reflection. Thus every six-note Z-relation at such n is an integer shadow.
In particular this holds for every prime n >= 257, and for arbitrary products
and powers of primes >= 257. No bound on n itself is needed.

**Stronger certificate version.** Match the fifteen unordered edges of A to
those of B with equal cyclic distance, choosing signs so their oriented
differences agree modulo n. Anchor one vertex in each set at zero, producing
the 15 by 10 integer matrix M described below. If one nonzero maximal-rank
minor of M has determinant coprime to n, that matching gives an integer lift.
Every such determinant has absolute value at most 252.

**Exact obstruction.** A pair is an integer shadow if and only if, for at
least one such signed edge matching, its anchored coordinate vector modulo n
is the reduction of an element of ker_Z M. Failure of a single matching or
a bounded lift search does not prove the pair purely cyclic. Smith normal
form decides the condition for a matching; exhausting all matchings decides
it for the pair. This is a diagnostic and lifting algorithm, not a small
generation grammar.

The theorem says nothing about completeness of a factor menu, the existence
of an integral factor flip in Z[Z_n], or whether a particular short lift works.
The lift can have large coordinates. Such distinctions matter even at prime n.

## 2. Matching matrix

Write A={a_0,...,a_5}, B={b_0,...,b_5} with distinct residues, and translate
each set separately so a_0=b_0=0. Equality of ICVs gives a bijection sigma
between their fifteen unordered edges. For each matched pair of edges choose
epsilon in {+1,-1} with

    a_j-a_i = epsilon (b_l-b_k)  (mod n).

There is one choice unless the distance is n/2; for an antipodal edge both
choices must be allowed. The corresponding row of M is

    (e_j-e_i | -epsilon(e_l-e_k)),

where the anchored coordinates e_0 are omitted from each five-column block.
Thus M=(D_A | D_B), with each block a row-signed, reduced graph incidence
matrix. There is no quotient by unit multiplication: vertices label the
actual T/I representatives, and units only transport a certificate to a
different pair.

## 3. Incidence minors and the bound

**Lemma S1.** Every square submatrix of a row-signed reduced incidence
matrix has determinant 0, +1 or -1.

Proof by induction on its size. A zero row gives determinant zero. If a row
has exactly one nonzero entry, it is +/-1; expansion along that row reduces
to a smaller submatrix. If every row has two nonzero entries, they are +1
and -1. The sum of the columns is then zero, so the matrix is singular.
These exhaust the possibilities, including submatrices obtained by omitting
the anchored vertex or further columns. The empty determinant is one. QED.

**Lemma S2.** Every r by r minor of M, using c columns of D_A and r-c of
D_B, has determinant with absolute value at most binomial(r,c). In
particular every nonzero maximal-rank minor has absolute value at most 252.

Expand along the c columns from D_A. There are binomial(r,c) summands.
Each is a signed product of a c by c incidence minor and an (r-c) by (r-c)
incidence minor, so by S1 its absolute value is at most one. Now r<=10 and
0<=c<=5, 0<=r-c<=5. The largest binomial coefficient allowed is
binomial(10,5)=252. QED.

## 4. Constructive lifting proof

**Lemma S3.** Let M be any integral matrix of rank r, and let v modulo n
satisfy Mv=0. If M has a nonzero r by r minor N with det(N)=delta and
gcd(delta,n)=1, v is the reduction of an integer element of ker M.

Reorder columns into pivot columns P and free columns F so N=M[R,P]
for some r rows R. Choose integer representatives f of v_F. Define the
integer vector w by

    w_F = delta f,
    w_P = -adj(N) M[R,F] f.

Then M[R,:]w=0, since N adj(N)=delta I. The rows R span the row space
of M over Q, so Mw=0 on every row, exactly over Z. Reducing modulo n,
the selected row equations for v give

    N v_P = -M[R,F] v_F.

Multiplication by adj(N), with invertibility of delta modulo n, shows
w_P = delta v_P modulo n; w_F = delta v_F modulo n as well. Choose an
integer t with t delta=1 modulo n. Then z=t w is an integer kernel element
with z=v modulo n. The rank-zero case is immediate. QED.

**Proof of S.** Choose any signed matching and its matrix M. Its rank is
at most ten. A nonzero maximal-rank minor exists and by S2 has determinant
delta with 1<=|delta|<=252. Every prime dividing delta is therefore at most
251. Under the theorem's hypothesis gcd(delta,n)=1, so S3 gives an integer
coordinate vector z reducing to the anchored sets. Restoring their separate
translations gives A', B' reducing exactly to A, B. Distinct residues force
each lifted set to have six distinct integer points. Every matched edge now
has exactly equal signed differences, hence equal absolute lengths, over Z.
The fifteen matched lengths give integer homometry. An integer rigid motion
between the lifts would reduce to a T/I equivalence between A and B, which
is excluded for a Z-pair. QED.

**Proof of the exact obstruction statement.** An integer kernel vector with
the prescribed residues gives the lift by the same matched-length argument.
Conversely any integer homometric lifts determine a bijection of their
fifteen absolute lengths, with signs. Reduce that bijection modulo n and
anchor the actual integer points representing a_0,b_0 by subtracting them.
The resulting vector is in ker_Z M and reduces to the anchored input vector.
This includes repeated lengths and antipodal residues. QED.

For implementation, write an integer representative v and seek z=v+n y.
This is equivalent to M y=-Mv/n over Z. The RHS is integral because the
matching satisfies Mv=0 modulo n. If D=U M V is a Smith decomposition,
solve D q=U(-Mv/n) by divisibility of each nonzero diagonal entry and
vanishing on zero rows, and set y=V q. This gives an exact lift or an exact
rejection for this matching, without a search bound on lifted coordinates.

## 5. Explicit integer mechanism: the classical Bloom family

For integers p,q, put

    X={0,p,q-2p,2q-2p,2q,3q-p},
    Y={0,p,q+2p,2q-p,2q+p,3q-p}.

Their directed difference multisets agree identically in the free abelian
group on p,q. Here is a signed factor proof. In Z[u^+/-1,v^+/-1] set

    F=1+u+v,     Q=u^2+uv^2-uv+v,
    R=u^2 v-uv+u+v^2 = u^2 v^2 Q~.

Expansion gives X=u^-2 FQ and Y=u^-1 FR. Therefore XX~=FF~ QQ~=YY~.
The substitution u=x^p, v=x^q proves the stated identity. It explains why
six points are possible despite the ordinary 0/1 2-by-3 flip exclusion:
Q is signed, and cancellation reduces the product to six positive terms.
Independent tests also check the free two-variable coefficient table. The
identity therefore survives substitution of arbitrary residues p,q in Z_n.
If both lists have six distinct residues they are homometric sets. They form
a Z-pair exactly when their T/I canonical forms differ. These are explicit
congruence/exclusion conditions, not a spectral existence assertion.

For any admissible modular parameters, choose arbitrary integer lifts of
p,q. Distinct residues ensure the six terms remain distinct as integers;
the group-ring identity gives integer homometry. Thus every such generated
pair is a shadow. No assertion here says these are all integer six-pairs
when distances repeat.

This family is classical: Postpischil and Gilbert, Experimental Mathematics
3(2) (1994), 147-152, §3 (primary source read), and the Yovanof-Golomb 1998
polynomial paper. Bekir-Golomb 2007 is not promoted from a secondary citation
to a read proof. The collision-free classification is stated and discussed
in Ranieri et al., arXiv:1308.3058v2, §IV.A/Theorem 1; that discussion does
not reproduce Bekir-Golomb's proof. Consequently we do not use its completeness
as an unverified dependency in Theorem S.

There is also a useful six-note exclusion: a nontrivial 0/1 direct-sum
factorization has factors of sizes two and three. Every two-element set is
a translate of its reversal. Flipping either factor therefore gives a
translate or reflection of the original product. A 0/1 direct-sum flip
cannot by itself give a genuine six-note Z-pair, in Z or in Z_n. Signed
factors, cancellation, complements, and composites remain available.

## 6. Cyclic cancellation with a six-note shell

The following exact restricted classification helps explain the free cyclic
families, including the three strict-menu gaps at n=18.

Take A=C disjoint-union {0,a+b} and B=C disjoint-union {a,b}, with |C|=4
and both displayed pairs disjoint from C and each other. Set

    W = C + x^(a+b) C~ + (1+x^a)(1+x^b).

In Z[Z_n] a direct expansion gives

    AA~-BB~ = x^(-a-b)(1-x^a)(1-x^b) W.              (D)

If gcd(a,n)=1, the kernel of (1-x^a)(1-x^b) over C[Z_n] is precisely the
kernel of 1-x^b: the zero characters of 1-x^a consist only of the trivial
character, already a zero of 1-x^b. The DFT is invertible, so the equivalence
also holds for integer vectors. Therefore these two six-sets are homometric
**if and only if W is periodic under translation by b**. This is an exact
classification of this dyad-exchange shape, not of all six-pairs.

W has nonnegative integral coefficients and total mass twelve. If h is
the order of b, periodicity forces h to divide twelve, by summing the
constant coefficients along each b-orbit. Thus only subgroup orders
1,2,3,4,6,12 can occur under the unit-step hypothesis. h=1 or the stated
distinctness conditions may make a case trivial or inadmissible.

An explicit generator when h=6 is as follows. Let H=<b>, take a outside H,
and S=H disjoint-union (a+H). Remove R={0,a,b,a+b}. Reflection rho(x)=a+b-x
preserves S and R. If rho has no fixed point in S\R, choose exactly one
point from each of its four two-point orbits to form C. Then
C+rho(C)=1_(S\R), so W=1_S, which is b-periodic. Equation (D) generates
A,B as above. Retain only T/I-distinct outputs. This generator makes no
unit assumption on a, since b-periodicity directly suffices in (D).
It includes six-sets with a 2/4 distribution across H-cosets, where L7's
half-per-coset hypothesis fails.

For n=18, b=3, a=1, C={12,13,16,7}, the output translates to
{0,1,4,6,10,13}/{0,1,4,7,9,13}. At n=24, b=4, a=1,
C={16,17,21,9}, it translates to
{0,1,5,8,13,17}/{0,1,5,9,12,17}.

The h=6 generator is a particular two-coset complement/reflection
construction. Goyette quotes Soderberg 1995 Thm 3.18d for the broader
two-coset complement principle; the Soderberg primary proof remains unread.
We give the proof above and claim no novelty. It separates a cyclic shell
mechanism from the integer-shadow and inflation tests. The construction
alone does not establish that each output is non-shadow.

### 6.1 Complete generation of the parallelogram-dyad shape

The unit-step restriction can be removed with an exact nonnegative
decomposition. This is a classification of the displayed shape, not an
assertion that every six-pair can be aligned to this shape.

**Lemma D1.** For any a,b in Z_n, a nonnegative integer vector W satisfies
(1-x^a)(1-x^b)W=0 if and only if

    W=U+V,

where U,V are nonnegative integer vectors, U is a-periodic and V is
b-periodic. Write h_a=ord(a), h_b=ord(b). If W has mass twelve then

    12 = h_a * sum_(a-orbits) U + h_b * sum_(b-orbits) V.       (M)

In particular at least one of h_a,h_b is at most twelve. If h_a>12,
necessarily U=0, so W is b-periodic and h_b divides twelve.

Proof. The converse follows by annihilating U with 1-x^a and V with
1-x^b. For the forward direction, diagonalize translations by the DFT.
Each character killed by the product is killed by at least one factor.
Thus the complex kernel is the sum of the two periodic subspaces.
Taking real parts gives real periodic U_0,V_0 with W=U_0+V_0.

Now work separately in each coset of L=<a,b>. Every coset of <a> in L
meets every coset of <b> in L: for any two representatives their difference
lies in <a>+<b>=L. The intersections partition the L-coset. Because W is
a sum of two orbit-constant functions it is constant on each intersection,
and its cell values satisfy w_ij=u_i+v_j, where i indexes a-orbits and j
b-orbits. Every w_ij is a nonnegative integer. Fix a column j_0 and put

    m=min_i w_(i,j_0),
    U_i=w_(i,j_0)-m,     V_j=w_(i_0,j)-w_(i_0,j_0)+m.

The additive identity makes V_j=min_i w_ij, independently of i_0.
Hence U_i,V_j are nonnegative integers and U_i+V_j=w_ij. These values
define the required orbit-constant U,V on this component; do this on every
L-coset. Summing coefficients gives (M). QED.

**Theorem D (exact dyad grammar).** Every homometric pair that can be
aligned by separate rigid motions to

    A=C union {0,a+b},       B=C union {a,b},

with six distinct points in each and four distinct corners outside C,
is generated by the following parameters and conditions, and every
admissible output is homometric:

1. Choose a,b with R={0,a,b,a+b} distinct. Choose nonnegative integer
   orbit weights for a-periodic U and b-periodic V satisfying (M).
2. Set W=U+V and rho(x)=a+b-x. Require W(r)=1 for r in R, rho(W)=W,
   W(x) in {0,1,2} off R, and W(x) in {0,2} at rho-fixed points off R.
3. Recover C off R orbit by orbit. At a two-point rho-orbit with W=0,
   take neither point; with W=1, choose either point; with W=2, take both.
   At a fixed point, take it exactly when W=2. Then output the displayed
   A,B, retaining only T/I-distinct pairs for Z-relations.

Mass twelve and four corners imply C has mass (12-4)/2=4. Every C is
binary, avoids R, and satisfies C+rho(C)=W-1_R. Equation (D) and D1 then
prove homometry. Conversely a pair of the displayed shape has exactly
these coefficient and reflection conditions by its definition of W;
Equation (D) and D1 produce the required U,V, and step 3 recovers its C.
This proves completeness within the shape, including repeated distances,
non-unit steps and arbitrary composite n. No inverse spectral search or
coefficient cap occurs in this grammar. The mass restriction is exact.

The theorem does not assume C occupies one point in each subgroup coset.
It includes the h=6 shell above with U=0 and V=1_S. Larger mechanisms,
including complement conjugation and compositions, may align a pair to
the shape, but this theorem does not classify those alignments.

### 6.2 Three explicit unbounded purely cyclic six-note families

**Theorem H (parametric cyclic hexachords, computer-assisted non-shadow
part).** Let m,a be integers with 0<a<m/2 and let n=6m. Then each of the
following is a six-note Z-pair, and each is purely cyclic: it is not the
reduction of any pair of homometric integer six-sets, however large their
coordinates. These are actual T/I classes, with no identification by units.

    X1={0,a,a+m,2m,a+3m,a+4m}
    Y1={0,a,a+m,a+2m,3m,a+4m}

    X2={0,a,m,2m,a+3m,4m}
    Y2={0,a,m,a+2m,3m,4m}

    X3={0,a,m,3m,a+3m,5m}
    Y3={0,a,m,3m,4m,a+4m}.

The construction is a specialization of the h=6 two-coset shell. Its
classical antecedents preclude a novelty claim. The result here includes
explicit parameters, exact nontriviality conditions, and the general
integer-shadow obstruction, rather than only a finite menu explanation.

**Homometry proof.** Put H=<m> and S=H union (a+H). The two cosets are
disjoint because 0<a<m. For types 1 and 2 translate both sets by -2m.
Their exchanged dyads become {0,a+m}/{a,m}. The common four points become

    type 1: C'={4m,a+4m,a+5m,a+2m},
    type 2: C'={4m,a+4m,5m,2m}.

In both cases rho(x)=a+m-x exchanges these C' with the four remaining
points of S outside R={0,a,m,a+m}. For type 3 translate both sets by -5m.
The exchanged dyads become {0,a+4m}/{5m,a+5m}, with common

    type 3: C'={m,a+m,2m,4m}.

Now use rho(x)=a+4m-x and R={0,5m,a+5m,a+4m}; again C' and rho(C')
partition S minus R. Thus W=1_S in all three cases. It is periodic by m
(also by 5m), so (D) proves homometry. All six points are distinct under
0<a<m/2.

**Nontriviality proof.** A cyclic gap word determines a T/I class up to
rotation and reversal. The displayed sorted sets have the following gap
words, including the closing gap to 6m:

    X1: (a,m,m-a,m+a,m,2m-a)
    Y1: (a,m,m,m-a,m+a,2m-a)
    X2: (a,m-a,m,m+a,m-a,2m)
    Y2: (a,m-a,m+a,m-a,m,2m)
    X3: (a,m-a,2m,a,2m-a,m)
    Y3: (a,m-a,2m,m,a,2m-a).

For types 1 and 2 the unique smallest gap is a. Rotation can only align
that gap with itself; the respective third entries differ. Reversing X
and starting at its a-gap gives second entry 2m-a (type 1) or 2m (type 2),
whereas Y's second entry is m or m-a. The strict parameter bounds exclude
all these equalities. For type 3 the unique largest gap is 2m. Starting
there gives second entry a for X and m for Y. Reversing X and starting
there gives second entry m-a, still different from m. Thus none of the
three pairs is T/I equivalent.

**Stable-matching lemma.** Every unordered distance for these six sets is
one of the following forms (some forms can have multiplicity zero):

    a < m-a < m < m+a < 2m-a < 2m < 2m+a < 3m-a < 3m.

To see this, every point is im+ja with j in {0,1}; differences have
a-coefficient -1,0,1 and m-coefficient between -5 and 5. Folding modulo
6m into [0,3m] gives precisely the listed possibilities. The inequalities
follow from 0<2a<m. The order of the six vertices is fixed as displayed.
Consequently edge distance buckets, their multiplicities, the sign of
each oriented modular equality, and which edges are antipodal are
constant throughout this entire parameter chamber. All compatible signed
matching matrices are therefore exactly those at m=3,a=1,n=18.

**Non-shadow proof.** Let v be the ten anchored coordinates, in the
displayed vertex order. Write v=a*v_a+m*v_m. Their integer coefficient
vectors are:

| Type | v_a (A then B) | v_m (A then B) |
|---|---|---|
| 1 | (1,1,0,1,1, 1,1,1,0,1) | (0,1,2,3,4, 0,1,2,3,4) |
| 2 | (1,0,0,1,0, 1,0,1,0,0) | (0,1,2,3,4, 0,1,2,3,4) |
| 3 | (1,0,0,1,0, 1,0,0,0,1) | (0,1,3,3,5, 0,1,3,4,4) |

The independent exhaustive edge-by-edge audit enumerates **384 matrices
for each type**, including both signs on antipodal matches. Exact saved
certificates contain, for each matrix M, an integer row combination c
such that:

    M v_a = 0,
    each coordinate of M v_m is divisible by 6,
    every coefficient of c M is divisible by 6,
    the integer -c M v_m / 6 is not divisible by 6.           (H-cert)

These are finite, exact, independently checked integer identities. They
are stored in `results/2026-09-30-six-shadow/n18.json` (type 1) and
`shell_type{2,3}_n18.json`. The independent reviewer does not trust the
production Smith routine: it enumerates matchings via a separate DFS,
reconstructs M, and multiplies each stored row combination directly.

An integer lift z=v+6m*y would require

    M y = -M v/(6m) = -M v_m/6.

Multiply by c. The left side is divisible by 6, the right side is not,
by (H-cert). Thus this matching cannot give any integer lift. The
stable-matching lemma exhausts all matching possibilities at every m,a
in the chamber, and the exact-obstruction theorem in §4 then excludes
every integer homometric lift. This proves the purely cyclic assertion
for arbitrary n=6m, not merely the largest computed n. QED.

At m=3,a=1 these are the three named n=18 strict/Bloom residues. At m=4,
a=1 they give three corresponding n=24 residues. At m=5,a=1 they give
primitive n=30 examples, and a=2 gives another three; ordinary inflation
accounts for parameters with gcd(a,m)>1. The prime-divisor content of
these templates is cyclic six-torsion, in agreement with Theorem S.
Theorem H does not say every h=6 shell output is non-shadow, nor that
these three families exhaust arbitrary six-note relations.

## 7. Remaining obstruction and evidence limits

Theorem S bounds the possible prime support of a purely cyclic obstruction,
but does not list the actual torsion templates. It gives no completeness
claim for n divisible by a prime <=251. The matching matrix of a single
example is not an invariant of the pair when intervals repeat: all
compatible matchings must be attacked.

The finite six-note inventory covers n=12..60 by two census methods; reference
agreement is n=6..24. The inherited all-cardinality census n=38..40 remains
single-method and provisional; the new six-only counts do not repair it.
Inherited factor menus remain coefficient-restricted above weight six,
and the global kappa definition defect and C3 closure are unaffected.

Next: classify the nondegenerate signed distance-matching lattices whose
torsion primes are <=251, and the repeated-distance integer six-pairs.
The observed primitive residues at 17,19,21,23,24,27,28,30,31 suggest a
much smaller boundary, but finite data cannot establish it. Neither
a capped factor failure nor one rank-ten matching proves a pair non-shadow.

Lean was not installed on the session PATH. Exact determinant, Smith-form
and coefficient identities supplement the written proof; they do not
replace its separate adversarial review.

## 8. Reproduction and checkpoint

Use the pinned environment from the repository root. The new tests do not
modify the immutable reference or the data directory.

```bash
.venv/bin/python tests/test_env.py
.venv/bin/python tests/run_tests.py
.venv/bin/python tests/test_six_structure.py
.venv/bin/python tests/test_six_parametric.py
.venv/bin/python tests/test_six_shadow_review.py --out results/2026-09-30-six-shadow-review.json
.venv/bin/python src/six_shell.py --nmin 12 --nmax 60

# Regenerate all three finite certificate lists used in Theorem H.
.venv/bin/python src/six_shadow.py --n 18 --a 0,1,4,6,10,13 --b 0,1,4,7,9,13 --out results/2026-09-30-six-shadow/n18.json
.venv/bin/python src/six_shadow.py --n 18 --a 0,1,3,6,10,12 --b 0,1,3,7,9,12 --out results/2026-09-30-six-shadow/shell_type2_n18.json
.venv/bin/python src/six_shadow.py --n 18 --a 0,1,3,9,10,15 --b 0,1,3,9,12,13 --out results/2026-09-30-six-shadow/shell_type3_n18.json
```

The shadow CLI labels a newly generated result unvalidated until an
independent audit; the saved audit and its payload hashes establish the
status of this checkpoint. Regeneration can change timings and metadata
hashes without changing the exact certificates. Run the independent review
again after regeneration. Its DFS matching enumerator, Bareiss determinants,
Fraction ranks, Cramer lifts, formal difference identities and direct integer
row-witness checks do not import the new production implementations.

**[COMPUTED]** The independent attack exhausts all 1,152 symbolic rejection
certificates in H, all 22,921 saved dyad-shape witnesses and every inventory
pair through n=60. It checks shape coverage independently relative to the
saved strict/Bloom labels; it does not recertify strict-menu discovery.
The formulas in H, canonized by the immutable reference in
`tests/test_six_parametric.py`, give exactly all 60 of the dyad-shaped edges
among those saved gaps through n=60. The per-n counts at
18/24/30/36/42/48/54/60 are 3/3/6/6/9/9/12/12. Prior QL or broader-menu
certificates may already explain these pairs; this is a more explicit
parametric mechanism and non-shadow proof, not a claim that the program
had no earlier explanation of the n=18 examples.
The n=21 benchmark also has no integer shadow: all 48 compatible signed
matchings have rank ten. This is compatible with its integral affine factor
flip in the cyclic group ring and distinguishes that mechanism from a
reduction of integer homometric sets. Selected prime examples at 17,19,23,31
are independently certified non-shadows as well; no parametrization of all
such prime exceptions is proved here.

The census checkpoint is `01f7550` (parent `d9881fc`). The mathematical
status promotion and reproduction section were added after review without
changing the reviewed statements, matrices, endpoints or certificates.
A human mathematician should review the proof and finite certificate
dependency before public sharing.
