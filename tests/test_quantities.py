from typing import Any

import pytest

from measured import Length, Numeric, One, Unit
from measured.si import Meter, Second


@pytest.mark.parametrize("value", [-2, 5, 0.1, -0.3, 2.5])
def test_constructing_quantities_by_multiplying_units(value: Numeric):
    assert Meter * value == value * Meter
    assert value * Meter * Meter == value * Meter**2
    assert value * Meter / Second == value * (Meter / Second)


def test_equality_only_with_quantities():
    assert 5 * One != 5
    assert 5 * Meter != 5
    assert 5 * Meter != Meter


def test_equality_only_in_same_dimension():
    assert 5 * Meter != 5 * Second


@pytest.mark.parametrize("value", ["nope", b"nah"])
def test_multiplication_only_with_number_types(value: Any):
    with pytest.raises(TypeError):
        Meter * value

    with pytest.raises(TypeError):
        value * Meter


@pytest.mark.parametrize("value", ["nope", b"nah"])
def test_division_only_with_number_types(value: Any):
    with pytest.raises(TypeError):
        Meter / value

    with pytest.raises(TypeError):
        value / Meter


def test_repr():
    assert repr(5 * Meter) == f"<Quantity(magnitude=5, unit={Meter!r})>"


def test_negative():
    assert -(5 * Meter) == -5 * Meter


def test_positive():
    assert +(5 * Meter) == +5 * Meter


def test_absolute_value():
    assert abs(-5 * Meter) == 5 * Meter


def test_ordering():
    assert (-5 * Meter) < (1 * Meter)
    assert (1 * Meter) > (-5 * Meter)
    assert (1 * Meter) >= (1 * Meter)
    assert (1 * Meter) <= (1 * Meter)


def test_ordering_only_with_quantities():
    with pytest.raises(TypeError):
        1 * Meter <= 1


def test_ordering_only_within_dimension():
    with pytest.raises(TypeError):
        1 * Meter < 1 * Second

    with pytest.raises(TypeError):
        1 * Meter <= 1 * Second

    with pytest.raises(TypeError):
        1 * Meter > 1 * Second

    with pytest.raises(TypeError):
        1 * Meter >= 1 * Second


def test_ordering_requires_compatible_types():
    Bogus = Unit.define(Length, name="bogus", symbol="bog")

    one = 1 * Meter
    other = 1 * Bogus

    with pytest.raises(TypeError):
        one < other

    with pytest.raises(TypeError):
        one <= other

    with pytest.raises(TypeError):
        one > other

    with pytest.raises(TypeError):
        one >= other


def test_sorting():
    unsorted = [1 * Meter, 0 * Meter, 5 * Meter]
    assert sorted(unsorted) == [0 * Meter, 1 * Meter, 5 * Meter]


def test_approximating():
    assert (1 * Meter).approximates(1.0 * Meter)
    assert (1 * Meter).approximates(1 * Meter)
    assert (1.0 * Meter).approximates(1.0 * Meter)
    assert (1 * Meter).approximates(1.0000000001 * Meter)
    assert not (1 * Meter).approximates(1.01 * Meter)
    assert not (1 * Meter).approximates(1.0 * Second)


def test_approximating_requires_units_with_conversion():
    Bogus = Unit.define(Length, name="bogus", symbol="bog")

    one = 1 * Meter
    other = 1 * Bogus

    assert not one.approximates(other, within=1e100)
