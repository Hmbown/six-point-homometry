# Exact-grid inverse tool: measured examples

1 October2026. **[COMPUTED] local measurements.** The new
[tool](../tools/inverse_grid/README.md) accepts exact directed pair counts
on products of cyclic groups and recovers binary arrangements, up to
translation and simultaneous global inversion. It supports arbitrary
cardinality through finite search and does not allocate the whole grid.
The [full proof](general_matching/INVERSE_GRID.md) and
[separate adversarial review](general_matching/INVERSE_GRID_REVIEW.md)
state its completeness and interruption contract.

| Input | Occupied sites | Ambient sites | Search nodes | Classes found | Completed | Local seconds |
|---|---:|---:|---:|---:|---|---:|
| Four-site Z12 ambiguity |4|12|54|2|Yes|0.002|
| Eight-site Z16 example |8|16|1509|2|Yes|0.076|
| Classical Bloom pair on a large circle |6|1000000007|589|2|Yes|0.042|
| Same pair embedded along one axis of a3D grid |6|about10^27|589|2|Yes|0.050|
| Seeded sparse circle |10|1000000007|313|1|Yes|0.066|
| Seeded generic3D coordinates |12|about10^27|471|1|Yes|0.190|
| Deliberately limited Z31 search |15|31|100|0|Partial|0.020|

The first two counts match independent exhaustive raw-subset enumeration.
The classical cases match two explicit known classes and bounded independent
tests. The seeded larger examples have independent literal pair-count
validation and include their known source arrangements; they do not have a
second exhaustive large-grid classification. Full proof correctness remains
the basis for the solver's general completeness statement. These timings
are specific to this machine and input, not a worst-case performance promise.

The last row illustrates the output contract: zero classes found during
a partial search does not mean the target has no realizations. Resume the
saved state or run a fresh complete search before asserting completeness.
Checkpoints are trusted state with corruption checks; deliberately altered
states are not mathematical completeness certificates.

Reproduce all examples from the math repository root, without installing
any packages:

```sh
python -S tools/inverse_grid/src/benchmark_inverse_grid.py --out .reproduction/inverse-grid-benchmarks --max-nodes 100000 --timeout 5
```

The fixed seed is20261001. The driver saves every input, result, checkpoint
and a machine-readable summary, validates every answer by separate literal
coordinate arithmetic, and performs the independent small-case enumeration.
Search can still grow exponentially for dense or highly ambiguous inputs;
time limits are soft and checked between nodes. Noise, weights and
continuous coordinates remain outside this exact binary interface.
