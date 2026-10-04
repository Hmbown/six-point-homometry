# Provenance and research status

This is a standalone mathematical extraction dated 1 October 2026. It starts
a new Git history and contains selected committed source, proofs, tests and
certificates from the research checkpoint identified in
[EXPORT_MANIFEST.json](EXPORT_MANIFEST.json).

That manifest binds every inherited file to its upstream SHA-256 and its
exported SHA-256. Most files are unchanged. Private machine-path prefixes
were redacted from a few historical descriptions. Two review notes omit
explicitly identified, unrelated media passages and carry an export notice.
Those edits do not change their mathematical arguments, hypotheses or
acceptance boundaries. Every transformation is recorded separately.

The reference `src/homometry.py`, `tests/run_tests.py` and `data/` are copied
unchanged. Raw computational inputs remain unchanged so historical input
hashes and resumable checker bindings remain meaningful. A historical digest
receipt describes its original checkpoint; it can also name an out-of-scope
file that is not part of this extraction. Use
[PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json) for the exact current package
inventory and exported file hashes.

The research was developed with AI assistance. Separate AI-assisted agents
performed internal adversarial reviews and independent arithmetic checks.
These are not human expert endorsements, external peer review or a complete
proof-kernel formalization. No historical novelty conclusion is inferred from
unsuccessful literature searches. Dated notes sometimes describe a gap that
was closed by a later note; the [result map](RESULTS.md) identifies current
and superseded scopes.

Two earlier manuscript PDFs and their editable mathematical sources are
included for reading convenience. The latest AP and weighted extensions are
in the dated proof notes, not retroactively included in those manuscripts.
Third-party papers are referenced by source links instead of being bundled.

The original research archive is retained separately by its owner. It is not
a dependency of this checkout. No authorship, reuse license, journal
acceptance or external validation is created by publishing this package.

## Authorship, 4 October 2026

The owner of the research archive, **Hunter Bown**, is the author of this
package and is responsible for its claims. The mathematics, code, exposition
and in-house adversarial reviews were produced with substantial assistance
from AI language-model agents working under the author's direction, and the
agents wrote first drafts of most proofs and documents. This disclosure
replaces the earlier "Homometry Program" placeholder. It changes no
mathematical statement. The same date added Lean 4 proofs of the elementary
soundness lemmas (`formal/`), an independent Ethos replay of the cvc5
certificates behind Theorems I and Iw (`tools/proof_replay/`), an attempted
solver-free re-derivation of Iw that terminates for four and five atoms but
not six (`tools/iw_enumeration/`), a prose specification of the low-rank checkers
(`docs/LR_CHECKER_SPECIFICATION.md`), a primary-source check of four
historical references (`docs/literature/`), and citation and release files
(`CITATION.cff`, `.zenodo.json`, `docs/RELEASE.md`). No license, DOI,
public visibility or external review exists at this date.
