"""Two exhaustive exact spanning-tree bounds for graphs with 2k-2 edges.

The command builds the adjacent C11 source using an existing compiler, runs
both independent traversals serially, checks every labelled graph count, and
saves source hashes, progress, resumable checkpoints, and an exact histogram.
Only 4 <= k <= 7 is supported: this is a bounded computation, not an
all-cardinality extremal-graph theorem. No graph-isomorphism quotient is used.

The small pure-Python routines supply transparent, independent test controls.
They do not extend or replace the protected homometry reference implementation.
"""
from __future__ import annotations

import argparse
from array import array
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import comb
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
C_SOURCE = Path(__file__).with_suffix(".c")
CHECKPOINT_HEADER = struct.Struct("<8sIIQQ")
METHOD_IDS = {"bareiss": 1, "pruefer": 2}


def validate_k(k: int) -> int:
    if isinstance(k, bool) or not isinstance(k, int) or not 4 <= k <= 7:
        raise ValueError("k must be an integer in 4..7; larger searches require a new plan")
    return k


def edge_list(k: int) -> tuple[tuple[int, int], ...]:
    return tuple(combinations(range(validate_k(k)), 2))


def graph_mask(k: int, selected) -> int:
    """Validate a simple graph; its edges use zero-based vertex labels."""
    edges = edge_list(k)
    index = {edge: i for i, edge in enumerate(edges)}
    mask = 0
    for edge in selected:
        if not isinstance(edge, (tuple, list)) or len(edge) != 2:
            raise ValueError("each edge must contain two integer vertices")
        a, b = edge
        if (isinstance(a, bool) or isinstance(b, bool) or
                not isinstance(a, int) or not isinstance(b, int) or
                not 0 <= a < k or not 0 <= b < k or a == b):
            raise ValueError("edge vertices must be distinct integers in 0..k-1")
        bit = 1 << index[tuple(sorted((a, b)))]
        if mask & bit:
            raise ValueError("duplicate undirected edge")
        mask |= bit
    return mask


def edges_from_mask(k: int, mask: int) -> tuple[tuple[int, int], ...]:
    edges = edge_list(k)
    if isinstance(mask, bool) or not isinstance(mask, int) or not 0 <= mask < 1 << len(edges):
        raise ValueError("invalid complete-graph edge mask")
    return tuple(edge for i, edge in enumerate(edges) if mask & (1 << i))


def kirchhoff_count(k: int, selected) -> int:
    """Laplacian cofactor with Fraction Gaussian elimination (not Bareiss)."""
    selected = edges_from_mask(k, graph_mask(k, selected))
    laplacian = [[0] * k for _ in range(k)]
    for a, b in selected:
        laplacian[a][a] += 1
        laplacian[b][b] += 1
        laplacian[a][b] -= 1
        laplacian[b][a] -= 1
    matrix = [[Fraction(x) for x in row[:-1]] for row in laplacian[:-1]]
    determinant = Fraction(1)
    for column in range(k - 1):
        row = next((i for i in range(column, k - 1) if matrix[i][column]), None)
        if row is None:
            return 0
        if row != column:
            matrix[row], matrix[column] = matrix[column], matrix[row]
            determinant = -determinant
        pivot = matrix[column][column]
        determinant *= pivot
        for i in range(column + 1, k - 1):
            ratio = matrix[i][column] / pivot
            for j in range(column + 1, k - 1):
                matrix[i][j] -= ratio * matrix[column][j]
            matrix[i][column] = 0
    if determinant.denominator != 1 or determinant < 0:
        raise ArithmeticError("Laplacian determinant is not a nonnegative integer")
    return int(determinant)


def tree_subset_count(k: int, selected) -> int:
    """Count acyclic (k-1)-edge subsets directly using a disjoint-set forest."""
    selected = edges_from_mask(k, graph_mask(k, selected))
    result = 0
    for subset in combinations(selected, k - 1):
        parent = list(range(k))

        def root(vertex):
            while parent[vertex] != vertex:
                vertex = parent[vertex]
            return vertex

        for a, b in subset:
            a, b = root(a), root(b)
            if a == b:
                break
            parent[a] = b
        else:
            # An acyclic graph on k vertices with k-1 edges is connected.
            result += 1
    return result


