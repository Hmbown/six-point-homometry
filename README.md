# Six-point homometry in finite cyclic groups

Different finite sets can have exactly the same pairwise distance multiset.
This repository studies that ambiguity for six-element subsets of
$\mathbb Z/n\mathbb Z$, up to translation and reflection.

It contains a computer-assisted generating grammar for **every cyclic
modulus**, an exact classification and count for the **classical Bloom
construction**, and extensions to weighted cyclic phase retrieval. It also
includes a general signed-matching reduction and an exact inverse tool for
binary configurations on periodic grids of any dimension and cardinality. Full
arguments, separate adversarial reviews, checking code and computational
certificates are included.

**Author:** Hunter Bown. **Research status:** working research produced
with substantial AI assistance under the author's direction, with internal
adversarial review; see [provenance](docs/PROVENANCE.md). The principal
proofs are tagged **[PROVED], in-house, computer-assisted**. The elementary
soundness lemmas and one reduction step are additionally machine-checked in
Lean 4 ([formal/](formal/README.md)); the weighted six-atom line theorem has
a second, solver-free derivation ([tools/iw_enumeration/](tools/iw_enumeration/README.md)).
External peer review and historical novelty remain unresolved. The Bloom
construction and other classical antecedents are explicitly credited, and
four historical sources were checked at first hand on 4 October 2026
([log](docs/literature/2026-10-04-four-sources-primary-check.md)).

## Main results

| Result | Scope | Read |
|---|---|---|
| **G: complete generating grammar** | For every $n$, the connected components of the construction graph on six-element translation/reflection classes are exactly the homometry classes. Compositions are allowed. | [Proof](notes/2026-09-30-six-generation.md) · [Separate review](notes/2026-09-30-six-generation-review.md) |
| **AP: classical Bloom pair classification** | Classifies the parameter fibres of the classical two-parameter construction for every $n$, including even and composite moduli. | [Proof](notes/2026-10-01-six-bloom-primary.md) · [Separate review](notes/2026-10-01-six-primary-review.md) |
| **Exact Bloom count** | Counts distinct nontrivial unordered pair edges in that construction: $B(n)=\lvert\Omega_n\rvert/12-2[12\mid n]$. This is a count of one construction's pair edges. | [Support formula and proof](notes/2026-10-01-six-bloom-support.md) |
| **Weighted phase-retrieval extensions** | Same-support ambiguity, reconstruction and stability modulo subgroup freedoms; aperiodic positive ambiguity; an exact six-support comparison. | [Subgroup proof](notes/2026-10-01-weighted-subgroup.md) · [Six-support proof](notes/2026-10-01-weighted-six-incidence.md) |
| **General reduction GM** | Every cardinality and abelian group; bounded torsion at every rank, cyclic cylinder reduction, and matching-specific exact integer lifts. A compact all-cardinality grammar remains open. | [Proof](docs/general_matching/GENERAL_MATCHING.md) · [Review](docs/general_matching/GENERAL_MATCHING_REVIEW.md) |
| **Exact inverse tool IG** | Reconstructs all binary configurations on finite periodic grids, modulo translation/global inversion, with explicit complete/partial results. Worst-case search is exponential. | [Use the tool](tools/inverse_grid/README.md) · [Proof](docs/general_matching/INVERSE_GRID.md) · [Benchmarks](docs/INVERSE_GRID_BENCHMARKS.md) |

| **Lean-checked soundness** | L2, L3\*, L4, L5, L7, the dyad identity and the Bloom factorization are proved in `ℤ[G]` for every abelian group `G`; the finite-union-of-subspaces step is proved for every infinite field. No `sorry`. | [formal/README.md](formal/README.md) |
| **Second derivation of Iw** | Exhaustive exact branch-and-bound over sorted interval orders, no SMT solver, standard library only. Result recorded in the tool's README. | [tools/iw_enumeration](tools/iw_enumeration/README.md) |
| **What the LR checkers verify** | Prose specification of every obligation checked by the two independent low-rank checkers, and of what remains prose. | [docs/LR_CHECKER_SPECIFICATION.md](docs/LR_CHECKER_SPECIFICATION.md) |

