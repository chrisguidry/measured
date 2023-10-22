from io import StringIO
from reprlib import Repr

import pytest

pytest.importorskip("IPython")

# flake8: noqa: E402 (imports not at top of file)

from typing import Union
from xml.etree import ElementTree

from IPython.lib.pretty import RepresentationPrinter

from measured import systems  # noqa: F401
from measured import (
    Area,
    Decibel,
    Dimension,
    Frequency,
    Length,
    Logarithm,
    Measurement,
    Neper,
    Number,
    Prefix,
    Quantity,
    Time,
    Unit,
    Volume,
    VolumetricFlow,
)
from measured.electronics import dBW
from measured.formatting import superscript
from measured.si import Hertz, Kilo, Mega, Meter, Milli, Ohm, Second, Watt


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
def test_superscripts(exponent: int, superscripted: str) -> None:
    assert superscript(exponent) == superscripted


def test_formatting_prefixes_simplifies() -> None:
    # This is a little surprising, but what's happening here is that
    # 5 meter per kilosecond is getting reduced to 5 millimeter per second
    assert str((5 * Meter) / (Kilo * Second)) == "5 mm⋅s⁻¹"


def test_do_the_best_we_can_with_odd_prefixes() -> None:
    kilo_plus_one = Prefix(10, 4)
    assert str(5 * (kilo_plus_one * Meter)) == "5 10⁴m"


@pytest.mark.parametrize(
    "dimension, string",
    [
        (Number, "1"),
        (Length, "L"),
        (Area, "L²"),
        (Volume, "L³"),
        (Frequency, "T⁻¹"),
    ],
)
def test_strings_of_dimensions(dimension: Dimension, string: str) -> None:
    assert str(dimension) == string


@pytest.mark.parametrize(
    "unit, string",
    [
        (Meter, "m"),
        (Meter**2, "m²"),
        (Meter**3, "m³"),
        ((Kilo * Meter) ** 2, "km²"),
        (Kilo * Meter**2, "1000 m²"),
        (Meter**3 / Second**2, "m³⋅s⁻²"),
        (Hertz, "Hz"),
        (Hertz**2, "s⁻²"),
        (Decibel[1 * Meter], "dB of 1 m"),
        (Logarithm(3), "1 log3(x/x₀)"),
    ],
)
def test_strings_of_units(unit: Unit, string: str) -> None:
    assert str(unit) == string


@pytest.mark.parametrize(
    "quantity, string",
    [
        (5 * Meter, "5 m"),
        (5.1 * Meter**2, "5.1 m²"),
        (5 * (Kilo * Meter), "5 km"),
        (5.1 * (Kilo * Meter) ** 2, "5.1 km²"),
        (5.1 * (Kilo * (Meter**2)), "5100.0 m²"),
        (5.1 * (Kilo * (Meter**2) / Second), "5100.0 m²⋅s⁻¹"),
        (5.1 * (Kilo * Meter**2) / Second, "5100.0 m²⋅s⁻¹"),
        (5.1 * (Kilo * Meter) ** 2 / Second, "5.1 km²⋅s⁻¹"),
        (5.1 * (Mega * Meter**-1), "5.1 μm⁻¹"),
        (5.1 * ((Mega * Meter) ** -1), "5.1 Mm⁻¹"),
    ],
)
def test_strings_of_quantities(quantity: Quantity, string: str) -> None:
    assert str(quantity) == string


@pytest.mark.parametrize(
    "quantity, template, string",
    [
        (5 * Meter, "{quantity}", "5 m"),
        (5.123 * Meter, "{quantity:.2f:/}", "5.12 m"),
        (5.123 * Meter / Second, "{quantity:.2f}", "5.12 m⋅s⁻¹"),
        (5.123 * Meter / Second, "{quantity:.2f:}", "5.12 m⋅s⁻¹"),
        (5.123 * Meter / Second, "{quantity:.2f:/}", "5.12 m/s"),
        (5 * Ohm, "{quantity}", "5 Ω"),
        (5 * Ohm, "{quantity::/}", "5 m²⋅kg/s⋅C²"),
        (5 * Milli * Ohm, "{quantity::/}", "0.005 m²⋅kg/s⋅C²"),
    ],
)
def test_format_specifiers(quantity: Quantity, template: str, string: str) -> None:
    assert template.format(quantity=quantity) == string


