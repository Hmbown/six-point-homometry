# Six-point homometry over fields: exact Bloom classification and counting

30 September 2026. **[PROVED], in-house:** Theorems A–C have a direct
algebraic proof accepted by a separate fresh adversarial review.
**[PROVED], computer-assisted, with inherited dependencies:** Corollaries
D–E use the earlier generation theorem G; E also uses the complete
two-method small-prime censuses. No historical novelty or external peer
review is claimed. Attack log: `notes/2026-09-30-six-prime-review.md`.
The two point configurations are classical. The object classified below is
their image under translation and inversion, without a quotient by general
field multiplication. This is a direct algebraic theorem: its proof uses
neither a finite census nor the computer-assisted general generation theorem.
The total-count corollaries retain the dependencies explicitly stated above.

## 1. Definitions and statements

Let K be a field of characteristic other than 2, 3, or 11. For v=(a,b) in
K² put

\[
 X_v=\{0,a,b-2a,2b-2a,2b,3b-a\},\qquad
 Y_v=\{0,a,b+2a,2b-a,2b+a,3b-a\}.
\]

Let Ω_K consist of parameters for which both displayed lists have six
distinct entries. Two sets are **rigidly equivalent** if B=εA+t for
ε in {1,−1} and t in K. We count the unordered pair
Φ(v)={ [X_v], [Y_v] } of rigid classes. The two classes may be translated
and inverted independently. No other nonzero scalar multiplication is
identified. In F_p these are precisely cyclic T/I classes; in F_(p^r)
with r>1 the additive group is elementary abelian and is not cyclic.

For finite sets A, define directed autocorrelation by

\[
 c_A(h)=\#\{(x,y)\in A^2:x-y=h\}\quad(h\in K).
\]

Homometry means c_A=c_B. In a cyclic group of odd prime order this is
equivalent to equality of interval-class vectors. The finite-field
extension concerns additive differences, not an ordered notion of length.

**Theorem A (exact image classification).** Every v in Ω_K gives a
homometric pair of different rigid classes. Define

\[
 R=\begin{pmatrix}0&-1\\1&-1\end{pmatrix},\quad
 T=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
 G=\{\pm I,\pm R,\pm R^2,\pm T,\pm RT,\pm R^2T\}.
\]

G is a group of order twelve isomorphic to S₃×C₂, acts freely on Ω_K,
and preserves Φ. For v,w in Ω_K the following are equivalent:

1. Φ(v)=Φ(w).
2. w is in Gv.
3. s(v)=s(w) and e(v)²=e(w)², where
   s=a²−ab+b² and e=ab(a−b).

Thus each pair has exactly twelve parameters, including every accidental
equality after projection, not just the formal planar symmetries.

**Theorem B (finite-field count).** For K=F_q in the allowed
characteristic, the number of distinct unordered Bloom pairs is

\[
 B(q)=\begin{cases}
 (q-1)(q-5)/12,&\operatorname{char}K=5,\\
 (q-1)(q-7)/12,&\operatorname{char}K=7,\\
 (q-1)(q-11)/12,&\operatorname{char}K\ge13.
 \end{cases}
\]

In particular B(p)=(p−1)(p−11)/12 for every prime p≥13. The original
lists produce no six-element pair in F₂,F₃,F₅,F₇,F₁₁. Theorems A–B
do not classify the Bloom image in extension fields of characteristic
2, 3, or 11.

**Theorem C (unique Bloom partner).** If the characteristic is also
different from 31, no two distinct pairs in the Bloom image share a rigid
class. Equivalently, the graph whose vertices are the rigid classes and
whose edges are Bloom pairs is a disjoint union of edges. This does not
exclude extra homometric partners outside the Bloom image.

**Corollary D (total cyclic six-point count, conditional on G).** Use the
earlier computer-assisted Theorem G and its large-prime corollary in
`notes/2026-09-30-six-paper.tex`: at every prime p>131, all nontrivial
six-point homometric pairs in Z_p are Bloom pairs. Then the total number
of such unordered pairs, and of maximal nontrivial six-point families, is
(p−1)(p−11)/12, and every such family has exactly two rigid classes.
Theorem G's finite certificate/solver obligations remain dependencies of
this total-count assertion. A–C themselves do not depend on them.

**Corollary E (all prime cyclic counts, with finite dependencies).** In
addition to G, use the previously independently checked complete six-set
census at primes ≤131. For primes p≥13, write B(p)=(p−1)(p−11)/12
and [p=r]=1 if p=r, zero otherwise. The total number of unordered
nontrivial pair edges is

