"""Main module."""

from typing import Tuple, Optional

from .token import TT, TSeq
from .strategy import Strategy
from .aligner import Aligner


def align(
    a: TSeq[TT],
    b: TSeq[TT],
    strategy: Strategy[TT],
    aligner: Optional[Aligner] = None,
) -> Tuple[TSeq[TT], float]:
    """Preprocess the tokens and call the aligner."""

    if aligner is None:
        aligner = Aligner()  # set the default aligner

    any(map(strategy.preprocess, a))
    any(map(strategy.preprocess, b))

    return aligner.align(strategy, a, b)


def to_string(tokens: TSeq, rank: int = 0):
    """Convert a sequence of tokens into a string.

    This function calls str() on each token.
    """
    return " ".join([str(mt[rank] or "-") for mt in tokens])


def to_table(seq: TSeq):
    """Convert a sequence of aligned tokens into an ascii table.

    This function calls str() on each token.
    """
    strings_columnwise = [[str(t or "-") for t in mt] for mt in seq]
    column_widths = [max(map(len, col)) for col in strings_columnwise]
    result = []
    for row in zip(*strings_columnwise):
        for s, length in zip(row, column_widths):
            result.append(f"{s:<{length + 1}}")
        result.append("\n")
    return "".join(result)
