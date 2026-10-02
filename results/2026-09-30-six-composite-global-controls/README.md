# Boundary controls for the full coprime-to-six theorem

Started30 September, completed1 October2026. **[COMPUTED]**, independent
actual-coordinate and cubic-root-permutation methods. These controls
supplement the eleven larger images in the earlier composite directory.
They enumerate the Bloom parameter image, not all six-subsets.

| n | Full Bloom pairs |
|---:|---:|
|25|30|
|35|72|
|49|154|
|55|200|
|65|290|
|77|420|
|91|602|
|121|1100|
|143|1562|
|187|2728|
|209|3432|
|341|9350|

All twelve images have exactly one G-orbit of size12 in every pair fiber,
no congruent endpoints, and agree with
`((n−1)(n−11)+24[5|n]+24[7|n])/12`. At341 the five shared endpoints
form exactly the inherited31 cycle inflated by11; all other components
are isolated edges. The complete original six-subset census stays6..135.

The new controls cover255732 parameters and19940 pair fibers. Together
with the previous eleven exact images this gives23 sampled moduli,
7310663 candidates and601526 pair fibers, largest parameter-image modulus2197.
The mathematical theorem instead depends on the finite coefficient-matching
classification and its fresh attack, not these sample moduli.

Reproduce:

```bash
.venv/bin/python src/six_composite_bloom.py --moduli 25 35 49 55 65 77 91 121 143 187 209 341 --out results/2026-09-30-six-composite-global-controls --resume
.venv/bin/python src/six_composite_arithmetic.py --direct results/2026-09-30-six-composite-global-controls --out results/2026-09-30-six-composite-global-control-audit
```

Direct enumeration finishes the largest341 image in0.674 seconds. The
independent arithmetic replay of all twelve takes0.550 seconds of summed
certificate-audit time. Exact fibers, excluded parameters, source hashes
and all independent location/orbit checks are retained. The first arithmetic
invocation failed because the CLI did not resolve a relative input path;
that path handling was fixed, a regression test added, and all23 images
were rerun successfully. The initial failure log is retained alongside the
successful logs in the parent results directory. No mathematical result
was inferred from that failed invocation.
