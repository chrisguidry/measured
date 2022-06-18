from measured import Length
from measured.si import Kilo, Meter, Micro, Milli
from measured.us import (
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
    StatuteMile,
    SurveyFoot,
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


def test_nautical_measures() -> None:
    assert 1 * Fathom == 2 * Yard
    assert 1 * Fathom == 1.8288 * Meter

    assert 1 * Cable == 0.219456 * Kilo * Meter

    assert 1 * NauticalMile == 1.852 * Kilo * Meter
    assert (1 * NauticalMile).approximates(1.151 * Mile, within=1e-3)
