# Composite Bloom parameters: a local-ring and CRT classification

30 September 2026. **[PROVED], in-house, with exact finite integer lift certificates;
accepted by the separate fresh attack in
`notes/2026-09-30-six-composite-review.md`.** No novelty claim. The accepted field
theorem in `notes/2026-09-30-six-prime-theorem.md` supplies the integer
coefficient identities restated here; its field orbit separation is not
silently applied to rings. This note concerns only the classical Bloom
image, not the complete six-point homometry grammar.

## 1. Domains and result

Use the ordered lists

\[
 X_v=(0,a,b-2a,2b-2a,2b,3b-a),\qquad
 Y_v=(0,a,b+2a,2b-a,2b+a,3b-a),\quad v=(a,b).
\]

An unordered pair consists of the two independent translation/reflection
classes; general units are never quotiented out. Put

\[
 s=a^2-ab+b^2,\quad e=ab(a-b),\quad
 d=(a+b)(2a-b)(a-2b).
\]

Let every prime divisor of n be at least13. Write n as a product of its
pairwise coprime prime powers q=p^k. Three domains must be distinguished.

* Ω_n: both lists have six distinct entries in Z/n.
* F_n: both lists have six distinct entries modulo **each prime** p|n.
* L_n: e and d are units modulo n, and both lists have six distinct
  entries modulo **each prime power** q||n.

Thus F_n⊆L_n⊆Ω_n. The second inclusion can be strict even when e,d are
units: distinct global entries need not remain distinct in every CRT
factor. In one prime-power ring the L condition is simply actual
six-element supports together with unit e,d.

Define

\[
 R=\begin{pmatrix}0&-1\\1&-1\end{pmatrix},\qquad
 T=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
 G=\{\lambda R^iT^j:\lambda\in\{1,-1\},\ i=0,1,2,\ j=0,1\}.
\]

**Theorem CR [PROVED].** On L_n, every parameter
gives two different homometric rigid classes, and two parameters give the
same unordered pair exactly when they belong to the same free G-orbit.
Consequently the number of pairs represented by L_n is

\[
 B_L(n)=\frac1{12}\prod_{p^k\Vert n}
 \left[p^{2k-2}(p-1)(p-5)-6p^{k-1}(p-1)\right].
\]

For the faithful-reduction subdomain F_n this specializes to

\[
 B_F(n)=\frac1{12}\prod_{p^k\Vert n}p^{2k-2}(p-1)(p-11).
\]

The denominator is twelve **once for the global parameter orbit**, not
once per CRT factor. These are counts of pair edges represented by the
stated domains. They do not count all six-point pairs or all Ω_n images.
The n221 moment obstruction remains: equal (s,e²) is not asserted to be
a complete global invariant. Actual point permutations supply the
additional gluing information.

## 2. Local-ring separation

Let A=Z/p^k with p≥13. Assume both supports are six-element sets and e,d
are units. Since2,3,11 are units, scaled centered coordinates are valid:
the six coordinates of X and Y are respectively

\[
 C_Xv=(2a-4b,5a-4b,-4a-b,-4a+2b,2a+2b,-a+5b),
\]
\[
 C_Yv=(-a-4b,2a-4b,5a-b,-4a+2b,2a+2b,-4a+5b).
\]

They equal3(x−μ), with μ the sum divided by6. Translation leaves them
unchanged and inversion negates them. They have six distinct entries
because3 is a unit. Let m_j be the sum of their jth powers. The integer
identities from the accepted field note remain identities in A:

\[
 d^2+27e^2=4s^3,\qquad m_2(X)=m_2(Y)=66s,
\]
\[
 m_3(X)=6d-243e,\qquad m_3(Y)=6d+243e,
\]
\[
 m_6(X)=23946s^3+6399e^2-4860de,\qquad
 m_6(Y)=23946s^3+6399e^2+4860de.
\]

Define

\[
 C_3=m_3(X)^2+m_3(Y)^2-288s^3,\qquad
 C_6=m_6(X)+m_6(Y)-47892s^3.
\]

Then 118C_6−13C_3=162e². Since66 and162 are units, equality of unordered
rigid pairs implies equality of s and e², without division by s.

If e(v)²=e(w)², the unit u=e(w)/e(v) satisfies(u−1)(u+1)=0.
In this local ring exactly one of u−1,u+1 is a unit unless the other is
zero: their difference is2, a unit. Reduction modulo p first chooses
u≡1 or−1, and the opposite factor is a unit. Therefore u=1 or−1 in A.
Negate w if needed to arrange e(w)=e(v).

