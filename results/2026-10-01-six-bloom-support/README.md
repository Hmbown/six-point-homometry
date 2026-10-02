# All-modulus support evidence

The exact support formula and its elementary proof are in
`notes/2026-10-01-six-bloom-support.md`; the separate fresh attack is
`notes/2026-10-01-six-primary-review.md`.

`certificate.json` retains all primitive coordinates of additive orders
2..8 lying on multiple raw collision kernels, every membership histogram,
the independent 4096-subset Smith weights, the source digest and all direct
parameter checks for n1..135 (829260 locations). These are parameter
checks, not a six-subset census. `tests.log` and `audit.log` retain the
five test groups and progress/timing.

```bash
.venv/bin/python tests/test_six_bloom_support.py
.venv/bin/python src/six_bloom_support.py --nmax 135 --out results/2026-10-01-six-bloom-support
```

The elementary exact-order argument and the Smith calculation use
separate methods. Fresh literal point reconstruction at n1..100 and a
different collision catalogue independently agree. The source includes
congruent endpoints; its count must not be divided by twelve without
the separately reviewed AP pair-fibre theorem.
