# https://en.wikipedia.org/wiki/Abelian_group

import pytest

from measured import Quantity, conversions
from measured.si import Hertz, Meter, Minute, Second
from measured.us import Foot, Inch


@pytest.mark.parametrize(
    "a, b, c",
    [
        (2 * Meter, 3 * Meter, 4 * Meter),
        (2 * Hertz, 3 * Hertz, 4 * Hertz),
        (2 * Meter / Second, 3 * Meter / Second, 4 * Meter / Second),
        (2 * Meter**2, 3 * Meter**2, 4 * Meter**2),
    ],
)
def test_abelian_addition_associativity(a: Quantity, b: Quantity, c: Quantity) -> None:
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
def test_abelian_addition_identity(a: Quantity) -> None:
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
def test_abelian_addition_inverse(a: Quantity) -> None:
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
def test_abelian_addition_commutativity(a: Quantity, b: Quantity) -> None:
    assert a + b == b + a


@pytest.mark.parametrize(
    "a, b, c",
    [
        (1 * Meter, 2 * Foot, 1.6096 * Meter),
        (1 * Meter, 2 * Inch, 1.0508 * Meter),
        (2 * Meter / Second, 30 * Foot / Minute, 2.1524 * Meter / Second),
    ],
)
def test_addition_of_different_units(a: Quantity, b: Quantity, c: Quantity) -> None:
    assert a + b == c


def test_addition_requires_same_dimension() -> None:
    with pytest.raises(conversions.ConversionNotFound):
        (1 * Meter) + (1 * Second)


@pytest.mark.parametrize(
    "a, b, c",
    [
        (1 * Meter, 2 * Foot, 0.39039999999999997 * Meter),
        (1 * Meter, 2 * Inch, 0.9492 * Meter),
        (2 * Meter / Second, 30 * Foot / Minute, 1.8476 * Meter / Second),
    ],
)
def test_subtraction_of_different_units(a: Quantity, b: Quantity, c: Quantity) -> None:
    assert a - b == c, str(a - b)


def test_subtraction_requires_same_dimension() -> None:
    with pytest.raises(conversions.ConversionNotFound):
        (1 * Meter) - (1 * Second)
