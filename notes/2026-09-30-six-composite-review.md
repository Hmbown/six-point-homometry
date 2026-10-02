# Fresh adversarial review of the composite Bloom argument

30 September 2026. **Independent review complete for the scopes below.** This independent review
owns only this note; the parent session owns the main plan and ledgers.
No novelty claim or unconditional arbitrary-modulus six-point counting
claim is made.

## Review plan

- Goal: attack Theorem CR on its actual enlarged domain `L_n`, including
  prime-power supports that are not faithful modulo the residue prime.
- Method: rederive the local moment/root argument and the CRT label
  permutation/sign alignment; independently verify exact coefficients.
- Success: either a concrete gap/counterexample, or an explicit acceptance
  of the bounded theorem with its hypotheses and computational limits.
- Compute: pinned startup suite, bounded independent parameter controls,
  and existing certificate replay; expected runtime under one minute per
  individual control, with larger jobs estimated before launch.

## Startup and scope

Read `README.md`, `RESEARCH_PROGRAM.md`, current `PROGRESS.md`,
`CONJECTURES.md`, `LITERATURE.md`, and `AGENTS.md`. The agenda is PQ1/PQ2;
the inherited prime/field proof is a coefficient-identity dependency, not
a license to use field root uniqueness over a ring.

`.venv/bin/python tests/run_tests.py` passed all 10 printed groups in this
fresh review session. The pinned interpreter is necessary under the repo's
environment warning. Protected reference files are unchanged by this review.

The proof under review is
`notes/2026-09-30-six-composite-algebra.md`. `L_n` requires both `e,d` to
be units and both endpoints to contain six distinct entries in **every
prime-power CRT factor**; `F_n` requires six distinct entries modulo every
residue prime. Neither theorem scope includes all `Omega_n` parameters.

## Initial attack log

1. **Local ring root uniqueness:** zero divisors would invalidate a naked
   factorization-uniqueness argument. Here `d` a unit makes all three root
   differences units. Reduction selects exactly one matching root; the
   other factors are units and force equality in the ring itself. This
   attack has not found a gap.
2. **Mixed CRT signs:** equality of squared odd moments does not synchronize
   local signs (the n221 control refutes that shortcut). The proposed proof
   instead uses the parity of one *global* point-label permutation. Every
   formal `R^i T^j` permutation is even, and a six-point local reflection
   has three transpositions. This synchronizes the signs before any CRT
   inference from moments.
3. **Remaining rotation index:** once the common sign is fixed, one global
   endpoint must use that sign directly; otherwise both local endpoints
   would reflect, contradicting the unit difference of squared third
   moments. Its unique label transport pins the same `i` in all factors.
4. **Small freeness wording correction:** `det(I-(-I))=4`, rather than the
   stated set `1,2,3` of determinant values. Four is a unit here. Handling
   `-I` directly by `2v=0` also repairs the prose. This is not a theorem
   counterexample; the author/parent was notified immediately.

## Disposition of CR, PP, and the complete-local-support CRT theorem

**[PROVED], in-house, independently accepted:** the local-ring separation
and CRT gluing of Theorem CR on `L_n`, after the minor freeness correction.
The written proof is algebraic and does not rely on finite image counts.

**[PROVED], in-house, with the explicitly audited finite integer table:**
Theorem PP in §8 classifies the entire actual-six-support Bloom image in
every `Z/(p^k)` with `p>=13`. Its fibers are free twelve-element `G`
orbits, its endpoints are different rigid classes, and its pair count is
`(p^k-1)(p^k-11)/12`. The forty-pattern elimination table is a proof
dependency; the finite sampled moduli are verification, not its proof.

**[PROVED], in-house, dependent on PP and its exact table:** §9 extends
the CRT theorem to `S_n`, requiring six actual entries in **each
prime-power factor**, without unit conditions on `e,d`. Its count is
`prod((p^k-1)(p^k-11))/12`. `F_n` and `L_n` remain proper useful
subdomains; their separate formulas remain valid. At squarefree moduli
all three domains coincide. At one prime power `S_n=Omega_n`.

