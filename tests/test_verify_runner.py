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

    def run_gate(self, repo: Path, tests: tuple[str, ...], timeout: float = 10,
                 suite: str = 'quick'):
        output = repo.parent/'logs'
        argv = ['verify.py', '--out', str(output), '--timeout', str(timeout), '--suite', suite]
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
                'assert os.environ["PYTHONHASHSEED"] == "1"\n'
                'assert os.environ["PYTHONUNBUFFERED"] == "1"\n'
                'assert not Path(".venv").exists()\n'
                'assert not Path(".git").exists()\n'
                'Path("results/archive.json").write_text("changed in scratch")\n')
            with patch.dict(os.environ, {'PYTHONPATH': str(repo/'unwanted'),
                                         'PYTHONHASHSEED': '0', 'PYTHONUNBUFFERED': '0'}):
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

    def test_new_tool_runs_from_copied_tree_with_child_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.fixture(directory)
            (repo/'src').mkdir()
            (repo/'src/reference.py').write_text('VALUE = 7\n')
            tool = repo/'tools/inverse_grid'
            (tool/'src').mkdir(parents=True)
            (tool/'tests').mkdir()
            (tool/'src/local_tool.py').write_text('VALUE = 11\n')
            (tool/'tests/check.py').write_text(
                'from pathlib import Path\nimport sys\n'
                'ROOT = Path(__file__).resolve().parents[1]\n'
                'sys.path.insert(0, str(ROOT/"src"))\n'
                'from local_tool import VALUE as tool_value\n'
                'sys.path.insert(0, str(ROOT.parents[1]/"src"))\n'
                'from reference import VALUE as reference_value\n'
                'assert (tool_value, reference_value) == (11, 7)\n'
                'Path("tools/inverse_grid/src/local_tool.py").write_text("scratch only")\n')
            code, receipt = self.run_gate(repo, ('tools/inverse_grid/tests/check.py',))
            self.assertEqual(code, 0)
            self.assertTrue(receipt['all_commands_passed'])
            self.assertEqual((tool/'src/local_tool.py').read_text(), 'VALUE = 11\n')

    def test_general_suite_appends_optional_checks_and_quick_does_not(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.fixture(directory)
            (repo/'tests/quick.py').write_text('raise SystemExit(0)\n')
            for path in verify.GENERAL:
                destination = repo/path
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text('raise SystemExit(0)\n')
            code, quick = self.run_gate(repo, ('tests/quick.py',))
            self.assertEqual(code, 0)
            self.assertEqual(len(quick['commands']), 2)
            code, general = self.run_gate(repo, ('tests/quick.py',), suite='general')
            self.assertEqual(code, 0)
            self.assertTrue(general['all_commands_passed'])
            self.assertEqual(general['suite'], 'general')
            self.assertEqual([entry['command'][1] for entry in general['commands']],
                             ['scripts/audit_repository.py', 'tests/quick.py', *verify.GENERAL])


if __name__ == '__main__':
    unittest.main()
