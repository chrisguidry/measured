import sys
import textwrap
from argparse import ArgumentParser, RawTextHelpFormatter
from typing import Generator, Iterable, Optional, Set, Tuple

from measured import Quantity, Unit, conversions, systems  # noqa: F401

parser = ArgumentParser(
    description="Unit conversions with measured",
    epilog=textwrap.dedent(
        """
        Quantities are expressed as a number followed by any number of terms multiplied,
        divided, or raised to powers.  For example:

        $ measured 5 mile
        $ measured 3 meter^2
        $ measured 4 meter/second
    """,
    ),
    formatter_class=RawTextHelpFormatter,
)
parser.add_argument(
    "quantity", metavar="term", nargs="*", help="The quantity to print conversions for"
)
parser.add_argument("--list", action="store_true", help="List all available units")


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


def print_unit_list() -> None:
    for symbol, unit in Unit._by_symbol.items():
        print(f"{symbol} ({unit.name}, {unit.dimension.name or unit.dimension.symbol})")


def print_quantity(input_string: str) -> None:
    try:
        quantity = Quantity.parse(input_string)
    except Exception as e:
        print(f"Error parsing quantity from {input_string!r}:\n{str(e)}")
        sys.exit(1)

    quantity = quantity.unprefixed()
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


def main() -> None:
    arguments = parser.parse_args()

    if arguments.list:
        print_unit_list()
        return

    input_string = " ".join(arguments.quantity)
    if input_string:
        print_quantity(input_string)
        return

    parser.print_help()
