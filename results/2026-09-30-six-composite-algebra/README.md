# Exact ring-lift and reflection certificates

30 September 2026. **[COMPUTED] exact proof certificates**, independently
reconstructed and accepted in `notes/2026-09-30-six-composite-review.md`.
The full algebraic arguments are in `notes/2026-09-30-six-composite-algebra.md`;
the precise scope and remaining global obstruction are in the counting note.

`lift-table.json` retains all 32 type-E and 8 type-D paired singular
matching systems. `endpoint-lift-table.json` retains all 16 type-E and
8 type-D single-endpoint systems. Each record contains the exact transport
matrix, all residual integer rows, their scalar gcd and a Bézout witness.
Nonzero gcds have only2/3 prime divisors. These fixed finite tables establish
general lifting statements for every p≥13 and every power, rather than
inferring them from sampled moduli.

`certificate.json` independently records formal point permutations, all
fifteen reflection matchings for each endpoint, and exact anchored-point
partitions: full/faithful/regular169 and faithful221. Every endpoint in those
partitions was checked against the immutable reference canonicalization and
interval vector. The new regression tests independently derive centered
matrices from the literal raw coordinates, construct all coupled systems
and their Smith forms, and verify the reflection cosets directly.

Reproduce:

```bash
.venv/bin/python src/six_prime_power_lifts.py
.venv/bin/python src/six_prime_power_endpoint_lifts.py
.venv/bin/python src/six_composite_auxiliary.py
.venv/bin/python tests/test_six_prime_power_lifts.py
```

Three regression groups pass in0.067 seconds. The first two outputs have
deterministic hashes including their source digests:

    lift-table.json
      02eb646237f2821b7a029675256c1bd1b1c4b780cf04e01604b88d7981e545c8
    endpoint-lift-table.json
      eb02da0114f9518eb885f164ab4a1337f0ae03c7f09960fcdd25bddc7a558732

The auxiliary output records elapsed times, so its full byte digest changes
on regeneration; its mathematical content is checked independently. The
frozen reviewed copy is bound in the review by
`428d2543250f74dbc04c655f0d4f597615bb58c2beed4ad1dc51f2ee6a8f8f7b`.
No reference source, reference test, or data file was edited. No Lean,
external peer review, or novelty claim is implied.
