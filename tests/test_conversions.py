import pytest

from measured import (
    Area,
    Length,
    Mass,
    Number,
    Numeric,
    One,
    Pressure,
    Quantity,
    Unit,
    conversions,
)
from measured.geometry import π
from measured.physics import gₙ
from measured.si import Degree, Meter, Minute, Newton, Pascal, Radian, Second
from measured.us import PSI, Acre, Foot, Inch, Pica, Pound, PoundForce, Yard


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

    assert not one.approximates(other)


def test_unit_conversion_must_be_in_same_dimension() -> None:
    with pytest.raises(conversions.ConversionNotFound):
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


def test_conversion_navigates_multiple_steps() -> None:
    # 1 Yard -> 36 Inch -> 216 Pica
    (1 * Yard).assert_approximates(216 * Pica)
    (216 * Pica).assert_approximates(1 * Yard)


def test_cancelling_units() -> None:
    speed = 10 * Meter / Second
    time = 1 * Minute
    distance = speed * time
    assert distance.in_unit(Meter) == 600 * Meter


def test_dimensionless_units() -> None:
    assert (π / 2 * Radian).in_unit(Degree) == 90 * Degree


def test_conversions_applied_during_subtraction() -> None:
    first = 2 * Meter / Second
    second = 30 * Foot / Minute
    assert first - second == 1.8476 * Meter / Second


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
        (
            Inch**2 * Foot**2,
            Acre**2,
            (0.006944444444444444 * 0.00002295684113865932) / 43560.0,
        ),
    ],
)
def test_conversion_can_navigate_exponents(
    start: Unit, end: Unit, magnitude: Numeric
) -> None:
    converted = conversions.convert(1 * start, end)
    assert converted.unit == end
    assert converted.magnitude == pytest.approx(magnitude)
    converted.assert_approximates(magnitude * end)


def test_backtracking_conversions_with_no_path() -> None:
    # Set up some arbitrary units that don't convert to one another, simulating the
    # situation of acres and square inches
    Inchy = Length.unit("inchy", "inchy")
    Achy = Area.unit("achy", "achy")

    with pytest.raises(conversions.ConversionNotFound):
        conversions.convert(1 * Inchy**2, Achy)

    with pytest.raises(conversions.ConversionNotFound):
        conversions.convert(1 * Achy, Inchy**2)


def test_failing_to_convert_numerator() -> None:
    Gud = Length.unit("goodbye", "goodbye")
    Mun = Length.unit("moon", "moon")

    with pytest.raises(conversions.ConversionNotFound):
        (1 * Gud).in_unit(Mun)


def test_replacing_complex_factors_when_there_are_no_alternatives() -> None:
    # This cover a particular branch through conversions._replace_factors, where there
    # are no alternatives for a given unit
    Krikey = Area.unit("krikey", "krikey")
    Mate = Area.unit("mate", "mate")

    with pytest.raises(conversions.ConversionNotFound):
        (1 * Krikey * Krikey).in_unit(Mate * Mate)


def test_alternatives_available_but_not_better() -> None:
    # This cover a particular branch through conversions._replace_factors, where there
    # are multiple alternatives, but none is particularly better
    Oy = Area.unit("oy", "oy")
    Vey = Area.unit("vey", "vey")
    Oof = Area.unit("oof", "oof")

    Oy.equals(1 * Oof)
    Vey.equals(1 * Oof)

    assert 1 * Oof * Second == 1 * Oy * Second


def test_failing_to_convert_denominator() -> None:
    Flib = Mass.unit("flibbidy", "flibbidy")
    Flob = Mass.unit("flobbidy", "flobbidy")

    assert (Meter / Flib).dimension is (Meter / Flob).dimension

    with pytest.raises(conversions.ConversionNotFound):
        (1 * Meter / Flib).in_unit(Meter / Flob)


def test_failing_to_collapse_dimensions() -> None:
    Jib = Mass.unit("jibbity", "jibbity")
    Job = Mass.unit("jobbity", "jobbity")

    assert (Jib / Job).dimension is Number
    assert (Job / Jib).dimension is Number

    with pytest.raises(conversions.ConversionNotFound):
        ((1 * Jib) / (1 * Job)).in_unit(One)


def test_replacing_multiple_factors() -> None:
    left = 1 * PoundForce * PoundForce
    right = (1 * Pound * gₙ) * (1 * Pound * gₙ)

    # These comparisons require replacing the PoundForce unit multiple times
    assert left == right
    assert right == left


PRESSURE_EQUIVALENTS = [
    10000 * Newton / Meter**2,
    10000 * Pascal,
    1.4503774 * PSI,
    1.4503774 * PoundForce / Inch**2,
    208.85434305 * PoundForce / Foot**2,
    22046.226 * (Pound * Meter / Second**2) / Meter**2,
    2048.163 * (Pound * Meter / Second**2) / Foot**2,
    6719.689751 * (Pound * Foot / Second**2) / Foot**2,
    46.664512 * (Pound * Foot / Second**2) / Inch**2,
    167992.2432 * (Pound * Foot / Minute**2) / Inch**2,
    9097695 * PoundForce / Acre,
    89217910.67175 * (Pound * Meter / Second**2) / Acre,
]


@pytest.mark.parametrize("equivalent", PRESSURE_EQUIVALENTS)
def test_converting_pressure_terms_forward(equivalent: Quantity) -> None:
    quantity = 10000 * Newton / Meter**2
    assert quantity.unit.dimension is Pressure

    converted = quantity.in_unit(equivalent.unit)
    assert converted.unit.dimension is Pressure
    assert converted.unit is equivalent.unit
    assert converted.magnitude == pytest.approx(equivalent.magnitude)


@pytest.mark.parametrize("equivalent", PRESSURE_EQUIVALENTS)
def test_converting_pressure_terms_backward(equivalent: Quantity) -> None:
    quantity = 10000 * Newton / Meter**2
    assert quantity.unit.dimension is Pressure

    reversed = equivalent.in_unit(Newton / Meter**2)
    assert reversed.unit.dimension is Pressure
    assert reversed.unit is Newton / Meter**2
    assert reversed.magnitude == pytest.approx(10000)
