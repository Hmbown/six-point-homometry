# ENV-AUDIT (wave 3): are recorded results trustworthy under the numpy elision bug?

Workstream ENV-AUDIT (Claude), 29 Sep 2026; reconciled by Codex at takeover.
Files written by the original workstream: `notes/env_audit.md` (this),
`tests/test_env.py`, `src/env_audit_trace.py`, `src/env_audit_site/sitecustomize.py`,
`src/env_audit_rerun.sh`, `src/env_audit_diff.py`, everything under `results/rerun_venv/`.
The original reruns use an isolated shadow tree. An initial result manifest was
claimed in the unfinished draft but was not found at takeover; see §6.

**Status: incomplete audit, with many completed reproductions.** The saved diff
snapshot finds 195 regenerated file payloads equal after timing normalization.
Two further file differences are configuration metadata. A third exposed an
empty inherited P4 table; it has been restored from the previous commit, with
all 12 entries matched to pinned rerun logs. This is evidence for those comparisons,
not completion of every rerun. Queues q1, q3 and q4 still have active workers.
The full serial test run finished, and takeover checks cover all 20 current test
files (§5). A historical P5 verifier log has wrong rows and remains superseded.
**[COMPUTED]** applies only to the completed comparisons and tests below.

---

## 1. The bug, characterised precisely

Interpreter at `/opt/homebrew/bin/python3`: Python 3.14.7 + numpy 1.26.4 (unsupported combination).
Good interpreter: `./.venv/bin/python` = Python 3.12.12, numpy 2.5.3,
numba 0.67.0 (`requirements.lock`). Also unaffected: `/opt/homebrew/bin/python3.12` (numpy 2.4.2).

The original workstream's empirical characterization (not a complete interpreter
specification) identifies these necessary conditions in its probes; `.venv`
does not show the mutation. An expression can corrupt an array X when:

1. it is **operator syntax** `+ - * / // ** & | ^ << >>` or unary `-`/`~` (not `%`, not comparisons,
   not `@`, not ufunc calls like `np.add(a, b)` / `np.multiply`, not `operator.mul(a, b)`);
2. X is the **left** operand, or the right operand of a commutative op whose left operand is not
   itself elidable (e.g. `2 * X`, `2 + X`);
3. X **owns its data** (views such as `a[:, j]`, `z.real`, `x.reshape(...)` of a view are safe),
   is ≥ **256 KiB** (float64/int64 ≥ 32768 elements; int32 ≥ 65536; uint8/bool ≥ 262144;
   complex128 ≥ 16384), and is referenced only from **function-local variable slots** — this
   includes a caller's local passed as an argument (`def g(x): y = x*2` corrupts the caller's
   array!), but not arrays held in a list/dict/attribute/global, nor module-level code;
4. the other operand is a scalar/0-d array or has **exactly X's shape** (broadcasting ⇒ no elision);
5. the result dtype equals X's dtype (e.g. `int32_array * 2.5` is safe).

Effect: X is overwritten with the result, silently. Example: `b = a*2; c = b + a` gives `4a`.
Not every syntactic match fires: `np.minimum(1, t / 0.02)` in `src/sonify.py` (t = 705 KB local)
did *not* corrupt `t` under 3.14 (byte-identical WAVs, §4) — apparently 3.14 takes a strong
reference when the expression is a call argument. So the rule above is a safe over-approximation.

Provenance: the workstream reports `.venv` creation at **21:38** and bare
`python3` commands for legacy wave-1/2 results. Those legacy plain-NumPy outputs
are treated as potentially exposed until rerun. This does not describe the
later pinned-environment wave-3 outputs. At takeover the legacy C census driver
had completed n = 40; its computation is in C. A legacy 3.14 sampled-coverage
job (`src/census_check2_explain_sample.py 22 32 200 4 1`, PID 44058 at snapshot)
was still active. Its final output remains provisional until a completed pinned
rerun agrees; the initial shadow sample attempt failed on a missing input.

## 2. Method

* **Static:** AST scan of every `src/*.py`, `tests/*.py`, `notes/*.py` that imports numpy, for
  in-function operator expressions whose operand is a bare local name (numba-jitted functions
  excluded); every hit on a potentially large array was read by hand against the rule in §1.
* **Dynamic (new tool):** `src/env_audit_trace.py`, installed in every Python process of a run
  (incl. multiprocessing spawn workers) through `src/env_audit_site/sitecustomize.py` when
  `ENV_AUDIT_TRACE_DIR` is set. Using `sys.monitoring` under the good interpreter it records every
  *executed* operator site where the operand (found by bytecode stack simulation) is a
  `LOAD_FAST` local ndarray that owns its data and is ≥ 256 KiB. It over-approximates (does not
  model refcounts, broadcasting or dtype), and cannot see numba/C code, which is immune anyway.
  Self-tested on a synthetic script (left/right/unary/callee-argument cases found; small arrays,
  container-held arrays ignored).
