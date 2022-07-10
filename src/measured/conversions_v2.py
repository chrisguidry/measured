import functools
import operator
from collections import defaultdict
from functools import reduce
from typing import Dict, Iterable, List, Set, Tuple, TypeVar

from measured import ic  # noqa: F401
from measured import (
    Dimension,
    FractionalDimensionError,
    Number,
    Numeric,
    One,
    Quantity,
    Unit,
)

from .compat import gcd

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

    for ratio, start, end, exponent in plan:
        path = _find_path(start, end)
        if not path:
            raise ConversionNotFound(f"No conversion from {start} to {end}")

        ic(path)
        factor = ratio * ((_apply_path(1, path) * end) ** exponent)
        factors.append(factor)

    ic(factors)

    final: Quantity = reduce(operator.mul, factors)
    ic((this.magnitude / other.magnitude) * final.magnitude)
    ic(f"{final.unit:/}", final.unit)
    ic(f"{final.unit.dimension}", final.unit.dimension)
    assert final.unit.dimension is other_unit.dimension

    return (this.magnitude / other.magnitude) * (final.magnitude * other_unit)


def _apply_path(
    magnitude: Numeric, path: Iterable[Tuple[Ratio, Offset, Unit]]
) -> Numeric:
    for scale, offset, _ in path:
        magnitude *= scale
        magnitude += offset
    return magnitude


Exponent = int
Plan = List[Tuple[Ratio, Unit, Unit, Exponent]]


@functools.lru_cache(maxsize=None)
def _plan_conversion(start: Unit, end: Unit) -> Plan:
    ic("*" * 50)
    ic(
        f"##### planning conversion from {start:/} -> {end:/}",
        start,
        start.dimension,
        end,
        end.dimension,
    )

    plan: Plan = []
    start_factors = _splat(start)
    end_factors = _splat(end)

    ic("start", plan, start_factors, end_factors)

    ic("pass 0: is there just a direct path?")
    direct_path = _find_path(start, end)
    if direct_path:
        ic(direct_path)
        return [(1, start, end, 1)]

    ic("pass 1: try to replace units with simpler ones from the conversions table")
    plan += [
        (1 / ratio, start, end, exponent)
        for ratio, start, end, exponent in _replace_factors(end_factors)
    ]
    ic("after replacing end factors", plan, start_factors, end_factors)
    plan += [
        (ratio, end, start, exponent)
        for ratio, start, end, exponent in _replace_factors(start_factors)
    ]
    ic("after replacing start factors", plan, start_factors, end_factors)

    ic("pass 2: collect factors of the end terms from the start terms")
    plan += _match_factors(start_factors, end_factors)
    ic("after matching factors", plan, start_factors, end_factors)

    ic("pass 3: collect factors of the start terms from the end terms")
    plan += [
        (1, end, start, exponent)
        for ratio, start, end, exponent in _match_factors(end_factors, start_factors)
    ]
    ic("after matching factors", plan, start_factors, end_factors)

    ic("pass 4: cancel any remaining terms of the end factors")
    plan += _cancel_factors(end_factors)
    ic("after cancelling end factors", plan, start_factors, end_factors)

    ic("pass 5: cancel any remaining terms of the start factors")
    plan += _cancel_factors(start_factors, invert=True)
    ic("after cancelling start factors", plan, start_factors, end_factors)

    ic("end", plan, start_factors, end_factors)

    assert not start_factors
    assert not end_factors

    return plan


def _replace_factors(factors: Dict[Dimension, List[Unit]]) -> Plan:
    plan: Plan = []

    # Continue looking for replacements until the plan stops changing
    previous_plan_size = -1
    while len(plan) != previous_plan_size:
        previous_plan_size = len(plan)

        replacements: List[Tuple[Dimension, Unit, Unit]] = []

        for dimension, units in factors.items():
            # Only try this for units in higher/derived dimensions
            if sum(abs(e) for e in dimension.exponents) <= 1:
                continue

            for unit in units:
                if not _ratios.get(unit):
                    continue

                # TODO: this is looking for the alternative unit with the most factors,
                # assuming that more factors means a higher chance that these are the
                # simplest units; is this a good assumption?
                alternatives = sorted(
                    _ratios[unit].keys(), key=lambda u: len(u.factors), reverse=True
                )
                for alternative in alternatives:
                    # Consider this a better alternative if it has more factors, or it
                    # has factors with higher exponents, and will thus "splat" out into
                    # a larger number of smaller/more fundamental units
                    has_more_factors = len(alternative.factors) > len(unit.factors)
                    has_smaller_factors = sum(alternative.factors.values()) > sum(
                        unit.factors.values()
                    )

                    if has_more_factors or has_smaller_factors:
                        replacements.append((dimension, unit, alternative))
                        break

        for dimension, unit, alternative in replacements:
            overall_sign = 1
            if not unit.dimension.is_factor(dimension):
                assert (unit**-1).dimension.is_factor(dimension)
                overall_sign = -1

            ratio = _ratios[unit][alternative]
            ic(dimension, unit, alternative, ratio)

            _clean_remove(factors, dimension, unit)
            for unit, exponent in alternative.factors.items():
                unit_sign = -1 if exponent < 0 else 1
                unit_dimension = unit.dimension ** (unit_sign * overall_sign)
                if unit_dimension not in factors:
                    factors[unit_dimension] = []
                factors[unit_dimension].extend([unit] * abs(exponent))
            plan.append((ratio, One, One, 1))
            ic(factors)

    return plan