[Condensed proof outline](docs/PROOF_OUTLINE.md) · [Detailed result map](docs/RESULTS.md)
· [References and attribution](docs/REFERENCES.md)
· [Reproduction guide](docs/REPRODUCING.md) · [Provenance](docs/PROVENANCE.md)

For an independent assessment, use the [precise claim and proof summary](docs/ASSESSMENT_REPLY.md)
with the linked full proof and component certificates.

The [universal mathematical formulation](docs/UNIVERSAL_THEOREM.md) states
the classical equivalence between autocorrelation, Fourier magnitudes,
spectral-unit convolution and every displacement-dependent pair functional.
It applies to all finite abelian groups and support sizes. G adds a
constructive grammar within the six-point binary constraint; the universal
identity and unrestricted factor reversal are established prior work.

## A concrete example

In $\mathbb Z/21\mathbb Z$, the sets

```text
A = {0, 1, 3, 7, 10, 15}
B = {0, 1, 4, 7, 14, 16}
```

have the same cyclic interval multiset and represent different
translation/reflection classes. The certificate driver explains this pair
and can replay the explanation independently of the discovery search.

## Try it

The new exact inverse tool uses only the Python standard library. From the
repository root, recover every arrangement compatible with the example's
pair counts and replay the result:

```sh
python -S tools/inverse_grid/src/inverse_grid.py solve --input tools/inverse_grid/examples/tetrachord-12.json --out .reproduction/inverse-example.json --checkpoint .reproduction/inverse-state.json
python -S tools/inverse_grid/src/inverse_grid.py verify --input .reproduction/inverse-example.json --recompute
```

It returns both four-point classes. For your own exact data, provide the
grid periods and directed displacement counts, including diagonals;
omitted bins mean zero. The [tool guide](tools/inverse_grid/README.md)
includes multidimensional inputs, the Python API, limits and resume commands.

Use **Python 3.12**. From a clone of this repository:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/verify.py
```

The default verification runs in a temporary copy and preserves the archived
certificates. It checks reference conventions, the environment, complete saved
Bloom tables, certificate generation/replay and weighted examples. It does
not rerun every exhaustive proof computation.

Generate and replay an explanation:

```sh
python src/six_generate.py 21 0,1,3,7,10,15 0,1,4,7,14,16 --out .reproduction/example.json
python src/six_generate.py --replay .reproduction/example.json
```

Saved certificates also demonstrate composed finite paths and very large
moduli. Their replay is portable. See the [full guide](docs/REPRODUCING.md)
for the independent proof checks, optional solvers and expensive regeneration.

## Evidence and limits

The archived complete six-subset census has two independent methods through
$n=135$. The arbitrary-modulus results depend on written reductions and
computational certificates. Their scope does not follow from extrapolating
the census.

G supplies constructions and connecting paths. Minimal generators, a
nonredundant classification of all constructions, all-modulus maximal-family
counts and arbitrary-cardinality completeness remain open. AP counts the
classical Bloom image; different pair edges can share an endpoint.
Multiplication by an arbitrary unit is not an extra equivalence relation.

Before relying on the universal claims, inspect their exact solver,
finite-cover and checker dependencies in the [result map](docs/RESULTS.md).
Internal review is evidence of scrutiny, not external validation.

## Repository layout

- `notes/`: full proofs, dated literature checks and separate attacks.
- `src/`: readable reference implementation, constructions and regenerators.
- `tests/`: reference regressions and independently written checking programs.
- `results/`: archived mathematical certificates and calculation records.
- `docs/`: result map, attribution, reproduction and extraction provenance.
- `scripts/`: portable verification and repository-integrity checks.

The included manuscript PDFs are earlier working expositions; the linked
proof notes above give the latest scopes. To reference this work, cite the
repository revision and the specific theorem/proof note; `CITATION.cff`
gives the metadata and `docs/RELEASE.md` the archiving steps. No reuse
license has been selected yet. Questions and mathematical corrections can
be recorded as repository issues.
