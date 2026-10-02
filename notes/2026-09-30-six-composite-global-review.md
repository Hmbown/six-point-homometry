# Independent attack of the proposed full composite Bloom classification

Started30 September, completed1 October2026. **Fresh review complete; accepted
scopes are stated below.** This is separate
from the frozen accepted partial review and owns only this note. The
arbitrary-global-Omega theorem is not assumed from authors' messages.

## Plan

- Read both complete proposed global proofs and their exact certificates.
- Independently reconstruct the matching equations from literal endpoint
  formulas and check elimination denominators, table coverage and torsion.
- Attack rank-one collision exclusion, rank-two effective-field inflation,
  arbitrary CRT compatibility, endpoint congruence and every count scope.
- Benchmark any complete replay first; use pinned exact arithmetic, keep
  all output/certificate reads nonmutating, and log accepted source hashes.

The partial checkpoint already passed startup controls. This task will
not edit that accepted review, ledgers, protected paths, or other agents'
proofs and certificates, and will not stage or commit anything.

## Preliminary checker reading

Read `src/six_composite_matching.cpp` and
`tests/test_six_composite_matching.py` before the new proof notes existed.
The proposed full matching space is `2 * 2 * 2 * 720 * 720 = 4,147,200`:
one endpoint swap, independent endpoint signs, and both label permutations.
No locally distinct-support reduction is built into that enumeration.

The X-pivot code uses two equations with determinant12 to derive
`12w=Mv`, then ten residual equations in v. The independent checker
uses a Y pivot and vectorized exact integer rows, not that X elimination.
Its endpoint checker uses original four-variable equations and determinant
expansion. A proof of the claimed rank/Smith menu and the consequences
still requires fresh verification of its entire finite domain.

One documentation correction was flagged: the checker's asserted entry
bound `<200` is too small. A direct scan of all literal one-endpoint
eliminations reached225. A simple two-row determinant bound for those
entries is101250. Signed paired systems require their own bound.
This does not threaten int64 exactness; no mathematical counterexample
has been found. The author was notified immediately. The final checker
uses safe bounds `<500` and `<500000`. Independently scanning every
paired Y-pivot/sign/permutation choice gives the sharper entry bound228
and determinant bound103968; all arithmetic is exact within int64.

## Final disposition

**[PROVED], in-house, computer-assisted, independently accepted:**
Theorem GM and Theorem GE in
`notes/2026-09-30-six-composite-global-matrix.md` for every positive n
with `gcd(n,6)=1`. The full global-support Bloom domain `Omega_n` has
exactly one free twelve-element G orbit per unordered pair, with
different endpoints. No local distinct-support assumption remains.
Its exact pair-edge count is

`[(n-1)(n-11)+24[5|n]+24[7|n]]/12`.

The count uses the independently accepted odd support lemma; when every
prime divisor is at least11 the corrections vanish. Modulus1 is the
empty, vacuous case. This is a Bloom-image count, not an all-mechanism
six-point census or a count for moduli divisible by2 or3.

**[PROVED], in-house, dependent on the accepted 40/24 integer lift tables
and the new 219/57 permutation table:** the independent weighted-list
route in `notes/2026-09-30-six-composite-global-attempt.md` establishes
the same full global-support theorem when every prime divisor is at
least13. It independently resolves the locally colliding CRT factors
and does not use the full 4,147,200-system matrix table.

**[PROVED], in-house, computer-assisted:** for `gcd(n,6)=1`, distinct
Bloom pairs can share an endpoint only through inflation of the actual
field31 configuration. The entire Bloom graph has isolated edges and
exactly one inflated five-cycle when31 divides n. Otherwise every
Bloom endpoint has a unique Bloom partner. The field31 graph is exactly
45 isolated edges plus one five-cycle; it was freshly reconstructed
from all600 actual-support parameters using the immutable reference.
Thus the number of connected nontrivial **Bloom** families is the
pair-edge count minus `4[31|n]`. This does not rule out partners from
non-Bloom homometry mechanisms.

No novelty claim, external peer review, full Lean verification, or
classification for moduli sharing a factor with6 is accepted here.

## Attack of the complete matrix proof

### 1. Enumeration coverage and denominators

Reconstructed the centered rows from the literal uncentered endpoint
formulas. Centering requires inversion of6 and the scale3 is invertible
exactly in the stated coprime6 scope. The first two rows of either
centered source matrix have determinant12, with the written integral
adjugates. Over every allowed ring elimination is equivalent to the
original labelled equations; no row equation is discarded except the
two equations used to solve w.

