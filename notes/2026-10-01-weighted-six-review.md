# Independent adversarial review of weighted six-support results

1 October 2026. Separate review of
`notes/2026-10-01-weighted-six-incidence.md`, principally §§2 and 4.
This is an in-house independent attack, not external peer review or a
historical-priority assessment. The reviewer previously audited relevant
literature but did not develop the author's six-support elimination.
A further separate-context subagent independently attacked §4.

## Verdict and review boundary

**[PROVED: in-house, independently attacked]** No substantive defect was
found in W21, the global real classification for nonzero A strengths and
arbitrary real competitor strengths supported on a subset of the stated
B. The positive intersection consists exactly of the equal-strength ray.
The two additional real projective types are the stated negative
golden-ratio-square patterns. No zero-valued B branch is omitted under
the theorem's nonzero-A hypothesis.

**[PROVED: in-house, independently attacked]** The R5 positive
same-support ambiguity, its inequivalence under the intrinsic real
symmetries, and the failure of a positive local lower Lipschitz bound
pass the attack. The Fourier-nonvanishing claim is independently
established without relying on the author's saved Bezout coefficients.
A short factorization below proves the stronger fact that all real
members of this particular line have no Fourier zeros.

**[PROVED: bounded corollary]** The normalized R5 A-to-B incidence in
§3 is isolated near the all-ones pair: this follows immediately from
the global W21 classification. The negative-r branches cannot enter
that neighborhood, and fixing the stated scale fixes the remaining ray.

**[OPEN: not reviewed here]** The other twelve template-local conclusions
in §3, their ranks, obstruction matrices, R2 analytic curves, R7 affine
line, and all-template transport claims were not attacked in this pass.
This review does not warrant promoting that full table. The general
weighted competitor problem outside the prescribed B is also untouched.
The author's particular saved integer Bezout identity was not checked
coefficient by coefficient; its Fourier-nonvanishing conclusion was
proved separately. No historical novelty is asserted.

## Independent derivation of W21

**[PROVED: review derivation]** All equations were rebuilt directly from
a length-21 grid using

```
C_x[d] = sum_{j=0}^{20} x[j] x[(j+d) mod 21].
```

The separate code imports neither the author implementation nor its
certificates. A second pair-enumeration implementation in the review's
tests agrees on the entire symbolic 21-coordinate correlation vector.
Its binary specialization also agrees with the immutable reference ICV.

The six singleton rows are indeed d=1,2,4,5,8,10. Since all A entries
are nonzero, these rows force b0,b1,b2,b4,b5 to be nonzero. They do not
initially force b3 nonzero, and no step below divides by b3.
With s=b0 the first four singleton equations give

```
b1=a0*a1/s, b2=a2*a3/s, b5=a4*a5/s,
b4=a1*a2*s/(a4*a5).
```

Substitution in d=8,10 gives exactly

```
a0*a1^2*a2=a3*a4*a5^2,
a1*a2^2*a3=a0*a4^2*a5.
```

Put p=a0/a3, q=a1/a5, h=a2/a4. Both constraints reduce to
`p*q^2*h=1` and `q*h^2/p=1`. Thus `(qh)^3=1`. Crucially, this
uses real strengths: `qh=1`, followed by `p=h`. It is invalid over
the complex numbers, which are outside the theorem.

Write r=h, x=a3, y=a4, z=a1. All r,x,y,z,s are nonzero. The resulting
normal form is

```
a=(r*x,z,r*y,x,y,r*z),
b=(s,r*x*z/s,r*x*y/s,t,s,r*y*z/s).
```

After division by xy,xz,yz, the d=3,6,9 differences have common constant
part and variable parts `-r^2*x*z/s^2`, `-r^2*y*z/s^2`,
`-r^2*x*y/s^2`. The first minus the second is
`-r^2*z*(x-y)/s^2`; the first minus the third is
`r^2*x*(y-z)/s^2`. Their nonzero prefactors force x=y=z=u.
This is an equality of real numbers, with no positivity assumption.

After dividing all strengths by u and putting k=r/s, direct correlation
has only four distinct equations:

```
sk=r,
k^2+kt=r^2+1,
s^2+2st=3r,
2s^2+3k^2+t^2=3(r^2+1).
```

Using s=r/k and t=(r^2+1-k^2)/k in the third equation yields
`5k^2=2r^2+r+2`. Here k is nonzero because r and s are nonzero;
also `2r^2+r+2=2(r+1/4)^2+15/8` is strictly positive for real r.
Independently substituting in the fourth equation, multiplied by k^2,
gives the polynomial

```
-4k^4+5k^2*r^2+5k^2-r^4-4r^2-1.
```

Replacing k^2 by `(2r^2+r+2)/5` factors this as
`9(r-1)^2(r^2+3r+1)/25`. No vanishing denominator is possible.
It follows that r=1 or r=(-3±sqrt(5))/2.

