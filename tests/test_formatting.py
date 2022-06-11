import pytest

from measured import Area, Frequency, Length, Number, Prefix, Volume
from measured.formatting import superscript
from measured.si import Hertz, Kilo, Meter, Second


@pytest.mark.parametrize(
    "exponent, superscripted",
    [
        (-1234567890, "⁻¹²³⁴⁵⁶⁷⁸⁹⁰"),
        (-123.456, "⁻¹²³.⁴⁵⁶"),
        (-123, "⁻¹²³"),
        (-23, "⁻²³"),
        (-3, "⁻³"),
        (-1.1, "⁻¹.¹"),
        (-1.0, "⁻¹.⁰"),
        (-1, "⁻¹"),
        (-0.9, "⁻⁰.⁹"),
        (0, "⁰"),
        (1, ""),
        (0.9, "⁰.⁹"),
        (1.0, ""),
        (1.1, "¹.¹"),
        (2, "²"),
        (23, "²³"),
        (345, "³⁴⁵"),
        (123.456, "¹²³.⁴⁵⁶"),
        (1234567890, "¹²³⁴⁵⁶⁷⁸⁹⁰"),
    ],
)
def test_superscripts(exponent: int, superscripted: str):
    assert superscript(exponent) == superscripted


def test_formatting_dimensions():
    assert str(Number) == "1"
    assert str(Length) == "L"
    assert str(Area) == "L²"
    assert str(Volume) == "L³"
    assert str(Frequency) == "T⁻¹"


def test_formatting_units():
    assert str(Meter) == "m"
    assert str(Meter**2) == "m²"
    assert str(Meter**3) == "m³"
    assert str(Meter**3 / Second**2) == "m³s⁻²"
    assert str(Hertz) == "Hz"
    assert str(Hertz**2) == "s⁻²"


def test_formatting_quantities():
    assert str(5 * Meter) == "5 m"
    assert str(5.1 * Meter**2) == "5.1 m²"


def test_formatting_prefixes():
    assert str(5 * (Kilo * Meter)) == "5 km"
    assert str(5.1 * (Kilo * Meter**2) / Second) == "5.1 km²s⁻¹"


def test_formatting_prefixes_simplifies():
    # This is a little surprising, but what's happening here is that
    # 5 meter per kilosecond is getting reduced to 5 millimeter per second
    assert str((5 * Meter) / (Kilo * Second)) == "5 mms⁻¹"


def test_do_the_best_we_can_with_odd_prefixes():
    kilo_plus_one = Prefix(10, 4)
    assert str(5 * (kilo_plus_one * Meter)) == "5 10⁴m"
