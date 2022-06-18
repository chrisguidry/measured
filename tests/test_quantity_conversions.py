import pytest

from measured import Length, Unit, conversions
from measured.si import Meter, Second
from measured.us import Acre, Foot, Inch


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


def test_conversion_with_exponents() -> None:
    assert (1 * Foot) ** 2 == (12 * Inch) ** 2
    assert 1 * Foot**2 == 144 * Inch**2

    assert (1 * Foot) ** 3 == (12 * Inch) ** 3
    assert 1 * Foot**3 == 1728 * Inch**3


def test_conversion_can_navigate_exponents() -> None:
    assert conversions.find(Foot, Inch) == [(12.0, Inch)]
    assert conversions.find(Foot**2, Inch**2) == [(144.0, Inch**2)]
    assert conversions.find(Acre, Foot**2) == [(43560.0, Foot**2)]
    assert conversions.find(Acre, Inch**2) == [
        (43560.0, Foot**2),
        (144.0, Inch**2),
    ]
