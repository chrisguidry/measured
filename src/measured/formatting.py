SUPERSCRIPT_DIGITS = ["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
SUPERSCRIPT_NEGATIVE = "⁻"


def superscript(exponent: int) -> str:
    """Given a signed integer exponent, returns the Unicode superscript string for it

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

    prefix = SUPERSCRIPT_NEGATIVE if exponent < 0 else ""
    exponent = abs(exponent)
    return prefix + "".join(SUPERSCRIPT_DIGITS[int(d)] for d in str(exponent))
