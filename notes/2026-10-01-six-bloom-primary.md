# Classical six-point Bloom pair fibres in every cyclic modulus

1 October 2026. **[PROVED], in-house, computer-assisted, after the separate
fresh attack in `notes/2026-10-01-six-primary-review.md`.**
The exact tables and finite controls below are **[COMPUTED]**. No novelty
claim. This theorem classifies the image of the classical two-parameter
Bloom construction, not all cyclic six-point homometry.

## 1. Statement

For `v=(a,b)` in `(Z/n)^2`, put

\[
 X_v=(0,a,b-2a,2b-2a,2b,3b-a),\qquad
 Y_v=(0,a,b+2a,2b-a,2b+a,3b-a).
\]

Let Ω_n consist of parameters for which both lists contain six distinct
points. Define Φ(v) to be the unordered pair of their independent
translation/reflection classes. No general unit multiplication is
quotiented out. Let

\[
 R=\begin{pmatrix}0&-1\\1&-1\end{pmatrix},\quad
 T=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
 G=\{\pm R^iT^j:0\le i<3,\ 0\le j<2\}.
\]

If `12|n`, write `h=n/12` and define three free G-orbits

\[
 C_n=G(h,5h),\qquad A_n=G(h,4h),\qquad B_n=G(3h,7h).
\]

**Theorem AP [PROVED] (all-modulus pair fibres).** For every positive n:

1. G acts freely on Ω_n and preserves Φ. Every parameter in Ω_n gives
   homometric endpoints.
2. The endpoints are congruent exactly on C_n when `12|n`; there are no
   congruent parameters when `12∤n`.
3. Every nontrivial pair fibre is one G-orbit, except that, when `12|n`,
   the single fibre `A_n ∪ B_n` is a union of two G-orbits. These two
   orbits represent the ordinary inflation of the 12-point pair
   `{0,1,2,3,6,8}` / `{0,1,2,4,6,7}`.

In particular, the number of nontrivial unordered pair edges represented
by the Bloom construction is

\[
 B(n)=|\Omega_n|/12-2[12\mid n].
\]

This count is of pair edges. A maximal full homometry family may contain
non-Bloom edges, and distinct Bloom pair edges may share an endpoint.
The theorem does not claim an all-modulus disjoint classification of
those endpoint graphs or of the full generation grammar.

The separate proof `notes/2026-10-01-six-bloom-support.md` supplies

\[
\begin{split}
|\Omega_n|={}&n^2-(9+3\gcd(n,2))n+11+15[2\mid n]+16[3\mid n]\\
&+18[4\mid n]+24[5\mid n]+12[6\mid n]+24[7\mid n]+12[8\mid n].
\end{split}
\]

That support formula is an explicitly separate proof dependency; pair
fibre identification below does not infer it from a numerical fit.

## 2. Denominator-free complete matching

Use the actual coefficient rows

\[
 P_X=((0,0),(1,0),(-2,1),(-2,2),(0,2),(-1,3)),
\]
\[
 P_Y=((0,0),(1,0),(2,1),(-1,2),(1,2),(-1,3)).
\]

Any equality `Φ(w)=Φ(v)` has one endpoint assignment `j∈{0,1}`,
independent signs `s_x,s_y∈{±1}`, independent permutations
`π_x,π_y∈S_6`, and independent translations. Put
`(U_x,U_y)=(P_X,P_Y)` for j=0 and `(P_Y,P_X)` for j=1. Its first
endpoint equation is

\[
 P_Xw=s_x(U_xv)_{[\pi_x]}+t_x\mathbf1.
\]

Subtract the label-zero equation from every equation. The rows for
labels 1 and 2 on the left are `(1,0)` and `(-2,1)`, determinant one.
They give the exact integer matrix relation `w=Mv`, with rows

\[
 M_1=s_x(U_{x,\pi_x(1)}-U_{x,\pi_x(0)}),
\]
\[
 M_2=s_x(U_{x,\pi_x(2)}+2U_{x,\pi_x(1)}-3U_{x,\pi_x(0)}).
\]

The three remaining first-endpoint equations and five nonanchor
second-endpoint equations become `Hv=0`, where H is an integer 8×2
matrix. Conversely, `w=Mv` and `Hv=0` recover both original translations
by the matched anchor equations. This is an equivalence over **every**
`Z/n`; neither centering nor division by 2, 3, 6, or a determinant is
used. All `2·4·720²=4,147,200` cases are enumerated without quotienting.

For a residual H let c be its entry gcd and D its 2×2 minor gcd. The
complete exact result is:

| Residual rank | Cases | Acceptance property |
|---|---:|---|
|0|12|M is one of the twelve G matrices; j equals its T exponent|
|1|864|Primitive direction is a support-collision normal; c=1, or c=2 on a,b,a−b only|
|2|4,146,324|D belongs to `{1,2,3,4,5,6,7,8,9,12,13,16,19}`|

The rank-two histogram, retaining c rather than only D, is