The ordered roots(a,−b,b−a) factor z³−sz−e. Their three pairwise
differences are a+b,2a−b,a−2b, up to sign; their product is a unit because
d is a unit. Thus they are pairwise distinct modulo p. Evaluate the
factorization at any root r of the other parameter's cubic. Modulo p,
r matches exactly one of these three roots; the other two differences
are units in A. From the product being zero, the remaining difference
is exactly zero in A. Hence the root multisets coincide and are related
by one permutation. This argument proves the needed ring version of root
separation directly; no uniqueness assertion for general ring
factorization or a Hensel theorem is assumed.

R cyclically permutes the root triple and−T transposes its first two
entries. They realize all six permutations; restoring the optional
negation gives w∈Gv. Conversely the integer coefficient identities for G
give the same unordered pair in every ring. Every parameter in the local
domain therefore has one G-orbit as its pair fiber.

Finally

\[
 m_3(X)^2-m_3(Y)^2=-5832de
\]

is a unit. The endpoint classes cannot be equal. If both endpoint sets
had reflection symmetries, both odd centered third moments would vanish,
also contradicting this identity. These conclusions hold in A itself,
even when some distinct entries become equal modulo p.

The G-action is free: all possible fixed lines are
a=0,b=0,b=a,b=−a,a=2b,b=2a; each would make e or d zero, contrary to
unit regularity. The other nonidentity elements have fixed-vector
matrices with unit determinants1,3,4. This uses the explicit G matrices,
not an orbit-size assumption.

## 3. Formal permutations and reflection parity

Permutations below use row indexing: C_XRv is the row list C_Xv indexed
byρ_X, and similarly for Y. Direct coefficient comparison gives

\[
 \rho_X=(3,2,5,4,0,1)=(0\ 3\ 4)(1\ 2\ 5),
\]
\[
 \rho_Y=(5,3,0,4,1,2)=(0\ 5\ 2)(1\ 3\ 4),
\]
\[
 \tau_X=(3,5,0,1,4,2),\qquad
 \tau_Y=(2,3,5,0,4,1)=\tau_X^{-1},
\]

with C_XTv=(C_Yv)_[τ_X] and C_YTv=(C_Xv)_[τ_Y]. Eachρ is a product
of two3-cycles and eachτ is a5-cycle with one fixed index. Therefore all
formal point permutations of R^iT^j are even. For each fixed endpoint and
j, its three formal permutations indexed by i are distinct, since the
relevantρ has order3.

A reflection of any six-element subset of A has at most one fixed point,
since2 is a unit. An involution on an even-sized set has an even number
of fixed points; hence this reflection has none and permutes the six
labels as three transpositions. Its permutation is odd. A nonzero
translation cannot stabilize a six-element set: its additive order is
a power of p and at least13, and all its point orbits have that order.
Thus a given sign determines at most one endpoint transport, including
its label permutation. These facts apply to actual six-element supports
in A, not necessarily six distinct residues modulo p.

## 4. CRT gluing with one global matching

Take v,w∈L_n giving the same unordered pair. Choose its global endpoint
assignment j∈{0,1}, global signs ε_X,ε_Y∈{1,−1}, translations and
point-label permutations π_X,π_Y. The centered equations remove the
translations. Every local support has six distinct entries, so the same
global permutations reduce to genuine unique local point matchings.

By §2 in each factor A_q there is a unique

\[
 w=\lambda_qR^{i_q}T^{j_q}v.
\]

Because X_v and Y_v are locally different rigid classes, the local
endpoint assignment j_q must equal the chosen global j. Compare the
formal centered equation for this local G-element with the actual global
endpoint equation. If ε_X=λ_q, the actual π_X is exactly the formal even
permutation. If ε_X=−λ_q, their quotient is a reflection permutation of
the matched local endpoint, hence odd. Therefore

\[
 \operatorname{sgn}(\pi_X)=\epsilon_X\lambda_q.
\]

The left side and ε_X are global, so λ_q is one common λ across all
factors. The same argument holds for Y. At least one of ε_X,ε_Y equals
λ: otherwise both local endpoints would have reflection symmetries,
which §2 excludes. Choose such an endpoint. Its actual global
permutation is exactly the formal permutation in every factor. For fixed
j the three formal permutations are distinct, so i_q is a common i.
CRT now gives w=λR^iT^jv modulo n.