**[OPEN]:** the arbitrary global `Omega_n` parameter fiber theorem and
pair formula. Six globally distinct entries can project to repeated
labels in a CRT factor. Neither parity gluing nor the PP local support
theorem covers that case. The observed full-image counts at products of
primes are not promoted to a proof. The pair-fiber arguments in §§1–6,
8–9 alone do not add uniqueness of partners; the subsequently accepted
§§10–11 add exactly the bounded uniqueness statements attacked below.
No unconditional all-modulus six-point completeness count is added.
Characteristic 31 may have shared endpoints even when pair fibers are
exactly `G`.

## Detailed fresh attacks on the enlarged statements

### A. Moment coefficients and arithmetic exceptions

Reconstructed centered coordinate rows from the literal uncentered
formulas, then expanded every polynomial using exact symbolic arithmetic.
All identities in §2 agree, including the coefficient combination
`118 C6 - 13 C3 = 162 e^2` and
`m3(X)^2-m3(Y)^2 = -5832 d e`. Recovering `s,e^2` uses only units
`66,162`, so there is no failure at primes 13,19,31,79,239, or an
isotropic `s`. Third moments are squared or added only where signs and
endpoint interchange require it; no sign-sensitive moment is silently
treated as a rigid invariant.

The independent matrix calculation gives eleven nonidentity fixed-vector
matrices: five rank-two matrices with determinants `4,3,1,3,1`, and six
rank-one matrices with the stated excluded fixed lines. The corrected
freeness proof includes determinant four; `2v=0` is also a direct check
for `-I`. The field proof is used
for integer identities and its actual stated field scope.

### B. CRT labels, signs, and translations

Recomputed all twelve formal point permutations, rather than checking
only the generators. All are even. For each fixed endpoint and endpoint
swap, its three permutations indexed by the rotation are distinct.
Actual local supports have six labels, so a centered transport with a
given sign has a unique label matching; any difference between two such
transports would be a stabilizing translation. A nonzero translation in
`Z/(p^k)` has order a positive power of `p>=13`; it cannot stabilize six
points.

Changing the sign of a transport creates a reflection of the matched
local six-point set. Since two is invertible, a reflection has at most
one fixed point. Six labels force an even number of fixed points, hence
zero. It is three transpositions and odd. The global permutation's
parity therefore fixes the same local `G` sign in every factor. The
no-simultaneous-reflections lemma supplies at least one endpoint with the
direct sign, whose unique formal permutation pins the same rotation
index. This is actual label gluing, and does not reuse the refuted
composite moment-key shortcut.

### C. Full prime-power singular strata

The moment calculations apply to six-labelled weighted lists after
reduction even if those labels coincide. Field cubic factorization
recovers the root *multiset* with repeated roots; an ordering is still
one of the six root permutations. No ring factorization uniqueness is
claimed in this step.

If `v=0 mod p`, the same cubic forces `w=0 mod p`. Every point and
every transport translation is divisible by `p`, because zero is in
each endpoint and its transported image is a support entry. Division is
an injection from the `p`-multiple subgroup to the smaller cyclic ring;
it preserves six distinct entries and transports. Iteration therefore
reduces to a primitive parameter without losing matching information.

For primitive parameters, distinct collision lines meet only at zero
modulo `p`. The six singular `e/d` lines form two transitive `G` triples.
Normalize to E (`b=0 mod p`) or D (`b=2a mod p`) and then normalize
`w=v mod p`; these changes preserve the original unordered rigid pair.
The nonzero differences between reduced coordinate values have prime
factors only 2,3,5. Hence the rational reduced equality patterns are the
entire patterns at every `p>=13`. Opposite signs are excluded by the
nonzero reduced third moments `12a^3` or `+/-486a^3`, rather than by a
faithful-support assumption.

