# Composite six-point counting: exact domains and remaining gluing obstruction

30 September 2026. **[PROVED] in the explicitly bounded scopes below, after a separate
fresh adversarial attack; the full coprime-to-six classification is proved in §5;
unrestricted modulus classification remains [OPEN].**
Full proofs of the prime-power and CRT orbit theorems are in
`notes/2026-09-30-six-composite-algebra.md`; their separate fresh attack is
`notes/2026-09-30-six-composite-review.md`. This synthesis makes no novelty
claim. It preserves translation/inversion classes and does not identify
general unit images.

## 1. Exact scope of the new classification

Use the classical labelled X,Y configurations from the field theorem.
Write Ω_n for parameters whose two supports have size six modulo n.
For n with every prime divisor at least13, write n=∏q, q=p^k,
and distinguish these invariant parameter domains:

* H_n: each support has size six in **every prime-power factor** Z/q.
* L_n: H_n together with e=ab(a−b) and
  d=(a+b)(2a−b)(a−2b) units modulo n.
* F_n: each support has size six modulo **every prime divisor**.

Thus F_n⊆L_n⊆H_n⊆Ω_n. These inclusions need not be equalities.

The local theorem PP classifies **all Ω_(p^k)** for every
prime p≥13 and every k≥1, including nonunits, reductions with colliding
points, and ordinary subgroup inflation. Its parameters for each pair
are exactly one free orbit of

\[
 G=\{\pm I,\pm R,\pm R^2,\pm T,\pm RT,\pm R^2T\}
 \cong S_3\times C_2.
\]

There are no congruent endpoints in that domain. Its exact number of
unordered pairs of distinct T/I classes is therefore

\[
 B(p^k)=\frac{(p^k-1)(p^k-11)}{12}.
\]

This is stronger than faithful reduction modulo p. The proof divides a
common p-factor until primitive, uses the integer moments on six-labelled
lists modulo p even when points coincide, and aligns parameters by their
cubic root multisets. In the six singular reflection directions it reduces
to two normal forms, b=0 and b=2a modulo p. The complete 32+8 exact lift
systems force either an actual support collision or one of the formal G
maps. Their integer Bézout certificates have denominators and nonzero gcds
with only2 and3 as prime factors. Finite sampled moduli are not the proof.

The CRT theorem on H_n uses one global labelled point matching.
Formal parameter transports induce even permutations. If a global endpoint
sign disagrees with a local G sign, the difference is a reflection of an
actual local six-element set, whose permutation is three transpositions
and hence odd. Parity forces a common local sign. At least one endpoint
has no such reflection, so its point permutation forces a common rotation
index. Consequently the same single G element works in every factor.
This is the compatibility information missing from even moments alone.

It gives the exact H_n count

\[
 B_H(n)=\frac1{12}\prod_{p^k\Vert n}(p^k-1)(p^k-11).
\]

There is only one global division by twelve, not twelve per CRT factor.
The L and F subdomains have the counts

\[
 B_L(n)=\frac1{12}\prod_{p^k\Vert n}
 \bigl[p^{2k-2}(p-1)(p-5)-6p^{k-1}(p-1)\bigr],
\]
\[
 B_F(n)=\frac1{12}\prod_{p^k\Vert n}p^{2k-2}(p-1)(p-11).
\]

**Conditional total-count corollary.** The inherited Theorem G and its
large-prime reduction make every cyclic six-pair Bloom when every prime
divisor of n exceeds131. For n=p^k with p>131, the PP theorem
therefore yields the total pair-edge count (n−1)(n−11)/12. This corollary
retains G's solver/finite-certificate dependencies. The accepted unique-
partner theorem below makes every nontrivial family size two, so the same
formula also counts maximal nontrivial families in this prime-power scope.

**Unique partners [PROVED].** At every prime power p^k with p≥13,
p≠31, an actual six-element Bloom endpoint has one Bloom partner. The
single-endpoint moment determinant is −2^4·3^12·31. An independent complete
sixteen-plus-eight singular lift table handles the repeated residue labels;
its nonzero residual gcds force exact collisions. The paired classification
and its count do not exclude31, but endpoint uniqueness must.

On H_n, when31∤n, every endpoint has a unique partner in the **entire
Bloom image**, not just within H_n. A shared-endpoint matching glues by
parity and the disjoint reflection cosets at13 and19. The weighted
zero-autocorrelation identity ensures any Bloom parameter sharing an H_n
endpoint automatically belongs to H_n. Thus the H_n graph consists of
disjoint edges and its Bloom-family count equals B_H(n). This does not
exclude partners from other homometry mechanisms. Full details and fresh
attack: algebra note §§10–11 and the separate review. H_n here is exactly
S_n in that note; the different letters are aliases for the same domain.

## 2. An elementary exact support-count lemma for every odd modulus

