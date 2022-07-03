import sys
from collections import defaultdict
from functools import lru_cache
from typing import Dict, Iterable, List, Optional, Set, Tuple

from measured import (
    Dimension,
    FractionalDimensionError,
    IdentityPrefix,
    Number,
    Numeric,
    One,
    Quantity,
    Unit,
)

if sys.version_info < (3, 9):  # pragma: no cover
    # math.gcd changed in Python 3.8 from a two-argument for to a variable argument form
    import math

    from typing_extensions import SupportsIndex

    def recursive_gcd(*integers: SupportsIndex) -> int:
        if len(integers) <= 2:
            return math.gcd(*integers)
        return math.gcd(integers[0], gcd(*integers[1:]))

    gcd = recursive_gcd

else:  # pragma: no cover
    from math import gcd


class ConversionNotFound(ValueError):
    pass


Ratio = Numeric
Offset = Numeric

_ratios: Dict[Unit, Dict[Unit, Ratio]] = defaultdict(dict)
_offsets: Dict[Unit, Dict[Unit, Offset]] = defaultdict(dict)


def equate(a: Quantity, b: Quantity) -> None:
    """Defines a conversion between one Unit and another, expressed as a ratio
    between the two."""

    if a.unit == b.unit and a.unit is not One:
        raise ValueError("No need to define conversions for a unit and itself")

    a = a.in_base_units()
    b = b.in_base_units()

    _ratios[a.unit][b.unit] = b.magnitude / a.magnitude
    _ratios[b.unit][a.unit] = a.magnitude / b.magnitude


def translate(scale: Unit, zero: Quantity) -> None:
    """Defines a unit as a scale starting from the given zero point in another
    unit"""
    if scale == zero.unit:
        raise ValueError("No need to define conversions for a unit and itself")

    degree = zero.unit
    offset = zero.magnitude

    _ratios[degree][scale] = 1
    _ratios[scale][degree] = 1

    _offsets[degree][scale] = -offset
    _offsets[scale][degree] = +offset


def convert(quantity: Quantity, other_unit: Unit) -> Quantity:
    """Converts the given quantity into another unit, if possible"""
    if quantity.unit.dimension != other_unit.dimension:
        raise ConversionNotFound(
            "No conversion from "
            f"{quantity.unit} ({quantity.unit.dimension}) to "
            f"{other_unit} ({other_unit.dimension})"
        )

    this = quantity.in_base_units()
    other = (1 * other_unit).in_base_units()

    this = this.magnitude * _collapse_by_dimension(this.unit)
    other = other.magnitude * _collapse_by_dimension(other.unit)

    this_numerator, this_denominator = this.unit.as_ratio()
    other_numerator, other_denominator = other.unit.as_ratio()

    numerator_path = _find(this_numerator, other_numerator)
    if not numerator_path:
        raise ConversionNotFound(
            f"No conversion from {this_numerator!r} to {other_numerator!r}"
        )

    denominator_path = _find(this_denominator, other_denominator)
    if not denominator_path:
        raise ConversionNotFound(
            f"No conversion from {this_denominator!r} to {other_denominator!r}"
        )

    numerator = this.magnitude
    for scale, offset, _ in numerator_path:
        numerator *= scale
        numerator += offset

    denominator = other.magnitude
    for scale, offset, _ in denominator_path:
        denominator *= scale
        denominator += offset

    return Quantity(numerator / denominator, other_unit)


@lru_cache(maxsize=None)
def _find(
    start: Unit,
    end: Unit,
) -> Optional[Iterable[Tuple[Ratio, Offset, Unit]]]:
    start_terms = _terms_by_dimension(start)
    end_terms = _terms_by_dimension(end)

    assert (
        start_terms.keys() == end_terms.keys()
    ), f"{start_terms.keys()} != {end_terms.keys()}"

    path: List[Tuple[Ratio, Offset, Unit]] = []
    for dimension in start_terms:
        for s, e in zip(start_terms[dimension], end_terms[dimension]):
            this_path = _find_path(s, e)
            if not this_path:
                return None
            path += this_path
    return path


def _terms_by_dimension(unit: Unit) -> Dict[Dimension, List[Unit]]:
    terms = defaultdict(list)
    for factor, exponent in unit.factors.items():
        factor = factor**exponent
        terms[factor.dimension].append(factor)
    return terms


