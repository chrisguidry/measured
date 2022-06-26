import pytest

from measured import Quantity, _measured_parser
from measured.iec import Byte, Kibi
from measured.si import Ampere, Hertz, Kilo, Meter, Micro, Ohm, Second


@pytest.mark.parametrize(
    "string",
    [
        "m",
        "5 zeebles",
    ],
)
def test_junk_that_should_not_parse(string: str) -> None:
    with pytest.raises((KeyError, _measured_parser.LarkError)):
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
def test_single_unit(string: str, quantity: Quantity) -> None:
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
def test_unit_with_exponent(string: str, quantity: Quantity) -> None:
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
def test_unit_series(string: str, quantity: Quantity) -> None:
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
def test_unit_ratio(string: str, quantity: Quantity) -> None:
    assert Quantity.parse(string) == quantity


@pytest.mark.parametrize(
    "string, quantity",
    [
        ("5 km", 5 * Kilo * Meter),
        ("5 KiB", 5 * Kibi * Byte),
        ("5 μm", 5 * Micro * Meter),
    ],
)
def test_unit_prefixes(string: str, quantity: Quantity) -> None:
    assert Quantity.parse(string) == quantity
