from typing import Union

SUPERSCRIPTS = {
    "-": "⁻",
    ".": ".",  # There does not seem to be a superscript '.' in Unicode yet
    **{
        str(i): v
        for i, v in enumerate(["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"])
    },
}


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
