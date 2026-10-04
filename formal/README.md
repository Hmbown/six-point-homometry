# Machine-checked lemmas (Lean 4 / Mathlib)

Author: Hunter Bown, with AI assistance. Added 4 October 2026.

This directory formalizes the **elementary core** of Theorem G: the facts a
reader could check by hand but that carry the whole soundness direction and
one key reduction step. It does **not** formalize the finite certificate
computations (the 135 bound as a graph computation, the census, the
real-line solver result, or the quotient DAG). Those remain audited
computations; see `docs/LR_CHECKER_SPECIFICATION.md` for exactly what the
checkers establish.

| File | What is proved | Statement in the proof |
|---|---|---|
| `SixPointHomometry/Soundness.lean` | In `ℤ[G]` for any additive commutative group `G`: the block moves **L2**, **L3\***, **L4**, **L5** preserve the autocorrelation `F F*` under their stated cross-term hypotheses; **L7** half-per-coset complementation preserves it (algebraic form `J A = k·J C`, `J J = 2k·J`, `J* = J`); the exact **D** identity `X X* − Y Y* = x^{−a−b}(1−x^a)(1−x^b)·K` and the resulting soundness of the dyad exchange when `(1−x^a)(1−x^b)K = 0`. | `notes/2026-09-30-six-generation.md`, Section 2 |
| `SixPointHomometry/Bloom.lean` | The Bloom/Yovanof–Golomb pair `X = {0,a,b−2a,2b−2a,2b,3b−a}`, `Y = {0,a,2a+b,2b−a,a+2b,3b−a}` has `X X* = Y Y*` in `ℤ[G]` for all `a, b : G`, via the signed factorization `X = F·Q`, `Y = F·x^{2b−a}·Q*`. | Section 1, generator **B** |
| `SixPointHomometry/FiniteUnion.lean` | A vector space over an infinite field is not a finite union of proper subspaces; if finitely many subspaces cover it, one is the whole space (wrapping Mathlib's `Submodule.iUnion_ssubset_of_forall_ne_top_of_card_lt`). | Section 3.3, the fixed-alignment step |

All theorems are stated for arbitrary ring elements `U, W, C, J, A : ℤ[G]`,
not only indicator functions. That is the right generality: the identities
are what make the moves sound, and the set-theoretic hypotheses (disjoint
blocks, six distinct points) are only needed so that the ring elements are
indicators of six-point sets.

## Reproducing the check

The files were compiled with **Lean 4.31.0** against **Mathlib commit
`5d1abc4cd8c71e2a463fb58d0e406decab077bdd`** (17 June 2026), pinned in
`lakefile.toml` and `lean-toolchain`. From this directory:

```sh
lake exe cache get      # downloads prebuilt Mathlib oleans for the pinned commit
lake build              # builds SixPointHomometry; no `sorry` anywhere
```

Equivalently, with any checkout of that Mathlib commit already built,
`lake env lean --root=. SixPointHomometry/Soundness.lean` and the two
other files compile with no errors (the Bloom file imports Soundness and
needs its `.olean`, which `lake build` produces).

The verifying run recorded in `PROGRESS.md` compiled all three files with
zero errors. Lean's kernel checks every proof term; the only trusted
components are Lean 4.31.0, the Mathlib commit above, and the statements
themselves, which a reader should compare with the prose.

## What a reader should compare

- The hypotheses of `L2`, `L3star`, `L4`, `L5` are exactly the four
  parameter conditions in the table of Section 1 of the synthesis note,
  written with `P = U * star' W` expanded.
- `L7` is stated algebraically. The translation from "H a subgroup of even
  order with exactly half of each occupied coset in A" to the three
  hypotheses `star' J = J`, `J * J = 2k * J`, `J * A = k * (J * C)` is the
  short computation in Section 2 of the synthesis; the Lean file proves the
  consequence, not that translation.
- The Bloom coordinates use `b + b` for `2b`, `a + a` for `2a`, so that the
  statement needs no scalar action on `G`.
