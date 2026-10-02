# General signed-matching graph bound

These tools and in-house computation records were authored on **1 October
2026**, after the repository's historical export. They are recorded separately
in [PROVENANCE.json](PROVENANCE.json); they do not change the inherited
`docs/EXPORT_MANIFEST.json` or establish historical novelty.

**[COMPUTED].** For every labelled simple graph on seven vertices with exactly
twelve edges, the spanning-tree count is at most **432**. Exactly **35** labelled
graphs attain the maximum, all copies of K₃,₄. The two independent traversals
agree pointwise on every one of the **293,930** graphs. This finite calculation
supplies a bound used in the separately documented signed-matching reduction;
it is not an all-cardinality extremal formula or a complete structural
classification of homometry.

| vertices k | edges 2k−2 | labelled graphs | maximum trees | labelled maximizers |
|---:|---:|---:|---:|---:|
| 4 | 6 | 1 | 16 | 1 |
| 5 | 8 | 45 | 45 | 15 |
| 6 | 10 | 3,003 | 135 | 60 |
| 7 | 12 | 293,930 | 432 | 35 |

The new tests independently count every graph through k=6 and compare the
six-vertex histogram with the inherited `src/six_completeness.py` result.
The executable deliberately refuses k outside **4..7**.

## Algorithms and evidence

The first traversal enumerates all graphs of the prescribed edge size,
forms each reduced Laplacian, and takes its exact determinant by Bareiss
elimination with exact-divisibility checks. The second traversal builds
every labelled tree from its Prüfer sequence and increments every eligible
graph containing that tree. It uses no determinant or linear algebra.

At k=7 there are 16,807 trees and 5,005 eligible supersets per tree, giving
84,119,035 graph/tree incidences. The sum of the independently computed
determinants is the same. The driver compares every one of the 2,097,152
edge-mask slots, including zeros outside the requested cardinality. Tests
also use rational Gaussian elimination, direct acyclic edge subsets,
vertex permutations, singular examples, and the complete set of 35 K₃,₄
partitions.

Only the corrected seven-vertex run is retained in
[`evidence/k7-provenance-v2/`](evidence/k7-provenance-v2/). It includes portable
compressed checkpoints, exact histograms, progress/counter logs, source and
build manifests, and archive hashes. The original corrected-run test record
is [`evidence/tests-provenance-final.json`](evidence/tests-provenance-final.json).
Its seven test groups passed in 3.6649 seconds in the originating workspace.
The packaged build/log command paths are normalized to the repository's
source and ignored `.reproduction/general-matching-archive/` paths. Compiler
metadata, numerical counters, timings and recorded source/binary hashes still
describe the originating run; its original records remain unchanged. The
path adaptations and original/package digests are recorded in provenance.
No uncompressed checkpoint, executable or third-party source is packaged.

The checkpoint count payload independently hashes to
`17d65a87a5b9a926f5ebf6e2d61945f085818f8d2c1166fa7c93551b2c655985`
for each counting method. The source and test hashes, including the explicit
test import-path adaptation for this repository layout, are in
[PROVENANCE.json](PROVENANCE.json).

## Fresh run, resume and tests

Run these commands from the **math-only repository root**. Use its documented
pinned Python environment, including SymPy 1.14.0 for the independent Smith
checks. An existing **clang C11 compiler** is required; `--compiler` can select
another compatible installed compiler. The tools install no compiler or
dependency. Each count table uses 8,388,608 bytes at k=7, and the original
partial-plus-resumed computation finished well below the 60-second estimate.

```sh
.venv/bin/python tools/general_matching/src/general_tree_bound.py --k 7 --limit 1000 --out .reproduction/general-matching-fresh
.venv/bin/python tools/general_matching/src/general_tree_bound.py --k 7 --resume --out .reproduction/general-matching-fresh
.venv/bin/python tools/general_matching/tests/test_general_tree_bound.py --k7-result .reproduction/general-matching-fresh --out .reproduction/general-matching-fresh-tests.json
.venv/bin/python tools/general_matching/tests/test_general_matching_reduction_review.py
```

The mirrored core source files are byte-for-byte identical to the corrected
authored sources. Only the new mirrored tests add the inherited repository's
`src/` import path; no `PYTHONPATH` setting or parent-workspace path is needed.
The independent reduction tests verify small incidence minors, rank/torsion
and chosen-minor bounds, a positive-free-rank torsion counterexample, and full
Smith identities and lift directions. They are bounded controls for the
written argument, rather than a proof of untested cases.

## Audit the archived counts

Extract the compressed evidence into the ignored `.reproduction/` folder
with the following command, which verifies both compressed and raw hashes.
It preserves the archival evidence and refuses to replace different existing
count files.

```sh
.venv/bin/python - <<'PY'
from hashlib import sha256
from pathlib import Path
import gzip
import json
import shutil

source = Path("tools/general_matching/evidence/k7-provenance-v2")
target = Path(".reproduction/general-matching-archive")
target.mkdir(parents=True, exist_ok=True)
records = json.loads((source / "archive-provenance.json").read_text())
for method in ("bareiss", "pruefer"):
    name = method + ".bin"
    record = records[name]
    packed = (source / (name + ".gz")).read_bytes()
    assert sha256(packed).hexdigest() == record["gzip_sha256"]
    raw = gzip.decompress(packed)
    assert len(raw) == record["raw_bytes"]
    assert sha256(raw).hexdigest() == record["raw_sha256"]
    assert sha256(raw[32:]).hexdigest() == record["count_payload_sha256"]
    destination = target / name
    if destination.exists() and destination.read_bytes() != raw:
        raise ValueError("different existing count file: " + str(destination))
    destination.write_bytes(raw)
shutil.copyfile(source / "comparison.json", target / "comparison.json")
print("Both archived count tables verified and extracted.")
PY
.venv/bin/python tools/general_matching/tests/test_general_tree_bound.py --k7-result .reproduction/general-matching-archive --out .reproduction/general-matching-archive-tests.json
```

The checkpoint format uses fixed-width little-endian integers. Resume
validates every saved table against its prior manifest digest **before any
output changes**, including the other method in a single-method resume.
It rejects changed, missing or unrecorded checkpoints and changed source
identities. The corruption regression alters a valid count while retaining
the header, payload length and allowed range; resume must reject its hash.

These hashes protect consistency with an intact, trusted local manifest.
They are provenance records, not signed authenticity or independent
mathematical proof. The archival test compares all stored counts by the
two methods and applies further independent arithmetic controls.
