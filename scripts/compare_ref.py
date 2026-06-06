#!/usr/bin/env python3
"""Compare application() in candidate kernel vs reference ntops kernel."""
from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path


def extract_application_source(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "application":
            if hasattr(ast, "get_source_segment"):
                seg = ast.get_source_segment(text, node)
                if seg:
                    return seg.strip()
            lines = text.splitlines()
            start = node.lineno - 1
            end = node.end_lineno or node.lineno
            return "\n".join(lines[start:end]).strip()
    return None


def normalize(body: str) -> str:
    lines = []
    for ln in body.splitlines():
        ln = ln.strip()
        if ln.startswith("def "):
            continue
        if "#" in ln:
            ln = ln.split("#", 1)[0].strip()
        if ln:
            lines.append(ln)
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description="Diff application() vs reference kernel")
    p.add_argument("candidate", type=Path, help="candidate kernel .py")
    p.add_argument("--ref", type=Path, required=True, help="reference kernel .py")
    args = p.parse_args()

    cand = extract_application_source(args.candidate)
    ref = extract_application_source(args.ref)
    if cand is None:
        print("FAIL: candidate missing application()", file=sys.stderr)
        return 1
    if ref is None:
        print("FAIL: reference missing application()", file=sys.stderr)
        return 1

    nc, nr = normalize(cand), normalize(ref)
    if nc == nr:
        print("OK: application() matches reference")
        return 0

    print("WARN: application() differs from reference")
    print("--- candidate")
    print(nc)
    print("--- reference")
    print(nr)
    print("--- hint: align formula using skills/ntops-copilot/formulas.md")
    return 2


if __name__ == "__main__":
    sys.exit(main())