Independently enumerated all 720 permutations at each endpoint, both
sign choices, and all paired matchings. The complete list is 32 E and
8 D systems. Reconstructed the elimination matrix using the inverse of
the first two centered X rows (determinant 12), then all twelve residual
rows. Compared **every** saved matrix, residual row, gcd, and supplied
Bezout combination to the independently computed values:

| Stratum | Residual coefficient gcd histogram | Independent Smith histogram |
|---|---|---|
| E | `0:2, 18:16, 36:12, 72:2` | `(1,3,0,0):2; (1,3,3,0):24; (1,3,6,0):6` |
| D | `0:2, 9:4, 36:2` | `(1,3,0,0):2; (1,3,3,0):6` |

All nonzero gcds are units here. They force `b=0` or `b=2a` exactly
modulo `p^k`, which is an actual endpoint collision, not just a residue
collision. The two zero-gcd cases per stratum give `I` and the stated
signed `R^2 T` matrices. The full table is exhaustive; no omitted local
torsion prime is present. A hypothetical congruent pair at `w=v` gives
a swapped identification, whose surviving map fixes only the respective
actual collision line, so congruent endpoints are excluded.

### D. Reflection descent and S-domain CRT gluing

For a parameter divisible by a maximal common `p^t`, a reflection shift
is divisible by the same power because it is the image of zero in the
support. Divide both reflection equations and labels into the smaller
ring. At its primitive level either `e,d` are units, when the unit
squared-third-moment difference forbids both reflections, or the E/D
reduced third moments are units, when neither endpoint can reflect.
This covers the nonunit strata in §9 without assuming a third moment
remains a unit before descent. G preserves reflection existence up to
endpoint interchange. The subsequent CRT parity and rotation-index
argument is consequently valid on the stated `S_n` domain.

## Exact verification record

All controls used the pinned `.venv/bin/python`. No output, source,
ledger, protected reference file, or other agent's artifact was modified
by this review. Commands run:

```bash
.venv/bin/python tests/run_tests.py
.venv/bin/python tests/test_six_composite_bloom.py
.venv/bin/python tests/test_six_composite_arithmetic.py
```

Results: startup 10/10 groups; dedicated direct composite 8/8 groups;
independent arithmetic 4/4 tests. The direct suite checks every literal
point canonicalization and every complete parameter image through n43
against immutable `homometry.py`, and checks the saved parameter
partitions, orbit bindings, and characteristic31 boundary. Saved large
fibers use formal orbit bindings; these are not a fresh six-subset census.

**[COMPUTED]:** a separate literal-point, all-anchor, both-sign
canonicalizer, importing only the immutable reference for final controls,
enumerated these complete domain images. Every image had different
endpoints, reference-equal ICV, and exactly twelve parameters equal to
one independently constructed `G` orbit.

| n | L parameters | L pairs | F parameters | F pairs |
|---:|---:|---:|---:|---:|
| 169 | 15,288 | 1,274 | 4,056 | 338 |
| 221 | 2,304 | 192 | 2,304 | 192 |
| 247 | 3,456 | 288 | 3,456 | 288 |
| 323 | 13,824 | 1,152 | 13,824 | 1,152 |

At n169, 11,232 checked L parameters are nonfaithful modulo 13. Thus
the enlarged-domain control really reaches beyond F. The four domain
controls took about 0.8,0.2,0.4,1.8 seconds respectively.

The auxiliary `verify.py` was imported and its functions called read-only,
without invoking `main` (which overwrites its certificate). Exact replay
agreed with its stored source/reference hashes, formal permutations,
reflection records, and every saved fiber: n169 full 2,212 pairs,
faithful 338, regular 1,274; n221 faithful 192. An initial comparison
mistakenly compared runtime tuples with JSON lists and failed an equality
assertion; JSON normalization resolved it. No numeric or mathematical
discrepancy occurred. These auxiliary exploratory full-domain counts remain
finite evidence; PP is established by the written singular-stratum proof.

