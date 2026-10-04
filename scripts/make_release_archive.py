#!/usr/bin/env python3
"""Build a reproducible tarball of the public files and print its SHA-256.

Uses the same public-file inventory as scripts/audit_repository.py, so the
archive contains exactly the files the public manifest covers (plus the
manifest itself). Timestamps and ownership are normalized so that two builds
of the same tree give the same bytes.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import audit_repository as audit  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path, default=ROOT / ".reproduction" / "release")
    parser.add_argument("--name", default="six-point-homometry-2026.10.04")
    args = parser.parse_args()
    root = args.root.resolve()
    report = audit.audit_repository(root)
    if not report["passed"]:
        print(json.dumps(report["errors"][:20], indent=2))
        return 1
    args.out.mkdir(parents=True, exist_ok=True)
    target = args.out / f"{args.name}.tar.gz"
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w") as tar:
        for relative in audit.public_paths(root):
            path = root / relative
            info = tar.gettarinfo(str(path), arcname=f"{args.name}/{relative}")
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.mtime = 0
            with path.open("rb") as handle:
                tar.addfile(info, handle)
    import gzip
    with open(target, "wb") as handle:
        with gzip.GzipFile(fileobj=handle, mode="wb", mtime=0) as gz:
            gz.write(buffer.getvalue())
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    (args.out / f"{args.name}.sha256").write_text(f"{digest}  {target.name}\n")
    try:
        commit = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        commit = "unknown"
    print(json.dumps({"archive": str(target), "sha256": digest, "files": report["public_files"], "commit": commit}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
