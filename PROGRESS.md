# Mathematics package progress

## 1 October 2026 — standalone sharing package

- Package the reviewed six-point grammar G, all-modulus Bloom theorem AP
  and support count, with weighted phase-retrieval extensions.
- Trace and retain complete proof/certificate dependencies, separate attacks
  and regenerating sources; exclude unrelated application and media assets.
- Add a clear mathematical overview, portable installation, a bounded check
  suite and an explicit map to heavier computational obligations.
- Verify in an isolated standalone checkout, audit local links and exported
  paths, and record copy provenance without importing private Git history.
- Runtime allocation: fifteen CPU minutes for packaging checks; document
  longer exhaustive runs instead of silently claiming they were regenerated.

**[COMPUTED] Standalone verification passed.** A fresh Python 3.12.12
environment installed all five pinned requirements; dependency consistency
passed. The isolated certificate suite completed all 18 commands in 66.62
seconds without timeouts. It covers the protected reference runner, AP and
support checks, generator/replay, weighted examples and their independent
checks, four structural/finite certificate checks, 18 package-audit regression
fixtures and three real-subprocess verification-runner regressions.

```sh
python -m pip install -r requirements.txt
python -m pip check
python scripts/verify.py --suite certificates
python src/six_generate.py 21 0,1,3,7,10,15 0,1,4,7,14,16 --out .reproduction/example.json
python src/six_generate.py --replay .reproduction/example.json
```

The documented example independently replays successfully. All inherited
archive bytes are bound by the export manifest; tests run in a temporary copy.
This sharing turn does not regenerate the complete census, all 315 structural
strata or all solver proof objects. See [PACKAGE_REVIEW](docs/PACKAGE_REVIEW.md)
for the separate packaging review and [REPRODUCING](docs/REPRODUCING.md) for
the remaining exact proof obligations.

The [condensed outline](docs/PROOF_OUTLINE.md) received a separate read
against Theorem G. It retains compositions, the finite-order bound, all free
rank/projection branches, integral lattices and specialization caveats.
G is relevant structural progress toward Erickson–Jones Problem 5.2;
complete disjoint classification and all-family enumeration are unresolved.

Git history starts with this mathematics-only extraction. The requested
GitHub destination is `Hmbown/six-point-homometry`; use private visibility
until a public-access preference is supplied. Hosted CI is a separate gate
from this local verification. This extraction adds no new theorem, establishes
no novelty or external peer review, and selects no reuse license.
