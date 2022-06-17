from measured import Length
from measured.si import Kilo, Meter, Micro, Milli
from measured.us import Foot, Inch, Mile, Pica, Point, Yard


def test_point() -> None:
    assert Point.name == "point"
    assert Point.symbol == "p."
    assert Point.dimension == Length

    assert 1 * Point == (1 / 12) * Pica
    assert 1 * Point == (1 / 72) * Inch
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
