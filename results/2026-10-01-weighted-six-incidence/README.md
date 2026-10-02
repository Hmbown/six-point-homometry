# Fixed-support weighted cyclic incidence certificates

**[COMPUTED]** exact coefficients and independent implementation controls.
W21 and its R5 local/instability corollaries passed the separate attack;
the other twelve template-local conclusions await separate review.
No arbitrary-support or novelty claim.

```bash
.venv/bin/python src/weighted_six_incidence.py --out results/2026-10-01-weighted-six-incidence
.venv/bin/python tests/test_weighted_six_incidence.py
```

`certificates.json` contains all 13 folded autocorrelation Jacobians,
nonzero rank minors, normalized tangent bases, left kernels and projected
quadratic obstructions. It also includes the 21-point benchmark's three
real projective amplitude types, its exact norm eliminant and an integer
Fourier Bezout identity. `summary.json` records the certificate digest and
build timing. `verification.txt` records the independent tests.

The global positive-strength benchmark incidence is the equal-strength ray.
Candidate local proofs say eleven of the thirteen pairs isolate after
fixing common scale, R2 has two analytic curves and R7 an exact line;
only R5's local conclusion has been separately reviewed. The benchmark A
also has a nontrivial positive same-support ambiguity arbitrarily near
equal strengths. These are prescribed-support statements; competing
supports outside the binary six-note grammar remain unclassified.

Full scope, accepted results and remaining candidate proofs:
`notes/2026-10-01-weighted-six-incidence.md`.
Separate attack: `notes/2026-10-01-weighted-six-review.md`.
