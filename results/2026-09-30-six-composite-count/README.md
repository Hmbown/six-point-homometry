# Direct composite Bloom parameter certificates

30 September 2026. **[COMPUTED]**, covered by the dedicated tests below.
This is the image of the classical two-parameter Bloom construction in cyclic
Z_n. It is not a census of arbitrary six-subsets or maximal homometry families,
and finite agreement alone is not a proof of a general composite formula.
The separate algebraic/permutation review belongs to the main task.

Every one of the n² labelled parameter values is evaluated directly. The
endpoint canonicalizer compares anchored point tuples, with a smallest-gap
pruning that retains all ties and both orientations. No moment key, formula,
parameter orbit, CRT identification or general unit quotient groups the
images. The exact fibres are subsequently compared with the twelve formal
parameter symmetries G. Rigid equivalence permits independent translations
and reflections of the two endpoints and endpoint interchange.

| n | factorization | excluded support collisions | congruent endpoints | full pairs | unit-separated pairs |
|---:|:---|---:|---:|---:|---:|
| 169 | 13² | 2,017 | 0 | 2,212 | 338 |
| 221 | 13·17 | 2,641 | 0 | 3,850 | 192 |
| 247 | 13·19 | 2,953 | 0 | 4,838 | 288 |
| 289 | 17² | 3,457 | 0 | 6,672 | 2,312 |
| 323 | 17·19 | 3,865 | 0 | 8,372 | 1,152 |
| 361 | 19² | 4,321 | 0 | 10,500 | 4,332 |
| 403 | 13·31 | 4,825 | 0 | 13,132 | 1,200 |
| 529 | 23² | 6,337 | 0 | 22,792 | 11,638 |
| 637 | 7²·13 | 7,609 | 0 | 33,180 | 0 |
| 961 | 31² | 11,521 | 0 | 76,000 | 48,050 |
| 2,197 | 13³ | 26,353 | 0 | 400,038 | 57,122 |

**[COMPUTED]** In all eleven cases every full fibre is exactly one G-orbit
of size twelve. All unit-separated graphs are disjoint unions of edges.
For the original nine full loci the same is true. Each added control at403
and961 has one five-vertex component, with each vertex of degree two, and
the remaining components are single edges. These five-cycles are exactly
the31 boundary endpoints inflated by13 and31, respectively. This
graph concerns Bloom edges alone, without asserting absence of homometric
partners from other constructions. The characteristic31 shared-endpoint
boundary is retained by a dedicated n31 test.

Here **unit-separated** means that both labelled endpoint lists have six
distinct reductions modulo *every* prime factor p of n. This is stronger
than gcd(a,b,n)=1. The candidate unit-separated count

    (1/12) product over p^k || n of p^(2k-2)(p-1)(p-11)

agrees in all ten tested cases whose prime factors are at least thirteen.
It is recorded as a comparison after direct enumeration; it does not drive
the algorithm. At637 the factor7 forces that subset to be empty; the
displayed candidate is not applied there.

The full counts at the ten large-prime cases also equal
`(n-1)(n-11)/12`, as a finite observation. At637 that expression is33178,
whereas the actual full count is33180. This small-prime correction remains
in the data instead of being absorbed into a changed definition.

Every leftover fibre is retained. `local_support_strata` gives parameter
categories, exact pair counts, fibre-size and G-orbit-count histograms for
each unordered endpoint support-size profile at the prime factors. For
example the four mod13 strata at2197 have support sizes `(1,1)`, `(4,4)`,
`(5,5)`, `(6,6)` and2212,85176,255528,57122 pairs, respectively.

## Certificate format and reproduction

The compressed `nN.json.gz` public certificates retain canonical endpoints,
all fibres and both excluded parameter lists. A parameter is stored as
`code=a*n+b`; recover it by `a=code//n`, `b=code%n`. Each fibre also records
its local support-size profile. Every parameter appears exactly once in
an excluded list or an admissible fibre. Source/reference SHA256 digests
are bound into each certificate. `summary.json` collects all summaries.

```bash
.venv/bin/python src/six_composite_bloom.py --moduli 169 221 289 247 323 361 529 637 2197 403 961 --out results/2026-09-30-six-composite-count --resume
.venv/bin/python tests/test_six_composite_bloom.py > results/2026-09-30-six-composite-count/tests-final.log
```

The tests compare every endpoint canonicalization and the complete
parameter image against immutable `src/homometry.py` for every2≤n≤43.
Larger enumerated certificates have spread-out reference canonical/ICV
controls, and the test audit checks every saved fibre representative,
exact G-orbit partition and every parameter's unique location. All
excluded parameters are replayed at small moduli and sampled at larger
ones. Tests also cover integer directed-difference equality, local support
definition, the retained n221 CRT-sign/moment counterexample, resumable
checkpoints with source-digest rejection and n31 shared endpoints.

The source cap is ten million parameter candidates. The benchmark at169,
221,289 took0.146,0.247,0.439 seconds of direct enumeration. The2197
extension took32.617 seconds of direct enumeration and43.30 seconds total
(including audit/export and prior certificate reads), with587,300,864 bytes
maximum resident memory and zero swaps. Progress is logged at five-second
intervals during enumeration. A source-bound checkpoint was written at
row1389 and removed after the public certificate completed. Checkpoint
continuation is independently exercised by the regression test.
All eleven public certificates together occupy35,740,244 bytes. The added
403/961 controls take1.454/6.486 seconds of direct enumeration; the whole
control command takes11.67 seconds including prior-certificate reads,
audit and export. Reusing a large public JSON certificate transiently
loads its full fibres; this replay peaks at965,312,512 bytes, with zero
swaps. Fresh direct2197 enumeration has the lower peak reported above.
Exact
progress/resource records: `enumeration.log`, `extension.log`,
`resources.log`, `characteristic31-controls.log`,
`characteristic31-resources.log`; test records: `tests.log`, `tests-final.log`.
The final eight-group audit streams certificate records, passes in15.05
seconds and peaks at36,749,312 resident bytes with zero swaps; its resource
record is `tests-resources.log`.

The general algebraic classification, singular cases beyond these moduli,
and independence of the headline counts are obligations of the separate
proof/review work. No novelty or complete composite six-point census is
claimed by this enumerator.
