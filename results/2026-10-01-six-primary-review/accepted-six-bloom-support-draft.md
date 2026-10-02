# Exact support parameters at every cyclic modulus

1 October 2026. **[OPEN] draft pending a fresh adversarial attack.**
This concerns the classical two-parameter six-point construction. It counts
parameters with six distinct points on each side; it includes parameters
whose endpoints are congruent. It is not by itself a count of Z-pairs.
The general arrangement-counting method is classical, as credited in
`notes/2026-09-30-six-composite-literature.md`; no novelty claim is made.

## Statement

For positive integer n, let Ω_n consist of (a,b) in (Z/n)^2 such that

\[
X=(0,a,b-2a,2b-2a,2b,3b-a),\qquad
Y=(0,a,b+2a,2b-a,2b+a,3b-a)
\]

both have six distinct coordinates. Write [m|n] for the divisibility indicator.
Then

\[
\begin{split}
|\Omega_n|={}&n^2-(9+3\gcd(n,2))n+11+15[2|n]+16[3|n]\\
&+18[4|n]+24[5|n]+12[6|n]+24[7|n]+12[8|n].
\end{split}
\]

For odd n this recovers the previously reviewed formula
n²−12n+11+16[3|n]+24[5|n]+24[7|n]. For even n it is

\[
n^2-15n+c_{v_2(n)}+28[3|n]+24[5|n]+24[7|n],
\quad c_1=26,\ c_2=44,\ c_{\ge3}=56.
\]

These are uniform formulas; they do not follow from a bounded modulus census.

## Proof by additive orders of overlap points

Subtract every pair of coefficient rows in X and Y, orienting a normal
so its first nonzero entry is positive. Both endpoints give the same
fifteen distinct normals. Three primitive normals (0,1),(1,0),(1,−1)
also occur doubled. Their primitive kernels are contained in their doubled
kernels, so the complete union of collision conditions is the union of
exactly the following twelve kernels, without division by a nonunit:

\[
K=\{(0,2),(1,-3),(1,-2),(2,-2),(1,1),(1,2),
 (2,-3),(2,-1),(2,0),(2,1),(3,-2),(3,-1)\}.
\]

Here the kernel of (u,v) is the equation ua+vb=0 modulo n.
The nine primitive normals each have a kernel of size n, by Bézout.
Each of the three doubled primitive normals has kernel size
n·gcd(n,2), again by transforming the primitive linear map into a
coordinate projection. Thus the sum of the twelve kernel sizes is
(9+3gcd(n,2))n.

All pairs of distinct normals are linearly independent over Q. Their
absolute determinants belong to {1,2,3,4,5,6,7,8}; this is checked directly
from the displayed twelve rows. If a parameter v lies on two kernels,
the adjugate identity says that their determinant annihilates v.
Consequently the additive order m of a nonzero parameter lying on two
or more kernels must belong to {2,3,4,5,6,7,8}. In particular, a point
of order six is retained; replacing the doubled normals by primitive
ones would incorrectly lose both this overlap and the order-two collisions.

If m divides n, the unique subgroup of Z/n killed by m is the image
of Z/m under u↦(n/m)u. This is injective, and applying it in both
coordinates identifies parameters of exact additive order m with the
coordinates (a,b) modulo m satisfying gcd(a,b,m)=1. A raw kernel
equation holds after embedding exactly when it holds modulo m.
Therefore the number r of collision kernels through such a point
depends only on its coordinates modulo m, not on n or other CRT factors.

For completeness the whole finite calculation of these overlap numbers
is given below. Each row is obtained by checking the displayed twelve
integer normals on the at most64 coordinates modulo m and retaining
gcd(a,b,m)=1. Entries `r: number` include every primitive coordinate,
not just a choice of projective representatives.

|m|Full histogram of r|Σ max(r−1,0)|
|---:|---|---:|
|2|6:3|15|
|3|3:8|16|
|4|1:6, 4:6|18|
|5|1:12, 3:12|24|
|6|1:12, 2:12|12|
|7|1:36, 3:12|24|
|8|1:36, 2:12|12|

The accompanying exact certificate lists every coordinate having r≥2
and all of its kernel indices, so the small table can be checked without
trusting a modulus-range search. Different exact additive orders are
disjoint. The origin belongs to all twelve kernels and contributes
overcount11. A nonzero point on r kernels contributes overcount r−1.
Subtracting these overcounts from the sum of kernel sizes gives the
size of their union; subtracting that union from n² gives the stated
formula. This proves the identity for every n, including n<6 where
the support domain is empty. ∎

## Independent arithmetic identity

Inclusion–exclusion on all4096 subsets of the twelve raw normals,
using their integer Smith factors, gives the independent expression

\[
\begin{split}
n^2-9n-3n g_2-12-6g_2+2g_3+6g_4+6g_5+6g_6+4g_7+3g_8+2g_2^2,
\end{split}
\]

where g_m=gcd(n,m). For a nonempty rank-one subset with Smith factor d,
its kernel has n·gcd(n,d) points. For rank two with factors d₁,d₂,
its kernel has gcd(n,d₁)gcd(n,d₂) points. The first factor is the entry
gcd; the product is the gcd of its2×2 minors. This check is separate
from the elementary exact-order calculation and agrees with it.

The new code retains both implementations. Actual point support sets
provide a third direct audit at every n=1..135; these are parameter
checks, not a new six-subset census. Immutable-reference interval counts
also verify homometry at every actual support parameter through48.
The general Smith-kernel formula/inclusion–exclusion is published prior
art (Kamiya–Takemura–Terao2008); the elementary overlap proof above
does not require their theorem as an unread axiom.

## Reproduction and proof boundary

```bash
.venv/bin/python tests/test_six_bloom_support.py
.venv/bin/python src/six_bloom_support.py --nmax 135 --out results/2026-10-01-six-bloom-support
```

Source: `src/six_bloom_support.py`; tests:
`tests/test_six_bloom_support.py`. Certificate/progress/verification logs
are under `results/2026-10-01-six-bloom-support/`.
Fresh attack: `notes/2026-10-01-six-primary-review.md` (pending).
Dividing |Ω_n| by twelve requires a separate classification of parameter
fibers and congruent endpoints. At n12, |Ω_12|=36, but there is only
one nontrivial Bloom pair. Hence unqualified division by twelve fails.
