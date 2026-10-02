# Direct prime Bloom parameter enumeration

**[COMPUTED]** This checkpoint enumerates all parameters `(a,b)` in each
prime field for the labelled configurations

```
X = (0, a, b-2a, 2b-2a, 2b, 3b-a)
Y = (0, a, b+2a, 2b-a, 2b+a, 3b-a).
```

It keeps six distinct residues on each side, rejects endpoints in the same
translation/reflection class, and counts unordered pairs after independent
T/I canonicalization of each endpoint. Unit multiplication does not identify
counted pairs. Every admissible parameter is retained in its exact pair fiber.
No formula or symmetry group is used by the enumeration algorithm.

## Reproduction and compute estimate

The pinned Python3.12 interpreter was used throughout. The immutable startup
reference suite passed10/10. Benchmarking primes13..43 completed before the
extension; p43 used1849 parameter candidates and0.009126 seconds. Scaling this
measurement suggested approximately5 seconds for the1018081 candidates at
p1009, with extra time for record construction and writing. The actual
p1009 enumeration/record construction took7.114707 seconds. No large complete
six-subset census was launched.

```
.venv/bin/python3.12 tests/run_tests.py
.venv/bin/python3.12 src/six_prime_bloom.py --primes 13..43 --out results/2026-09-30-six-prime-count
.venv/bin/python3.12 src/six_prime_bloom.py --primes 13..251 1009 --out results/2026-09-30-six-prime-count --resume
.venv/bin/python3.12 tests/test_six_prime_bloom.py > results/2026-09-30-six-prime-count/tests.log
```

Per-prime JSON checkpoints are written atomically, retain the implementation
source hash, and can be resumed only with the same schema and source hash.
`enumeration.log` retains progress within each run; `summary.json` and
`summary.csv` contain the requested50 primes. The test log records6/6 passing
groups, including replay of every saved parameter fiber.

## Observed results and exact scope

**[COMPUTED]** All50 checked primes (every prime13..251 and1009) have precisely
12 collision directions, no congruence exclusions among six-distinct
parameters, and fibers of size12. There are no non12 fibers in this sample.
The counts equal `(p-1)(p-11)/12` in this sample. This direct computation alone
does not prove the formula for arbitrary primes or prove prime Bloom
completeness.

| p | Bloom pairs | Admissible parameters | Colliding parameters |
|---|---:|---:|---:|
|13|2|24|145|
|17|8|96|193|
|19|12|144|217|
|23|22|264|265|
|31|50|600|361|
|131|1300|15600|1561|
|251|5000|60000|3001|
|1009|83832|1005984|12097|

The raw coefficient differences in each JSON record give all30 exact support
collision equations. Their12 primitive integer lines have coefficient pairs
`(0,1),(1,-3),(1,-2),(1,-1),(1,0),(1,1),(1,2),(2,-3),(2,-1),(2,1),(3,-2),(3,-1)`.
For p>=13 these correspond to excluded slopes b/a
`infinity,0,1,-1,2,-2,3,1/2,-1/2,3/2,1/3,2/3`. The code also preserves raw
differences before primitive normalization, so small-characteristic collapse
is checkable. Edge controls p=2,3,5,7,11 have no six-distinct parameters.

**[COMPUTED]** Every enumerated pair is present in the saved complete six-set
census wherever available (all tested primes through131). Those complete
censuses have additional non-Bloom pairs at17 (8 extra),19 (9 extra),23
(11 extra), and31 (20 extra). They agree exactly with the Bloom pair image at
the other tested primes through131. Each comparison records the complete
checkpoint hash and its advertised methods; it does not rerun those censuses.

## Independent checks

The gap-necklace canonicalizer is compared with all2p rigid images from
immutable `src/homometry.py` for all subsets at n=7,8, every Bloom parameter at
11,13,17,19,23, and all saved endpoints through43 plus deterministic larger
endpoint controls. The complete parameter-to-pair map, including every fiber,
is independently rebuilt with the immutable reference at p<=19. A fresh
reference six-subset census at13 agrees with the parameter image.

The tests independently verify the formal integer-vector difference identity,
all30 collision equations, explicit unit-multiplication controls, the
R=(-b,a-b), T=(b,a), -I parameter group against saved fibers, and the12
fractional collision slopes. All saved parameters are independently replayed
and all pair ICVs are recomputed with immutable `homometry.py`.

The second exact algebraic method and arbitrary-prime proof belong to the
parent task and are not claimed by this checkpoint.
