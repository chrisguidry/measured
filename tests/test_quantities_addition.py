# https://en.wikipedia.org/wiki/Abelian_group

import pytest

from measured import Quantity
from measured.si import Hertz, Meter, Second


@pytest.mark.parametrize(
    "a, b, c",
    [
        (2 * Meter, 3 * Meter, 4 * Meter),
        (2 * Hertz, 3 * Hertz, 4 * Hertz),
        (2 * Meter / Second, 3 * Meter / Second, 4 * Meter / Second),
        (2 * Meter**2, 3 * Meter**2, 4 * Meter**2),
    ],
)
def test_abelian_addition_associativity(a: Quantity, b: Quantity, c: Quantity):
    assert (a + b) + c == a + (b + c)


@pytest.mark.parametrize(
    "a",
    [
        2 * Meter,
        3 * Hertz,
        4 * Meter / Second,
        5 * Meter**2,
    ],
)
def test_abelian_addition_identity(a: Quantity):
    identity = 0 * a.unit
    inverse = -a

    assert identity + a == a
    assert a + identity == a

    assert a - identity == a
    assert identity - a == inverse


@pytest.mark.parametrize(
    "a",
    [
        2 * Meter,
        3 * Hertz,
        4 * Meter / Second,
        5 * Meter**2,
    ],
)
def test_abelian_addition_inverse(a: Quantity):
    identity = 0 * a.unit
    inverse = -a

    assert inverse + a == a + inverse
    assert inverse + a == identity


@pytest.mark.parametrize(
    "a, b",
    [
        (2 * Meter, 3 * Meter),
        (2 * Hertz, 3 * Hertz),
        (2 * Meter / Second, 3 * Meter / Second),
        (2 * Meter**2, 3 * Meter**2),
    ],
)
def test_abelian_addition_commutativity(a: Quantity, b: Quantity):
    assert a + b == b + a