\[
 P_6(p)=B(p)+8[p=17]+9[p=19]+11[p=23]+20[p=31].
\]

The total number of maximal nontrivial families is

\[
 F_6(p)=B(p)+8[p=17]+9[p=19]+11[p=23]+11[p=31].
\]

Every family has size two except one family of size five in Z₃₁.
At primes less than 13 there are no nontrivial six-set families.
This is a computer-assisted corollary with explicit finite-census and
G dependencies; it is not claimed as a pure algebraic classification of
the small-prime extra pairs.

## 2. Homometry and support collisions

The configurations in coefficient space are

\[
 P=((0,0),(1,0),(-2,1),(-2,2),(0,2),(-1,3)),
\]
\[
 Q=((0,0),(1,0),(2,1),(-1,2),(1,2),(-1,3)).
\]

The fifteen differences from either configuration, taken up to sign with
multiplicity, are the same list:

\[
 a,\ b-2a,\ 2b-2a,\ 2b,\ 3b-a,\ b-3a,\ 2b-3a,
\]
\[
 2b-a,\ 3b-2a,\ b,\ b+2a,\ 2b+a,\ 2a,\ b-a,\ b+a.
\]

Replacing each entry ℓ by the two directed entries ℓ and −ℓ, and
including six diagonal zero differences, proves equality of directed
autocorrelations whenever both supports have size six. Distances need
not be distinct. This is an integer coefficient identity, so homometry
survives reduction into every additive group, although collisions must
be dealt with before interpreting lists as six-element sets.

In the allowed characteristic, collision occurs exactly on the union of
the following twelve linear kernels:

\[
 a,\ b,\ b-a,\ b+a,\ b-2a,\ b+2a,\ b-3a,
 2b-a,\ 2b+a,\ 2b-3a,\ 3b-a,\ 3b-2a.
\]

This follows by setting each displayed difference to zero, removing only
the invertible factors 2. Some kernels coincide in characteristics 5 and
7; the description as a union is still exact. In particular, on Ω_K

\[
 e=ab(a-b)\ne0,\qquad
 d=(a+b)(2a-b)(a-2b)\ne0.
\]

These six factors occur among the collision kernels.

## 3. The free twelve-element action

The relations R³=T²=I, TRT=R⁻¹, and central −I show that G is a
group. The six indicated matrices and their negatives are distinct in
characteristic different from 2 and 3, as inspection of their entries
shows. Thus G≅S₃×C₂. Exact coefficient identities give:

| M | X_(Mv) | Y_(Mv) |
|---|---|---|
| I | X_v | Y_v |
| R | X_v+2a−2b | Y_v+a−3b |
| R² | X_v−2b | Y_v−2a−b |
| T | Y_v+a−2b | X_v+2a−b |
| RT | Y_v−a | X_v−a |
| R²T | Y_v−a−2b | X_v+a−3b |

For −M negate the sets and translations on the right. Consequently G
preserves Ω_K and Φ. Each endpoint's translation is allowed to differ.

The only fixed vector of R or R² is zero because det(R−I)=
det(R²−I)=3. The only fixed vector of −R or −R² is zero because
det(R+I)=det(R²+I)=1. The same holds for −I since 2 is invertible.
The fixed lines of T,−T,RT,−RT,R²T,−R²T are respectively

\[
 b=a,\quad b=-a,\quad a=0,\quad a=2b,\quad b=0,\quad b=2a.
\]

Every one is a collision line. Zero is inadmissible, so the action is
free. This proves an orbit has twelve parameters; it does not yet show
that different orbits give different projected pairs. That is the next
step.

## 4. Algebraic moment invariants separate all projected pairs

For a six-element set A put μ_A=(Σ_(x∈A)x)/6 and define the scaled
centered moment

\[
 m_j(A)=\sum_{x\in A}\bigl(3(x-\mu_A)\bigr)^j.
\]

Translation leaves every m_j unchanged; inversion multiplies it by
(−1)^j. Hence m₂,m₆,m₃² are invariants of a rigid class. Their sums
over the unordered endpoints are invariants of Φ.

Direct polynomial expansion gives

\[
 d^2+27e^2=4s^3,\qquad m_2(X_v)=m_2(Y_v)=66s,
\]
\[
 m_3(X_v)=6d-243e,\qquad m_3(Y_v)=6d+243e,
\]
\[
 m_6(X_v)=23946s^3+6399e^2-4860de,
\]
\[
 m_6(Y_v)=23946s^3+6399e^2+4860de.
\]

