# Fresh adversarial attack of the extended six-point manuscript

30 September 2026. Separate fresh-context reviewer from the manuscript
authors. **Accepted as an in-house computer-assisted exposition, with the
explicit computational trust stated below.** The final accepted source is
SHA256 `b5ad4f4748d943a5d35fd1995cc7a631475840dd4d1ddae711159abf119eb372`.
The reviewer may write this
note only; manuscript repairs belong to the root author.

## Scope and verification boundary

The attack reads the expanded mathematical arguments rather than accepting
the prior `[PROVED]` tags. Its targets are weighted normalization and the
exact real formula, integral presentations and lattice witnesses, the
fixed-free-alignment reduction, BF and HR covers, low-rank roots and quotient
DAG, torsion characters, specialization, the finite branch and path
inflation, D's nonnegative weights, the shadow/large-prime interfaces, and
the revised main theorem. The reference comparison checks the manuscript's
claim scopes against the new focused primary-reading note; this reviewer
does not represent that comparison as another independent reading of the
original sources.

Fresh computation is confined to inexpensive exact certificate replays and
controls. No census, solver, discovery search, installation, inherited report
rewrite, protected-file mutation, publication, or outside communication was
performed. The root supplied the passing startup baseline; this reviewer also
repeated `.venv/bin/python tests/run_tests.py`, with all10 tests passing. The exact real
UNSAT obligation U, the 3003-graph spanning-tree histogram, and the complete
six-only census/path table through135 are **not rerun by this attack**.
Those remain inherited, explicitly identified trusted computations. Fresh
finite replays do not discharge U or turn the proof into a Lean/kernel proof.

## Objections, attacks and dispositions

### 1. Weighted real-line normalization and exact formula

The diameter proof survives repeated endpoint atoms and repeated copies of
the diameter. Removing the labelled edge `(0,5)` leaves both `(0,4)` and
`(1,5)` and every remaining distance is bounded by one of them. Independent
reflections therefore put the same largest remaining distance at coordinate
four. Equal normalized lists would imply congruence; comparing their three
unshared interior coordinates supplies the lexicographic interchange.

The reflection exclusion tests all four interior positions of the sorted
lists. The edge-count constraints retain all15 labelled edges, including
zero; matching every A-support multiplicity uses all15 B occurrences and
prevents extra B-support values. Six diagonal zeros and twice the unordered
zero count give the corresponding directed weighted autocorrelation.

The displayed Cramer equations have the correct coefficients and characterize
the full real two-parameter plane. There is no rational-coordinate or bounded
parameter assumption. The weak-order gaps recover exactly the stated two
chambers, and the recovered unscaled parameters are integer differences for
integer coordinates. I requested that the initially implicit
noncongruence/gap argument be printed. The author added all four gap lists
and the first/reflected-first-gap comparisons, which include the allowed
repeated-coordinate boundary cases. **Disposition: repaired exposition; no
counterexample or remaining logical gap found.** U remains a solver premise.

### 2. Occurrence matchings and integral presentation

The occurrence lemma distinguishes two-element sign orbits, nonzero
involutions and zero. This prevents loss of multiplicities or either sign
at order-two differences. Anchoring creates the stated10 generators; the
first incidence block gives rank at least5, and the presentation maps to
every realization. Universal collisions and rigid equivalences transport to
every quotient.

Two-way integer products certify equality of relation lattices. Rational
row-space equality is correctly rejected as insufficient. The row-coordinate
map `z -> zV` in a unimodular diagonalization is the right quotient-coordinate
map. The torsion-minor proof uses incidence total unimodularity and the
triangle inequality in the ten-row Laplace expansion, without a common-sign
assumption. Cauchy--Binet supplies the Laplacian/tree-count identity. The
135 maximum is visibly a finite computation, not asserted as a purely
symbolic estimate. **Disposition: accepted conditional on its specified
finite histogram.**

### 3. Fixed free alignment and exhaustive height strata

