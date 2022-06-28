import pytest

from measured import Numeric, ParseError, Quantity, Unit, systems  # noqa: F401
from measured.iec import Byte, Kibi
from measured.si import Ampere, Hertz, Kilo, Meter, Micro, Ohm, Second

ALL_UNITS = sorted(Unit.base(), key=lambda u: u.name or "")


def test_unit_symbols_should_not_have_spaces() -> None:
    with pytest.raises(ValueError, match="spaces"):
        Meter.alias(symbol="the metre")


@pytest.mark.parametrize("unit", ALL_UNITS, ids=[u.name for u in ALL_UNITS])
def test_each_unit_parsable(unit: Unit) -> None:
    assert Unit.parse(str(unit)) is unit


@pytest.mark.parametrize("magnitude", [-1e-30 - 1.1, -1, 0, 1, 1.1, 1e30])
@pytest.mark.parametrize("unit", ALL_UNITS, ids=[u.name for u in ALL_UNITS])
def test_int_quantity_in_each_unit_parsable(magnitude: Numeric, unit: Unit) -> None:
    assert Quantity.parse(str(magnitude * unit)) == magnitude * unit


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
