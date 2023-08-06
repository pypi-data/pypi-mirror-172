"""This module implements token."""

from typing import (
    Any,
    Optional,
    Sequence,
    Iterator,
    Generic,
    TypeVar,
)


TT = TypeVar("TT")  # Token Type


class Token(Generic[TT]):
    """The token API.

    Implemented by SingleToken and MultiToken.
    """

    def __init__(self):
        """Initialize the token."""
        self.strategy_data: Any = None
        """A data store reserved for use by strategies."""

    def __len__(self) -> int:
        """Return how many tokens are in the tree."""
        raise NotImplementedError()

    def __iter__(self) -> Iterator["OptToken"]:
        """Iterate the tokens in the tree."""
        raise NotImplementedError()

    def __getitem__(self, n) -> "OptToken":
        """Return the nth token in the iteration."""
        raise NotImplementedError()

    def __str__(self) -> str:
        """Return a string represenation of the token tree."""
        raise NotImplementedError()


OptToken = Optional[Token[TT]]
TSeq = Sequence[Token[TT]]


class SingleToken(Token[TT]):
    """Represents one input token."""

    def __init__(self, data: TT, user_data: Any = None):
        """Initialize the token.

        :param Any user_data: user data that will be round-tripped unchanged.
        """
        super().__init__()
        self.data: TT = data
        """The data to align."""
        self.user_data: Any = user_data
        """A data store reserved for user data."""

    def __len__(self) -> int:
        return 1

    def __iter__(self) -> Iterator[Optional[Token[TT]]]:
        yield self

    def __getitem__(self, n: int) -> Optional[Token[TT]]:
        if n == 0:
            return self
        raise IndexError()

    def __str__(self) -> str:
        return str(self.data)


# class Gap(Token):
#     pass


class MultiToken(Token[TT]):
    """A container for one or two tokens.

    A MultiToken is a node in a binary tree that mimics the order in which multiple
    aligments were done.

    An alignment produces a sequence of MultiToken trees.  Each tree contains all the
    tokens that were aligned at this position plus any gaps represented as None.
    """

    def __init__(self, *args: Optional[Token[TT]]):
        super().__init__()
        self._tokens = args

    def __len__(self) -> int:
        return sum(len(t) if t is not None else 1 for t in self._tokens)  # recurse

    def __iter__(self) -> Iterator[Optional[Token[TT]]]:
        for t in self._tokens:
            if t is not None:
                yield from t.__iter__()
            else:
                yield None

    def __getitem__(self, n: int) -> Optional[Token[TT]]:
        return list(self)[n]

    def __str__(self) -> str:
        return " ".join([str(t) if t is not None else "-" for t in self._tokens])
