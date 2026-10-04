#!/usr/bin/env python3
"""Replay the saved cvc5 proof certificates for Theorems I and Iw in Ethos.

The repository stores three cvc5 1.4.1 unsatisfiability proofs in cvc5's
Cooperating Proof Calculus (CPC) format:

  results/2026-09-30-six-integer-two-plane/cvc5.proof.gz
      the original "count" encoding of Theorem I (six distinct points)
  results/2026-09-30-six-integer-review/gap-bijection.proof.gz
      the reviewer's independent gap/bijection encoding of Theorem I
  results/2026-09-30-six-integer-weighted-review-ordered/gap-bijection.proof.gz
      the reviewer's gap/bijection encoding of Theorem Iw (repeated atoms)

This script checks each proof with the Ethos checker against the CPC
signature shipped in the cvc5 1.4.1 source tree, and checks with
check_assumptions.py that the proof's free assumptions are exactly (a
sub-multiset of) the assertions of the saved SMT-LIB problem.  Ethos is a
separate program from cvc5; cvc5's own "check-proofs" option is not involved.

Usage:
  python tools/proof_replay/replay_cpc_proofs.py --ethos PATH/TO/ethos \
      --cpc PATH/TO/cvc5-1.4.1/proofs/eo/cpc/Cpc.eo [--out DIR]

Standard library only.  Writes DIR/replay.json with hashes, commands,
Ethos output and timings.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

PROOFS = [
    {
        "name": "theorem-I-count-encoding",
        "proof": "results/2026-09-30-six-integer-two-plane/cvc5.proof.gz",
        "problem": "results/2026-09-30-six-integer-two-plane/count.smt2",
    },
    {
        "name": "theorem-I-gap-bijection-encoding",
        "proof": "results/2026-09-30-six-integer-review/gap-bijection.proof.gz",
        "problem": "results/2026-09-30-six-integer-review/gap-bijection.smt2",
    },
    {
        "name": "theorem-Iw-gap-bijection-encoding",
        "proof": "results/2026-09-30-six-integer-weighted-review-ordered/gap-bijection.proof.gz",
        "problem": "results/2026-09-30-six-integer-weighted-review-ordered/gap-bijection.smt2",
    },
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(proof_gz: Path, cpc: Path, dest: Path) -> None:
    """cvc5's API output wraps the proof in one outer pair of parentheses and
    has no include line; Ethos wants the signature included first."""
    text = gzip.decompress(proof_gz.read_bytes()).decode("utf-8")
    lines = text.rstrip("\n").split("\n")
    if lines[0].strip() != "(" or lines[-1].strip() != ")":
        raise SystemExit(f"{proof_gz}: unexpected wrapper lines {lines[0]!r} .. {lines[-1]!r}")
    body = "\n".join(lines[1:-1])
    dest.write_text(f'(include "{cpc}")\n{body}\n')


def portable(c) -> str:
    """Record repository paths relative to the root; keep other arguments as given."""
    s = str(c)
    try:
        return str(Path(s).resolve().relative_to(ROOT))
    except (ValueError, OSError):
        return Path(s).name if s.startswith("/") else s


def run(cmd, timeout):
    t = time.monotonic()
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return {"command": [portable(c) for c in cmd], "returncode": proc.returncode,
            "stdout": proc.stdout[-2000:], "stderr": proc.stderr[-2000:],
            "seconds": round(time.monotonic() - t, 2)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ethos", type=Path, required=True)
    ap.add_argument("--cpc", type=Path, required=True, help="path to cvc5's proofs/eo/cpc/Cpc.eo")
    ap.add_argument("--ethos-commit", default="", help="git commit of the Ethos checkout, for the record")
    ap.add_argument("--cvc5-version", default="1.4.1")
    ap.add_argument("--out", type=Path, default=HERE / "evidence")
    ap.add_argument("--timeout", type=float, default=3600)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    cpc = args.cpc.resolve()
    cpc_dir = cpc.parent
    signature_files = sorted(p for p in cpc_dir.rglob("*.eo"))
    report = {
        "ethos": args.ethos.name, "ethos_commit": args.ethos_commit,
        "ethos_show_config": run([args.ethos, "--show-config"], 60)["stdout"],
        "cvc5_version_of_signature": args.cvc5_version,
        "cpc_signature_file": cpc.name,
        "cpc_signature": {str(p.relative_to(cpc_dir)): sha256(p) for p in signature_files},
        "proofs": [],
    }
    all_ok = True
    with tempfile.TemporaryDirectory(prefix="cpc-replay-") as tmp:
        for item in PROOFS:
            proof_gz = ROOT / item["proof"]
            problem = ROOT / item["problem"]
            eo = Path(tmp) / (item["name"] + ".eo")
            prepare(proof_gz, cpc, eo)
            rec = dict(item)
            rec["proof_sha256"] = sha256(proof_gz)
            rec["problem_sha256"] = sha256(problem)
            rec["prepared_eo_bytes"] = eo.stat().st_size
            rec["ethos"] = run([args.ethos, "--require-proof-of-false", eo], args.timeout)
            rec["assumptions"] = run([sys.executable, HERE / "check_assumptions.py", eo, problem], args.timeout)
            rec["ethos_correct"] = rec["ethos"]["returncode"] == 0 and rec["ethos"]["stdout"].strip().endswith("correct")
            rec["assumptions_match"] = rec["assumptions"]["returncode"] == 0
            rec["verdict"] = "REPLAYED" if rec["ethos_correct"] and rec["assumptions_match"] else "FAILED"
            all_ok &= rec["verdict"] == "REPLAYED"
            report["proofs"].append(rec)
            print(f'{rec["verdict"]:9s} {item["name"]}  ethos={rec["ethos"]["stdout"].strip()[-10:]} '
                  f'({rec["ethos"]["seconds"]}s)  assumptions={"match" if rec["assumptions_match"] else "MISMATCH"}', flush=True)
    report["all_replayed"] = all_ok
    (args.out / "replay.json").write_text(json.dumps(report, indent=2) + "\n")
    print("all proofs replayed" if all_ok else "SOME PROOF FAILED TO REPLAY")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
