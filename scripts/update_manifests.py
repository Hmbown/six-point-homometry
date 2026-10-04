#!/usr/bin/env python3
"""Regenerate the public integrity manifest and record scope edits of inherited files.

`docs/PUBLIC_MANIFEST.json` lists every public file with its SHA-256 and size;
`scripts/audit_repository.py` refuses a package whose files do not match it.
`docs/EXPORT_MANIFEST.json` binds every *inherited* file (copied from the
original research checkpoint) to its upstream and exported hashes.  Editing
an inherited file is allowed only as a recorded "scope-edit" that keeps the
upstream hash and describes the change.

Usage:
    python scripts/update_manifests.py                      # regenerate PUBLIC_MANIFEST only
    python scripts/update_manifests.py --scope-edit PATH "what changed" [--scope-edit ...]

This script changes manifests only; it never edits content files.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import audit_repository as audit  # noqa: E402


def regenerate_public_manifest(root: Path) -> int:
    files = []
    for relative in audit.public_paths(root):
        if relative == audit.PUBLIC_MANIFEST:
            continue
        digest, size, _ = audit.digest_file(root / relative, relative)
        files.append({"path": relative, "sha256": digest, "bytes": size})
    (root / audit.PUBLIC_MANIFEST).write_text(json.dumps({"schema_version": 1, "files": files}, indent=2) + "\n")
    return len(files)


def record_scope_edits(root: Path, edits: list[tuple[str, str]]) -> None:
    path = root / audit.EXPORT_MANIFEST
    manifest = json.loads(path.read_text())
    by_path = {entry["path"]: entry for entry in manifest["entries"]}
    for relative, description in edits:
        entry = by_path.get(relative)
        if entry is None:
            raise SystemExit(f"{relative} is not an inherited file; no export entry to update")
        digest, size, _ = audit.digest_file(root / relative, relative)
        if digest == entry["upstream_sha256"]:
            raise SystemExit(f"{relative} is byte-identical to its upstream; nothing to record")
        entry["exported_sha256"] = digest
        entry["exported_bytes"] = size
        entry["transform"] = "scope-edit"
        entry.setdefault("redaction_count", 0)
        entry.setdefault("scope_edits", [])
        if description not in entry["scope_edits"]:
            entry["scope_edits"].append(description)
    path.write_text(json.dumps(manifest, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--scope-edit", nargs=2, action="append", metavar=("PATH", "DESCRIPTION"), default=[])
    args = parser.parse_args()
    if args.scope_edit:
        record_scope_edits(args.root, [tuple(e) for e in args.scope_edit])
    count = regenerate_public_manifest(args.root)
    report = audit.audit_repository(args.root)
    print(json.dumps({"public_files": count, "audit_passed": report["passed"], "errors": report["errors"][:20]}, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
