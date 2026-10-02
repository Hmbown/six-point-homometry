# Periodic supports: exact convolution symmetries and a generic fiber theorem

1 October 2026. **[PROVED]**, in-house, independently attacked: U, F, C,
H and S below. The separate attack is logged in
`notes/2026-10-01-weighted-subgroup-review.md`, including a frozen copy and
digest of the accepted draft. The spectral-unit construction itself is
classical. This note makes no historical-priority or external-review claim.

## Definitions and scope

Let G=Z/N, N>=1. A real signal x has coordinates x_i, i in G. For a
nonempty support set S, E_S is the real coordinate space of signals zero
outside S; its elements may also vanish at some coordinates of S. Write

    c_x(d)=sum_i x_i x_(i+d),
    (u*x)_i=sum_j u_j x_(i-j),
    X(k)=sum_i x_i exp(-2 pi i k i/N).

Then the Fourier transform of c_x is |X(k)|^2. Folded distance classes include
zero, with d and -d identified. The intrinsic real symmetry group is global
sign times translation/reflection. It is finite. A support may be periodic
even when its unequal weighted signals are not periodic.

We first classify convolution operators that preserve an entire coordinate
space. We then give an exact generic same-support fiber theorem for a family
of supports. Neither theorem classifies all competitors on different supports,
all fixed linear operators, or all nonlinear ambiguities for arbitrary S.

## Theorem U: universal support-preserving convolution

Put H_S={h in G:S+h=S}, of order m. This is a subgroup.

1. A real cyclic convolution C_u sends E_S into E_S if and only if
   supp(u) is contained in H_S.
2. Such a convolution preserves c_x for every x in E_S if and only if its
   Fourier coefficients all have modulus one. Thus these operators form the
   real spectral-unit group of H_S, isomorphic to

       {+1,-1}^epsilon x (S^1)^floor((m-1)/2),

   where epsilon=1 for m odd and epsilon=2 for m even.
3. On a Zariski-open dense set in E_S, the action is free. Its identity
   component gives a smooth constant-autocorrelation orbit of dimension
   floor((m-1)/2). For strictly positive strengths on S, a neighborhood of the
   identity orbit stays strictly positive with exactly the same support.

### Proof of U

The subgroup assertion follows from closure under addition and negation of
support periods. Suppose C_u preserves E_S. For every s in S apply it to
delta_s. Every t in supp(u) must obey s+t in S; hence S+t is contained in S,
and equality follows from equal finite cardinality. Thus t in H_S.
Conversely every translate by a point of H_S preserves S, so any linear
combination of these translates preserves E_S. No cancellation assumption
is needed: testing individual coordinate basis vectors excludes cancellation.

If C_u preserves autocorrelation, testing delta_s gives c_u=delta_0, or
equivalently |U(k)|=1 for every ambient character k. This condition also
suffices for every signal, since the Fourier transform of u*x is U(k)X(k).
Characters of G restrict onto all characters of H_S. A kernel supported on
H_S has ambient transform given by its transform on H_S evaluated at these
restrictions. The condition is exactly that each subgroup Fourier coefficient
has modulus one. Reality requires conjugate character values to be conjugate.
There is one real character when m is odd and two when m is even; their
values are +/-1. All other characters occur in conjugate pairs with arbitrary
unit phases. This proves the stated group description.

For generic x, all its ambient Fourier coefficients are nonzero. Indeed
each |X(k)|^2 is a nonzero real polynomial on E_S (evaluate at delta_s),
and the finite product of these polynomials is nonzero. On this Zariski-open
set, C_u x=x implies U(k)=1 at every k and thus u=delta_0. The group action
is free. Its compact torus identity component therefore has the indicated
orbit dimension. Convolution is continuous, it leaves all outside coordinates
zero, and strict positivity on finitely many inside coordinates is open.
This proves the positivity assertion. QED.

