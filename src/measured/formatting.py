from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:  # pragma: no cover
    from measured import Dimension

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
    return int("".join(DIGITS[c] for c in string))


def dimension_mathml(dimension: "Dimension") -> str:
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
        return f"<math>{n}</math>"

    return f"<math><mfrac><mrow>{n}</mrow><mrow>{d}</mrow></mfrac></math>"