**Support lemma [PROVED], independently attacked.** For every odd n≥3, the
number of parameters with six distinct coordinates on both sides is

\[
 |\Omega_n|=n^2-12n+11+16[3\mid n]+24[5\mid n]+24[7\mid n].
\]

Here [p|n] is1 or0 according as p divides n or does not. This counts
parameters, not pair classes, and it remains true at small moduli where
there are no six-element supports. Dividing it by twelve is not justified
without an independently proved fiber classification in the desired scope.

Proof. The common fifteen coefficient differences give exactly twelve
primitive collision kernels, because the only discarded factors are2,
which is a unit when n is odd. Their normals are

\[
 (1,0),(0,1),(-1,1),(1,1),(-2,1),(2,1),(-3,1),
 (-1,2),(1,2),(-3,2),(-1,3),(-2,3).
\]

Each primitive linear kernel has n points. Every pair of different
normals has nonzero absolute determinant in{1,2,3,4,5,7,8}. If v
lies on two kernels then that determinant annihilates v by the adjugate
identity. In an odd ring, a nonzero such v has additive order precisely
3,5 or7. For different orders those point sets are disjoint. At an
order-p point, v=(n/p)u with nonzero u∈F_p²; the number r of kernels
through it is the number of reduced normals orthogonal to its projective
direction. The twelve lines reduce to respectively d_p=4,6,8 distinct
directions at p=3,5,7, and every nonzero direction is covered there.
Consequently Σ_directions(r−1)=12−d_p, and each direction contains p−1
nonzero u. The overcount away from the origin in the sum of the twelve
kernel sizes is thus (12−d_p)(p−1):16,24,24 respectively, when p|n.
The origin was counted twelve times and needs correction11. Subtract
the resulting union size from n² to obtain the formula. This argument
also covers higher powers of3,5,7: any point on two kernels is killed by
a determinant with only first power of that odd prime, so no new
higher-order overlap points occur. End proof.

For n with all prime divisors≥13 this simplifies to |Ω_n|=(n−1)(n−11).
For n637=7²·13 it gives398160 parameters. The direct image has33180
pairs, while the uncorrected large-prime quadratic would give33178.
The support formula explains the arithmetic difference without promoting
full-domain pair classification at n637 to a theorem.

The independent inclusion–exclusion implementation uses all4096 subsets
and their exact two-column Smith factors. Its aggregated rank-two weights
are {1:−16,2:3,3:8,4:3,5:6,7:4,8:3}, giving equivalently

\[
 n^2-12n-7+8\gcd(n,3)+6\gcd(n,5)+4\gcd(n,7)
\]

for odd n. This computation independently confirms the elementary formula.
The general Smith/gcd counting framework is established prior art in
Kamiya–Takemura–Terao2008; the renewed primary-source reading is logged in
`notes/2026-09-30-six-composite-literature.md`. No new general counting
method or quasipolynomial-existence claim is made here.

## 3. The former gluing gap and its eventual resolution

At n221=13·17, choose v=(1,104). Its global lists are

\[
 X_v=(0,1,102,206,208,90),\quad
 Y_v=(0,1,106,207,209,90)\pmod{221}.
\]

Both have six distinct entries. Modulo13 the parameter is(1,0), so
each labelled list has only four distinct values. Modulo17 it is(1,2),
and each list has five distinct values. Thus v∈Ω_221 but v∉H_221.
Local repeated labels defeat the permutation-parity proof as presently
written: a local matching can permute equal labels without changing the
projected multiset. The direct full image at221 has3850 pairs but H_221
has192, so the omitted region was substantial. This obstructed the
original parity proof. The complete coefficient proof in §5 now covers
it without changing support or rigid-class definitions.

**Former full global conjecture — [PROVED], now closed by §5.** For every n whose prime divisors are
at least13, every Ω_n pair fiber is still one free G-orbit. The full Bloom count is(n−1)(n−11)/12 in this scope. The sampled
checks support it; the proof for locally repeated labels is the separate
global argument, not an inference from PP or H.
The old n221 mixed-sign example continues to show that matching moment
invariants alone cannot settle this gluing problem. General unit
multiplication must not be included as an equivalence to remove it.

## 4. Independent exact computations and reproduction

The point enumerator uses actual anchored coordinates and no moment
or count formula to group its image. All pair fibers and excluded
parameters are retained in exact compressed certificates. The independent
arithmetic implementation imports no point canonicalizer: it verifies
all parameter locations by collision equations and every fiber by
permutations of the ordered cubic roots, binds the domain counts to
their independent formulas and records every direct certificate digest.

Complete cyclic six-subset census is still6..135. These computations
enumerate two-parameter images, not all six-subsets at the larger moduli.
Exact commands and benchmark records are in the two dated output folders:

```bash
.venv/bin/python src/six_composite_bloom.py --moduli 169 221 289 247 323 361 529 637 2197 403 961 --resume
.venv/bin/python src/six_composite_arithmetic.py > results/2026-09-30-six-composite-arithmetic/replay.log
.venv/bin/python tests/test_six_composite_bloom.py
.venv/bin/python tests/test_six_composite_arithmetic.py
.venv/bin/python src/six_prime_power_lifts.py
.venv/bin/python src/six_prime_power_endpoint_lifts.py
.venv/bin/python src/six_composite_auxiliary.py
.venv/bin/python tests/test_six_prime_power_lifts.py
```

Published constructions and the general counting methods are credited
in the new literature pass. Historical novelty remains unestablished.
There is no Lean formalization, external review or public submission.

## 5. Full global classification established on 1 October2026

**[PROVED], in-house, computer-assisted, after the complete separate
fresh adversarial attack.**
The complete coefficient-matching proof in
`notes/2026-09-30-six-composite-global-matrix.md` removes every local-support
restriction. For every n≥2 with gcd(n,6)=1, all support-admissible Bloom
parameters give distinct homometric T/I endpoints, and every pair fiber
is exactly one free G-orbit. The exact full Bloom pair count is

\[
 B(n)=\frac{(n-1)(n-11)+24[5\mid n]+24[7\mid n]}{12}.
\]

The numerator is the support lemma in §2, with3∤n. Thus the formula
includes the small-prime corrections instead of silently narrowing the
classification to avoid them. If5,7∤n it is the quadratic(n−1)(n−11)/12.
No general unit quotient is used. At221 the previously omitted3658 pairs
are now covered by this coefficient argument; the moment-key refutation
remains valid because moments are not the gluing proof.

The complete matching space has4,147,200 paired systems. Each residual
matrix has rank zero (one formal G map), rank one (an exact collision),
or rank two. The rank-two minor gcd has at most one prime≥5, with
valuation one. Adjugate equations and Bézout therefore force the entire
parameter into one order-p subgroup, regardless of how many prime powers
divide n. Fields5/7 supply no actual six-point support; fields13/19 give
the accepted field G orbit. An independent full Y-pivot implementation
agrees with every histogram class, and a second conceptual proof for all
prime factors≥13 uses only219 paired point-permutation patterns. These
are finite coefficient classifications that prove arbitrary-modulus
statements, rather than finite modulus censuses.

All5760 one-endpoint matching systems similarly reduce to formal maps,
collisions or order-p subgroup inflations. The possible extra primes are
11 and31: Ω_11 is empty, and31 supplies the sole shared-partner exception.
Consequently if31∤n each Bloom endpoint has one Bloom partner. If31|n,
the entire Bloom graph has exactly one inflated31 five-cycle and otherwise
isolated edges. Its number of connected nontrivial Bloom components is
`B(n)−4[31|n]`; these components are not asserted to include every possible
non-Bloom homometric partner. The field31 graph has been independently
reconstructed from all600 admissible parameters and all50 pair edges.

**Conditional total-six-count corollary.** If every prime divisor of n
exceeds131, the inherited Theorem G makes every cyclic six-pair Bloom.
The new theorem therefore gives `(n−1)(n−11)/12` total pair classes and
maximal nontrivial families for **all such composite n and prime powers**,
each family of size two. This retains G's solver/finite-certificate
dependencies. Its scope is broader than the original prime-power
corollary in §1, and does not claim a total count at other moduli.

The original full-global conjecture in §3 is closed by this theorem.
The remaining classification/counting obstruction is the2/3-primary part
(where centering and the determinant12 pivot are not invertible), together
with a disjoint accounting of non-Bloom cyclic constructions and their
overlaps at small prime divisors. Arbitrary-n generation G was already
closed; unrestricted disjoint classification and counting remain separate.
Historical originality is unestablished.

Complete proofs and separate fresh attack:
`notes/2026-09-30-six-composite-global-matrix.md`,
`notes/2026-09-30-six-composite-global-attempt.md`,
`notes/2026-09-30-six-composite-global-review.md`.
Reproduction:

```bash
.venv/bin/python tests/test_six_composite_matching.py --full
.venv/bin/python src/six_composite_weighted_gluing.py
.venv/bin/python tests/test_six_composite_weighted_gluing.py
.venv/bin/python src/six_composite_bloom.py --moduli 25 35 49 55 65 77 91 121 143 187 209 341 --out results/2026-09-30-six-composite-global-controls --resume
.venv/bin/python src/six_composite_arithmetic.py --direct results/2026-09-30-six-composite-global-controls --out results/2026-09-30-six-composite-global-control-audit
```

The23 exact sampled images cover7310663 parameter candidates and601526
pair fibers, largest modulus2197; they are independently checked. Complete
six-subset census remains6..135. No paper source or existing media is edited
by this checkpoint.
