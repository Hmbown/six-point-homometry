# Weighted strengths on rigid cyclic six-support pairs

1 October 2026. PQ3/PQ5, authorized standard-coordinate sparse
phase-retrieval extension. **[PROVED]** W21 in §2, its R5 local corollary,
and §4 passed the separate attack logged in
`notes/2026-10-01-weighted-six-review.md`. **[COMPUTED]** all thirteen
incidence certificates; the other twelve local conclusions in §3 remain
**[OPEN: review pending]**. **Historical priority is unestablished.**
These are prescribed-support results, rather than a classification of every
weighted competitor with at most six nonzero coordinates.

## 1. Model and exact scope

For a support S=(s0,...,s5) in Z_n and real strengths w, write

    q_S(w)_0 = sum_i w_i^2,
    q_S(w)_d = sum_{i<j, min(|s_i-s_j|,n-|s_i-s_j|)=d} w_i w_j.

The full directed autocorrelation C_S(w)[d]=sum_t x[t]x[t+d] equals q_d
at every nonzero non-antipodal class, and equals 2q_d at the antipodal
class. Its zero entry is q_0. Consequently q equality is exactly equality
of the squared discrete Fourier magnitudes, for any consistent fixed
Fourier normalization. The tests reconstruct C on all n grid coordinates;
they do not merely repeat the folded-edge implementation.

The main benchmark has

    n=21,
    A=(0,1,3,7,10,15), B=(0,1,4,7,14,16).

Both are six-support signals on the ordinary cyclic grid. Their support
relation is the purely cyclic R5 example of the earlier program. The proof
below uses its actual cyclic equations; it does not invoke collision-free
integer-line weighted uniqueness.

## 2. Global fixed-support classification at the 21-point benchmark

**[PROVED] Statement W21, in-house, independently attacked.** Suppose each
of the six A strengths is nonzero and real, and a
real competitor is supported on a subset of B. Then equal autocorrelation
holds if and only if, for some nonzero real u, one of the following occurs:

1. a=u(1,1,1,1,1,1), b=epsilon*u(1,1,1,1,1,1);
2. a=u(r,1,r,1,1,r),
   b=epsilon*u*sqrt(-r)(-1,1,1,2,-1,1), where
   r=(-3+sqrt(5))/2 or r=(-3-sqrt(5))/2.

Here epsilon independently belongs to {+1,-1}. All resulting B strengths
are nonzero. If both signals have positive strengths, only case 1 with
epsilon=+1 survives. Thus the positive fixed-support incidence consists
exactly of the equal-strength ray, globally rather than just near that ray.
The two signed types are isolated projective alternatives involving the
golden-ratio square and its reciprocal.

### Full proof of W21

Label a,b in the stated sorted support orders. The eleven equations are
the equality of the following two columns:

| d | q_A(a) | q_B(b) |
|---:|---|---|
|0|a0²+a1²+a2²+a3²+a4²+a5²|b0²+b1²+b2²+b3²+b4²+b5²|
|1|a0 a1|b0 b1|
|2|a1 a2|b4 b5|
|3|a0 a2+a3 a4|b1 b2+b2 b3|
|4|a2 a3|b0 b2|
|5|a4 a5|b0 b5|
|6|a0 a5+a1 a3|b1 b3+b1 b5|
|7|a0 a3+a1 a5+a2 a4|b0 b3+b0 b4+b3 b4|
|8|a3 a5|b1 b4|
|9|a1 a4+a2 a5|b2 b5+b3 b5|
|10|a0 a4|b2 b4|

The six singleton rows d=1,2,4,5,8,10 force b0,b1,b2,b4,b5 to be
nonzero. No division by b3 is needed. The first five named nonzero weights
give

    b1=a0 a1/b0, b2=a2 a3/b0, b5=a4 a5/b0,
    b4=a1 a2 b0/(a4 a5).

The two remaining singleton constraints imply

    a0 a1² a2 = a3 a4 a5²,
    a1 a2² a3 = a0 a4² a5.