Independently computed all 15 reflection matchings per endpoint. The
gcd histogram for each is `3:1,6:3,9:3,12:3,18:3,39:1,57:1`, with
the exact exceptional rows stated in §6. Normalized faithful reflections
are precisely X/Y slopes 10/4 at p13 and 8/12 at p19. The shifts are
8/7 at p13 and 1/1 at p19. Every L parameter at prime squares169,289,361
has neither endpoint reflective; checked parameter counts are
15,288/53,856/88,920. This is a finite control, not an added theorem
classifying all nonfaithful reflection loci.

## Independent audit of the odd full-support parameter count

This count concerns `Omega_n` **parameters**, not pair fibers. Derived
the twelve primitive collision normals directly from the fifteen
differences of each literal endpoint list. The only removed scalar
multipliers are 1 and 2, so the normal union is exact at every odd n.
Distinct normal determinants are exactly `1,2,3,4,5,7,8` in absolute
value. Independently computed Smith factors for all 4,083 rank-two
subsets (the other 13 subsets have size zero or one). Their signed
inclusion-exclusion weights are

```text
d:      1   2  3  4  5  7  8
weight:-16  3  8  3  6  4  3
```

Each first Smith factor is one. A rank-two kernel modulo n has
`gcd(n,d)` elements. This gives the exact support count

`n^2-12n+11+16[3|n]+24[5|n]+24[7|n]` for odd n.

An elementary independent reading gives the same formula. A nonzero
point in two collision lines has additive order dividing their nonzero
determinant. At odd n that order must be 3,5,or7, since the determinant
menu contains no 9,25,49. Points of order p are exactly the embedded
`F_p^2` points. The twelve lines reduce to 4,6,8 distinct lines at
p3,p5,p7, respectively. Their overcount corrections are
`(12-4)(3-1)=16`, `(12-6)(5-1)=24`, `(12-8)(7-1)=24`.
Every other intersection is only zero. Literal parameter counting at
every odd n3..151 agrees. The arithmetic test separately checks literal
endpoint supports at every odd n3..121. This confirms the support lemma
without asserting a small-prime or general-composite pair formula.

## Reproduction appendix: independent finite singular-table attack

This exact read-only command was run; it does not invoke the author's
generator or overwrite its result. Its centered matrices are derived
from the uncentered endpoint formulas.

