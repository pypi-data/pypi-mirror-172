""" Simple test. """

# pylint: disable=missing-docstring

import pytest

from super_collator.aligner import Aligner
from super_collator.strategy import CommonNgramsStrategy, StringEqualsStrategy
from super_collator.token import SingleToken, MultiToken


class TestCommonNGramsStrategy:
    def test_strategy_preprocess_1(self):
        strategy = CommonNgramsStrategy(1)
        a = SingleToken("hello")
        b = SingleToken("world")
        c = SingleToken("cacao")
        strategy.preprocess(a)
        strategy.preprocess(b)
        strategy.preprocess(c)
        assert len(a.strategy_data) == 4
        assert len(b.strategy_data) == 5
        assert len(c.strategy_data) == 3

    def test_strategy_preprocess_2(self):
        strategy = CommonNgramsStrategy(2)
        a = SingleToken("hello")
        b = SingleToken("world")
        c = SingleToken("cacao")
        strategy.preprocess(a)
        strategy.preprocess(b)
        strategy.preprocess(c)
        assert len(a.strategy_data) == 6
        assert len(b.strategy_data) == 6
        assert len(c.strategy_data) == 5

    def test_strategy_preprocess_3(self):
        strategy = CommonNgramsStrategy(3)
        a = SingleToken("hello")
        b = SingleToken("world")
        c = SingleToken("cacao")
        strategy.preprocess(a)
        strategy.preprocess(b)
        strategy.preprocess(c)
        assert len(a.strategy_data) == 7
        assert len(b.strategy_data) == 7
        assert len(c.strategy_data) == 7

    def test_strategy_similarity(self):
        strategy = CommonNgramsStrategy(2)

        a = SingleToken("hello")
        b = SingleToken("hello")
        strategy.preprocess(a)
        strategy.preprocess(b)
        assert strategy.similarity(a, b) == 2.0

        a = SingleToken("hello")
        b = SingleToken("kitty")
        strategy.preprocess(a)
        strategy.preprocess(b)
        assert strategy.similarity(a, b) == 0.0

        a = SingleToken("hello")
        b = SingleToken("worlo")
        strategy.preprocess(a)
        strategy.preprocess(b)
        assert strategy.similarity(a, b) == 8 / 12

    def test_strategy_similarity_2(self):
        strategy = CommonNgramsStrategy(1)
        a = SingleToken("")
        b = SingleToken("")
        strategy.preprocess(a)
        strategy.preprocess(b)
        assert strategy.similarity(a, b) == 0.0

    def test_strategy_similarity_3(self):
        strategy = StringEqualsStrategy()
        a = SingleToken("abc")
        b = SingleToken("abc")
        c = SingleToken("cde")
        strategy.preprocess(a)
        strategy.preprocess(b)
        assert strategy.similarity(a, b) == 1.0
        assert strategy.similarity(a, c) == 0.0

