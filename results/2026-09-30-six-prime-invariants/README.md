# Independent invariant verification and finite-field controls

30 September 2026. **[COMPUTED]**; theorem proof/status/review:
`notes/2026-09-30-six-prime-theorem.md` and
`notes/2026-09-30-six-prime-review.md`.

The independent implementation counts all admissible parameters by the
polynomial key `(a²−ab+b², [ab(a−b)]²)`. It constructs no cyclic chord
classes and assumes no count formula. It compares its entire partition
with the direct point enumerator's saved fibers: every parameter is visited
once, every key fiber corresponds to one direct fiber, and each actual
saved pair's centered moments reproduce the same key. Equality of headline
counts alone would be insufficient for this replay.

Every prime13..251 plus1009 is checked:50 primes,2,013,650 parameter
candidates. At1009 both methods give83,832 pairs and167,664 vertices of
degree one. At31 the Bloom image has50 edges,90 degree-one vertices and
five degree-two vertices. All prime pair fibers have exactly12 parameters.
The dedicated algebraic replay initially took approximately5.2 seconds
over all prime certificates; timings are retained per modulus. Its
computation is parameter enumeration, not a complete six-subset census.

Independent direct additive-field checks construct F25,F49,F169 as
Fp[t]/(t²−d) with d=2,3,2 respectively. Anchored translation/inversion
canonicalization and algebraic invariant partitions agree on all parameters:

| Additive field | Pairs | Parameters per fiber |
|---|---:|---:|
|F25|40|12|
|F49|168|12|
|F169|2212|12|

These groups are `(Z/pZ)²`, not cyclic groups of order p². General scalar
multiplication or linear automorphisms are never quotiented out.

The tiny integer polynomial kernel verifies all moment identities,
homometry as an exact directed coefficient identity, the line determinant
set and the single-endpoint determinant. Regression tests include the
genuine shared-endpoint example in characteristic31, isotropic s=0,
the individual coefficient exceptions79/239, and independent immutable
reference partitions through43. These tests do not assume the theorem to
compute its invariant keys or the direct point images.

The small-prime census audit rechecks every displayed family member's
anchored T/I form, ICV, disjoint membership, family sizes and edge counts.
It records hashes and the two original methods. **Its completeness is
inherited from those complete census checkpoints; this replay is not a
new complete enumeration.** It verifies the four correction coefficients
used in Corollary E, including60 size-two families and one size-five
family at31. Complete two-method six-subset enumeration remains6..135.

The separate `composite-obstruction.json` retains the n221 CRT sign witness:
two distinct internally homometric T/I pairs have the same field invariant
key and all even centered moments/squared odd centered moments. The fresh
review's §8 independently checks it. This is an exact domain boundary,
not a composite count or a claim of homometry between the two pairs.

```bash
.venv/bin/python tests/test_six_prime_boundary.py
```

Reproduce in the pinned environment:

```bash
.venv/bin/python src/six_prime_bloom.py --primes 13..251 1009 --out results/2026-09-30-six-prime-count --resume
.venv/bin/python src/six_bloom_invariants.py > results/2026-09-30-six-prime-invariants/replay.log
.venv/bin/python tests/test_six_prime_bloom.py
.venv/bin/python tests/test_six_bloom_invariants.py > results/2026-09-30-six-prime-invariants/tests.log 2>&1
```

The direct checkpoints require their recorded source hash when resumed;
reproduction in a new output directory can omit `--resume`. `summary.json`
binds the invariant implementation hash, all50 direct file hashes and
the inherited small-prime census hashes. Full proofs concern arbitrary
fields/primes; the finite verification is supporting evidence.