Audited both nested loops. The paired table exhausts endpoint assignment,
both independent signs, and both full permutations: `2*4*720^2` cases.
The single-endpoint table exhausts all four source/target choices, both
signs, and every permutation: `4*2*720` cases. There is no quotient or
local-injectivity symmetry reduction.

The C++ X-pivot table records rational rank by entry/minor gcds. Its
independent paired checker uses the first two Y equations and exact
integer batches of all720 X permutations. I freshly ran the complete
checker **read-only** and compared every histogram class:

| Table | rank0 | rank1 | rank2 | complete cases |
|---|---:|---:|---:|---:|
| Paired | 12 | 864 | 4,146,324 | 4,147,200 |
| Single endpoint | 24 | 432 | 5,304 | 5,760 |

All39 rank-one direction/content classes and all46 paired rank-two
content/minor-gcd classes agree. The paired replay took2.584seconds.
The single-endpoint independent method constructs the original6x4
equations and expands every4x4 determinant; where needed it also checks
all3x3 determinants. It takes1.439seconds and agrees with the complete
exceptional-prime menu. The two-column source block has rank2 at every
allowed prime, because its pivot determinant is12; eliminating it can
introduce only2/3 denominator primes. This validates the comparison of
the original equation determinantal divisors with residual rank.

Every rank-zero matrix is12 times a G element; the paired rank-zero
endpoint assignment agrees with that element's T exponent. Every
rank-one normal is a literal support-collision normal and its content
has only2/3 factors. The rank-two coprime6 part of D is:

| Table | 1 | 5 | 7 | 11 | 13 | 19 | 31 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Paired | 4,144,428 | 936 | 912 | 0 | 24 | 24 | 0 |
| Single endpoint | 4,632 | 144 | 144 | 288 | 24 | 24 | 48 |

In every nontrivial case there is one exceptional prime with valuation
exactly one, rather than a product of primes or a square. This property
was checked from all histogram entries, not inferred from sampled
moduli. The preliminary note printed4,464 instead of4,632 in the
single-endpoint unit row; the former does not sum to5,304. Both this
review and the parent independently flagged it; the frozen note now
has4,632. This was a prose typo, not an arithmetic discrepancy.

### 2. Rank-one exclusion and arbitrary-CRT rank-two descent

For rational rank one, write each row as an integer multiple of its
primitive collision normal. The gcd of those multiples is the entry
content, since the primitive normal has coprime entries. A Bezout
combination consequently forces the collision form to vanish *exactly*
modulo n. Its content is a unit under `gcd(n,6)=1`, contradicting an
actual global six-element endpoint. This does not assume a primitive
parameter or local distinctness.

For rank two, the adjugate equations annihilate v by each two-by-two
minor. A Bezout combination annihilates v by their gcd D. If D has
only2/3 factors then v=0. Otherwise `D=u*p` for a unit u and one prime
p, so `p*v=0`. In Z/n this forces both coordinates into the single
order-p subgroup `(n/p) Z/n`, including when p has higher powers in n
and when n has many CRT factors. The equation `12w=Mv` puts w in that
same subgroup. No division by a nonunit or primitive-coordinate
assumption is hidden here.

The subgroup map from Fp is injective. Six distinct global labels remain
six distinct field labels, and any rigid transport shift is a difference
of two subgroup points, so it belongs to the subgroup and descends.
This prevents mixed local collision directions: a nonformal matching
does not retain two independent exceptional CRT factors.

Paired rank two leaves only5/7/13/19. At5 six points are impossible;
at7 every field parameter lies on one of the eight projective collision
directions. The13/19 surviving actual supports satisfy the accepted
field classification, so their parameters are G-related. Single-endpoint
rank two adds11 and31. All twelve projective directions are covered at
11, so there is no actual six-element Bloom endpoint there. Accepted
field uniqueness resolves13/19, and31 gives precisely the inherited
shared-endpoint exception. The argument proves the broader coprime6
scope, not merely prime divisors at least13.

### 3. Distinct endpoints, freeness and exact exception locus

A hypothetical globally congruent pair yields a swapped identification
with w=v. Rank0 has a reflection-type G matrix whose fixed line is an
actual collision line; rank1 forces a collision; rank2 descends to
actual field13/19 endpoints, which are different by the accepted field
theorem. Hence the endpoints are different. The other nonidentity G
fixed matrices have unit determinants1,3,4, so the G action is free.