The converse follows from the integer coefficient identities. Freeness
follows by reducing a hypothetical fixed parameter to any local factor,
where §2 already establishes freeness. This proves the orbit
classification on L_n. It explicitly rules out mixed local signs even
though mixed signs preserve all even moments and squared odd moments.

## 5. Counting the two domains

The twelve primitive collision kernels have normals

\[
 (1,0),(0,1),(-1,1),(1,1),(-2,1),(2,1),(-3,1),
 (-1,2),(1,2),(-3,2),(-1,3),(-2,3).
\]

Every nonzero determinant between different normals has absolute value
in{1,2,3,4,5,7,8}; hence it is a unit at every prime considered here.
All twelve lines are distinct modulo p and any two meet only at zero
over Z/p^k as well. The six unit conditions arising from e and d exclude
six of these lines modulo p. The number of allowed mod-p parameters is
(p−1)(p−5), each with p^{2k−2} lifts.

The six remaining collision kernels are not among these six. A point on
one remaining kernel satisfies the unit conditions exactly when it is
primitive, since its line meets each excluded line only at the origin
modulo p. Each such kernel has p^k−p^{k−1}=p^{k−1}(p−1) primitive
points; distinct kernels cannot meet at one of these points. Subtracting
these six disjoint sets yields

\[
 |L_{p^k}|=p^{2k-2}(p-1)(p-5)-6p^{k-1}(p-1).
\]

For F, all twelve mod-p lines are excluded, so

\[
 |F_{p^k}|=p^{2k-2}(p-1)(p-11).
\]

CRT multiplies these domain sizes. Divide the resulting parameter count
by twelve, once, using §4 and freeness. This gives the formulas in §1.
For comparison the full globally support-admissible domain has
|Ω_n|=(n−1)(n−11), because each of the twelve kernels modulo n has n
points and their pairwise intersections are exactly the origin. That
support count alone does **not** prove a full Ω_n pair-count formula.

## 6. Endpoint reflection and the characteristic31 boundary

Reflection parity in §4 needs no list of exceptional reflections. An
exact optional audit is useful. Pairing six centered entries into three
opposite pairs gives fifteen perfect matchings per endpoint. For X the
only matchings whose2×2-minor gcd has a prime factor≥13 are

* (01)(23)(45): rows(7,−8),(−8,1),(1,7), gcd57=3·19.
* (02)(14)(35): rows(−2,−5),(7,−2),(−5,7), gcd39=3·13.

For Y they are

* (01)(24)(35): rows(1,−8),(7,1),(−8,7), gcd57.
* (03)(12)(45): rows(−5,−2),(7,−5),(−2,7), gcd39.

All other matchings have nonzero gcd with no prime factor≥13. Thus on
the faithful-reduction locus reflections occur only at p13 or19, on an
isotropic slope s=0. At p13, X reflects at b/a=10 and Y at4. At p19,
X reflects at8 and Y at12. These examples really have six distinct
entries. For example X_(1,8) in Z19 is{0,1,4,6,14,16}, fixed by1−x.
For k≥2 these same faithful reflections cannot persist: the relevant
minor has p-adic valuation1, and its adjugate equations force p v=0
modulo p^k, incompatible with a primitive reduction. This last statement
only concerns faithful reduction; reflections of nonfaithful lifts are
not classified by that shortcut.

Characteristic31 causes no problem for pair classification or gluing.
The local-ring proof uses pair invariants with units66,162, not the
single-endpoint determinant divisible by31. The accepted shared-endpoint
example at31 survives as a boundary to unique-partner assertions.
Section11 proves that the complete-local-support graph has disjoint
edges when31 does not divide n; that statement concerns Bloom partners.

## 7. Verification and remaining obstruction

Startup pinned reference suite: `.venv/bin/python tests/run_tests.py`,
10/10 groups pass. The parent session owns new implementations and tests;
this note owns only the argument and its optional exact auxiliary
certificate directory. The separate fresh review accepts the local-ring
and permutation gluing steps and the extensions in §§8–11.

Exact prospective counts: B_F(169)=338, B_L(169)=1274;
B_F(221)=192; B_F(247)=288; B_F(323)=1152;
B_F(961)=48050. Parameter-only checks must distinguish these domains
from Ω_n. An exploratory independent anchored-point partition of the
full Ω_169 image found2212 pairs, all fibers twelve and exactlyG, with no
congruent endpoints; it independently verifies the stronger statement now proved in §8.
The separate certificate below records its method and exact fibers.

