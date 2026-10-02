# Mathematical results and proof boundaries

This repository studies finite cyclic sets with identical difference data.
Its main results are a complete generating theorem for six-element sets
and an exact classification and count of the classical two-parameter
six-point construction. A separate extension treats real weighted signals.

The status **[PROVED]** here means a written in-house argument with a
separate adversarial review. The work and reviews were AI-assisted.
Computer-assisted arguments retain their certificate, runtime and solver
dependencies. This is a research proof package, without external peer review
or complete proof-assistant certification. Historical novelty remains
unestablished; the classical constructions and general counting methods
are credited in [REFERENCES.md](REFERENCES.md).

For the universal backdrop, see
[the autocorrelation theorem and binary constraint](UNIVERSAL_THEOREM.md).
Equal autocorrelation, Fourier magnitudes and spectral-unit convolution
are classical at every support size; Rosenblatt's cyclic factorization is
also all-cardinality prior art. The six-point result supplies additional
constructive structure within the binary constraint.

## Definitions

For a positive integer $n$, write $\mathbb Z_n=\mathbb Z/n\mathbb Z$.
For a set $A\subseteq\mathbb Z_n$, its directed autocorrelation is

$$
r_A(t)=\#\{(a,a')\in A^2:a-a'=t\}.
$$

Two sets are **homometric** when their autocorrelations agree. For sets of
the same cardinality, this is equivalent to equality of their multisets of
pairwise cyclic distances; equivalently, the
discrete Fourier transforms of their indicators have equal magnitudes.

Sets are identified under translation and reflection:
$B=\varepsilon A+t$, with $\varepsilon\in\{1,-1\}$.
Each such orbit is a **rigid class**. A nontrivial homometric pair consists
of two different rigid classes. A **homometry family** contains all rigid
classes sharing one autocorrelation. A pair edge and a maximal family are
different counting objects. General multiplication by a unit modulo $n$
is never part of the equivalence relation.

## 1. Theorem G: generation of all six-point cyclic homometry

**[PROVED, computer-assisted]** For every positive integer $n$, construct
a graph on the rigid classes of six-element subsets of $\mathbb Z_n$.
Join classes using the explicit moves in the
[full theorem](../notes/2026-09-30-six-generation.md). Its connected
components are exactly the homometry families.

The grammar consists of a classical integer-factor construction, block
translations and reflections with explicit cross-difference conditions,
a parallelogram-dyad construction, half-coset complementation,
autocorrelation-preserving unit multiplication, and thirteen fixed cyclic
templates. Every endpoint must remain a six-element set. The unit move
requires an explicit autocorrelation-invariance condition.

Completeness comes from an exhaustive split of universal signed edge-matching
presentations. The finite-torsion branch reduces to groups of order at most
135. Positive free-rank branches use a complete line classification and
exact integral presentation certificates. Two independent six-subset
enumerations cover the finite range $6\le n\le135$. The arbitrary-modulus
conclusion also needs the written reductions and the positive-rank branches;
it does not follow from extrapolating those enumerations.

The theorem permits compositions of moves. It supplies neither a minimal
list nor a unique normal form, and it does not count all families or extend
to arbitrary cardinality.

**Read:** [proof](../notes/2026-09-30-six-generation.md),
[assembled adversarial review](../notes/2026-09-30-six-generation-review.md),
[certificate-driver contract](../notes/2026-09-30-six-generate.md).
The proof's component map identifies its exact finite-checker and line-solver
dependencies. Independent review repaired a coset-projection issue and a
block-reflection alignment before acceptance.

## 2. Theorem AP: the classical construction in every modulus

For $v=(a,b)\in\mathbb Z_n^2$, define

$$
\begin{aligned}
X_v&=(0,a,b-2a,2b-2a,2b,3b-a),\\
Y_v&=(0,a,b+2a,2b-a,2b+a,3b-a).
\end{aligned}
$$

Let $\Omega_n$ contain exactly the parameters for which both lists have
six distinct entries. Let $\Phi(v)$ be the unordered pair of their
independently translated/reflected classes. This is the classical family,
called the **Bloom construction** in the proof notes; its formulas and
factor-flip mechanism are prior art.

Set

$$
R=\begin{pmatrix}0&-1\\1&-1\end{pmatrix},\qquad
T=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
\Gamma=\{\pm R^iT^j:0\le i<3,\ 0\le j<2\}.
$$

**[PROVED, computer-assisted]** The twelve-element group $\Gamma$ acts
freely on $\Omega_n$ and preserves $\Phi$. Every nontrivial pair
fiber is one $\Gamma$-orbit, with exactly these exceptions when
$12\mid n$. Writing $h=n/12$:

- $\Gamma(h,5h)$ produces congruent endpoints, so it contributes no
  nontrivial pair.
- $\Gamma(h,4h)$ and $\Gamma(3h,7h)$ produce the same nontrivial
  pair. This is the subgroup inflation of
  $\{0,1,2,3,6,8\}/\{0,1,2,4,6,7\}$ from $\mathbb Z_{12}$.

Consequently the number of nontrivial unordered pair edges represented by
this construction is

$$
B(n)=\frac{|\Omega_n|}{12}-2[12\mid n],
$$

where $[d\mid n]$ is 1 when $d$ divides $n$, and 0 otherwise.
The independently reviewed support formula is

$$
\begin{aligned}
|\Omega_n|={}&n^2-(9+3\gcd(n,2))n+11
 +15[2\mid n]+16[3\mid n]\\
&+18[4\mid n]+24[5\mid n]+12[6\mid n]
 +24[7\mid n]+12[8\mid n].
\end{aligned}
$$

At $n=12$, there are 36 admissible parameters but only one nontrivial
Bloom pair. Dividing the parameter count by twelve without the exceptions
would therefore be wrong.

