#!/usr/bin/env python3
"""Pack Proposal + skill into one zip for InfiniTensor submission attachment."""
from __future__ import annotations

import zipfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / f"submission-proposal-{datetime.now().strftime('%Y%m%d')}.zip"

INCLUDE = [
    "README.md",
    "HONOR_CODE.md",
    "REFERENCE.md",
    "docs/Proposal.md",
    "skills/ntops-copilot",
    "scripts",
]


def main() -> None:
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in INCLUDE:
            path = ROOT / rel
            if path.is_file():
                zf.write(path, rel)
            elif path.is_dir():
                for f in path.rglob("*"):
                    if f.is_file() and "__pycache__" not in f.parts:
                        zf.write(f, f.relative_to(ROOT).as_posix())
            else:
                print(f"skip missing: {rel}")
    print(f"Created {OUT}")


if __name__ == "__main__":
    main()