Set p=a0/a3, q=a1/a5, h=a2/a4. These are nonzero real numbers. The last
two equalities become p q² h=1 and q h²/p=1. Multiplication gives
(qh)³=1. Over the real numbers qh=1, and then p=h. Put r=h and
x=a3, y=a4, z=a1. We therefore have

    a=(r x,z,r y,x,y,r z),
    b=(s,r xz/s,r xy/s,t,s,r yz/s), s=b0, t=b3.

The doubled rows d=3,6,9, after division by the respective nonzero
products xy,xz,yz, say

    r²+1 = r² xz/s² + rt/s
          = r² yz/s² + rt/s
          = r² xy/s² + rt/s.

The first two imply x=y; the first and third imply z=y. Thus
x=y=z=u !=0. Divide both signals by u and rename their B parameters s,t.
The equations now have

    a=(r,1,r,1,1,r), b=(s,k,k,t,s,k), sk=r,
    r²+1=k²+kt,             3r=s²+2st,
    3(r²+1)=2s²+3k²+t².                       (1)

Because r and s are nonzero, k is nonzero. Substitute s=r/k and
t=(r²+1-k²)/k into the second equation of (1). Dividing by r gives

    k²=(2r²+r+2)/5, kt=(3r²-r+3)/5.

The right-hand side for k² is strictly positive for every real r: the
quadratic 2r²+r+2 has negative discriminant. Substitution into the norm
equation gives the exact rational identity

    3(r²+1)-(2r²/k²+3k²+t²)
      = 9(r-1)²(r²+3r+1) / [5(2r²+r+2)].       (2)

The denominator never vanishes on the real line. Hence r=1 or
r=(-3±sqrt(5))/2. For r=1 we obtain k=±1, s=k, t=k. For either other
root r²+3r+1=0 gives k²=-r, s=-k and t=2k. This yields exactly the listed
branches. Conversely direct substitution verifies every row of the table;
the independent tests check all 21 directed autocorrelation entries with
exact radicals. Restoring u proves completeness. Positivity requires u>0
and r>0, leaving only r=1 and epsilon=+1. QED; separate attack accepted
the complete stated real scope.

The real assumption matters: (qh)³=1 has two more roots over C. The
theorem does not classify complex strengths. Likewise, allowing zeros on
A creates additional lower-support cases outside its hypothesis.

## 3. Local incidence on all thirteen rigid cyclic templates

The following **candidate local statement** describes the real solution
set near (a,b)=(1,1), with a,b in the prescribed support order. It includes
positive strengths by taking a sufficiently small neighborhood. Fix common
scale with sum_i(a_i+b_i)=12. This is legitimate near (1,1): the sum is
nonzero, and the autocorrelation equations are homogeneous of degree two.

| Seed | n | rank J_A | rank J_B | rank [J_A,-J_B] | tangent dimension after fixing scale | real local incidence after fixing scale |
|---|---:|---:|---:|---:|---:|---|
|R1|17|3|6|8|3|isolated|
|R2|19|6|6|9|2|two analytic curves with distinct tangent lines|
|R3|21|6|5|10|1|isolated|
|R4|21|6|6|10|1|isolated|
|R5|21|5|6|10|1|isolated|
|R6|23|6|6|10|1|isolated|
|R7|24|6|6|10|1|one exact affine line|
|R8|27|6|6|11|0|isolated|
|R9|27|6|6|11|0|isolated|
|R10|28|6|6|11|0|isolated|
|R11|30|6|6|11|0|isolated|
|R12|30|6|6|11|0|isolated|
|R13|31|6|6|11|0|isolated|

The support coordinates are recorded in the certificates and copied from
`notes/2026-09-30-six-templates.md`. These exact rank numbers are
**[COMPUTED]** by SymPy and independently checked with rational Gaussian
elimination, explicit nonzero minors and directed-correlation polarization.
The R5 local conclusion is **[PROVED]** directly from W21; the other
twelve mathematical local conclusions remain pending separate proof review.

### Full candidate local proof

Write z=(a,b), e=(1,...,1), F(z)=q_A(a)-q_B(b), J=DF(e). Let E be the
eleven-dimensional real hyperplane sum z=0 for increments about e. Its
kernel T=ker(J|E) is saved as the columns of N. Choose a linear complement
W of T in E, and choose rank(J|E) independent output rows, denoted F_I.
The derivative of F_I(e+Nt+w) in w in W is invertible. By the real
analytic implicit function theorem there is a unique real analytic
w=w(t), with w(0)=0 and Dw(0)=0, that solves F_I=0 nearby. Thus w(t)=O(||t||²).
Every nearby solution of all equations is of this form.

