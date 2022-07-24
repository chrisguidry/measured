from functools import wraps
from typing import TYPE_CHECKING, Callable, TypeVar, Union

if TYPE_CHECKING:  # pragma: no cover
    from IPython.lib.pretty import RepresentationPrinter

    from measured import Dimension, Measurement, Prefix, Quantity, Unit

SUPERSCRIPTS = {
    "-": "⁻",
    ".": ".",  # There does not seem to be a superscript '.' in Unicode yet
    **{
        str(i): v
        for i, v in enumerate(["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"])
    },
}
DIGITS = {v: k for k, v in SUPERSCRIPTS.items()}


def superscript(exponent: Union[int, float]) -> str:
    """Given a signed integer exponent, returns the Unicode superscript string for it

    Examples:

        >>> f"x{superscript(123)}"
        'x¹²³'
        >>> f"x{superscript(0)}"
        'x⁰'
        >>> f"x{superscript(-1)}"
        'x⁻¹'
        >>> f"x{superscript(1)}"
        'x'
    """
    if exponent == 1:
        return ""

    return "".join(SUPERSCRIPTS[c] for c in str(exponent))


def from_superscript(string: str) -> int:
    """Given a Unicode superscript string, return it as an integer."""
    return int("".join(DIGITS[c] for c in string))


M = TypeVar("M")


def mathml(function: Callable[[M], str]) -> Callable[[M], str]:
    """Wraps the given MathML-producing function to produce a self-contained
    MathML tag.  This allows for composable MathML functions that can produce both
    expressions and root MathML tag."""

    @wraps(function)
    def inner(measured_object: M) -> str:
        return f"<math>{function(measured_object)}</math>"

    return inner


def dimension_repr(dimension: "Dimension") -> str:
    """Formats the given Dimension as a Python `repr`"""
    return (
        "Dimension("
        f"exponents={dimension.exponents!r}, "
        f"name={dimension.name!r}, symbol={dimension.symbol!r}"
        ")"
    )


def dimension_str(dimension: "Dimension") -> str:
    """Formats the given Dimension as a plaintext string"""
    if dimension.symbol:
        return dimension.symbol

    return (
        "⋅".join(
            f"{fundamental.symbol}{superscript(dimension.exponents[i])}"
            for i, fundamental in enumerate(dimension._fundamental)
            if dimension.exponents[i] != 0
        )
        or "?"
    )


def dimension_pretty(
    dimension: "Dimension", pretty: "RepresentationPrinter", cycle: bool
) -> None:
    """Formats the given Dimension to the provided pretty printer"""
    with pretty.group():
        pretty.text(str(dimension))
        with pretty.group(indent=2):
            pretty.break_()
            if dimension.name:
                pretty.text(dimension.name)
                pretty.break_()
            pretty.text(repr(dimension))


def dimension_mathml(dimension: "Dimension") -> str:
    """Formats the given Dimension as a MathML expression"""
    numerator, denominator = dimension.as_ratio()

    n = (
        "<mo>⋅</mo>".join(
            (
                "<msup>"
                f"<mi>{dimension.symbol}</mi>"
                "<mn>"
                f"{numerator.exponents[i] if numerator.exponents[i] != 1 else ''}"
                "</mn>"
                "</msup>"
            )
            for i, dimension in enumerate(dimension._fundamental)
            if numerator.exponents[i] != 0
        )
        or "<mi>1</mi>"
    )

    d = "<mo>⋅</mo>".join(
        (
            "<msup>"
            f"<mi>{dimension.symbol}</mi>"
            "<mn>"
            f"{denominator.exponents[i] if denominator.exponents[i] != 1 else ''}"
            "</mn>"
            "</msup>"
        )
        for i, dimension in enumerate(dimension._fundamental)
        if denominator.exponents[i] != 0
    )

    if n and not d:
        return f"<mrow>{n}</mrow>"

    return f"<mfrac><mrow>{n}</mrow><mrow>{d}</mrow></mfrac>"


def prefix_repr(prefix: "Prefix") -> str:
    """Formats the given Prefix as a Python `repr`"""
    return f"Prefix(base={prefix.base!r}, exponent={prefix.exponent!r})"


def prefix_str(prefix: "Prefix") -> str:
    """Formats the given Prefix as a plaintext string"""
    if prefix.symbol:
        return prefix.symbol
    if prefix.exponent == 0:
        return ""
    return f"{prefix.base}{superscript(prefix.exponent)}"


