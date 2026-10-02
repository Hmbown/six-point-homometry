"""Controls for the bounded, independently exhaustive graph/tree calculation.

Every k<=6 graph is checked by Python rational elimination and direct acyclic
edge subsets, in addition to both C traversals. Checkpoints are tested before
and after resume, and invalid inputs/corrupt payloads must be rejected.
The optional --k7-result check audits the persisted full seven-vertex pass.
"""
from __future__ import annotations

import argparse
from contextlib import redirect_stdout
from io import StringIO
from itertools import combinations
import json
from pathlib import Path
import random
import struct
import subprocess
import sys
from tempfile import TemporaryDirectory
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1] / "src"))
sys.path.insert(0, str(ROOT / "src"))
from general_tree_bound import (CHECKPOINT_HEADER, build_enumerator,
    compare_complete_checkpoints, edge_list, edges_from_mask, estimate,
    file_hash, graph_mask, graph_masks, kirchhoff_count, load_checkpoint,
    run_bound, tree_subset_count, validate_k)


def quiet_run(*args, **kwargs):
    with redirect_stdout(StringIO()):
        return run_bound(*args, **kwargs)


def raises(error_type, function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except error_type:
        return
    raise AssertionError(f"expected {error_type.__name__}")


def test_small_graph_exhaustion(base):
    checked = 0
    reports = []
    for k, expected_graphs, expected_max, expected_maximizers in (
            (4, 1, 16, 1), (5, 45, 45, 15), (6, 3003, 135, 60)):
        out = base / f"k{k}"
        result = quiet_run(k, out)
        assert result["labelled_graphs"] == expected_graphs
        assert result["maximum"] == expected_max
        assert result["maximizer_count"] == expected_maximizers
        assert result["pointwise_agreement"]
        _, counts = load_checkpoint(out / "bareiss.bin", k, "bareiss")
        for mask in graph_masks(k):
            graph = edges_from_mask(k, mask)
            assert kirchhoff_count(k, graph) == counts[mask]
            assert tree_subset_count(k, graph) == counts[mask]
            checked += 1
        reports.append({key: result[key] for key in
                        ("vertices", "labelled_graphs", "maximum", "maximizer_count")})
    # The existing six-point graph-bound implementation is a third traversal:
    # enumerate all five-edge subsets of K6 and retain the acyclic ones.
    from six_completeness import graph_minor_bound
    inherited = graph_minor_bound()
    computed = json.loads((base / "k6" / "comparison.json").read_text())
    assert inherited["maximum"] == computed["maximum"]
    assert {str(key): value for key, value in inherited["histogram"].items()} == computed["histogram"]
    return {"every_graph_python_controls": checked, "passes": reports,
            "inherited_k6_histogram_agrees": True}


def test_checkpoint_resume(base):
    out = base / "resume"
    partial = quiet_run(5, out, limit=3)
    assert not partial["complete"] and "maximum" not in partial
    for method in ("bareiss", "pruefer"):
        processed, _ = load_checkpoint(out / f"{method}.bin", 5, method)
        assert processed == 3
    raises(ValueError, compare_complete_checkpoints, 5, out)
    raises(ValueError, run_bound, 5, out)  # Never overwrite a prior run silently.
    final = quiet_run(5, out, resume=True)
    for method in ("bareiss", "pruefer"):
        assert json.loads((out / f"{method}.json").read_text())["resumed_from"] == 3
    assert final["histogram"] == json.loads((base / "k5" / "comparison.json").read_text())["histogram"] or {
        str(key): value for key, value in final["histogram"].items()
    } == json.loads((base / "k5" / "comparison.json").read_text())["histogram"]
    before = {m: file_hash(out / f"{m}.bin") for m in ("bareiss", "pruefer")}
    quiet_run(5, out, resume=True)
    after = {m: file_hash(out / f"{m}.bin") for m in ("bareiss", "pruefer")}
    assert before == after
    raises(ValueError, run_bound, 6, out, resume=True)
    orphan = base / "orphan"
    orphan.mkdir()
    (orphan / "keep.txt").write_text("unowned\n")
    raises(ValueError, run_bound, 4, orphan)
    assert (orphan / "keep.txt").read_text() == "unowned\n"
    return {"partial_items_per_method": 3, "resume_matches_fresh_run": True,
            "complete_resume_preserves_payload": True}


def test_input_controls(base):
    for k in (3, 8, -1, 0, 4.0, True, None):
        raises(ValueError, validate_k, k)
    for selected in (((0, 0),), ((0, 4),), ((-1, 1),), ((0.0, 1),),
                     ((False, 1),), ((0, 1), (1, 0)), ((0,),)):
        raises(ValueError, graph_mask, 4, selected)
    for mask in (-1, 1 << 6, True, 1.0):
        raises(ValueError, edges_from_mask, 4, mask)
    raises(ValueError, run_bound, 4, base / "negative", limit=-1)
    raises(ValueError, run_bound, 4, base / "bad-method", methods=("other",))
    raises(ValueError, run_bound, 4, base / "duplicate-method", methods=("bareiss", "bareiss"))
    binary = base / "k4" / "general_tree_bound"
    for arguments in (("8", "bareiss"), ("3", "pruefer"), ("4", "other"),
                      ("-1", "bareiss"), ("4x", "pruefer")):
        process = subprocess.run([str(binary), *arguments, str(base / "invalid.bin"),
                                  str(base / "invalid.json")], capture_output=True, text=True)
        assert process.returncode == 2 and "ERROR" in process.stderr
    assert not (base / "invalid.bin").exists()
    return {"malformed_graphs_cardinalities_methods_rejected": True}


def test_corrupt_checkpoint(base):
    valid = (base / "k4" / "bareiss.bin").read_bytes()
    target = base / "corrupt.bin"
    corruptions = (valid[:20], valid[:-1], valid + b"x", b"BADMAGIC" + valid[8:],
                   valid[:CHECKPOINT_HEADER.size] + struct.pack("<I", 17) + valid[CHECKPOINT_HEADER.size + 4:])
    binary = base / "k4" / "general_tree_bound"
    for payload in corruptions:
        target.write_bytes(payload)
        raises(ValueError, load_checkpoint, target, 4, "bareiss")
        process = subprocess.run([str(binary), "4", "bareiss", str(target),
                                  str(base / "corrupt.json")], capture_output=True, text=True)
        assert process.returncode == 2 and "ERROR" in process.stderr
    target.write_bytes(valid)
    raises(ValueError, load_checkpoint, target, 5, "bareiss")
    raises(ValueError, load_checkpoint, target, 4, "pruefer")
    return {"malformed_checkpoint_controls": len(corruptions) + 2}


def test_resume_payload_provenance(base):
    out = base / "provenance"
    quiet_run(5, out, limit=3)
    original_manifest = (out / "manifest.json").read_bytes()
    original_log = (out / "progress.log").read_bytes()
    original_build = (out / "build.json").read_bytes()
    bareiss = out / "bareiss.bin"
    original_checkpoint = bareiss.read_bytes()
    # Alter a count on an eligible graph, preserving magic/header/length and
    # keeping it within the Cayley bound. The structural loader accepts it.
    mask = next(graph_masks(5))
    modified = bytearray(original_checkpoint)
    offset = CHECKPOINT_HEADER.size + 4 * mask
    old_count = struct.unpack_from("<I", modified, offset)[0]
    struct.pack_into("<I", modified, offset, old_count + 1)
    bareiss.write_bytes(modified)
    assert load_checkpoint(bareiss, 5, "bareiss")[0] == 3
    try:
        # Even when only the other method is requested, validate both tables.
        quiet_run(5, out, resume=True, methods=("pruefer",))
    except ValueError as error:
        assert "checkpoint hash mismatch: bareiss" in str(error)
    else:
        raise AssertionError("valid-shaped checkpoint corruption was accepted")
    assert bareiss.read_bytes() == modified
    assert (out / "manifest.json").read_bytes() == original_manifest
    assert (out / "progress.log").read_bytes() == original_log
    assert (out / "build.json").read_bytes() == original_build
    # A missing table with a recorded digest must not silently start from zero.
    bareiss.unlink()
    raises(ValueError, quiet_run, 5, out, resume=True)
    assert (out / "manifest.json").read_bytes() == original_manifest
    bareiss.write_bytes(original_checkpoint)
    # Single-method resume retains the other method's already verified digest.
    quiet_run(5, out, resume=True, methods=("bareiss",))
    hashes = json.loads((out / "manifest.json").read_text())["checkpoint_sha256"]
    assert set(hashes) == {"bareiss", "pruefer"}
    assert all(hashes[method] == file_hash(out / f"{method}.bin") for method in hashes)
    quiet_run(5, out, resume=True, methods=("pruefer",))
    assert compare_complete_checkpoints(5, out)["maximum"] == 45
    return {"valid_shaped_count_corruption_rejected_before_any_output_mutation": True,
            "unrequested_method_checkpoint_also_verified": True,
            "missing_recorded_checkpoint_rejected": True,
            "single_method_resume_preserves_other_digest": True}


def test_seven_vertex_controls():
    k = 7
    star = tuple((0, v) for v in range(1, k))
    complete = edge_list(k)
    disconnected = tuple(combinations(range(6), 2))
    assert kirchhoff_count(k, ()) == tree_subset_count(k, ()) == 0
    assert kirchhoff_count(k, star) == tree_subset_count(k, star) == 1
    assert kirchhoff_count(k, complete) == tree_subset_count(k, complete) == 16807
    assert kirchhoff_count(k, disconnected) == tree_subset_count(k, disconnected) == 0
    rng = random.Random(20261001)
    checked = 0
    for _ in range(40):
        graph = tuple(rng.sample(complete, 12))
        count = kirchhoff_count(k, graph)
        assert tree_subset_count(k, graph) == count
        permutation = list(range(k))
        rng.shuffle(permutation)
        relabelled = tuple((permutation[a], permutation[b]) for a, b in graph)
        assert kirchhoff_count(k, relabelled) == tree_subset_count(k, relabelled) == count
        assert graph_mask(k, reversed(graph)) == graph_mask(k, graph)
        checked += 2
    expected = estimate(k)
    assert expected["labelled_graphs"] == 293930
    assert expected["pruefer_sequences"] == 16807
    assert expected["superset_additions"] == 84119035
    return {"seven_vertex_small_controls": checked + 4,
            "permutation_and_edge_order_controls": True}


def test_persisted_seven_vertex_result(out):
    actual = compare_complete_checkpoints(7, out)
    stored = json.loads((out / "comparison.json").read_text())
    for key in ("maximum", "maximizer_count", "labelled_graphs", "graph_tree_incidence_sum"):
        assert actual[key] == stored[key]
    assert {str(key): value for key, value in actual["histogram"].items()} == stored["histogram"]
    assert actual["labelled_graphs"] == 293930 and actual["pointwise_agreement"]
    assert actual["maximum"] == 432 and actual["maximizer_count"] == 35
    _, counts = load_checkpoint(out / "bareiss.bin", 7, "bareiss")
    actual_maximizers = {mask for mask in graph_masks(7) if counts[mask] == 432}
    bipartite_maximizers = set()
    for part in combinations(range(7), 3):
        part = set(part)
        selected = tuple(edge for edge in edge_list(7) if (edge[0] in part) != (edge[1] in part))
        bipartite_maximizers.add(graph_mask(7, selected))
    assert len(bipartite_maximizers) == 35
    assert actual_maximizers == bipartite_maximizers
    rng = random.Random(20261001)
    edges = edge_list(7)
    for _ in range(100):
        selected = tuple(rng.sample(edges, 12))
        mask = graph_mask(7, selected)
        assert counts[mask] == kirchhoff_count(7, selected) == tree_subset_count(7, selected)
    return {"persisted_global_pass": {key: actual[key] for key in
            ("vertices", "labelled_graphs", "maximum", "maximizer_count", "all_masks_compared")},
            "independent_python_sample_controls": 100,
            "all_maximizers_are_complete_bipartite_K3_4": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--k7-result", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    reports = {}
    with TemporaryDirectory(prefix="general-tree-bound-tests-") as temporary:
        base = Path(temporary)
        for test in (test_small_graph_exhaustion, test_checkpoint_resume,
                     test_input_controls, test_corrupt_checkpoint,
                     test_resume_payload_provenance):
            reports[test.__name__] = test(base)
            print("PASS", test.__name__, flush=True)
    reports["test_seven_vertex_controls"] = test_seven_vertex_controls()
    print("PASS test_seven_vertex_controls", flush=True)
    if args.k7_result:
        reports["test_persisted_seven_vertex_result"] = test_persisted_seven_vertex_result(args.k7_result)
        print("PASS test_persisted_seven_vertex_result", flush=True)
    payload = {"status": "COMPUTED", "tests": reports, "seconds": time.monotonic() - started}
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"passed": len(reports), "seconds": payload["seconds"]}), flush=True)


if __name__ == "__main__":
    main()
