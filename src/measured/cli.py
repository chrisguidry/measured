import argparse
from typing import Optional, Set

from measured import Numeric, Offset, Quantity, Unit, conversions, systems  # noqa: F401

parser = argparse.ArgumentParser(description="Unit conversions with measured")
parser.add_argument(
    "quantity", metavar="term", nargs="+", help="The quantity to print conversions for"
)


def print_conversion_tree(
    quantity: Quantity,
    depth: int = 0,
    visited: Optional[Set[Unit]] = None,
) -> None:
    unit = quantity.unit

    if visited is None:
        visited = {unit}
    else:
        visited.add(unit)

    indent = "  " * depth

    children = sorted(
        conversions._ratios[unit].items(),
        key=lambda p: p[1],
        reverse=True,
    )
    for other, ratio in children:
        if other in visited:
            continue

        offset = conversions._offsets[unit].get(other, 0)

        magnitude = (quantity.magnitude * ratio) + offset
        next_quantity = Quantity(magnitude, other)

        print(f"{indent}{next_quantity}")
        print_conversion_tree(next_quantity, depth=depth + 1, visited=visited)


def main() -> None:
    arguments = parser.parse_args()
    quantity = Quantity.parse(" ".join(arguments.quantity))
    unit = quantity.unit
    dimension = unit.dimension

    print("Magnitude:", quantity.magnitude)
    print("Unit:", unit.name or f"{unit:/}")
    print("Dimension:", dimension.name or f"{dimension}")

    print("Equivalent to:")
    print_conversion_tree(quantity)
