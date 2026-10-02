# Exact binary reconstruction from displacement counts

This tool enumerates binary arrangements on a finite periodic grid
`C_n1 × ... × C_nd` from exact directed pair counts. It returns one
representative per translation/global-inversion class. Every coordinate is
a grid site and every occupied site has weight one. The solver uses sparse
displacement support rather than allocating the ambient grid.

This is new research software authored on **1 October 2026**, after the
historical extraction checkpoint. Its source, tests and examples are
described in [PROVENANCE.json](PROVENANCE.json); they are not inherited
assets in the repository's export manifest. No novelty, physical prediction,
efficient worst-case recovery or arbitrary-cardinality structural
classification is claimed.

## Input contract

Inputs are JSON objects with schema `homometry.grid-input/v1`, a nonempty
`shape` list of positive integer periods, and `pair_counts` records:

```json
{
  "schema": "homometry.grid-input/v1",
  "shape": [5],
  "pair_counts": [
    {"shift": [0], "count": 2},
    {"shift": [1], "count": 1},
    {"shift": [4], "count": 1}
  ]
}
```

Each record contains exactly `shift` and `count`. A shift has one integer
coordinate per dimension, in `0,...,n_i-1`. Shifts must be unique; counts
are nonnegative integers. The count at displacement `s` means
`#{(a,b) in A×A : a-b=s}`, including both directions and the diagonal.
Missing bins mean **zero**, and explicit zero-count records are omitted
from the normalized target. This is complete displacement data, not a list
of measured bins with unmeasured values left unknown.

Let `k=C(0)`, taking an absent zero bin as zero. Validation requires
`k<=product(shape)`, total count `k²`, inversion symmetry `C(s)=C(-s)`,
counts at most `k`, and even counts at nonzero self-inverse displacements.
These are necessary conditions; an accepted target may still have no
binary realization. Empty input counts represent the empty arrangement.
Booleans and floating point values are not integer coordinates or counts.

The two included targets are [four sites in C12](examples/tetrachord-12.json)
and [eight sites in C16](examples/eight-sites-16.json). They are copied
byte-for-byte from the newly authored benchmark inputs. No saved result or
checkpoint is supplied as a substitute for running the search.

## Command-line use

Use Python 3.12 from the repository root. The solver and benchmark use only
the standard library; the original tests also import the repository's
immutable one-dimensional reference implementation.

```sh
python tools/inverse_grid/src/inverse_grid.py solve --input tools/inverse_grid/examples/tetrachord-12.json --out .reproduction/grid-result.json --checkpoint .reproduction/grid-state.json --max-nodes 100000 --timeout 10
python tools/inverse_grid/src/inverse_grid.py verify --input .reproduction/grid-result.json --recompute --max-nodes 100000 --timeout 10
```

Build a target directly from sites in two dimensions:

```sh
python tools/inverse_grid/src/inverse_grid.py target --shape 5,7 --points '0,0;1,2;3,4' --out .reproduction/grid-input.json
python tools/inverse_grid/src/inverse_grid.py solve --input .reproduction/grid-input.json --out .reproduction/grid-result-2d.json --max-nodes 100000 --timeout 10
```

To deliberately stop and then resume the same target:

```sh
python tools/inverse_grid/src/inverse_grid.py solve --input tools/inverse_grid/examples/eight-sites-16.json --out .reproduction/grid-partial.json --checkpoint .reproduction/grid-state-16.json --max-nodes 10 --timeout 10
python tools/inverse_grid/src/inverse_grid.py solve --input tools/inverse_grid/examples/eight-sites-16.json --out .reproduction/grid-result-16.json --checkpoint .reproduction/grid-state-16.json --resume .reproduction/grid-state-16.json --max-nodes 100000 --timeout 10
```

`solve` defaults to 1,000,000 nodes and 60 seconds per invocation. The node
budget counts newly expanded nodes on that invocation; `--max-solutions`
limits the cumulative number of found classes. Time limits are **soft**:
they are checked between node expansions, so a costly expansion can exceed
the requested seconds. Interruptions retain the unfinished branch for
resume. There is no polynomial worst-case bound, and dense support can make
the search impractical even on a small ambient grid.

## Results and completeness

The result schema is `homometry.grid-result/v1`. It embeds the normalized
`input`, input/solver SHA-256 identifiers, `equivalence`, `cardinality`,
`grid_sites`, `complete`, `termination`, sorted `solutions`, search `stats`
and a `checkpoint`. Each solution is a list of coordinate lists, sorted
and canonical under translation and simultaneous inversion of all axes.
Axis permutations, rotations, independent axis reflections and unit
multiplication are not additional equivalences.

`complete: true` means the search frontier is exhausted; a complete empty
solution list means no realization exists. Otherwise the termination is
`node_limit`, `time_limit`, `solution_limit` or `interrupted`, and the list
contains only the classes found so far. A successful process exit can
return a partial result: inspect `complete` and `termination`.

Ordinary `verify` checks input/result metadata and every listed class's
binary coordinates, canonical representative and literal pair counts.
It does not establish that no class was omitted. With `--recompute`, it
runs a fresh search; completeness is accepted only when the output field
`completeness_verified_by_fresh_replay` is true. A limited replay may
report `replay_complete: false` and cannot verify completeness.

Checkpoints use `homometry.grid-checkpoint/v1`. Their checksum detects
accidental edits, and resume requires the same normalized target and loaded
solver-source digest. These are trusted search states, not adversarial
proofs of exhaustive coverage: a self-consistent altered frontier can omit
work. Fresh complete replay is the route to checking a completeness claim.

## Python API and bounded checks

```python
import sys
sys.path.insert(0, "tools/inverse_grid/src")
from inverse_grid import Problem, solve, verify_result

problem = Problem.from_points([12], [[0], [1], [4], [6]])
result = solve(problem, max_nodes=100000, timeout=10)
check = verify_result(result, recompute=True, max_nodes=100000, timeout=10)
assert check["completeness_verified_by_fresh_replay"]
```

For JSON data use `Problem.read(document)`. `problem.document()` returns
the normalized JSON input. The API also accepts `max_solutions`, a saved
checkpoint as `resume`, and a progress callback. An unrestricted API call
with no limits can run for a long time.

Run the original, independent-review and benchmark-control tests:

```sh
python tools/inverse_grid/tests/test_inverse_grid.py
python tools/inverse_grid/tests/test_inverse_grid_review.py
python tools/inverse_grid/tests/test_inverse_grid_benchmark.py
python tools/inverse_grid/src/benchmark_inverse_grid.py --out .reproduction/grid-benchmarks --max-nodes 100000 --timeout 5
```

The repository's bounded verification wrapper includes the three test
programs in its disposable copy. The seven-case benchmark includes a
deliberate partial-search example. Its large-grid cases validate each
returned class and known sources; they are not independent large-grid
classification proofs or a promise of useful runtime for every target.

The solver's packaged SHA-256 is
`12a378c6f7a64ba7d85846771495a9e9ef96b562aee585eb482cdd1a345eda92`.
The benchmark's is
`bbd0e56eda541fde3d2a45f667a43cfcd22df89f075f43f29d9f1530f350fe17`.
Both sources and both example inputs are byte-identical to their origin
files. The original test's import of `homometry` is adapted to the
standalone repository's protected `src/`; all local tool imports and CLI
paths are preserved. Per-file origin and packaged hashes, sizes and this
adaptation and removal of an extra trailing blank line are recorded in the tool provenance file. The repository's
public manifest separately binds the complete authored package.
