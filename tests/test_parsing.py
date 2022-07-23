from math import inf, nan

import pytest
from hypothesis import assume, example, given
from hypothesis.strategies import floats, integers

from measured import Numeric, Quantity, Unit, approximately, systems  # noqa: F401
from measured.hypothesis import units
from measured.iec import Byte, Kibi
from measured.parsing import ParseError
from measured.si import (
    Ampere,
    Gram,
    Hertz,
    Kilo,
    Kilogram,
    Liter,
    Mega,
    Meter,
    Micro,
    Ohm,
    Second,
)


def test_unit_symbols_should_not_have_spaces() -> None:
    with pytest.raises(ValueError, match="spaces"):
        Meter.alias(symbol="the metre")


@given(unit=units())
def test_each_unit_roundtrips(unit: Unit) -> None:
    assume(unit is not (Kilo * Gram))  # see test below
    assert Unit.parse(str(unit)) is unit


def test_kilogram_converts_to_kilogram() -> None:
    # This test is a special case for Kilo*Gram versus Kilogram, which measured will
    # always parse to Kilogram
    assert Unit.parse(str(Kilogram)) is Kilogram
    assert Unit.parse(str(Kilo * Gram)) is Kilogram


@given(
    magnitude=integers(min_value=-1000000000000, max_value=1000000000000),
    unit=units(),
)
@example(magnitude=1, unit=Liter)
@example(magnitude=1, unit=Mega * (Meter**-1))
def test_small_integer_quantities_parse_exactly(magnitude: Numeric, unit: Unit) -> None:
    assert Quantity.parse(str(magnitude * unit)) == magnitude * unit


@given(magnitude=integers(), unit=units())
@example(magnitude=1, unit=Liter)
def test_large_integer_quantities_are_parsable(magnitude: Numeric, unit: Unit) -> None:
    assert Quantity.parse(str(magnitude * unit)) == approximately(magnitude * unit)


@given(magnitude=floats(allow_infinity=False, allow_nan=False), unit=units())
@example(magnitude=1.0, unit=Liter)
def test_float_quantities_are_parsable(magnitude: Numeric, unit: Unit) -> None:
    assert Quantity.parse(str(magnitude * unit)) == magnitude * unit


@given(unit=units())
@pytest.mark.parametrize("magnitude", [nan, inf, -inf])
def test_unparsable_floats(magnitude: float, unit: Unit) -> None:
    with pytest.raises(ParseError):
        Quantity.parse(str(magnitude * unit))


@pytest.mark.parametrize(
    "string",
    [
        "fleebles",
        "queeble²",
        ",,,",
        "",
        " ",
    ],
)
def test_unit_that_should_not_parse(string: str) -> None:
    with pytest.raises((KeyError, ParseError)):
        Unit.parse(string)


@pytest.mark.parametrize(
    "string, unit",
    [
        ("m", Meter),
        ("meter", Meter),
        ("Hz", Hertz),
        ("hertz", Hertz),
        ("Ω", Ohm),
        ("ohm", Ohm),
    ],
)
def test_single_unit(string: str, unit: Unit) -> None:
    assert Unit.parse(string) is unit


@pytest.mark.parametrize(
    "string, unit",
    [
        ("m²", Meter**2),
        ("meter²", Meter**2),
        ("m²²²", Meter**222),
        ("m⁻¹", Meter**-1),
        ("m^2", Meter**2),
        ("m^222", Meter**222),
        ("m^-1", Meter**-1),
    ],
)
def test_unit_with_exponent(string: str, unit: Unit) -> None:
    assert Unit.parse(string) is unit


@pytest.mark.parametrize(
    "string, unit",
    [
        ("m²A³", Meter**2 * Ampere**3),
        ("m²⋅A³", Meter**2 * Ampere**3),
        ("m²*A³", Meter**2 * Ampere**3),
        ("m²A³s⁻³", Meter**2 * Ampere**3 * Second**-3),
        ("m²⋅A³⋅s^-3", Meter**2 * Ampere**3 * Second**-3),
        ("m²*A³*s^-3", Meter**2 * Ampere**3 * Second**-3),
    ],
)
def test_unit_series(string: str, unit: Unit) -> None:
    assert Unit.parse(string) is unit


