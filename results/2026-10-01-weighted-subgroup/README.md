# Exact weighted subgroup controls

1 October 2026. **[COMPUTED]** Exact rational controls for the full proof in
`notes/2026-10-01-weighted-subgroup.md`; theorem status is tracked there.
These are construction checks, not a subset census or a priority claim.

- `certificate.json`: complete positive rational Z/21 pair, its exact
  autocorrelation, rigid-orbit distance, nonvanishing Fourier gcd and
  Jacobian rank. Sixty independent parameter choices cover q in
  {7,8,9,11,13,31}, m=3..12, with exact Cayley all-pass kernels.
- An independently authored implementation, different rational witness,
  ambient DFT checks and additional exact ranks are in
  `results/2026-10-01-weighted-subgroup-review/`.
- `certificate.json` also contains an aperiodic14-point Z/35 example:
  an isolated quartic root and rational Cayley expression specify its
  partner exactly; exact norm bounds certify positivity and inequivalence.
  Its18-by-14 Jacobian has rank13. This example is weighted, not binary.

Reproduce in the pinned Python3.12.12/NumPy2.5.3 environment:

```sh
.venv/bin/python src/weighted_subgroup.py
.venv/bin/python tests/test_weighted_subgroup.py
.venv/bin/python src/weighted_subgroup_review.py
.venv/bin/python tests/test_weighted_subgroup_review.py
```

The author test additionally reconstructs known-support consistent powers
modulo subgroup units at21(q,m) choices, and checks the stated stability
bound numerically. It imports the immutable reference for binary
autocorrelation-convention controls. Numerical examples support the exact
written reconstruction/bound proofs; they do not prove them by extrapolation.
The initial m=12 rational Cayley benchmark was0.0016s; all60 exact controls
took0.53s (0.86s including the later algebraic puncture certificate).
U/F/C/H/S passed the independent attack. Protected files, old media and
the open manuscript are preserved.
