# The full global Bloom image by exact labelled-point matching

Started30 September2026; completed1 October2026. **[PROVED], in-house, computer-assisted; accepted
by the separate fresh attack in
`notes/2026-09-30-six-composite-global-review.md`.** The finite tables are **[COMPUTED]** and checked by independent
complete methods. No novelty claim. The argument concerns the classical
two-parameter Bloom image, not all six-point homometry. It removes the
local-six-support assumption in the earlier composite note.

## 1. Statement and scope

Write

\[
 X_v=(0,a,b-2a,2b-2a,2b,3b-a),\quad
 Y_v=(0,a,b+2a,2b-a,2b+a,3b-a),\quad v=(a,b).
\]

Let Ω_n be the parameters for which **both global lists have six
distinct entries** in Z/n. Projections to individual prime powers may
have collisions. Let Φ(v) be the unordered pair of independent T/I
classes of X_v,Y_v; general units are not quotiented out. Set

\[
 R=\begin{pmatrix}0&-1\\1&-1\end{pmatrix},\quad
 T=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
 G=\{\lambda R^iT^j: \lambda=\pm1,\;i=0,1,2,\;j=0,1\}.
\]

**Theorem GM [PROVED].** If gcd(n,6)=1, each parameter in Ω_n gives two
different homometric T/I classes. For v,w∈Ω_n,

\[
 \Phi(v)=\Phi(w)\quad\Longleftrightarrow\quad w\in Gv.
\]

The G-action is free. The number of represented unordered pair edges is

\[
 B_\Omega(n)=\big[(n-1)(n-11)+24[5\mid n]+24[7\mid n]\big]/12.
\]

The correction terms use the separately proved and attacked odd support
lemma in `notes/2026-09-30-six-composite-counting.md`, §2. In particular
the formula simplifies to(n−1)(n−11)/12 if all prime divisors are at
least11. This is a stronger threshold than the original requested
prime-divisors≥13 scope; the finite table below supplies the additional
5/7/11 exclusions explicitly.

**Theorem GE [PROVED].** If gcd(n,6)=1 and31∤n, the Bloom graph on Ω_n
is a disjoint union of edges. For arbitrary gcd(n,6)=1, any endpoint
having two different Bloom partners is an ordinary inflation of an
actual six-element Bloom endpoint in Z/31. Every shared-endpoint
identification between different global Bloom pairs is induced by a
shared-endpoint identification in that field, followed by the unique
order31 subgroup embedding Z/31→Z/n. Thus multiple partners are possible
only when31|n and are confined to order31-supported sets up to T/I.

The exact field31 Bloom graph consists of45 disjoint edges and one
five-cycle, independently rebuilt from the immutable reference and
compared with the inherited full parameter certificate. Therefore the
global Bloom graph consists of disjoint edges together with exactly one
inflated five-cycle if31|n. Neither theorem excludes non-Bloom homometric
partners.

## 2. Complete finite systems; no hidden symmetry reduction

Since2 and3 are units, the six **scaled centered coordinates** are

\[
 C_X=\begin{pmatrix}2&-4\\5&-4\\-4&-1\\-4&2\\2&2\\-1&5\end{pmatrix},\quad
 C_Y=\begin{pmatrix}-1&-4\\2&-4\\5&-1\\-4&2\\2&2\\-4&5\end{pmatrix}.
\]

Each coordinate equals3(x−μ), with μ the mean of its endpoint list.
Translation removes the mean and reflection negates the list. Equality
of the unordered pairs therefore gives a global endpoint assignment
j∈{0,1}, independent signs ε_X,ε_Y∈{±1}, and independent label
permutations π_X,π_Y∈S_6 such that

\[
 C_Xw=\epsilon_X(U_Xv)_{[\pi_X]},\qquad
 C_Yw=\epsilon_Y(U_Yv)_{[\pi_Y]},
\]

where (U_X,U_Y)=(C_X,C_Y) if j=0 and (C_Y,C_X) if j=1. The global
supports are actual sets, so these permutations exist even when their
local projections have repeated entries. The method never asks for
locally unique matchings or a parity rule for repeated labels.

