# Independent attack of the universal autocorrelation formulation

Date: 1 October 2026. Reviewed text:
`notes/2026-10-01-universal-autocorrelation.md`, §§1–5 and Sources.
Separate review context; no computational check or full re-verification of
Theorem G was performed. The shared session startup reference-suite pass
is recorded in PROGRESS; no numerical claim below depends on it.

## Verdict and exact accepted scope

The four-way equivalence in §§1–2 has a complete elementary written proof
for **arbitrary complex functions on any finite abelian group**, including
the trivial group, zero functions and Fourier zeros. I found no mathematical
correctness blocker. It can be accepted as **[PROVED], in-house exposition
of established identities**, with this separate attack logged. This accepts
the displayed theorem and its binary-fibre corollary; it adds no novelty,
constructive-completeness, efficiency or physical-material claim.

The finite group, unnormalized transform and unnormalized convolution are
essential parts of the statement. The arbitrary-group wording here concerns
finite **abelian** groups; no nonabelian or infinite-group extension was
reviewed or inferred.

## Adversarial checks of the proof

1. **Normalization and signs.** With the given transform, the inverse factor
   is `1/|G|`, convolution transforms to pointwise multiplication, involution
   transforms to complex conjugation, and the transform of `delta_0` is
   exactly one. Thus the condition is `u*u*=delta_0`, with no missing group
   order. Directly, `C_f(t)=sum_x f(x) conjugate(f(x-t))`; this is the
   displacement orientation used in `Q_K`, so there is no hidden sign
   reversal in §2's last identity.
2. **Zero bins and existence.** Equal magnitudes force the two transforms to
   vanish at precisely the same characters. Assigning phase one at each
   shared zero is legitimate, produces an invertible spectral unit, and
   leaves `u*f=g`. This also handles `f=g=0`. The constructed unit is
   generally nonunique at zero bins; no uniqueness is asserted.
3. **Real signals.** The character-conjugation symmetry of the ratios is
   preserved by the common value one on zero bins. Self-conjugate characters
   have real transform values and hence nonzero ratios in `{+1,-1}`.
   These facts suffice for the inverse transform to be real. Positivity,
   nonnegative coefficients, rationality and binary preservation do not
   follow, and the note does not assert them.
4. **Convolution converse.** Reordering factors in
   `(u*f)*(u*f)*` uses the abelian group algebra. The stated scope supplies
   that hypothesis, so the converse gives precisely `C_g=C_f`.
5. **All pair kernels.** Grouping ordered pairs by `t=x-y` proves the
   functional identity for every complex kernel. Point-indicator kernels
   recover each autocorrelation coefficient; a restricted family of kernels
   would need its own separation argument. The displayed functional includes
   diagonal/self terms and the conjugated second weight. It does not claim
   to encompass arbitrary higher-order interactions or vector/species
   cross-correlations.
6. **Binary intersection.** Both inclusions follow from the universal
   equivalence. For binary outputs the zero-displacement coefficient is
   the cardinality, so the claim about automatic preservation of `|A|` is
   correct, including empty sets. This relies on the full autocorrelation,
   including its zero coefficient; it must not be silently replaced by
   off-diagonal interval data when comparing arbitrary cardinalities.

## Interpretive and validation boundaries

Theorem G's stated graph conclusion in the exported
`six-point-homometry/notes/2026-09-30-six-generation.md`, §1, agrees with
§3's description: cyclic groups, six distinct occupied points at every
vertex, and T/I classes connected by guarded constructions and compositions.
The spectral-unit orbit itself is much larger and need not stay binary.
The universal theorem therefore does not prove G, a disjoint classification,
an admissibility algorithm or an all-cardinality generating grammar. My
comparison checks this scope only; G's mathematical and finite certificates
were not independently reverified in this attack.

Section 4 is valid for the declared finite periodic scalar-weight model
with **all character intensities at a fixed contrast and a known common
scale**. Missing bins, unknown normalization, noise, continuously positioned
atoms, contrast-dependent factors and correlated disorder require additional
hypotheses. The note already keeps those model changes separate. Its
pair-energy consequence concerns the chosen scalar translation-invariant
quadratic functional on the specified configurations; it gives no formation,
relaxation, stability, dynamics, electronic or superconducting conclusion.

Section 5 correctly keeps the user-supplied outside checks as **reported
evidence**, separate from locally inspected runs. No raw code, logs or new
executions of those checks were available to this reviewer. Finite-range
agreement cannot replace the universal line, high-rank, DAG-coverage and
specialization obligations. An independently chosen dyad menu also needs an
exact equivalence argument before it can validate G's particular D grammar.

## Attribution and remaining issues

No required mathematical repair was found. For referee-facing clarity,
explicitly state the complete-data/known-scale qualification when summarizing
the diffraction conclusion; it is a model boundary, not a defect in the
algebraic proof.

The note credits the spectral-unit and phase-orbit antecedents and makes no
historical-first claim. I read its citations and the exported reference map,
but did **not** freshly read those primary sources in this attack. Their
recorded reading scopes are not promoted to a new independent source audit.
In particular the exact Rosenblatt–Seymour antecedent remains a separate
source-attribution task; no unread factorization or coefficient-field theorem
is used as an axiom by the complete proof above. The wider finite-abelian
formulation is justified by that proof, rather than an unverified assertion
that a cyclic source states the same scope.

## Addendum: accepted factorization and measurement-scope revision

On 1 October 2026 I reread the revised canonical note in full, including
the new classical-factorization subsection. The complete-character,
fixed-scalar and known-common-scale qualification now explicitly resolves
the exposition suggestion above. The four-way proof and binary-fibre
statement are unchanged, so the original mathematical verdict still applies.

The new factorization statement is compatible with the note's separation
of universal weighted identities from constrained six-point generation.
It explicitly restricts Rosenblatt's Theorem 3.6 to cyclic groups and
conjugation-closed coefficient fields, allows signed rational factors for
binary inputs, and makes no positivity, sparsity, uniqueness or binary-factor
claim. Its converse follows directly from commutative convolution:
the two autocorrelations are both `(P*Pstar)*(Q*Qstar)`; each sign has
squared modulus one and each endpoint translation disappears from its
autocorrelation. Thus the formula is consistent with the normalization and
involution already fixed in §1, including singular/zero factors.

The cyclic restriction is consequential. This precise signed-translation
factorization must not be promoted to every finite abelian group simply
because the preceding spectral-unit theorem covers them. For example, over
the real group algebra of `Z_2 x Z_2`, involution fixes every function, so
`P*Qstar=P*Q`; the displayed formula would permit only signed translates.
There are additional real spectral units: an inverse transform of character
signs `(1,1,1,-1)` is not a signed point mass and has autocorrelation
`delta_0`. The revised note does not make that false extension.

The source-completeness claim in this new subsection relies on the root
agent's and literature agent's freshly recorded primary reading of
Rosenblatt (1984), §3's field hypotheses and Theorem 3.6/proof, pp.327–328.
I checked the restated scope and its mathematical compatibility, but did
not independently reread the scan or replace that published proof with a
new proof here. The root reports only metadata/abstract access for the
1982 Rosenblatt–Seymour original, and the canonical note now explicitly
preserves that limit and attributes its restatement through 1984. This
supersedes the initial review's attribution-pending remark for the cyclic
1984 theorem; it does not promote the unread 1982 proof to independently
verified source evidence. No new G review, numerical check or outside-run
verification was performed. No further correctness issue was found.
