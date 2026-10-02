# Six-note inventory and computational boundary

## Current closure, 30 September 2026

**[PROVED], in-house, computer-assisted:** Theorem G now supplies the complete arbitrary-n six-note generating grammar; see `2026-09-30-six-generation.md` and its separate review. Integer six-pairs, including repeated distances, are classified by I/Iw, so modular Bloom membership is exactly the shadow criterion. The two-method six-only census extends to135; all725,132 nontrivial families are connected, with73 indirect pair paths supplied by compositions. Full finite certificates and review are in `2026-09-30-six-finite-torsion.md`; arbitrary-n use is documented in `2026-09-30-six-generate.md`. The inventory below is the historical initial restricted-menu pass: its missed families and then-open statements are superseded by these results, not evidence of current gaps or sporadicity. The inherited factor-menu caps and all-cardinality audit limitations remain in force.

## Historical initial inventory

30 September 2026, PQ1/P3. [COMPUTED] census; restricted coverage labels
remain [COMPUTED-UNVALIDATED] until independently re-enumerated. No
six-note completeness or novelty claim follows from this inventory.

## Scope and independent enumeration

`src/six_census.py` studies only six-subsets. Its new point method anchors
one note at zero, compares all twelve anchored rigid images, and computes
interval content by exact bit correlations. The independent existing C
method enumerates positive cyclic gaps and counts unordered pair distances.
Their complete family payloads agree at every n=12..60. The immutable
reference agrees at n=6..24 (6..18 also in the regression test); inherited
saved six-note slices agree at n=12..32 where available. Set classes are
T/I bracelets throughout. Units do not identify distinct bracelets.

At n=60 there are 4,466 six-note Z-families and 4,486 pair edges, with
largest family size three. The point pass took 1.266 seconds and the C pass
0.115 seconds in the saved run. This says nothing about all-cardinality
M(60). All-cardinality n=38..40 remains single-method and provisional.

Full payloads: `results/2026-09-30-six-census/n{12..60}.json` and
`summary.csv`. Each payload has exact representatives, ICVs, method names,
timings and source hash. Atomic per-n checkpoints support resumption.

## Mechanisms retained as distinct explanations

| Mechanism | Conditions / certificate | Evidence boundary |
|---|---|---|
| Classical complementation | six of twelve notes; exact complementary representatives | Explains all 15 n=12 pairs; inherited reviewed result |
| Classical integer family | Bloom parameters p,q; signed four-term factor flip with cancellation; two lists distinct and T/I distinct | Explicit integer shadows; no claim that repeated-distance integer six-pairs are exhausted |
| Strict inherited moves | endpoints plus label L2/L3/L4/L5/L6/L7/L8/L9; proofs in P2/P3 notes | New strict pass is one coverage implementation; excludes dense-complement direct products |
| Complement-conjugated swap | exact inherited n=21 certificate | Structural composition, distinct from an integer lift |
| Integral cyclic factor flip | full inherited coefficient certificate where present | Does not imply an integer homometric lift; signed/heightful menu complete only through weight six |
| Quotient lift | subgroup, quotient residual and integral lift certificate | Soundness reviewed; the broad distribution counts retain inherited limitations |
| Difference-set exchange | exact n=21 Z_3 x Z_7 certificate | Benchmark explanation; does not classify arbitrary six-note families |
| Parallelogram-dyad shell | shared C of size four, exchanged corners 0,a+b / a,b, periodic weights and reflection choices | New exact shape theorem is in the separate proof/review; h=6 gives an arbitrary-n parametric mechanism |
| Ordinary inflation | d divides n, multiply each residue by n/d | Preserves six notes; keep source division and T/I representatives |
| Integer-shadow decision | all compatible signed edge matchings; exact integer-kernel reduction / Smith divisibility | One failed matching or bounded lift is insufficient; capped runs explicitly undecided |