Real congruence gives a finite set of sign/permutation/anchor subspaces.
The nonzero-polynomial argument proves the finite-union lemma over both R
and Q. Relabelling, inversion and reanchoring are unimodular, so a fixed
real alignment does not add integral relations or kill torsion. The
substituted anchored kernel has exactly dimension `d`; hence the height
span has rank `5-d`.

Differences of signed incidence roots give precisely the three printed
projective direction shapes. Content division occurs only in the rational
height enumeration. The induction extending representative spans is valid:
remove the last member of a direction basis, carry the lower span to its
representative, and use S6-invariance of the direction set. Generic integral
heights exist by excluding finitely many proper rational hyperplanes and
clearing denominators. **Disposition: accepted; fresh full low/high rank
height predicates pass.**

### 4. BF finite lifting and HR

I independently recomputed both15-element formal coefficient-distance
multisets, all exceptional ratios and their bin/sign factorials. They give
exactly `3,4,5` and `3/2,5/3`, with counts `128,16,4` and `128,4`.
Away from those ratios the formal coefficient matching is unique. Zero
bins retain all independent signs.

Fresh complete BF replay checks all282 matchings, all21 labelled integral
lattices, their two-way witnesses and all group-valued Bloom identities.
Collision outcomes cannot realize the assumed six-sets. This establishes
the group-valued parameter step; it does not infer that real parameters
lift without certificates.

For HR, finitely many labelled Bloom subspaces have dimension at most2,
so no such subspace contains a solution space of dimension at least3.
The union lemma forces a congruence alignment. Fresh replay covers all4176
rank-at-most-two spans,25 orbits and14475 matchings, including all17246
discard identities and four survivor master identities. The free determinant
and nonzero order-two element show the survivors generate the entire
`C2 + Z^3`, rather than a proper free sublattice. Thus the exclusions of
free ranks4 and5 are justified.

The new direct L3* simplification is algebraically correct: with fixed C,
moving dyad D and `s=p-2r`, `(C-P C*)(1+H)=0` gives `x^(-s) CD*=(CD*)*`.
I also verified this cross identity with exact formal coordinates in
`C2 + Z^3`. It requires no half of s and no global reflection. The earlier
global-reflection L5 description remains valid. **Disposition: accepted,
with U and the explicit finite-predicate trust retained.**

### 5. Low-rank quotient coverage, termination and cache maps

The root cover includes every nonzero projected signed matching and omits
no zero-edge completion: roots impose only actual cross-edge relations,
while subsequent quotient branches supply residual relations. Independent
source/target height-fiber relabellings preserve the chosen heights and
transport anchored integral presentations by unimodular maps.

Cancelling universal unsigned classes preserves multiplicity equality in
every full quotient. A chosen residual A occurrence must equal some
residual B class there. Choosing one representative per universal B class
is sufficient when both signs are tested. The full original presentation
retains the chosen real-height map, so the compatible sign is among the
branches even though the cyclic target has no nonzero map to R.

Quotienting cannot destroy a prior cancellation. Joining a previously
residual A class to a residual B class increases the cancelled multiplicity
by at least1; thus the residual multiplicity strictly decreases from at
most15. Cache keys are labelled integral lattices **within one fixed height
stratum**. Two-way root/child integer witnesses give the same quotient,
labels and height map. No cross-stratum height restriction is silently
introduced.

I requested explicit variable-row dimensions for node Smith witnesses,
because the foundation's15-row contract applies to full matchings, whereas
DAG nodes can have other row counts. The final integrated fragment explicitly
supplies those dimensions, cache locality and the upward-edge sign conversion.
Fresh full read-only structural replay checks all315 strata,
4822240 cross-bijections,328473 roots,10602 nodes,974 branches and658894
two-way lattice inclusions. All620 homometric terminals have been freshly
replayed against exact mechanism predicates. I read the entire final423-line
fragment and verified it is exactly inlined between the integration markers.
**Disposition: accepted; no structural counterexample or logical gap found.**

