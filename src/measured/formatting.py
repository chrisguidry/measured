import math
from functools import wraps
from typing import TYPE_CHECKING, Callable, Optional, Sequence, Tuple, TypeVar

from typing_extensions import TypeAlias

if TYPE_CHECKING:  # pragma: no cover
    from IPython.lib.pretty import RepresentationPrinter

    from measured import (
        Dimension,
        Level,
        Logarithm,
        LogarithmicUnit,
        Measurement,
        Numeric,
        Prefix,
        Quantity,
        Unit,
    )

SUPERSCRIPTS = {
    "-": "⁻",
    ".": ".",  # There does not seem to be a superscript '.' in Unicode yet
    **{
        str(i): v
        for i, v in enumerate(["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"])
    },
}
DIGITS = {v: k for k, v in SUPERSCRIPTS.items()}


def superscript(exponent: "Numeric") -> str:
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


UnitTerm: TypeAlias = Tuple["Prefix", Optional[str], int]


def _unit_to_magnitude_and_terms(
    unit: "Unit",
) -> Tuple["Numeric", Sequence[UnitTerm]]:
    from measured import FractionalDimensionError

    # In order to handle cases like `Mega * (Meter**-1)`, which naively becomes
    # "Mm⁻¹", which looks like it should parse to `(Mega*Meter)**-1`, take this
    # unit's prefix and push it down as the prefix of the first factor, which would
    # turn `Mega * (Meter**-1)` into the correct `(Micro*Meter)**-1`.
    #
    # While it seems odd to have this in `str`, it's just a side-effect of the
    # string representations not having parentheses.
    first, *rest = [
        (factor.prefix, factor.symbol, exponent)
        for factor, exponent in unit.factors.items()
    ]

    magnitude: Numeric = 1
    prefix, symbol, exponent = first
    prefix = unit.prefix * prefix
    try:
        prefix = prefix.root(exponent)
        first = (prefix, symbol, exponent)
    except FractionalDimensionError:
        magnitude = prefix.quantify()

    return magnitude, [first, *rest]


