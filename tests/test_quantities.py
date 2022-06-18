from typing import Any

import pytest

from measured import Length, Numeric, One, Unit
from measured.si import Meter, Second


@pytest.mark.parametrize("value", [-2, 5, 0.1, -0.3, 2.5])
def test_constructing_quantities_by_multiplying_units(value: Numeric) -> None:
    assert Meter * value == value * Meter
    assert value * Meter * Meter == value * Meter**2
    assert value * Meter / Second == value * (Meter / Second)


@pytest.mark.parametrize("value", ["nope", b"nah"])
def test_construction_by_multiplication_only_with_number_types(value: Any) -> None:
    with pytest.raises(TypeError):
        Meter * value

    with pytest.raises(TypeError):
        value * Meter


@pytest.mark.parametrize("value", ["nope", b"nah"])
def test_construction_by_division_only_with_number_types(value: Any) -> None:
    with pytest.raises(TypeError):
        Meter / value

    with pytest.raises(TypeError):
        value / Meter


def test_equality_only_with_quantities() -> None:
    assert 5 * One != 5
    assert 5 * Meter != 5
    assert 5 * Meter != Meter


def test_equality_only_in_same_dimension() -> None:
    assert 5 * Meter != 5 * Second


def test_addition_only_with_quantities() -> None:
    with pytest.raises(TypeError):
        (5 * Meter) + 10  # type: ignore

    with pytest.raises(TypeError):
        10 + (5 * Meter)  # type: ignore


def test_subtraction_only_with_quantities() -> None:
    with pytest.raises(TypeError):
        (5 * Meter) - 10  # type: ignore

    with pytest.raises(TypeError):
        10 - (5 * Meter)  # type: ignore


def test_multiplication_by_scalar() -> None:
    assert 10 * (5 * Meter) == 50 * Meter


def test_division_by_scalar() -> None:
    assert (500 * Meter) / 10 == 50 * Meter


def test_exponentation_by_scalar() -> None:
    assert (5 * Meter) ** 2 == 25 * Meter**2


def test_cannot_multiply_by_random_types() -> None:
    with pytest.raises(TypeError):
        "hi" * (5 * Meter)  # type: ignore

    with pytest.raises(TypeError):
        (5 * Meter) * "hi"  # type: ignore


def test_cannot_divide_by_random_types() -> None:
    with pytest.raises(TypeError):
        (5 * Meter) / "hi"  # type: ignore


def test_repr() -> None:
    assert repr(5 * Meter) == f"<Quantity(magnitude=5, unit={Meter!r})>"


def test_negative() -> None:
    assert -(5 * Meter) == -5 * Meter


def test_positive() -> None:
    assert +(5 * Meter) == +5 * Meter


def test_absolute_value() -> None:
    assert abs(-5 * Meter) == 5 * Meter


def test_ordering() -> None:
    assert (-5 * Meter) < (1 * Meter)
    assert (1 * Meter) > (-5 * Meter)
    assert (1 * Meter) >= (1 * Meter)
    assert (1 * Meter) <= (1 * Meter)


def test_ordering_only_with_quantities() -> None:
    with pytest.raises(TypeError):
        1 * Meter <= 1


def test_ordering_only_within_dimension() -> None:
    with pytest.raises(TypeError):
        1 * Meter < 1 * Second

    with pytest.raises(TypeError):
        1 * Meter <= 1 * Second

    with pytest.raises(TypeError):
        1 * Meter > 1 * Second

    with pytest.raises(TypeError):
        1 * Meter >= 1 * Second


def test_ordering_requires_types_with_a_conversion() -> None:
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


def test_ordering_requires_types_in_the_same_dimension() -> None:
    one = 1 * Meter
    other = 1 * Second

    with pytest.raises(TypeError):
        one < other

    with pytest.raises(TypeError):
        one <= other

    with pytest.raises(TypeError):
        one > other

    with pytest.raises(TypeError):
        one >= other


def test_sorting() -> None:
    unsorted = [1 * Meter, 0 * Meter, 5 * Meter]
    assert sorted(unsorted) == [0 * Meter, 1 * Meter, 5 * Meter]


def test_approximating() -> None:
    assert (1 * Meter).approximates(1.0 * Meter)
    assert (1 * Meter).approximates(1 * Meter)
    assert (1.0 * Meter).approximates(1.0 * Meter)
    assert (1 * Meter).approximates(1.0000000001 * Meter)
    assert not (1 * Meter).approximates(1.01 * Meter)
    assert not (1 * Meter).approximates(1.0 * Second)


def test_approximating_requires_units_with_conversion() -> None:
    Bogus = Unit.define(Length, name="bogus", symbol="bog")

    one = 1 * Meter
    other = 1 * Bogus

    assert not one.approximates(other, within=1e100)


def test_unit_conversion_must_be_in_same_dimension() -> None:
    with pytest.raises(TypeError):
        (1 * Meter).in_unit(Second)


def test_unit_always_converts_to_itself() -> None:
    converted = (10 * Meter).in_unit(Meter)
    assert converted.magnitude == 10
    assert converted.unit == Meter