def _match_factors(
    start_factors: Dict[Dimension, List[Unit]],
    end_factors: Dict[Dimension, List[Unit]],
) -> Plan:

    plan: Plan = []

    dimensions_to_match = _by_complex_first(
        dimension for dimension, factors in end_factors.items() for _ in factors
    )

    for end_dimension in dimensions_to_match:
        ic(end_dimension)

        # go see if you can make a complete factor of end_dimension out of the
        # dimensions available in start_factors
        dimension_factors: List[Dimension] = []
        dimensions_to_check = _by_complex_first(
            dimension for dimension, factors in start_factors.items() for _ in factors
        )

        remaining = end_dimension
        while dimensions_to_check:
            ic(remaining)
            start_dimension = dimensions_to_check.pop(0)
            if start_dimension.is_factor(remaining):
                ic(start_dimension)
                dimension_factors.append(start_dimension)
                remaining /= start_dimension

            if remaining is Number:
                break

        if not dimension_factors:
            continue

        discovered_dimension = reduce(operator.mul, dimension_factors)
        ic(end_dimension, discovered_dimension, discovered_dimension is end_dimension)
        if discovered_dimension is not end_dimension:
            continue

        combined_start_factor: Unit = reduce(
            operator.mul,
            [_clean_pop(start_factors, d) for d in dimension_factors],
        )
        end_factor = _clean_pop(end_factors, end_dimension)

        # TODO: this doesn't seem right in light of complex units with mixed exponents
        exponent = -1 if any(e < 0 for e in end_dimension.exponents) else 1

        plan.append((1, combined_start_factor, end_factor, exponent))

    return plan


def _cancel_factors(factors: Dict[Dimension, List[Unit]], invert: bool = False) -> Plan:
    plan: Plan = []

    for dimension in list(factors):
        exponent = -1 if any(e < 0 for e in dimension.exponents) else 1
        ic(dimension, exponent)
        inverse = dimension**-1
        while dimension in factors and inverse in factors:
            end_factor = _clean_pop(factors, dimension)
            if dimension is inverse:
                continue
            start_factor = _clean_pop(factors, inverse)

            if invert:
                plan.append((1, start_factor, end_factor, -exponent))
                plan.append((1, end_factor, end_factor, exponent))
            else:
                plan.append((1, start_factor, end_factor, exponent))
                plan.append((1, start_factor, start_factor, -exponent))

    return plan


def _splat(unit: Unit) -> Dict[Dimension, List[Unit]]:
    splatted: Dict[Dimension, List[Unit]] = defaultdict(list)

    for factor, exponent in unit.factors.items():
        if exponent < 0:
            splatted[factor.dimension**-1].extend([factor] * abs(exponent))
        else:
            splatted[factor.dimension].extend([factor] * exponent)

    return dict(splatted)


def _by_complex_first(dimensions: Iterable[Dimension]) -> List[Dimension]:
    return sorted(
        dimensions, key=lambda d: sum(abs(e) for e in d.exponents), reverse=True
    )


K = TypeVar("K")
V = TypeVar("V")


def _clean_pop(dictionary: Dict[K, List[V]], key: K) -> V:
    value = dictionary[key].pop(0)
    if not dictionary[key]:
        dictionary.pop(key)
    return value


def _clean_remove(dictionary: Dict[K, List[V]], key: K, item: V) -> None:
    dictionary[key].remove(item)
    if not dictionary[key]:
        dictionary.pop(key)


Path = List[Tuple[Ratio, Offset, Unit]]


@functools.lru_cache(maxsize=None)
def _find_path(
    start: Unit,
    end: Unit,
) -> Path:
    return _find_path_recursive(start, end, visited=set())


def _find_path_recursive(
    start: Unit,
    end: Unit,
    visited: Set[Unit],
) -> Path:

    if start is end:
        return [(1, 0, end)]

    if start in visited:
        return []
    else:
        visited.add(start)

    exponent, start, end = _reduce_dimension(start, end)

    best_path: Path = []

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

    return []


def _reduce_dimension(start: Unit, end: Unit) -> Tuple[int, Unit, Unit]:
    """Reduce the dimension of the given units to their lowest common exponents"""
    assert start.dimension is end.dimension, (
        f"{start} ({start.dimension}) and {end} ({end.dimension}) measure "
        "different dimensions"
    )

    if start.dimension is Number:
        return 1, start, end

    exponent = gcd(*start.dimension.exponents)

    try:
        start_root = start.root(exponent)
        end_root = end.root(exponent)
    except FractionalDimensionError:
        return 1, start, end

    return exponent, start_root, end_root