def prefix_pretty(
    prefix: "Prefix", pretty: "RepresentationPrinter", cycle: bool
) -> None:
    """Formats the given Prefix to the provided pretty printer"""
    with pretty.group():
        pretty.text(str(prefix))
        with pretty.group(indent=2):
            pretty.break_()
            pretty.text(f"{prefix.base}{superscript(prefix.exponent)}")
            pretty.break_()
            pretty.text(repr(prefix))


def prefix_mathml(prefix: "Prefix") -> str:
    """Formats the given Prefix as a MathML expression"""
    if prefix.symbol:
        return f"<mi>{prefix.symbol}</mi>"

    if prefix.exponent == 0:
        return ""

    return f"<msup><mn>{prefix.base}</mn><mn>{prefix.exponent}</mn></msup>"


def unit_repr(unit: "Unit") -> str:
    """Formats the given Unit as a Python `repr`"""
    if unit.name:
        return f"Unit.named({unit.name!r})"

    return (
        "Unit("
        f"prefix={unit.prefix!r}, "
        f"factors={unit.factors!r}, "
        f"dimension={unit.dimension!r}, "
        f"name={unit.name!r}, symbol={unit.symbol!r}"
        ")"
    )


def unit_str(unit: "Unit") -> str:
    """Formats the given Unit as a plaintext string"""
    if unit.symbol:
        return unit.symbol

    # In order to handle cases like `Mega * (Meter**-1)`, which naively becomes
    # "Mm⁻¹", which looks like it should parse to `(Mega*Meter)**-1`, take this
    # unit's prefix and push it down as the prefix of the first factor, which would
    # turn `Mega * (Meter**-1)` into the correct `(Micro*Meter)**-1`.
    #
    # While it seems odd to have this in `str`, it's just a side-effect of the
    # string represeentations not having parentheses.
    first, *rest = [
        (factor.prefix, factor.symbol, exponent)
        for factor, exponent in unit.factors.items()
    ]
    prefix, symbol, exponent = first
    sign = 1 if exponent >= 0 else -1
    first = ((unit.prefix * prefix) ** sign, symbol, exponent)

    return "⋅".join(
        f"{prefix}{symbol}{superscript(exponent)}"
        for prefix, symbol, exponent in [first, *rest]
    )


def unit_format(unit: "Unit", format_specifier: str) -> str:
    """Formats the given Unit as a plaintext string, using the provided format
    specifier to control the output"""
    from measured import One

    if not format_specifier:
        return unit_str(unit)

    if format_specifier == "/":
        numerator, denominator = unit.as_ratio()
        if denominator == One:
            return unit_str(unit)
        return str(numerator) + "/" + str(denominator)

    raise ValueError(f"Unrecognized format specifier {format_specifier!r}")


def unit_pretty(unit: "Unit", pretty: "RepresentationPrinter", cycle: bool) -> None:
    """Formats the given Unit to the provided pretty printer"""
    with pretty.group():
        if unit.symbol:
            pretty.text(f"{unit.symbol} ({unit:/})")
        else:
            pretty.text(f"{unit:/}")

        with pretty.group(indent=2):
            pretty.break_()
            if unit.name:
                pretty.text(unit.name)
                pretty.break_()
            pretty.pretty(unit.dimension)
            pretty.break_()
            pretty.text(repr(unit))


def unit_mathml(unit: "Unit") -> str:
    """Formats the given Unit as a MathML expression"""
    if unit.symbol:
        return f"<mi>{unit.symbol}</mi>"

    # In order to handle cases like `Mega * (Meter**-1)`, which naively becomes
    # "Mm⁻¹", which looks like it should parse to `(Mega*Meter)**-1`, take this
    # unit's prefix and push it down as the prefix of the first factor, which would
    # turn `Mega * (Meter**-1)` into the correct `(Micro*Meter)**-1`.
    #
    # While it seems odd to have this in `str`, it's just a side-effect of the
    # string represeentations not having parentheses.
    first, *rest = [
        (unit.prefix, unit.symbol, exponent) for unit, exponent in unit.factors.items()
    ]
    prefix, symbol, exponent = first
    sign = 1 if exponent >= 0 else -1
    first = ((unit.prefix * prefix) ** sign, symbol, exponent)

    numerator = [(p, s, e) for p, s, e in [first, *rest] if e >= 0]
    denominator = [(p, s, e * -1) for p, s, e in [first, *rest] if e < 0]

    n = (
        "<mo>⋅</mo>".join(
            (
                "<msup>"
                f"<mrow>{prefix_mathml(prefix)}<mi>{symbol}</mi></mrow>"
                "<mn>"
                f"{exponent if exponent != 1 else ''}"
                "</mn>"
                "</msup>"
            )
            for prefix, symbol, exponent in numerator
        )
        or "<mi>1</mi>"
    )

    d = "<mo>⋅</mo>".join(
        (
            "<msup>"
            f"<mrow>{prefix_mathml(prefix)}<mi>{symbol}</mi></mrow>"
            "<mn>"
            f"{exponent if exponent != 1 else ''}"
            "</mn>"
            "</msup>"
        )
        for prefix, symbol, exponent in denominator
    )

    if n and not d:
        return f"<mrow>{n}</mrow>"

    return f"<mfrac><mrow>{n}</mrow><mrow>{d}</mrow></mfrac>"


