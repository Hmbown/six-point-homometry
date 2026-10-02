# Separate exact R5 review

Review: `notes/2026-10-01-weighted-six-review.md`.

Independent derivation rebuilds all21 directed autocorrelation equations,
does not import the author's implementation or certificates, and checks:
the global real fixed-support classification, initially allowed B zeros,
all signed radical branches, positive same-support ambiguity, dihedral
inequivalence, exact second-order measurement change and Fourier
nonvanishing. The review's tests use a second ordered-pair model and the
immutable reference ICV.

```sh
.venv/bin/python src/weighted_six_review.py
.venv/bin/python tests/test_weighted_six_review.py
```

`independent-audit.json` retains the independently derived equations,
eliminant, branch checks, correlation changes, stabilizer enumeration,
cyclotomic remainders and own rational Euclidean gcd. `verification.txt`
and `tests.txt` retain passing checks.

Scope: R5 only. R5's local normalized A-to-B isolation follows from its
global classification; the other twelve template-local conclusions and
their certificate entries are not reviewed by this artifact. This is an
in-house attack, not external peer review or a novelty assessment.