* **Re-run + diff:** every result-producing command re-run under `.venv` with the tracer active,
  in a shadow copy of the repo (`results/rerun_venv/tree`, own `results/`; only the C-produced
  `results/fastcensus/families_n*.txt.gz` are symlinked, read-only). `src/env_audit_diff.py`
  compares every regenerated file with the original at the same path (npz: array equality; JSON:
  structural equality minus timing keys; CSV: cells minus timing columns; text: lines with timing
  tokens masked), and every stdout log with the original log.

  Reproduce: `bash src/env_audit_rerun.sh q1` (… `q2`–`q6`, `bg`), then
  `.venv/bin/python src/env_audit_diff.py`. Logs: `results/rerun_venv/logs/` (`_timeline.txt`,
  `_summary.tsv`), tracer reports: `results/rerun_venv/traces/<job>/trace_<pid>.json`,
  diff report: `results/rerun_venv/diff_report.txt`.

## 3. Inventory (task 1)

"Exposed" = a site matching §1 on an array that is ≥ 256 KiB at the sizes actually recorded.
Tracer column = hits in the re-runs of §4 (0 = no executed operator site on a large local array).

This is the bounded inventory recoverable from the completed logs and source
inspection. It is not a claim that all remaining dynamic paths have run.

| Path / group | Observed exposure and current evidence |
|---|---|
| `fastcensus.c`, `kappa_search` C kernel | Enumeration executes in C, outside Python operator elision. Census independently checked through n = 37; n = 38..40 still single-method. |
| `census_check2.py`, `fastmoves.py` enumeration kernels | Numba kernels; pinned reruns and family-partition comparison n = 8..32 completed. |
| `census_check2_compare.py:34` | Tracer sees `fa`, `fb` up to 152,445,312 bytes. Arithmetic builds the pair key; remapping each partition label injectively does not change the partition test, but the pinned rerun is the actual evidence: every n = 8..32 agrees. |
| `proofs_short_review_check.py:87,89` | Tracer sees `S`, `img` up to 21,035,488 bytes. Sign reversal leaves the tested T/I orbit unchanged; the anchor subtraction broadcasts and is outside the observed equal-shape rule. Pinned short-proof rerun completed with the same mathematical output. |
| `p3_coverage.py:552`, `p3_diagnose.py:63` | Tracer candidates on large complex matrices. The other operand broadcasts over rows, so these hits over-approximate the reported bug. Coverage reruns completed; diagnose n = 21 is still computing. |
| P2 certificates, literature checks, P4 phase/LD checks | Completed queue logs have exit 0; compared result payloads agree subject to §4 qualifications. |
| Legacy P5 verifier | Good-environment 8..24 finished; 25..30 still running. Independently written wave-3 subset-deck enumeration already agrees with the C kernel n = 8..31. |
| `sonify.py` | Both recorded WAVs independently hashed at takeover and are byte-identical to pinned reruns (§4). |

At 23:20 PDT, 78 trace report files existed. Traces are an over-approximation,
not a proof of output integrity by themselves.

## 4. Re-runs under `.venv` and diffs (task 2)

Snapshot: `results/2026-09-29-takeover-env-diff.json` and `.log`, generated at
**22:44:36 PDT**. It records file statuses SAME:195, DIFF:3, INPUT-COPY:39,
NO-ORIGINAL:4; log statuses SAME:14, DIFF:13, NOT-RUN:8. The later queue snapshot
is saved separately in `results/2026-09-29-takeover-audit/`.

| Completed group | Scope and comparison |
|---|---|
| Independent census + comparison | n = 8..32 summary and exact family partitions reproduce; all recorded comparisons true. Gosper rerun n = 33..34 completed, but has a different CSV range from the legacy run. |
| Fast move coverage | n = 8..32 regenerated coverage JSONs and unexplained-family files compare equal. |
| Old reference explanation | n = 12..20 completed and JSONL equal; 21..23 still running (n = 21 completed within the live job). |
| P2 / short proofs / literature | All q2 and q5 commands completed with exit 0. Type certificates through 120; attacks through 240; Rosenblatt count through 64; EJ check through 40. |
| P3 coverage | Both legacy tiers n = 8..22 completed. The diff tool reports log differences; regenerated comparable family lists agree. Diagnose 18 and 20 completed; later diagnoses/reviews pending. |
| P4 | Three phase-census ranges and torsion, LD, member, half-flip and full quick-review checks completed. The later `p4_analysis` rerun has not started. |
| P5 | Kernel rerun 8..30 equal; legacy verifier 8..24 exit 0. The independent subset-deck comparison 8..31 passes class-for-class (dated takeover log). |
| Audio | `z12_all_interval_tetrachords.wav` (793,828 bytes) and `z16_largest_family.wav` (2,081,500 bytes) match pinned outputs byte for byte. |