The pair-fiber proof enumerates all 4,147,200 labeled matching systems with
denominator-free elimination. Exact minor identities reduce exceptional
solutions in arbitrary moduli to a finite list of subgroup orders.
An independent implementation uses a different elimination pivot and
reconstructs the complete table. The support formula also has two independent
arithmetic derivations: exact-order overlap counting and Smith-factor
inclusion–exclusion.

**Read:** [AP proof](../notes/2026-10-01-six-bloom-primary.md),
[support proof](../notes/2026-10-01-six-bloom-support.md),
[fresh independent attack](../notes/2026-10-01-six-primary-review.md).

## 3. Prime and composite consequences

For every prime $p\ge13$, the Bloom pair count simplifies to
$(p-1)(p-11)/12$. The
[field theorem](../notes/2026-09-30-six-prime-theorem.md) gives a direct
algebraic classification using the invariants
$a^2-ab+b^2$ and $a^2b^2(a-b)^2$. Its field extension uses additive
differences; the additive group of $\mathbb F_{p^r}$ for $r>1$ is
not a cyclic group of order $p^r$.

Combining that theorem with G and the independently checked small-prime
censuses gives, for primes $p\ge13$,

$$
\begin{aligned}
P_6(p)&=B(p)+8[p=17]+9[p=19]+11[p=23]+20[p=31],\\
F_6(p)&=B(p)+8[p=17]+9[p=19]+11[p=23]+11[p=31].
\end{aligned}
$$

Here $P_6$ counts all nontrivial pair edges and $F_6$ counts all
maximal nontrivial families. Every prime-order family has size two except
one size-five family in $\mathbb Z_{31}$. These total-count statements
retain G's computational dependencies and the finite census dependency.
[Prime review](../notes/2026-09-30-six-prime-review.md).

For $\gcd(n,6)=1$, the earlier
[composite theorem](../notes/2026-09-30-six-composite-global-matrix.md)
also classifies the Bloom endpoint graph: isolated edges, plus one inflated
31-point five-cycle exactly when $31\mid n$.
[Composite review](../notes/2026-09-30-six-composite-global-review.md).
If every prime divisor of $n$ exceeds 131, G makes every six-point
pair Bloom. Thus the total pair and family counts in that scope are both
$(n-1)(n-11)/12$, and every nontrivial family has size two.

AP now covers pair fibers at every modulus, including the even and
3-primary cases left unfinished in earlier notes. It does not classify
the complete all-modulus Bloom endpoint graph. Indeed, its proof supplies
two different Bloom edges sharing an endpoint for every even $n\ge18$.
Nor does it provide disjoint counts of all the other mechanisms in G.

## 4. Weighted cyclic phase-retrieval extensions

For real signals $x$ on $\mathbb Z_N$, replace the set autocorrelation
by $c_x(d)=\sum_i x_i x_{i+d}$. Intrinsic equivalence now also allows
global sign. The binary generation theorem does not classify weighted
competitors.

**[PROVED, separately scoped]** The
[subgroup/fiber note](../notes/2026-10-01-weighted-subgroup.md) proves U, F,
C, H and S, accepted in a
[separate attack](../notes/2026-10-01-weighted-subgroup-review.md):

- **U:** every convolution preserving a nonempty coordinate support space
  is supported on that support's period subgroup. The ones preserving all
  autocorrelations are exactly its real spectral units.
- **F/C:** for $S=Q+q\mathbb Z_{qm}$, with at least three quotient
  points and distinct ordered nonzero quotient differences, the entire
  generic real same-support fiber is a subgroup-unit orbit of dimension
  $\lfloor(m-1)/2\rfloor$. Sparse positive signals can therefore have
  generic continuous ambiguity despite having more folded difference
  classes than support coordinates.
- **H:** deleting one point from the three-coset support gives aperiodic
  supports with generic local fiber dimension
  $\lfloor(m-1)/2\rfloor-1$ for $m\ge5$. Excluding periodic
  supports alone does not remove the obstruction.
- **S:** known-support reconstruction and explicit stability bounds hold
  on a bounded nonvanishing domain after quotienting by the enlarged
  subgroup-unit group. They do not imply recovery modulo only sign,
  translation and reflection.

These examples contradict the literal fixed-support generic uniqueness
statements of Conjectures 4.7 and 4.11 in
[Bendory–Edidin, arXiv:2002.10081v2](https://arxiv.org/abs/2002.10081v2).
The journal wording and historical priority remain unresolved. No conclusion
is asserted about its distinct-support or measure-zero conjectures or about
generic-basis recovery theorems. Spectral-unit ambiguity itself is classical.

A separate
[six-support note](../notes/2026-10-01-weighted-six-incidence.md) and
[review](../notes/2026-10-01-weighted-six-review.md) establish **W21/R5**.
For the prescribed binary pair
$A=(0,1,3,7,10,15)$, $B=(0,1,4,7,14,16)$ in $\mathbb Z_{21}$,
the positive A-to-B weighted intersection is exactly the common
equal-strength ray. Yet A alone has inequivalent positive signals
$\mathbf1\pm t(1,-1,1,-1,-1,1)$, $0<|t|<1$, with identical powers.
They rule out local injectivity and a positive lower Lipschitz bound near
equal strengths. This is a special amplitude locus, not a generic-amplitude
counterexample. The other twelve template-local conclusions in that note
remain **[OPEN: review pending]**.

## What remains open

External specialist review, historical priority, a minimal or disjoint
six-point classification, total all-modulus counts, higher-cardinality
generation, and general unknown-support weighted recovery remain open.
The repository separates exact theorems, computed checks and unfinished
claims so readers can inspect or challenge each at its actual scope.
