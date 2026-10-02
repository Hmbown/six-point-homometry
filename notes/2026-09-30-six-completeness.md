# Six-note completeness reduction to bounded cyclic cylinders

30 September 2026. PQ1/P3, six notes only. **[PROVED], in-house, with computer-assisted bound.**
Separate attack: `2026-09-30-six-cylinder-templates-review.md`.
No novelty claim. This is a structural reduction of the arbitrary-modulus
problem, not a classification of all the remaining cylinder pairs.

## 1. Statements and scope

**Theorem C (bounded cylinder reduction).** Every homometric pair of six-subsets
A,B of Z_n is the image of a pair of homometric six-subsets P,Q of
Z x C_q, where q divides n and **1 <= q <= 135**, under

    phi(z,t) = z + (n/q)t  mod n.

The projection is injective on P and on Q. If A,B are T/I distinct, P,Q
are also distinct under translation and inversion in Z x C_q.
Conversely, any such P,Q with injective projections give homometric six-subsets
of Z_n; retain exactly the projections that are T/I distinct.

The bound 135 uses a finite, independently checked enumeration of all 3,003
labelled ten-edge subgraphs of K6. Replacing 135 by 252 gives a proof using
only the already-reviewed incidence-minor bound, without this enumeration.

**Corollary C1 (sharper shadow boundary).** If every prime divisor of n
exceeds 131, every six-note pair in Z_n is an integer shadow. Thus the
sufficient cutoff 251 in Theorem S can be reduced to 131. This is not
claimed sharp.

**Corollary C2 (full-rank isolation).** If a compatible signed matching has
rank ten, then, after anchoring each set independently, A and B both lie
in the subgroup of Z_n of order q <= 135. Consequently they are an ordinary
inflation of a pair in Z_q. In particular, a pair generating all of Z_n
through its anchored coordinates cannot have a full-rank matching unless
n <= 135.

These statements distinguish three sources of relations. q=1 is an integer
shadow. Rank-ten matchings yield ordinary finite cyclic inflation. Positive
free rank with q>1 gives a mixture of an integer coordinate and bounded cyclic
torsion, as in the reviewed infinite order-six families. No chosen q is
asserted minimal or unique. A q>1 certificate does **not** establish that a
pair lacks a separate q=1 certificate.

The remaining classification problem is explicit: classify six-point
homometric configurations on the 135 cylinders Z x C_q (q=1,...,135),
including their parameter families, collision exclusions, and projections.
This removes unbounded torsion order from the arbitrary-n problem. It does
not by itself supply the desired small, exhaustive list of mechanisms.

## 2. The matching presentation

Use a compatible signed edge matching from Theorem S. The two anchored
six-sets have coordinates

    (0,a_1,...,a_5), (0,b_1,...,b_5),

and M is the 15 by 10 integral matrix whose rows are

    e_j-e_i - epsilon(f_l-f_k).

The first five columns, restricted to all fifteen rows, are a reduced
incidence matrix of K6; the last five are a permuted and row-signed such
matrix. In particular **5 <= rank_Q(M) <= 10**.

Define the finitely generated abelian group

    G = Z^10 / <rows of M>.

Let E_i,F_j denote the corresponding coordinate generators in G and put
E_0=F_0=0. The relations make every matched difference equal up to sign in
G. Thus the two formal six-point configurations in G have equal directed
difference multisets. The input vector v modulo n defines a homomorphism
f:G -> Z_n, since Mv=0 mod n. Their images are the anchored input sets.
Distinctness of those images proves the original six points in each formal
configuration are distinct as well.

No division, generic-position hypothesis, or distinct-distance assumption
is used. Repeated distances and both signs of antipodal edges are allowed.

## 3. The improved minor bound

The reviewed incidence lemma says every minor of either five-column block
has determinant in {0,+1,-1}. For an r by r minor with c first-block
columns, expansion along these columns gives the bound binomial(r,c).
If r <= 9 the largest allowed value is binomial(9,4)=126.

For r=10 all ten columns are present. Its selected rows correspond to ten
distinct edges of K6 in the first block. A five-row reduced-incidence minor
is nonzero exactly when those five edges form a spanning tree: a cycle gives
row dependence; five acyclic edges on six vertices form a connected tree;
and a tree has determinant +/-1 by successive leaf elimination.

In the block expansion, therefore, only spanning trees of the selected
ten-edge graph can contribute. The complementary second-block determinant
is still 0 or +/-1. Hence

    |det(M_R)| <= tau(K6[R]),

