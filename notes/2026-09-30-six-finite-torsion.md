# The finite torsion branch: exact census and structural certificates

30 September 2026. **[PROVED], in-house, computer-assisted**, after the
separate attack in `2026-09-30-six-finite-torsion-review.md`.
No novelty claim. This note concerns cardinality six only.

## 1. Why this finite range matters

Reviewed Corollary C2 states that a cyclic six-pair with a full-rank signed
matching is, after independent anchors, an ordinary inflation of a pair
in Z_q for q<=135. The stronger free-rank results do not settle all
positive-rank presentations. Exhausting q<=135 therefore closes a specific
bounded torsion branch once all its families have verified generating
mechanisms. It cannot establish arbitrary-n completeness on its own.

The finite-generation theorem FT is: every six-note family in
Z_q, 6<=q<=135, is connected by classical Bloom, rigid templates R,
parallelogram-dyad D, L2 translation, L3 co-symmetric swap, L4 half-turn,
L5 block reflection, L6 unit multiplication, or L7 half-coset complement.
Consequently the same holds for every ordinary inflation of those pairs.
The exact count and independent replay result are recorded below.
Missing *direct* pair edges are retained; graph
connectivity allows compositions, as required by PQ1's definition.

## 2. Two independently implemented six-only enumerations

`src/six_large_census.c` has two separate traversals and interval kernels:

* **Gap/pair mode.** Enumerate all positive six-gap lists summing to n,
  with the first gap minimal. Keep exactly the lexicographically least
  gap word under all rotations and reversal. Its cumulative sums give
  the canonical pitch tuple. Count the fifteen unordered pair distances.
* **Point/correlation mode.** Enumerate every anchored point tuple
  `0<a1<...<a5<n`, with no gap pruning. Compare all twelve anchored rigid
  images as sorted point tuples. For each d, count memberships of x+d
  over the six input points, halving the antipodal entry when 2d=n.

Both modes keep T/I classes; neither identifies unit multiples. They share
only exact record storage and sorting. The sorted fifteen distances occupy
fifteen bytes in two 64-bit words; every distance is <=127 for n<=255.
The five nonzero points occupy five bytes. These encodings are injective,
and grouping uses both complete distance words, not a hash. Therefore
different ICVs cannot be merged by a collision in a hash function.

The two modes agree family-for-family and in total T/I class counts at
every n=12..135. They agree with the previous independent point/bit and
C-gap census at every n=12..60, and with the immutable reference in the
affordable small range (direct regression6..22, inherited full agreement
through24). Every emitted endpoint is also checked by the immutable
reference for canonical form and equal ICV. Additional regressions cover
31..33 and63..65 to attack representation boundaries.

Measured serial enumeration benchmarks, before extra endpoint checks:

| n | T/I six-classes | gap/pair seconds | point/correlation seconds |
|---:|---:|---:|---:|
|60|419,266|0.050|0.108|
|72|1,088,616|0.129|0.303|
|96|4,837,120|0.583|1.435|
|135|27,845,587|3.400|9.545|

Each modulus is an atomic JSON checkpoint with complete family endpoints,
ICVs, method timings and source hash. The two modes at135 require roughly
668 MB of live record payload each, run serially; allocation capacity can
be larger. No all-cardinality job was started or duplicated.

## 3. Exact mechanism discovery and independent replay

`src/six_pair_mechanisms.py` is independent of the inherited 64-bit strict
menu. It tests all modular Bloom parameters and the explicit R generator.
For other pairs it enumerates rigid alignments and **all** nonempty
subsets of their common block, not just their whole intersection: a moving
block can overlap its new position. A saved block certificate records the
alignment, fixed subset and translation or reflection parameter.

The sufficient group-ring conditions are exactly the previously proved
L2--L5 identities. D additionally checks its nonnegative periodic weight
decomposition through the reviewed implementation. Half-coset complements
test possible subgroup orders2,4,6,12: those are all possible even orders
because occupied cosets each contain half the subgroup, and total weight
is six. L6 records an actual unit fixing the autocorrelation.

`tests/test_six_pair_mechanisms.py` independently reconstructs each move
using integer Counters, checks endpoints with the immutable reference,
expands D's mixed-difference identity, and verifies each family is connected
by a union-find algorithm. The producer uses iterative graph reachability.
It also verifies that recorded certified and missing edges partition the
complete pair set with no omissions or duplicates. The old strict-menu
labels are not a dependency of this new coverage calculation.

## 4. Why ordinary inflation preserves these generators

The embedding Z_q -> Z_n for q|n sends x to (n/q)x. Group-ring identities,
disjointness, subgroup-periodic weights and half-coset complementation all
transfer along this injective homomorphism. A generating path thus embeds
edge by edge. Separate input anchors add only independent translations.

For L6 choose an ambient unit u' congruent to the original unit u modulo q.
Such a unit exists: keep the congruence modulo q and require u'=1 modulo
each prime dividing n but not q, using the Chinese remainder theorem.
Primes already dividing q cannot divide u', since u is a unit modulo q.
Then u' is a unit modulo n and acts on the embedded subgroup exactly as u.
An ambient T/I equivalence between two nonempty subsets of this subgroup,
both anchored there, must have its translation in the subgroup. Hence
inflation neither merges the original T/I classes nor breaks the paths.

Combining the fully checked finite generating table with C2 proves the
rank-ten branch for arbitrary n. It leaves positive free ranks one
and two with congruent free projections as a separate proof obligation.

## 5. Reproduction and current evidence

```bash
.venv/bin/python tests/test_six_large_census.py
.venv/bin/python src/six_large_census.py --nmin 6 --nmax 135 --resume
.venv/bin/python src/six_pair_mechanisms.py --nmin 12 --nmax 135 --resume
.venv/bin/python tests/test_six_pair_mechanisms.py --nmax 135
```

Outputs are in `results/2026-09-30-six-large-census/` and
`results/2026-09-30-six-pair-mechanisms/`; dated benchmark, regression and
replay logs are adjacent. Census files contain725,132 nontrivial families
and728,424 pair edges across12..135, with largest family size5 (the
classical31-note examples and their inflations). These are six-only
numbers. The inherited all-cardinality38..40 provisional status is unchanged.

The replay through135 is complete:725,132 families,728,424 pair edges,
73 missing direct edges, **zero disconnected families**. All728,351 direct
certificates pass the independent reconstruction. Their labels are:

| Mechanism | Certified edges |
|---|---:|
|D dyad|398,642|
|L3 swap|222,262|
|Bloom|59,211|
|L7 half-coset complement|18,018|
|L5 reflection|16,432|
|L4 half-turn|13,101|
|R rigid templates|561|
|L2 translation|79|
|L6 unit|45|

The aggregate replay is `results/2026-09-30-six-pair-mechanisms-review-135.json`.
The six-only census at6..11 has no nontrivial family, checked by both
traversals and the immutable reference. The separate adversarial review
accepted the finite/inflation bridge, additionally checking all130 class
counts by Burnside, explicit paths for all73 missing direct edges,
38,920 ambient-unit CRT lifts and27 inflation controls. Its reproduction
command is `.venv/bin/python tests/test_six_finite_torsion_review.py`.
No status is inferred from endpoint counts alone.
