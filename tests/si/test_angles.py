from math import pi as π

import pytest

from measured import Number, One, PlaneAngle, Quantity, SolidAngle
from measured.si import Arcminute, Arcsecond, Degree, Radian, Steradian


def test_radian_is_dimensionless_but_unique() -> None:
    assert Radian.dimension is Number
    assert Radian.dimension is PlaneAngle
    assert Radian != One
    assert Radian != Steradian
    assert Radian.name == "radian"
    assert Radian.symbol == "rad"


def test_steradian_is_dimensionless_but_unique() -> None:
    assert Steradian.dimension is Number
    assert Steradian.dimension is SolidAngle
    assert Steradian != One
    assert Steradian != Radian
    assert Steradian.name == "steradian"
    assert Steradian.symbol == "sr"


@pytest.mark.parametrize(
    "left, right",
    [
        (0 * Radian, 0 * Degree),
        (π / 4 * Radian, 45 * Degree),
        (1 * Radian, 180 / π * Degree),
        (π / 2 * Radian, 90 * Degree),
        (2 * Radian, 360 / π * Degree),
        (π * Radian, 180 * Degree),
        (3 * π / 2 * Radian, 270 * Degree),
        (2 * π * Radian, 360 * Degree),
        (1 * Arcminute, 60 * Arcsecond),
        (1 * Degree, 60 * Arcminute),
        (1 * Arcsecond, 0.000004848136 * Radian),
        (1 * Arcminute, 0.000290888 * Radian),
    ],
)
def test_angle_conversions(left: Quantity, right: Quantity) -> None:
    left.assert_approximates(right)
    right.assert_approximates(left)