The precise remaining cases are local support collisions that disappear
globally in different CRT factors. The local nonunit problem is settled
in §8, but a global label permutation can still reduce to a matching
of repeated labels. The parity proof in §4 cannot be used after discarding
its local six-element-support hypothesis. A full Ω_n classification and
its potential count(n−1)(n−11)/12 therefore remain open here.

## 8. Complete local prime-power classification

**[PROVED], with the independently audited forty-system integer table.** The
following closes the local nonunit strata by a small exact integer table.
It does not yet close arbitrary CRT gluing when local supports collide.
The proof and certificate are separate from the regular theorem above.

**Theorem PP.** For every p≥13 and k≥1, the full Ω_(p^k) image
has exactly one free G-orbit per unordered rigid pair and no congruent
endpoints. Its pair count is(p^k−1)(p^k−11)/12.

### 8.1 Weighted field alignment

The centered moment identities apply to six-labelled lists even if some
entries coincide after reduction. A point permutation of the actual
six-element supports modulo p^k therefore gives equality of the unordered
centered list moments modulo p. Over the field F_p the recovered s,e²
again give one G-orbit, including the cases e=0 or d=0: e² equality still
chooses e or−e, and monic cubic factorization gives equality of root
multisets even when roots repeat. This field observation does not require
the reduced supports to have size six.

If v≡0 modulo p, the same invariant values force w≡0 modulo p: the
cubic z³ has all three roots zero. All support entries and any transport
translation are then divisible by p. Divide both parameters, points and
translations by p and work modulo p^(k−1). The six-element-support
condition is preserved under this division. Induction reduces to a
primitive parameter; the k=1 case is the accepted field theorem.

For a primitive v, exactly zero or one of the twelve collision forms
vanishes modulo p, since distinct collision lines have unit determinant.
If e,d are units the local proof in §2 applies. Otherwise v lies on one
of the six e/d lines. G preserves the separate e=0 and d=0 line triples
and is transitive on each triple. Simultaneously change v and w by G to
put the line into b≡0 (type E) or b≡2a (type D), with a a unit. Change
w once more by a suitable G-element so that w≡v modulo p; such a change
preserves equality of the unordered rigid pairs. The preceding weighted
field alignment justifies this normalization.

### 8.2 All possible reduced matchings

At the normalized reductions, after factoring out the unit a, the
centered coordinate lists are

| Type | C_X base | C_Y base |
|---|---|---|
| E, b=0 | (2,5,−4,−4,2,−1) | (−1,2,5,−4,2,−4) |
| D, b=2a | (−6,−3,−6,0,6,9) | (−9,−6,3,0,6,6) |

In E the two weighted lists coincide up to permutation, but neither is
its own negative; only sign+1 is possible for either endpoint, whether
or not the endpoints are swapped. Each endpoint has two equal pairs,
giving exactly four possible point permutations. There are consequently
2·4·4=32 paired matching patterns.

In D the two lists are negatives up to permutation, and neither equals
its own negative. Nonswapped endpoints require sign+1 at both endpoints;
swapped endpoints require sign−1 at both. Each endpoint has one equal
pair, giving two possible point permutations and2·2·2=8 patterns.

These are the entire reduced matching lists for every p≥13, not just
over the rationals. Within the relevant signed lists the nonzero integer
value differences belong to{3,6,9,12,15}; none has a prime divisor≥13.
Wrong-sign matches are impossible since the third moments are nonzero:
in E they equal12a³ at both endpoints, and in D they equal±486a³.
The point permutation carries centering across reduction, so translations
cannot add any further matching patterns.

### 8.3 Integer elimination table

For a possible endpoint swap j and its sign ε, let U_X,U_Y be C_X,C_Y
in their appropriate order, and let π_X,π_Y be one of the reduced
matching patterns. The actual equations in Z/p^k are

\[
 C_Xw=\epsilon(U_Xv)_{[\pi_X]},\qquad
 C_Yw=\epsilon(U_Yv)_{[\pi_Y]}.
\]

The first two rows of C_X form A=[[2,−4],[5,−4]] with determinant12.
Thus12w=Mv, where the integer matrix M is obtained by multiplying the
first two permuted target rows by12A^−1=[[-4,4],[-5,2]]. Substitution
in all twelve coordinate equations produces twelve integer rows H_l
with H_l v=0. This is exact because12 is a unit in Z/p^k.