```bash
.venv/bin/python - <<'PY'
from collections import Counter
from hashlib import sha256
from itertools import permutations,product
from math import gcd
from pathlib import Path
import json,sympy as S
from sympy.matrices.normalforms import smith_normal_form
P=S.Matrix([[0,0],[1,0],[-2,1],[-2,2],[0,2],[-1,3]])
Q=S.Matrix([[0,0],[1,0],[2,1],[-1,2],[1,2],[-1,3]])
Cs=[S.Matrix([[3*M[j,i]-sum(M[:,i])/2 for i in range(2)]
              for j in range(6)]) for M in (P,Q)]
A=Cs[0][:2,:];assert A.det()==12
record=json.loads(Path('results/2026-09-30-six-composite-algebra/lift-table.json').read_text())
assert record['source_sha256']==sha256(Path('src/six_prime_power_lifts.py').read_bytes()).hexdigest()
for kind,base in (('E',(1,0)),('D',(1,2))):
    gcds=Counter();smiths=Counter();matches=0
    for swap in (0,1):
        lists=[Cs[swap],Cs[1-swap]]
        sign=1 if kind=='E' or swap==0 else -1
        options=[]
        for endpoint in (0,1):
            source=tuple(Cs[endpoint]*S.Matrix(base))
            target=tuple(lists[endpoint]*S.Matrix(base))
            found=[p for p in permutations(range(6))
                   if source==tuple(sign*target[h] for h in p)]
            assert not [p for p in permutations(range(6))
                        if source==tuple(-sign*target[h] for h in p)]
            options.append(found)
            for prime in (13,17,19,23,31,79):
                finite=[p for p in permutations(range(6))
                        if tuple(x%prime for x in source)==
                           tuple((sign*target[h])%prime for h in p)]
                assert finite==found
        for px,py in product(*options):
            targets=[S.Matrix([lists[e].tolist()[h] for h in p])*sign
                     for e,p in enumerate((px,py))]
            M=12*A.inv()*targets[0][:2,:]
            H=(Cs[0]*M-12*targets[0]).col_join(Cs[1]*M-12*targets[1])
            assert all(int(H[h,0])==(0 if kind=='E' else -2*int(H[h,1]))
                       for h in range(12))
            D=0
            for h in range(12):D=gcd(D,abs(int(H[h,1])))
            gcds[D]+=1
            equations=Cs[0].row_join(-targets[0]).col_join(Cs[1].row_join(-targets[1]))
            snf=smith_normal_form(equations,domain=S.ZZ)
            smiths[tuple(abs(int(snf[h,h])) for h in range(4))]+=1
            saved=[r for r in record['tables'][kind]['patterns']
                   if r['swap']==swap and tuple(r['permutation_X'])==px
                      and tuple(r['permutation_Y'])==py]
            assert len(saved)==1;r=saved[0];matches+=1
            assert r['sign']==sign and r['twelve_w_matrix']==M.tolist()
            assert r['residual_rows']==H.tolist() and r['residual_coefficient_gcd']==D
            assert sum(r['gcd_bezout_coefficients'][h]*int(H[h,1])
                       for h in range(12))==D
    assert matches==len(record['tables'][kind]['patterns'])
    print(kind,matches,dict(gcds),dict(smiths))
print('PASS full 40-system independent lift audit')
PY
```

## Final attack of unique partners and assembled counting

**[PROVED], in-house, with the audited 24-system integer table:** §10
gives a unique Bloom partner for every actual six-element Bloom endpoint
in `Z/(p^k)` when `p>=13` and `p!=31`. Independently expanded the
single-endpoint moments: after `s` is known, their coefficient matrix
for `e^2` and the appropriately signed `de` is
`[[58077,-2916],[6399,-4860]]`, of determinant
`-263594736 = -2^4 * 3^12 * 31`. Thus no endpoint-label choice is
needed to recover `e^2`; the sign is absorbed in the second unknown.
Repeated-root field alignment, zero-reduction descent, and the regular
local-ring argument apply with a shared endpoint alone.

Independently enumerated all four source/target endpoint choices and all
720 possible permutations for each. Every saved one-endpoint matrix,
residual row, gcd, and Bezout witness agrees. E has 16 systems with
gcd histogram `0:4,18:8,36:4`; D has 8 systems with
`0:4,9:2,36:2`. Independent Smith histograms are
E `(1,3,0,0):4, (1,3,3,0):8, (1,3,6,0):4` and
D `(1,3,0,0):4, (1,3,3,0):4`. The surviving maps belong to G;
the others force an exact collision. Excluding 31 is essential to the
upstream invariant recovery and retains the genuine field counterexample.

**[PROVED], in-house, dependent on PP, §10, and the exact reflection
catalog:** §11 gives a unique partner in the entire Bloom image for each
endpoint represented by `S_n`, when all prime factors are at least13
and 31 does not divide n. `H_n` in the counting synthesis is exactly
the same domain as `S_n` in the algebra note. The names are aliases;
neither means faithful residue-prime reduction.

The catalog includes every possible nonfaithful reflection. At a
primitive effective level `p^ell`, an exceptional matching determinant
is `p` times a unit. For `ell>=2` its adjugate equations force
`p u=0`, contradicting primitivity. The only remaining reflections are
inflations from F13 or F19. Recomputed their actual label permutations
from the literal centered lists and every twisted rotation array:

