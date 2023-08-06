""" Simple test. """

# pylint: disable=missing-docstring

import pytest

from super_collator.super_collator import to_string
from super_collator.token import SingleToken


class TestToString:
    def test_to_string(self):
        a = [SingleToken(s) for s in "the quick dog".split()]
        assert to_string(a, 0) == "the quick dog"
        with pytest.raises(IndexError):
            assert to_string(a, 1) == "the quick dog"

