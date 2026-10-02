# Arbitrary-cardinality signed matching: universal groups, bounded torsion, and certified lifts

1 October 2026. PQ1/PQ3, arbitrary cardinality and modulus.

**Status: [PROVED], in-house.** The complete written argument received a
separate fresh adversarial review in
`docs/general_matching/GENERAL_MATCHING_REVIEW.md`, with six independent
test groups. This is not external peer review. No novelty claim is made.
The finite signed-matching
presentation is a reduction and a known-pair certificate procedure; by
itself it is not a useful complete catalogue of structural mechanisms or
an efficient inverse solver.

The startup tests and the parent research plan were completed by the parent
agent before this delegated task. This task changes only this note. It
does not launch a census, change the reference, or enter applications.

## 1. Definitions and exact proposed conclusions

Write an abelian group additively. For a labelled tuple
`A=(a_0,...,a_{k-1})`, its directed difference multiset is

    D(A) = multiset of a_j-a_i over all ordered pairs (i,j).

For a binary tuple the entries are distinct. Two binary tuples are
homometric when their directed difference multisets agree. In a cyclic
group this is exactly equality of interval-class vectors. Translation and
inversion mean `A -> t+A` and `A -> t-A`; a Z-pair is homometric and not
equivalent under these operations. No other group automorphism is included
in that equivalence.

Fix `k>=1`, put `m=k(k-1)/2` and `c=2k-2`, and orient the edges of `K_k`
as `(i,j)` with `i<j`. Let `B` be its `m` by `k-1` incidence matrix:
the row `(i,j)` is `e_j-e_i` with the column for vertex zero omitted.
Thus the incidence convention here puts edges in rows.

A signed edge matching is a bijection `pi:E(K_k)->E(K_k)` together with
a sign `epsilon_e in {+1,-1}` for every edge. Define `M` to have the rows

    (e_j-e_i | -epsilon_e(e_l-e_h)),  e=(i,j), pi(e)=(h,l),

with both anchor columns omitted. Equivalently,
`M=[B | -D_epsilon P_pi B]`. Define

    U_M = Z^c / <rows of M>_Z,
    r = rank_Q(M),
    d = c-r,
    T = Tor(U_M),  t = |T|.

An empty presentation has torsion order one. For `k>=2`, let

    q_k = min(2k-2, m),
    T_k = max tau(H),

where the maximum runs over simple graphs on the labelled `k` vertices
with exactly `q_k` edges, and `tau(H)` is the number of spanning trees.
Set `T_1=1`. For `k>=4` this is precisely the proposed `2k-2`-edge graph
maximum. The cap by `m` handles the otherwise impossible edge counts at
`k=2,3`.

**Theorem GM [PROVED].**

1. Every signed matching gives a homometric universal pair of labelled
   tuples in `U_M`. Every group-valued realization of that matching is
   uniquely its image under a homomorphism `U_M -> G`.
2. Every homometric pair of `k`-point subsets of any abelian group comes
   from one of these presentations, after separate anchor translations.
   Signs at differences of order two must be permitted in both directions.
   In any presentation realizing a Z-pair, the universal endpoints are
   binary and T/I distinct.
3. `k-1 <= r <= min(m,2k-2)` and `0 <= d <= k-1` for `k>=2`; for `k=1`
   both ranks are zero. At **every** rank,

       t <= T_k <= floor(4^(k-1)/k)       (k>=2).

   More precisely, there is a simple `r`-edge graph `H` with
   `t <= tau(H)`, so one can also use

       t <= floor((2r/(k-1))^(k-1)/k).

   If `r=k-1`, then `t=1`. The exact low-cardinality possibilities are
   `U_M=0` for `k=1`, `U_M=Z` for `k=2`, and `U_M=Z^2` or
   `Z direct-sum C_2` for `k=3`.