Every type-E residual row has the form(0,h_l); every type-D residual
row has the form(−2h_l,h_l). The complete coefficient table is:

| Type | gcd of all h_l | Number of patterns | Consequence |
|---|---:|---:|---|
| E | 0 | 2 | w=v or w=R²Tv |
| E | 18 | 16 | b=0 exactly |
| E | 36 | 12 | b=0 exactly |
| E | 72 | 2 | b=0 exactly |
| D | 0 | 2 | w=v or w=−R²Tv |
| D | 9 | 4 | b=2a exactly |
| D | 36 | 2 | b=2a exactly |

For every nonzero row gcd the certificate exhibits Bézout coefficients
combining the h_l into that gcd. It has only2 and3 as prime factors,
so it is a unit modulo every p^k considered here. The corresponding
collision form b or b−2a is therefore exactly zero, not merely zero
modulo p. These patterns contradict the actual six-element supports and
are eliminated. The zero-gcd patterns give the four stated G maps by
the explicit M matrices12I,12R²T,−12R²T.

The table is small enough to audit in full. Its reproducible generator
uses only integer arithmetic; no symbolic solver, Smith normal form or
floating-point calculation is a dependency. It enumerates all720
permutations at each endpoint, filters by the displayed exact weighted
lists, and retains every one of the32/8 paired systems, its M,H rows,
gcd, Bézout combination and consequence:

```bash
.venv/bin/python src/six_prime_power_lifts.py
```

Output: `results/2026-09-30-six-composite-algebra/lift-table.json`, SHA256
`02eb646237f2821b7a029675256c1bd1b1c4b780cf04e01604b88d7981e545c8`.
An auxiliary independent Smith-normal-form derivation agrees: E has
24 rank-three systems with diagonal(1,3,3,0), six with(1,3,6,0), and two
rank-two systems with(1,3,0,0); D has six rank-three(1,3,3,0) and two
rank-two(1,3,0,0). The integer elimination/Bézout data above suffice for
the proof; the unrecorded exploratory Smith calculation is not needed.

All surviving cases give w∈Gv, restoring the changes of parameters used
for normalization. Conversely each G map preserves the pair. Freeness
on the full actual-support domain follows directly from the fixed-line
calculation: every reflection fixed line is an actual collision line,
and all other nonidentity fixed-vector determinants are units. Congruent
endpoints in the singular normalized cases would correspond to a
matching of X_v to Y_v alone; the paired-equation argument applies by
setting w=v and using that hypothetical congruence to build a swapped
pair identification. The surviving swapped maps are R²T or−R²T, whose
fixed parameters require b=0 or b=2a exactly, again collisions. In the
regular case congruence is already excluded by−5832de being a unit.
This proves the local statement using the exact table, independently
reconstructed and accepted in the separate fresh review. Counting follows from the twelve collision
kernels and the free twelve-element orbit, as in §5.

**Precise remaining global obstruction:** a globally six-element support
can have repeated labels in one CRT prime-power projection. Such local
repetition breaks the permutation-parity argument of §4; the preceding
local theorem assumes actual local six-element supports. Arbitrary global
Ω_n classification is not supplied by this extension.

## 9. CRT with complete local supports

**[PROVED], corollary of Theorem PP, separately attacked.** Let S_n be
the parameters whose two supports have six distinct entries in **every
prime-power factor** Z/p^k of Z/n. No unit condition on e,d is imposed.
Then F_n⊆L_n⊆S_n⊆Ω_n. Using the exact local theorem in §8, the
global pair fibers on S_n are exactly the free G-orbits, and

\[
 B_S(n)=\frac1{12}\prod_{p^k\Vert n}(p^k-1)(p^k-11).
\]

There are two additional points to justify before reusing §4.

First, at most one endpoint of an actual locally six-element Bloom pair
can have a reflection symmetry even when e,d are nonunits. Divide the
parameter by its maximal common p-power; division takes actual supports
and any reflection transport to the corresponding smaller ring, since
the reflection shift is itself a support entry (zero belongs to the
support). The resulting primitive reduction lies on at most one of the
twelve collision lines. In the regular e,d-unit case, §2 already excludes
simultaneous reflections by the unit third-moment difference. On an
e=0 or d=0 reduction line, move to E or D by G. The weighted reduced
third moments in §8.2 are12a³ at both endpoints or±486a³, all nonzero
for p≥13. A reflection of an actual endpoint would reduce to negation
of its centered weighted list, making its odd third moment zero. Thus
neither endpoint can reflect in these singular primitive cases. G
preserves whether endpoints reflect, up to exchanging them. These cases
exhaust every primitive reduction and prove the required assertion.