def estimate(k: int) -> dict:
    k = validate_k(k)
    edge_count = k * (k - 1) // 2
    graph_edges = 2 * k - 2
    trees = k ** (k - 2)
    return {"vertices": k, "complete_graph_edges": edge_count,
            "graph_edges": graph_edges, "labelled_graphs": comb(edge_count, graph_edges),
            "pruefer_sequences": trees,
            "supersets_per_tree": comb(edge_count - k + 1, k - 1),
            "superset_additions": trees * comb(edge_count - k + 1, k - 1),
            "count_table_bytes_per_method": 4 * (1 << edge_count),
            "planned_wall_seconds_upper_estimate": 60 if k == 7 else 10}


def file_hash(path: Path) -> str:
    with path.open("rb") as handle:
        digest = sha256()
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, payload) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def load_checkpoint(path: Path, k: int, method: str) -> tuple[int, array]:
    """Read the fixed-width checkpoint, rejecting short/foreign payloads."""
    validate_k(k)
    if method not in METHOD_IDS:
        raise ValueError("unknown counting method")
    with path.open("rb") as handle:
        header = handle.read(CHECKPOINT_HEADER.size)
        if len(header) != CHECKPOINT_HEADER.size:
            raise ValueError("short checkpoint header")
        magic, saved_k, saved_method, processed, length = CHECKPOINT_HEADER.unpack(header)
        expected_length = 1 << (k * (k - 1) // 2)
        total = estimate(k)["labelled_graphs" if method == "bareiss" else "pruefer_sequences"]
        if (magic != b"GTBOUND1" or saved_k != k or saved_method != METHOD_IDS[method] or
                length != expected_length or processed > total):
            raise ValueError("invalid checkpoint header")
        payload = handle.read()
    if len(payload) != 4 * length:
        raise ValueError("invalid checkpoint payload length")
    counts = array("I")
    if counts.itemsize != 4:
        raise RuntimeError("checkpoint requires 32-bit unsigned int arrays")
    counts.frombytes(payload)
    if sys.byteorder != "little":
        counts.byteswap()
    if max(counts) > k ** (k - 2):
        raise ValueError("checkpoint count exceeds complete-graph tree count")
    return processed, counts


def graph_masks(k: int):
    """Independent Python combinations iterator; C uses increasing bitmasks."""
    edge_count = len(edge_list(k))
    for selected in combinations(range(edge_count), 2 * k - 2):
        yield sum(1 << i for i in selected)


def compare_complete_checkpoints(k: int, out: Path) -> dict:
    estimated = estimate(k)
    bareiss_processed, bareiss = load_checkpoint(out / "bareiss.bin", k, "bareiss")
    pruefer_processed, pruefer = load_checkpoint(out / "pruefer.bin", k, "pruefer")
    if (bareiss_processed != estimated["labelled_graphs"] or
            pruefer_processed != estimated["pruefer_sequences"]):
        raise ValueError("pointwise global comparison requires both complete traversals")
    # Compare ALL masks, including the zero entries outside the requested size.
    if bareiss != pruefer:
        for mask, (a, b) in enumerate(zip(bareiss, pruefer)):
            if a != b:
                raise ArithmeticError(f"independent methods disagree at graph {mask}: {a} != {b}")
    histogram = Counter()
    maximum, maximizing_mask = -1, None
    examined = 0
    eligible_count_sum = 0
    for mask in graph_masks(k):
        count = bareiss[mask]
        histogram[count] += 1
        examined += 1
        eligible_count_sum += count
        if count > maximum:
            maximum, maximizing_mask = count, mask
    if examined != estimated["labelled_graphs"]:
        raise ArithmeticError("Python labelled-graph enumeration count mismatch")
    if sum(bareiss) != eligible_count_sum:
        raise ArithmeticError("nonzero count outside requested edge cardinality")
    if eligible_count_sum != estimated["superset_additions"]:
        raise ArithmeticError("double-counted graph/tree incidence total mismatch")
    selected = edges_from_mask(k, maximizing_mask)
    if kirchhoff_count(k, selected) != maximum or tree_subset_count(k, selected) != maximum:
        raise ArithmeticError("transparent controls disagree on the maximizing graph")
    degrees = [sum(vertex in edge for edge in selected) for vertex in range(k)]
    return {"status": "COMPUTED", "vertices": k, "graph_edges": 2 * k - 2,
            "labelled_graphs": examined, "maximum": maximum,
            "maximizer_count": histogram[maximum],
            "histogram": dict(sorted(histogram.items())),
            "maximizing_graph_mask": maximizing_mask,
            "maximizing_graph": selected, "maximizing_graph_degree_sequence": sorted(degrees),
            "graph_tree_incidence_sum": eligible_count_sum,
            "all_masks_compared": len(bareiss), "pointwise_agreement": True,
            "complete_graph_trees": estimated["pruefer_sequences"],
            "scope": "Every labelled simple graph on k vertices with exactly 2k-2 edges; k<=7 only.",
            "methods": ["Laplacian cofactor/Bareiss for every graph",
                        "Every Prufer tree accumulated into every eligible edge superset"],
            "additional_controls": ["Python Fraction cofactor on maximizing graph",
                                    "Direct acyclic edge subsets on maximizing graph",
                                    "Total graph/tree incidences by double counting"]}


def build_enumerator(out: Path, compiler: str | None = None) -> tuple[Path, dict]:
    compiler_path = shutil.which(compiler or "clang")
    if compiler_path is None:
        raise RuntimeError("An existing C11 compiler is required; none was installed")
    binary = out / "general_tree_bound"
    command = [compiler_path, "-O3", "-std=c11", "-Wall", "-Wextra", "-Werror",
               str(C_SOURCE), "-o", str(binary)]
    result = subprocess.run(command, text=True, capture_output=True, check=True)
    version = subprocess.run([compiler_path, "--version"], text=True, capture_output=True, check=True)
    return binary, {"compile_command": command, "compile_stdout": result.stdout,
                    "compile_stderr": result.stderr, "compiler_version": version.stdout,
                    "c_source_sha256": file_hash(C_SOURCE),
                    "python_source_sha256": file_hash(Path(__file__)),
                    "binary_sha256": file_hash(binary)}


def run_bound(k: int, out: Path, *, resume: bool = False, limit: int | None = None,
              methods: tuple[str, ...] = ("bareiss", "pruefer"),
              compiler: str | None = None) -> dict:
    estimated = estimate(k)
    if limit is not None and (isinstance(limit, bool) or not isinstance(limit, int) or limit < 0):
        raise ValueError("item limit must be a nonnegative integer")
    if not methods or len(set(methods)) != len(methods) or any(m not in METHOD_IDS for m in methods):
        raise ValueError("methods must be distinct known counting methods")
    out = out.resolve()
    identity = {"vertices": k, "c_source_sha256": file_hash(C_SOURCE),
                "python_source_sha256": file_hash(Path(__file__))}
    manifest_path = out / "manifest.json"
    previous = None
    if manifest_path.exists():
        if not resume:
            raise ValueError("output already exists; use --resume to preserve its checkpoints")
        previous = json.loads(manifest_path.read_text())
        if previous["identity"] != identity:
            raise ValueError("resume source/cardinality mismatch; use a separate output directory")
        # Validate every existing checkpoint before writing the manifest, build,
        # log, or either count table. Header/length validity alone does not show
        # that an unchanged-looking count payload is the one previously saved.
        recorded_hashes = previous.get("checkpoint_sha256", {})
        if not isinstance(recorded_hashes, dict) or set(recorded_hashes) - set(METHOD_IDS):
            raise ValueError("invalid checkpoint hash manifest")
        for method in METHOD_IDS:
            checkpoint = out / f"{method}.bin"
            recorded_hash = recorded_hashes.get(method)
            if checkpoint.exists():
                if recorded_hash is None:
                    raise ValueError(f"resume checkpoint has no recorded hash: {method}")
                if file_hash(checkpoint) != recorded_hash:
                    raise ValueError(f"resume checkpoint hash mismatch: {method}")
                load_checkpoint(checkpoint, k, method)
            elif recorded_hash is not None:
                raise ValueError(f"resume checkpoint missing: {method}")
    elif out.exists() and any(out.iterdir()):
        raise ValueError("output directory has unowned files and no matching manifest")
    out.mkdir(parents=True, exist_ok=True)
    invocation = {"started_utc": datetime.now(timezone.utc).isoformat(), "resume": resume,
                  "limit": limit, "methods": methods}
    manifest = {"identity": identity, "estimate": estimated,
                "status": "COMPUTED-UNVALIDATED", "invocations": (previous or {}).get("invocations", []) + [invocation],
                "checkpoint_sha256": dict((previous or {}).get("checkpoint_sha256", {})),
                "checkpoint_format": "GTBOUND1 + little-endian u32 k/method + u64 processed/length + u32 counts"}
    write_json(manifest_path, manifest)
    binary, build = build_enumerator(out, compiler)
    write_json(out / "build.json", build)
    print(json.dumps({"estimate_before_run": estimated}, sort_keys=True), flush=True)
    started = time.monotonic()
    summaries = {}
    with (out / "progress.log").open("a") as log:
        log.write(json.dumps({"invocation": invocation, "estimate_before_run": estimated}, sort_keys=True) + "\n")
        log.flush()
        for method in methods:
            command = [str(binary), str(k), method, str(out / f"{method}.bin"),
                       str(out / f"{method}.json")]
            if limit is not None:
                command.append(str(limit))
            log.write(json.dumps({"command": command}, sort_keys=True) + "\n")
            log.flush()
            process = subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            assert process.stdout is not None
            for line in process.stdout:
                log.write(line); log.flush()
                print(line, end="", flush=True)
            if process.wait() != 0:
                raise RuntimeError(f"{method} enumerator failed; see {out / 'progress.log'}")
            summaries[method] = json.loads((out / f"{method}.json").read_text())
            manifest.setdefault("checkpoint_sha256", {})[method] = file_hash(out / f"{method}.bin")
            write_json(manifest_path, manifest)
    both_complete = all((out / f"{method}.json").exists() and
                        json.loads((out / f"{method}.json").read_text())["complete"]
                        for method in METHOD_IDS)
    result = compare_complete_checkpoints(k, out) if both_complete else {
        "status": "COMPUTED-UNVALIDATED", "complete": False,
        "vertices": k, "scope": "Partial checkpoint: no global maximum claim."}
    result["invocation_wall_seconds"] = time.monotonic() - started
    result["source_hashes"] = identity
    write_json(out / "comparison.json", result)
    manifest["status"] = result["status"]
    manifest["complete_two_method_comparison"] = both_complete
    manifest["last_invocation_wall_seconds"] = result["invocation_wall_seconds"]
    write_json(manifest_path, manifest)
    print(json.dumps({key: result[key] for key in ("status", "vertices", "maximum", "maximizer_count")
                      if key in result}, sort_keys=True), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--k", type=int, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--limit", type=int, help="items per method this invocation, for resumable benchmark controls")
    parser.add_argument("--method", choices=["both", "bareiss", "pruefer"], default="both")
    parser.add_argument("--compiler", help="existing compiler executable; default clang")
    args = parser.parse_args()
    try:
        run_bound(args.k, args.out, resume=args.resume, limit=args.limit,
                  methods=tuple(METHOD_IDS) if args.method == "both" else (args.method,), compiler=args.compiler)
    except (ValueError, RuntimeError, ArithmeticError, subprocess.CalledProcessError) as error:
        parser.exit(2, f"ERROR: {error}\n")


if __name__ == "__main__":
    main()
