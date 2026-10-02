# Exploratory routes set aside during the six-note proof

30 September 2026. **[COMPUTED] bounded experiments and implementation
controls only. None of the completeness proof depends on these routes.**
All original outputs are preserved. The successful replacement was the
weighted-real projection split, exact height-arrangement cover, and
independently reviewed integral quotient DAG.

## 1. Centered-moment elimination

`src/six_moments.py` uses Newton identities for six centered roots, computes
even moments of the directed difference multiset, and eliminates some
elementary-symmetric coordinates between two candidate root multisets.
Its preserved algebra is in `results/2026-09-30-six-moments-explore.json`
and the corresponding `.log`. The calculation reaches necessary polynomial
relations through moment20. It does **not** solve the resulting real
algebraic system, prove that its solutions are exactly T/I or Bloom, or
handle finite-characteristic denominator exceptions. It was therefore set
aside as a proof route, rather than being interpreted as a classification.

The new test `tests/test_six_moments.py` constructs elementary symmetric
functions directly from root combinations and independently sums powers
and differences. It checks 434 direct-root identities through power30,
ten symbolic two-root controls (including degrees above the root count),
and seven exact Bloom parameter choices. Three choices have repeated
support points, and five exercise a nonzero elimination parameter. Every
saved symbolic expression is compared with a fresh derivation; a
nonhomometric six-point perturbation is a negative control. The tests pass
in about two seconds. These checks verify the algebra, **not** completeness
of the moment equations.

The displayed reduced expressions have denominators involving 2,11 and13;
centering itself can introduce division by6. No modular consequence is
asserted at primes dividing those quantities, and no general modular
classification is deduced at other primes either.

```
.venv/bin/python tests/test_six_moments.py
```

Recorded test output: `results/2026-09-30-six-moments-tests.log`. The
exploratory generator can be rerun with `.venv/bin/python src/six_moments.py`,
but doing so overwrites its two same-name report files when redirected;
the original outputs were not regenerated during this bookkeeping task.

## 2. Unrestricted circle SMT with affine-plane exclusions

The exact real-circle encoding and controls are documented in
`notes/2026-09-30-six-templates-circle.md`. Preloading 583 signed-matching
affine planes from the census through24 did not produce an UNSAT proof:
the folded-distance encoding returned `unknown` at15 seconds, and the
direct equality-or-sum-one encoding returned `unknown` at30 seconds.
These timeouts neither prove a missing family nor establish completeness.

An unseeded three-step control found exact valid models at n=96,224,12 and
learned five additional planes. Its matching cap was100 per model. The
last `sat` in that original report refers to the query before the final
plane exclusions; the final saved formula was not queried. Current code
makes that distinction explicit. Independent controls verify the588 saved
affine row spaces, six solver fixtures, and6,435 reference canonicalizations.
No theorem relies on exhausting these affine planes.

```
.venv/bin/python tests/test_six_templates_circle.py
```

Preserved folders: `results/2026-09-30-six-templates-circle/`,
`...-circle-direct/`, and `...-circle-unseeded/`, plus their dated logs.

## 3. Unrestricted oriented-star quotient search

`src/six_star_quotient.py` groups96,096 oriented five-edge selections into
107 vertex-permutation/global-reversal orbits, then attempts a quotient
DAG without the height-stratum restriction used in the completed proof.
The orbit reduction has an independent test, but the unrestricted DAGs
are intentionally capped and unfinished:

| output folder suffix | nodes | completed roots | elapsed | complete |
|---|---:|---:|---:|---|
| `six-star-quotient` | 5,000 | 6 | 4.04s | false |
| `six-star-quotient100k` | 100,000 | 11 | 104.66s | false |

The larger run stops with `benchmark bound`; only11 of107 roots are
complete. Its2,955 homometric terminals are discovery output, without the
full independent lattice/branch cover or structural classification needed
for a proof. They are not used in place of the completed315-stratum DAG.

`tests/test_six_star_quotient.py` independently reconstructs the full
107-orbit partition using all vertex permutations. It also checks a small
completed search and an intentionally capped search, ensuring that the
completion flag distinguishes them. It does not make the100,000-node
artifact complete.

```
.venv/bin/python tests/test_six_star_quotient.py
```

Both saved `summary.json` files and `dag.json.gz` files remain intact.
The failed unrestricted approaches motivated a different reduction, rather
than a larger unreviewed search budget or a claim that capped residuals were
sporadic. The accepted proof dependencies are listed in
`notes/2026-09-30-six-generation.md` and its separate reviews.
