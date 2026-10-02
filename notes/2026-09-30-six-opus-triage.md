# Independent source audit of the Iw/BF dependency

30 September 2026. Scoped reviewer, separate from the review coordinator.
This note records an independent source audit of the Iw/BF dependency by the
existing project team. It is **not an Opus review**, and it is **not an
independent replay of the weighted UNSAT result**. No claim of novelty or
human specialist review is made.

## Scope and present verdict

**[COMPUTED]** The current weighted builder and independent checker regenerate
their saved SMT inputs byte for byte. Exact coefficient controls and the saved
BF finite certificates pass their existing independent arithmetic checker.
No mathematical assumption mismatch was found between the written Iw theorem,
its two weighted encodings, and the use of Iw in BF.

This reviewer **did not independently replay the weighted UNSAT query or
check its proof in a new proof kernel**. The Iw completeness conclusion retains
the existing exact-solver qualification. Source inspection and BF certificate
replay are the new work here; saved UNSAT metadata was read only.

## 1. Weighted normalization audit

`notes/2026-09-30-six-integer-theorem.md:238-248` is valid also when the
minimum or maximum is repeated. For a weakly sorted six-atom list
`0 <= a1 <= a2 <= a3 <= a4 <= 1`, remove the occurrence corresponding to
the labelled edge `(0,5)`. Every remaining edge length is at most
`max(a4,1-a1)`, and both candidate lengths still occur as labelled edges.
Thus the largest remaining value has exactly that value, even when it equals
the removed diameter or is attained several times. Reflection interchanges
the candidates and can place that value at coordinate `a4`.

The same operation on B gives the shared r. An orientation tie may be broken
either way; the encoding only requires the non-strict orientation inequality.
Translation congruence after the minima are anchored at zero is literal
multiset equality. Reflection congruence after diameter-one normalization is
equality of the full reversed list with `1-B`; the two endpoint equalities are
automatic and all four remaining equalities are included. Strict lexicographic
order after swapping A/B is legitimate precisely because congruent partners
have been excluded.

At the I.2 weighted endpoint the A orientation is not unique: its first and
last gaps coincide. This does not contradict Iw, whose note explicitly does
not extend the strict-form uniqueness assertion to these boundaries. The two
boundary presentations are equivalent by independent reflection as stated.

## 2. Builder/checker audit

The builder's coordinate formula in `src/six_integer_smt.py:71-113` ranges
over real variables without a denominator/grid bound. The weighted wrapper
`src/six_integer_weighted.py:6-10` replaces exactly the ten adjacent coordinate
inequalities by weak inequalities. It does not weaken the strict pair-order
test, add a strict interior-point assumption, or discard zero edge values.

The 15 occurrence-count equations are sufficient for multiset equality: for
each value present among A's edges, its total multiplicity on B equals its
total multiplicity on A; these prescribed multiplicities already sum to 15,
so B cannot contain an additional value. Zero is included. A multiset of six
labelled atoms contributes six diagonal zeros plus twice the number of
unordered coincident-atom pairs to directed autocorrelation, which is exactly
consistent with the distance formulation.

The Cramer plane equations have the correct determinant/sign convention and
test membership in the entire two-dimensional plane. Weak sorted-coordinate
conditions then force the relaxed parameter chambers. For I.1, `p` is the
last gap; `p=0` gives equality of the two lists and is excluded. For I.2,
`p=A4-A3`; diameter positivity and weak gaps force `p>0`, and `q=2p` gives
equal lists. The two allowed lower endpoints remain noncongruent.

The separate encoding in `tests/test_six_integer_review.py:127-182` uses weak
nonnegative gaps when requested. Its shared last gap is just the same shared
r normalization. The three cancelled labelled edges have lengths `1-t,1,t`
on both sides; multiset subtraction of these occurrences remains valid when
values repeat or vanish. Twelve nonempty matching rows, with at most one
selected row per column, imply exactly one selection per row and per column
by the pigeonhole principle. The optional order rule matches occurrences of
one repeated value in increasing target-index order; such a bijection always
exists, including for zero-valued occurrences.

## 3. BF dependency audit and finite replay

