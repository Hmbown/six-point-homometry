# Independent attack of coset and aperiodic weighted phase ambiguity

> Mathematics-only export. Nonmathematical media passages were omitted;
> mathematical arguments and acceptance boundaries are retained. Copy provenance
> and upstream/export hashes are in `docs/EXPORT_MANIFEST.json`.

1 October 2026. **Written-proof attack: ACCEPTED for U, F, C, H and S.**
The independently reproduced controls below are **[COMPUTED]**. This is
an in-house mathematical attack, not an external specialist review. No
novelty, historical-priority or external human-review claim is made.

## Plan and evidence standard

1. Read the original standard-coordinate conjecture, including its
   difference convention, real symmetry group and genericity definition.
2. Reconstruct the subgroup convolution, embedding and positivity
   arguments independently, looking for an excluded hypothesis.
3. Produce an exact rational positive witness, full rigid-orbit control
   and Jacobian obstruction, plus an independent ambient DFT audit.
4. Attack the root's full written statement before accepting a proof;
   keep the convolution-group result separate from a classification of
   every weighted phase-retrieval ambiguity. Estimated compute: seconds.

## Original primary-source hypothesis check

Freshly read Bendory–Edidin,
[arXiv:2002.10081v2](https://arxiv.org/pdf/2002.10081),
§§1.3,4.1.1–4.1.2,4.3.1–4.3.2,4.3.4 and the real group discussion
in §5. The PDF identifies v2, 2 July 2020.

Conjecture 4.7 fixes a support S with more folded cyclic difference
classes than support coordinates, and asserts recovery for a nonempty
Zariski-open subset of its coordinate space. Conjecture 4.11 states
the same-support recovery claim. The real intrinsic group consists
of sign, cyclic shifts and reflection. Zero is included in the folded
difference set. No aperiodic-support exclusion appears in those
statements. The notation section explicitly extends the even-N setup
to odd N using floor(N/2). This review tests the stated sparse setting
and even keeps both candidates on the same support.

This is a reading of those original statements, not a claim that their
status, corrections or all subsequent literature have been resolved.
The separate literature agent owns that broader audit.

## Independently reconstructed mechanism

Let N=7m, H={0,7,…,7(m−1)} and S=H+{0,1,3}. The quotient positions
have difference set `{0,±1,±2,±3}=Z/7`; therefore `S−S=Z/N` before
folding. There are exactly `floor(7m/2)+1` folded classes and K=3m
coordinates. Their difference is `floor(m/2)+1>0`, and K≤floor(N/2).
The period subgroup is exactly H: a nonzero period of the three-element
quotient support in prime order seven would force the whole quotient.

For a kernel supported in H, ambient convolution acts separately on
each H-coset block and hence preserves the coordinate space E_S.
With the unnormalized DFT convention, its ambient multiplier at k is
the H-DFT multiplier at k modulo m: `exp(−2πik·7j/(7m))`
equals `exp(−2πikj/m)`. Conjugate phase pairs and real unit signs at
self-conjugate frequencies give a real kernel and unit modulus at all
ambient frequencies.

The proposed support-space equivalence passes the independent initial
attack for **nonempty** S. Apply a convolution to each delta vector
δ_s. Every h in its kernel support must satisfy S+h⊆S; equal finite
cardinalities give S+h=S. Conversely support in the period subgroup
preserves E_S. Applying power preservation to δ_s forces every
ambient multiplier to have modulus one. Thus restricting to the period
subgroup loses no kernel in this particular fixed convolution group.
The identity component has dimension `floor((|H|−1)/2)`; the number
of independent real sign factors is one for odd |H| and two for even
|H|. Empty S must be excluded because both delta-vector necessity
arguments are then vacuous.

At a vector with every ambient Fourier coefficient nonzero the action
is free: a stabilizing multiplier must equal one at every frequency.
Those nonvanishing conditions are a nonempty Zariski-open subset of
E_S; each excluded Fourier coefficient is a nonzero real linear or
two-real-component polynomial condition, since it is nonzero on δ_s.
Near identity a positive vector stays positive in every supported
coordinate, while zeros outside S remain exact. A positive-dimensional
free orbit cannot fit into the finite real intrinsic orbit.

## Exact three-point rational control

For m=3, define a kernel on H by

\[
 u(t)=\frac{(1-t^2,\;2t(t-1),\;2t(t+1))}{1+3t^2}.
\]

Independent symbolic expansion gives sum 1, squared norm 1 and zero
nonzero-lag cyclic autocorrelation for every real t. Hence the ambient
embedded kernel has autocorrelation δ_0 exactly. At t=0 it is the
identity kernel; its derivative is `2(δ_14−δ_7)`. The tangent vanishes
exactly when all three H-coset blocks are constant, a proper
three-dimensional linear subspace of the nine-dimensional E_S.
Outside this subspace the local curve is nonconstant. For every
exact-support positive vector a sufficiently small interval remains
positive and has nonrigid points; the finite intrinsic orbit cannot
exhaust a nonconstant local curve.

At t=1/6, `u=(35,−10,14)/39` on positions 0,7,14. Use the positive
integer coset blocks

```
positions 0,7,14:  2, 3, 5
positions 1,8,15:  7,11,13
positions 3,10,17:17,19,23
```

The exact convolution y has the same nine-point support and minimum
positive amplitude 62/39. Its full rational ambient autocorrelation
equals that of x. Its minimum squared Euclidean distance from all
84 sign/shift/reflection images of x is 168/13, strictly positive.
Thus the witness is not a disguised rigid transform.

The exact gcd of the signal polynomial with `z^21−1` is one, proving
that this explicit x has no ambient Fourier zero. The folded
autocorrelation Jacobian is 11×9 with exact rank 8; multiplication by
the nonzero convolution tangent gives the zero vector. This verifies
the local infinitesimal obstruction separately from the exact
rational fibre calculation.

The full output, including rational x,u,y, tangent, distances and DFT
residuals, is retained in
`results/2026-10-01-weighted-subgroup-review/independent-audit.json`.

## Reproduction

```bash
.venv/bin/python src/weighted_subgroup_review.py
.venv/bin/python tests/test_weighted_subgroup_review.py
```

All six independent regression groups pass. Exact support, period and
folded-distance conditions were checked for m=3 through 24. Independent
ambient-DFT controls for m=3 through 12 include both odd and even subgroup
orders and verify real kernels, support, positivity and Fourier power.
The finite calculations take less than one second and are controls of
the displayed identities, not a large support census or a proof by fit.
The startup pinned guards/reference tests had already passed in the root.

## Stronger fixed-support quotient reconstruction: independent derivation

For an ordered-difference Sidon quotient Q⊂Z/q of cardinality r≥3,
put `S=Q+qZ/(qm)`. No coprimality of q and m is required. Partition
ambient frequencies as `k=ℓ+tm`, with t=0,…,q−1. This q-tuple is the
q-point DFT of quotient coefficients

\[
 a_r(\ell)=e^{-2\pi i\ell r/(qm)}
          \sum_{j=0}^{m-1}x_{r+qj}e^{-2\pi i\ell j/m}.
\]

The inverse q-DFT of that q-tuple's powers gives each ordered product
`a_r conjugate(a_s)` at difference r−s, because nonzero differences
are unique. If all the coset DFT coefficients of x are nonzero, any
same-support candidate y with equal power has nonzero coefficient
ratios ρ_r. They satisfy `ρ_r conjugate(ρ_s)=1` at every pair.
Three vertices force every modulus to one and every phase to the same
value. Further vertices have the same value by their pair constraints.
Hence the whole fixed-support fibre is obtained by one phase per H
frequency. Reality imposes conjugate pairs and real signs at the one
or two self-conjugate H frequencies, exactly the H spectral-unit group.
This is a full same-support conclusion; candidate supports outside S
remain unclassified.

Differentiating the pair products gives
`η_r+conjugate(η_s)=0` for infinitesimal ratios η_r. Three vertices
force all real parts to zero and all imaginary parts equal. The
self-conjugate frequencies have zero tangent, and opposite frequencies
have opposite tangent phases. Thus the expected Jacobian kernel is
exactly the subgroup torus tangent, of dimension floor((m−1)/2).

The exact folded difference count is

\[
 |S-S|_{\mathrm{fold}}=m\binom r2+\lfloor m/2\rfloor+1.
\]

Indeed the raw difference count is `m(1+r(r−1))`. Inversion has one
fixed element when m is odd and two when m is even. If q is even and
m is odd, the ambient half-period projects to q/2, which cannot be a
Sidon quotient difference: its reversed ordered pair would duplicate
it. For even m the ambient half-period projects to zero and is present.
The Sidon bound `q≥1+r(r−1)` also ensures K=rm≤floor(qm/2).
For r≥3 the displayed folded count exceeds K.

Additional independent controls use q=7,8,9 with m=3 through 8, and the
four-point quotient `{0,1,3,9}` at q=13, m=3,4. Every exact rational
Jacobian has rank `K−floor((m−1)/2)`. Integer skew-convolution tangent
columns have exact rank floor((m−1)/2) and are killed by the Jacobian.
A separate ambient frequency-block calculation recovers every ordered
pair product, agreeing within 1e−9. These include q,m with common
factors. All 20 exact rank controls are retained in the review output.
The six regression groups finish in 1.140 seconds.

## Written-proof attack: U, F and C

The complete written argument attacked is
`notes/2026-10-01-weighted-subgroup.md`, rather than the author's initial
chat sketch. The accepted draft is preserved verbatim in
`results/2026-10-01-weighted-subgroup-review/accepted-root-draft.md`.
Its SHA256 is
`79283b0144622bf1f73f681252d14b7c62e12c03f8a64267ea7677ece4b9c507`.

U's delta-basis argument defeats the possible cancellation objection,
and its nonempty-support condition prevents a vacuous counterexample.
The restriction of ambient characters to a cyclic subgroup is surjective,
so embedding a subgroup unit loses no required ambient frequency.
F's pair-product argument uses ordered differences, including their
orientation; no CRT or coprimality assumption is needed. The action
is free under block nonvanishing even if an ambient transform happens
to cancel between cosets. This condition is distinct from U's sufficient
ambient nonvanishing condition. The differential proof establishes the
rank at every stated generic point, not just at the sampled controls.
C's count treats the ambient half-period correctly even when q is even
and m is odd. All three written proofs pass the independent attack.

The positive examples satisfy the literal fixed-support genericity and
difference assumptions of the original v2 conjectures described above.
Both Conjectures 4.7 and 4.11 are contradicted in that stated real setting.
The generic positive failure occurs on a nonempty relatively Euclidean-open
subset of E_S and therefore cannot be hidden in a proper algebraic
exceptional set. No journal full-text, correction or later-status claim is
inferred from this comparison. Weighted periodic examples have K>=9;
binary full-coset indicators have zero nonzero block frequencies and lie
outside F's generic set.

## Written-proof attack: H and the aperiodic obstruction

Independently take `S0={0,1,3}+qZ/(qm)` and delete zero to obtain S, with
q>=7 and m>=5. A support period projects to a quotient period. The Sidon
ordered-difference argument excludes every nonzero quotient period.
The period subgroup is therefore inside H, and its order divides both
m and 3m-1. Their gcd is one, proving `H_S={0}`. Thus this is an
aperiodic support, rather than an unequal weighting of a periodic support.

Deleting zero does not remove any raw difference: a surviving point of
the punctured coset minus a full coset fills the whole difference H-coset,
and an unchanged full coset supplies every within-H difference. Consequently
the same folded count `floor(7m/2)+1` exceeds `K=3m-1`, with K<N/2.
The block nonvanishing conditions remain nonzero polynomials on E_S;
testing a surviving coordinate in each block proves this explicitly.

F describes the fibre inside E_S0 as a free subgroup-unit orbit. To stay
inside E_S it must satisfy the additional single scalar equation y_0=0.
Its derivative along the first skew convolution generator is
`x_(-q)-x_q` (or twice this under the Cayley parameter convention).
This is a nonzero linear form on E_S. Requiring it to be nonzero gives
a nonempty Zariski-open set, which intersects the positive exact-support
orthant densely and openly. The implicit function theorem then gives a
smooth local level set of dimension `d-1`, where `d=floor((m-1)/2)`.
Freeness transfers that dimension to the signal fibre. Intersecting F's
exact Jacobian kernel with h_0=0 removes precisely one dimension, giving
rank `3m-d`. Positivity persists along the local level set, and its positive
dimension excludes exhaustion by the finite intrinsic orbit.

This proves the local dimension and generic positive nonuniqueness in H
as written. It does not classify the global topology of this punctured
fibre. The kernels live on the period subgroup of S0, and their permitted
parameters depend on x through the hole equation; they do not contradict
U's universal convolution classification on the smaller E_S.

Independent exact controls use q=7,8,9 and m=5 through10 (18 cases).
Each support has period group `{0}`, retains the full folded difference
set, and has exact rational Jacobian rank `3m-floor((m-1)/2)`.
Convolution tangent columns are combined to satisfy the hole constraint;
their exact rank is `floor((m-1)/2)-1` and the Jacobian kills all of them.
Every block polynomial is checked coprime to `z^m-1` in these controls.

For the author's Z35 algebraic witness, a second symbolic construction
solves `(I-A)w=x` and uses `Cx=2w-x`, independently of the author's
adjugate multiplication. It reproduces all five primitive quartic
coefficients exactly. A Sturm count gives one root in
`(-6/14917,-5/12431)` and opposite endpoint signs, with |t|<1/1000.
The skew-matrix inverse bound is valid for all real t,v because
`||(I-A)z||²=||z||²+||Az||²`. It gives displacement squared less than
`(8/1000)²*8257<1`; minimum surviving amplitude 2 proves positivity.
The full nonidentity intrinsic separation of x is exactly 502.
The Cayley matrix is nonidentity since v is nonzero and the two skew
generators are independent, and the block-gcd freeness excludes y=x.
The quartic therefore specifies an exact positive nonintrinsic partner,
without relying on rounded roots. The independently computed 18×14
Jacobian has rank13 and kills the displayed nonzero hole tangent.
The entire H proof and algebraic certificate pass the attack. Here K>=14.

## Written-proof attack: S, gauge reality and quantitative constants

S fixes one untwisted anchor coset at every subgroup frequency. This is
essential for the real reconstruction: the phases at opposite frequencies
then conjugate, while self-conjugate frequencies use real signs. An arbitrary
frequency-dependent anchor would require an additional compatibility rule.
The written fixed-anchor choice supplies that rule directly.

The three pair-product formula for the anchor magnitude is correct.
The inverse q-transform bounds each product error by
`e_l=||power-block error||_2/sqrt(q)`. Splitting the quotient AB/C into
three terms gives exactly `2M²/delta²+M⁴/delta⁴`; dividing the difference
of squares by an anchor sum at least 2delta gives L0. Dividing the other
products by their anchors gives `L1=1/delta+M²L0/delta²`. Parseval's
factor 1/m together with the 1/q block error factor yields precisely
`sqrt(r/N)L`, with the unnormalized DFT convention. The reverse bound
`2NR` follows from the Fourier-coordinate bound sqrt(N)R and Parseval.
Both constants have the correct scaling when signals are multiplied by
a common positive scalar.

Independent numeric controls use q=7,8,9 and m=3 through9 (21 cases),
fixing the nonzero anchor coset 3 to stress representative phases and
wraparound differences. Recovered block products and the real canonical
gauge agree with the independently computed transforms; both stability
bounds hold, including odd and even self-conjugate frequencies. S's
written proof passes the attack. It establishes stability on the enlarged
unit-group quotient for known support and consistent powers, bounded
away from vanishing block coefficients. It does not establish the false
finite-intrinsic-group recovery claim, unknown-support recovery, or an
algorithm for inconsistent noisy powers.

## Reproduction, frozen evidence and accepted boundaries

The final independent script writes ten ambient phase controls, twenty
full-coset exact rank controls, eighteen punctured exact rank controls,
twenty-one independent stability controls, and both exact witnesses to
`results/2026-10-01-weighted-subgroup-review/independent-audit.json`.
All eight independent regression groups pass (17.778 seconds). The
author's current seven groups pass (0.405 seconds), including its
algebraic puncture and constructive reconstruction controls. The pinned
immutable reference suite was rerun in this review and passes all ten
groups. These are small structural controls, not a support census.

The reviewed source, tests and certificates are identified in
`results/2026-10-01-weighted-subgroup-review/reviewed-digests.json`.
Review source SHA256:
`973f656d281f5142c10578fdd045ee14776bf3261f05c4a5f0d80e60087bd5a0`.
Independent output SHA256:
`e3e9f2d84fa0c85b4f82887c33d7a1f12e786efdf59718cd5929d58da14eee2f`.

Accepted: U's exact universal convolution group; F's complete generic real
same-support fibre for ordered-difference Sidon quotient lifts; C's folded
counts and generic positive periodic obstruction; H's generic aperiodic
local fibre, exact rank and positive obstruction; S's stated reconstruction
and stability on the enlarged quotient. Rejected as conclusions: generic
uniqueness for these supports, an aperiodicity-only repair, a classification
of other support competitors or all arbitrary-support fibres, and recovery
in the original finite intrinsic quotient. None of these controls establishes
historical priority. The literature audit is separate, and human specialist
review remains appropriate before any public mathematical claim.

## Promotion-only verification and final freeze

The promoted root note has SHA256
`ff3c7e94791cb3541afaf0fde54031d73d77054b312b306d645db1b75dd3c924`.
Its complete diff against the frozen accepted draft was read independently.
Only the header status/review link, the version-specific conjecture-comparison
status, and final review/timing metadata changed. Every mathematical theorem,
proof, displayed formula and witness definition is byte-for-byte unchanged.
All previously recorded source, test and certificate digests still match.
Thus the promotion is accepted on the same mathematical scope. The final
file digests are in `results/2026-10-01-weighted-subgroup-review/final-digests.json`.
The review source, tests, note and independent result are now frozen.
