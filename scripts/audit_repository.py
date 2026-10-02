#!/usr/bin/env python3
"""Audit public package integrity without an upstream checkout or dependencies.

The export manifest describes inherited files.  The public manifest covers
every candidate public file except itself.  Hash verification is integrity
evidence, not a proof replay or a determination of historical priority.
"""
from __future__ import annotations

import argparse
import ast
import gzip
import hashlib
import json
import re
import subprocess
import sys
import zlib
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

EXPORT_MANIFEST = "docs/EXPORT_MANIFEST.json"
PUBLIC_MANIFEST = "docs/PUBLIC_MANIFEST.json"
IGNORED_PARTS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".reproduction", "reproduced"}
MEDIA_SUFFIXES = {".wav", ".mp3", ".m4a", ".flac", ".ogg", ".aif", ".aiff", ".mid", ".midi", ".mp4", ".mov", ".avi", ".webm", ".mkv", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".pptx"}
SECRET_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".kdbx"}
FORBIDDEN_COMPONENT = re.compile(r"(?:^|[-_])(audio|video|piano|sonify|sonification|explainer|hydride|superconductivity|superconducting|mgir|vacancy|pairing|materials)(?:[-_.]|$)", re.I)
PRIVATE_PATH = re.compile(rb"/(?:Users|Volumes|home)/[A-Za-z0-9_.-]+(?:[/\\][^\s\"'<>]*)?")
SECRET_CONTENT = re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|AKIA[A-Z0-9]{16}|sk-(?:proj-)?[A-Za-z0-9_-]{30,})\b")
HASH = re.compile(r"[0-9a-f]{64}\Z")
TEXT_SUFFIXES = {".md", ".txt", ".py", ".c", ".cpp", ".h", ".hpp", ".json", ".toml", ".yml", ".yaml", ".tex", ".smt2", ".log", ".diff", ".csv", ".sh"}
PUBLIC_SUFFIXES = TEXT_SUFFIXES | {".gz", ".rst", ".ini", ".cfg", ".pdf"}
PUBLIC_BASENAMES = {".gitignore", ".gitattributes", ".gitkeep", "LICENSE", "CITATION", "Makefile"}