For reproducibility, these are identities over Z: the scaled centered
coordinates are 3x−(Σx)/2, and ΣX=−4a+8b, ΣY=2a+8b.
Thus the coordinates are integral linear forms:

\[
 X:\ (2a-4b,\ 5a-4b,\ -4a-b,\ -4a+2b,\ 2a+2b,\ -a+5b),
\]
\[
 Y:\ (-a-4b,\ 2a-4b,\ 5a-b,\ -4a+2b,\ 2a+2b,\ -4a+5b).
\]

Raising these six linear forms to the stated powers and summing verifies
every moment identity. No division in a polynomial expansion is needed.

Put

\[
 C_3=m_3(X_v)^2+m_3(Y_v)^2-288s^3=116154e^2,
\]
\[
 C_6=m_6(X_v)+m_6(Y_v)-47892s^3=12798e^2.
\]

Since 116154=162·717, 12798=162·79, and
118·79−13·717=1, the exact elimination identity is

\[
 118C_6-13C_3=162e^2.
\]

The constant 66 is invertible in the stated characteristic, as is 162.
Thus Φ(v)=Φ(w) implies s(v)=s(w) and e(v)²=e(w)². Using both
C₃ and C₆ avoids losing characteristic 239 or 79 through division by
one coefficient. We never divide by s; isotropic parameters s=0 are
fully included.

Conversely these two invariants determine the G-orbit. The cubic identity

\[
 (z-a)(z+b)(z-b+a)=z^3-sz-e
\]

has ordered roots (a,−b,b−a). From equality of e² we have
e(w)=e(v) or e(w)=−e(v); replace w by −w in the second case.
The two ordered root triples then factor the identical monic cubic, so
their root multisets are equal, including multiplicities. The map R
cyclically permutes that triple; −T transposes the first two entries.
They realize all six permutations. Since the first two entries recover
a,b, the aligned w is in the group generated by R and −T; restoring a
possible negation puts the original w in Gv. This also proves that the
two invariant values characterize G-orbits over any allowed field.

Finally, the two endpoint classes are different: equality would force
equality of their squared third moments, while

\[
 m_3(X_v)^2-m_3(Y_v)^2=-5832de\ne0.
\]

Here 5832 has only 2 and 3 as prime factors, and d,e are nonzero on Ω_K.
This completes Theorem A. In particular there is no extra congruence
exclusion to subtract from the support-admissible parameters.

## 5. Counting the line complement over a finite field

Represent the collision kernels by the primitive normals

\[
 (1,0),(0,1),(-1,1),(1,1),(-2,1),(2,1),(-3,1),
 (-1,2),(1,2),(-3,2),(-1,3),(-2,3).
\]

The nonzero absolute determinants between pairs are exactly
{1,2,3,4,5,7,8}. Hence for characteristic ≥13 their twelve kernels
are distinct over K. Their slopes b/a are

\[
 \infty,0,1,-1,2,-2,3,1/2,-1/2,3/2,1/3,2/3.
\]

In characteristic 5 the reduced directions are all six points of
P¹(F₅); in characteristic 7 they are all eight points of P¹(F₇).
These remain six or eight distinct K-lines in extension fields: two
different base-field slopes cannot become equal in an extension.
Each K-line contains q−1 nonzero vectors, and distinct lines meet only
at zero. If d_p is the number of these lines, then

\[
 |\Omega_K|=q^2-1-d_p(q-1)=(q-1)(q+1-d_p).
\]

Take d₅=6, d₇=8, d_p=12 for p≥13 and divide by twelve using
Theorem A. This proves Theorem B. For q=5,7 the result is zero. In F₁₁
the listed slopes cover all twelve projective directions, so there are
no admissible parameters there either. This last support observation
does not extend the invariant proof into characteristic 11.

## 6. A single endpoint determines its Bloom partner

Let a rigid class occur as either endpoint of a Bloom pair. The value of
m₂ recovers s. Subtract 144s³ from m₃² and 23946s³ from m₆. If
the endpoint is X, the resulting two values are

\[
 \begin{pmatrix}58077&-2916\\6399&-4860\end{pmatrix}
 \begin{pmatrix}e^2\\de\end{pmatrix}.
\]

If the endpoint is Y, use the same matrix with −de as the second unknown.
This follows by squaring the third-moment formulas and replacing d² by
4s³−27e². The determinant is