For any ell in ker(J^T), homogeneity and F(e)=0 give exactly

    ell·F(e+h) = ell·F(h).

The right side is a quadratic form. On h=Nt+w(t), its leading term is
t^T H_ell t, where H_ell is the saved projected quadratic obstruction;
the error is O(||t||³). Any definite H_ell therefore excludes all small
nonzero t. If T is zero the implicit function theorem itself gives
isolation. This proves the listed isolated cases using the following
exact obstruction matrices in the saved rational tangent bases:

    R1: -6 I_3, R3: [18], R4: [-54/25],
    R5: [-18], R6: [135/8].

The remaining R8–R13 have T=0. Zero measurement rows contribute no
constraint and are retained explicitly in the certificates.

For R2 all ten measurement rows are active and J has rank nine. There is
exactly one residual equation after solving the nine selected equations.
The left kernel is spanned by ell=(-5/2,1,...,1); every entry is nonzero,
so ell·F=0 is equivalent to the one unselected equation after F_I=0.
In the saved two-dimensional tangent coordinates the quadratic form is

    H = (1/150) [[641,91],[91,-859]], det H=-621/25<0.

Let g(t1,t2)=ell·F(e+N(t1,t2)+w(t1,t2)). Then
g=(641t1²+182t1t2-859t2²)/150+O(||t||³).
Its two null lines are t2=c_± t1 with

    c_±=(91±30 sqrt(621))/859.

Both have nonzero t1 component. In a small punctured neighborhood, every
zero direction of g must lie near one of these lines: otherwise its
quadratic leading term has a uniform nonzero bound on the compact unit
circle. The function g(t,t*c)/t² extends real analytically to t=0;
at each c_± its c derivative is nonzero. The implicit function theorem
therefore supplies exactly two real analytic functions c_±(t) and hence
two local zero curves (t,t*c_±(t)). There can be no further zero curves,
by the directional bound and the local uniqueness at each root. Their
distinct tangent lines make them transverse within the two-dimensional
implicit chart. Lifting with w(t) gives precisely the stated two curves
in the normalized twelve-amplitude incidence. They contain nonconstant
positive-strength solutions for sufficiently small real parameter t.

For R7 the saved one-dimensional normalized tangent is v=(v_A,v_B),

    v_A=(1,-1,1,-1,-1,1),
    v_B=(-1,1,-1,-1,1,1).

Direct coefficient comparison gives F(e)=0, Jv=0 and F(v)=0. Since F is
quadratic, F(e+t v)=0 for every real t. Also sum v=0. The ten selected
implicit equations have exactly one free coordinate, and their locally
unique solution chart is exhausted by this line. Therefore all nearby
solutions of the entire system are exactly e+t v. Before normalization,
the local solution set is the plane c e+t v. Positivity holds when c>|t|.
QED pending fresh review.

Faithful subgroup inflation, simultaneous multiplication by a cyclic
unit, and rigid motion of either support transport these conclusions:
they permute or insert zero autocorrelation rows and relabel amplitude
coordinates. Proper non-faithful images can merge distance rows and
change the incidence, so the result is not asserted for those images.

## 4. A same-support positive ambiguity and an actual stability obstruction

**[PROVED] Consequence, separately attacked.**
For the benchmark A let v=(1,-1,1,-1,-1,1). For every real t,

    q_A(1+t v)=q_A(1-t v).

Indeed J_A v=0 and q is quadratic, so the two signs have identical
expansions. For 0<|t|<1 both strengths are positive. The only cyclic
translation/reflection preserving A is the identity (the tests examine
all 42 possibilities), so these signals are inequivalent under cyclic
shift, reflection and global sign.

Unit-normalized signals

    x_±(t)=(1_A ± t v_A)/sqrt(6(1+t²))