# A file's presence is a separate obligation from its integrity.  These are
# the headline results and the principal dependencies stated in their proofs.
REQUIRED_FILES = {
    "README.md", "AGENTS.md", "PROGRESS.md", "requirements.txt",
    "docs/RESULTS.md", "docs/REFERENCES.md", "docs/REPRODUCING.md",
    "docs/PACKAGE_REVIEW.md",
    "src/homometry.py", "tests/run_tests.py", "src/six_generate.py",
    "notes/2026-09-30-six-generation.md", "notes/2026-09-30-six-generation-review.md",
    "notes/2026-09-30-six-integer-theorem.md", "notes/2026-09-30-six-integer-review.md",
    "notes/2026-09-30-six-shadow-theorem.md", "notes/2026-09-30-six-shadow-review.md",
    "notes/2026-09-30-six-completeness.md", "notes/2026-09-30-six-templates.md",
    "notes/2026-09-30-six-cylinder-templates-review.md",
    "notes/2026-09-30-six-bloom-cylinders.md", "notes/2026-09-30-six-free-rank.md",
    "notes/2026-09-30-six-cylinder-branches-review.md", "notes/2026-09-30-six-free-dag.md",
    "notes/2026-09-30-six-low-rank-review.md", "notes/2026-09-30-six-finite-torsion.md",
    "notes/2026-09-30-six-finite-torsion-review.md",
    "notes/2026-10-01-six-bloom-primary.md", "notes/2026-10-01-six-bloom-support.md",
    "notes/2026-10-01-six-primary-review.md",
    "notes/2026-10-01-weighted-six-incidence.md", "notes/2026-10-01-weighted-six-review.md",
    "notes/2026-10-01-weighted-subgroup.md", "notes/2026-10-01-weighted-subgroup-review.md",
    "results/2026-09-30-six-integer-proof/count.smt2",
    "results/2026-09-30-six-integer-proof/count.proof.gz",
    "results/2026-09-30-six-integer-weighted-two/weighted.smt2",
    "results/2026-09-30-six-integer-weighted-two/weighted.proof.gz",
    "results/2026-09-30-six-completeness.json",
    "results/2026-09-30-six-templates/inventory.json",
    "results/2026-09-30-six-templates/smith.json",
    "results/2026-09-30-six-templates/verification.json",
    "results/2026-09-30-six-bloom-cylinders.json",
    "results/2026-09-30-six-cylinder-branches-review.json",
    "results/2026-09-30-six-free-rank/verification.json",
    "results/2026-09-30-six-free-dag-review/summary.json",
    "results/2026-09-30-six-low-rank-review/verification.json",
    "results/2026-09-30-six-low-rank-review/mechanism-certificates.json",
    "results/2026-09-30-six-finite-torsion-review.json",
    "results/2026-09-30-six-pair-mechanisms-review-135.json",
    "results/2026-10-01-six-bloom-primary/pair-certificate.json",
    "results/2026-10-01-six-bloom-support/certificate.json",
    "results/2026-10-01-six-primary-review/independent-audit.json",
    "results/2026-10-01-weighted-six-incidence/certificates.json",
    "results/2026-10-01-weighted-six-review/independent-audit.json",
    "results/2026-10-01-weighted-subgroup/certificate.json",
    "results/2026-10-01-weighted-subgroup-review/independent-audit.json",
}
REQUIRED_FILES.update(f"results/2026-09-30-six-pair-mechanisms/n{n}.json" for n in range(12, 136))
REQUIRED_FILES.update(f"results/2026-09-30-six-large-census/n{n}.json" for n in range(12, 136))


def public_paths(root: Path) -> list[str]:
    """Include tracked and nonignored untracked files, also before git init."""
    try:
        top = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
        if Path(top).resolve() == root.resolve():
            result = subprocess.run(["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard", "-z"], capture_output=True, check=True)
            return sorted(set(p.decode("utf-8") for p in result.stdout.split(b"\0") if p))
    except (OSError, subprocess.CalledProcessError, UnicodeError):
        pass
    return sorted(str(p.relative_to(root).as_posix()) for p in root.rglob("*") if (p.is_file() or p.is_symlink()) and not any(part in IGNORED_PARTS for part in p.relative_to(root).parts))