| Endpoint / prime | i=0 | i=1 | i=2 |
|---|---|---|---|
| X / 13 | `2,4,0,5,1,3` | `5,0,3,1,2,4` | `1,3,4,2,5,0` |
| X / 19 | `1,0,3,2,5,4` | `2,3,4,5,1,0` | `5,4,0,1,2,3` |
| Y / 13 | `3,2,1,0,5,4` | `4,0,3,5,2,1` | `1,5,4,2,0,3` |
| Y / 19 | `1,0,4,5,2,3` | `3,5,1,2,0,4` | `4,2,3,0,5,1` |

Row-index composition is `chi[rho^i[h]]`, matching the stated tables.
For either endpoint the 13/19 three-element sets are disjoint. Normalize
the shared endpoint to X on both parameters. Local PP uniqueness then
forces the G-elements to have no endpoint swap. Their signs are common
by the global matching parity. With the direct sign, the three distinct
formal rotations pin one index. With the opposite sign, all factors
must reflect. Disjoint reflection cosets prevent a mixed 13/19 product,
so only one prime-power factor remains and §10 resolves it. No global
rigid transport of the other endpoint was assumed in this argument.

Independently checked all full-Omega parameters at prime squares169,
289,361 for reflection: total parameters 26,544/80,064/126,000,
reflected-X/Y counts 12/12, 0/0, 18/18. Each reflective parameter has
effective modulus 13 or19 and exactly the cataloged label permutation.
The control took 6.2 seconds and is finite evidence for the proved catalog.

Finally verified the literal integer directed-difference multiset identity.
For a reduced six-labelled list, the zero correlation is the integer
sum of squared multiplicities. It equals six exactly for six distinct
labels. Therefore a parameter sharing an S/H endpoint in the global
Bloom image has both endpoints locally six-element and itself lies in
S/H. This justifies uniqueness against the *entire* Bloom image while
leaving possible non-Bloom homometric partners outside the claim.

The assembled counting note is accepted with that same distinction.
Its n221 boundary `(1,104)` has literal lists
`X=(0,1,102,206,208,90)` and `Y=(0,1,106,207,209,90)`, each of
size six globally; both have sizes four modulo13 and five modulo17.
This is a genuine Omega-minus-H region, not a fiber counterexample.
Its elementary support lemma was freshly attacked and accepted above.

The conditional total-count corollary at `n=p^k,p>131` is also accepted.
The inherited large-prime corollary in `six-paper.tex` explicitly says
*every prime divisor* exceeds131, with its line-solver qualification.
At a single prime power PP covers the entire Bloom image, and §10
gives unique partners because p cannot be31. Thus total pair-edge and
maximal nontrivial six-family counts both equal `(n-1)(n-11)/12` and
each family has size two **with G's solver/finite-certificate dependencies
retained**. This review does not revalidate G's entire proof or finite
census. It does not establish the total count for a general composite n.

## Reproduction appendix: independent reflection-coset check

```bash
.venv/bin/python - <<'PY'
import sympy as S
P=S.Matrix([[0,0],[1,0],[-2,1],[-2,2],[0,2],[-1,3]])
Q=S.Matrix([[0,0],[1,0],[2,1],[-1,2],[1,2],[-1,3]])
Cs=[S.Matrix([[3*M[j,i]-sum(M[:,i])/2 for i in range(2)]
              for j in range(6)]) for M in (P,Q)]
R=S.Matrix([[0,-1],[1,-1]])
expected={(0,13):(2,4,0,5,1,3),(0,19):(1,0,3,2,5,4),
          (1,13):(3,2,1,0,5,4),(1,19):(1,0,4,5,2,3)}
for endpoint,C in enumerate(Cs):
    rows=[tuple(row) for row in C.tolist()]
    rhos=[tuple(rows.index(tuple(row)) for row in (C*R**i).tolist())
          for i in range(3)]
    cosets=[]
    for p,slope in ((13,(10,4)[endpoint]),(19,(8,12)[endpoint])):
        values=tuple(int(x)%p for x in C*S.Matrix([1,slope]))
        assert len(set(values))==6
        chi=tuple(values.index(-x%p) for x in values)
        assert chi==expected[(endpoint,p)]
        twisted=tuple(tuple(chi[h] for h in rho) for rho in rhos)
        assert len(set(twisted))==3;cosets.append(set(twisted))
        print(endpoint,p,chi,twisted)
    assert cosets[0].isdisjoint(cosets[1])
print('PASS actual reflection permutations and disjoint cosets')
PY
```

