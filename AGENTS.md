# Maintaining this mathematics repository

This repository is a standalone extraction of mathematical research, code
and certificates. It contains finite cyclic homometry and weighted phase
retrieval. Keep applications, audio, scores and video outside this repository.

- Read `README.md`, `docs/RESULTS.md`, `docs/REPRODUCING.md` and `PROGRESS.md`
  before changing a mathematical claim.
- Preserve `src/homometry.py`, `tests/run_tests.py` and `data/` as reference
  assets. Add implementations and tests instead of altering their conventions.
- Run `python scripts/verify.py` for the bounded default verification suite.
  Full regeneration and independent proof-certificate replays are separate
  gates; see `docs/REPRODUCING.md` for commands and costs.
- Write a proof in full before using `[PROVED]`; retain a separate logged
  adversarial review. Internal AI-assisted review is not external peer review.
- Keep classical attribution, unresolved historical priority and every
  hypothesis explicit. Do not infer arbitrary-modulus claims from a census.
- Do not confuse pair-edge counts with maximal homometry-family counts, or
  quotient out multiplication by arbitrary units.
- Preserve inherited certificate bytes and hash manifests. Regenerated
  outputs belong in a temporary checkout or an ignored reproduction folder.
- Record substantive changes and exact verification commands in `PROGRESS.md`.

No open-source license has been selected. Do not add a license or infer human
authorship, external validation or publication status without owner direction.