4. If `f:U_M->C_n` realizes a Z-pair, its torsion image has order
   `q` dividing both `n` and `t`. The realized pair factors through a
   binary, T/I-distinct homometric pair in `Z direct-sum C_q`, with
   `q<=T_k`. If `d=0` this intermediate pair lies entirely in `C_q`.
5. If `gcd(n,t)=1` for **one compatible matching**, the original pair is
   the exact reduction of a T/I-distinct integer homometric pair, with
   neither endpoint colliding. An exact integer lift for that matching
   can be computed from a Smith decomposition and checked directly.
6. Consequently, if every prime divisor of `n` exceeds `T_k`, every
   cyclic Z-pair of cardinality `k` is an integer shadow. The explicitly
   computable sufficient bound `floor(4^(k-1)/k)` may replace `T_k`.
   Exact low-cardinality analysis shows that no Z-pairs exist for
   `k<=3`, in any abelian group.

The torsion statement in item 3 is stronger than a bound restricted to
finite universal groups. The crucial point is to choose a maximal minor
which contains **all** first-block columns; arbitrary maximal minors need
not have that form.

## 2. Equality of differences gives an exhaustive signed matching

**Lemma GM1 [PROVED].** For two labelled `k`-tuples, equality of
directed difference multisets is equivalent to the existence of a signed
bijection between their unordered edge occurrences.

For an unordered edge with oriented difference `g`, the two ordered
edge occurrences contribute `g` and `-g`. Partition group elements into
orbits under `g -> -g`.

For an orbit `{g,-g}` with two elements, every edge in that orbit
contributes one occurrence to each element. Equality of directed content
therefore gives exactly the same number of unordered edges in the orbit
on the two sides. For an orbit with one element (`2g=0`, including zero),
each such edge contributes **two** copies of that element. The same
conclusion follows after dividing the equal multiplicities by two.
The `k` diagonal occurrences at zero are common and can first be removed.
This argument also handles tuples with repeated entries, although binary
realizations have no zero unordered edge.

Choose a bijection of edge occurrences separately in each orbit. Each
matched pair has either equal or opposite oriented differences, so assign
the corresponding sign. If `2g=0`, both signs work; dropping one sign is
permitted for finding a single witness but not for an exhaustive list of
all compatible matchings. Conversely, a signed matching identifies every
unordered contribution `{g,-g}` with its counterpart and hence identifies
the directed multisets, including multiplicity. This proves the lemma.

For `C_n`, the orbit key is the usual interval class
`min(delta,n-delta)`, with `delta` chosen in `0,...,n-1`. Thus GM1 is
exactly the cyclic ICV statement, including antipodal intervals.

## 3. Universal soundness, anchoring, collisions, and T/I

Let `x_0=y_0=0` and let the other `x_i,y_j` be the images in `U_M` of
the standard generators. The defining row for a matched edge is exactly

    x_j-x_i = epsilon_e(y_l-y_h).

GM1 therefore gives universal homometry. A homomorphism out of `U_M`
preserves each equation and all multiplicities. Images can collide, so
homometry of labelled tuples alone is not a binary-realization condition.

For any abelian `G`, assigning images to the `c` standard generators
gives a homomorphism `Z^c->G`. It factors through `U_M` if and only if it
kills every defining row, which is if and only if its coordinate tuple
satisfies `M v=0` in `G`. Uniqueness follows because the standard
generators generate `U_M`. This proves the universal solution assertion.

Given an actual homometric pair, independently choose a point in each
endpoint and subtract it from that endpoint. Differences are unchanged.
Apply GM1 to the anchored tuples to obtain a compatible signed matching.
The preceding universal property supplies the required map. Adding the
two original anchors back recovers the precise original pair; separate
translations do not alter homometry or either endpoint's T/I class.

If two universal coordinates within one endpoint were equal, their
images would be equal, contradicting binary distinctness of the actual
endpoint. If the universal endpoint sets satisfied `Y=s+epsilon X`,
their images would satisfy the same T/I relation. Consequently a
presentation mapping to a Z-pair has binary, noncongruent universal
endpoints. The converses need not hold for an arbitrary image.

