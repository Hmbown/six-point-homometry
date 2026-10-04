"""Checks for tools/proof_replay/check_assumptions.py on small synthetic inputs."""
from pathlib import Path
import importlib.util
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "check_assumptions.py"
spec = importlib.util.spec_from_file_location("ca", SCRIPT)
ca = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ca)

PROBLEM = """(set-logic QF_LRA)
(declare-fun x () Real)
(declare-fun y () Real)
(define-fun d () Real (- x y))
(assert (> d 0))
(assert (and (< x 1)))
(assert (or (= x y) (> y 2)))
(assert (< y 0.5))
"""

PROOF_OK = """(
(declare-const x Real)
(declare-const y Real)
(define @t1 () (> (- x y) 0/1))
(define @t2 () (< x 1/1))
(define @t3 () (or (= x y) (> y 2/1)))
(assume @p1 @t1)
(assume @p2 @t2)
(assume @p3 @t3)
(step @p4 false :rule contra :premises (@p1 @p2 @p3))
)
"""

PROOF_BAD = PROOF_OK.replace("(define @t2 () (< x 1/1))", "(define @t2 () (< x 2/1))")
PROOF_NOT_FALSE = PROOF_OK.replace("(step @p4 false", "(step @p4 (> x 0/1)")


def run(proof_text):
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "p.eo"
        q = Path(tmp) / "q.smt2"
        p.write_text(proof_text)
        q.write_text(PROBLEM)
        r = subprocess.run([sys.executable, str(SCRIPT), str(p), str(q)], capture_output=True, text=True)
        return r.returncode, r.stdout


def main():
    code, out = run(PROOF_OK)
    assert code == 0 and "MATCH" in out and "1 assertion(s) unused" in out, out
    code, out = run(PROOF_BAD)
    assert code == 1 and "MISMATCH" in out, out
    code, out = run(PROOF_NOT_FALSE)
    assert code == 1, out
    # numeral and unary-and normalization
    assert ca.normalize(("and", ("<", "x", "1")), {}) == ("<", "x", ("#num", ca.Fraction(1)))
    assert ca.normalize("3/2", {}) == ("#num", ca.Fraction(3, 2))
    assert ca.normalize(("-", "2"), {}) == ("#num", ca.Fraction(-2))
    print("PASS test_check_assumptions")


if __name__ == "__main__":
    main()
