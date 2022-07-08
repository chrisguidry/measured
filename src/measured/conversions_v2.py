import operator
from collections import defaultdict
from functools import reduce
from typing import Dict, Iterable, List, Set, Tuple, TypeVar

from measured import Dimension, Number, Numeric, One, Quantity, Unit, ic  # noqa: F401

Ratio = Numeric
Offset = Numeric

_ratios: Dict[Unit, Dict[Unit, Ratio]] = defaultdict(dict)
_offsets: Dict[Unit, Dict[Unit, Offset]] = defaultdict(dict)


def equate(a: Quantity, b: Quantity) -> None:
    """Defines a conversion between one Unit and another, expressed as a ratio
    between the two."""

    if a.unit == b.unit and a.unit is not One:
        raise ValueError("No need to define conversions for a unit and itself")

    a = a.unprefixed()
    b = b.unprefixed()

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


class ConversionNotFound(ValueError):
    pass


def convert(quantity: Quantity, other_unit: Unit) -> Quantity:
    """Converts the given quantity into another unit, if possible"""
    if quantity.unit.dimension != other_unit.dimension:
        raise ConversionNotFound(
            "No conversion from "
            f"{quantity.unit} ({quantity.unit.dimension}) to "
            f"{other_unit} ({other_unit.dimension})"
        )

    this = quantity.unprefixed()
    other = other_unit.quantify()

    plan = _plan_conversion(this.unit, other.unit)
    ic(plan)

    factors = []

    for start, end, exponent in plan:
        path = _find_path(start, end)
        if not path:
            raise ConversionNotFound(f"No conversion from {start} to {end}")

        ic(path)
        factor = (_apply_path(1, path) * end) ** exponent
        factors.append(factor)

    ic(factors)

    final: Quantity = reduce(operator.mul, factors)
    ic((this.magnitude / other.magnitude) * final.magnitude)
    ic(f"{final.unit:/}", final.unit)
    ic(f"{final.unit.dimension}", final.unit.dimension)

    return (this.magnitude / other.magnitude) * final


def _plan_conversion(start: Unit, end: Unit) -> List[Tuple[Unit, Unit, int]]:
    ic(
        f"planning conversion from {start:/} -> {end:/}",
        start,
        start.dimension,
        end,
        end.dimension,
    )

    plan: List[Tuple[Unit, Unit, int]] = []
    start_factors = _splat(start)
    end_factors = _splat(end)

    ic("start", plan, start_factors, end_factors)

    ic("pass 1: find terms in start that should be cancelled")
    for dimension in list(start_factors):
        exponent = -1 if any(e < 0 for e in dimension.exponents) else 1
        ic(dimension, exponent)
        inverse = dimension**-1
        while dimension in start_factors and inverse in start_factors:
            end_factor = _clean_pop(start_factors, dimension)
            start_factor = _clean_pop(start_factors, inverse)

            plan.append((start_factor, end_factor, -exponent))
            plan.append((end_factor, end_factor, exponent))
    ic("after cancelling start_factors", plan, start_factors, end_factors)

    ic("pass 2: find 1:1 matches by dimension")
    for dimension in list(end_factors):
        exponent = -1 if any(e < 0 for e in dimension.exponents) else 1
        ic(dimension, exponent)
        while dimension in end_factors and dimension in start_factors:
            end_factor = _clean_pop(end_factors, dimension)
            start_factor = _clean_pop(start_factors, dimension)
            plan.append((start_factor, end_factor, exponent))
    ic("after matching", plan, start_factors, end_factors)

    ic("pass 3: find terms remaining in end that should be cancelled")
    for dimension in list(end_factors):
        exponent = -1 if any(e < 0 for e in dimension.exponents) else 1
        ic(dimension, exponent)
        inverse = dimension**-1
        while dimension in end_factors and inverse in end_factors:
            end_factor = _clean_pop(end_factors, dimension)
            start_factor = _clean_pop(end_factors, inverse)

            plan.append((start_factor, end_factor, exponent))
            plan.append((start_factor, start_factor, -exponent))
    ic("after cancelling end_factors", plan, start_factors, end_factors)

    ic("end", plan, start_factors, end_factors)

    assert not start_factors
    assert not end_factors

    return plan


def _splat(unit: Unit) -> Dict[Dimension, List[Unit]]:
    splatted: Dict[Dimension, List[Unit]] = defaultdict(list)

    for factor, exponent in unit.factors.items():
        if exponent > 0:
            splatted[factor.dimension].extend([factor] * exponent)
        elif exponent < 0:
            splatted[factor.dimension**-1].extend([factor] * abs(exponent))

    return dict(splatted)


K = TypeVar("K")
V = TypeVar("V")


def _clean_pop(dictionary: Dict[K, List[V]], key: K) -> V:
    value = dictionary[key].pop()
    if not dictionary[key]:
        dictionary.pop(key)
    return value


def _find_path(
    start: Unit,
    end: Unit,
) -> List[Tuple[Ratio, Offset, Unit]]:
    return _find_path_recursive(start, end, visited=set())


def _find_path_recursive(
    start: Unit,
    end: Unit,
    visited: Set[Unit],
) -> List[Tuple[Ratio, Offset, Unit]]:

    if start is end:
        return [(1, 0, end)]

    if start in visited:
        return []
    else:
        visited.add(start)

    best_path: List[Tuple[Ratio, Offset, Unit]] = []

    for intermediate, scale in _ratios[start].items():
        offset = _offsets[start].get(intermediate, 0)
        if intermediate == end:
            return [(scale, offset, end)]

        path = _find_path_recursive(intermediate, end, visited=visited)
        if not path:
            continue

        path = [(scale, offset, intermediate)] + list(path)
        path = [(scale, offset, unit) for scale, offset, unit in path]
        if not best_path or len(path) < len(best_path):
            best_path = path

    if best_path:
        return best_path

    return []


def _apply_path(
    magnitude: Numeric, path: Iterable[Tuple[Ratio, Offset, Unit]]
) -> Numeric:
    for scale, offset, _ in path:
        magnitude *= scale
        magnitude += offset
    return magnitude