For m<=2 this convolution group consists only of signed subgroup
translations. This observation is not a sufficient recovery criterion for
arbitrary aperiodic supports; it only removes this particular universal
convolution obstruction.

## Theorem F: the entire generic fixed-support fiber of a quotient lift

Let N=q m, with q,m positive integers, H=q Z/(q m), and let Q be a subset
of Z/q with r>=3 points. Assume that **all ordered nonzero differences**

    a-b (mod q), (a,b) in Q^2, a!=b,

are distinct. Set S=Q+H using any fixed quotient representatives.
Then H_S=H and |S|=r m. Let U be the Zariski-open dense subset of E_S
where every subgroup Fourier coefficient of every coset block is nonzero.

For each real x in U, the complete real fiber inside E_S is exactly

    {y in E_S:c_y=c_x}={u*x:u is a real spectral unit supported on H}.

The action is free, and this fiber is a disjoint union of 2^epsilon tori
of dimension d=floor((m-1)/2). The autocorrelation Jacobian on E_S has
rank **r m-d** at every x in U. Its positive part near a positive x has
dimension d. No claim about competitors on other coordinate supports is made.

### Proof of F: recovering the coset pair products

Write x_(a+qj)=x_a(j), j in Z/m, for a in Q, and define

    X_a(l)=sum_j x_a(j) exp(-2 pi i l j/m),  l in Z/m.

For k=l+t m, 0<=l<m and 0<=t<q, the ambient transform is

    X(l+t m)=sum_(a in Q) A_a(l) exp(-2 pi i t a/q),
    A_a(l)=exp(-2 pi i l a/(q m)) X_a(l).

Fix l. Taking the inverse q-point Fourier transform in t of the q powers
|X(l+t m)|^2 recovers, at difference a-b, the product
A_a(l) conjugate(A_b(l)). The ordered-difference hypothesis ensures that
this is one product, with no other term sharing its nonzero difference.
The zero difference recovers the sum of squared magnitudes.

Suppose y in E_S has the same autocorrelation. Its block coefficients
B_a(l) therefore have exactly the same nonzero pair products. They are
nonzero because all A_a(l) are nonzero and there are at least three points.
Let z_a=B_a/A_a at this frequency. For every distinct a,b,

    z_a conjugate(z_b)=1.

For three distinct a,b,c, comparison of the equations for (a,b) and (a,c)
gives z_b=z_c; the equation for (b,c) then gives |z_b|=1, and the equation
for (a,b) gives z_a=z_b. Thus every ratio equals one common phase lambda_l.
This applies to every l. The diagonal sum imposes no further condition.
The twisting factors cancel in these ratios, so

    Y_a(l)=lambda_l X_a(l), for every a in Q.

Reality of x and y gives lambda_(-l)=conjugate(lambda_l), with +/-1 at
self-conjugate subgroup frequencies. Inverting the m-point transform yields
a real subgroup kernel whose transform is lambda_l. Embedded on H, it is
a spectral unit and sends x to y. Conversely such a kernel preserves E_S
and autocorrelation by U. Nonzero block coefficients imply the action is
free, so the asserted group and connected-component description follows.

The genericity set is defined by a finite product of nonzero real
polynomials |X_a(l)|^2. Each polynomial is nonzero by testing a single
coordinate in its own coset. Their product is nonzero in the real polynomial
ring. Thus U is Zariski-open dense, and meets the strictly positive orthant
in a relatively open dense set.

Finally a period of S induces a period of Q. A nonzero quotient period t
would give at least r distinct ordered pairs (a+t,a) of difference t,
contradicting the ordered-difference hypothesis. Thus H_S=H. QED for the
set-theoretic fiber assertions.

### Proof of the exact Jacobian rank

Let h be a real infinitesimal perturbation in E_S for which the derivative
of autocorrelation vanishes. The same inverse q-point transform gives,
at every l and every distinct a,b,

    dA_a conjugate(A_b)+A_a conjugate(dA_b)=0.

