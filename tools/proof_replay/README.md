# Independent replay of the cvc5 proof certificates (Theorems I and Iw)

Author: Hunter Bown, with AI assistance. Replay performed 4 October 2026.

Theorem I (six distinct real points with equal distance multisets are a
Bloom pair or congruent) and Theorem Iw (the same for six-atom multisets)
are proved in `notes/2026-09-30-six-integer-theorem.md` by exact SMT
unsatisfiability. Branch BF of Theorem G depends on Iw. Until now the only
checks of those certificates were cvc5's own internal proof checker and a
second solver (Z3) on one of the encodings. A solver checking its own proof
is not independent evidence. This directory records a replay of the saved
proofs in **Ethos**, a proof checker that shares no code with cvc5's solving
engine, together with a check that each proof's assumptions are the saved
problem's assertions.

## What was replayed

cvc5 1.4.1 emits proofs in its Cooperating Proof Calculus (CPC), a Eunoia
signature shipped in the cvc5 source tree (`proofs/eo/cpc/Cpc.eo`). The
three saved proofs are:

| Proof (gzipped, in `results/`) | Encodes | SHA-256 of proof | SHA-256 of problem |
|---|---|---|---|
| `2026-09-30-six-integer-two-plane/cvc5.proof.gz` | Theorem I, original "count" encoding (`count.smt2`, 31 assertions) | `72f76396…3ada02` | `845fb30d…2de667` |
| `2026-09-30-six-integer-review/gap-bijection.proof.gz` | Theorem I, reviewer's gap/bijection encoding (965 assertions) | `08e17029…773923` | `83b1adbd…013b00` |
| `2026-09-30-six-integer-weighted-review-ordered/gap-bijection.proof.gz` | Theorem Iw, gap/bijection encoding with weak gaps (1,175 assertions) | `1cdbb27c…c92b0c` | `e8a9bcf7…cbccb30` |

Full hashes are in `evidence/replay.json`.

## Checker and signature

- **Ethos 0.2.5**, built from source at commit
  `08e4aa40c4f8a6e00833f10e8d8985777e424027` (github.com/cvc5/ethos). This is
  exactly the commit that cvc5 1.4.1's `contrib/get-ethos-checker` pins, so
  checker and signature are the versions cvc5 itself tests against.
- **CPC signature** from the cvc5 1.4.1 source tarball
  (`cvc5-1.4.1.tar.gz`, SHA-256 `5448e826…bb4f76`), file `proofs/eo/cpc/Cpc.eo`
  with SHA-256 `8c612363…4d98bf36` and its included theory and program files;
  all their hashes are recorded in `evidence/replay.json`.
- Ethos was run with `--require-proof-of-false`, so a proof whose last
  top-level step does not conclude `false` is rejected.

## Result

All three proofs check as `correct`:

| Proof | Ethos | Time | Assumptions vs. assertions |
|---|---|---|---|
| Theorem I, count encoding | correct | ≈7 s | 30 assumptions, all among the 31 assertions; `(< r 1)` unused |
| Theorem I, gap/bijection | correct | ≈5 s | 965 = 965, exact match |
| Theorem Iw, gap/bijection | correct | ≈11 s | 1,175 = 1,175, exact match |

The assumption comparison (`check_assumptions.py`) expands the proof's
`define`s and the problem's `define-fun`s, normalizes numerals (`0/1` vs
`0`) and cvc5's flattening of a one-argument `and`, and requires every
`assume` of the proof to be an assertion of the problem. An assertion the
proof never uses is allowed: deriving `false` from a subset refutes the
whole problem.

## What this does and does not establish

Established: each saved `.smt2` problem is unsatisfiable, as certified by a
checker independent of cvc5, at the signature version matching the solver
that produced the proofs. The two Theorem I encodings were written
independently (builder and reviewer) and both are refuted.

Still trusted: Ethos itself and the CPC signature (the signature's header
states that its rules are additionally verified in Lean through the Logos
project; that is the signature authors' statement, not something checked
here); and, above all, that the SMT **encodings** say what the theorems
say. The encodings are audited in prose in
`notes/2026-09-30-six-integer-theorem.md` §§2–3, 6 and in the reviewer's
`notes/2026-09-30-six-integer-review.md`. A reader who doubts Iw should read
the encodings, not the solver.

## Reproducing

```sh
# 1. Checker at cvc5 1.4.1's pinned commit
git clone https://github.com/cvc5/ethos && cd ethos && git checkout 08e4aa40c4f8a6e00833f10e8d8985777e424027
mkdir build && cd build && cmake .. -DCMAKE_BUILD_TYPE=Release && make -j
# 2. Signature from the cvc5 1.4.1 source
curl -L https://github.com/cvc5/cvc5/archive/refs/tags/cvc5-1.4.1.tar.gz | tar xz
# 3. Replay (from the repository root)
.venv/bin/python tools/proof_replay/replay_cpc_proofs.py \
    --ethos /path/to/ethos/build/src/ethos \
    --cpc /path/to/cvc5-cvc5-1.4.1/proofs/eo/cpc/Cpc.eo \
    --ethos-commit 08e4aa40c4f8a6e00833f10e8d8985777e424027
```

The script strips the single outer parenthesis pair that cvc5's API adds
around a dumped proof, prepends the `include` of the signature, runs Ethos,
runs the assumption check, and writes `evidence/replay.json`. Total time
under a minute. `tests/test_check_assumptions.py` exercises the comparison
on synthetic inputs and is part of `scripts/verify.py`.