## Accepted draft digests and limitations

These hashes bind the **accepted pre-promotion draft**, before the parent
changes pending/open status prose or consolidates the S/H name. Such
editorial changes require a final-source hash but do not strengthen scope.
The mathematical-body digest selects sections 1–6 and 8 through EOF;
section7 is the exploratory verification/open-obstruction narrative.

| Accepted item | SHA256 |
|---|---|
| Algebra source, reviewed §§1–6,8–11 | `c42685a258ea4462fa0ad68db0ee13dbbede752f8052b6758f2d499642d9f5f6` |
| Algebra mathematical body | `47c741ef6446f563d00ac17f8640ca02a6c60eab583ebae007e444b2cc7d5b7a` |
| Counting synthesis before §10/11 conclusions added | `42142bd93cd08e846aca76e974f5d7aae09ff7d826a2a5ddc7207a43146ac069` |
| Auxiliary verify source | `c366a9a985a5ca9d8dacb18e47f5de319c35cbd8b89ed2557d09019790971c98` |
| Auxiliary certificate | `e2801ad6b0adfa0d1b46b823213838e19946b8b744f568fb500446ac91b74da1` |
| Paired lift source | `4fa7177d716e01a8a6b7a8e7a9cecf6c84efc569b3a77f66d19574b0f96038df` |
| Paired lift certificate | `7dcd51876a159c0b3b5ebebd215674ec551ac82bb358ea1ef5071ac3c57ad5b7` |
| Endpoint lift source | `5a6b07bff6f25f6999b59f168eccfffd35cebbba8634d1732ddf051e88d4ddf6` |
| Endpoint lift certificate | `945aaa206e4756d028681b2eac7db562db6097cac74b35a7e99899298b635e2d` |
| Direct enumerator | `7aa4ab981a633b25d250a8cb32a65d0ffd41b4b92c46459cb05bc2eba12639be` |
| Direct tests | `35590f36fbe9b0b39544f49c8b2e23ef55caa6d3848cf03ef11a0f42dc19266f` |
| Arithmetic counter, H counts included | `8b3703bdcc526f84c595e0d81a8902b34d7b221f059b43b924881fc61fdf39fb` |
| Arithmetic tests | `32158ebc0aa97d0a3f5b3c40878ab5505528a9562a31c49b9383817ec1563726` |
| Immutable homometry reference | `520a929aff08f5d9eb7d59977e495ac9fdcb80ff90045493cfb72abe85cff0d6` |
| Immutable startup suite | `951d14fe5ead93338a949d95412f51b658fe36d34bf4cd2b0032a8dc85545aa5` |

Reproduce the mathematical-body digest exactly:

```bash
.venv/bin/python - <<'PY'
from pathlib import Path
from hashlib import sha256
t=Path('notes/2026-09-30-six-composite-algebra.md').read_text()
body=t[t.index('## 1.'):t.index('## 7.')]+t[t.index('## 8.'):]
print(sha256(body.encode()).hexdigest())
PY
```

No substantive counterexample to the accepted statements was found.
The determinant wording error was corrected. Explicitly **not accepted**
as proved: global Omega CRT fibers/pair formula, general small-prime
pair counts from the support formula, global uniqueness when31 divides
n, novelty, complete formal verification, or external mathematical
review. Before public circulation a human specialist should review the
weighted reduction, finite elimination tables, reflection gluing, and
inherited G dependencies. No file was staged or committed by this reviewer.

