# Mathematics package progress

## 4 October 2026 — owner-directed release preparation (plan)

Owner direction received today: Hunter Bown is the named human author; AI
assistance is to be disclosed plainly. Five tasks, in order of credibility
gained per effort:

1. Authorship and disclosure: name the author on the manuscript, README,
   PROVENANCE and a CITATION file; remove physics/application framing from
   the mathematics package (keep classical crystallographic *references*,
   remove the measurement/"crystal" exposition). Success: no application
   claim remains; `scripts/verify.py` still passes.
2. Primary sources: attempt to read Yovanof 1988, Soderberg 1995,
   Patterson 1944 and Bullough 1961/1964 (web agent, separate dated note);
   update REFERENCES and the manuscript bibliography with whatever is
   verified. Success: each source has an explicit access status and any
   priority-relevant statement recorded verbatim.
3. Second derivation of Theorem Iw by a non-SMT method: an exact rational
   branch-and-bound over inclusion-respecting sorted orders of the fifteen
   interval lengths, with exact LP feasibility and affine-hull containment
   in the Bloom lines or the congruent locus. Success: every feasible leaf
   is certified Bloom or congruent; non-vacuity controls find the Bloom
   lines. Estimated compute: minutes to an hour, pure Python.
4. Lean 4/Mathlib formalization of the elementary core: block-move
   soundness (L2, L3*, L4, L5), half-coset complementation (L7), the
   finite-union-of-proper-subspaces step, and the Laplace-expansion bound.
   Success criterion is a compiling file with no `sorry`; partial progress
   is recorded honestly.
5. Prose specification of the LR quotient-DAG checker's obligations, and
   archive packaging (CITATION.cff, .zenodo.json, release tarball with
   hashes). Publishing a DOI or changing repository visibility is left to
   the owner; this task prepares the deposit only.

Each completed task gets its own commit in this repository.

### Outcome, 4 October 2026

**Task 1, authorship and scope — done.** Hunter Bown is named as author in
the manuscript title block and authorship section, README, PROVENANCE and
RESULTS; AI assistance is disclosed in each. `CITATION.cff` and
`.zenodo.json` added. The measurement/"crystal" exposition in
UNIVERSAL_THEOREM §4 was replaced by a neutral scope statement and one
INVERSE_GRID phrase was neutralized; cited paper titles are unchanged. The
manuscript recompiles (29 pages). The tex edit is recorded as a scope-edit
in EXPORT_MANIFEST; `scripts/update_manifests.py` (new) regenerates
PUBLIC_MANIFEST and records such edits. `scripts/audit_repository.py` now
accepts `.lean`, `.cff`, `lean-toolchain` and `.zenodo.json` and requires
the new assets. Audit: pass.

