import argparse
from typing import Generator, Iterable, Optional, Set, Tuple

from measured import Numeric, Offset, Quantity, Unit, conversions, systems  # noqa: F401

parser = argparse.ArgumentParser(description="Unit conversions with measured")
parser.add_argument(
    "quantity", metavar="term", nargs="+", help="The quantity to print conversions for"
)


def all_equivalents(
    quantity: Quantity,
    depth: int = 0,
    visited: Optional[Set[Unit]] = None,
) -> Generator[Quantity, None, None]:
    unit = quantity.unit

    if visited is None:
        visited = {unit}
    else:
        visited.add(unit)

    for other, ratio in conversions._ratios[unit].items():
        if other in visited:
            continue

        offset = conversions._offsets[unit].get(other, 0)

        magnitude = (quantity.magnitude * ratio) + offset
        next_quantity = Quantity(magnitude, other)

        yield next_quantity
        yield from all_equivalents(next_quantity, depth + 1, visited=visited)


def dot_aligned(
    quantities: Iterable[Quantity],
) -> Generator[Tuple[str, Unit], None, None]:
    try:
        magnitudes, units = zip(*((q.magnitude, q.unit) for q in quantities))
    except ValueError:
        return

    magnitude_strings = [str(m) for m in magnitudes]
    dot_indices = [s.find(".") for s in magnitude_strings]
    largest_left = max(dot_indices)
    right_padding = max(len(m) for m in magnitude_strings) + largest_left
    for (magnitude_string, dot_index), unit in zip(
        zip(magnitude_strings, dot_indices), units
    ):
        left_padding = largest_left - dot_index
        yield format(" " * left_padding + magnitude_string, f"<{right_padding}"), unit


def main() -> None:
    arguments = parser.parse_args()
    quantity = Quantity.parse(" ".join(arguments.quantity))
    quantity = quantity.in_base_units()
    unit = quantity.unit
    dimension = unit.dimension

    print("Magnitude:", quantity.magnitude)
    print("Unit:", unit.name or f"{unit:/}")
    print("Dimension:", dimension.name or f"{dimension}")

    print("Equivalent to:")
    equivalents = sorted(
        all_equivalents(quantity), key=lambda q: abs(q.magnitude), reverse=True
    )
    for magnitude_string, unit in dot_aligned(equivalents):
        print(f"{magnitude_string} {unit.name}")
