#!/usr/bin/env python3
"""Environment guard: fail LOUDLY if the interpreter has the numpy temporary-elision bug.

Background (notes/env_audit.md, notes/p3_review.md §5): python 3.14.7 + numpy 1.26.4
(an unsupported combination) misapplies numpy's "temporary elision": inside a function,
`c = a * b` writes its result INTO the local array `a` when a >= 256 KiB.  Results computed
under such an interpreter are silently wrong.  Use the project venv:

    ./.venv/bin/python tests/test_env.py

Each check below is one measured trigger form of the bug (all verified to fail under
python 3.14.7/numpy 1.26.4 and to pass under .venv python 3.12.12/numpy 2.5.3).
Run directly (exit status 1 on failure) or under pytest.
"""
import sys

import numpy as np

N_F64 = 40000          # 320 KB > 256 KiB elision threshold
BANNER = ("ENVIRONMENT BUG: this interpreter (python {py}, numpy {npv}) corrupts local numpy "
          "arrays via temporary elision. Results computed with it are NOT trustworthy. "
          "Use ./.venv/bin/python (see notes/env_audit.md).")


def _msg():
    return BANNER.format(py=sys.version.split()[0], npv=np.__version__)


def _minimal_repro(N):
    a = np.full(N, 2.0) + 0.0
    b = np.full(N, 3.0) + 0.0
    c = a * b  # noqa: F841
    return float(a[0])


def test_minimal_repro_gives_2():
    """The canonical minimal repro must return 2.0 (the bad interpreter returns 6.0)."""
    for N in (32768, N_F64, 1 << 20):
        assert _minimal_repro(N) == 2.0, _msg() + f" [minimal repro, N={N}]"


def _callee(x):
    y = x * 2
    return y


def test_argument_not_overwritten_by_callee():
    """A callee computing x*2 must not overwrite the caller's local array."""
    z = np.full(N_F64, 6.0) + 0.0
    y = _callee(z)
    assert float(z[0]) == 6.0 and float(y[0]) == 12.0, _msg() + " [callee x*2 overwrote caller array]"


def test_scalar_left_commutative():
    """`2 * b` must not overwrite b (right operand of a commutative op)."""
    b = np.full(N_F64, 3.0) + 0.0
    d = 2 * b  # noqa: F841
    assert float(b[0]) == 3.0, _msg() + " [2*b overwrote b]"


def test_int_bool_complex_and_unary():
    """Integer, boolean, complex binary ops and unary minus must not modify operands."""
    a = np.arange(N_F64, dtype=np.int64) + 0
    c = a + 1  # noqa: F841
    assert int(a[1]) == 1, _msg() + " [int64 a+1 overwrote a]"
    m = np.zeros(1 << 19, dtype=bool) | np.zeros(1, dtype=bool)
    m[0] = True
    q = m & np.zeros(1 << 19, dtype=bool)  # noqa: F841
    assert bool(m[0]), _msg() + " [bool m&x overwrote m]"
    z = np.full(N_F64, 6.0) + 0j
    w = z * 2  # noqa: F841
    assert z[0] == 6.0, _msg() + " [complex z*2 overwrote z]"
    u = np.full(N_F64, 6.0) + 0.0
    v = -u  # noqa: F841
    assert float(u[0]) == 6.0, _msg() + " [unary -u overwrote u]"


def test_chained_expression_value():
    """Value-level check: b = a*2; c = b + a must equal 3a (bad interpreter gives 4a)."""
    a = np.full(N_F64, 6.0) + 0.0
    b = a * 2
    c = b + a
    assert float(c[0]) == 18.0, _msg() + f" [c = a*2 + a gave {float(c[0])}, expected 18.0]"


if __name__ == "__main__":
    print(f"python {sys.version.split()[0]} ({sys.executable}), numpy {np.__version__}")
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print("PASS", name)
            except AssertionError as e:
                fails += 1
                print("FAIL", name, "--", e)
    if fails:
        print("\n" + "!" * 78 + "\n" + _msg() + "\n" + "!" * 78)
    sys.exit(1 if fails else 0)