Second, Theorem PP gives locally different endpoint classes and a unique
local G-element, even on its nonunit strata. Therefore the global
endpoint assignment reduces to the same assignment in every factor.
Because each support is actually six-element in each factor, the global
label permutation reduces to a unique actual local matching. A reflected
matching still has three transpositions and odd parity:2 is a unit in
each factor, so a six-point reflection has no fixed points. All formal G
point permutations are even as in §3.

Now the parity argument of §4 gives one common local G sign. The
preceding no-simultaneous-reflection assertion ensures at least one
endpoint transport uses that sign; its formal point permutation pins one
common rotation index. CRT gives one global G-element. The converse and
freeness follow as before. Each local support domain has
(p^k−1)(p^k−11) parameters by the twelve collision kernels. CRT multiplies
these sizes and the free global orbit divides by twelve once.

The distinction from the full Ω_n domain persists. For example at a
product of distinct primes S_n equals F_n. Global six-element supports
can arise from different local collisions; these are omitted from S_n,
and §9 does not infer their parameter fibers or count.

## 10. Unique partner over prime powers

**[PROVED], with the independently audited twenty-four-system table.** If p≥13 and
p≠31, every six-element Bloom endpoint in Z/p^k belongs to exactly one
unordered Bloom pair, for every k≥1. This concerns the full actual-support
domain Ω_(p^k), with no faithful-reduction or unit restriction. It is not
asserted for arbitrary composite n here.

The single-endpoint moment matrix from the accepted field theorem has
determinant−2^4·3^12·31. It is invertible in Z/p^k under the stated
restriction. The identities apply to the actual six-element endpoint and
also to its reduced six-labelled list. Thus a shared endpoint recovers s
and e² for both parameter pairs without needing to know whether the
shared side is X or Y. Over F_p the weighted root-multiset argument of
§8.1 aligns their reductions by G. If the common reduction is zero,
divide the parameters and the shared-endpoint transport by p and use
induction. On a primitive reduction with e,d units, the local-ring
unit-separated cubic argument in §2 already aligns the exact parameters.

The remaining primitive cases are E and D from §8. A G change can
interchange endpoint labels, so retain all four choices of source and
target endpoint. Their normalized reduced signs and point permutations
are exactly the same reduced lists of §8.2, now using one six-row
equation. The first two rows of either source matrix have determinant12:
12(C_Y[first two])^−1=[[-4,4],[-2,−1]], while C_X's inverse is as before.
Eliminating w gives six residual rows of the form(0,h_l) in E or
(−2h_l,h_l) in D. The complete one-endpoint table is:

| Type | gcd of h_l | Number of patterns | Consequence |
|---|---:|---:|---|
| E | 0 | 4 | w=v or w=R²Tv |
| E | 18 | 8 | b=0 exactly |
| E | 36 | 4 | b=0 exactly |
| D | 0 | 4 | w=v or w=−R²Tv |
| D | 9 | 2 | b=2a exactly |
| D | 36 | 2 | b=2a exactly |

Every nonzero gcd is a unit modulo p^k; its logged Bézout combination
forces an actual support collision and excludes that pattern. Every
remaining matrix is a member of12G. Hence sharing an endpoint puts the
parameters in the same G-orbit and gives the same pair, proving the
local unique-partner statement.

Reproduce all24 exact matching systems and Bézout witnesses:

```bash
.venv/bin/python src/six_prime_power_endpoint_lifts.py
```

Output: `results/2026-09-30-six-composite-algebra/endpoint-lift-table.json`,
SHA256 `eb02da0114f9518eb885f164ab4a1337f0ae03c7f09960fcdd25bddc7a558732`.
At p31 the single-endpoint moment matrix is singular, and the inherited
characteristic31 example already gives two different pairs sharing an
endpoint at k=1. This exception is retained. Neither the paired-table
proof nor the pair-count formula has to exclude31.

Global CRT unique-partner statements need an additional shared-endpoint
matching argument: local unique partner classes do not by themselves
produce one global rigid transport of the other endpoint. Section10
does not make that inference.