For r=1, k=±1 and s=t=k. For the other roots, r^2+3r+1=0 implies
k^2=-r, s=-k and t=2k. These produce exactly the author's branches.
Every branch was independently substituted into all 21 directed
correlation entries using exact radicals. All B entries, including the
initially unrestricted b3=t, are then nonzero.

For positive A entries, u>0 from its slots 1,3,4 and r>0 from its
other slots. Both quadratic roots are negative, so only r=1 remains;
positive B then forces the common sign to be positive. This confirms
the global positive claim and the completeness of the real signed
claim. Allowing an A zero or using complex strengths changes the
argument and is correctly excluded by the theorem.

## Separate attack on same-support instability

**[PROVED: independent hand argument and exact checks]** Let
`p=1_{S}` with `S={0,3,15}` and let T translate by 7. Then
`T S={1,7,10}`, these supports are disjoint, and

```
u=1_A=p+Tp,        v=p-Tp.
```

Translation preserves autocorrelation. The mixed term in
`C_{u+t v}` is therefore `2(C_p-C_{Tp})=0`; hence
`C_{u+t v}=C_u+t^2 C_v=C_{u-t v}` for every real t.
For `0<|t|<1`, both signals have exactly support A and strictly
positive strengths. This supplies a short structural check independent
of the author's Jacobian certificate.

The unique cyclic adjacent gap of length one in A is 0 to 1. A
preserving translation must fix that directed gap, so is the identity.
A preserving reflection would swap its endpoints and therefore be
`a -> 1-a`; it sends 3 to 19, outside A. Thus the support stabilizer
is trivial. Independent enumeration of all 42 dihedral maps agrees.
Positivity excludes global-sign equivalence, and the identity does
not exchange the two signals for t nonzero.

Because `<u,v>=0` and `||u||^2=||v||^2=6`, the normalization in the
author note is exact. In particular

```
||x(t)-x(0)||^2=2-2/sqrt(1+t^2),
||x_+(t)-x_-(t)||=2|t|/sqrt(1+t^2).
```

The first distance is Theta(|t|). For normalized correlation the exact
measurement change is

```
C_{x(t)}-C_{x(0)} = t^2*(C_v-C_u)/(6*(1+t^2)).
```

The coefficient vector is nonzero. Fourier transformation therefore
gives squared-power change Theta(t^2). For the unnormalized DFT,
the DC squared-power change alone is `-6t^2/(1+t^2)`, and the DC
magnitude change is `sqrt(6)*((1+t^2)^(-1/2)-1)`.
Smoothness of all other magnitude coordinates follows from the
nonvanishing proof below. The full magnitude change is Theta(t^2).
Thus even a selected single branch has no Lipschitz inverse extending
to x(0); keeping both branches makes the neighborhood noninjective.
For a quotient metric modulo intrinsic symmetries, the same conclusion
holds locally: the base has trivial stabilizer and its finitely many
other symmetry images are positively separated.

## Fourier nonvanishing without the author's certificate

**[PROVED: independent strengthening]** On z^21=1,

```
P_t(z)=(1+z^3+z^15)*[(1+t)+(1-t)z^7].
```

The separate code checks this polynomial identity modulo X^21-1.
Put y=z^3, so y^7=1. The first factor is `1+y+y^5`. At y=1 it is
3. At a nontrivial seventh root, it cannot vanish: its rational
polynomial has degree five, less than degree six of the minimal
polynomial Phi_7. The second factor also cannot vanish for real t.
If z^7=1 it equals 2. Otherwise z^7 is a nonreal cube root; its
imaginary part would force t=1, leaving value 2. Consequently every
real point of this line, including t=±1 where some weights vanish,
has no zero Fourier coordinate.

For the base polynomial P_A, the review also ran its own rational
Euclidean division and obtained `gcd(P_A,X^21-1)=1`. A separate SymPy
check against each of Phi_1,Phi_3,Phi_7,Phi_21 agrees. These checks
do not reuse the author's integer Bezout coefficients.

## Reproduction and evidence

**[COMPUTED]** Independent audit source and tests are
`src/weighted_six_review.py` and `tests/test_weighted_six_review.py`.
The code uses the full-grid directed model; the tests independently
use all ordered support pairs. The classification, zero-coordinate
issue, branch identities, critical line, stabilizer, exact order-two
measurement change and Fourier nonvanishing all pass.

```sh
.venv/bin/python src/weighted_six_review.py
.venv/bin/python tests/test_weighted_six_review.py
```

Both commands complete in seconds on the pinned environment.
Outputs are `results/2026-10-01-weighted-six-review/independent-audit.json`,
`verification.txt` and `tests.txt`. The result README records the scope.
No author's source, protected reference, data, ledger or open LaTeX file
was edited. No commit was made by this reviewer. This review closes
only the stated in-house proof gate; external mathematician review and
historical priority remain separate work.
