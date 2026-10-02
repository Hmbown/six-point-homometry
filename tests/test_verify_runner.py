"""Exercise real subprocesses to test preservation, failure and timeout gates."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('homometry_verify', ROOT/'scripts/verify.py')
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)


class VerifyRunnerTests(unittest.TestCase):
    def fixture(self, directory: str) -> Path:
        repo = Path(directory)/'repo'
        for name in ('scripts', 'tests', 'results', '.venv', '.git'):
            (repo/name).mkdir(parents=True)
        (repo/'results/archive.json').write_text('{"immutable": true}\n')
        (repo/'scripts/audit_repository.py').write_text('raise SystemExit(0)\n')
        return repo

    def run_gate(self, repo: Path, tests: tuple[str, ...], timeout: float = 10):
        output = repo.parent/'logs'
        argv = ['verify.py', '--out', str(output), '--timeout', str(timeout)]
        with patch.object(verify, 'ROOT', repo), patch.object(verify, 'QUICK', tests), \
             patch.object(verify.sys, 'argv', argv), contextlib.redirect_stdout(io.StringIO()), \
             contextlib.redirect_stderr(io.StringIO()):
            code = verify.main()
        return code, json.loads((output/'receipt.json').read_text())

    def test_scratch_mutation_preserves_archive_and_removes_parent_runtime(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.fixture(directory)
            original = (repo/'results/archive.json').read_bytes()
            (repo/'tests/check.py').write_text(
                'import os\nfrom pathlib import Path\n'
                'assert "PYTHONPATH" not in os.environ\n'
                'assert os.environ["PYTHONNOUSERSITE"] == "1"\n'
                'assert not Path(".venv").exists()\n'
                'assert not Path(".git").exists()\n'
                'Path("results/archive.json").write_text("changed in scratch")\n')
            with patch.dict(os.environ, {'PYTHONPATH': str(repo/'unwanted')}):
                code, receipt = self.run_gate(repo, ('tests/check.py',))
            self.assertEqual(code, 0)
            self.assertTrue(receipt['all_commands_passed'])
            self.assertEqual((repo/'results/archive.json').read_bytes(), original)

    def test_failure_stops_before_later_command(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.fixture(directory)
            (repo/'tests/fail.py').write_text('raise SystemExit(7)\n')
            (repo/'tests/later.py').write_text('raise RuntimeError("must not execute")\n')
            code, receipt = self.run_gate(repo, ('tests/fail.py', 'tests/later.py'))
            self.assertEqual(code, 7)
            self.assertFalse(receipt['all_commands_passed'])
            self.assertEqual(len(receipt['commands']), 2)
            self.assertFalse(receipt['commands'][-1]['timed_out'])

    def test_timeout_is_recorded_as_incomplete(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.fixture(directory)
            (repo/'tests/slow.py').write_text('import time\ntime.sleep(2)\n')
            code, receipt = self.run_gate(repo, ('tests/slow.py',), timeout=0.3)
            self.assertEqual(code, 124)
            self.assertFalse(receipt['all_commands_passed'])
            self.assertTrue(receipt['commands'][-1]['timed_out'])
            self.assertIn('TIMEOUT', (repo.parent/'logs'/receipt['commands'][-1]['log']).read_text())


if __name__ == '__main__':
    unittest.main()