\[
 -2^4\,3^{12}\,31.
\]

In the allowed characteristic other than 31 it is invertible. Thus the
single endpoint recovers s,e², without knowing which side it occupies,
and without dividing by s or any data-dependent value. Any two Bloom
pairs sharing that endpoint have the same s,e²; Theorem A makes them
the same pair. This proves Theorem C, and Corollary D follows from the
stated large-prime generation result.

Characteristic 31 is a genuine exceptional boundary for the unique-
partner assertion, not just a failed matrix inverse. In F₃₁ take
v=(2,12) and w=(8,17). Their pairs share A but have different other
endpoints:

\[
 A=\{0,1,3,8,12,18\},\quad
 B=\{0,1,3,10,14,26\},\quad
 C=\{0,1,4,10,12,17\}.
\]

The exact transports are A=3−Y_v=X_w, B=3−X_v, and C=12−Y_w.
All three have each cyclic distance 1,…,15 exactly once. They are
different rigid classes, as their anchored translation/reflection lists
or cyclic gap necklaces verify. The invariant s is zero for both
parameters, whereas e(v)²=2 and e(w)²=8. By Theorem A the two pairs
are distinct. The classification of pairs in A and count in B continue
to hold in characteristic 31.

For Corollary E, D handles every prime above 131. At the finitely many
smaller primes, the saved complete two-method census payloads give
the extra pair counts 8,9,11,20 at 17,19,23,31 and zero at all others.
At 31 the payload has sixty size-two families and one size-five family,
hence 61 families and 60+binomial(5,2)=70 edges. At 17,19,23 all
families have size two. Those facts give the displayed corrections.
Primes below six support no six-set; the complete checks at 7 and 11
have no nontrivial family. The read-only small-prime audit records the
source hashes, verifies family payloads and counts, and explicitly retains
the inherited completeness dependency rather than treating its replay
as a new full enumeration.

## 7. Verification, prior art and remaining scope

The auxiliary derivation in `notes/2026-09-30-six-prime-symmetries.md`
independently checks the formal coefficient identities and planar symmetry
group. The direct point enumerator `src/six_prime_bloom.py` retains exact
parameter fibers without assuming this formula. An independent invariant
implementation and its finite-field controls accompany this proof.
Those finite checks support the symbolic proof and are not its basis.

**[COMPUTED]** Two independent methods agree on every exact parameter
fiber at all primes 13..251 and at 1009 (50 primes, 2,013,650 parameter
candidates). At 1009 there are 83,832 Bloom pairs. Direct and invariant
partitions also agree on every parameter over F25, F49, F169, giving
40,168,2212 pairs. These extension fields' additive groups are not cyclic.
The read-only complete-census audit verifies the small-prime corrections
and records the inherited source hashes. Complete two-method six-subset
enumeration remains 6..135; the larger prime checks are of the parameter
image, not full six-subset enumerations.

Reproduce the exact certificates and tests in the pinned environment:

```bash
.venv/bin/python src/six_prime_bloom.py --primes 13..251 1009 --out results/2026-09-30-six-prime-count --resume
.venv/bin/python src/six_bloom_invariants.py > results/2026-09-30-six-prime-invariants/replay.log
.venv/bin/python tests/test_six_prime_bloom.py
.venv/bin/python tests/test_six_bloom_invariants.py
```

The second implementation's `summary.json` records its source digest,
the direct file digests, integer identity checks, field controls and
small-prime checkpoint hashes. The two new test files pass 6/6 and 8/8
groups. The fresh attack independently expands the identities, checks
the group action, reconstructs selected prime and extension-field
partitions, and audits every displayed small-prime census member. It
does not reprove G or rerun the complete six-subset census through135.

The underlying family and triangular geometry are classical:
Bloom–Golomb (1977), Bekir–Golomb (2007), and Postpischil–Gilbert (1994)
are discussed with primary-source scope in
`notes/2026-09-30-six-prime-literature.md`. That search covers the required
venues and records access limits. It found no exact matching finite-field
quotient/count statement in the sources read; novelty remains unestablished.

This is a complete classification of the specified Bloom image, not of
all six-point homometry over every finite abelian group. Below the large-
prime boundary, extra purely cyclic pairs must be added separately.
Composite cyclic moduli require a disjoint treatment of torsion mechanisms,
inflation and overlaps. Characteristics 2,3,11 in extension fields remain
outside this argument. Theorem G is still computer-assisted; this moment
proof replaces none of its general-modulus finite obligations.