```
(c,D): cases
(1,1):3970476  (1,2):145944  (1,3):12384  (1,4):12420
(1,5):936     (1,6):936     (1,7):912    (1,8):540
(1,12):108    (1,13):24    (1,19):24
(2,4):1476    (2,8):72     (2,12):12   (2,16):36
(3,9):12      (4,16):12
```

The finite catalogue is
`results/2026-10-01-six-bloom-primary/pair-certificate.json`.
Every histogram class retains a full matching witness and exact H,M.
Actual largest absolute entry and minor are 27 and 112, respectively;
int64 arithmetic is therefore exact with a large safety margin. The
full NumPy table took 1.687 seconds after a 72,000-case benchmark.

The twelve primitive collision directions are
`(1,0),(0,1),(1,-1),(1,1),(2,-1),(2,1),(3,-1),`
`(1,-2),(1,2),(3,-2),(1,-3),(2,-3)`, up to sign. The actual raw
collision equations include `2a=0`, `2b=0`, `2(a−b)=0` and the other
nine primitive equations. Thus every rank-one kernel in the table
forces an actual support collision for every modulus, including even n.
The extra factor two is retained, not cancelled.

## 3. Why the finite table gives an arbitrary-modulus theorem

For rank two, `Hv=0` implies `Dv=0`: multiplying each pair of row
equations by its adjugate gives `det(B)v=0`; taking a Bézout integer
combination of the finitely many determinants gives the assertion.
This uses neither a Smith decomposition nor division by a minor.

Set `d=gcd(n,D)`. The solutions of `Dx=0 mod n` are exactly the unique
order-d subgroup `K_d=(n/d)Z/n`. Consequently **both coordinates of v
and w** lie in K_d; w lies there because `w=Mv` is an integer matrix
relation. Write `v=(n/d)v_0,w=(n/d)w_0` with parameters over `Z/d`.

The subgroup embedding is injective. Thus the global lists are actual
six-element sets iff their lists over `Z/d` are. A rigid equivalence
between two sets supported in K_d has translation in K_d: subtract a
matched signed source point from its target point. All endpoint
equivalences and unordered pair equalities therefore descend to `Z/d`.

The possible d are exactly among
`{1,2,3,4,5,6,7,8,9,12,13,16,19}`. Every parameter of every one of
these moduli has been enumerated twice, once with an independently
implemented gap-word class key, and once with the immutable reference's
full translation/reflection class key:

| d | Actual parameters | Congruent parameters | Nontrivial pair edges | Nontrivial fibre sizes |
|---|---:|---:|---:|---|
|1,2,3,4,5,6,7,8,9|0|0|0|—|
|12|36|12|1|24|
|13|24|0|2|12|
|16|72|0|6|12|
|19|144|0|12|12|

Both methods retain the full fibres and formal G-orbit partitions, not
only the counts. Their certificates are `small-gap-images.json` and
`small-reference-images.json`. At d12 the exact three G-orbits have
representatives `(1,5)`, `(1,4)`, `(3,7)`, respectively. The first has
equal endpoint class `{0,1,2,3,5,7}`. The other two have the displayed
nontrivial pair. Thus the finite exceptions identified in §1 are exact.

Rank zero gives G directly. Rank one is impossible on Ω. Rank two
reduces to the preceding finite theorem; only d12 can introduce
additional fibres or congruent endpoints. Its ordinary subgroup
inflations have exactly the same parameters and equivalences.
In particular, a parameter in an exceptional order-12 orbit cannot
acquire a matching partner outside K_12: every rank-zero partner stays
inside it, and a rank-two partner forces its order to divide a listed D;
the only listed D divisible by 12 is 12 itself.

## 4. Freeness, congruence, and counting

The two lists have the same fifteen difference coefficient rows, up to
independent signs, with multiplicities:
`(0,1),(0,2),(1,-3),(1,-2),(1,-1),(1,0),(1,1),(1,2),`
`(2,-3),(2,-2),(2,-1),(2,0),(2,1),(3,-2),(3,-1)`.
Evaluation modulo any n gives identical signed difference multisets,
and therefore identical cyclic autocorrelations whenever the supports
are actual sets. This proves homometry directly in every modulus.

Formal integer affine endpoint identities prove G preserves Φ in every
ring. The rank-zero certificate records the twelve integer matrices,
the actual label permutations, endpoint assignments, and signs. These
coefficient identities can be checked without a modulus.

For freeness, the fixed-vector equations for the six reflections
`±R^iT` force one of
`a=b,a=0,b=0,a=−b,a=2b,b=2a`, all actual collision equations. The two
nonidentity positive rotations have `det(I−R^i)=3`, and hence a fixed
parameter is supported in the order-gcd(n,3) subgroup, which has fewer
than six points. The matrices `I+R` and `I+R²` have determinant one and
fix only zero. Negation fixes only parameters with `2a=2b=0`, again an
actual support collision. Therefore every Ω_n G-orbit has size12.