def safe_relative(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    p = PurePosixPath(value)
    return not p.is_absolute() and ".." not in p.parts and p.as_posix() == value


def digest_file(path: Path) -> tuple[str, int, set[str]]:
    digest = hashlib.sha256()
    size = 0
    hygiene = set()
    tail = b""
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
            size += len(chunk)
            window = tail + chunk
            if PRIVATE_PATH.search(window):
                hygiene.add("private absolute path")
            if SECRET_CONTENT.search(window):
                hygiene.add("credential or private-key content")
            tail = window[-8192:]
    # Certificates can be large gzip-compressed text.  Scan the actual public
    # content as well as the container, rather than trusting a filename.
    if path.suffix.lower() == ".gz":
        if len(path.suffixes) < 2 or path.suffixes[-2].lower() not in {".json", ".proof", ".smt2", ".txt"}:
            hygiene.add("undocumented compressed archive")
        else:
            try:
                tail = b""
                with gzip.open(path, "rb") as handle:
                    while chunk := handle.read(1024 * 1024):
                        window = tail + chunk
                        if PRIVATE_PATH.search(window):
                            hygiene.add("private absolute path in compressed text")
                        if SECRET_CONTENT.search(window):
                            hygiene.add("credential or private-key content in compressed text")
                        tail = window[-8192:]
            except (OSError, EOFError, zlib.error):
                hygiene.add("invalid compressed certificate")
    return digest.hexdigest(), size, hygiene


def markdown_targets(content: str) -> list[str]:
    """Extract inline and reference links without treating fenced code as links."""
    content = re.sub(r"^\s*(```|~~~).*?^\s*\1\s*$", "", content, flags=re.M | re.S)
    refs = {m.group(1).strip().casefold(): m.group(2) or m.group(3) for m in re.finditer(r"^ {0,3}\[([^\]]+)\]:\s*(?:<([^>]+)>|(\S+))", content, re.M)}
    targets = list(refs.values())
    targets.extend((m.group(1) or m.group(2)) for m in re.finditer(r"!?\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+[\"'][^\n]*?[\"'])?\s*\)", content))
    for match in re.finditer(r"!?\[([^\]]+)\]\[([^\]]*)\]", content):
        key = (match.group(2) or match.group(1)).strip().casefold()
        targets.append(refs.get(key, "UNRESOLVED_REFERENCE:" + key))
    # Shortcut references are links only when a definition exists.
    for match in re.finditer(r"(?<!!)\[([^\]]+)\](?![\[(])", content):
        key = match.group(1).strip().casefold()
        if key in refs:
            targets.append(refs[key])
    targets.extend(m.group(1) for m in re.finditer(r"(?:href|src)=[\"']([^\"']+)[\"']", content))
    return targets


def markdown_anchors(content: str) -> set[str]:
    content = re.sub(r"^\s*(```|~~~).*?^\s*\1\s*$", "", content, flags=re.M | re.S)
    anchors = set(re.findall(r"\bid=[\"']([^\"']+)[\"']", content))
    counts = {}
    headings = re.findall(r"^ {0,3}#{1,6}\s+(.+?)(?:\s+#+)?\s*$", content, re.M)
    headings.extend(re.findall(r"^([^\n]+)\n {0,3}(?:=+|-+)\s*$", content, re.M))
    for heading in headings:
        heading = re.sub(r"<[^>]+>", "", heading)
        heading = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", heading)
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        number = counts.get(slug, 0)
        counts[slug] = number + 1
        anchors.add(slug if not number else f"{slug}-{number}")
    return anchors


def markdown_errors(root: Path, relative: str, content: str) -> list[str]:
    errors = []
    for target in markdown_targets(content):
        if target.startswith("UNRESOLVED_REFERENCE:"):
            errors.append(f"{relative}: undefined Markdown reference {target.split(':', 1)[1]}")
            continue
        split = urlsplit(target)
        if split.scheme or split.netloc:
            if split.scheme in {"file", "project-file", "library-file"}:
                errors.append(f"{relative}: nonportable local link")
            continue
        path = unquote(split.path)
        if path.startswith("/"):
            errors.append(f"{relative}: absolute local Markdown link")
            continue
        resolved = (root / relative).parent.joinpath(path).resolve() if path else root / relative
        if not resolved.is_relative_to(root.resolve()):
            errors.append(f"{relative}: Markdown link escapes repository")
        elif not resolved.exists():
            errors.append(f"{relative}: unresolved local Markdown link: {path}")
        elif split.fragment and resolved.suffix.lower() == ".md":
            try:
                target_content = content if resolved == root / relative else resolved.read_text(encoding="utf-8")
                if unquote(split.fragment) not in markdown_anchors(target_content):
                    errors.append(f"{relative}: unresolved local Markdown heading: {path}#{split.fragment}")
            except (OSError, UnicodeError):
                errors.append(f"{relative}: unreadable Markdown link target: {path}")
    return errors


def python_runtime_errors(relative: str, content: str) -> list[str]:
    errors = []
    try:
        tree = ast.parse(content, filename=relative)
    except SyntaxError:
        return [f"{relative}: invalid Python source"]
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            modules = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            if any(name.split(".")[0] == "babbitt2" for name in modules):
                errors.append(f"{relative}: parent project import")
            if isinstance(node, ast.ImportFrom) and node.level >= 2:
                errors.append(f"{relative}: import beyond standalone package")
        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Attribute) and node.value.attr == "parents" and isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, int) and node.slice.value >= 2:
            errors.append(f"{relative}:{node.lineno}: ancestor outside standalone repository")
        if isinstance(node, ast.Attribute) and node.attr == "parent" and isinstance(node.value, ast.Name) and node.value.id.upper() in {"ROOT", "PROJECT_ROOT", "REPO_ROOT"}:
            errors.append(f"{relative}:{node.lineno}: runtime parent-checkout path")
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div) and isinstance(node.left, ast.Name) and node.left.id.upper() in {"ROOT", "PROJECT_ROOT", "REPO_ROOT"} and isinstance(node.right, ast.Constant) and node.right.value == "..":
            errors.append(f"{relative}:{node.lineno}: runtime parent-checkout path")
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and re.match(r"(?:\.\./)+(?:src|data|results|notes)(?:/|$)", node.value):
            errors.append(f"{relative}:{node.lineno}: runtime relative parent path")
    return errors