For different pairs sharing an endpoint, neither rank0 nor rank1 can
survive and the13/19 rank-two cases already give the same pair. Every
remaining identification has `31*v=31*w=0` and is precisely the order31
subgroup inflation of a field identification. Conversely the subgroup
injection preserves all six labels and rigid-class distinctions.
The complete field31 graph has one five-cycle, so its injection produces
one, and only one, global exceptional component whenever31 divides n.
An additional partner outside that subgroup would itself be a distinct
shared-endpoint identification and is excluded by this same reduction.

The optional augmented-minor witnesses linking M to G are not needed
for the proof. I checked all their retained matrices and the stated
minor gcds nevertheless. The main proof uses the simpler subgroup
descent, so no inference from an augmented matrix's rational kernel
to its general ring kernel is required.

## Attack of the assembled counting synthesis, section5

Freshly read the complete newly appended section5 of
`notes/2026-09-30-six-composite-counting.md`. Its coprime6 pair formula,
Bloom-component count `B(n)-4[31|n]`, retained moment-key counterexample,
and precise difference from the full six-subset census are accepted.
At221, the formerly omitted region has `3850-192=3658` pair edges;
the complete matching argument covers those global-support parameters.

The conditional total-count corollary is accepted for **every n whose
every prime divisor exceeds131**, including arbitrary composites and
prime powers. The inherited G large-prime corollary puts every cyclic
six-pair in the Bloom image; the full-Omega theorem now counts that
entire image. Such n excludes5,7,31, so there are no support-count
corrections or exceptional cycle. Every nontrivial full six-point
family consequently has size two, and both total pair-edge and maximal
nontrivial-family counts are `(n-1)(n-11)/12`. G's solver/finite-certificate
dependencies remain; this review does not rerun or remove them. No total
all-mechanism count at other moduli is inferred.

Independently aggregated the eleven old and twelve new exact saved
parameter-image certificates:23 distinct moduli,7,310,663 candidates,
601,526 pair fibers, largest n2197. During this check the new direct
aggregate summary listed only the last seven requested moduli, while
all twelve individual certificates existed. The parent reran `--resume`
with all twelve to regenerate the aggregate; individual certificates
and their digests were unchanged. Direct aggregation of all individual
files confirmed the claimed totals even before that correction. This
was a manifest/invocation consistency issue, not a mathematics failure.

The accepted pre-promotion counting synthesis source SHA256 is
`03defeb52af0ad95e4212e9c79d0252d73975aa1ca52bec45bfbb2512a3c1708`.
Its section5 digest (text from `## 5.` through EOF) is
`e195a5a3ddbebeea6e252a2e705a99891f81af7b2b8609d2ccd2e03a28a297ad`.

## Attack of the independent weighted-list proof

The weighted local extension does not discard the former collision
branches. Independently checked all64 inherited paired/single-endpoint
matrices: each maps the E/D base vector to12 times that vector. A
nonzero residual gcd forces the exact E/D collision line and then
gives w=v; zero residuals give the formal G maps. Field alignment applies
to six-labelled lists with multiplicities, using root *multisets*.
Zero reductions of v force zero reductions of w; transport shifts divide
by the same p, so the induction remains valid on weighted lists.

For a primitive effective parameter, at most one collision form can
vanish mod p, because all collision-normal determinants are units at
p>=13. An actual collision modulo the effective prime power therefore
has exactly one rational direction and exactly its rational equal-label
partition. A near collision modulo p that is nonzero at the effective
modulus has no actual equal-label automorphisms. This distinction was
specifically checked by the six-group weighted regression suite.

Derived all twelve direction vectors from the literal endpoint
differences, then rebuilt every positive automorphism group directly
from its exact equal-coordinate blocks. Recomputed rotation permutations
from the coefficient matrices, rather than trusting the supplied arrays.
Independently generated the complete219 paired patterns and57 patterns
at each endpoint, including **every** witness (rotation,line) set.
The witness multiplicities are216 singleton patterns plus3 formal
patterns with12 witnesses in the paired table; at either endpoint they
are54 singletons plus3 formal patterns with12 witnesses. Every pattern
determines one rotation index. Repeated-label transpositions can be
odd; the proof correctly uses full permutation arrays instead of parity
for these positive tables.

