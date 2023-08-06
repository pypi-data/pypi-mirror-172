"""This module implements the aligner."""

import collections
import logging
from typing import Tuple, List

from .token import Token, MultiToken, TT, TSeq
from .strategy import Strategy


class Data:
    """Private data class for the Needleman-Wunsch+Gotoh sequence aligner."""

    __slots__ = ("score", "p", "q", "pSize", "qSize")

    def __init__(self, score: float):
        self.score: float = score
        """The current score."""
        self.p: float = 0.0
        """`P_{m,n}` in [Gotoh1982]_."""
        self.q: float = 0.0
        """`Q_{m,n}` in [Gotoh1982]_."""
        self.pSize: int = 0
        """The size of the p gap. `k` in [Gotoh1982]_."""
        self.qSize: int = 0
        """The size of the q gap. `k` in [Gotoh1982]_."""


class Aligner:
    r"""A generic Needleman-Wunsch+Gotoh sequence aligner.

    This implementation uses Gotoh's improvements to get `\mathcal{O}(mn)` running time
    and reduce memory requirements to essentially the backtracking matrix only.  In
    Gotoh's technique the gap weight formula must be of the special form `w_k = uk + v`
    (affine gap).  `k` is the gap size, `v` is the gap opening score and `u` the gap
    extension score.

    The aligner is type-agnostic and expects only to call the method
    :func:`Strategy.similarity` on the given strategy.

    .. seealso::

       [NeedlemanWunsch1970]_

       [Gotoh1982]_
    """

    __slots__ = ("open_score", "extend_score", "start_score")

    def __init__(
        self,
        start_score: float = -1.0,
        open_score: float = -1.0,
        extend_score: float = -0.5,
    ):
        self.start_score: float = start_score
        """The gap opening score at the start of the string.
        Set this to 0 to find local alignments."""
        self.open_score: float = open_score
        """The gap opening score `v`."""
        self.extend_score: float = extend_score
        """The gap extension score `u`."""

    def align(
        self, strategy: Strategy[TT], tokens_a: TSeq[TT], tokens_b: TSeq[TT]
    ) -> Tuple[TSeq[TT], float]:
        """Align two sequences.

        :return: the aligned sequence (of MultiTokens) and the score
        """

        len_a = len(tokens_a)
        len_b = len(tokens_b)

        len_matrix: List[List[int]] = []  # list[len_a + 1]
        """The backtracking matrix.  0 stands for a match.  Negative numbers represent a
        DEL TOP operation.  Positive numbers represent an INS LEFT operation.  The abs()
        of the number is the length of the gap.
        """
        matrix: List[List[Data]] = []
        """The scoring matrix. We need only the last row of the scoring matrix for our
        calculations, so we build the full scoring matrix only when debugging.
        """
        this_len_row: List[int] = []  # list[len_b + 1]
        """The current row of the backtracking matrix."""
        this_row: List[Data] = []  # list[len_b + 1]
        """The current row of the scoring matrix."""

        # Initialize len_matrix and one row of the scoring matrix.

        len_matrix.append(this_len_row)
        this_row.append(Data(0.0))
        this_len_row.append(0)

        for j in range(1, len_b + 1):
            data = Data(self.start_score + (j - 1) * self.extend_score)
            data.p = data.score
            # data.pSize = j;
            this_row.append(data)
            this_len_row.append(j)

        if __debug__:
            matrix = []
            matrix.append(this_row[:])

        # Score the matrix
        for i, a in enumerate(tokens_a, start=1):

            # add new len_row to matrix
            this_len_row = []
            len_matrix.append(this_len_row)
            this_len_row.append(-i)
            # DEL TOP

            diag = this_row[0]
            left = Data(self.start_score + (i - 1) * self.extend_score)
            left.q = left.score
            # left.qSize = i
            j = 0
            for j, b in enumerate(tokens_b, start=1):
                top = this_row[j]
                curr = Data(0.0)

                curr.p = top.score + self.open_score
                curr.pSize = 1
                if curr.p < top.p + self.extend_score:
                    curr.p = top.p + self.extend_score
                    curr.pSize = top.pSize + 1

                curr.q = left.score + self.open_score
                curr.qSize = 1
                if curr.q < left.q + self.extend_score:
                    curr.q = left.q + self.extend_score
                    curr.qSize = left.qSize + 1

                d: float = diag.score + strategy.similarity(a, b)

                # Decide which operation is optimal and perform it
                if (d > curr.p) and (d > curr.q):
                    curr.score = d
                    this_len_row.append(0)
                elif curr.q > curr.p:
                    curr.score = curr.q
                    this_len_row.append(curr.qSize)  # INS LEFT
                else:
                    curr.score = curr.p
                    this_len_row.append(-curr.pSize)  # DEL TOP

                # Advance to next column
                this_row[j - 1] = left
                this_row[j] = curr
                diag = top
                left = curr

            if __debug__:
                matrix.append(this_row[:])

        # Walk back and output alignments.

        alignment: collections.deque[Token[TT]] = collections.deque()

        i = len_a
        j = len_b
        while (i > 0) or (j > 0):
            len_m = len_matrix[i][j]
            if len_m == 0:
                alignment.appendleft(MultiToken(tokens_a[i - 1], tokens_b[j - 1]))
                i -= 1
                j -= 1
            else:
                if len_m < 0:
                    for _ in range(-len_m):
                        alignment.appendleft(MultiToken(tokens_a[i - 1], None))
                        i -= 1
                else:
                    for _ in range(len_m):
                        alignment.appendleft(MultiToken(None, tokens_b[j - 1]))
                        j -= 1

        if __debug__:
            logging.debug(build_debug_matrix(matrix, len_matrix, tokens_a, tokens_b))

        return alignment, this_row[-1].score


def build_debug_matrix(
    matrix: List[List[Data]],
    len_matrix: List[List[int]],
    ts_a: TSeq,
    ts_b: TSeq,
) -> str:
    """Build a human-readable debug matrix.

    :param matrix: the full scoring matrix
    :param len_matrix: the backtracking matrix
    :param ts_a: the first aligned string
    :param ts_b: the second aligned string
    :return str: the debug matrix as human readable string
    """

    s = []

    s.append(str.format("{0:29s} | ", ""))
    s.append(str.format("{0:29s} | ", ""))
    for b in ts_b:
        s.append(str.format("{0:29s} | ", str(b)))
    s.append("\n")

    for i, m in enumerate(matrix):
        s.append(str.format("{0:>29s} | ", str(ts_a[i - 1]) if i > 0 else ""))
        _debug_add(m, len_matrix[i], s)
    s.append("\n")

    return "".join(s)


def _debug_add(data_row: List[Data], len_row: List[int], out: List[str]):
    """
    Private helper function.

    :param data_row:
    :param len_row:
    :param out:
    """

    for i, data in enumerate(data_row):
        l = len_row[i]
        if l == 0:
            out.append("↖ ")
        else:
            if l < 0:
                out.append("↑ ")
            else:
                out.append("← ")
        out.append(str.format("{0: 2.6f} ", data.score))
        out.append(str.format("{0: 2.2f} ", data.p))
        out.append(str.format("{0: 2d} ", data.pSize))
        out.append(str.format("{0: 2.2f} ", data.q))
        out.append(str.format("{0: 2d} | ", data.qSize))
    out.append("\n")