Divide by the nonzero product and put rho_a=dA_a/A_a. Then
rho_a+conjugate(rho_b)=0 for all distinct a,b. With r>=3, comparing three
equations forces all real parts to be zero and all imaginary parts equal.
Thus dX_a(l)=i theta_l X_a(l), with one real theta_l common to all cosets.
Reality gives theta_(-l)=-theta_l; at self-conjugate frequencies theta_l=0.
There are exactly d=floor((m-1)/2) free real parameters. Conversely every
such perturbation is tangent to the subgroup spectral-unit orbit and has
zero derivative. Hence the kernel dimension is d and the rank is r m-d.
The full autocorrelation, folded autocorrelation and full Fourier powers
have the same differential kernel by the invertible real Fourier transform
on even real sequences. QED.

## Corollary C: a difference-rich generic obstruction

For the supports in F the number of folded distance classes, including zero,
is

    D=m r(r-1)/2+floor(m/2)+1.

Indeed every nonzero ordered quotient difference contributes an entire
coset of H to S-S, as does zero, so the raw difference set has
m(1+r(r-1)) elements. Inversion fixes 0 and, exactly when m is even,
the element N/2. A nonzero self-inverse quotient difference is impossible:
it would repeat the ordered differences of (a,b) and (b,a). These facts
give the formula. For r>=3, D>r m. Also q>=r(r-1)+1 by the distinct
ordered-difference assumption, so r m<N/2. For m>=3 the generic fiber
has positive dimension despite this strict sparsity and difference surplus.

In particular Q={0,1,3} satisfies the ordered-difference assumption for
**every q>=7**, with six differences +/-1,+/-2,+/-3. For every m>=3,

    N=q m, K=3m, D=floor(7m/2)+1>K,
    generic fiber dimension=floor((m-1)/2).

For q=7 the full raw difference set is G. Taking q arbitrarily large
makes density K/N=3/q arbitrarily small; taking m large makes the
ambiguity dimension arbitrarily large. These are weighted results with
K>=9, not a new binary six-note construction. Binary indicators of these
coset unions are fixed by the identity component (their nonzero subgroup
frequencies vanish), and are outside U.

## Exact positive rational witness in Z/21

Take S=(0,1,3,7,8,10,14,15,17), with respective strengths 10,11,...,18.
The classical rational order-three kernel, embedded at (0,7,14), is

    u_t=((1-t^2), 2t(t-1), 2t(t+1))/(1+3t^2).

Its entries sum to one, its squared norm is one and its off-zero cyclic
autocorrelation is zero. Expanding the numerators proves these identities
over Q[t]. Thus c_(u_t*x)=c_x for every t. At t=1/10 the entries are
(99,-18,22)/103. Every inside strength of y=u_t*x is positive, every
outside strength is zero, and at least one strength is nonintegral. Since
x has only integer coordinates, y is neither a sign, translation nor
reflection of x. This is an exact same-cardinality counterexample.

The source-generated certificate contains every coordinate, autocorrelation,
the minimum squared distance over all 84 intrinsic images, a polynomial-gcd
check that all ambient Fourier coefficients are nonzero, and the exact
11-by-9 Jacobian rank 8. The independent auditor uses a different x and
t=1/6, exact direct autocorrelation, and independent ambient DFT controls.
The derivative u'_0=2(delta_14-delta_7) gives a nonzero kernel direction
for generic x, so the ambiguity persists arbitrarily close to x.

## Theorem H: aperiodic punctured supports also have generic continuous fibers

Let q>=7, m>=5, N=q m, Q={0,1,3}, H=q Z/N. Delete the point 0 from
S0=Q+H and set S=S0 minus {0}. Then

    |S|=3m-1<N/2, H_S={0},
    |(S-S)/sign|=floor(7m/2)+1>|S|.