If the endpoints of v are congruent, combining that transport with its
inverse gives a swapped pair matching with w=v. In rank zero its matrix
is a reflection `±R^iT`, which cannot fix an actual parameter by the
previous paragraph. Rank one is impossible. Rank two descends to the
small table, whose only congruent parameters are `G(1,5)` at d12.
This proves the exact congruent set C_n. It has twelve parameters.

All remaining pair fibres have size twelve, except the one inflated
24-parameter fibre. Remove the twelve congruent parameters, divide the
remainder by twelve, and subtract one for the merged pair of G-orbits.
The resulting edge count is `|Ω_n|/12−2[12|n]`.

## 5. What remains unfinished

There is an explicit infinite even-modulus obstruction to isolated
Bloom edges. For **every** `n=2m≥18`, put

\[
 v=(m+3,1),\qquad w=(-3,m-2).
\]

The actual lists, written as sets of residues, are

\[
 X_v=\{0,2,2m-5,2m-4,m,m+3\},
\]
\[
 Y_v=\{0,7,m-1,m,m+3,m+5\},
\]
\[
 X_w=\{0,2,2m-4,2m-3,m-3,m+4\},
\]
\[
 Y_w=\{0,m-8,m-3,2m-7,2m-3,2m-1\}.
\]

For m≥9 every displayed set has six distinct residues. Direct
subtraction gives `X_w=Y_v−(m+3)`. This is the rank-one endpoint
matching with

\[
 M=\begin{pmatrix}-2&3\\-3&7\end{pmatrix},\qquad
 H=\begin{pmatrix}-2&6\\-4&12\\-6&18\end{pmatrix};
\]

its residual condition is `2(a−3b)=0`, and our parameters have
`a−3b=m`, an actual half-period rather than zero. Both v and w generate
the full cyclic modulus: v has b=1; if a common divisor divides 2m,
3, and m−2 for w, it must be 3, but then it would divide both m and
m−2, impossible. Since n>12 neither parameter can lie in any of the
three order-12 exceptional orbits, including the two merged orbits.
The possible first coordinates in Gv are
`±1,±(m+3),±(m+2)`; none equals `−3 mod2m` for m≥9. Thus w is not in
Gv, and AP says the two nontrivial pair edges are different. They share
the class `[Y_v]=[X_w]`, giving at least three different Bloom vertices
in one component at every even modulus n≥18. This is an explicit
parametric shared-endpoint mechanism, not a claim of novelty or of
complete even endpoint classification.
The immutable-reference certificate verifies all 120 even moduli from
18 through 256, with the four actual supports, their three T/I classes,
and exact interval vectors retained in `even-endpoint-controls.json`.
This bounded check supports the displayed arbitrary-m proof; it is not
a six-subset census.

The single-endpoint denominator-free table has 5,760 cases and ranks
`24,432,5304`. Unlike the paired table, its rank-one residuals can have
content two on six primitive normals whose **actual** collision
equations have content one. Their kernels can therefore survive on
globally six-point supports in even moduli. Its rank-two minor gcds
also include 20,28,31,36,39. This leaves genuine periodic even-modulus
shared-endpoint mechanisms; the all-modulus endpoint graph is not yet
classified. The exact endpoint table is retained in
`endpoint-certificate.json` for that next problem. This obstruction does
not affect the pair-fibre theorem, whose separate paired table excludes
these residuals.

The theorem classifies a classical construction. Historical priority
for these image identifications/counts remains unestablished. General
six-point generation and any total-count corollary retain the
dependencies and limitations of the separately reviewed Theorem G.

## 6. Reproduction

From the repository root, use only the pinned environment:

```
.venv/bin/python src/six_bloom_primary.py --limit 72000 --out results/2026-10-01-six-bloom-primary/benchmark.json
.venv/bin/python src/six_bloom_primary.py --out results/2026-10-01-six-bloom-primary/pair-certificate.json
.venv/bin/python src/six_bloom_primary.py --endpoint --out results/2026-10-01-six-bloom-primary/endpoint-certificate.json
.venv/bin/python src/six_bloom_primary.py --images 1 2 3 4 5 6 7 8 9 12 13 16 19 --out results/2026-10-01-six-bloom-primary/small-gap-images.json
.venv/bin/python src/six_bloom_primary.py --images 1 2 3 4 5 6 7 8 9 12 13 16 19 --reference --out results/2026-10-01-six-bloom-primary/small-reference-images.json
.venv/bin/python src/six_bloom_primary.py --even-endpoints 9 128 --out results/2026-10-01-six-bloom-primary/even-endpoint-controls.json
.venv/bin/python tests/test_six_bloom_primary.py
```

The separate fresh attack in `notes/2026-10-01-six-primary-review.md`
accepts AP, the support formula and the explicit even-modulus
shared-endpoint family. Its independently implemented complete matching
replay is `src/six_bloom_primary_review.py`; exact evidence and frozen
digests are in `results/2026-10-01-six-primary-review/`.
No novelty or external human peer-review claim follows from that attack.
