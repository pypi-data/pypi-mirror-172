""" Simple test. """

# pylint: disable=missing-docstring

import pytest

from super_collator.token import SingleToken, MultiToken


class TestToken:
    def test_token(self):
        t = SingleToken("string")
        assert len(t) == 1
        assert str(t) == "string"


class TestMultiToken:
    def test_multitoken(self):
        mt1 = MultiToken(SingleToken("string1"), SingleToken("string2"))
        assert len(mt1) == 2
        mt2 = MultiToken(SingleToken("string3"), None)
        assert len(mt2) == 2
        mt3 = MultiToken(mt1, mt2)
        assert len(mt3) == 4
        assert str(mt3) == "string1 string2 string3 -"