def quantity_repr(quantity: "Quantity") -> str:
    """Formats the given Quantity as a Python `repr`"""
    return f"Quantity(magnitude={quantity.magnitude!r}, unit={quantity.unit!r})"


def quantity_str(quantity: "Quantity") -> str:
    """Formats the given Quantity as a plaintext string"""
    return f"{quantity.magnitude} {quantity.unit}"


def quantity_format(quantity: "Quantity", format_specifier: str) -> str:
    """Formats the given Quantity as a plaintext string, using the provided format
    specifier to control the output"""
    magnitude_format, _, unit_format = format_specifier.partition(":")
    magnitude = quantity.magnitude.__format__(magnitude_format)
    unit = quantity.unit.__format__(unit_format)
    return f"{magnitude} {unit}"


def quantity_pretty(
    quantity: "Quantity", pretty: "RepresentationPrinter", cycle: bool
) -> None:
    """Formats the given Quantity to the provided pretty printer"""
    with pretty.group():
        pretty.text(f"{quantity::/}")
        with pretty.group(indent=2):
            pretty.break_()
            pretty.pretty(quantity.magnitude)
            pretty.break_()
            pretty.pretty(quantity.unit)
            pretty.break_()
            pretty.text(repr(quantity))


def quantity_mathml(quantity: "Quantity") -> str:
    """Formats the given Quantity as a MathML expression"""
    return (
        "<mrow>"
        f"<mn>{quantity.magnitude}</mn>"
        "<mo></mo>"
        f"{unit_mathml(quantity.unit)}"
        "</mrow>"
    )


def measurement_repr(measurement: "Measurement") -> str:
    """Formats the given Measurement as a Python `repr`"""
    return (
        f"Measurement("
        f"measurand={measurement.measurand!r}, "
        f"uncertainty={measurement.uncertainty.magnitude!r}"
        ")"
    )


def measurement_str(measurement: "Measurement") -> str:
    """Formats the given Measurement as a plaintext string"""
    return measurement_format(measurement, "")


def measurement_format(measurement: "Measurement", format_specifier: str) -> str:
    """Formats the given Measurement as a plaintext string, using the provided format
    specifier to control the output"""
    uncertainty_format, _, quantity_format = format_specifier.partition(":")

    style, magnitude_format = "", ""
    if uncertainty_format:
        style, magnitude_format = uncertainty_format[0], uncertainty_format[1:]

    if style in ("", "+", "±"):
        magnitude = measurement.uncertainty.magnitude.__format__(magnitude_format)
        uncertainty = f"±{magnitude}"
    elif style == "%":
        magnitude_format = magnitude_format or ".2f"
        percent = measurement.uncertainty_percent.__format__(magnitude_format)
        uncertainty = f"±{percent}%"
    else:
        raise ValueError(f"Unrecognized uncertainty style {style!r}")

    magnitude_format, _, unit_format = quantity_format.partition(":")
    magnitude = measurement.measurand.magnitude.__format__(magnitude_format)
    unit = measurement.measurand.unit.__format__(unit_format)
    return f"{magnitude}{uncertainty} {unit}"


def measurement_pretty(
    measurement: "Measurement", pretty: "RepresentationPrinter", cycle: bool
) -> None:
    """Formats the given Measurement to the provided pretty printer"""
    with pretty.group():
        pretty.text(f"{measurement:::/}")
        with pretty.group(indent=2):
            pretty.break_()
            pretty.pretty(measurement.measurand.magnitude)
            pretty.text(" ±")
            pretty.pretty(measurement.uncertainty.magnitude)
            pretty.break_()
            pretty.pretty(measurement.measurand.unit)
            pretty.break_()
            pretty.text(repr(measurement))


def measurement_mathml(measurement: "Measurement") -> str:
    """Formats the given Measurement as a MathML expression"""
    return (
        "<mrow>"
        f"<mn>{measurement.measurand.magnitude}</mn>"
        "<mo>±</mo>"
        f"<mn>{measurement.uncertainty.magnitude}</mn>"
        "<mo></mo>"
        f"{unit_mathml(measurement.measurand.unit)}"
        "</mrow>"
    )