The following is an exact finite test for a proposed image of a universal
pair. Require every within-endpoint difference to be nonzero. Because both
endpoints contain zero, any T/I equivalence must have translation
`s=-epsilon x_h` for some source point `x_h`. Thus test the `2k` candidates

    Y = epsilon (X-x_h).

Equality here is equality of actual finite sets. This checks T/I without
identifying endpoints under unit multiplication or other automorphisms.
It also shows that embedding an anchored pair into a larger group cannot
create an extra T/I equivalence: the required translation lies in the
subgroup generated by the points.

## 4. Incidence minors and the rank bound

**Lemma GM2 [PROVED].** Every square minor of a reduced oriented
incidence matrix is `0,+1,-1`; the same is true after row permutations,
row sign changes, and selecting only some columns.

Here is an elementary proof, avoiding any separate total-unimodularity
input. In a square submatrix each row has at most two nonzero entries.
If a row has zero entries the determinant vanishes. If it has one entry,
expand along that row and use induction, since its entry is `+1` or
`-1`. If every row has two entries, those entries have opposite signs,
so the all-ones vector is in the kernel and the determinant vanishes.
The empty minor has determinant one. This proves the assertion and is
unchanged by row signs or permutations.

The full first block `B` has column rank `k-1`: select the `k-1` edges
from the anchor to the other vertices to obtain an identity matrix up
to signs. Therefore `rank M>=k-1`. Its row and column counts give the
upper bound in GM. Since `d=2k-2-r`, the claimed free-rank bound follows.
No assumption about binary realizability is required for these bounds.

For completeness there is a separate, coarser all-minors argument. An
`r` by `r` minor using `a` first-block columns and `r-a` second-block
columns expands into `binom(r,a)` products of incidence minors, all with
absolute value at most one. Its absolute determinant is at most
`binom(r,a) <= binom(2k-2,k-1)`. Smith normal form identifies `t` with
the gcd of all nonzero `r` by `r` minors, so

    t <= binom(2k-2,k-1).

For `d>0`, the same argument gives
`t<=binom(2k-3,k-2)` when `k>=2`. These coarse bounds are valid, but the
next section improves the uniform bound at every rank.

## 5. The spanning-tree bound works at every rank

**Lemma GM3 [PROVED].** There is a simple `r`-edge graph `H` on
`k` vertices such that `t<=tau(H)`.

The `k-1` first-block columns are independent in the full matrix `M`.
Extend them to a basis of its column space by adding
`r-(k-1)` columns from the second block. This gives `r` columns of rank
`r`. Choose `r` rows for which the resulting square matrix `N` is
nonsingular. Those rows correspond to `r` distinct edges of the **first**
copy of `K_k`; let `H` be that simple graph. The first `k-1` columns of
`N` are exactly the full reduced incidence matrix of `H`, restricted to
these rows.

Expand `det N` along these first `k-1` columns. A selected `k-1`-row
incidence minor is nonzero if and only if its edges form a spanning tree
of `H`, and then has absolute value one. To verify that criterion:
a cycle gives a signed linear dependence among edge rows; an acyclic
set of `k-1` edges on `k` vertices is a tree; and leaf elimination gives
determinant `+1` or `-1` for a tree, with the anchor omitted. Equivalently,
if the selected graph is disconnected its reduced incidence matrix has
rank less than `k-1`.

Every complementary minor has only second-block columns and has absolute
value at most one by GM2. There is one potentially nonzero expansion term
per spanning tree of `H`. Consequently

    0 < |det N| <= tau(H).

The order `t` of the torsion subgroup is the gcd of **all** nonzero
rank-sized minors. In particular it divides this chosen nonzero `det N`,
so `t<=|det N|<=tau(H)`. This is why it is legitimate to choose the minor
containing all first-block columns. One does not need to bound every
arbitrarily selected maximal minor by the tree count.