### 6. Torsion-character factorization

For a finite torsion group of exponent E, a cyclic image has order dividing
E and can be embedded in `C_E`. The listed coefficients `k_i E/d_i` exhaust
all such characters; normalization by the common gcd retains its actual
cyclic image. A homomorphism into `C_n` factors through that actual image,
which has order dividing n. No assertion `E | n` is needed. Free-generator
images remain arbitrary and may overlap the torsion image in the target.
Fresh terminal replay verifies all60 listed characters,44 forced collisions
and16 surviving mechanisms, as well as the independently produced atlas.
**Disposition: accepted.**

### 7. D, L7 and homomorphic specialization

I found one literal sign error in the Fourier eigenvalue: the printed
positive-exponent character and action `W(t-a)` give eigenvalue `chi_k(-a)`,
not `chi_k(a)`. I requested the two negative arguments. The annihilator
condition is identical, so this affects the accuracy of that sentence,
not the kernel theorem. The final source contains both negative arguments.
**Disposition of the literal sign error: repaired and rechecked.**

The Fourier kernel decomposition alone would fail to prove nonnegative
integer weights. The manuscript's component/intersection rectangle argument
supplies both missing properties: subtract a minimum integer row weight,
and the complementary weights are column minima. All H- and J-cosets in an
H+J-component meet, so the rectangle identities apply without missing
intersections. The mass formula is exact, and order-at-most12 follows from
nonnegative integral mass rather than an experimental cap.

The dyad-shape reverse construction recovers exactly four C-points. The
fixed-point parity condition and two-point orbit choices give the required
binary indicator. The theorem is explicitly limited to that exchange shape.
Under specialization a shared equal-sum dyad corner gives equal dyads;
surviving nontrivial images retain four distinct corners and fall under D.

The L7 coefficient proof uses the half-coset counts to prove equality of
both cross distributions. For specialization, subgroup order loss greater
than2 forces endpoint collisions; kernel size2 makes both endpoints equal.
Two source cosets merging makes a common full image coset. The printed
case split at subgroup orders2,4,6,12 then gives global rigid equivalence
or equality. Fresh controls verify150 order-loss and1448 merger cases,
without replacing the general argument by those checks. **Disposition:
accepted.**

### 8. Finite source paths, inflation and the main branch split

The mathematical finite-source reduction uses the cyclic image order,
not the whole possibly noncyclic torsion group. Its order is at most135,
and injectivity on each endpoint gives six distinct source points.

Ordinary subgroup inflation transports every group-ring condition and
combinatorial condition along an injective map. An ambient unit lifting a
source unit exists by CRT against the primes of n not already dividing q;
primes dividing q remain avoided because the source unit is invertible.
Autocorrelation is zero outside the subgroup and stays so under that unit.
An ambient rigid equivalence has translation in the subgroup by comparing
one matched point, so source T/I vertices do not merge.

The complete finite-family census and exact edge/path records are an
identified acceptance obligation. A list of counts or73 missing direct
edges alone would not suffice; the manuscript correctly permits paths.
This attack inspects the algorithms/interfaces but does not repeat the
135 census or complete path replay. The main proof must invoke the
original matching's rank and the full dual-space dichotomy; it does so in
the current integrated draft. I read the complete expanded finite enumeration,
Burnside, record schema, path and CRT arguments in the final integrated
fragment and rechecked the main proof's original-rank/projection case split.
**Disposition: accepted on those explicit finite premises; no omitted branch
or interface gap found.**

### 9. Integer shadows, large primes and R rigidity

Arbitrary integer lifts of modular B parameters produce distinct integer
terms because their residues are distinct. The Laurent identity gives
line homometry; an integer rigid equivalence would reduce to a forbidden
cyclic one. Conversely U and the integer recovery formulas give modular
B from any integer shadow. This exact n-squared modular test has no bound
on integer lift size.