Independently expanded `m5=15*s*(38*d +/-567*e)`. In a nonzero weighted
reflection, the E/D singular reductions are excluded by their unit third
moments. Else e,d are units, and vanishing third/fifth moments forces
s=0 and `6669=3^3*13*19=0` in the effective ring. Thus reflection is
possible only at effective field13 or19, and their slopes avoid every
collision direction. A nonzero colliding weighted endpoint never
reflects. The reflected permutations are exactly the previously checked
three-transposition catalog.

The positive57 sets and the two negative reflected triples are pairwise
disjoint as full label arrays. They were recomputed from actual field
coordinates, not asserted by parity. Factors where v=w=0 impose no
constraint and can be filled by the eventual common G element. At a
nonzero factor with locally congruent weighted endpoints, the E/D
reflection-type parameter stabilizer corrects the local G representative
to the global endpoint assignment; no actual matching permutation is
discarded. For equal global signs, the219 table pins a common rotation;
for opposite signs, a reflection forces actual local distinctness and
the old parity argument applies. The one-endpoint57/negative table
similarly pins the sign/rotation alternative. No gluing gap was found.

## Independent actual-field and characteristic31 controls

Built actual points from the literal uncentered formulas and used only
immutable `homometry.py` for T/I canonicalization and ICV. The admissible
parameter counts are0 at5/7/11,24 at13,144 at19,600 at31.
Replayed **every** retained exceptional system's actual-support field
solutions. The paired13/19 systems exercise288/432 solutions; the
single-endpoint13/19/31 systems exercise288/432/1440 solutions. All
declared endpoint assignments and rigid images agree.

The entire field31 image has50 edges and connected components45 of
size2 and one of size5. Every vertex of the size5 component has degree2.
The new saved cycle classes/edges and the inherited complete31 parameter
certificate agree exactly with the fresh reference-derived graph.
This is an independent complete finite field-image check, not a new
all-six-subset census.

## Exact commands and nonmutating replay

The new weighted regression was run directly; it writes no artifact:

```bash
.venv/bin/python tests/test_six_composite_weighted_gluing.py
```

All6/6 groups pass. The author's complete matrix test main writes audit
artifacts, so this reviewer instead called its audited independent
functions read-only:

```bash
.venv/bin/python - <<'PY'
from pathlib import Path
from collections import Counter
import importlib.util,json
path=Path('tests/test_six_composite_matching.py')
spec=importlib.util.spec_from_file_location('fresh_global_audit',path)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.test_paired_retained_witnesses();m.test_endpoint_table()
print(m.independent_endpoints())
processed,hist,r1,r2,seconds=m.independent_paired()
d=json.loads(Path('results/2026-09-30-six-composite-global-matrix/matching-certificate.json').read_text())
assert processed==4147200 and hist==Counter({0:12,1:864,2:4146324})
assert Counter({(tuple(r['direction']),r['content']):r['count']
                for r in d['rank1']})==r1
assert Counter({(r['content'],r['minor_gcd']):r['count']
                for r in d['rank2']})==r2
print(processed,dict(hist),len(r1),len(r2),seconds)
PY
```

Both complete numerical controls passed in about4seconds. My independent
219/57 derivation imported no gluing functions: it used literal raw
coordinate matrices, derived normals, exact S6 enumeration, symbolic
fifth moments, and compared every saved witness set. That replay took
0.13seconds. An initial command used the source's old output-directory
path during the parent's relocation and failed with FileNotFoundError;
rerunning with the current `src/` path passed. No mathematical or numeric
failure occurred. No certificate or source owned by another agent was
modified by this reviewer.

## Accepted pre-promotion source and proof digests

The notes were frozen as OPEN pending this attack. These hashes bind the
exact accepted draft; later status-only edits require a new source hash,
while the proof/certificate scope stays as accepted above.