def unit_str(unit: "Unit") -> str:
    """Formats the given Unit as a plaintext string"""
    if unit.symbol:
        return unit.symbol

    magnitude, terms = _unit_to_magnitude_and_terms(unit)
    return (str(magnitude) + " " if magnitude != 1 else "") + (
        "⋅".join(
            f"{prefix}{symbol}{superscript(exponent)}"
            for prefix, symbol, exponent in terms
        )
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


def _unit_terms_mathml(magnitude: "Numeric", terms: Sequence[UnitTerm]) -> str:
    numerator = [(p, s, e) for p, s, e in terms if e >= 0]
    denominator = [(p, s, e * -1) for p, s, e in terms if e < 0]

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
    if magnitude != 1:
        n = f"<mn>{magnitude}</mn><mo>⋅</mo>" + n

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


def unit_mathml(unit: "Unit") -> str:
    """Formats the given Unit as a MathML expression"""
    if unit.symbol:
        return f"<mi>{unit.symbol}</mi>"

    magnitude, terms = _unit_to_magnitude_and_terms(unit)
    return _unit_terms_mathml(magnitude, terms)


def quantity_repr(quantity: "Quantity") -> str:
    """Formats the given Quantity as a Python `repr`"""
    return f"Quantity(magnitude={quantity.magnitude!r}, unit={quantity.unit!r})"


def quantity_str(quantity: "Quantity") -> str:
    """Formats the given Quantity as a plaintext string"""
    if quantity.unit.symbol:
        return f"{quantity.magnitude} {quantity.unit.symbol}"

    unit_magnitude, unit_terms = _unit_to_magnitude_and_terms(quantity.unit)
    quantity = quantity * unit_magnitude
    return f"{quantity.magnitude} " + (
        "⋅".join(
            f"{prefix}{symbol}{superscript(exponent)}"
            for prefix, symbol, exponent in unit_terms
        )
    )


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
    if quantity.unit.symbol:
        return (
            "<mrow>"
            f"<mn>{quantity.magnitude}</mn>"
            "<mo></mo>"
            f"<mi>{quantity.unit.symbol}</mi>"
            "</mrow>"
        )

    unit_magnitude, unit_terms = _unit_to_magnitude_and_terms(quantity.unit)
    quantity = quantity * unit_magnitude
    return (
        "<mrow>"
        f"<mn>{quantity.magnitude}</mn>"
        "<mo></mo>"
        f"{_unit_terms_mathml(1, unit_terms)}"
        "</mrow>"
    )


def logarithm_repr(logarithm: "Logarithm") -> str:
    """Formats the given Logarithm as a Python `repr`"""
    return (
        "Logarithm("
        f"prefix={logarithm.prefix!r}, "
        f"base={logarithm.base!r}, "
        f"name={logarithm.name!r}, "
        f"symbol={logarithm.symbol!r}"
        ")"
    )


def logarithm_str(logarithm: "Logarithm") -> str:
    """Formats the given Logarithm as a plaintext string"""
    if logarithm.symbol:
        return logarithm.symbol

    function = "ln" if logarithm.base == math.e else f"log{logarithm.base}"
    return f"{logarithm.prefix.quantify()} {function}(x/x₀)"


def logarithm_pretty(
    logarithm: "Logarithm", pretty: "RepresentationPrinter", cycle: bool
) -> None:
    """Formats the given Logarithm to the provided pretty printer"""
    with pretty.group():
        pretty.text(str(logarithm))
        with pretty.group(indent=2):
            pretty.break_()
            pretty.text(repr(logarithm))


def logarithm_mathml(logarithm: "Logarithm") -> str:
    """Formats the given Logarithm as a MathML expression"""
    if logarithm.symbol:
        return f"<mi>{logarithm.symbol}</mi>"

    prefix = (
        f"<mn>{logarithm.prefix.quantify()}</mn>" if logarithm.prefix.exponent else ""
    )
    function = "ln" if logarithm.base == math.e else f"log{logarithm.base}"
    return (
        "<mrow>"
        f"{prefix}"
        f"<mi>{function}</mi>"
        "<mo>(</mo>"
        "<mfrac>"
        f"<mi>x</mi>"
        f"<mi>x₀</mi>"
        "</mfrac>"
        "<mo>)</mo>"
        "</mrow>"
    )


def logarithmic_unit_repr(logarithmic_unit: "LogarithmicUnit") -> str:
    """Formats the given LogarithmicUnit as a Python `repr`"""
    return (
        "LogarithmicUnit("
        f"logarithm={logarithmic_unit.logarithm!r}, "
        f"reference={logarithmic_unit.reference!r}"
        ")"
    )


def logarithmic_unit_str(logarithmic_unit: "LogarithmicUnit") -> str:
    """Formats the given LogarithmicUnit as a plaintext string"""
    if logarithmic_unit.symbol:
        return logarithmic_unit.symbol

    return f"{logarithmic_unit.logarithm} of {logarithmic_unit.reference}"


def logarithmic_unit_pretty(
    logarithmic_unit: "LogarithmicUnit", pretty: "RepresentationPrinter", cycle: bool
) -> None:
    """Formats the given LogarithmicUnit to the provided pretty printer"""
    with pretty.group():
        pretty.text(str(logarithmic_unit))
        with pretty.group(indent=2):
            pretty.break_()
            pretty.text(repr(logarithmic_unit))


def logarithmic_unit_mathml(logarithmic_unit: "LogarithmicUnit") -> str:
    """Formats the given LogarithmicUnit as a MathML expression"""
    if logarithmic_unit.symbol:
        return f"<mi>{logarithmic_unit.symbol}</mi>"

    return (
        "<mrow>"
        f"{logarithm_mathml(logarithmic_unit.logarithm)}"
        "<mo>of</mo>"
        f"{quantity_mathml(logarithmic_unit.reference)}"
        "</mrow>"
    )


def level_repr(level: "Level") -> str:
    """Formats the given Level as a Python `repr`"""
    return f"Level(magnitude={level.magnitude!r}, unit={level.unit!r})"


def level_str(level: "Level") -> str:
    """Formats the given Level as a plaintext string"""
    return f"{level.magnitude} {level.unit}"


def level_pretty(level: "Level", pretty: "RepresentationPrinter", cycle: bool) -> None:
    """Formats the given Level to the provided pretty printer"""
    with pretty.group():
        pretty.text(str(level))
        with pretty.group(indent=2):
            pretty.break_()
            pretty.pretty(level.magnitude)
            pretty.break_()
            pretty.pretty(level.unit)
            pretty.break_()
            pretty.text(repr(level))


def level_mathml(level: "Level") -> str:
    """Formats the given Level as a MathML expression"""
    return (
        "<mrow>"
        f"<mn>{level.magnitude}</mn>"
        "<mo>⋅</mo>"
        f"{logarithmic_unit_mathml(level.unit)}"
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