I suggested removing the unnecessary generic-functional perturbation in
the large-prime proof. The author adopted the direct argument: torsion
image is trivial when all prime divisors exceed131; any integer lifts of
the free-basis images give a functional reducing to the original cyclic
map, and every within-endpoint difference has nonzero residue, hence
nonzero integer value. The sufficient131 boundary does not prove a prime
counting formula, and the manuscript says so.

The added R acceptance contract exhausts seed-compatible labelled matchings,
requires full-rank unimodular diagonal witnesses and checks the seed's
coordinate generator by unit congruences. I independently checked all13
printed rows for exact cyclic autocorrelation and all admissible divisor
orders. The root separately replayed all536 Smith witnesses; that current
replay is not claimed as this reviewer's execution.

The faithful non-shadow argument is independent of U: integer lifts give
one exhausted rank-ten matching, forcing all anchored integer coordinates
to zero. Faithful subgroup images reduce to seed lifts because anchoring
at residue0 makes their integer coordinates divisible by n/q, and a
nonzero integer inverse of the subgroup unit preserves homometry and
distinctness. Proper images are correctly excluded from this inference.
**Disposition: accepted.**

### 10. Classical attribution and scope

The focused reference note supplies read-source scopes for Family N's
exact endpoint formula and signed factor, the secondary Hosemann--Bagchi
attribution through Table1, Callender--Hall's block constructions and
Goyette's printed formulas. Its scan-product-label correction agrees with
the manuscript's algebraic orientation. Unread1954/1961 originals, thesis
and early Bloom sources are not promoted to direct proof dependencies.
Goyette's empirical criteria are explicitly qualified. No novelty,
disjoint normal forms, prime count or proof-assistant completeness is
inferred from these references. **Disposition: scope comparison passes in
the fixed final source.** An additional fresh read-only agent compared the
stable attributions/bibliography against both reference-audit notes and
found no required correction. That comparison was explicitly not represented
as independent primary-source verification. The final PG DOI wrapping and
bibliography font-size changes affect only typesetting.

## Fresh exact replay commands and actual results

All commands used the pinned `.venv/bin/python` from the project root.
They imported independent checker functions and printed results without
calling checker `main()` functions, which would overwrite saved reports.

1. `bloom_audit(Path('results/2026-09-30-six-bloom-cylinders.json'))` from
   `tests/test_six_cylinder_branches_review.py`: PASS,282 matchings,21
   lattices,210 inequivalent-lattice pairs,8460 row identities,19 Bloom
   outcomes and2 collision outcomes;0.081seconds.
2. `orbit_audit(Path('results/2026-09-30-six-free-rank'))` from the same
   checker: PASS,120 directions,4176 spans,25 orbits,14475 matchings,
   17246 row identities and4 master survivors;0.900seconds.
3. Read-only reproduction of `tests/test_six_free_rank_growth.py:main`,
   omitting only its output write: PASS,43770/116401 spans and104/211
   orbits, every generic height against all120 directions;2.369seconds.
4. Read-only loop over ranks3/4 orbit files, invoking `cross_audit` and
   `dag_audit` from `tests/test_six_free_dag_review.py` on every saved
   root/DAG package: PASS,315 strata,4822240 bijections,328473 roots,
   10602 nodes,974 branches,658894 inclusions;57.545seconds.
5. Read-only reproduction of the mechanism/character/atlas/control parts
   of `tests/test_six_low_rank_mechanisms_review.py:main`, omitting all
   report writes: PASS,620 terminals; direct labels481 D,71 L5,24 L3*,
   20 L4,14 B,1 L2 and9 character covers; all60 characters; independent
   builder atlas;150/1448 L7 controls;4.057seconds.
6. Separate exact rational slope/bin-factorial derivation from the two
   printed coefficient lists; formal HR cross-identity check in
   `C2 + Z^3`; exact13-row R autocorrelation/divisor-order check: PASS.
   The first R-table extraction pattern omitted the LaTeX math delimiters
   and rejected its expected row count; correcting the parser produced
   the stated complete13-row check. This was not a mathematical failure.