On a Zariski-open dense subset of E_S, the local same-support fiber has
dimension **floor((m-1)/2)-1**, and its autocorrelation Jacobian has rank
**3m-floor((m-1)/2)**. The subset meets the positive exact-support orthant
in an open dense set, and every such positive point has arbitrarily close
nonintrinsic positive partners with the same support and powers. In
particular, excluding periodic supports does not repair generic uniqueness.

### Proof of H

Every quotient coset in Q still has a point. A support period projects to
a period of Q, which is trivial by the ordered-difference argument in F.
Thus H_S is contained in H. Its order divides both m and |S|=3m-1, so
it is one. The zero quotient difference still fills all H using either
unchanged coset. For a nonzero quotient difference, its unique ordered
pair of cosets is either unchanged or involves one nonempty punctured
coset and one full coset. Subtracting a full H-coset from any one point
of the other fills the entire difference H-coset. Therefore S-S=S0-S0
and the asserted difference count follows from C.

Let U0 be F's generic subset for S0, and restrict it to E_S. Its block
nonvanishing polynomials remain nonzero: a one-coordinate test is still
possible inside each coset, including the punctured coset. The restriction
is therefore Zariski-open dense. On it, F identifies the complete fiber
inside E_S0 with the free d-dimensional subgroup-unit orbit, d=floor((m-1)/2).
The fiber inside E_S is exactly the part of that orbit satisfying the
single additional equation y_0=0.

Use the skew-circulant subgroup generator L=P-P^T, where P shifts one
step in H, in a Cayley path C_t=(I+tL)(I-tL)^(-1). Its derivative is 2L,
so the derivative of y_0 at the identity is

    2(x_(-q)-x_q).

This is a nonzero real linear form on E_S (q and -q are distinct for
m>=5). Require it to be nonzero as an additional Zariski-open condition.
The real implicit function theorem on the unit torus then makes y_0=0
a smooth local hypersurface of dimension d-1. The action is free, so
the signal fiber has that same dimension. Intersecting the exact tangent
kernel from F with the one constraint h_0=0 removes one dimension, which
gives the asserted exact Jacobian rank on E_S.

At a positive exact-support point, the surviving coordinates stay positive
in a sufficiently small neighborhood, while the omitted coordinate is
exactly zero. Since d-1>=1, this neighborhood contains a nonconstant
smooth family. A finite intrinsic orbit cannot contain it; near the point
its nonconstant partners can be chosen outside that finite orbit.
All polynomial/linear nonvanishing conditions meet the positive orthant
dense openly, which proves the generic positive assertion. QED.

These ambiguities use kernels supported in H_S0, not H_S. Their parameters
are restricted by a signal-dependent zero equation. Thus they are fully
consistent with U's classification of universal fixed convolution operators
on E_S. They expose an obstruction beyond a support's own period subgroup.

### An exact algebraic positive aperiodic witness in Z/35

Use coset blocks

    r=0: (0,2,3,5,7), r=1: (11,13,17,19,23),
    r=3: (29,31,37,41,43), positions r+7j, 0<=j<5.

Let L1=P-P^T, L2=P^2-(P^2)^T, A=tL1+vL2 and
C=(I+A)(I-A)^(-1), applied to every coset block. This is a real
orthogonal circulant matrix: A is skew-symmetric and I-A is invertible
for all real parameters. It preserves every Fourier magnitude. Set
v=1/1000. The omitted coordinate is zero exactly when t satisfies

    17000000000000 t^4 + 7966000000000 t^3
      + 7982983000000 t^2 + 4998001034000 t + 2009009017 = 0.

Choose the unique root in (-6/14917,-5/12431); exact rational root
isolation verifies uniqueness and |t|<1/1000. This polynomial, interval
and rational matrix expression specify y=Cx exactly, without decimal
approximation. The numerator's identity gradient is (10,4), giving the
curve tangent t'(0)=-2/5.

