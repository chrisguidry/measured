import operator
from functools import reduce
from typing import Any, Optional

from measured import Numeric, One, Quantity, Unit

from . import _parser
from .formatting import from_superscript

ParseError = _parser.LarkError


class QuantityTransformer(_parser.Transformer[Any, "Quantity"]):
    inline = _parser.v_args(inline=True)

    @inline
    def unit(self, numerator: Unit, denominator: Optional[Unit] = None) -> Unit:
        return numerator / (denominator or One)

    @inline
    def unit_sequence(self, *terms: Unit) -> Unit:
        return reduce(operator.mul, terms)

    @inline
    def term(self, symbol: str, exponent: int = 1) -> Unit:
        return Unit.resolve_symbol(symbol) ** exponent

    @inline
    def carat_exponent(self, exponent: str) -> int:
        return int(exponent[1:])

    @inline
    def superscript_exponent(self, exponent: str) -> int:
        value = from_superscript(exponent)
        assert isinstance(value, int)
        return value

    @inline
    def quantity(self, magnitude: Numeric, unit: Unit) -> "Quantity":
        return Quantity(magnitude, unit)

    int = inline(int)
    float = inline(float)


parser: _parser.Lark = _parser.Parser(transformer=QuantityTransformer())  # type: ignore
