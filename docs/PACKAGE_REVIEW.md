# Independent mathematics-package review

1 October 2026. This is an AI-assisted packaging review performed by an
agent separate from the exporter. It examines scope, provenance, portable
execution and evidence availability. It is not a new adversarial proof
review, external specialist endorsement or historical-priority determination.

## Initial findings and changes

The reviewed overview and result map distinguish the complete six-point
generating theorem G from the classical Bloom image theorem AP, pair-edge
counts from maximal-family counts, and finite census evidence from the
arbitrary-modulus reductions. Weighted statements retain their prescribed
support, genericity and enlarged-equivalence hypotheses. Internal proof
acceptance, external peer review and historical novelty are kept distinct.
No unresolved publication overclaim was identified in those documents.

A definition precision issue was identified: unordered pair-distance
multisets determine autocorrelation when cardinality is fixed, but the
empty and singleton sets both have an empty pair-distance multiset.
The six-point statements are unaffected. The result map now explicitly
includes the equal-cardinality condition; the corrected wording was re-read.

The export has ten transformed historical files. Each was compared with
its actual blob at source checkpoint
`e48e0ed9f6e6ae088dd41b3d444fd12f73e6a436`, and both recorded SHA-256 values
were checked. Eight changes are local-path substitutions. The other two
add an export notice and omit the explicitly described media review and
media chronology. The mathematical equations, hypotheses and proof-acceptance
boundaries in those differences are retained. Numerical certificate files
are unchanged. The [export manifest](EXPORT_MANIFEST.json) identifies these
transformations individually; historical review digests still describe their
original checkpoints.

The new audit makes missing proof dependencies a failure separately from
hash mismatches. Its required inventory includes G's line/weighted-atom,
bounded-cylinder, rigid-template, Bloom-cylinder, free-rank, low-rank and
finite-torsion proofs and reviews; all finite pair and census tables through
135; AP/support and weighted evidence. It scans both raw files and gzip
certificate contents for private paths and recognizable credentials, rejects
public media/application assets and unexplained archive types, checks local
Markdown files and heading targets, and checks Python source for parent
checkout references. Symlinks are rejected.

The workflow's action references were checked against the official
[checkout v7](https://github.com/actions/checkout/releases/tag/v7) and
[setup-python v7](https://github.com/actions/setup-python/releases/tag/v7)
release records. Both tags exist. This check does not establish a successful
hosted CI run.

**[COMPUTED]** Eighteen adversarial audit regression cases pass. They cover
changed bytes, omitted dependencies and manifest entries, invalid transformation
metadata, duplicate entries, broken or escaping links, hidden compressed
content, invalid UTF-8/compression, secrets, symlinks and parent paths.

## Acceptance gate

**[COMPUTED] The independent package-integrity audit passed:** 2,448 public
candidate files, 2,428 inherited files, ten transformed historical files
(two scope-edited), 83 Markdown files, and zero findings. The audit's eighteen
regression cases also pass. The checked package includes the condensed proof
outline. The actual executed commands were `python3 tests/test_repository_audit.py`
and `python3 scripts/audit_repository.py`.

**[COMPUTED] The isolated certificate suite passed all eighteen commands**
in a fresh Python 3.12.12 environment with the five pinned dependencies.
The exporter executed the suite, and this reviewer independently read the
receipt: every exit code is zero, no command timed out, and total elapsed
time is 66.622 seconds. The receipt explicitly records
`full_exhaustive_regeneration: false`.

Those commands cover the immutable reference and environment controls,
AP/support/independent-AP controls, generator and replay checks, four weighted
test programs, the eighteen audit fixtures, three wrapper isolation/failure/
timeout tests, and cylinder/high-rank/low-rank-mechanism/finite-torsion replays.
They do not regenerate the complete census, full low-rank DAG or all SMT
proof objects. The exact receipt and logs are generated under the ignored
`.reproduction/verification/` directory.

The package is accepted for mathematical inspection at those explicit
verification boundaries. The public manifest must be refreshed after the
final documentation edit, then the integrity gate rerun before freezing the
repository. Reproduce from the repository root:

```sh
python tests/test_repository_audit.py
python scripts/audit_repository.py
python scripts/verify.py
python scripts/verify.py --suite certificates --timeout 600
```

The first command checks the audit's rejection behavior. The second checks
the exact current package. The third executes its documented mathematics
suite in a temporary copy. The [reproduction guide](REPRODUCING.md) separates
that bounded suite from independent certificate replays and full regeneration.

## Limits of this review

The audit requires every candidate public file except the public manifest
itself to have a matching entry in [PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json).
The inherited assets additionally need an entry in the export manifest.
These checks bind the recorded package bytes. On a fresh clone, the upstream
commit's actual objects must be supplied independently to authenticate the
source origin; a self-contained hash list is not an outside signature.

Presence and integrity of a proof or certificate do not verify its mathematical
predicate. This packaging turn does not regenerate the full census, full
low-rank structural cover or all SMT proof objects. The separate original
attacks and documented checker obligations remain part of the trust boundary.
The proofs' theorem status, unresolved historical priority, absent external
peer review and absent complete proof-assistant validation remain as stated
in the [result map](RESULTS.md). No license or authorship conclusion is added.

## Hosted-runtime follow-up

The initial Linux quick CI run reached `tests/test_weighted_six_review.py`
and timed out at its unchanged 180-second command limit. Earlier gates
passed. This is a failed hosted verification gate; the prior local pass
does not supersede it. The timed-out program performs exact SymPy/Fraction
arithmetic and has no NumPy or numerical SVD dependency.

**[COMPUTED]** This reviewer independently reproduced a seed-0 timeout
after two completed checks using a four-second diagnostic limit. Seeds
1, 2, 3, 4, 5, 10, 42 and 999 each completed all four assertions in
0.65–0.81 seconds. Other seed-0 diagnostics can pass, so the observed
failure is a possible stall, not a claim that every seed-0 invocation fails.
These controls identify runtime variability; they do not prove an upstream
SymPy defect or alter the theorem's mathematical predicates.

The wrapper now starts every checking subprocess with `PYTHONHASHSEED=1`
and `PYTHONUNBUFFERED=1`. This makes the selected hash order reproducible
and retains progress output if a gate stalls. A real subprocess regression
checks that even a caller providing seed 0 is overridden before Python
starts; this reviewer reran all three wrapper tests successfully. All
mathematical sources, assertions and timeout/failure behavior are retained.

The corrected full local suite and corrected hosted run remain pending at
this follow-up checkpoint. Their eventual results must be recorded separately;
the runtime adjustment alone is not a successful CI result.