**Task 2, primary sources — done to the extent accessible.** Web agent
report in `docs/literature/2026-10-04-four-sources-primary-check.md`:
Yovanof 1988 read in part (USC viewer; distinct-distance scope only, "no
attempt" at cyclic sets); Soderberg 1995 p. 77 only; Patterson 1944
abstract only; Bullough 1961/1964 first pages only. Goyette 2012 and
Callender–Hall 2008 verified (the handout's real title is "Crystallography
and the structure of Z-related sets"). Nothing read states a six-point
generating theorem or the repeated-distance classification. REFERENCES.md
and the manuscript bibliography updated with exact reading scopes.

**Task 3, independent check of Iw — done by proof-checker replay; the
enumeration route failed at six atoms.** `tools/proof_replay/`: the three
saved cvc5 1.4.1 CPC proofs (Theorem I in the builder's count encoding and
the reviewer's gap/bijection encoding; Theorem Iw in the gap/bijection
encoding) check as `correct` in Ethos 0.2.5 built at commit
`08e4aa40c4f8a6e00833f10e8d8985777e424027`, the commit cvc5 1.4.1 pins,
against the CPC signature from the cvc5 1.4.1 source, with
`--require-proof-of-false`; a separate script matches each proof's
assumptions to the saved SMT problem (965 = 965, 1,175 = 1,175, and 30 of
31 with one unused assertion). Hashes and commands are in
`tools/proof_replay/evidence/replay.json`. `tools/iw_enumeration/`
(standard library, exact rational branch-and-bound over sorted interval
orders) re-derives the four- and five-atom statements (161 and 30,499
nodes, every branch congruent) but does not terminate for six: nodes per
level 1, 25, 400, 4,624, 44,086 smallest-first and 1, 1, 4, 16, 100, 624,
4,096 largest-first, with almost no LP cuts, because of configurations with
many tied lengths. Recorded as a negative result; the tool and its tests
stay.

**Task 4, Lean 4 — done for the elementary core.** `formal/` compiles with
zero errors and zero `sorry` against Lean 4.31.0 / Mathlib
`5d1abc4cd8c71e2a463fb58d0e406decab077bdd`: L2, L3*, L4, L5, L7 soundness,
the exact dyad identity and D soundness, the Bloom factorization
`X X* = Y Y*`, and the finite-union-of-proper-subspaces step (two forms).
All stated in `ℤ[G]` for arbitrary abelian `G` and arbitrary ring elements.
Not formalized: the 135 bound as a graph computation, the census, Iw, the
quotient DAG. Commands and trust boundary in `formal/README.md`.

**Task 5, specification and archive — done except the owner's publish
steps.** `docs/LR_CHECKER_SPECIFICATION.md` states every obligation of the
two low-rank checkers and what remains prose. `scripts/make_release_archive.py`
builds a reproducible tarball with SHA-256; `docs/RELEASE.md` lists the
owner-only decisions (license, visibility, tag) and the DOI steps. No
license, DOI, visibility change or submission was made.

Verification commands run today: `scripts/update_manifests.py` (audit
pass), `tools/iw_enumeration/tests/test_iw_enumeration.py`,
`lake env lean --root=formal` on all three Lean files from a Mathlib checkout
at the pinned commit, `pdflatex` twice on the manuscript,
`tools/proof_replay/replay_cpc_proofs.py` (all three proofs REPLAYED), and
`scripts/verify.py` (19 commands pass).


## 1 October2026 — general constructive reduction and exact-grid tool

Plan carried forward from the parent research task and user selection of
exact pair counts on a periodic grid:

- Prove and separately attack an arbitrary-cardinality signed-matching reduction, keeping the remaining compact-grammar gap explicit.
- Deliver sparse exact binary reconstruction on products of cyclic groups with complete/partial status, limits, replay and trusted resumable checkpoints.
- Compare against immutable reference fibres and independent multidimensional/turnpike enumeration; attack interruption and provenance behavior.
- Package new work as dated authored docs/tools, preserving historical export bytes and the original dependency contract; run the default and optional general checks before a local checkpoint.
- Keep local performance, mathematical proof, historical novelty and external validation distinct; no publication, license, visibility or outreach action.

**[PROVED], in-house.** New GM/IG full proofs and separate adversarial
reviews are in `docs/general_matching/`. GM's torsion bound applies at
every rank and every cardinality, with a cyclic cylinder reduction and
matching-specific integer-lift criterion. IG gives exact exhaustive
binary-grid reconstruction, with exponential worst-case search. Neither
is described as a compact all-cardinality grammar or a historical novelty.
Classical rectification/universal-group antecedents and source access
limits are in the adjacent literature note and REFERENCES.

**[COMPUTED].** `tools/inverse_grid/` provides a standard-library JSON CLI
and Python API. Original tests compare1511 immutable-reference fibres and
506 independently enumerated grid fibres; a fresh review checks557 other
fibres, impossible targets, separate integer turnpike, loaded-source
identity and interruptions at every node and commit boundary. The two
review findings were repaired before packaging: interrupted active branches
are retained, and resident code keeps its loaded-source identity. Source
bytes match the parent tested implementation; copied tests explicitly
locate this package's inherited reference code.

`tools/general_matching/` supplies two exhaustive graph-bound methods,
their focused tests and corrected portable k7 certificates. The maximum
is432 over293930 eligible graphs, with35 labelled K3,4 maximizers. Prior
checkpoint hashes are checked before any resume mutation; the corrected
tables are byte-identical to the originals. This is a graph bound, not
a seven-point homometry census. Full claims/controls are in that tool guide.

The default wrapper now checks the inverse tool without adding a compiler
dependency. Optional `--suite general` adds signed-matching and C11 graph
tests. Newly authored paths are recorded in their tool provenance notices,
`docs/GENERAL_WORK_PROVENANCE.json` and the full PUBLIC_MANIFEST; the original
EXPORT_MANIFEST and all inherited certificate/reference bytes are preserved.
Exact verification receipt and local checkpoint follow below.

**Final local verification passed.** Command:

```sh
../.venv/bin/python scripts/verify.py --suite general --out .reproduction/general-verification-20261001
```

All19 commands passed in a disposable copy: the complete default suite,
the three new inverse programs, and both general reduction/graph programs.
The [receipt](docs/GENERAL_VERIFICATION.json) records every exit/timing,
tested source hashes, log digests and the pre-receipt package manifest hash.
The package audit passed with2485 files,94 Markdown documents and all2428
inherited hashes matching. Adding this receipt and final documentation
does not change tested source bytes; the final package manifest is refreshed
and its audit rerun before the local checkpoint. Archived graph tests
independently compared the complete portable k7 tables; fresh partial/resume
also reproduced432/35. Hosted CI and external mathematical validation are
unobserved by this task; older full structural/solver gates retain their
previously recorded scopes.

Parent research checkpoint: `a1ff8b4a910d89ec9c8c70de618905980f275cf2`.
This child checkpoint adds general math/tools and authored provenance
locally, preserving the historical export manifest and certificate bytes.

## 1 October 2026 — universal framing and supplied outside review plan

- State and prove the established universal autocorrelation equivalence on finite abelian groups, with zero-frequency and binary-admissibility conditions explicit.
- Connect that framework to G's six-point constructive claim; distinguish measurement information from crystal formation.
- Incorporate the supplied review as reported checks, not locally reproduced external results, and map the remaining free-parameter proof obligations.
- Verify Rosenblatt–Seymour attribution against an accessible primary source; retain any full-text access limit.
- Obtain a separate adversarial read and run the existing bounded checks; expected computation under two CPU minutes, with no new exhaustive census or solver replay.
- Record the exact changed files and validation boundaries before a local checkpoint; select no public visibility, license or outreach.

**Completed framing — [PROVED], in-house exposition of established
identities.** [The universal formulation](docs/UNIVERSAL_THEOREM.md)
contains the complete four-way autocorrelation/Fourier/spectral-unit/
pair-functional proof and binary constraint. A
[separate attack](docs/UNIVERSAL_REVIEW.md) found no correctness blocker.
This is classical harmonic analysis, not a newly discovered universal
crystal law or an all-cardinality constructive classification.
The references now credit Rosenblatt–Seymour1982 with original full-proof
access unresolved, and Rosenblatt1984's freshly read complete cyclic
factorization proof. Signed/rational factors may violate binary constraints.

**[COMPUTED] Four fresh structural checks passed without site packages.**
Using the existing independent checkers in a disposable copy, `python -S`
passed height growth, HR/BF, all315 DAG strata and the620 terminal mechanisms.
No DAG audit report was reused. The DAG covered10602nodes and658894integral
lattice inclusions in56.687seconds; total isolation/replay took65.232seconds.
The [receipt and input hashes](docs/STRUCTURAL_REPLAY.json) retain the exact
commands. No line-solver proof was regenerated; this local run does not
replace specialist scrutiny of encoding, coverage and written reductions.
The14-command bounded suite passed in46.783seconds before these explanatory
edits. Final document/provenance audit follows the public-manifest refresh;
its local receipt is `.reproduction/universal-final-audit.json`.

The supplied outside-review report remains **reported evidence** for its
bounded n12..44 census/grammar,135 bound and n6..120 Bloom checks; its raw
implementation/logs were not inspected. The alternate D-menu equivalence
remains unverified. The [assessment reply](docs/ASSESSMENT_REPLY.md) and
[reproduction guide](docs/REPRODUCING.md) now give the exact scope and
dependency-free fresh commands, including the resume-hash limitation.
All inherited proofs/code/certificates/reference assets remain byte-identical.
This is a local documentation checkpoint, with no new GitHub push,
visibility, license or outreach decision.

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

**Runtime follow-up:** the first hosted Ubuntu/Python3.12.14 bounded run
passed its first eleven commands, then timed out in the exact SymPy
weighted-six review at the 180-second limit. A separate reviewer confirmed
hash-order-dependent stalls under seed 0 and complete subsecond runs under
seeds 1, 2, 3, 4, 5, 10, 42 and 999. The wrapper now records seed 1 and
unbuffered subprocess output; its real-subprocess regression proves it
overrides a caller's seed 0. Mathematical sources and assertions are unchanged,
and timeouts still fail the gate. Full corrected local/hosted receipts are
kept separately from the initial run. This runtime repair is not proof
evidence for a new theorem.