## Source relocation and independent regression replay

The parent relocated new executable code into `src/` as required by the
user's repository instructions. `six_composite_auxiliary.py` replaces
the original output-directory `verify.py`; `six_prime_power_lifts.py`
and `six_prime_power_endpoint_lifts.py` replace the two lift generators.
The finite mathematical records are unchanged; only source paths,
source-binding hashes, and the computation metadata status changed.
The reproduction appendix above now binds the paired table to the current
source path. Its independent 40-system replay passes after relocation.

```bash
.venv/bin/python tests/test_six_prime_power_lifts.py
```

All 3 groups pass. They rederive the coupled paired and single-endpoint
systems from literal uncentered coordinates, independently compute their
matrices and Smith factors, and verify every perfect matching/reflection
coset. A fresh read-only auxiliary import replay also passes all four
saved partitions (n169 full/F/L and n221 F), with the new source digest
and unchanged actual mathematical contents. No generator `main` was run
by this reviewer and no output was overwritten.

| Relocated artifact | SHA256 |
|---|---|
| `src/six_composite_auxiliary.py` | `39fd9905fe7fbcd0558e90500e0c102af77a0e0366659fa388c50bab848459f2` |
| `src/six_prime_power_lifts.py` | `2add9866e02d73fdaf36d733bb446c0b73c635f6ad25328046fba8e946722dc5` |
| `src/six_prime_power_endpoint_lifts.py` | `49f673ae6e6cd04112670f9f7546555f18556d7f7ed6bb75b894b7f1e8852f90` |
| `tests/test_six_prime_power_lifts.py` | `0f32d545b033767096109a41c1522257e337d1cfd5318d6111e41443a80a63e9` |
| `certificate.json` | `428d2543250f74dbc04c655f0d4f597615bb58c2beed4ad1dc51f2ee6a8f8f7b` |
| `lift-table.json` | `02eb646237f2821b7a029675256c1bd1b1c4b780cf04e01604b88d7981e545c8` |
| `endpoint-lift-table.json` | `eb02da0114f9518eb885f164ab4a1337f0ae03c7f09960fcdd25bddc7a558732` |

New proposed full-Omega arguments, if appended later, are outside the
accepted §§1–6,8–11 scope of this checkpoint and require a fresh attack.

## Frozen accepted partial checkpoint after status promotion

Freshly reread the final algebra status statements, remaining-obstruction
scope, relocated reproduction paths, §10/11 conclusions, and the entire
counting synthesis after the parent's editorial promotion. The synthesis
now includes the accepted bounded uniqueness and conditional total
prime-power family count. No mathematical strengthening beyond the
accepted arguments was found.

| Final accepted partial item | SHA256 |
|---|---|
| `notes/2026-09-30-six-composite-algebra.md` | `1fd627f0329ff4c879e4bde9e64f9c780bae52e80a46802e37817e933da60826` |
| Algebra mathematical body, sections1–6 and8–11 | `090d25f41d9425d9ff46379dadd06b70d8bc4fb17c1d9ffbedfe6f5f9c19ad1d` |
| `notes/2026-09-30-six-composite-counting.md` | `cd0db10d210f46532a265f79f0f5ff4abeef12f8c966546712e9d1d006be963f` |

For a later source with new sections, reproduce the accepted-body boundary
without accidentally including an unreviewed §12:

```bash
.venv/bin/python - <<'PY'
from pathlib import Path
from hashlib import sha256
t=Path('notes/2026-09-30-six-composite-algebra.md').read_text()
end=t.find('## 12.')
end=len(t) if end<0 else end
body=t[t.index('## 1.'):t.index('## 7.')]+t[t.index('## 8.'):end]
print(sha256(body.encode()).hexdigest())
PY
```

This checkpoint accepts the exact stated local/CRT domains, unique-partner
exceptions, elementary support lemma, and conditional total prime-power
corollary; the arbitrary-global-Omega fiber conjecture remains open here.
