import pytest

from measured import Quantity
from measured.si import Kilo, Meter
from measured.us import (
    Acre,
    Chain,
    Foot,
    League,
    Rod,
    Section,
    StatuteMile,
    SurveyFoot,
    SurveyTownship,
)


@pytest.mark.parametrize(
    "left, right",
    [
        (1 * Chain**2, 4356 * SurveyFoot**2),
        (1 * Chain**2, 16 * Rod**2),
        (1 * Acre, 43560 * Foot**2),
    ],
)
def test_areas_equal(left: Quantity, right: Quantity) -> None:
    assert (
        left == right
    ), f"{left} != {right.in_unit(left.unit)} or {right} != {left.in_unit(right.unit)}"
    assert (
        right == left
    ), f"{right} != {left.in_unit(right.unit)} or {left} != {right.in_unit(left.unit)}"


@pytest.mark.parametrize(
    "left, right, within",
    [
        (1 * Chain**2, 404.6873 * Meter**2, 1e-4),
        (1 * Acre, 4046.86 * Meter**2, 1e-2),
        (1 * Acre, 10 * Chain**2, 4e-06),
        (1 * Section, 640 * Acre, 1e-15),
        (1 * Section, 2.589998 * (Kilo * Meter) ** 2, 1e0),
        (1 * Section, 1 * StatuteMile**2, 4e-06),
        (1 * SurveyTownship, 93.23993 * (Kilo * Meter) ** 2, 1e2),
        (1 * SurveyTownship, 36 * Section, 3e-16),
        (1 * SurveyTownship, 4 * League**2, 4e-06),
    ],
)
def test_areas_approximate(left: Quantity, right: Quantity, within: float) -> None:
    left.assert_approximates(right, within)
    right.assert_approximates(left, within)