The graph `H` has `r<=q_k` edges. Add unused edges until it has `q_k`
edges. Existing spanning trees remain spanning trees, so their count
cannot decrease. Hence `tau(H)<=T_k`. If `r=k-1`, the nonzero determinant
forces `H` itself to be a tree and forces `t=1`.

### Analytic bound, including its constant

Let `H` have `r` edges and Laplacian `L`. Cauchy--Binet applied to its
reduced incidence matrix gives

    det L_reduced = sum (tree-incidence determinants)^2 = tau(H).

If `H` is connected, its Laplacian eigenvalues are
`0,lambda_1,...,lambda_{k-1}`, all remaining eigenvalues positive, and

    sum lambda_i = trace L = 2r,
    product lambda_i = k tau(H).

For the second identity, the adjugate of a connected Laplacian is
`tau(H) 11^T`: its columns are in the one-dimensional kernel and its
diagonal cofactors are the just-established tree count. The determinant
of `L+(1/k)11^T` is then `k tau(H)` by the rank-one determinant expansion;
its eigenvalues are `1,lambda_1,...,lambda_{k-1}`, giving the identity.
For a disconnected graph the tree count is zero and the bound is immediate.

Arithmetic--geometric mean now yields

    tau(H) <= (1/k) (2r/(k-1))^(k-1)
           <= 4^(k-1)/k,

since `r<=2k-2`. Both tree count and torsion order are integers, so floors
are permitted. This proves the rank-specific and uniform analytic bounds
in GM. There is no graph enumeration in this analytic argument.

For `k>=4`, the full-rank case uses exactly `2k-2` selected rows and
recovers the originally proposed sharp graph maximum. The same maximum
also bounds every smaller-rank presentation by the basis-extension and
edge-addition argument above. It is not asserted that `T_k` is attained
as the torsion order of a signed-matching presentation.

The existing separately reviewed six-point graph calculation establishes
`T_6=135` in `2026-09-30-six-completeness.md`, with its two independent
enumerations attacked in `2026-09-30-six-cylinder-templates-review.md`.
The general argument here consequently recovers the sufficient bound
`t<=135` at **all** six-point ranks. The analytic formula alone gives
`t<=170` there. No new numerical value of `T_k` is asserted in this note.
For `k=7`, the analytic bound is the explicit sufficient value `585`.

## 6. Low cardinalities, with no division in the target group

For `k=1` the universal group is zero and all singleton sets are
translation equivalent. For `k=2` there is one relation `x_1=epsilon y_1`,
so the universal group is `Z` and its two endpoints are inversion
equivalent.

For `k=3`, every permutation of the three edges of a triangle is induced
by a permutation of its vertices. Relabel and reanchor the second tuple
accordingly; orientation changes merely change the recorded signs. Thus
any matching reduces to the edgewise matching between
`A=(0,x_1,x_2)` and `B=(0,u,v)`. Reflect the first endpoint if necessary
so the sign on edge `(0,1)` is positive. Write the other two signs as
`s` on `(0,2)` and `z` on `(1,2)`. The equations are

    x_1=u,  x_2=s v,  s v-u = z(v-u).

There are four cases.

* `s=z=1`: no further relation, `U_M=Z^2`, and `A=B`.
* `s=1,z=-1`: the remaining relation is `2(v-u)=0`; still `A=B`.
* `s=-1,z=1`: the remaining relation is `2v=0`, so `-v=v` and `A=B`.
* `s=z=-1`: the remaining relation is `2u=0`, so `-u=u` and `A=-B`.

In each of the last three cases a primitive change of the two generators
identifies the presentation with `Z direct-sum C_2`. No element of the
target group was divided by two. Thus the low-cardinality group statements
and the absence of Z-pairs hold in arbitrary abelian groups, including
groups with two-torsion. The graph bound gives `T_2=1,T_3=3`; the explicit
triangle argument improves the latter torsion bound to two.