def test_unrecognized_unit_format_specifier() -> None:
    with pytest.raises(ValueError):
        "{quantity::nope}".format(quantity=5 * Meter)


Formattable = Union[Dimension, Prefix, Unit, Quantity, Measurement]


@pytest.fixture
def pretty() -> RepresentationPrinter:
    return RepresentationPrinter(output=StringIO())


@pytest.mark.parametrize(
    "formattable",
    [
        Length,
        Area,
        VolumetricFlow,
        Kilo,
        Prefix(10, 4),
        Meter,
        Kilo * Meter,
        Prefix(10, 4) * Meter,
        Ohm,
        5 * Meter,
        Measurement(5 * Meter, 0.1),
        Decibel,
        Neper,
        Decibel[1 * Watt],
        30 * Decibel[1 * Watt],
    ],
)
def test_pretty_repr_includes_string_and_repr_of_self(
    formattable: Formattable, pretty: RepresentationPrinter
) -> None:
    formattable._repr_pretty_(pretty, False)
    assert str(formattable) in pretty.output.getvalue()
    assert repr(formattable) in pretty.output.getvalue()


@pytest.mark.parametrize(
    "formattable, specifier",
    [
        (Kilo * Meter / Second, "/"),
        (5 * Meter / Second, ":/"),
        (Measurement(5 * Meter / Second, 0.1), "::/"),
    ],
)
def test_pretty_repr_includes_string_of_self(
    formattable: Formattable, specifier: str, pretty: RepresentationPrinter
) -> None:
    formattable._repr_pretty_(pretty, False)
    assert formattable.__format__(specifier) in pretty.output.getvalue()


@pytest.mark.parametrize(
    "formattable",
    [
        Length,
        Area,
        VolumetricFlow,
        Kilo,
        Prefix(10, 4),
        Meter,
        Kilo * Meter,
        Prefix(10, 4) * Meter,
        Ohm,
        Kilo * Meter / Second,
        5 * Meter,
        5 * Meter / Second,
        Measurement(5 * Meter, 0.1),
        Measurement(5 * Meter / Second, 0.1),
        Neper,
        Decibel[1 * Watt],
        30 * Decibel[1 * Watt],
        (Kilo * Meter) ** 2,
        (Kilo * (Meter**2)),
        (5.1 * (Kilo * Meter) ** 2),
        (5.1 * (Kilo * (Meter**2))),
        (5.1 * (Kilo * (Meter**2) / Second)),
        (5.1 * (Kilo * Meter**2) / Second),
        (5.1 * (Kilo * Meter) ** 2 / Second),
        (5.1 * (Mega * Meter**-1)),
        (5.1 * ((Mega * Meter) ** -1)),
    ],
)
def test_html_is_mathml(formattable: Formattable) -> None:
    math = ElementTree.fromstring(formattable._repr_html_())
    assert math.tag == "math"


@pytest.mark.parametrize(
    "formattable",
    [
        Length / Time,
        Meter / Second,
    ],
)
def test_mathml_root_is_fraction(formattable: Formattable) -> None:
    math = ElementTree.fromstring(formattable._repr_html_())
    assert math[0].tag == "mfrac"


@pytest.mark.parametrize(
    "formattable",
    [
        Kilo,
        Meter,
        Hertz,
        Neper,
        dBW,
        Decibel[1 * Watt],
    ],
)
def test_mathml_root_is_identifier(formattable: Formattable) -> None:
    math = ElementTree.fromstring(formattable._repr_html_())
    assert math[0].tag == "mi"


@pytest.mark.parametrize(
    "formattable",
    [
        Length,
        Length * Time,
        (Kilo * Meter),
        Meter * Second,
        Logarithm(3),
        Decibel[1 * Meter],  # a dB that we wouldn't have a symbol for
        Neper[1 * Meter],
        30 * Decibel[1 * Watt],
        (5.1 * (Kilo * Meter) ** 2),
        (5.1 * (Kilo * (Meter**2))),
        (5.1 * (Kilo * (Meter**2) / Second)),
        (5.1 * (Kilo * Meter**2) / Second),
        (5.1 * (Kilo * Meter) ** 2 / Second),
        (5.1 * (Mega * Meter**-1)),
        (5.1 * ((Mega * Meter) ** -1)),
    ],
)
def test_mathml_root_is_subexpression(formattable: Formattable) -> None:
    math = ElementTree.fromstring(formattable._repr_html_())
    assert math[0].tag == "mrow"