def load_manifest(root: Path, name: str, errors: list[str]) -> dict:
    try:
        value = json.loads((root / name).read_text())
        if not isinstance(value, dict) or value.get("schema_version") != 1:
            raise ValueError("unsupported schema")
        return value
    except (OSError, UnicodeError, ValueError):
        errors.append(f"{name}: missing or invalid schema_version=1 manifest")
        return {}


def audit_repository(root: Path, *, required_files: set[str] | None = None) -> dict:
    root = root.resolve()
    errors: list[str] = []
    paths = public_paths(root)
    candidates = set(paths)
    digests = {}
    for relative in paths:
        path = root / relative
        if not safe_relative(relative) or path.is_symlink() or not path.is_file():
            errors.append(f"{relative}: unsafe public path, symlink or missing file")
            continue
        suffix = path.suffix.lower()
        if suffix not in PUBLIC_SUFFIXES and path.name not in PUBLIC_BASENAMES:
            errors.append(f"{relative}: undocumented public file type")
        if suffix in MEDIA_SUFFIXES or any(FORBIDDEN_COMPONENT.search(part) for part in path.relative_to(root).parts):
            errors.append(f"{relative}: media or application asset outside mathematics package")
        if suffix in SECRET_SUFFIXES or path.name.lower() in {".ds_store", "id_rsa", "id_ed25519", "credentials.json", "secrets.json", "token.json"} or path.name.startswith(".env"):
            errors.append(f"{relative}: secret or machine-local artifact")
        digest, size, hygiene = digest_file(path)
        digests[relative] = (digest, size)
        errors.extend(f"{relative}: {finding}" for finding in sorted(hygiene))
        if suffix == ".md" or (suffix == ".py" and relative.startswith(("src/", "scripts/", "tests/"))):
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeError:
                errors.append(f"{relative}: public Markdown or Python is not UTF-8 text")
                continue
            if suffix == ".md":
                errors.extend(markdown_errors(root, relative, content))
            else:
                errors.extend(python_runtime_errors(relative, content))
    for relative in sorted(REQUIRED_FILES if required_files is None else required_files):
        if relative not in candidates:
            errors.append(f"{relative}: required proof, review, certificate or setup asset is absent")

    exported = load_manifest(root, EXPORT_MANIFEST, errors)
    entries = exported.get("entries", [])
    if not isinstance(entries, list) or not entries:
        errors.append(f"{EXPORT_MANIFEST}: entries must be a nonempty list")
        entries = []
    checkpoint = exported.get("source_checkpoint", "")
    if not isinstance(checkpoint, str) or not re.fullmatch(r"[0-9a-f]{40}", checkpoint):
        errors.append(f"{EXPORT_MANIFEST}: source_checkpoint must be a full Git commit hash")
    inherited_paths = set()
    transformed = 0
    scope_edited = 0
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append(f"{EXPORT_MANIFEST}: invalid entry")
            continue
        relative = entry.get("path")
        if not safe_relative(relative) or relative in inherited_paths:
            errors.append(f"{EXPORT_MANIFEST}: unsafe or duplicate entry path")
            continue
        inherited_paths.add(relative)
        expected = (entry.get("exported_sha256"), entry.get("exported_bytes"))
        if relative not in digests or digests[relative] != expected:
            errors.append(f"{relative}: exported bytes differ from provenance manifest")
        upstream = (entry.get("upstream_sha256"), entry.get("upstream_bytes"))
        if not isinstance(upstream[0], str) or not HASH.fullmatch(upstream[0]) or type(upstream[1]) is not int or upstream[1] < 0:
            errors.append(f"{relative}: invalid upstream provenance hash or size")
        transform, count = entry.get("transform"), entry.get("redaction_count")
        if transform == "unchanged":
            if upstream != expected or type(count) is not int or count != 0:
                errors.append(f"{relative}: unchanged copy has divergent source/export provenance")
        elif transform == "local-path-redaction":
            transformed += 1
            if upstream[0] == expected[0] or type(count) is not int or count <= 0:
                errors.append(f"{relative}: transformed history must identify actual positive redactions")
        elif transform == "scope-edit":
            transformed += 1
            scope_edited += 1
            edits = entry.get("scope_edits")
            if upstream[0] == expected[0] or type(count) is not int or count < 0 or not isinstance(edits, list) or not edits or not all(isinstance(e, str) and e.strip() for e in edits):
                errors.append(f"{relative}: scope-edited history must identify actual descriptive edits")
        else:
            errors.append(f"{relative}: undocumented inherited-file transformation")
    # Historical code, proofs, certificates and baseline data must not silently
    # become newly authored files outside the upstream provenance inventory.
    for relative in sorted(candidates):
        if relative.startswith(("src/", "notes/", "results/", "data/")) or (relative.startswith("tests/") and relative not in {"tests/test_repository_audit.py", "tests/test_verify_runner.py"}):
            if relative not in inherited_paths:
                errors.append(f"{relative}: historical asset lacks export provenance")

    public = load_manifest(root, PUBLIC_MANIFEST, errors)
    files = public.get("files", [])
    if not isinstance(files, list) or not files:
        errors.append(f"{PUBLIC_MANIFEST}: files must be a nonempty list")
        files = []
    manifested = set()
    for entry in files:
        if not isinstance(entry, dict) or not safe_relative(entry.get("path")) or entry.get("path") in manifested:
            errors.append(f"{PUBLIC_MANIFEST}: invalid or duplicate file entry")
            continue
        relative = entry["path"]
        manifested.add(relative)
        if digests.get(relative) != (entry.get("sha256"), entry.get("bytes")):
            errors.append(f"{relative}: public integrity hash or size mismatch")
    expected_public = candidates - {PUBLIC_MANIFEST}
    errors.extend(f"{p}: missing from complete public manifest" for p in sorted(expected_public - manifested))
    errors.extend(f"{p}: stale or self-referential public manifest entry" for p in sorted(manifested - expected_public))
    return {"passed": not errors, "public_files": len(paths), "inherited_files": len(inherited_paths), "transformed_historical_files": transformed, "scope_edited_historical_files": scope_edited, "markdown_files": sum(p.endswith(".md") for p in paths), "errors": sorted(set(errors)), "limitations": ["Hashes authenticate packaged bytes against the recorded manifests; upstream commit origin needs the original Git objects or an independent source record.", "Artifact presence and packaging integrity do not replay mathematical certificates, prove theorem correctness, establish historical priority, or provide external peer review."]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    report = audit_repository(args.root)
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
