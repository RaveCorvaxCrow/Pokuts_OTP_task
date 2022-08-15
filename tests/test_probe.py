import pytest
from pytest import assume


def test_simple_assume():
    x, y = 1, 2
    with assume: assert x == y
    with assume: assert True
    with assume: assert False