| Item | SHA256 |
|---|---|
| Matrix proof note | `7b068f0a94f52a72d56cd61c95dfbbda7abb3f620cdd43899b68d73e72d9ba24` |
| Matrix mathematical body, §§1–7 | `df14488dd186428df9efc01ccd8c85b7856a4feb36c0d01a67c69638a05d1c50` |
| Weighted proof note | `6b85be9bd964745ac373b534162c9a97a8cc2aea872ac8105277fc1b5b02d92c` |
| Weighted mathematical body, §§1–6 | `5b259aba0a4ec66000596466edcf41102ae2667b61bb48a1f516b1fbbb87b55e` |
| `src/six_composite_matching.cpp` | `25acb01045790c6721b4372148370cf391804a35bd4bad2797c695a2bdf187dd` |
| `tests/test_six_composite_matching.py` | `1c867b2370f93d4c2febac349ce748f647ba2d1c95148be0b05c6d07c3879aef` |
| `src/six_composite_weighted_gluing.py` | `8556cfef14690d2aa5f8ab93297f797d67f85924658d35867ee9d8acd170c3d6` |
| `tests/test_six_composite_weighted_gluing.py` | `93ddfec87911e8e36d727d17275f86cc39c0d6df62fe5335c249dde72d214002` |
| Paired matrix certificate | `01feec2da14a77715489c43ac206f936098f89e2627a10b09825a051aff73f0a` |
| Endpoint matrix certificate | `c47fcccc2e684c5d0d317503cd6cf8ebae2faaafbc292ce092636db83e9d3930` |
| Complete reference-derived field31 graph | `f878647b41d2715d3bc68d3a05700a1acf90e3e78e3b06ae0ccee33905071773` |
| Saved independent matrix audit | `b3e062e66ae81dc7999f66c26769913c4b453993fc9aa76675ce5b8d526cbbd5` |
| Weighted219/57 certificate | `ceeea3aff49a49f0edcaf284cf3a744355a8d855d618b466049178ce43641865` |

Mathematical-body digests select the text from `## 1.` up to `## 8.`
for the matrix note and up to `## 7.` for the weighted note. They exclude
the introductory status line and the verification/provenance section.

## Honest limits

The global-Omega obstruction from the partial checkpoint is now resolved
in the coprime6 scope by the full matrix argument, and independently in
the prime-factors>=13 scope by the weighted argument. The old partial
review remains an accurate frozen checkpoint. These results classify
and count the classical Bloom image; they do not remove non-Bloom
relations from the full generation grammar. Conditional total counts
using G retain its solver/finite-certificate dependencies. No result
for cardinalities other than six, even/divisible-by3 moduli, historical
priority or external validation follows. Human review should focus on
finite enumeration completeness, the denominator-unit scope, and the
subgroup descent before public sharing. No staging or commit was made.

## Final status promotion and publication freeze

After this attack was saved, the parent promoted the theorem status text
and superseded the synthesis's historical OPEN paragraph. Freshly read
the final notes and section5; their mathematical scope and dependencies
remain exactly the accepted ones above. Reversing the precise status
phrases inside the two mathematical bodies recovers the accepted OPEN
draft body digests **byte for byte**. Thus the changed raw body hashes
reflect explicit status/prose promotion, not a changed theorem or proof.

The reversals checked were `Theorem GM [PROVED]` and
`Theorem GE [PROVED]` to their former `Proposed Theorem GM` and
`Proposed Theorem GE`; `Theorem GLOBAL [PROVED]` to
`Proposed Theorem GLOBAL [OPEN]`; `Weighted local lemma WL [PROVED]`
to `Weighted local lemma WL [OPEN]`; and `the pair-edge formula.`
to `the proposed pair-edge formula.` within the weighted mathematical
body. All four source/test files and all five finite evidence files in
the preceding hash table were independently rehashed and are unchanged.

| Final item | SHA256 |
|---|---|
| Matrix proof note | `f3d7d47ee12b318c49cc81f390dd5a66cedc595cb6f7bda67dcc74ea3c5faef4` |
| Matrix mathematical body, §§1–7 | `fcef9d818b3fb691d6525d30147a9803e6e506c7f2e6e8cc7da3ad95bb7382cc` |
| Weighted proof note | `6ab94764d1c57413698de1876d0548f7c90020abaa322b82437e10ffe9ab193c` |
| Weighted mathematical body, §§1–6 | `193b3c128f2df501acce7853b60bf43b2d647749e4ef98f496368a212b7a4f84` |
| Counting synthesis | `c6f55df26e1dab82897058c3eb574b3df3c6fb0135f06399024ac393b84964fc` |
| Counting synthesis section5 | `2381817951a6179a91392b2c5a6eb799427e2f465ca81dda495f8a50b899c25e` |
| Corrected12-modulus direct aggregate | `0b52d391c506c427fe84c0d6b6d90cca0b8f9acc0a4ff5d57fdfbc034dbfa7e9` |

The final direct aggregate now lists exactly
`[25,35,49,55,65,77,91,121,143,187,209,341]`; independently checked its
255,732 parameter candidates and19,940 pair edges. All individual
certificate digests remain unchanged. The two proof bodies, complete
finite tables, field31 graph, and assembled section5 are accepted for
the exact scopes and limitations recorded here. This reviewer made no
other file edits, staging, or commits.