## 11. Unique partner on the CRT local-support domain

**[PROVED], with the exact reflection catalog and a separate fresh attack.** Suppose every prime
divisor of n is at least13 and31 does not divide n. Every endpoint of a
pair represented by S_n has a unique partner in the **entire Bloom
image**, and the S_n Bloom graph consists of disjoint edges. Its number
of nontrivial Bloom families is B_S(n) from §9. This still does not count
all Ω_n families or exclude non-Bloom homometric partners.

### 11.1 Complete local reflection catalog

The fifteen perfect-matching calculations in §6 apply to every actual
reflection, including nonfaithful parameters. Divide a parameter by its
maximal common p-power, obtaining a primitive parameter u in an effective
ring Z/p^ell. Actual reflection label permutations are still three
transpositions, so one of those fifteen matching matrices annihilates u.
Every matching has rank two over Q. At primes≥13 only the displayed13/19
matchings can have nonunit minors; each has a2×2 minor of p-adic
valuation exactly one. If ell≥2, the adjugate equations give p u=0,
forcing both coordinates divisible by p^(ell−1), contrary to primitivity.
Thus a reflected endpoint is necessarily an inflation of a reflected
six-element endpoint in F13 or F19. For X its label permutation is

\[
 \chi_{X,13}=(2,4,0,5,1,3),\qquad
 \chi_{X,19}=(1,0,3,2,5,4).
\]

For Y the corresponding permutations are

\[
 \chi_{Y,13}=(3,2,1,0,5,4),\qquad
 \chi_{Y,19}=(1,0,4,5,2,3).
\]

The primitive kernel slope is unique and multiplication of the parameter
by a nonzero scalar does not change these label permutations. Division
and inflation also preserve them.

### 11.2 The reflection cosets cannot mix13 and19

Compose permutations using row indexing as in §3. The three possible
reflection-twisted rotation matchings for X are:

| Prime | i=0 | i=1 | i=2 |
|---|---|---|---|
|13|(2,4,0,5,1,3)|(5,0,3,1,2,4)|(1,3,4,2,5,0)|
|19|(1,0,3,2,5,4)|(2,3,4,5,1,0)|(5,4,0,1,2,3)|

The two three-element sets are disjoint. For completeness the Y cosets
are also disjoint:

| Prime | i=0 | i=1 | i=2 |
|---|---|---|---|
|13|(3,2,1,0,5,4)|(4,0,3,5,2,1)|(1,5,4,2,0,3)|
|19|(1,0,4,5,2,3)|(3,5,1,2,0,4)|(4,2,3,0,5,1)|

These are exact label arrays, not sampled point configurations.

### 11.3 Shared-endpoint gluing

Normalize a shared global endpoint to be X_v and X_w by applying T to
either parameter when required; T exchanges endpoints by the integer
coefficient identity. In each CRT factor, §10 makes the two local Bloom
pairs equal. The locally different endpoints from §8 then force the
local G-element to preserve endpoint labels, so
w=λ_qR^(i_q)v locally.

Let ε and π be the sign and fixed label permutation of the actual global
shared-endpoint transport. The same parity comparison as in §4 gives
sgn(π)=ελ_q, so all local signs equal one λ. If ε=λ, every local matching
is the formalρ_X^(i_q). Its three label permutations are distinct, giving
one common i and w=λR^iv globally.

If ε=−λ, the matched endpoint reflects in every local factor. By §11.1
every factor then has prime13 or19 and the match belongs to the
appropriate coset in §11.2. Both primes cannot occur because the cosets
are disjoint. There is only one prime-power CRT factor per prime; hence
n is a single prime power and §10 gives the global conclusion directly.
Thus sharing an endpoint always yields the same global G-orbit and pair.

Finally this uniqueness is not limited to a second parameter already
declared in S_n. The exact Bloom directed-difference identity is an
identity of six-labelled multisets. For such a list the autocorrelation
at zero is the sum of the squares of its point multiplicities. It equals
six exactly when the six labels are distinct. Therefore in every factor
one Bloom endpoint has six distinct entries if and only if the other
does. An arbitrary global Bloom parameter sharing an S_n endpoint has
that endpoint locally six-element, so its other endpoint is also locally
six-element and its parameter automatically belongs to S_n. The preceding
gluing proof consequently covers every other Bloom partner.

The exception31 is inherited from the genuine field shared-partner
counterexample. No unique-partner assertion is made when31 divides n.
