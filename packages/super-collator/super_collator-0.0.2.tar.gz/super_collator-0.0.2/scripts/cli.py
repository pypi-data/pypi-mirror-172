"""CLI script"""

import argparse
import sys

from super_collator.aligner import Aligner
from super_collator.strategy import CommonNgramsStrategy
from super_collator.token import SingleToken
from super_collator.super_collator import align, to_table


def build_parser(description: str) -> argparse.ArgumentParser:
    """Build the commandline parser."""
    parser = argparse.ArgumentParser(
        description=description,
        # don't wrap my description
        formatter_class=argparse.RawDescriptionHelpFormatter,
        fromfile_prefix_chars="@",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="count",
        help="increase output verbosity",
        default=0,
    )
    parser.add_argument(
        "inputs",
        metavar="TOKENS",
        type=str,
        nargs="+",
        help="the input strings to process",
    )

    return parser


def main():
    parser = build_parser(__doc__)
    args = parser.parse_args()

    a = [SingleToken(s) for s in args.inputs[0].split()]
    for inp in args.inputs[1:]:
        b = [SingleToken(s) for s in inp.split()]
        a, score = align(a, b, CommonNgramsStrategy(2))

    print(to_table(a).strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
