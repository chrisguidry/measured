import argparse

from measured import Quantity, conversions, systems  # noqa: F401

parser = argparse.ArgumentParser(description="Unit conversions with measured")
parser.add_argument("quantity", help="The quantity to print conversions for")


def main() -> None:
    arguments = parser.parse_args()
    quantity = Quantity.parse(arguments.quantity)
    unit = quantity.unit
    dimension = unit.dimension

    print("Magnitude:", quantity.magnitude)
    print("Unit:", unit.name or f"{unit:/}")
    print("Dimension:", dimension.name or f"{dimension}")

    print("Defined conversions:")
    defined_conversions = sorted(
        conversions._ratios[unit].items(), key=lambda p: p[1], reverse=True
    )
    for other, ratio in defined_conversions:
        print(f"{ratio} {other.name or str(other)}")
