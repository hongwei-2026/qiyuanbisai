#!/usr/bin/env python3
"""Preflight checks for ntops-copilot skill layout or kernel .py files."""
from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

SKILL_REQUIRED = ("SKILL.md", "reference.md")
KERNEL_REQUIRED_CALLS = ("arrangement", "application")
KERNEL_REQUIRED_ATTR = "make"


def check_skill_dir(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.is_dir():
        return [f"not a directory: {path}"]
    for name in SKILL_REQUIRED:
        if not (path / name).is_file():
            errors.append(f"missing {name}")
    skill_md = path / "SKILL.md"
    if skill_md.is_file():
        text = skill_md.read_text(encoding="utf-8")
        if "name:" not in text[:400]:
            errors.append("SKILL.md missing YAML frontmatter name:")
        if "ninetoothed.make" not in text:
            errors.append("SKILL.md should mention ninetoothed.make workflow")
    return errors


def check_kernel(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"not a file: {path}"]
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as e:
        return [f"syntax error: {e}"]

    funcs = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    for fn in KERNEL_REQUIRED_CALLS:
        if fn not in funcs:
            errors.append(f"missing function: {fn}")

    has_make = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute) and func.attr == KERNEL_REQUIRED_ATTR:
                has_make = True
            if isinstance(func, ast.Name) and func.id == "make":
                has_make = True
    if not has_make:
        errors.append("missing ninetoothed.make(...) call")

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        if isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    if "ninetoothed" not in imports:
        errors.append("missing import ninetoothed")

    return errors


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("path", type=Path, help="skill directory or kernel .py")
    p.add_argument("--kernel", action="store_true", help="treat path as kernel file")
    args = p.parse_args()

    if args.kernel:
        errors = check_kernel(args.path)
    else:
        errors = check_skill_dir(args.path)

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        sys.exit(1)
    print("OK: preflight passed")
    sys.exit(0)


if __name__ == "__main__":
    main()