For a skew matrix, ||(I-A)^(-1)||<=1, since
||(I-A)z||^2=||z||^2+||Az||^2. Also ||Lj||<=2, so
||C-I||<=2||A||<=4(|t|+|v|)<8/1000. Here ||x||^2=8257,
giving ||y-x||^2<(8/1000)^2*8257<1. Every surviving x coordinate is
at least 2, hence every surviving y coordinate is positive. The hole is
exactly zero by the quartic, and outside S0 stays zero by convolution.
Each block polynomial is coprime to z^5-1, verified exactly, so the
subgroup action at x is free. Because L1,L2 are independent and v!=0,
C is not the identity and y!=x. The smallest squared distance from x to
any nonidentity intrinsic image is 502, checked over all 139 other
sign/shift/reflection elements. With ||y-x||<1, y cannot equal one of
those images either. Thus this is an exact positive aperiodic counterexample.

The certificate also gives H_S={0}, all 18 folded distances, the
18-by-14 Jacobian rank 13, and an exact nonzero kernel tangent. This
finite witness supports H; its arbitrary-parameter proof is the argument
above, not an extrapolation from ranks.

## Consequences and literature boundaries

### Theorem S: explicit reconstruction and stability on the necessary quotient

Retain F's hypotheses. The inverse q-point transform reconstructs every
block pair product P_ab(l)=X_a(l) conjugate(X_b(l)), after removing the
known representative-dependent phase. For any three distinct cosets a,b,c,

    |X_a(l)|^2=|P_ab(l)| |P_ac(l)| / |P_bc(l)|.

Use one fixed anchor coset a at every frequency. Choosing its untwisted
X_a(l) positive real then reconstructs each other block coefficient
as conjugate(P_ab(l))/|X_a(l)|. These choices are conjugate at l and -l,
and real at self-conjugate frequencies, so they give a real signal in the
same subgroup-unit orbit. This explicitly recovers the full fiber class
from the powers, rather than merely asserting existence of a unit.

For a quantitative statement suppose x,y are two real signals in U, and
every block Fourier magnitude of each signal lies in [delta,M], delta>0.
Let p_x=|X|^2 denote the unnormalized ambient Fourier powers. Let d_H(x,y)
be the minimum Euclidean distance between their orbits under the full real
subgroup-unit group. Define

    L0=(2M^2/delta^2+M^4/delta^4)/(2delta),
    L1=1/delta+M^2 L0/delta^2, L=max(L0,L1).

Then

    d_H(x,y) <= sqrt(r/N) L ||p_x-p_y||_2.

If also ||x||_2,||y||_2<=R, the reverse estimate is

    ||p_x-p_y||_2 <= 2 N R d_H(x,y).

These explicit nonoptimal bounds establish bi-Lipschitz recovery on
bounded subsets away from vanishing block coefficients, **modulo the enlarged
subgroup-unit group**. They do not establish recovery modulo the original
finite intrinsic group; that recovery is false here. Reconstruction assumes
a known support and consistent powers, not an unknown-support or noisy-data
algorithm. No priority claim is made for this stability argument.

### Proof of S

The reconstruction formula follows from the three pair products; all
denominators are nonzero. Let

    e_l=(q^(-1) sum_(t=0)^(q-1)
         |p_x(l+t m)-p_y(l+t m)|^2)^(1/2).

The inverse q-point transform and Cauchy--Schwarz bound the error in every
recovered pair product at this l by e_l. The known phase factors have
modulus one and do not change this bound.

For A=|P_ab|, B=|P_ac|, C=|P_bc| (and primed quantities for y), all six
numbers are between delta^2 and M^2 and each paired difference is at most
e_l. Splitting AB/C-A'B'/C' into three terms gives

    |AB/C-A'B'/C'|
       <= (2M^2/delta^2+M^4/delta^4) e_l.

Taking square roots divides this bound by at least 2delta. Hence the
positive-anchor magnitudes differ by at most L0 e_l. For every other
coordinate, divide its pair product by the anchor. Its error is at most

    e_l/delta + M^2 (L0 e_l)/delta^2 = L1 e_l.