@pytest.mark.parametrize(
    "string, unit",
    [
        ("m/s", Meter / Second),
        ("m²A³/s^3", (Meter**2 * Ampere**3) / Second**3),
        ("m²⋅A³/s^3", (Meter**2 * Ampere**3) / Second**3),
        ("m²*A³/s^3", (Meter**2 * Ampere**3) / Second**3),
    ],
)
def test_unit_ratio(string: str, unit: Unit) -> None:
    assert Unit.parse(string) == unit


@pytest.mark.parametrize(
    "string",
    [
        "m",
        "5 zeebles",
    ],
)
def test_quantities_that_should_not_parse(string: str) -> None:
    with pytest.raises((KeyError, ParseError)):
        Quantity.parse(string)


@pytest.mark.parametrize(
    "string, quantity",
    [
        ("5m", 5 * Meter),
        ("5 m", 5 * Meter),
        ("5.1 m", 5.1 * Meter),
        ("5 Hz", 5 * Hertz),
        ("5.1 Hz", 5.1 * Hertz),
        ("5 Ω", 5 * Ohm),
        ("5.1 Ω", 5.1 * Ohm),
    ],
)
def test_quantity_with_single_unit(string: str, quantity: Quantity) -> None:
    assert Quantity.parse(string) == quantity


@pytest.mark.parametrize(
    "string, quantity",
    [
        ("5 m²", 5 * Meter**2),
        ("5.1 m²", 5.1 * Meter**2),
        ("5 m²²²", 5 * Meter**222),
        ("5 m⁻¹", 5 * Meter**-1),
        ("5 m^2", 5 * Meter**2),
        ("5.1 m^2", 5.1 * Meter**2),
        ("5 m^222", 5 * Meter**222),
        ("5 m^-1", 5 * Meter**-1),
    ],
)
def test_quantity_with_unit_exponent(string: str, quantity: Quantity) -> None:
    assert Quantity.parse(string) == quantity


@pytest.mark.parametrize(
    "string, quantity",
    [
        ("5 m²A³", 5 * Meter**2 * Ampere**3),
        ("5 m²⋅A³", 5 * Meter**2 * Ampere**3),
        ("5 m²*A³", 5 * Meter**2 * Ampere**3),
        ("5 m²A³s⁻³", 5 * Meter**2 * Ampere**3 * Second**-3),
        ("5 m²⋅A³⋅s^-3", 5 * Meter**2 * Ampere**3 * Second**-3),
        ("5 m²*A³*s^-3", 5 * Meter**2 * Ampere**3 * Second**-3),
    ],
)
def test_quantity_with_unit_series(string: str, quantity: Quantity) -> None:
    assert Quantity.parse(string) == quantity


@pytest.mark.parametrize(
    "string, quantity",
    [
        ("5 m/s", 5 * Meter / Second),
        ("5 m²A³/s^3", 5 * (Meter**2 * Ampere**3) / Second**3),
        ("5 m²⋅A³/s^3", 5 * (Meter**2 * Ampere**3) / Second**3),
        ("5 m²*A³/s^3", 5 * (Meter**2 * Ampere**3) / Second**3),
    ],
)
def test_quantity_with_unit_ratio(string: str, quantity: Quantity) -> None:
    assert Quantity.parse(string) == quantity


@pytest.mark.parametrize(
    "string, quantity",
    [
        ("5 km", 5 * Kilo * Meter),
        ("5 KiB", 5 * Kibi * Byte),
        ("5 μm", 5 * Micro * Meter),
    ],
)
def test_quantity_with_unit_prefixes(string: str, quantity: Quantity) -> None:
    assert Quantity.parse(string) == quantity