**The three file DIFF entries were inspected structurally.**

* `p2_move_coverage.json`: only `args.jobs`, and presence of default `census` /
  `mincover` fields differ.
* `p2_move_coverage_census_8_16.json`: only `args.jobs` and default `mincover` differ.
* `p4_review_ldpairs.json`: the main-checkout table was an empty object at
  takeover (mtime 21:50:41), and the shadow's latest partial run retained only
  n = 22,24. The earlier committed table has 12 entries. All 12 match the
  completed pinned rerun stdout logs, and the committed bytes were restored.
  The exact original caller that emptied the table was not identified. The
  script wrote on import and replaced the whole table on partial runs; it now
  has a guarded CLI, preserves unrequested entries, and supports `--out`.

The conservative diff tool does not normalize every output path or range.
Its DIFF / NOT-RUN labels must not be treated as final verdicts: e.g. diagnose
18 and 20 logs now exist, but its mapping expects different legacy names.
Partial running logs and nonmatching ranges also produce log DIFF entries.
The failed initial sampled rerun has a `FileNotFoundError` for a shadow family
input; it is queued again after the current census explanation, and has not
been accepted as a successful rerun.

## 5. Test suite under `.venv` (task 3) and the new guard (task 4)

The original serial runner completed **13 test files**, every exit code 0,
with `DONE` in `results/rerun_venv/tests/summary.tsv`. It ran from the main
checkout, not the shadow tree, before the seven remaining/current checks below.

| Original runner | Seconds |
|---|---:|
| `test_env`, `run_tests`, `test_c3_singer` | 0, 4, 4 |
| `test_census_check2`, `test_fastcensus`, `test_kappa_search` | 27, 221, 16 |
| `test_lit_rosenblatt_k4`, `test_moves_adversarial`, `test_moves` | 1, 589, 515 |
| `test_p3_moves_adversarial`, `test_p3_moves` | 707, 353 |
| `test_p4_largest`, `test_p4_review` | 4, 9 |

Takeover checks (all exit 0): `test_p3_quotient_lift`, `test_p5v`,
`test_c3_review`, `test_p3_menu_review`, `test_p5v_cli`, `test_p5v_compare`, and
`test_p4_review_io` (safe import, partial-run preservation, missing-input rejection).
Logs are `results/2026-09-29-takeover-test-*.log`. This is passing evidence
for **all 20 current files**, not a claim of a second monolithic full-suite run.
`tests/test_env.py` guards the pinned environment and demonstrates that ordinary
arithmetic leaves the source arrays intact. `.venv/bin/python tests/run_tests.py`
also passed all 10 reference tests at the start of this takeover.

## 6. Integrity of originals

No pre-audit SHA-256 manifest could be found. Consequently this audit does not
claim retrospective byte preservation for every original result file. The
protected `src/homometry.py`, `tests/run_tests.py`, and `data/baseline_table.md`
were independently compared with the preceding commit and are unchanged.
`results/2026-09-29-takeover-audit/snapshot.json` records their current hashes
and the snapshot boundary; it is a takeover manifest, not an initial one.
Original historical logs, including the faulty P5 log, are retained.
The large live shadow tree and partial traces are left out of the checkpoint;
completed test logs and a dated queue-log snapshot are retained.

## 7. Status of claims after the audit

* **[COMPUTED]** Completed rerun comparisons listed in §4, and all 20 current
  test files listed in §5, survive the pinned environment.
* **[COMPUTED]** The P5 least-n statements (D1 24 / D2 18) now have independent
  class-for-class verification through 31. They concern nontrivial Z-pairs,
  not the global literal-subset κ definition; see the separate definition audit.
* **[COMPUTED-UNVALIDATED]** Remaining reruns, larger P3 menu thresholds, n = 32..36
  exact higher-deck counts, and census n = 38..40 remain qualified as such.
* **Superseded:** `results/p5_kappa_verify_8_21.log` has wrong zero-family rows
  and false stored-match flags. Its cause is suspected environment corruption;
  that causal attribution is not proved. The independent pinned verifier and
  correlation kernel replace its mathematical claims.
* **Not an acceptance:** a queue's exit 0 alone, a copied input, or a partial
  log is insufficient to certify an unreconciled result.

**Next audit action:** let the existing workers finish, then regenerate the diff
and reconcile their exact mathematical rows before closing ENV-AUDIT. Do not
start a second copy of q1, q3 or q4 while those workers are alive.
