# Independent composite Bloom arithmetic audit

30 September 2026. **[COMPUTED]**, exact integer arithmetic. This audit
imports neither the point enumerator nor its canonicalization. It reads
the direct certificates, reconstructs parameter orbits by permutations
of the cubic-root triple, and checks every parameter's unique location
using independently listed collision equations. It also derives support
counts by all 4096 subsets of the twelve-line arrangement and exact
two-column Smith factors.

The eleven moduli are 169,221,247,289,323,361,403,529,637,961,2197.
They cover 7,054,931 parameter candidates and 581,586 Bloom pair fibers.
Every saved fiber is exactly a twelve-element orbit; the replay checks
every excluded parameter and every admissible parameter. The two methods
agree on all full image counts and the F/L/H domain counts in `summary.json`.
The complete cyclic six-subset census remains 6..135: the larger checks
enumerate only the classical two-parameter image.

| n | Full image pairs | H pairs | L pairs | F pairs |
|---:|---:|---:|---:|---:|
|169|2212|2212|1274|338|
|221|3850|192|192|192|
|247|4838|288|288|288|
|289|6672|6672|4488|2312|
|323|8372|1152|1152|1152|
|361|10500|10500|7410|4332|
|403|13132|1200|1200|1200|
|529|22792|22792|17204|11638|
|637|33180|3696|672|0|
|961|76000|76000|62000|48050|
|2197|400038|400038|227474|57122|

H requires six distinct entries in every prime-power projection. L adds
unit e,d; F requires six distinct entries modulo every prime divisor.
The general domain theorems require every prime divisor at least13;
n637 is an explicit small-prime control outside that scope. Full-image
fiber observations at mixed-prime products are not a universal proof.

The elementary odd-modulus support formula and exact proof scopes are in
`notes/2026-09-30-six-composite-counting.md`, with the separate attack in
`notes/2026-09-30-six-composite-review.md`. The Smith/gcd arrangement
counting framework is established prior art, credited in the renewed
literature note. No novelty or all-modulus disjoint classification is
claimed by this audit.

Reproduce with the pinned environment:

```bash
.venv/bin/python src/six_composite_arithmetic.py > results/2026-09-30-six-composite-arithmetic/replay.log
.venv/bin/python tests/test_six_composite_arithmetic.py > results/2026-09-30-six-composite-arithmetic/tests.log 2>&1
```

All eleven bindings passed in 14.362 seconds of recorded per-certificate
audit time. The five regression groups pass in 8.027 seconds, including a relative
input-path regression added for the later boundary-control replay. These tests
independently check actual six-coordinate support counts at every odd
n3..121, individual Smith kernel counts, and actual reference canonical
classes and interval vectors on the regular domains at 13,17,19,31,169,221.
The direct enumerator separately agrees with the immutable reference on
every complete parameter image n2..43 and replays all larger saved fibers.
Each audit record binds the input certificate SHA256. Current arithmetic
source digest:

    c7f23749256b8c1abe168a221f52b0835fb1f1a1740a5931ccccabd72a02f7b4

No floating-point calculation, default Python/NumPy environment, or
reference-file edit is used.
