# Exact global Bloom matching certificates

Started 30 September2026; completed1 October2026. **[COMPUTED]** exact
finite tables with independent complete audits and immutable-reference
controls. The global classification/graph theorems are **[PROVED], in-house,
computer-assisted, after the separate fresh review**. No novelty claim and no
all-cardinality or all-six-subset census.

The proof is `notes/2026-09-30-six-composite-global-matrix.md`. The table
classifies all possible label matchings over every modulus, rather than
testing a finite list of moduli. It uses integer linear equations only.

| Finite matching problem | Cases | Residual ranks0/1/2 |
|---|---:|---:|
|Unordered endpoint pair, independent signs and permutations|4,147,200|12/864/4,146,324|
|One shared endpoint, both source/target choices|5,760|24/432/5,304|

Every rank-one residual is an exact support collision. Every rank-two
minor gcd has at most one prime≥5 and that prime has valuation one.
The paired prime set is5/7/13/19; the single-endpoint set adds11/31.
These statements allow the proof to reduce every nonformal global
matching to a single order-p subgroup, including moduli with several
prime factors and repeated prime powers.

Files:

- `matching-certificate.json`: all39 rank-one histogram entries,
  all46 rank-two histogram entries, all12 rank-zero systems and all48
  full systems exceptional at primes≥11. The auxiliary G-row containment
  witnesses for those48 are verified but unnecessary to the final proof.
- `endpoint-certificate.json`: all39 rank-one histogram entries,
  all29 rank-two histogram entries, all24 rank-zero systems, all432
  rank-one systems and all384 systems exceptional at primes≥11.
- `independent-audit.json`: independently exhaustive Y-pivot paired
  enumeration, and original6×4 determinant-minor single-endpoint
  enumeration; exact agreement and current certificate hashes.
- `field31-graph.json`: all five cycle classes/edges and component counts
  for the field31 Bloom graph, independently rebuilt with immutable
  reference T/I canonicalization and compared with the inherited full
  direct parameter-image certificate.
- `benchmark.json`, `benchmark-log.txt`: first72,000-case timing before
  the complete run; approximately0.011seconds and under one second for
  the full C++ run. The benchmark is explicitly incomplete.
- `enumeration-log.txt`, `endpoint-log.txt`, `independent-log.txt`:
  complete-run logs.
- `provenance.json`: SHA256 hashes of source, test, proof and outputs.

Reproduce from the project root with the pinned Python environment:

```bash
clang++ -O3 -std=c++17 src/six_composite_matching.cpp -o results/2026-09-30-six-composite-global-matrix/matching-enumerator
results/2026-09-30-six-composite-global-matrix/matching-enumerator --out results/2026-09-30-six-composite-global-matrix/matching-certificate.json
results/2026-09-30-six-composite-global-matrix/matching-enumerator --endpoint --out results/2026-09-30-six-composite-global-matrix/endpoint-certificate.json
.venv/bin/python tests/test_six_composite_matching.py --full
```

The default test command checks every retained witness, every exceptional
actual-support field solution with `src/homometry.py`, every one of the
5,760 original endpoint systems, and a Y-pivot paired benchmark. `--full`
adds all4,147,200 paired systems. The full independent audit takes about
five seconds. Safe coefficient bounds are far below signed int64 limits.

The proof uses the accepted prime/field pair and unique-partner theorems
only at13/19 and the independently attacked odd support-count lemma for
its exact coprime6 count. Every remaining proof obligation and status
scope is stated in the note. Fresh review output is owned separately at
`notes/2026-09-30-six-composite-global-review.md`.
