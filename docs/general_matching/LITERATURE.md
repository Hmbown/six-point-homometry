# General signed-matching reduction: literature and independent audit

Date: 1 October 2026. Scope: PQ1/PQ3, arbitrary cardinality and cyclic
modulus. This is an independently derived conceptual check and a bounded
literature pass. The agent did **not** read the contemporaneous theorem
draft before deriving the arguments below. No novelty claim is made.

Status: the primary-reading scopes below are **VERIFIED**. The new
incidence-specific argument is a candidate for the main theorem's separate
adversarial review; this file alone does not confer **[PROVED]** status.
The universal-group presentation is a reduction, not a compressed structural
classification or an efficient all-cardinality enumerator.

## 1. Strongest independent implication

Let k >= 2, m = binom(k,2), and let a signed bijection between the unordered
edges of two labeled k-point configurations determine the matrix

    M = [D | -S P D],

where D is the m by (k-1) reduced oriented incidence matrix of the complete
graph, P permutes its rows, and S changes row signs. The generators on each
side are translated separately so that a_0 = b_0 = 0. Put

    U = Z^(2k-2) / row_Z(M),
    r = rank_Q(M), d = 2k-2-r, t = |Tor(U)|.

Every labeled cyclic realization of the matching is a homomorphism
U -> Z_n. Conversely every such homomorphism with distinct endpoints on
each side gives a homometric pair, because every unordered difference has
an equally signed partner. This includes antipodal differences and repeated
distances: matching occurrence multiplicities, rather than only distinct
difference values, is essential.

### 1.1 Free rank and torsion: all ranks

The first k-1 columns of M are independent: they form the complete reduced
incidence matrix. Therefore r >= k-1 and d <= k-1.

An r by r nonsingular minor can be chosen to contain **all** those k-1
columns. Extend them to an r-column basis, then choose r rows on which that
basis remains independent. Let H be the simple graph on k vertices whose
edges index the chosen rows. Laplace expansion along the complete A block
has one term for each (k-1)-edge subset of H. Its A determinant is 0 unless
the edges form a spanning tree, in which case its absolute value is 1.
The complementary B determinant is 0 or +/-1, by total unimodularity of
oriented incidence matrices and preservation under row signs/permutations.
Consequently

    t divides det(minor),
    t <= |det(minor)| <= tau(H),
    |E(H)| = r <= R := min(2k-2, binom(k,2)).

The first line is the Smith-normal-form determinantal-divisor identity:
the order of the torsion cokernel equals the gcd of all nonzero r-minors.
This remains valid when U has positive free rank. In particular, the
spanning-tree bound is **not restricted to the full-rank branch**.

Define T_k as the maximum number of spanning trees of a simple graph on k
vertices with R edges. Add distinct edges to H until it has R edges; this
cannot decrease the tree count. Thus t <= T_k. The matrix-tree identity and
AM-GM give the coarser closed form

    t <= floor((2R/(k-1))^(k-1) / k)
       <= floor(4^(k-1)/k).

For the actual rank r, the same argument yields

    t <= min{binom(r,k-1), floor((2r/(k-1))^(k-1)/k)}.

The elementary bound binom(2k-2,k-1) from arbitrary incidence-minor
expansion is valid, but weaker. For k=7 the closed-form all-rank bound is
585, compared with that binomial bound 924. These are proved arithmetic
evaluations of stated formulas, not an exhaustive computation of T_7.
The main theorem must independently review and certify its chosen exact
T_k values.

The tree inequality used here can be derived directly. If the nonzero
Laplacian eigenvalues of connected H are lambda_1,...,lambda_(k-1), then

    tau(H) = (1/k) product(lambda_i),
    sum(lambda_i) = 2r.

Apply AM-GM. The matrix-tree identity follows by Cauchy-Binet on the reduced
incidence matrix: its nonzero squared minors are precisely the trees. This
is classical graph linear algebra; no priority is claimed for it.

### 1.2 Residue-preserving integer shadow

Suppose gcd(n,t)=1. A homomorphism phi:U -> Z_n kills Tor(U): the order of
each image divides both n and the order of that torsion element. It factors
through the free quotient F = U/Tor(U), isomorphic to Z^d.

Distinct original endpoint images imply that their corresponding points
in F are distinct. Choose a basis of F and any integer representatives
c_1,...,c_d for the residues phi of its basis elements. Every map

    chi_z(v) = sum_j (c_j + n z_j) v_j,  z in Z^d,

