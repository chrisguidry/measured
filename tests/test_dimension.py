from fractions import Fraction

import pytest
from hypothesis import given

from measured import (
    AmountOfSubstance,
    Area,
    Charge,
    Current,
    Dimension,
    Frequency,
    Length,
    LuminousIntensity,
    Mass,
    Number,
    PlaneAngle,
    Potential,
    Resistance,
    SolidAngle,
    Speed,
    Temperature,
    Time,
    Volume,
)
from measured.hypothesis import dimensions


@pytest.fixture(scope="module")
def identity() -> Dimension:
    return Number


@given(a=dimensions(), b=dimensions())
def test_homogenous_under_addition(a: Dimension, b: Dimension) -> None:
    # https://en.wikipedia.org/wiki/Dimensional_analysis#Dimensional_homogeneity
    #
    # Only commensurable quantities (physical quantities having the same dimension) may
    # be compared, equated, added, or subtracted.
    if a is b:
        assert a + b == a
    else:
        with pytest.raises(TypeError):
            a + b


@given(a=dimensions(), b=dimensions())
def test_homogenous_under_subtraction(a: Dimension, b: Dimension) -> None:
    # https://en.wikipedia.org/wiki/Dimensional_analysis#Dimensional_homogeneity
    #
    # Only commensurable quantities (physical quantities having the same dimension) may
    # be compared, equated, added, or subtracted.
    if a is b:
        assert a - b == a
    else:
        with pytest.raises(TypeError):
            a - b


@given(a=dimensions(), b=dimensions(), c=dimensions())
def test_abelian_associativity(a: Dimension, b: Dimension, c: Dimension) -> None:
    # https://en.wikipedia.org/wiki/Abelian_group
    assert (a * b) * c == a * (b * c)


@given(a=dimensions())
def test_abelian_identity(identity: Dimension, a: Dimension) -> None:
    assert identity * a == a


@given(a=dimensions())
def test_abelian_inverse(identity: Dimension, a: Dimension) -> None:
    inverse = a**-1
    assert inverse * a == a * inverse
    assert inverse * a == identity
    assert identity / a == inverse


@given(a=dimensions(), b=dimensions())
def test_abelian_commutativity(a: Dimension, b: Dimension) -> None:
    assert a * b == b * a


@given(dimension=dimensions())
def test_no_dimensional_exponentation(dimension: Dimension) -> None:
    with pytest.raises(TypeError):
        dimension**dimension  # type: ignore


@given(dimension=dimensions())
def test_no_floating_point_exponentation(dimension: Dimension) -> None:
    with pytest.raises(TypeError):
        dimension**0.5  # type: ignore


@given(dimension=dimensions())
def test_no_fractional_exponentation(dimension: Dimension) -> None:
    with pytest.raises(TypeError):
        dimension ** Fraction(1, 2)  # type: ignore


@given(dimension=dimensions())
def test_only_dimensional_multiplication(dimension: Dimension) -> None:
    with pytest.raises(TypeError):
        5 * dimension  # type: ignore

    with pytest.raises(TypeError):
        dimension * 5  # type: ignore


@given(dimension=dimensions())
def test_only_dimensional_division(dimension: Dimension) -> None:
    with pytest.raises(TypeError):
        dimension / 5  # type: ignore

    with pytest.raises(TypeError):
        5 / dimension  # type: ignore


@given(dimension=dimensions())
def test_repr(dimension: Dimension) -> None:
    r = repr(dimension)
    assert r.startswith("Dimension(exponents=(0,")
    assert dimension.name and dimension.name in r
    assert dimension.symbol and dimension.symbol in r
    assert r.endswith(")")


@given(dimension=dimensions())
def test_repr_roundtrips(dimension: Dimension) -> None:
    assert eval(repr(dimension)) is dimension


def test_number() -> None:
    assert isinstance(Number, Dimension)
    assert Number.name == "number"
    assert Number.symbol == "1"
    assert Number is Number * Number


def test_length() -> None:
    assert isinstance(Length, Dimension)
    assert Length.name == "length"
    assert Length.symbol == "L"
    assert Length is Number * Length


def test_area() -> None:
    assert isinstance(Area, Dimension)
    assert Area is Length * Length


def test_volume() -> None:
    assert isinstance(Area, Dimension)
    assert Volume is Length * Length * Length
    assert Volume is Length * Area
    assert Volume is Area * Length


def test_time() -> None:
    assert isinstance(Time, Dimension)
    assert Time.name == "time"
    assert Time.symbol == "T"
    assert Time is Number * Time


def test_frequency() -> None:
    assert isinstance(Frequency, Dimension)
    assert Frequency is Number / Time


def test_mass() -> None:
    assert isinstance(Mass, Dimension)
    assert Mass.name == "mass"
    assert Mass.symbol == "M"
    assert Mass is Number * Mass


def test_temperature() -> None:
    assert isinstance(Temperature, Dimension)
    assert Temperature.name == "temperature"
    assert Temperature.symbol == "Θ"
    assert Temperature is Number * Temperature


def test_charge() -> None:
    assert isinstance(Charge, Dimension)
    assert Charge.name == "charge"
    assert Charge.symbol == "Q"
    assert Charge is Number * Charge


def test_amount_of_substance() -> None:
    assert isinstance(AmountOfSubstance, Dimension)
    assert AmountOfSubstance.name == "amount of substance"
    assert AmountOfSubstance.symbol == "N"
    assert AmountOfSubstance is Number * AmountOfSubstance


def test_luminous_intensity() -> None:
    assert isinstance(LuminousIntensity, Dimension)
    assert LuminousIntensity.name == "luminous intensity"
    assert LuminousIntensity.symbol == "J"
    assert LuminousIntensity is Number * LuminousIntensity


def test_plane_angle_is_dimensionless() -> None:
    assert isinstance(PlaneAngle, Dimension)
    assert PlaneAngle == Number


def test_solid_angle_is_dimensionless() -> None:
    assert isinstance(SolidAngle, Dimension)
    assert SolidAngle == Number


def test_roots() -> None:
    assert Number.root(0) == Number
    assert Number.root(100) == Number
    assert Length.root(0) == Number
    assert Length.root(1) == Length
    assert Area.root(2) == Length
    assert Volume.root(3) == Length
    assert (Area / Time**2).root(2) == Speed


def test_only_integer_roots() -> None:
    with pytest.raises(TypeError):
        Area.root(0.5)  # type: ignore


def test_whole_power_roots_only() -> None:
    with pytest.raises(ValueError):
        Volume.root(2)


@pytest.mark.parametrize(
    "factor, whole",
    [
        (Number, Number),
        (Number, Mass),
        (Number, Area),
        (Number, Resistance),
        (Length, Area),
        (Area, Area),
        (Area, Volume),
        (Potential, Current),
    ],
)
def test_testing_factors(factor: Dimension, whole: Dimension) -> None:
    assert factor.is_factor(whole)


@pytest.mark.parametrize(
    "nonfactor, whole",
    [
        (Time, Length),
        (Length, Time),
        (Mass, Number),
        (Area, Number),
        (Area, Length),
    ],
)
def test_testing_non_factors(nonfactor: Dimension, whole: Dimension) -> None:
    assert not nonfactor.is_factor(whole)
