#!/usr/bin/env python3
"""Check that a cvc5 CPC proof's free assumptions are exactly the SMT-LIB assertions.

A proof checker (Ethos) establishes that a proof derives `false` from its
`assume` steps.  That is only a proof of unsatisfiability of the *intended*
problem if those assumed formulas are the problem's assertions.  This script
expands the proof's `define`s and the problem's `define-fun`s, normalizes
numerals, and compares the two multisets of formulas.  Standard library only.

Usage: python check_assumptions.py PROOF.eo PROBLEM.smt2
Exit code 0 when every assumption is an assertion and the proof ends in `false`.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path


def tokenize(text: str):
    out = []
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c in " \t\r\n":
            i += 1
        elif c == ";":
            while i < n and text[i] != "\n":
                i += 1
        elif c in "()":
            out.append(c)
            i += 1
        elif c == "|":
            j = text.index("|", i + 1)
            out.append(text[i:j + 1])
            i = j + 1
        elif c == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 1
            out.append(text[i:j + 1])
            i = j + 1
        else:
            j = i
            while j < n and text[j] not in " \t\r\n()":
                j += 1
            out.append(text[i:j])
            i = j
    return out


def parse_all(tokens):
    pos = 0
    items = []

    def read():
        nonlocal pos
        tok = tokens[pos]
        pos += 1
        if tok == "(":
            lst = []
            while tokens[pos] != ")":
                lst.append(read())
            pos += 1
            return tuple(lst)
        if tok == ")":
            raise ValueError("unexpected )")
        return tok

    while pos < len(tokens):
        items.append(read())
    return items


def numeral(tok: str):
    try:
        if "/" in tok:
            a, b = tok.split("/")
            return Fraction(int(a), int(b))
        if "." in tok:
            return Fraction(tok)
        return Fraction(int(tok))
    except (ValueError, ZeroDivisionError):
        return None


def normalize(expr, env):
    """Expand 0-ary definitions and canonicalize numerals; unary minus on a
    numeral is folded; `(- x 0)` is kept as is (both sides print it the same)."""
    if isinstance(expr, str):
        if expr in env:
            return normalize(env[expr], env)
        q = numeral(expr)
        if q is not None:
            return ("#num", q)
        return expr
    if expr and isinstance(expr[0], str) and expr[0] in env and len(expr) == 1:
        return normalize(env[expr[0]], env)
    items = tuple(normalize(e, env) for e in expr)
    if len(items) == 2 and items[0] == "-" and isinstance(items[1], tuple) and items[1][0] == "#num":
        return ("#num", -items[1][1])
    if len(items) == 2 and items[0] in ("and", "or"):
        return items[1]  # cvc5 prints a unary and/or as its single argument
    return items


def load_problem(path: Path):
    env = {}
    asserts = []
    for item in parse_all(tokenize(path.read_text())):
        if not isinstance(item, tuple) or not item:
            continue
        head = item[0]
        if head == "define-fun" and item[2] == ():
            env[item[1]] = item[4]
        elif head == "assert":
            asserts.append(item[1])
    return env, asserts


def load_proof(path: Path):
    env = {}
    assumes = []
    conclusion = None
    text = path.read_text()
    items = parse_all(tokenize(text))
    # cvc5's API output wraps everything in one outer list
    if len(items) == 1 and isinstance(items[0], tuple) and items[0] and isinstance(items[0][0], tuple):
        items = list(items[0])
    for item in items:
        if not isinstance(item, tuple) or not item:
            continue
        head = item[0]
        if head == "define" and item[2] == ():
            env[item[1]] = item[3]
        elif head == "assume":
            assumes.append(item[2])
        elif head == "step":
            conclusion = item[2]
    return env, assumes, conclusion


def main():
    proof_path, problem_path = Path(sys.argv[1]), Path(sys.argv[2])
    penv, asserts = load_problem(problem_path)
    qenv, assumes, conclusion = load_proof(proof_path)
    A = sorted(repr(normalize(a, penv)) for a in asserts)
    B = sorted(repr(normalize(b, qenv)) for b in assumes)
    from collections import Counter
    ca, cb = Counter(A), Counter(B)
    only_problem = list((ca - cb).elements())
    only_proof = list((cb - ca).elements())
    print(f"problem assertions: {len(A)}   proof assumptions: {len(B)}   final step concludes: {conclusion}")
    print(f"assertions not assumed: {len(only_problem)}   assumptions not asserted: {len(only_proof)}")
    for x in only_problem[:5]:
        print("  only in problem:", x[:300])
    for x in only_proof[:5]:
        print("  only in proof:  ", x[:300])
    # Every assumption must be an assertion.  Assertions the proof never uses are
    # allowed: false from a subset of the assertions refutes the whole problem.
    ok = not only_proof and conclusion == "false"
    if only_problem:
        print(f"note: {len(only_problem)} assertion(s) unused by the proof (allowed)")
    print("MATCH: assumptions are a sub-multiset of the assertions and the proof concludes false" if ok else "MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