The full command bodies and tool outputs remain in the current task
transcript. The actual complete LR structural command was:

```sh
.venv/bin/python - <<'PY'
import sys,json,time
from pathlib import Path
from collections import Counter
sys.path.insert(0,'tests')
from test_six_free_dag_review import read,cross_audit,dag_audit
base=Path('results/2026-09-30-six-free-dag-all'); totals=Counter(); terms=Counter(); start=time.monotonic(); strata=0
for rank in (3,4):
 saved=json.loads(Path(f'results/2026-09-30-six-free-rank/rank{rank}-orbits.json').read_text())
 for orbit in saved['orbits']:
  stem=f'rank{rank}-orbit{orbit["index"]:03}'
  data=read(base/f'{stem}.json.gz'); assert data['heights']==orbit['heights']
  matrices,total=cross_audit(orbit['heights'],read(base/f'{stem}-cross.json.gz'))
  r=dag_audit(orbit['heights'],data,matrices)
  totals['cross_bijections']+=total
  for k in ('nodes','roots','branches','lattice_inclusions'):totals[k]+=r[k]
  terms.update(r['terminals']);strata+=1
print('FULL READ-ONLY LR STRUCTURAL REPLAY',strata,dict(totals),dict(terms),'seconds',round(time.monotonic()-start,3))
assert strata==315
PY
```

The actual complete terminal/character/atlas/L7 command was:

```sh
.venv/bin/python - <<'PY'
import sys,json,gzip,time
from pathlib import Path
from collections import Counter
sys.path.insert(0,'tests')
from test_six_low_rank_mechanisms_review import mechanism,characters,builder_atlas,halfcoset_degeneration_controls
base=Path('results/2026-09-30-six-free-dag-all'); start=time.monotonic()
saved=json.loads(Path('results/2026-09-30-six-low-rank-review/exploratory-mechanisms.json').read_text()); indexed={(r['rank'],r['orbit'],r['node']):r for r in saved['rows']}; assert len(indexed)==len(saved['rows'])
summary=json.loads((base/'summary.json').read_text());expected={}
for s in summary['strata']:
 with gzip.open(base/f'rank{s["rank"]}-orbit{s["orbit"]:03}.json.gz','rt') as f:dag=json.load(f)
 assert dag['complete']
 for node in dag['nodes']:
  if node.get('terminal')=='homometric':expected[(s['rank'],s['orbit'],node['id'])]=node
assert set(indexed)==set(expected) and len(expected)==620
hist=Counter();qh=Counter()
for key,rec in expected.items():
 row=indexed[key]
 if row['mechanism']:hist[mechanism(rec,row['mechanism'])]+=1
 else:hist['cyclic-character-cover']+=1;qh.update(characters(rec,row['cyclic_cover']))
assert hist==Counter({'D-dyad':481,'L5-reflect':71,'L3star-cosymmetric':24,'L4-halfturn':20,'Bloom':14,'L2-translate':1,'cyclic-character-cover':9})
assert qh==Counter({'collision':44,'D-dyad':16})
print('FULL READ-ONLY LR TERMINAL REPLAY',len(expected),dict(hist),dict(qh))
print('BUILDER ATLAS',builder_atlas(expected))
print('L7 CONTROLS',halfcoset_degeneration_controls())
print('seconds',round(time.monotonic()-start,3))
PY
```

The other fresh complete replay commands were:

```sh
.venv/bin/python - <<'PY'
import sys
sys.path.insert(0,'tests')
from test_six_cylinder_branches_review import bloom_audit
from pathlib import Path
print(bloom_audit(Path('results/2026-09-30-six-bloom-cylinders.json')))
PY
```

```sh
.venv/bin/python - <<'PY'
import sys
sys.path.insert(0,'tests')
from test_six_cylinder_branches_review import orbit_audit
from pathlib import Path
r=orbit_audit(Path('results/2026-09-30-six-free-rank'))
print({k:v for k,v in r.items() if k!='survivors'})
print('survivors',r['survivors'])
PY
```

