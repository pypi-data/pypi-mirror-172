""" Simple test. """

# pylint: disable=missing-docstring

import pytest

from super_collator.strategy import Strategy
from super_collator.token import SingleToken
from super_collator.super_collator import align, to_string, to_table


class PosStrategy(Strategy):
    def similarity(self, a, b):
        return 1.0 if a.user_data == b.user_data else 0.0


class TestAlign:
    def test_align_pos(self):
        a = "it/PRP was/VBD a/DT dark/JJ and/CC stormy/JJ night/NN"
        b = "it/PRP is/VBZ a/DT fine/JJ day/NN"

        a = [SingleToken(*s.split("/")) for s in a.split()]
        b = [SingleToken(*s.split("/")) for s in b.split()]
        c, score = align(a, b, PosStrategy())

        print(to_table(c))  # only visible on test failure
        assert to_string(c, 1) == "it is a fine - - day"
