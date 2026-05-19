#!/usr/bin/env python3
"""Generate ntops NineToothed kernel skeleton (unary / binary)."""
from __future__ import annotations

import argparse
from pathlib import Path
from textwrap import dedent

UNARY = dedent(
    '''\
    import ninetoothed
    import ninetoothed.language as ntl
    from ninetoothed import Symbol, Tensor

    BLOCK_SIZE = Symbol("BLOCK_SIZE", constexpr=True)

    def arrangement(input, output, BLOCK_SIZE=BLOCK_SIZE):
        return input.tile((BLOCK_SIZE,)), output.tile((BLOCK_SIZE,))

    def application(input, output):
        x = input
        output = x  # TODO: replace with operator formula

    tensors = (Tensor(1), Tensor(1))
    kernel = ninetoothed.make(arrangement, application, tensors)
    '''
)

BINARY = dedent(
    '''\
    import ninetoothed
    from ninetoothed import Symbol, Tensor

    BLOCK_SIZE = Symbol("BLOCK_SIZE", constexpr=True)

    def arrangement(input, other, output, BLOCK_SIZE=BLOCK_SIZE):
        return (
            input.tile((BLOCK_SIZE,)),
            other.tile((BLOCK_SIZE,)),
            output.tile((BLOCK_SIZE,)),
        )

    def application(input, other, output):
        output = input + other  # TODO: replace; noqa: F841

    tensors = tuple(Tensor(1) for _ in range(3))
    kernel = ninetoothed.make(arrangement, application, tensors)
    '''
)

PATTERNS = {"unary": UNARY, "binary": BINARY}


def main() -> None:
    p = argparse.ArgumentParser(description="Scaffold ntops NineToothed kernel")
    p.add_argument("--name", required=True, help="Operator name, e.g. gelu")
    p.add_argument(
        "--pattern",
        choices=PATTERNS,
        required=True,
        help="unary or binary elementwise template",
    )
    p.add_argument("--out", required=True, type=Path, help="Output .py path")
    args = p.parse_args()
    body = PATTERNS[args.pattern]
    header = f'"""NineToothed kernel: {args.name} (scaffold — edit application)."""\n\n'
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(header + body, encoding="utf-8")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
