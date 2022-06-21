import pytest

from measured import Area, ConversionNotFound, Length, Mass, Numeric, Unit, conversions
from measured.si import Meter, Second
from measured.us import Acre, Foot, Inch


def test_disallow_self_conversion() -> None:
    with pytest.raises(ValueError, match="unit and itself"):
        Meter.equals(1 * Meter)

    with pytest.raises(ValueError, match="unit and itself"):
        conversions.equate(1 * Meter, 1 * Meter)

    with pytest.raises(ValueError, match="unit and itself"):
        conversions.equate(1 * Meter, 2 * Meter)


def test_disallow_self_zeroing() -> None:
    with pytest.raises(ValueError, match="unit and itself"):
        Meter.zero(1 * Meter)

    with pytest.raises(ValueError, match="unit and itself"):
        conversions.translate(Meter, 1 * Meter)


def test_approximating_requires_units_with_conversion() -> None:
    Bogus = Length.unit(name="bogus", symbol="bog")

    one = 1 * Meter
    other = 1 * Bogus

    assert not one.approximates(other, within=1e100)


def test_unit_conversion_must_be_in_same_dimension() -> None:
    with pytest.raises(ConversionNotFound):
        (1 * Meter).in_unit(Second)


def test_unit_always_converts_to_itself() -> None:
    converted = (10 * Meter).in_unit(Meter)
    assert converted.magnitude == 10
    assert converted.unit == Meter


def test_conversion_with_exponents() -> None:
    assert (1 * Foot) ** 2 == (12 * Inch) ** 2
    assert 1 * Foot**2 == 144 * Inch**2

    assert (1 * Foot) ** 3 == (12 * Inch) ** 3
    assert 1 * Foot**3 == 1728 * Inch**3


@pytest.mark.parametrize(
    "start, end, magnitude",
    [
        (Foot, Inch, 12.0),
        (Foot**2, Meter**2, 0.09290304),
        (Meter**2, Foot**2, 10.76391041670972),
        (Acre, Foot**2, 43560.0),
        (Foot**2, Inch**2, 144.0),
        (Acre, Inch**2, 43560.0 * 144.0),
        (Inch**2, Foot**2, 0.006944444444444444),
        (Foot**2, Acre, 0.00002295684113865932),
        (Inch**2, Acre, 0.006944444444444444 * 0.00002295684113865932),
    ],
)
def test_conversion_can_navigate_exponents(
    start: Unit, end: Unit, magnitude: Numeric
) -> None:
    converted = conversions.convert(1 * start, end)
    assert converted == magnitude * end
    assert converted.unit == end
    assert converted.magnitude == magnitude


def test_backtracking_conversions_with_no_path() -> None:
    # Set up some arbitrary units that don't convert to one another
    Hiya = Length.unit("hello", "hello")
    Mundo = Area.unit("world", "world")

    with pytest.raises(ConversionNotFound):
        conversions.convert(1 * Hiya**2, Mundo)

    with pytest.raises(ConversionNotFound):
        conversions.convert(1 * Mundo, Hiya**2)


def test_failing_to_convert_numerator() -> None:
    Gud = Length.unit("goodbye", "goodbye")
    Mun = Length.unit("moon", "moon")

    with pytest.raises(ConversionNotFound):
        (1 * Gud).in_unit(Mun)


def test_failing_to_convert_denominator() -> None:
    Flib = Mass.unit("flibbidy", "flibbidy")
    Flob = Mass.unit("flobbidy", "flobbidy")

    assert (Meter / Flib).dimension == (Meter / Flob).dimension

    with pytest.raises(ConversionNotFound):
        (1 * Meter / Flib).in_unit(Meter / Flob)