BF assumes six-element subsets in G while applying Iw to their six-atom
projected **multisets**. Pushforward of directed autocorrelation under a group
homomorphism preserves equality and retains coincident projected atoms.
Its hypothesis is a noncongruent real projection, exactly Iw's domain. It
does not apply Iw to the separate congruent-projection branch.

The normalization in G uses actual vertices as translation anchors. Its p,q
are initially only real projected parameters; the written proof does not
assume they lift before checking the universal presentations. Both signs are
retained for edges with zero real height, even if the corresponding difference
in G is nonzero torsion. Nonzero increasing real differences force the positive
sign. These are the exact compatibility conditions used in the matching audit.

The existing independent `bloom_audit` was replayed in this session, without
calling Smith/Hermite routines or a solver. It reconstructed both coefficient
lists and all exceptional slopes, independently enumerated every signed
matching, checked both row-lattice inclusions for every matching, checked each
representative's unimodular transformations, and evaluated every saved Bloom
identity. Results:

- 282 signed matchings: I.1 counts `1,128,16,4` at generic, 3, 4, 5; I.2 counts
  `1,128,4` at generic, 3/2, 5/3.
- 21 labelled presentations; 210 pairwise lattice distinctions checked.
- 19 explicit Bloom identities and two forced-collision presentations.
- Inventory: eight free-rank-two torsion-free, three free-rank-one
  torsion-free, eight free-rank-one with C2.
- 8,460 exact row identities checked.

These checks establish the finite BF step conditional on Iw. They do not
independently establish Iw's real-domain UNSAT step.

## 4. Reproduction and hashes

Estimated compute was below one second; the actual arithmetic replay was
about 0.09 seconds, and the whole control invocation finished below one second.
No expensive census or SMT query was launched.

The following read-only pinned-environment command was run from the repository:

```bash
.venv/bin/python - <<'PY'
from pathlib import Path
import sys, hashlib, json
sys.path.insert(0, 'src')
sys.path.insert(0, 'tests')
from six_integer_smt import encode
from test_six_integer_review import model, formal_audit
from test_six_cylinder_branches_review import bloom_audit
s,_=encode(timeout_ms=60000,normal_forms=True,proof=True)
for pts in [('0','a1','a2','a3','r','1'),('0','b1','b2','b3','r','1')]:
    for x,y in zip(pts,pts[1:]):
        s=s.replace(f'(assert (< {x} {y}))',f'(assert (<= {x} {y}))')
assert s==Path('results/2026-09-30-six-integer-weighted-two/weighted.smt2').read_text()
print('Weighted builder byte-match:',hashlib.sha256(s.encode()).hexdigest())
s=model(weighted=True,order_matches=True)
assert s==Path('results/2026-09-30-six-integer-weighted-review-ordered/gap-bijection.smt2').read_text()
print('Weighted checker byte-match:',hashlib.sha256(s.encode()).hexdigest())
print('Formal exact controls:',json.dumps(formal_audit(),sort_keys=True))
print('BF finite certificate replay:',json.dumps(bloom_audit(Path('results/2026-09-30-six-bloom-cylinders.json')),sort_keys=True))
PY
```

Builder input SHA256:
`f3e837ef369ed1a9df3d37573a17b4dbaa9834f941216786b2a540c748ab19f6`.
Independent checker input SHA256:
`e8a9bcf7c94c9f3c8c352b92ea8a22a48872cd723463a6d2bdbe61740cbccb30`.
Formal controls passed both normal-form coefficient identities, the formal
Bloom autocorrelation, the explicit rigid substitutions and eight rigid-motion
controls. Existing solver metadata reports Z3 UNSAT and eagerly checked cvc5
1.4.1 UNSAT; those reports are historical evidence, not a new solver replay.

## 5. Requested external-model review

The coordinator reported that the exact Claude Opus 5.5 invocation returned
HTTP 429 for the account's weekly quota; the returned assistant record had
model `<synthetic>`. No Opus verdict or substantive objection was produced
for this reviewer to triage. None of the observations above is attributed
to Opus. The failed requested invocation does not add adversarial review
evidence for the theorem.
