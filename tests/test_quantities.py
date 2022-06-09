from typing import Any

import pytest

from measured import Numeric, One
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
