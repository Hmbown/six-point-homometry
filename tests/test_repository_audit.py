"""Adversarial fixtures for the standalone public-package audit."""
import hashlib
import gzip
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("repository_audit", ROOT / "scripts/audit_repository.py")
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


class RepositoryAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.put("README.md", "# Example\n\n[proof](notes/proof.md)\n")
        self.put("notes/proof.md", "# Proof\n\nA retained mathematical note.\n")
        self.make_manifests()

    def tearDown(self):
        self.temp.cleanup()

    def put(self, path, text):
        destination = self.root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text)

    def make_manifests(self, *, transform="unchanged", redaction_count=0, scope_edits=None):
        path = self.root / "notes/proof.md"
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        upstream_digest = "a" * 64 if transform != "unchanged" else digest
        self.put(audit.EXPORT_MANIFEST, json.dumps({"schema_version": 1, "source_checkpoint": "b" * 40, "entries": [{"path": "notes/proof.md", "upstream_sha256": upstream_digest, "exported_sha256": digest, "upstream_bytes": len(data), "exported_bytes": len(data), "transform": transform, "redaction_count": redaction_count, "scope_edits": scope_edits}]}))
        files = []
        for name in audit.public_paths(self.root):
            if name != audit.PUBLIC_MANIFEST:
                blob = (self.root / name).read_bytes()
                files.append({"path": name, "sha256": hashlib.sha256(blob).hexdigest(), "bytes": len(blob)})
        self.put(audit.PUBLIC_MANIFEST, json.dumps({"schema_version": 1, "files": files}))

    def run_audit(self, required=None):
        return audit.audit_repository(self.root, required_files=set() if required is None else required)

    def assert_finding(self, text):
        report = self.run_audit()
        self.assertFalse(report["passed"])
        self.assertTrue(any(text in e for e in report["errors"]), report)

    def test_complete_package_passes(self):
        self.assertTrue(self.run_audit()["passed"])

    def test_modified_historical_bytes_fail_both_manifests(self):
        self.put("notes/proof.md", "A changed theorem.\n")
        self.assert_finding("exported bytes differ")
        self.assert_finding("public integrity hash")

    def test_transformed_history_is_explicit(self):
        self.make_manifests(transform="local-path-redaction", redaction_count=2)
        report = self.run_audit()
        self.assertTrue(report["passed"], report)
        self.assertEqual(report["transformed_historical_files"], 1)
        self.make_manifests(transform="local-path-redaction", redaction_count=0)
        self.assert_finding("actual positive redactions")

    def test_required_dependency_missing_even_if_manifests_complete(self):
        report = self.run_audit({"notes/missing-review.md"})
        self.assertFalse(report["passed"])
        self.assertTrue(any("required proof" in e for e in report["errors"]))

    def test_scope_edits_require_descriptions(self):
        self.make_manifests(transform="scope-edit", scope_edits=["Removed an unrelated application appendix."])
        self.assertTrue(self.run_audit()["passed"])
        self.make_manifests(transform="scope-edit", scope_edits=[])
        self.assert_finding("actual descriptive edits")

    def test_missing_and_escaping_markdown_links(self):
        self.put("README.md", "[lost](missing.md)\n[escape](../outside.md)\n")
        self.make_manifests()
        self.assert_finding("unresolved local Markdown")
        self.assert_finding("escapes repository")

    def test_reference_and_percent_encoded_links(self):
        self.put("docs/a note.md", "# Note\n")
        self.put("README.md", "[a](docs/a%20note.md#note)\n[b][proof]\n[proof]: notes/proof.md\n")
        self.make_manifests()
        self.assertTrue(self.run_audit()["passed"])
        self.put("README.md", "[lost][undefined]\n")
        self.make_manifests()
        self.assert_finding("undefined Markdown reference")

    def test_local_heading_links_are_verified(self):
        self.put("README.md", "# First\n\n[here](#first)\n[there](notes/proof.md#proof)\n")
        self.make_manifests()
        self.assertTrue(self.run_audit()["passed"])
        self.put("README.md", "[lost](notes/proof.md#missing)\n")
        self.make_manifests()
        self.assert_finding("unresolved local Markdown heading")

    def test_media_private_paths_and_secrets_are_rejected(self):
        self.put("clip.mp4", "video")
        self.put(".env", "CREDENTIAL=value\n")
        self.put("README.md", "/" + "Users" + "/private-user/workspace/file\n")
        self.make_manifests()
        self.assert_finding("media or application asset")
        self.assert_finding("secret or machine-local")
        self.assert_finding("private absolute path")

    def test_credential_content_is_rejected_without_printing_value(self):
        secret = "ghp" + "_" + "a" * 36
        self.put("README.md", secret)
        self.make_manifests()
        report = self.run_audit()
        self.assertTrue(any("credential or private-key" in e for e in report["errors"]))
        self.assertNotIn(secret, json.dumps(report))

    def test_compressed_text_is_scanned(self):
        with gzip.open(self.root / "saved.json.gz", "wt") as handle:
            handle.write("/" + "Volumes" + "/private-disk/workspace")
        self.make_manifests()
        self.assert_finding("private absolute path in compressed text")

    def test_unexplained_archives_are_rejected(self):
        self.put("hidden.zip", "an unexplained container")
        self.make_manifests()
        self.assert_finding("undocumented public file type")

    def test_invalid_compressed_certificate_is_a_finding(self):
        self.put("bad.json.gz", "not compressed data")
        self.make_manifests()
        self.assert_finding("invalid compressed certificate")

    def test_binary_markdown_is_a_finding(self):
        (self.root / "README.md").write_bytes(b"\xff\xfe")
        self.make_manifests()
        self.assert_finding("not UTF-8 text")

    def test_parent_runtime_path_is_rejected(self):
        self.put("scripts/example.py", "from pathlib import Path\nROOT = Path(__file__).resolve().parents[2]\n")
        self.make_manifests()
        self.assert_finding("ancestor outside standalone")

    def test_unmanifested_asset_and_duplicate_entry_rejected(self):
        self.put("notes/unrecorded.md", "# Forgotten history\n")
        self.assert_finding("historical asset lacks export")
        self.assert_finding("missing from complete public")
        data = json.loads((self.root / audit.EXPORT_MANIFEST).read_text())
        data["entries"].append(data["entries"][0])
        self.put(audit.EXPORT_MANIFEST, json.dumps(data))
        self.assert_finding("unsafe or duplicate entry")

    def test_symlink_cannot_escape_repository(self):
        (self.root / "linked.md").symlink_to(self.root / "README.md")
        self.assert_finding("symlink")

    def test_fenced_examples_do_not_create_spurious_links(self):
        self.put("README.md", "```text\n[example](not-a-real-file.md)\n```\n[actual](notes/proof.md)\n")
        self.make_manifests()
        self.assertTrue(self.run_audit()["passed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