Enumerating j, the two signs and all720 permutations at each endpoint
gives exactly2·4·720²=4,147,200 cases. **No cases are quotiented out.**
The first two rows A of C_X satisfy det(A)=12 and

\[
 12A^{-1}=\begin{pmatrix}-4&4\\-5&2\end{pmatrix}.
\]

The first two equations determine an integer matrix M with12w=Mv.
Substitution in the remaining ten equations gives an integer10×2 matrix
H with Hv=0. This elimination is equivalent to the original matching
over every Z/n under consideration because12 is a unit.

For a residual matrix write c=gcd of its20 entries and D=gcd of all45
two-by-two minors. The two nonzero Smith factors are c,D/c when rank2.
The script records these quantities and example full matrices, not just
floating ranks. All entries and minors are signed integers and their gcds
are nonnegative. A safe direct coefficient bound is |H_ij|<500 and
|det(H_r,H_s)|<500,000, many orders below int64 overflow.

## 3. Exact paired table and acceptance conditions

The complete table, including39 rank-one (direction,c) histogram entries,
46 rank-two (c,D) entries, and all48≥11 exceptional full systems, is in
`results/2026-09-30-six-composite-global-matrix/matching-certificate.json`.
The exact observed partition is:

| Residual rank | Number of cases | Required property |
|---|---:|---|
|0|12|M=12g for one of the twelve g∈G; swap j equals g's T exponent|
|1|864|primitive direction is a support-collision normal; c∈{9,18,36,72}|
|2|4,146,324|c has only2/3 factors; D after removing2/3 factors is1,5,7,13 or19|

More precisely, the rank-two cases grouped by the part of D coprime6
are:

| coprime6 part of D | Cases |
|---:|---:|
|1|4,144,428|
|5|936|
|7|912|
|13|24|
|19|24|

There is **at most one** prime≥5 in any D, and its valuation is exactly
one. The13/19 systems have (c,D)=(3,1404),(12,5616),(3,2052),
(12,8208), twelve cases each. No determinant contains two exceptional
prime directions or a higher exceptional prime power. This exact
property is what prevents globally surviving mixed CRT collisions.

The twelve primitive collision normals, up to sign, are

\[
 (1,0),(0,1),(1,-1),(1,1),(2,-1),(2,1),(3,-1),
 (1,-2),(1,2),(3,-2),(1,-3),(2,-3).
\]

They arise by subtracting pairs of actual coefficient rows. The omitted
scale on every original difference has only2/3 factors, so each primitive
normal is equivalent to its original collision equation under gcd(n,6)=1.

These are the complete acceptance conditions for the proof. In
particular, the proof does not use the optional48 stored witnesses that
adding M−12g preserves the prime≥11 minor gcd, although those are also
replayed exactly by the checker.

## 4. Rank-two torsion lemma

**Elementary lemma.** Suppose H has rational rank2, Hv=0 modulo n,
and D is its two-by-two-minor gcd. Then Dv=0 modulo n.

For every pair of rows B, the equations Bv=0 give det(B)v=0 by
multiplying by adj(B). The integer gcd D is an integer linear combination
of these finitely many determinants by the Euclidean algorithm. Taking
that combination gives Dv=0. No Smith decomposition, division by an
individual minor or assumption about primitive v is required.

Under gcd(n,6)=1, write D=u or D=up, where u has only2/3 factors and
p∈{5,7,13,19}. Since u is a unit modulo n, the first case gives v=0.
The second gives pv=0. If p∤n this again gives v=0. Otherwise both
coordinates lie in the unique order-p subgroup

\[
 K_p=(n/p)\,\mathbb Z/n\cong\mathbb F_p.
\]

Indeed n|px implies n/p|x, and conversely. This description applies
equally when p²|n and when n has many other prime factors. The equation
12w=Mv puts w in the same subgroup because12 is a unit.