```sh
.venv/bin/python - <<'PY'
from itertools import combinations
from collections import Counter
from math import factorial
from pathlib import Path
import sys,json,time
sys.path.insert(0,'tests')
from test_six_free_rank_growth import exterior,actions,act,independent,directions
base=Path('results/2026-09-30-six-free-rank');previous=json.loads((base/'spans.json').read_text())['orbits'];started=time.monotonic()
for rank in (3,4):
 saved=json.loads((base/f'rank{rank}-orbits.json').read_text());covered=set();maps=actions(rank)
 for orbit in saved['orbits']:
  seed=exterior(orbit['rows']);assert seed
  group={act(seed,a) for a in maps};assert len(group)==orbit['size'] and not group&covered;covered|=group
  h=orbit['heights'];assert not any(sum(x*y for x,y in zip(row,h)) for row in orbit['rows'])
  counts=Counter(abs(h[j]-h[i]) for i,j in combinations(range(6),2));number=1
  for distance,count in counts.items():number*=factorial(count)*(2**count if distance==0 else 1)
  assert number==orbit['matching_count'] and sorted(Counter(h).values())==orbit['height_multiplicities']
  for d in directions():
   belongs=len(independent.rational_pivots(orbit['rows']+[list(d)]))==rank
   assert (sum(x*y for x,y in zip(d,h))==0)==belongs
 candidates={exterior(row['rows']+[list(d)]) for row in previous if len(row['rows'])==rank-1 for d in directions()};candidates.discard(())
 assert candidates<=covered and len(candidates)==saved['extension_candidates']
 for orbit in saved['orbits']:
  seed=exterior(orbit['rows']);assert any(act(seed,a) in candidates for a in maps)
 assert len(covered)==saved['spans']
 print('FULL READ-ONLY HEIGHT-GROWTH REPLAY',rank,'spans',len(covered),'orbits',len(saved['orbits']))
 previous=saved['orbits']
print('seconds',round(time.monotonic()-started,3))
PY
```

## Final verdict and exact source binding

The root first froze source SHA256
`3fa72859aedcfd9f99d25e10f23f4e4423d8af60c928441b7f9110b6c0d150ba`.
It then reported typographic repairs for the L3* bookmark and PG DOI
wrapping (SHA256 `79df46c108fa00346204b62ec92926dd947c04c4c835591d6a0b1a3930f25387`),
followed by a smaller bibliography font to avoid an orphan page.
I independently read and hashed the final source, confirmed the LR fragment
is exactly inlined, and checked the prior precision repairs and bibliography
scope at SHA256
`b5ad4f4748d943a5d35fd1995cc7a631475840dd4d1ddae711159abf119eb372`.
The final source passes this substantive mathematical attack.

The expanded proof gives explicit mathematical reductions and finite
acceptance predicates instead of relying on reported totals or earlier
status tags. No counterexample or remaining logical gap was found within
those premises. The claim is a complete generating grammar with
compositions, retaining T/I classes and arbitrary modulus; it is not a
disjoint/minimal normal-form classification or a prime counting theorem.

Acceptance remains acceptance of an **in-house computer-assisted proof**.
This attack personally reran the complete BF, HR, low-rank height, root/DAG,
terminal and character predicates. U and the full135 census/path table were
not rerun here and remain inherited disclosed dependencies. The root
separately reran the complete spanning-tree histogram by both methods and R
Smith witnesses; those runs are not attributed to this reviewer. No full
Lean/external proof-kernel verification, novelty determination or external
specialist approval follows from the review.

The following hashes bind the exact sources and saved input sets inspected
or replayed by this reviewer. An aggregate input-set digest is SHA256 of
the UTF-8 manifest whose lines are `relative_path<TAB>file_sha256<LF>`,
sorted by relative path; it is not a digest of guessed headline totals.

### Individually bound sources