The two canonical-gauge block vectors therefore differ by at most
sqrt(r) L e_l in Euclidean norm at frequency l. Each canonical gauge
is attained by one real subgroup unit, because the untwisted block
transforms of real signals have conjugate frequencies, and their anchor
phases obey that same conjugation rule. Parseval for the unnormalized
m-point transforms now yields

    d_H(x,y)^2 <= (r L^2/m) sum_l e_l^2
               = (r L^2/(m q)) ||p_x-p_y||_2^2.

For the upper estimate, choose orbit representatives achieving d_H; the
group is compact and orthogonal so a minimum exists and their norms stay
bounded by R. Pointwise
||X|^2-|Y|^2|<= (|X|+|Y|)|X-Y|. Each Fourier coordinate is bounded by
sqrt(N) R, and Fourier Parseval gives ||X-Y||_2=sqrt(N)||x-y||_2.
The upper estimate follows. QED.

For positive x in U, no local inverse of autocorrelation modulo the usual
finite intrinsic group exists: arbitrarily close nonintrinsic signals have
identical data. In particular no positive lower Lipschitz or Holder recovery
bound in the intrinsic quotient can hold in such a neighborhood. This is
a negative statement about recovery on the full class, not a denial of
stability on a chosen transverse slice or modulo the enlarged unit group.

**[PROVED: in-house, independently attacked, version-specific]** C and H
contradict the literal
generic uniqueness assertions of Conjectures 4.7 and 4.11 in
*Bendory--Edidin, arXiv:2002.10081v2*: their hypotheses use D>K and
genericity in each fixed support, without excluding support periods.
It does not by itself contradict distinct-support Conjecture 4.8,
a measure-zero assertion in a larger phase torus, or a generic-basis theorem.
The journal full-text wording has not been independently compared.

**[PROVED-LIT]** Real spectral-unit circles are described explicitly by
Mandereau et al., JMM 5(2) (2011), pp.6--7; positive order-three ambiguity
and subgroup embeddings are proved by Il'inskaya, Mat.Stud.46(1) (2016),
pp.91--93. These are classical antecedents, freshly read in the literature
audit. The coset pair-product argument above classifies the complete
same-support fiber under its stated quotient-difference condition. No
claim that this application or theorem was previously unknown is made.
Primary reading, exact conjecture formulation and venue/access gaps:
`notes/2026-10-01-weighted-phase-literature.md`.

The next obstruction is to characterize the **structured supersupports**
whose unit orbits survive zero constraints, and then distinguish them from
supports admitting generic recovery. H_S={0} alone is insufficient, by H.
Competing-support recovery is also outside F/H, and a general exact-support
classification or intrinsic stability theorem remains open here. A human
phase-retrieval specialist should check this conjecture
comparison and the antecedents before any public claim.

## Reproduction and review record

Python3.12.12, NumPy2.5.3, SymPy1.14.0; Lean/lake not installed. No pinned
reference file, data artifact or open LaTeX source was edited. Cayley-kernel
benchmark m=12: approximately0.0016s; complete60 exact family controls:0.53s.

    .venv/bin/python src/weighted_subgroup.py
    .venv/bin/python tests/test_weighted_subgroup.py
    .venv/bin/python src/weighted_subgroup_review.py
    .venv/bin/python tests/test_weighted_subgroup_review.py

Root certificate: `results/2026-10-01-weighted-subgroup/certificate.json`.
Separate attack: `notes/2026-10-01-weighted-subgroup-review.md` and its
independently generated results. The written U/F/C/H/S proofs were accepted
after independent derivations, including exact Z/21 and algebraic Z/35
certificates,18 punctured-support ranks and21 stability controls using a
different fixed anchor. The reviewer previously worked on the binary
project, then independently reconstructed this weighted proof; this is a
separate context re-read, not a claim of external human review. All7 author
and8 independent regression groups passed. Root construction build including
the puncture certificate took0.86s; the first m=12 benchmark was0.0016s.