Put v=(n/p)v_0 and w=(n/p)w_0, with v_0,w_0∈F_p². The subgroup
embedding is injective, so both lists have six distinct global entries
if and only if their field lists have six distinct entries. Moreover any
rigid transport between two supported sets has its translation in K_p:
choose a matched point and subtract it and its reflected source point.
The translation is a difference of two K_p points. Therefore all rigid
equivalences and unordered pair equalities descend to the field.

This lemma explains exactly why different local collision directions
cannot combine to create an unclassified globally six-point solution:
a nonformal matching forces all parameters into **one order-p subgroup**.

## 5. Proof of GM

Apply the exhaustive matching table to an actual pair equality.

Rank0 gives w=gv immediately. Rank1 gives cℓ(v)=0, where ℓ is one
primitive collision normal: write every row as h_rℓ and use gcd(h_r)=c,
which follows because the entries of ℓ are coprime. Since c is a unit,
ℓ(v)=0 exactly, contradicting v∈Ω_n.

In rank2 the lemma leaves only field inflations at5,7,13 or19. There are
no six-point subsets at5. At7 the twelve collision normals reduce to
eight distinct projective lines, the entire projective line P¹(F_7).
Every field parameter lies on a collision line, so Ω_7 is empty. The
checker independently counts these eight directions from actual point
differences. Consequently only13 and19 remain. The accepted field
Theorem A in `notes/2026-09-30-six-prime-theorem.md` applies to their
actual six-point lists and gives w_0∈Gv_0. Inflate to obtain w∈Gv.
This proves the forward implication for every gcd(n,6)=1. Conversely,
the integer coefficient identities for R,T and negation preserve the
unordered pair in every ring, as already checked in the accepted prime
and composite notes.

To show the endpoints are distinct, assume X_v and Y_v are rigidly
equivalent. Using the transport in one direction and its inverse gives
a swapped pair equality with w=v. In rank0 its matrix is one of
±R^iT. The fixed-vector equations for these six matrices force one of
a=0,b=0,a=b,a=−b,a=2b,b=2a, because2 is a unit; each is a support
collision. Rank1 already contradicts actual support. Rank2 reduces to
actual field13/19 lists whose endpoints are different by the accepted
field theorem. This contradiction proves global noncongruence.

The group action is free: the reflection fixed-vector cases are the
same six collision lines. The other five nonidentity G matrices have
fixed-vector determinants1,3 or4, units when gcd(n,6)=1, and hence fix
only zero. No nonidentity g fixes a parameter in Ω_n.

Finally, if all prime divisors are at least11, the nonzero determinants
between distinct collision normals have absolute values in
{1,2,3,4,5,7,8}, all units modulo n. Each primitive line has exactly n
points, and any two meet only at zero. The union of the twelve lines
therefore has1+12(n−1) points; its complement has(n−1)(n−11) points.
Divide once by the free global orbit size12 to obtain the simplified
count. For general gcd(n,6)=1 the separately accepted odd support lemma
gives |Ω_n|=(n−1)(n−11)+24[5|n]+24[7|n]. Divide by the same free orbit
size to obtain the complete count formula in §1. Its support-lattice
inclusion–exclusion certificate is an explicit retained dependency.

## 6. Exact single-endpoint table

Sharing one endpoint gives an equation

\[
 C_Sw=\epsilon(C_Uv)_{[\pi]},\quad S,U\in\{X,Y\},\;
 \epsilon=\pm1,\;\pi\in S_6.
\]

There are exactly4·2·720=5,760 cases, with no quotient. The first two
rows of either source matrix have determinant12. For C_Y the adjugate
used in elimination is[[-4,4],[-2,−1]]. Substitution leaves four rows H.
The exact complete partition is:

| Rank | Cases | Property |
|---|---:|---|
|0|24|M=12g for some g∈G|
|1|432|a collision normal; c∈{9,18,36,72}|
|2|5,304|c has only2/3 factors; coprime6 part of D is1,5,7,11,13,19 or31|

The rank-two partition by the coprime6 part of D is:

| coprime6 part of D | Cases |
|---:|---:|
|1|4,632|
|5|144|
|7|144|
|11|288|
|13|24|
|19|24|
|31|48|

Every nontrivial coprime6 part is one prime to exponent one. The file
`endpoint-certificate.json` gives the complete29 rank-two histogram
entries, all24 rank-zero matrices, all432 rank-one matrices and all384
systems exceptional at primes≥11. Here too the5/7 systems are completely
counted in the histogram and do not need individual storage for the proof.

## 7. Proof of GE

Rank0 gives the same G-orbit and hence the same Bloom pair. Rank1 forces
a global support collision. The rank-two lemma reduces any surviving
identification to one order-p subgroup, now with
p∈{5,7,11,13,19,31}. The5/7 exclusions apply as before. At11 the twelve
collision normals give all twelve projective directions, so Ω_11 is
empty as well; the checker verifies this directly. At13/19 the accepted
field unique-partner Theorem C gives the same pair. At31 the global
identification is exactly an inflation of the actual field one. Thus
two distinct Bloom pairs sharing an endpoint can occur only in the
order31 subgroup up to translation/reflection. Conversely every field31
shared-endpoint identification inflates whenever31|n, and subgroup
injectivity preserves all support and rigid-class distinctions.

There is a unique order31 subgroup when31|n. All field31 edges inflate
to a single graph on its rigid classes; inflation is injective on rigid
classes by the transport argument in §4. Every global vertex of degree
at least two belongs to this inflated graph. The field graph certificate
shows one five-cycle and otherwise edges, so the full global graph has
exactly that one five-cycle and otherwise disjoint edges.

This proves the claimed unique-partner scope and the exact source of its
31 exceptions, conditional only on the complete finite tables and the
accepted field theorem. It does not silently extend field uniqueness to
CRT; the exhaustive global matching is what performs that reduction.

## 8. Verification and reproduction

Runtime was estimated from72,000 cases before the full run. The benchmark
took about0.011seconds; the full C++ paired run took under one second.
No long job, subset census or all-cardinality enumeration was launched.

```bash
clang++ -O3 -std=c++17 src/six_composite_matching.cpp -o results/2026-09-30-six-composite-global-matrix/matching-enumerator
results/2026-09-30-six-composite-global-matrix/matching-enumerator --out results/2026-09-30-six-composite-global-matrix/matching-certificate.json
results/2026-09-30-six-composite-global-matrix/matching-enumerator --endpoint --out results/2026-09-30-six-composite-global-matrix/endpoint-certificate.json
.venv/bin/python tests/test_six_composite_matching.py --full
```

The independent complete paired method uses the **first two Y equations**
as its pivot, exact int64 batches and all45 minors. It agrees with all
39 rank-one histogram entries and all46 rank-two histogram entries as
well as the12/864/4,146,324 rank counts. The independent single-endpoint
method does **no elimination**: it constructs the original6×4 equations
and uses permutation-expansion determinants of all4×4 minors, and all
3×3 minors where necessary. It agrees with24/432/5,304 and the complete
exceptional-prime partition. These methods also independently confirm
the headline case counts without relying on the classification proof.

The tests replay every retained matrix and check every exceptional
actual-support field solution against canonicalization and ICV from
the immutable `src/homometry.py`. They verify Ω_5,Ω_7,Ω_11 are empty,
including the exact projective-line exhaustion at7/11. The tests also
reconstruct all50 field31 Bloom pair edges with reference T/I
canonicalization and compare them with the inherited complete direct
certificate. `field31-graph.json` retains its45 size-two components and
the full five-cycle classes and edges. This is the bounded field graph
dependency for the corresponding global assertion.

All code is in the pinned project environment. Certificate SHA256 values and exact
independent results are in `independent-audit.json`; logs retain commands'
outputs. The source/header and certificate hashes will be frozen after
fresh review. The separate fresh review accepts the theorem, all finite acceptance
conditions and the exact field31 graph. No historical priority or novelty conclusion follows.
