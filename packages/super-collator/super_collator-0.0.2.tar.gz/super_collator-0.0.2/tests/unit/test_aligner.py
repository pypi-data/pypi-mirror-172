""" Simple test. """

# pylint: disable=missing-docstring

import pytest

from super_collator.aligner import Aligner
from super_collator.strategy import CommonNgramsStrategy
from super_collator.token import SingleToken, MultiToken
from super_collator.super_collator import align, to_string, to_table


@pytest.fixture
def the_fox():
    return [
        SingleToken(s) for s in "the quick brown fox jumps over the lazy dog".split()
    ]


STRATEGIES = [CommonNgramsStrategy(2), CommonNgramsStrategy(3)]


@pytest.mark.parametrize("strategy", STRATEGIES)
class TestAlign:
    def test_align_1(self, strategy, the_fox):
        b = [SingleToken(s) for s in "rumps".split()]
        aligned, score = align(the_fox, b, strategy)
        assert to_string(aligned, 1) == "- - - - rumps - - - -"

    def test_align_2(self, strategy, the_fox):
        b = [SingleToken(s) for s in "the brown dog".split()]
        aligned, score = align(the_fox, b, strategy)
        assert to_string(aligned, 1) == "the - brown - - - - - dog"

    def test_align_3(self, strategy, the_fox):
        aligner = Aligner()
        aligner.start_score = 0
        b = [SingleToken(s) for s in "the sissy".split()]
        aligned, score = align(the_fox, b, strategy, aligner)
        assert to_string(aligned, 1) == "- - - - - - the sissy -"


@pytest.mark.parametrize("strategy", STRATEGIES)
class TestMultiAlign:
    def test_multi_align_1(self, strategy, the_fox):
        aligner = Aligner()
        aligner.open_score = -0.5
        aligner.start_score = -0.5
        a = the_fox
        b = [SingleToken(s) for s in "the quick dog".split()]
        c = [SingleToken(s) for s in "rumps".split()]
        d = [SingleToken(s) for s in "lady".split()]
        assert to_string(b, 0) == "the quick dog"

        e, score = align(a, b, strategy, aligner)
        assert to_string(e, 1) == "the quick - - - - - - dog"

        f, score = align(e, c, strategy, aligner)
        assert to_string(f, 2) == "- - - - rumps - - - -"

        g, score = align(f, d, strategy, aligner)
        assert to_string(g, 3) == "- - - - - - - lady -"
