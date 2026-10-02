# Replaying a six-note generation certificate at arbitrary n

30 September 2026. **[COMPUTED] implementation and exact replay tests.**
The coverage contract depends on the separately reviewed arbitrary-n
six-note generation theorem and its BF/HR/LR/FT branches. This driver is
not a new proof or novelty claim.

`src/six_generate.py` accepts any positive modulus n>=6 and two lists of
six integer pitches. It normalizes pitches modulo n, rejects collisions
and nonhomometric input, and preserves T/I set classes. T/I-equivalent
inputs receive an explicit trivial certificate rather than a Z-relation
claim. A search failure on validated homometric input raises
`GenerationInvariantError`; it never becomes a negative homometry decision.

## Commands and Python interface

Generate a portable exact certificate:

```
.venv/bin/python src/six_generate.py 21 0,1,3,7,10,15 0,1,4,7,14,16 \
  --out results/2026-09-30-six-generate/benchmark21.json
```

To prefer the proved finite-family path whenever the ordinary support
quotient has size at most135, add `--prefer-finite`. This is useful when
showing compositions rather than another available direct identity.

Replay a saved certificate without loading the finite family tables:

```
.venv/bin/python src/six_generate.py --replay \
  results/2026-09-30-six-generate/missing-edge-inflated.json
```

The Python functions are `generate(n,A,B,prefer_finite=False)` and
`replay(certificate)`. Replay returns the actual ambient T/I path. The JSON
also records independent rigid alignments from the exact input endpoints
to the first and last canonical path vertices. Thus coordinates and chord
classes can be reconstructed rather than inferred from a mechanism label.

## What the certificate contains

The direct route records exact Bloom parameters, parallelogram dyad
parameters and its sparse mixed-periodic weight, a fixed block and its
motion for L2/L3*/L4/L5, an L7 subgroup order, or a rigid seed parameter.
All direct identities are replayed with exact integer Counters. The L3*
condition is P shifted by -s equals P*, with no assumption that s has a
modular half.

The finite route computes

    g=gcd(n, every coordinate in both anchored T/I representatives),
    q=n/g.

This is the ordinary subgroup supporting both point sets. Independent
translations to another vertex and inversion leave that subgroup unchanged.
For q<=135, breadth-first search in the proved saved finite table returns
a path, embedding every original edge record directly into the certificate.
Every edge is replayed with its original FT semantics, including the old
L3 halving condition, unit condition, and rigid seed numbering. Finally
x->g*x embeds every path vertex into Z_n. Ordinary inflation is explicit;
unit multiplication is never used to collapse chord classes.

The direct recognizer checks at most72 relevant rigid alignments: any
nontrivial block mechanism has a nonempty fixed block, so an image of one
B point must meet an A point. It checks every nonempty subset of that
intersection. Bloom candidates come from three distinct points specifying
0,p,q-2p, so no n-by-n parameter menu is required. Possible L7 orders are
2,4,6,12; L7 uses its own alignment to the disjoint complement, with at
most twelve candidates per subgroup. It must not reuse the block alignment
list, which requires an intersection with A. The thirteen rigid seeds require at most31 torsion parameters each.
All work is sparse in the six-point support; it allocates no n-entry vectors.

For n<=4096, validation explicitly agrees with the immutable reference ICV
and canonical form. Larger n uses exact fifteen-distance Counters and the
twelve anchored T/I candidates; these implementations are independently
regressed against the immutable reference on660 random small six-sets.
This avoids pretending the reference's O(n) allocation and translation
loop are practical at a billion divisions.

If q>135, a rank-zero universal presentation is impossible: its finite
support order would be at most135. The reviewed positive-rank branches
therefore guarantee one of the direct mechanisms. If q<=135, the proved
finite-family connectivity gives the fallback path. This is the precise
coverage justification, rather than an empirical extrapolation of a menu.

## Tests and saved outputs

```
.venv/bin/python tests/test_six_generate.py
```

The test recovers all73 previously missing direct edges as paths, checks
each saved edge again with the independent FT replay checker, and replays
all nine legacy certificate labels. It tests portable replay with table
access deliberately disabled and rejects tampered certificates.

Saved examples include:

- the high-rank22-note example inflated to220154 divisions;
- a Bloom pair in the prime modulus1000000007;
- all three proven non-shadow H families in6000018 divisions;
- a direct L3* example in3000090 divisions;
- a literal L7 complement with primitive support400012;
- a missing-edge composition inflated to1800054 divisions.

An additional12-note fixture has L3* move s=9, for which no modular half
exists; its exact generalized condition and T/I distinction are checked.
The direct classifier may give that pair a different valid mechanism,
since mechanisms overlap.

Certificates and the test summary are in
`results/2026-09-30-six-generate/`; the log is
`results/2026-09-30-six-generate-tests.log`. The protected reference, test
runner, census outputs and data files were not modified.

## Separate implementation review and repair

The separate driver reviewer found that the initial implementation reused
the intersecting block-alignment list for L7. Since the required complement
is disjoint from A, that made L7 discovery unreachable. The dedicated
`halfcoset_certificate` now aligns B directly to the complement. Regressions
exercise both the helper and the public driver at n16 and n400012, where
the driver actually returns L7. This was an implementation defect; the
reviewed L7 identity and mathematical completeness theorem were unchanged.

Replay also checks the advertised top-level `vertices` field whenever it
is present. A tampered display path is rejected even when its separately
embedded executable path is valid. The exact source/certificate/table
boundaries remain explicit.

The separate executable review is now **ACCEPTED** in
`notes/2026-09-30-six-generate-review.md`. Its independent checker is
`tests/test_six_generate_review.py`; the reviewed driver SHA256 is
`ef3c38eb59a3a2a18469cffdcdfe5e4559f246ebf0eb65ad719ba6d060ef6f30`.
The review checks candidate-search coverage as well as concrete certificates
and explicitly records the repaired discovery defect. This implementation
review is separate from the mathematical theorem's proof review.