remain inequivalent, positive, and exactly equal in Fourier magnitudes.
Thus no neighborhood of the equal-strength A signal is injective on the
positive six-sparse class, even restricting competitors to A itself. No
strictly positive lower Lipschitz bound on that neighborhood is possible,
under either the squared-power or Fourier-magnitude measurement metric.
This is a special one-parameter amplitude locus; it does not refute a
generic-amplitude uniqueness statement.

The equal-strength A polynomial P_A(X)=1+X+X³+X⁷+X¹⁰+X¹⁵ has no
Fourier zero on the 21-point grid. The independently checked integer
Bezout identity saved in `benchmark_fourier_bezout` is

    U(X) P_A(X)+V(X)(X²¹-1)=12.

Thus its criticality is not explained by a vanished Fourier coordinate.
The separate reviewer proved a stronger uniform nonvanishing statement.
Writing z for a 21st root and w=z^3, the signal polynomial factors as

    P_t(z)=(1+z^3+z^15)((1+t)+(1-t)z^7).

The first factor is 1+w+w^5 with w^7=1: it equals 3 at w=1 and cannot
vanish at a primitive seventh root, whose minimal polynomial has degree6.
The second factor is nonzero for every real t: z^7 is a cube root, its
only real value is 1, and the value at 1 is 2. The endpoint cases t=+/-1
are also nonzero. Thus every real member of this line has no Fourier zero.
Along one chosen sign of x(t), the signal's change from x(0) has order |t|
and the squared-power change has order t², because J_A v=0. Since all
Fourier coordinates at x(0) are nonzero, taking positive square roots
is a local smooth invertible coordinate change; the magnitude change
also has order t². Even if one selects only one of the two indistinguishable
branches, a Lipschitz inverse cannot extend to x(0). A sharp bound on
regions separated from critical and ambiguity loci remains additional
work, rather than a consequence of this obstruction calculation.

## 5. What this does and does not advance

The benchmark global result answers whether its actual purely cyclic
binary pair persists under arbitrary strengths on those same supports.
The local table also distinguishes a definite second-order obstruction,
an indefinite persistent intersection, an exactly persistent family,
and a nonsingular isolated intersection. A Jacobian rank calculation
alone would miss the first three distinctions.

Neither binary support homometry nor its complete six-note grammar
classifies all weighted competitors. A weighted competitor can use a
support whose unweighted interval multiplicities differ, and signed
strengths can cancel autocorrelation rows. This note has not enumerated
those supports and does not establish generic recovery among all supports
of size at most six. It does not resolve the standard-coordinate
crystallographic phase-retrieval conjectures or the frontier stability
problem. No claim of novelty is made.

## 6. Verification, failures and reproduction

Parent session reference controls were already green before this delegated
task. The new build takes approximately 0.2 seconds and the independent
tests approximately 0.5 seconds on the pinned environment. They cover:

- the immutable reference ICV/T-I controls for all 13 pairs;
- 208 signed rational weighted correlations against full directed sums;
- every saved Jacobian, rank, nonzero minor, tangent and quadratic form;
- all three exact real projective benchmark types and the norm eliminant;
- R7's exact family and R5's positive same-support ambiguity;
- the integer Fourier Bezout identity.

The first test run used a mistaken hand-written expected R2 determinant
(-570781/22500). The saved matrix and independent rational calculation
both give -621/25; the assertion was corrected. No scope or data was
altered. An exploratory Hessian print initially used the matrix-only
`jacobian` method on a scalar expression; it was corrected to `hessian`.
These are development errors, not failed mathematical approaches.

```bash
.venv/bin/python src/weighted_six_incidence.py --out results/2026-10-01-weighted-six-incidence
.venv/bin/python tests/test_weighted_six_incidence.py
```

The certificate and summary are in that output directory. This note, its
source and tests are new files. Protected references, data, shared ledgers
and the open LaTeX editor were preserved. No commit was made by this
delegated worker. The separate review accepts only W21, its R5 local
corollary and §4. It rebuilt the full directed equations without importing
the author implementation/certificates, derived the eliminant independently,
checked all signed branches and eliminated the initially allowed B-zero
cases. Eleven exact audit checks and four independent test groups passed:

```bash
.venv/bin/python src/weighted_six_review.py
.venv/bin/python tests/test_weighted_six_review.py
```

Other template-local proofs remain pending. Internal acceptance does not
establish historical priority or external peer review.
