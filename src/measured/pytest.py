from typing import Any, List, Optional, Union

from _pytest.config import Config

from measured import Measurement, Quantity
from measured.conversions import ConversionNotFound

Comparable = Union[Quantity, Measurement]
COMPARABLE = (Quantity, Measurement)


class MeasuredPlugin:
    def pytest_assertrepr_compare(
        self, op: str, left: Any, right: Any
    ) -> Optional[List[str]]:

        if not isinstance(left, COMPARABLE) and not isinstance(right, COMPARABLE):
            return None

        comparison = ""
        difference = ""

        if isinstance(left, COMPARABLE) and isinstance(right, COMPARABLE):
            left_quantity = left.measurand if isinstance(left, Measurement) else left
            right_quantity = (
                right.measurand if isinstance(right, Measurement) else right
            )
            left_unit = left_quantity.unit

            right_comparison = right

            if isinstance(right, Quantity):
                try:
                    right_comparison = right.in_unit(left_unit)
                    difference = str(left_quantity - right_comparison)
                except ConversionNotFound:
                    difference = "(conversion not found)"

            elif isinstance(right, Measurement):
                try:
                    right_comparison = Measurement(
                        measurand=right_quantity.in_unit(left_unit),
                        uncertainty=right.uncertainty.in_unit(left_unit),
                    )
                    difference = str(left_quantity - right_comparison.measurand)
                except ConversionNotFound:
                    difference = "(conversion not found)"

            comparison = f"{left} {op} {right_comparison}"

        return [
            f"{left} {op} {right}",
            comparison,
            f"difference: {difference}",
            "where",
            f"{str(left)!r} is {left!r}",
            "and",
            f"{str(right)!r} is {right!r}",
        ]


def pytest_configure(config: Config) -> None:
    config.pluginmanager.register(MeasuredPlugin())