reduces to phi modulo n. Each endpoint collision is one proper affine
hyperplane in z. A finite union of proper affine hyperplanes cannot cover
Z^d: for example substitute z=(q,q^2,...,q^d); each forbidden condition is
a nonzero polynomial with finitely many roots. Choose q outside the finite
root set. Then chi_z is injective on each endpoint set. All matched signed
differences remain equal in Z, so the integer sets are homometric and
reduce to the given cyclic pair. If the integers were translates or
reflections, reduction would make the cyclic sets T/I-equivalent too.

Thus the certificate-specific condition gcd(n,t)=1 suffices for a shadow.
Uniformly, **every k-point cyclic homometric pair is an integer shadow when
every prime factor of n exceeds T_k**; the coarser sufficient condition
uses floor(4^(k-1)/k). This is valid for composite n as well as primes.
It does not classify all homometric integer pairs at arbitrary k.

If d=0, a distinct-endpoint cyclic realization cannot exist under this
coprimality condition, since phi is then zero. The finite branch has no
hidden large-prime exception.

## 2. Primary sources read and comparison

### Bilu--Lev--Ruzsa 1998: VERIFIED, primary author preprint

Y. F. Bilu, V. F. Lev and I. Z. Ruzsa, *Rectification principles in additive
number theory*, Discrete & Computational Geometry **19**(3) (1998),
343--353, DOI [10.1007/PL00009351](https://doi.org/10.1007/PL00009351).
[Author source](https://math.haifa.ac.il/seva/Papers/rectif.dvi).

Read the entire direct-rectification argument, pp.4--5, Theorem 3.1 and its
proof; also pp.2--3, Theorem 2.1 and its proof. Theorem 3.1 explicitly
constructs an integer set whose ordinary reduction is a Freiman isomorphism
of order s onto a set K in Z_p, when |K| <= log_(2s)(p). Therefore integer
shadows at sufficiently large primes are already a classical consequence.
Applying s=2 after translating both k-point sets to contain zero uses a
union of at most 2k-1 points; a sufficient prime threshold is 4^(2k-1).
This broad result preserves all two-sum relations, beyond matched edges.

### Lev 2008: VERIFIED, complete primary author preprint

V. F. Lev, *The rectifiability threshold in abelian groups*, Combinatorica
**28**(4) (2008), 491--497.
[Author source](https://math.haifa.ac.il/seva/Papers/recthrsh.dvi).

Read all six preprint pages, including Theorem 1, the determinant lemmas,
their included proof, and the relation-matrix proof. If p(G) is the least
order of a nonzero element, every S with |S| <= ceil(log_t p(G)) is
Freiman t-isomorphic to an integer set, and this threshold is sharp.
The argument uses bounded relation determinants and finite-hyperplane
avoidance. For two k-point sets, translate each to contain zero, and use
their union of size at most 2k-1. The t=2 theorem therefore supplies an
integer homometric model when p(G)>4^(k-1). T/I inequivalence survives,
since an integer point correspondence asserting equal sums or differences
transfers back through the Freiman isomorphism. Ordinary residue-preserving
reduction is not an explicit requirement of this published theorem. Our
quotient argument in 1.2 supplies that refinement. Compared with this
naive general antecedent, the incidence bound divides the closed-form
threshold by k; this is a comparison, **not a novelty assertion**.

### Konyagin--Lev 2000: VERIFIED, primary sections 1--2

S. V. Konyagin and V. F. Lev, *Combinatorics and linear algebra of Freiman's
isomorphism*, Mathematika **47**(1--2) (2000), 39--51.
[Author source](https://math.haifa.ac.il/seva/Papers/colifr.dvi).

Read preprint pp.1--7, especially the relation-vector space in section 2
and Theorems 3--4. The linear-algebraic encoding of additive equivalence
and dimension has classical antecedents here. Later construction/counting
arguments and concluding conjectures were only searched, not fully read.
This paper is not used as a proof input for signed-edge completeness.

### Grynkiewicz 2013: VERIFIED abstract; full proof [LIT-VERIFY]

D. J. Grynkiewicz, *Freiman Homomorphisms Revisited*, chapter 20 of
*Structural Additive Theory*, Developments in Mathematics **30** (2013),
299--365, DOI [10.1007/978-3-319-00416-7_20](https://link.springer.com/chapter/10.1007/978-3-319-00416-7_20).

The publisher's primary abstract explicitly describes a universal ambient
group, an upper bound on its torsion subgroup, and integer models for
sufficiently small subsets of arbitrary abelian groups. The table of
contents places the torsion bound at pp.316--320 and consequences at
pp.321--332. Institutional/payment access prevented reading these proofs.
This is a **priority-comparison gap**, not a theorem input. Whether its
distinct-summand formulation already gives an incidence/tree bound remains
unresolved. Do not claim the universal-group or torsion method is new.

### Costa--Della Fiore 2024: VERIFIED, primary proof scope

S. Costa and S. Della Fiore, *Weak Freiman isomorphisms and sequencings of
small sets*, [arXiv:2407.15785v2](https://arxiv.org/html/2407.15785v2),
29 July 2024. Primary text read: section 2, Theorems 2.4--2.5 and proof;
Lemma 3.8 and proof; references.

The section 2 proof rectifies selected linear relations by determinant
bounds, Cramer's rule and denominator clearing when all prime factors of
the cyclic modulus are sufficiently large. Its weak-isomorphism scope is
zero-sums of distinct elements, not homometry. The exact same style of
modular-to-characteristic-zero linear reduction is established prior art.
No result about matching incidence minors or homometry is inferred from it.

### Classical graph bound: VERIFIED restatement and independent derivation

Ş. B. Bozkurt, *Upper bounds for the number of spanning trees of graphs*,
Journal of Inequalities and Applications **2012**, article 269,
DOI [10.1186/1029-242X-2012-269](https://link.springer.com/article/10.1186/1029-242X-2012-269).
Read the primary PDF's pp.1--3, equation (1), equation (3), attribution and
references. Equation (3) is exactly tau(H) <= (1/k)(2r/(k-1))^(k-1).
Bozkurt attributes it to G. R. Grimmett's 1976 paper. Grimmett's original
was inaccessible (403) and is not an independently verified proof input.
Section 1.1 gives the direct elementary derivation used in this audit.
Bozkurt's later improved inequalities were not reviewed.

### Existing homometry results

Rosenblatt 1984's already-verified group factorization and spectral-unit
theorems remain acknowledged background. They are not rediscovered or
promoted as this task's structural result. The present bounded search did
not locate a primary statement of the exact signed-incidence tree bound
for homometry. Absence in this search does not establish historical
priority, particularly with Grynkiewicz's full chapter unread.

## 3. Required-venue search and access boundaries

All queries were made on 1 October 2026. Exact queries and direct endpoint
results are saved in
`results/2026-10-01-general-reduction-literature/search-log.json`.

| Venue | Bounded query/access result |
|---|---|
| arXiv | Homometry/torsion and rectification searches; primary Costa--Della Fiore v2 read, Green--Ruzsa abstract located only. |
| MathSciNet | Indexed `homometric rectification` query; direct homometric search endpoint inaccessible. No exhaustive search claimed. |
| zbMATH | Indexed `homometric rectification` query; direct homometric endpoint inaccessible. |
| Google Scholar | Indexed `homometric universal group` query; direct `homometric rectification` endpoint inaccessible. |
| OEIS | Indexed quoted homometric query found no relevant bound sequence; direct search endpoint inaccessible. Unrelated broad-search hits discarded. |
| Journal of Mathematics and Music | Indexed homometric/group/lift query located Mandereau et al.2011 (publisher abstract read through indexed primary result) and Zhao2026 (current-issue title only); direct publisher requests returned 403. No unread proof used. |
| Journal of Music Theory | Indexed homometric/cyclic and Z-related queries did not produce a relevant primary lifting theorem. Earlier Soderberg lead remains unresolved. |
| Music Theory Online | Indexed homometric and Z-related searches located Capuzzo2008 and related music-transformational work. Capuzzo's introductory mod-12 scope read; no arbitrary-modulus lifting result inferred. |

The source-search pass also used exact title/author queries for Bilu--Lev--
Ruzsa, Lev, Konyagin--Lev, Grynkiewicz and Grimmett, plus incidence/TU and
spanning-tree determinant searches. The live web tool could not parse
author DVI files, so the public author originals were downloaded and
converted locally with the installed converter. Fetch hashes and statuses
are recorded in `author-fetches.json`; DVI originals are preserved.

## 4. Honest boundary and next comparison

The strongest clean advance supported by the independent argument is an
incidence-specific, certificate-sensitive torsion obstruction and ordinary
residue-preserving integer shadow. General rectification, universal ambient
groups, finite relation presentations, determinant bounds and generic
integer projection are classical methods. Neither a finite matching menu
nor this large-prime shadow conclusion supplies integer homometry
classification for arbitrary k, an efficient all-cardinality grammar,
nonredundant parameters, or a closed count of all families.

Before any priority claim, a human or accessible institutional source should
compare Grynkiewicz chapter 20, especially sections 20.4--20.7, against the
all-rank spanning-tree refinement. The exact homometry-specific numerical
cutoff and whether it occurs elsewhere remain **[OPEN]** as historical
questions. No material was submitted or shared externally.