## 7. Cyclic factorization through a bounded cylinder

Choose an abstract splitting `U_M=Z^d direct-sum T`. Let
`f:U_M->C_n` be a map realizing an actual Z-pair. Its finite torsion image
`H=f(T)` is a subgroup of `C_n`, hence cyclic. Write its order as `q`.
By the first isomorphism theorem and subgroup order,

    q divides t,  q divides n,  q <= t <= T_k.

The subgroup `H` is generated by `n/q`. Thus there is a homomorphism
`chi:T->C_q` such that `f(tau)=(n/q)chi(tau)` in `C_n`.
For each chosen free generator choose any integer lift `a_i` of its
`f`-image. Define

    ell(z) = sum a_i z_i,
    p(z,tau) = (ell(z), chi(tau)) in Z direct-sum C_q,
    h(s,c) = s + (n/q)c in C_n.

Then **exactly** `f=h p`. Applying `p` to the universal tuples preserves
homometry. Any endpoint collision or T/I equivalence in this intermediate
image would persist under `h`, contradicting the properties of the actual
Z-pair. Therefore the intermediate pair is binary and T/I distinct.
If `d=0`, its first coordinate is zero, so it lies in the finite group
`C_q` alone. For `q=1` the intermediate group is just `Z`.

This compression does not assert that `T` itself is cyclic. Only its
actual image is cyclic. Nor does it assert that the free image and the
torsion image inside `C_n` are disjoint; they can overlap. The construction
uses the actual images of the chosen free generators and the identity
`f=h p`, not an assumption of genericity.

For an arbitrary finite abelian target, retain `Z^d direct-sum f(T)`
instead. That finite factor has order at most `T_k`, but it need not be
cyclic and the free image need not compress to a single `Z` coordinate.
The universal statement in Sections 2--5 does not require a cyclic target.

## 8. Integer shadows and an exact, usable known-pair procedure

**Corollary GM4 [PROVED].** If `gcd(n,t)=1` for one compatible
matching, the original cyclic Z-pair has a nontrivial binary integer
homometric lift realizing that matching.

Every element of `T` is killed by `t`. An element of `C_n` killed by `t`
is zero when `gcd(n,t)=1`, by a Bezout identity. Thus `f(T)=0` and the
preceding cylinder has `q=1`. Its integer pair reduces exactly to the
original anchored pair. If its integer endpoints collided, their modular
endpoints would collide. If it were translation/inversion equivalent,
reduction of that relation would make the actual modular endpoints T/I
equivalent. This proves the asserted binary and nontrivial properties.
Add any integer representatives of the two original anchors back to
recover the original unanchored pair under reduction.

Here is an explicit version that needs only one chosen matching. This
procedure does not enumerate `m! 2^m` patterns.

1. Given two binary cyclic endpoints, anchor them separately and form
   all `m` oriented edge differences. Sort each edge list by the unsigned
   residue `min(delta,n-delta)`, breaking ties by the edge labels. If the
   sorted key lists differ the endpoints are not homometric. Otherwise
   pair corresponding occurrences and choose the sign satisfying
   `delta_A=epsilon delta_B mod n`, choosing `+1` in the antipodal case.
   This deterministically supplies one valid matrix `M` in
   `O(k^2 log k)` comparisons and modular operations.
2. Compute an exact Smith decomposition with integer unimodular matrices
   `P,Q` such that

       P M Q = D = diag(s_1,...,s_r,0,...,0),
       s_i>0,  s_i divides s_(i+1).

   Here `P` has size `m` and `Q` has size `c`; rectangular diagonal zero
   rows/columns are retained. Then `t=product s_i`, and `d=c-r`.
