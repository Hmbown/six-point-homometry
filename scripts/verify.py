#!/usr/bin/env python3
"""Bounded verification in a disposable copy; preserve archival evidence."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
QUICK = (
    'tests/test_env.py',
    'tests/run_tests.py',
    'tests/test_six_bloom_support.py',
    'tests/test_six_bloom_primary.py',
    'tests/test_six_bloom_primary_review.py',
    'tests/test_six_generate.py',
    'tests/test_six_generate_review.py',
    'tests/test_weighted_subgroup.py',
    'tests/test_weighted_subgroup_review.py',
    'tests/test_weighted_six_incidence.py',
    'tests/test_weighted_six_review.py',
    'tests/test_repository_audit.py',
    'tests/test_verify_runner.py',
    'tools/inverse_grid/tests/test_inverse_grid.py',
    'tools/inverse_grid/tests/test_inverse_grid_review.py',
    'tools/inverse_grid/tests/test_inverse_grid_benchmark.py',
    'tools/iw_enumeration/tests/test_iw_enumeration.py',
    'tools/proof_replay/tests/test_check_assumptions.py',
)
CERTIFICATES = (
    'tests/test_six_cylinder_branches_review.py',
    'tests/test_six_free_rank_growth.py',
    'tests/test_six_low_rank_mechanisms_review.py',
    'tests/test_six_finite_torsion_review.py',
)
GENERAL = (
    'tools/general_matching/tests/test_general_tree_bound.py',
    'tools/general_matching/tests/test_general_matching_reduction_review.py',
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--suite', choices=('quick', 'certificates', 'general'), default='quick',
                        help='quick: bounded default; certificates: add inherited checks; '
                             'general: add new general-matching checks (requires an existing C11 compiler)')
    parser.add_argument('--timeout', type=float, default=180,
                        help='wall-clock limit per command in seconds')
    parser.add_argument('--out', type=Path, default=ROOT/'.reproduction/verification')
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    output = args.out.resolve()
    output.mkdir(parents=True, exist_ok=True)
    commands = [list((sys.executable, 'scripts/audit_repository.py'))]
    commands.extend([sys.executable, test] for test in QUICK)
    if args.suite == 'certificates':
        commands.extend([sys.executable, test] for test in CERTIFICATES)
    elif args.suite == 'general':
        commands.extend([sys.executable, test] for test in GENERAL)
    records = []
    env = os.environ.copy()
    env.pop('PYTHONPATH', None)
    env['PYTHONNOUSERSITE'] = '1'
    # SymPy's exact simplification path can depend on hashed expression order.
    # A recorded seed makes the same predicates reproducible across platforms.
    env['PYTHONHASHSEED'] = '1'
    env['PYTHONUNBUFFERED'] = '1'
    started = time.monotonic()
    # Never copy a virtual environment, .git directory or previous run output.
    with tempfile.TemporaryDirectory(prefix='homometry-verification-') as directory:
        scratch = Path(directory)
        for name in ('src', 'tests', 'results', 'data', 'notes', 'docs', 'scripts', 'tools', 'formal', '.github'):
            source = ROOT/name
            if source.exists():
                shutil.copytree(source, scratch/name,
                                ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        for name in ('README.md', 'REPORT.md', 'AGENTS.md', 'PROGRESS.md', 'CITATION.cff',
                     '.zenodo.json', '.gitignore', 'requirements.txt', 'requirements-solvers.txt'):
            if (ROOT/name).exists():
                shutil.copy2(ROOT/name, scratch/name)
        for index, command in enumerate(commands):
            command_started = time.monotonic()
            timed_out = False
            try:
                result = subprocess.run(command, cwd=scratch, env=env, text=True,
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                        timeout=args.timeout)
                code, text = result.returncode, result.stdout
            except subprocess.TimeoutExpired as error:
                timed_out = True
                code = 124
                text = error.stdout or ''
                if isinstance(text, bytes):
                    text = text.decode('utf-8', errors='replace')
                text += '\nTIMEOUT: this gate is incomplete.\n'
            log = f'{index:02d}-{Path(command[1]).stem}.log'
            (output/log).write_text(text)
            record = {'command': ['python', *command[1:]], 'exit_code': code,
                      'timed_out': timed_out, 'log': log,
                      'wall_seconds': time.monotonic()-command_started}
            records.append(record)
            print(f'{"PASS" if code == 0 else "FAIL"} {command[1]}', flush=True)
            receipt = {'suite': args.suite, 'all_commands_passed': code == 0,
                       'commands': records, 'temporary_copy': True,
                       'wall_seconds': time.monotonic()-started,
                       'full_exhaustive_regeneration': False}
            (output/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
            if code:
                print(text, file=sys.stderr)
                return code
    print(f'Passed {len(records)} verification commands; logs: {output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