where tau counts spanning trees. It suffices to bound tau for every labelled
ten-edge graph; it is unnecessary to assume that every counted summand can
have a common sign or that 135 is attained by a matching determinant.

### 3.1 Finite exhaustive certificate

There are C(15,10)=3,003 selected graphs. The production calculation enumerates
all C(15,5)=3,003 possible five-edge sets, keeps precisely the acyclic ones
(1,296 spanning trees), and counts containment in each ten-edge graph. It
uses **no graph-isomorphism or unit symmetry reduction**. The independent
calculation constructs each graph's Laplacian and evaluates a 5 by 5
cofactor by exact Bareiss elimination, using Kirchhoff's tree formula.
Both methods give exactly the following histogram:

| Number of spanning trees | Number of labelled graphs |
| ---: | ---: |
| 0 | 6 |
| 75 | 300 |
| 96 | 90 |
| 99 | 360 |
| 100 | 90 |
| 104 | 360 |
| 111 | 360 |
| 114 | 360 |
| 115 | 360 |
| 120 | 180 |
| 121 | 72 |
| 128 | 45 |
| 130 | 360 |
| 135 | 60 |

The counts sum to 3,003, so the maximum is 135. A maximizing graph is K3,3
with one additional edge inside one part. Its complement is a triangle and
a three-vertex path, on disjoint vertex sets. The example is a useful check,
not a substitute for exhausting all selected graphs.

Combining r<=9 and r=10 proves **every minor of M has absolute determinant
at most 135**. It follows in particular for a nonzero maximal-rank minor.

## 4. Proof of the cylinder reduction

By Smith normal form,

    G = Z^d direct-sum T,    d=10-rank(M) <= 5,

where T is finite. The order of T is the gcd of the nonzero maximal-rank
minors of M. To recall why, unimodular row and column operations preserve
the ideal generated by minors of any fixed order, by Cauchy--Binet in both
directions. In Smith form the rank-r minor ideal is generated by the product
of the r nonzero diagonal entries; this product is exactly |T|.

Thus |T| <= 135. Restrict the given map f:G -> Z_n to T, and let its image
be H. H is cyclic of some order q dividing n, and Lagrange's theorem gives
q dividing |T|. Therefore q <= 135. Identify H with C_q by the embedding

    t |-> (n/q)t mod n.

Under G=Z^d direct-sum T, write f on the free basis as residues c_1,...,c_d,
and choose arbitrary integer representatives of them. For t in T, write
f(t)=(n/q)theta(t), where theta:T -> C_q is a homomorphism. Define

    psi(z_1,...,z_d,t) = (sum_i c_i z_i, theta(t)) in Z x C_q.

Then phi composed with psi is exactly f. Applying psi to the two six-point
configurations preserves their matched differences, and therefore preserves
homometry. Distinct input residues force the two images to have six points
each. There is no need for a generic linear functional: any chosen lifts of
c_i work, since distinctness is already witnessed by the final projection.
Restoring the two original anchor translations in the integer coordinate
gives projections exactly A and B, not only their anchored translates.

If P and Q were related by a translation or inversion in the cylinder,
applying phi would give the corresponding T/I relation between A and B.
Thus T/I distinction of the input is preserved. Conversely, applying any
group homomorphism to equal directed difference multisets preserves their
equality. Injectivity on each projected six-point set makes this multiset
identity the usual six-set homometry identity. This proves Theorem C.

For C1, q is a divisor of n of size at most 135. If every prime factor of n
is greater than 131, q cannot have any prime factor: the next prime is 137.
Hence q=1, so the cylinder is Z. For C2, d=0 when rank(M)=10, so every
anchored input coordinate belongs to f(T)=H. This is precisely the subgroup
inflation assertion. QED, subject to the finite tree bound in Section 3.1.

## 5. Exact certificate implementation

`src/six_completeness.py` chooses one compatible signed matching and obtains
integer unimodular matrices U,V with

    U M V = D.

If v is the anchored input vector, set w=V^-1 v modulo n. For nonzero Smith
diagonal indices i<r, the order of the subgroup generated by w_i is

    q = n / gcd(n,w_0,...,w_(r-1)).

Let h=n/q. Since h divides all these w_i, the cylinder coordinates for the
original coordinate generator e_j are

    integer part = sum_(i>=r) V[j,i] w_i,
    cyclic part  = sum_(i<r) V[j,i] (w_i/h) mod q.

