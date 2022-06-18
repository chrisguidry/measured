import pytest

from measured import Length, Quantity
from measured.si import Kilo, Meter, Micro, Milli
from measured.us import (
    Acre,
    Cable,
    Chain,
    Fathom,
    Foot,
    Furlong,
    Inch,
    League,
    Link,
    Mile,
    NauticalMile,
    Pica,
    Point,
    Rod,
    Section,
    StatuteMile,
    SurveyFoot,
    SurveyTownship,
    Yard,
)


def test_point() -> None:
    assert Point.name == "point"
    assert Point.symbol == "p."
    assert Point.dimension == Length

    assert 1 * Point == (1 / 12) * Pica
    assert (1 * Point).approximates((1 / 72) * Inch, within=1e-9)
    assert 1 * Point == (127 / 360 * Milli * Meter)
    assert (1 * Point).approximates(352.778 * Micro * Meter)


def test_pica() -> None:
    assert Pica.name == "pica"
    assert Pica.symbol == "P."
    assert Pica.dimension == Length

    assert 1 * Pica == 12 * Point
    assert 1 * Pica == (1 / 6) * Inch
    assert (1 * Pica).approximates(4.233 * Milli * Meter)


def test_inch() -> None:
    assert Inch.name == "inch"
    assert Inch.symbol == "in."
    assert Inch.dimension == Length

    assert 1 * Inch == 72 * Point
    assert 1 * Inch == 6 * Pica
    assert 1 * Inch == (1 / 12) * Foot
    assert 1 * Inch == (1 / 36) * Yard
    assert 1 * Inch == 25.4 * Milli * Meter


def test_foot() -> None:
    assert Foot.name == "foot"
    assert Foot.symbol == "ft."
    assert Foot.dimension == Length

    assert (1 * Foot).approximates(864 * Point, within=1e-3)
    assert 1 * Foot == 72 * Pica
    assert 1 * Foot == 12 * Inch
    assert 1 * Foot == (1 / 3) * Yard
    assert 1 * Foot == 0.3048 * Meter


def test_yard() -> None:
    assert Yard.name == "yard"
    assert Yard.symbol == "yd."
    assert Yard.dimension == Length

    assert 1 * Yard == 36 * Inch
    assert 1 * Yard == 3 * Foot
    assert 1 * Yard == 0.9144 * Meter


def test_mile() -> None:
    assert Mile.name == "mile"
    assert Mile.symbol == "mi."
    assert Mile.dimension == Length

    assert 1 * Mile == 5280 * Foot
    assert 1 * Mile == 1760 * Yard
    assert 1 * Mile == 1.609344 * Kilo * Meter


def test_ordering() -> None:
    assert 1 * Point < 1 * Pica
    assert 1 * Pica < 1 * Inch
    assert 1 * Inch < 1 * Foot
    assert 1 * Foot < 1 * Yard
    assert 1 * Yard < 1 * Meter
    assert 1 * Kilo * Meter < 1 * Mile


def test_survey_measures() -> None:
    assert 1 * Link == 792 / 3937 * Meter
    assert (1 * Link).approximates(0.2011684 * Meter)

    assert 1 * SurveyFoot == 1200 / 3937 * Meter
    assert (1 * SurveyFoot).approximates(0.3048006 * Meter)

    assert 1 * Rod == (19800 / 3937) * Meter
    assert (1 * Rod).approximates(5.0292100 * Meter)

    assert 1 * Chain == (79200 / 3937) * Meter
    assert (1 * Chain).approximates(20.1168402 * Meter)

    assert 1 * Furlong == (792 / 3937) * Kilo * Meter
    assert (1 * Furlong).approximates(201.1684023 * Meter)

    assert 1 * StatuteMile == (6336 / 3937) * Kilo * Meter
    assert (1 * StatuteMile).approximates(1609.3472186 * Meter)

    assert 1 * League == (19008 / 3937) * Kilo * Meter
    assert (1 * League).approximates(4828.0416560 * Meter)


@pytest.mark.parametrize(
    "left, right",
    [
        (1 * Fathom, 2 * Yard),
        (1 * Fathom, 1.8288 * Meter),
        (1 * NauticalMile, 1.852 * Kilo * Meter),
    ],
)
def test_nautical_measures_equal(left: Quantity, right: Quantity) -> None:
    assert left == right, f"{left} != {right.in_unit(left.unit)}"
    assert right == left, f"{right} != {left.in_unit(right.unit)}"


@pytest.mark.parametrize(
    "left, right, within",
    [
        (1 * Cable, 0.219456 * Kilo * Meter, 1e-6),
        (1 * NauticalMile, 1.151 * Mile, 1e-3),
    ],
)
def test_nautical_measures_approximate(
    left: Quantity, right: Quantity, within: float
) -> None:
    assert left.approximates(right, within), f"{left} !~ {right.in_unit(left.unit)}"
    assert right.approximates(left, within), f"{right} !~ {left.in_unit(left.unit)}"


@pytest.mark.parametrize(
    "left, right",
    [
        (1 * Chain**2, 4356 * SurveyFoot**2),
        (1 * Chain**2, 16 * Rod**2),
        (1 * Acre, 43560 * SurveyFoot**2),
        (1 * Acre, 10 * Chain**2),
        pytest.param(
            1 * Acre,
            4046.873 * Meter**2,
            marks=pytest.mark.xfail(
                reason=(
                    "finding conversions from a defined Area "
                    "only works in one direction right now"
                )
            ),
        ),
        (1 * Section, 640 * Acre),
        (1 * Section, 1 * StatuteMile**2),
        pytest.param(
            1 * Section,
            2.589998 * (Kilo * Meter) ** 2,
            marks=pytest.mark.xfail(
                reason=(
                    "finding conversions from a defined Area "
                    "only works in one direction right now"
                )
            ),
        ),
        pytest.param(
            1 * SurveyTownship,
            36 * Section,
            marks=pytest.mark.xfail(
                reason=(
                    "finding conversions from a defined Area "
                    "only works in one direction right now"
                )
            ),
        ),
        pytest.param(
            1 * SurveyTownship,
            4 * League**2,
            marks=pytest.mark.xfail(
                reason=(
                    "finding conversions from a defined Area "
                    "only works in one direction right now"
                )
            ),
        ),
        pytest.param(
            1 * SurveyTownship,
            93.23993 * (Kilo * Meter) ** 2,
            marks=pytest.mark.xfail(
                reason=(
                    "finding conversions from a defined Area "
                    "only works in one direction right now"
                )
            ),
        ),
    ],
)
def test_areas_equal(left: Quantity, right: Quantity) -> None:
    assert left == right, f"{left} != {right.in_unit(left.unit)}"
    assert right == left, f"{right} != {left.in_unit(right.unit)}"


@pytest.mark.parametrize(
    "left, right, within",
    [
        (1 * Chain**2, 404.6873 * Meter**2, 1e-4),
    ],
)
def test_areas_approximate(left: Quantity, right: Quantity, within: float) -> None:
    assert left.approximates(right, within), f"{left} !~ {right.in_unit(left.unit)}"
    assert right.approximates(left, within), f"{right} !~ {left.in_unit(left.unit)}"