3. Let `v` be the anchored coordinate vector in `(C_n)^c` and put
   `z=Q^{-1}v mod n`. The equations imply `s_i z_i=0 mod n` for
   `i<=r`. If `gcd(n,t)=1`, each `s_i` is invertible modulo `n`, so
   `z_i=0 mod n` for all those indices.
4. More generally, an integer lift realizing this **specific matching**
   exists if and only if `z_i=0 mod n` for all `i<=r`. If so, lift the
   remaining `d` coordinates to arbitrary integers, set the first `r`
   coordinates to integer zero, and return

       w = Q (0,...,0, lifted z_(r+1),...,lifted z_c)^T.

   Then `M w=0` over the integers and `w=v mod n`.

The exact criterion in item 4 follows because integer solutions of
`D z=0` have the first `r` coordinates zero, while their remaining
coordinates are free. The transformations are unimodular, so this is
equivalent to the original integer system and its modular reduction.
If a computation writes a Smith certificate, verify the full matrix
identity and both unimodular determinants; one selected determinant
alone does not give the Smith invariants. The final integer-shadow
certificate is even simpler to check: the matching/sign list, exact
vector `w`, the identities `M w=0`, and `w=v mod n` suffice. They imply
integer homometry directly, independently of how the Smith form was found.

Failure of item 4 proves absence of an integer lift for **that matching**
only. Another compatible matching may admit a lift. It does not certify
that a pair is non-shadow, and the existence of nonzero universal torsion
does not certify non-shadow status. Conversely, when the direct lift
certificate succeeds it establishes shadow status even if `gcd(n,t)>1`.

No practical runtime guarantee is claimed here for a particular Smith
implementation. The input matrix has `O(k^2)` rows, `O(k)` columns and
entries in `{-1,0,1}`. A single matrix computation on a supplied pair is
the intended use of this certificate procedure. The inverse problem of
finding all endpoints from a supplied interval vector is a separate
algorithmic task, under development in the parent workstream.

### A fixed-cardinality arithmetic consequence

For fixed `k`, all possible universal torsion primes are at most `T_k`.
If every prime divisor of `n` exceeds `T_k`, then `gcd(n,t)=1` for every
matching. By GM4, every cyclic Z-pair of cardinality `k` is an integer
shadow. The same holds for every modulus satisfying the stronger numerical
condition that its prime divisors exceed `floor(4^(k-1)/k)`.

The condition concerns **prime divisors**, rather than the magnitude of
`n`. Arbitrarily large multiples of a small prime can retain torsion.
For a supplied matching, using the exact `t` or the exact zero-coordinate
criterion is more informative than using the uniform bound.

The draft does not identify the smallest valid prime cutoff. It does not
assert that every prime up to the bound occurs in a realizable matching,
that any such torsion produces a Z-pair, or that the determinant bound is
attained. It only gives a rigorous sufficient arithmetic reduction.

## 9. Why bounded torsion does not classify the remaining configurations

Passing from `U_M` to `U_M/T` preserves homometry of labelled tuples, but
may collapse endpoint points or make the two endpoint multisets T/I
congruent. A real or integer projection always kills torsion. Therefore
a nontrivial binary pair in `U_M` need not become a nontrivial binary pair
in its free quotient. This is a genuine obstruction when the target map
uses torsion; it cannot occur for the actual factorization used in GM4.

Here is an explicit algebraic example. In
`G=Z r direct-sum C_4 t`, take

    A=(0,r,r+t,2t),
    B=(0,r+t,2t,r+2t).

The signed matching of edges is

    A01 -> +B23,   A02 -> +B01,   A03 -> +B02,
    A12 -> +B13,   A13 -> -B03,   A23 -> +B12.

All six equalities hold: the only equality using a torsion relation is
`2t-r=-(r+2t)`, which uses `4t=0`. In fact this is exactly the universal
presentation of that matching. Writing its unknowns as
`(a,b,c;u,v,w)`, elimination gives

    b=u, c=v, w=a+c, 2c=0, 2u-2a-c=0.