@lru_cache(maxsize=None)
def _collapse_by_dimension(unit: Unit) -> Quantity:
    """Return a new quantity with at most a single unit in each dimension, by
    converting individual terms"""
    magnitude: Numeric = 1
    by_dimension: Dict[Dimension, Tuple[Unit, int]] = {}

    # Convert units until there is only one for each dimension
    for unit, exponent in unit.factors.items():
        dimension = unit.dimension
        quantified = unit.quantify()

        if dimension not in by_dimension:
            magnitude *= quantified.magnitude**exponent
            by_dimension[dimension] = (quantified.unit, exponent)
            continue

        current_unit, current_exponent = by_dimension[dimension]

        path = _find_path(quantified.unit, current_unit)
        if not path:
            raise ConversionNotFound(
                f"No conversion between {dimension} units {quantified.unit} "
                f"and {current_unit}"
            )

        for scale, offset, _ in path:
            magnitude *= scale**exponent
            magnitude += offset

        by_dimension[dimension] = (current_unit, current_exponent + exponent)

    final_factors = {
        unit: exponent for unit, exponent in by_dimension.values() if exponent != 0
    } or {One: 1}

    final_dimension = Number
    for dimension in by_dimension.keys():
        final_dimension *= dimension

    return Quantity(magnitude, Unit(IdentityPrefix, final_factors, final_dimension))


@lru_cache(maxsize=None)
def _find_path(
    start: Unit,
    end: Unit,
) -> Optional[List[Tuple[Ratio, Offset, Unit]]]:
    return _find_path_recursive(start, end)


def _find_path_recursive(
    start: Unit,
    end: Unit,
    visited: Optional[Set[Unit]] = None,
) -> Optional[List[Tuple[Ratio, Offset, Unit]]]:

    if start is end:
        return [(1, 0, end)]

    if visited is None:
        visited = {start}
    elif start in visited:
        return None
    else:
        visited.add(start)

    exponent, start, end = _reduce_dimension(start, end)

    if sum(start.factors.values()) > sum(end.factors.values()):
        # This is a conversion like m² -> acre, where the end dimension is defined
        # directly in the higher exponent and there isn't a lower-power unit (e.g.
        # there's no unit that represents the square root of an acre that we can
        # compare the meter to); in this case, perform the search in reverse and it
        # should be able to find available conversions
        backtracked = _backtrack(_find_path(end, start), exponent, end)
        return backtracked

    best_path = None

    for intermediate, scale in _ratios[start].items():
        offset = _offsets[start].get(intermediate, 0)
        if intermediate == end:
            return [(scale**exponent, offset**exponent, end**exponent)]

        path = _find_path_recursive(intermediate, end, visited=visited)
        if not path:
            continue

        path = [(scale, offset, intermediate)] + list(path)
        path = [
            (scale**exponent, offset**exponent, unit**exponent)
            for scale, offset, unit in path
        ]
        if not best_path or len(path) < len(best_path):
            best_path = path

    if best_path:
        return best_path

    return None


def _reduce_dimension(start: Unit, end: Unit) -> Tuple[int, Unit, Unit]:
    """Reduce the dimension of the given units to their lowest common exponents"""
    assert (
        start.dimension is end.dimension
    ), f"{start} and {end} measure different dimensions"

    if start.dimension is Number:
        return 1, start, end

    exponent = gcd(*start.dimension.exponents)

    try:
        start_root = start.root(exponent)
        end_root = end.root(exponent)
    except FractionalDimensionError:
        return 1, start, end

    return exponent, start_root, end_root


def _backtrack(
    path: Optional[Iterable[Tuple[Ratio, Offset, Unit]]],
    exponent: int,
    end: Unit,
) -> Optional[List[Tuple[Ratio, Offset, Unit]]]:
    """Given a path to convert a start unit to an end unit, produce the reverse
    path, which would convert the end unit to the start unit"""
    if path is None:
        return None

    path = list(reversed(list(path)))

    units = [u for _, _, u in path[1:]] + [end]
    scales_and_offsets = [(s, o) for s, o, _ in path]

    backtracked = [
        (1 / (scale**exponent), -(offset**exponent), unit**exponent)
        for (scale, offset), unit in zip(scales_and_offsets, units)
    ]
    return backtracked
