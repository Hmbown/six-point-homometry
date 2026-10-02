# Reproducing the mathematics

## Environment

Use Python 3.12 and the exact packages in `requirements.txt`. NumPy 2.5.3,
SymPy 1.14.0, mpmath 1.3.0, Numba 0.67.0 and llvmlite 0.49.0 match the
recorded environment. The default checks require no compiler or external
solver. `tests/test_env.py` independently checks that array operands remain
unchanged under the arithmetic used by the certificate programs.

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/verify.py
```

The wrapper first audits package integrity, then copies the mathematical
assets into a temporary directory and executes a bounded suite there. The
original certificate files stay unchanged. Logs and an exact command/exit
receipt are saved under the ignored `.reproduction/` directory. A nonzero
exit or timeout is a failed gate, not a successful partial check.

The wrapper also sets `PYTHONHASHSEED=1` and `PYTHONUNBUFFERED=1` for each
fresh subprocess. The first hosted Linux run timed out in the exact SymPy
weighted-six review. Separate local controls found hash-order-dependent
runtime: seed 0 could stall after a completed assertion group, while seeds
1, 2, 3, 42 and 99 completed the same predicates in under a second.
The recorded seed makes execution reproducible; unbuffered output preserves
progress if a later gate times out. No mathematical assertion is skipped and
the original time limit is retained. If running the individual SymPy checker
directly, use `PYTHONHASHSEED=1 python tests/test_weighted_six_review.py`.

The default suite covers:

- Ten immutable reference regressions and five environment controls.
- The all-modulus Bloom support formula, original matching equations and
  complete saved matching histograms against the independent audit.
- Sparse certificate generation, all 73 composed finite paths, large-modulus
  examples, independent replay and malformed-certificate rejection.
- The four weighted source/review test programs, including exact rational
  and algebraic examples and separate numerical controls.

It does **not** regenerate the full census, all matching systems, all solver
proofs or every low-rank structural cover. Those are distinct obligations.

## Certificate examples

```sh
python src/six_generate.py 21 0,1,3,7,10,15 0,1,4,7,14,16 --out .reproduction/example.json
python src/six_generate.py --replay .reproduction/example.json
python src/six_generate.py --replay results/2026-09-30-six-generate/missing-edge-inflated.json
python src/six_generate.py --replay results/2026-09-30-six-generate/Bloom-large-prime.json
```

Replay checks the explanation using its embedded data. The finite discovery
fallback uses the included `n12.json` through `n135.json` certificate tables;
the repository does not silently download missing evidence.

## Independent proof-certificate replays

### Structural checks without a package registry

The height-growth, HR/BF, complete low-rank DAG and terminal-mechanism
checkers use Python's standard library only. Their transitive imports do
not require NumPy, SymPy or the discovery builders. This is distinct from
the full default suite's package requirements.

Use a **disposable copy** of the repository: the growth and terminal
programs write inherited result locations. From that copy, run:

```sh
mkdir -p .reproduction
python3.12 -S tests/test_six_free_rank_growth.py
python3.12 -S tests/test_six_cylinder_branches_review.py --out .reproduction/cylinder.json
python3.12 -S tests/test_six_free_dag_review.py --require-complete --out .reproduction/dag-fresh
python3.12 -S tests/test_six_low_rank_mechanisms_review.py
```

The `-S` option disables installed site packages. A fresh isolated run on
1 October 2026 passed all four commands with that option: height growth,
HR/BF, all 315 DAG strata and the separate 620-terminal mechanism check.
The DAG run checked 10,602 nodes and 658,894 integral lattice inclusions;
the four commands plus isolation took about 65 seconds on that host.
This is a measured local runtime, not a promise for another machine.

| Checker | Obligation |
|---|---|
| Growth | Exhaustive height-span and permutation-orbit coverage; generic heights for all 104+211 strata. |
| HR/BF | High-rank and Bloom-cylinder reductions, with explicit integral witnesses. |
| DAG | Cross-match orbits, roots, signed branches, decreasing residual multiplicity, Smith witnesses and two-way integral lattice inclusions. |
| Terminals | Construction identities, complete residual cyclic-character covers and half-coset degeneration controls. |

The terminal checker alone is insufficient for exhaustive coverage.
Passing these programs checks their stated predicates against the supplied
certificates; a specialist should also inspect the predicates and the
written reductions that connect them to an arbitrary input pair.

For **fresh** DAG verification, omit `--resume` and use a new output
directory. The optional resume key covers the compressed DAG and cross-file
hashes only; it does not bind checker-source or height-file hashes, nor
recompute skipped predicates. Thus `complete: true` in a resumed run is
not evidence of a fresh replay. The old 9.25-second saved run was a resumed
tail; the new complete DAG replay took approximately 56.7 seconds.

The real-line branch remains a separate solver obligation. With cvc5 1.4.1
available, its independent encodings can be run in the disposable copy:

```sh
python3.12 tests/test_six_integer_review.py --module-dir '' --timeout 60 --out .reproduction/line-strict
python3.12 tests/test_six_integer_review.py --module-dir '' --weighted --order-matches --timeout 60 --out .reproduction/line-weighted
```

Those rebuild independent strict and repeated-atom models and request
internally checked solver proofs. They need the stated solver, and do not
constitute external verification by a small proof kernel. They were not
regenerated in the 1 October framing/structural follow-up.

The following original commands can write outputs. Run them in a disposable
clone, or use the wrapper's `--suite certificates`, which executes them in a
temporary copy. Start with a per-command limit of ten minutes; treat a timeout
as incomplete and increase the budget only deliberately.

```sh
python scripts/verify.py --suite certificates --timeout 600
```

This adds the cylinder-branch checker, free-rank growth controls, the
low-rank terminal checker and the finite-torsion checker. The full structural
low-rank cover is a separate, resumable command:

```sh
python tests/test_six_free_dag_review.py --require-complete --out .reproduction/structural-review-fresh
```

Add `--resume` to continue interrupted work; it uses input hashes to reuse
matching saved work. Reusing a prior
record is not a fresh replay of the skipped calculation. With a new output
directory, this command reconstructs all 315 strata and checks the integral
lattice witnesses. Inspect `summary.json` for `complete: true`. Detailed
source commands and historical costs are in the
[G proof map](../notes/2026-09-30-six-generation.md) and its component notes.

## Regenerating universal Bloom tables

The archived author and independent tables contain all 4,147,200 paired
systems. Small tests inspect those tables and regenerate a bounded independent
slice; full generation is a separate run. Read each program's `--help` and
the [AP proof](../notes/2026-10-01-six-bloom-primary.md), section 6, before
running it. Use an ignored output directory or a disposable checkout.

The support count has a separate Smith/inclusion–exclusion derivation and
literal finite controls. Its arbitrary-modulus proof is not a fitted formula.

## Solver and census obligations

The G real-line branch needs both strict six-point and repeated-atom cases.
Its original records use **Z3 4.15.4** and **cvc5 1.4.1**, with separate
gap/bijection encodings and internally checked compressed proof output.
Those solver runs are outside the default suite. Optional Python solver
packages are listed in `requirements-solvers.txt`; the Z3 commands also need
a `z3` executable on `PATH`. No solver proof was regenerated just by importing
a solver package. See the
[integer proof/review](../notes/2026-09-30-six-integer-review.md) for the exact
models, timeout semantics and version records. In the original independent
checker, use `--module-dir ''` to select the active environment instead of
its historical temporary module directory.

The complete six-subset census through 135 has two C implementations and
full archived family payloads. Rebuilding it requires a C11 compiler and can
be expensive. `src/six_large_census.py` compiles from source and supports
`--resume`; it does not ship a machine-specific binary. Estimate a small
modulus first before scheduling a large range. A resumed completed record
does not establish fresh enumeration.

## Verification boundaries

Package hashes certify exported bytes. Tests certify their stated arithmetic
and rejection controls. Independent proof checks certify the mathematical
predicates they actually replay. None alone establishes historical novelty,
external peer review, every open question or full proof-assistant validation.
The [result map](RESULTS.md) gives the exact dependency and scope of each claim.