`src/six_inventory.py` combines exact six-note family lists with inherited
menu fields/certificates and a restricted strict-move pass. The `cZ` and
`cQ` fields are inherited table labels, not independently established
unrestricted minimum factor weights. Old historical "unimplemented" QL
remarks are superseded by the 29 September QL review. The six-note notes
do not reopen the global kappa defect or the classical closure of C3.

`src/six_explore.py` stores a Bloom certificate per generated edge and
records all missed pair edges. Edges can carry several explanations;
"shadow" is a pair property, not a label assigned to an entire maximal
ICV family. The known n=21 benchmark is retained even when other menus
already explain it.

## Selected counts and residues

The first two numerical columns below are independently checked census
counts [COMPUTED]. The last column is explicitly menu-relative,
[COMPUTED-UNVALIDATED], and is not a count of proved sporadics.

| n | Six-note families | Pair edges | Families disconnected by restricted strict + Bloom |
|---:|---:|---:|---:|
| 12 | 15 | 15 | 0 |
| 17 | 16 | 16 | 8 |
| 18 | 62 | 74 | 3 |
| 19 | 21 | 21 | 9 |
| 21 | 96 | 96 | 13 |
| 23 | 33 | 33 | 11 |
| 24 | 275 | 300 | 7 |
| 27 | 183 | 189 | 18 |
| 28 | 327 | 333 | 6 |
| 30 | 428 | 436 | 14 |
| 31 | 61 | 70 | 15 |
| 36 | 1,012 | 1,036 | 6 |
| 60 | 4,466 | 4,486 | 20 |

The h=6 shell has exact certificates for all three named n=18 residues,
including

    {0,1,4,6,10,13} / {0,1,4,7,9,13}.

It also generates

    {0,1,5,8,13,17} / {0,1,5,9,12,17} in Z_24,

and non-inflated instances at n=30,36,42,48,54,60. Full parameters and
periodic vectors are in `results/2026-09-30-six-shell/nN.json`. Recognition
tries every separate rigid alignment of the two classes; it does not
replace T/I by affine equivalence.

## Failed approaches and the mathematical next step

1. A 0/1 direct-sum 2-by-3 flip is rigidly trivial: the two-point factor
   is a translate of its reversal. This cannot generate genuine six-pairs.
2. Bloom-only generation fails already at n=17. The pair
   `{0,1,3,8,12,14}/{0,1,4,6,12,14}` is an exact counterexample to that
   menu. It has 192 compatible signed matchings; all have rank ten.
3. Adding the inherited strict moves and the complete parallelogram-dyad
   shape still does not cover that pair: none of its rigid alignments has
   the required shape. Thus a finite successful menu in a few divisions
   is not a proof of the six-note agenda.

The response is to study the obstruction itself, not rename these gaps
"sporadic". The separate proof gives a universal 252 determinant bound
and an integer lifting theorem for moduli whose prime factors exceed 251.
The remaining task is to classify actual nondegenerate matching lattices
with small torsion, and the integer six-point pairs with repeated lengths.

## Reproduction

Use the pinned environment; the default NumPy mutation defect remains a
known inherited issue. No protected reference/data file was edited.

```bash
.venv/bin/python tests/test_env.py
.venv/bin/python tests/run_tests.py
.venv/bin/python tests/test_six_census.py
.venv/bin/python src/six_census.py --nmin 12 --nmax 32 --reference-max 24 --compare-inherited
.venv/bin/python src/six_census.py --nmin 12 --nmax 60 --reference-max 24 --compare-inherited --resume
.venv/bin/python src/six_explore.py
.venv/bin/python src/six_inventory.py --nmin 12 --nmax 60
.venv/bin/python tests/test_six_structure.py
.venv/bin/python src/six_shell.py --nmin 12 --nmax 60
```

The shape proof, exact negative shadow certificates and their separate
audit are checkpointed in the subsequent mathematical task. Their status
must be read from the completed review, not inferred from this inventory.
