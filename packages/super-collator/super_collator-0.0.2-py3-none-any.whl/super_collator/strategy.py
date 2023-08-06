"""This module implements the token comparison strategies."""

from typing import List, Generic

from .token import Token, TT


def bit_count(x: int) -> int:
    """Count the set bits in the given integer.

    Replacement for bit_count in Python < 3.10.
    See: [Warren2013]_, chapter 5, page 81ff.
    """
    x = (x & 0x5555555555555555) + ((x >> 1) & 0x5555555555555555)
    x = (x & 0x3333333333333333) + ((x >> 2) & 0x3333333333333333)
    x = (x & 0x0F0F0F0F0F0F0F0F) + ((x >> 4) & 0x0F0F0F0F0F0F0F0F)
    x = x + (x >> 8)
    x = x + (x >> 16)
    x = x + (x >> 32)
    return x & 0x0000007F


class Strategy(Generic[TT]):
    r"""Base class for all classes that implement a strategy.

    When the aligner wants to compare two tokens, it calls the method
    :func:`similarity`.  This method should return the score of the alignment.  The
    score should increase with the desirability of the alignment, but otherwise there
    are no fixed rules.

    The score must harmonize with the penalties for inserting gaps (these are set in the
    aligner). If the score for opening a gap is -1.0 (the default) then a satisfactory
    match should return a score > 1.0.

    Subclasses will implement different algorithms, like consulting a PAM or BLOSUM
    matrix, or computing a hamming distance between the input tokens.

    Auxiliary input needed for similarity calculation may be stored in
    :attr:`user_data`.  Eg. you can store a POS-tag into :attr:`user_data` and write a
    strategy that uses the POS-tag while computing the similarity.

    The method :func:`preprocess` is called once on every token before the aligner
    starts working.  The strategy may then precompute some values and store them in
    :attr:`strategy_data`.  The total time spent in preprocessing will be linear in
    `\mathcal{O}(n+m)` while the total time spent in alignment is quadratic in
    `\mathcal{O}(nm)`, with `n` and `m` being the lengths of the two strings to be
    aligned.
    """

    def preprocess(self, a: Token[TT]) -> None:
        """Preprocess a token.

        This function is called once for each token to give us a chance to preprocess
        it into a more easily comparable form.
        """

    def similarity(self, a: Token[TT], b: Token[TT]) -> float:
        """Return similarity between two tokens."""
        raise NotImplementedError()


class StringEqualsStrategy(Strategy[TT]):
    """Calculates the similarity of two string tokens by string equality."""

    def similarity(self, a: Token[TT], b: Token[TT]) -> float:
        """Return 1.0 if the strings are equal, 0.0 otherwise."""
        for t1 in a:
            for t2 in b:
                if str(t1) == str(t2):
                    return 1.0
        return 0.0


class CommonNgramsStrategy(Strategy[str]):
    """Calculates the similarity of two string tokens by common N-grams.

    The similarity score is 4 times the count of common Ngrams divided by the count of
    all Ngrams.
    """

    def __init__(self, n: int = 2):
        self.n = n

    def similarity(self, a: Token[TT], b: Token[TT]) -> float:
        """Return similarity between two tokens."""
        total = len(a.strategy_data) + len(b.strategy_data)
        if total == 0:
            return 0.0
        common = len(a.strategy_data & b.strategy_data)
        return 4 * common / total

    @staticmethod
    def split_ngrams(s: str, n: int) -> List[str]:
        """Split a string into ngrams."""
        if n == 1:
            return list(s)
        pad = " " * (n - 1)
        sp = pad + s + pad
        return [sp[i : i + n] for i in range(len(s) + n - 1)]

    def preprocess(self, a: Token[str]) -> None:
        a.strategy_data = set()
        for st in a:
            a.strategy_data.update(self.split_ngrams(str(st), self.n))
