from typing import Any, List, Optional, Union

from _pytest.config import Config

from measured import Level, Measurement, Quantity, _div
from measured.conversions import ConversionNotFound

Comparable = Union[Quantity, Level, Measurement]
COMPARABLE = (Quantity, Level, Measurement)


class MeasuredPlugin:
    def pytest_assertrepr_compare(
        self, op: str, left: Any, right: Any
    ) -> Optional[List[str]]:
        if not isinstance(left, COMPARABLE) and not isinstance(right, COMPARABLE):
            return None

        comparison = ""
        difference: Optional[Quantity] = None
        relative = None

        if isinstance(left, COMPARABLE) and isinstance(right, COMPARABLE):
            if isinstance(left, Level):
                left_quantity = left.quantify()
            elif isinstance(left, Measurement):
                left_quantity = left.measurand
            elif isinstance(left, Quantity):
                left_quantity = left

            if isinstance(right, Level):
                right_quantity = right.quantify()
            elif isinstance(right, Measurement):
                right_quantity = right.measurand
            elif isinstance(right, Quantity):
                right_quantity = right

            left_unit = left_quantity.unit

            right_comparison = right

            if isinstance(right, Level):
                try:
                    right_comparison = right_quantity.in_unit(left_unit)
                    difference = left_quantity - right_comparison
                except ConversionNotFound:
                    difference = None

            elif isinstance(right, Measurement):
                try:
                    right_comparison = Measurement(
                        measurand=right_quantity.in_unit(left_unit),
                        uncertainty=right.uncertainty.in_unit(left_unit),
                    )
                    difference = left_quantity - right_comparison.measurand
                except ConversionNotFound:
                    difference = None

            elif isinstance(right, Quantity):
                try:
                    right_comparison = right.in_unit(left_unit)
                    difference = left_quantity - right_comparison
                except ConversionNotFound:
                    difference = None

            comparison = f"{left} {op} {right_comparison}"

            if difference:
                if left_quantity.magnitude != 0:
                    relative = abs(_div(difference.magnitude, left_quantity.magnitude))
                elif right_quantity.magnitude != 0:
                    relative = abs(_div(difference.magnitude, right_quantity.magnitude))
                else:
                    relative = None

        if difference is None:
            difference_description = "difference: (conversion not found)"
        else:
            difference_description = (
                f"difference: absolute={difference} relative={relative})"
            )

        return [
            f"{left} {op} {right}",
            comparison,
            difference_description,
            "where",
            f"{str(left)!r} is {left!r}",
            "and",
            f"{str(right)!r} is {right!r}",
        ]


def pytest_configure(config: Config) -> None:
    config.pluginmanager.register(MeasuredPlugin())
