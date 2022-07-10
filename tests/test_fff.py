from measured import Length, Mass, Time
from measured.fff import Firkin, Fortnight, Furlong
from measured.physics import c
from measured.si import (
    Centi,
    Day,
    Hour,
    Kilo,
    Kilogram,
    Mega,
    Meter,
    Micro,
    Minute,
    Second,
)
from measured.us import Inch, Mile, Pound, Yard

# https://en.wikipedia.org/wiki/FFF_system


def test_furlong() -> None:
    assert Furlong.dimension is Length
    assert Furlong.name == "furlong"
    assert Furlong.symbol == "fur."
    (1 * Furlong).assert_approximates(201.168 * Meter, 3e-6)
    (1 * Furlong) == 220 * Yard


def test_firkin() -> None:
    assert Firkin.dimension is Mass
    assert Firkin.name == "firkin"
    assert Firkin.symbol == "fir"
    assert (1 * Firkin) == 40.8233133 * Kilogram
    assert (1 * Firkin) == 90 * Pound


def test_fortnight() -> None:
    assert Fortnight.dimension is Time
    assert Fortnight.name == "fortnight"
    assert Fortnight.symbol == "ftn"
    assert (1 * Fortnight) == 14 * Day
    assert (1 * Fortnight) == 1209600 * Second
    assert (1 * Micro * Fortnight) == 1.2096 * Second


def test_furlongs_per_fortnight() -> None:
    fpf = 1 * Furlong / Fortnight

    fpf.assert_approximates(1.663e-4 * Meter / Second, 6e-5)
    fpf.assert_approximates(1 * (Centi * Meter) / Minute, 1 / 400)
    fpf.assert_approximates(5.987e-4 * (Kilo * Meter) / Hour, 3e-5)
    fpf.assert_approximates((3 / 8) * (Inch / Minute), 5e-2)
    fpf.assert_approximates(3.720e-4 * Mile / Hour, 7e-5)

    c.assert_approximates(1.8026e12 * Furlong / Fortnight, 8e-6)
    c.assert_approximates(1.8026 * (Mega * Furlong) / (Micro * Fortnight), 8e-6)