Put `r=a` and `t=u-a`; then `c=2t` and the sole remaining relation is
`4t=0`. Thus the universal group is `Z direct-sum C_4`, with the displayed
coordinates.

Both endpoints are binary. They are T/I distinct in this group: for a
translation with positive sign the two free heights force translation
height zero. The height-zero fiber `{0,2t}` allows torsion shift only
`0` or `2t`, neither of which maps the height-one fiber `{0,t}` onto
`{t,2t}`. For an inversion, the two heights force translation height
one, and the height-zero target fiber would have to be an inversion and
translation of an adjacent pair, which cannot be the antipodal pair
`{0,2t}`. Nevertheless both free-quotient tuples are the **same** multiset
`(0,r,r,0)` up to ordering; the free quotient has collisions.

The cyclic map `r->1,t->3` into `C_12` gives
`{0,1,4,6}` and `{0,4,6,7}`. Their cyclic gap multisets are respectively
`{1,2,3,6}` and `{1,2,4,5}`, so they are T/I distinct there too. This
example is the classical four-point mechanism; no novelty is attributed
to it. The point of the example is the exact distinction between universal
binary injectivity and injectivity of a torsion-free projection.

Even when a chosen free projection happens to remain binary, proving its
real T/I equivalence does not prove T/I equivalence before torsion is
removed. One must control the torsion arrangement over that projection.
Likewise, an abstract homometric integer projection does not automatically
lift the **original modular coordinates** when their map uses torsion.
The identity through the actual map in Section 7, or the explicit lattice
lift criterion in Section 8, is needed for that conclusion.

## 10. Remaining structural and algorithmic gap

For each fixed `k` there are only finitely many signed patterns, with free
rank at most `k-1` and bounded finite torsion. This does not yet compress
the presentations into a short list of meaningful generators. The raw
`m! 2^m` menu grows too quickly to serve as that compression.

The unresolved work is to organize the binary, T/I-distinct images of the
positive-free-rank presentations into explicit structural mechanisms,
including repeated free heights and torsion arrangements over congruent
free projections; organize finite-rank-zero cyclic images without merging
actual T/I endpoints; and provide useful inverse generation/enumeration
with certified completeness boundaries. At large prime divisors, the
remaining structure is still the general integer homometry problem, not
an automatic six-point Bloom classification at every cardinality.

The already reviewed six-point theorem addresses these structural tasks
at `k=6` using special proofs and finite certificates. The general
determinant and lifting arguments above do not transplant that particular
classification to `k>=7`. A finite tree-count calculation can improve a
cutoff but cannot close this structural gap.

## 11. Completed independent review obligations

The separate attack checked:

1. Directed versus unsigned multiplicities at zero and two-torsion;
   independent anchors and orientation changes.
2. The full first-block basis extension for arbitrary rank; why a single
   selected minor suffices for torsion order; the simple-graph row count;
   the matrix-tree constant `1/k` and the low-cardinality edge cap.
3. The distinction between noncyclic `T` and its cyclic actual image;
   the exact identity `f=h p`; preservation of binary and T/I properties
   through that identity.
4. The direction of the Smith change of variables `v=Q z` and the exact
   matching-specific lift criterion, including `gcd(n,t)>1` cases.
5. The absence of any inference from one failed matching to non-shadow
   status, or from a free-projection congruence to universal congruence.
6. The triangle sign analysis in groups with two-torsion and the explicit
   `Z direct-sum C_4` counterexample.

No Lean toolchain was available. The separate review independently checked
the low-cardinality presentations, Smith identities, the counterexample,
and saved graph certificates. Formalizing the incidence-minor,
basis-extension, and Smith-lift lemmas remains useful. The review identifies
the original draft by its hash; subsequent edits here promote status and
record that review without changing the argument. Historical comparison and novelty
search belong to the parent literature workstream; this note supplies no
new priority claim and cites no unread `[LIT-VERIFY]` source.