```text
notes/2026-09-30-six-paper.tex	b5ad4f4748d943a5d35fd1995cc7a631475840dd4d1ddae711159abf119eb372
notes/2026-09-30-six-formal-algebra.tex	c96d0a9a0f6406b8d082421adb8b95224435092c7cb8592873e52ff23541378c
notes/2026-09-30-six-formal-foundations.tex	76de14bc57404dab0890185ba870fa97074f73a974c2c2923948feea14013bff
notes/2026-09-30-six-formal-low-rank.tex	299fb3b0f22eff0c56f3244ac18569f35a22efa43bcb651e578cd87e7b82d693
notes/2026-09-30-six-formal-references.md	b775b2ce2c0d4a21a45bc373f480363b5129dea22937ae52fab69f85a85f19d8
notes/2026-09-30-six-paper-references.md	1cdda73a579b0978c48cfd83eb8ad57880639445fe8fda9b41c641bea27d2be3
notes/2026-09-30-six-integer-theorem.md	6497f7031456504904a94379829c96232f1669605f6ea08eba6b17b37c1100f5
notes/2026-09-30-six-integer-review.md	4784c03c5227b634b58de8be78a874867b30c85f007047e1200295b4045c7b82
notes/2026-09-30-six-free-dag.md	512d5375844ecb81171bb35fe18837f350ce4d7b8a07bb92e5efd307ed672462
notes/2026-09-30-six-finite-torsion.md	6df160feb72b11c78fa71151db81cba2be41a5e302e675c2cc024b88a1bde40a
src/six_free_dag.py	655b1bed99c4ecff8dfcffd3c26db6011af36fb905ac53a7c57785a6999ec828
src/six_large_census.c	7a227e2d6aabd0f4fa99fe370f962269a5cba936fcddfb55e6a2e7029e88ecf6
src/homometry.py	520a929aff08f5d9eb7d59977e495ac9fdcb80ff90045493cfb72abe85cff0d6
tests/run_tests.py	951d14fe5ead93338a949d95412f51b658fe36d34bf4cd2b0032a8dc85545aa5
tests/test_six_cylinder_branches_review.py	90d3e84b8ad2eee653d166dad920abe8b99666c5c6db7bccc32f792f6d7a9402
tests/test_six_free_rank_growth.py	313f52529fb37a0426cb64cc0279558b44d048fc2ecf22ac127d65ff31438573
tests/test_six_free_dag_review.py	4b70ebf9c1613590e382fc34269009aaa0ad10735b16da4e9ddedbefbb7fe20d
tests/test_six_low_rank_mechanisms_review.py	6a1b1e2bcf0fab8b10f46b1a87a24e69cfb07ee503030645e7760cd90ad2d734
tests/test_six_shadow_review.py	a1bae86abb7208b5488bd8d6dff1cbf5d3bd3eb4bbd78cb62134936f90eef734
tests/test_six_free_rank.py	e30a1ea51f79dc9a32c1c09131748c2a35e6d62a97d784aadf42ad8479a5c12d
tests/test_six_pair_mechanisms.py	5b4569cd45b97c1c7375394bb5670f05a1357c9f79deed966d2901f10cfac78a
```

### Complete replay input-set digests

| Input set | File count | Aggregate SHA256 |
|---|---:|---|
| BF | 1 | `5ba7461d628a1e730ef5545aea05fcb36403712b8111fc285df210f240663253` |
| HR | 27 | `56e572abc3372661a754b6d3a5b4982093aa52a1821c703f66ba8afe54bce30a` |
| LR-height | 2 | `2695308b102761765550936e2a4af7f503060e9c6d6ca0e280c5759ad1510c88` |
| LR-root-DAG | 631 | `747a1c5762271aba658f0b9673b71f1bbd3caba7b4f6fd35f4f7b9584bd18c89` |
| LR-terminal | 2 | `67a939cb85348628c8cce7f54037493ca13b8780df53685dac62e9e2c10c310a` |