This is the constructive map in Section 4. The output records M,D,U,V,
q, both cylinder sets, the input pair, and the edge matching. Verification
uses exact matrix multiplication, unimodularity, direct cylinder difference
counts, and the immutable reference for the projected pair.

Examples from the first compatible matching:

| Input | q | Free rank | Interpretation |
| --- | ---: | ---: | --- |
| Reviewed family H1 in Z18 | 6 | 1 | A genuine integer-axis/cyclic mixture |
| The benchmark six-pair in Z21 | 21 | 0 | Finite cyclic seed |
| Classical Bloom pair in Z37 | 1 | 2 | Integer shadow |

The example records are computed, independently checked certificates. Their
q values are not assertions of minimal torsion order over all possible
presentations. The exact no-integer-lift claims for H and the Z21 benchmark
remain supplied by the separate exhaustive-matching review already in the
project.

## 6. A three-common-note reduction outside a small collision regime

This is a second structural restriction that may make the remaining cylinder
classification tractable.

**Lemma E.** Put r_A(t)=#{(x,y) in A^2:x-y=t}. For homometric six-subsets
A,B in Z_n, if

    E(A) = sum_t r_A(t)^2 > 72,

then a translate of B shares at least three points with A.

Let c(s)=|A intersection (B+s)|. Counting point pairs gives sum_s c(s)=36.
Counting ordered pairs of such intersections in the other order gives

    sum_s c(s)^2 = sum_t r_A(t) r_B(t) = E(A),

where the last equality uses homometry. If every c(s)<=2, then
c(s)^2<=2c(s) pointwise, so E(A)<=72. This proves the claim.

In a six-set, r_A(0)=6 and sum_(t!=0) r_A(t)=30. Thus

    E(A)=66 + sum_(t!=0) r_A(t)(r_A(t)-1).

Every non-antipodal repeated interval class with multiplicity two adds four
to this excess, because the directed residues t,-t both occur twice. A
multiplicity-three ordinary class adds twelve, already too large. An
antipodal unordered pair adds two; two antipodal pairs add twelve.
Consequently failure of the energy criterion confines the pair to this
precise regime: **at most one ordinary interval class occurs twice, all
other ordinary classes occur at most once, and there is at most one
antipodal pair.** This is necessary for a counterexample to the three-common-
note reduction, not evidence that every such near-collision-free pair fails
it.

The existing independently enumerated n=12..60 data has 32,106 pair edges.
A dedicated Counter-based cross-correlation scan, checked independently by
all 2n rigid set intersections, finds:

| Largest intersection under T/I | Pair edges |
| ---: | ---: |
| 3 | 3,130 |
| 4 | 25,197 |
| 5 | 3,779 |

The energy lemma proves the reduction for 20,605 of these edges directly;
the other 11,501 still have an overlap of at least three by computation.
It remains **[OPEN]** whether every six-note Z-pair in every Z_n can be
T/I-aligned to share at least three points. No classification proof relies
on that conjecture here. The current data cannot turn it into a theorem.

## 7. Reproduction, failed route, and next obstruction

Run with the pinned environment:

```bash
.venv/bin/python src/six_completeness.py --out results/2026-09-30-six-completeness.json
.venv/bin/python tests/test_six_completeness.py
```

Outputs: `results/2026-09-30-six-completeness.json` and
`results/2026-09-30-six-completeness-tests.json`. Test runtime on this checkout
was 2.6 seconds. New files do not alter the immutable reference or data.
The first test attempted a fourth matching for the collision-free Bloom
example, which has only one. The corrected test uses index zero there;
multiple indices are still checked for the cyclic examples.

The attempted direct completeness route was to classify all oriented images
of one B-star among the fifteen A-edges before imposing the ten residual
triangle equations. There are C(15,5)*2^5 = 96,096 labelled oriented stars,
before vertex and root symmetries. This is much smaller than the full
15!*2^15 matching space, but the remaining signed edge assignments are not
yet bounded by a small structural list. The compression is an approach,
not a completed search or proof.

The concrete next obstruction is to classify the bounded cyclic-cylinder
systems with positive free rank. Full-rank primitive systems need only occur
at moduli <=135, but exhausting those finite seeds is also unfinished. For
the latter, even a census of moduli <=135 would not classify positive-rank
families or prove the three-common-note assertion. The low-collision regime
in Section 6 identifies where a separate structural argument is required.
