from fractions import Fraction

import pytest

from measured import (
    AmountOfSubstance,
    Area,
    Current,
    Dimension,
    Frequency,
    Length,
    LuminousIntensity,
    Mass,
    Number,
    Temperature,
    Time,
    Volume,
)


def pytest_generate_tests(metafunc):
    fundamental = [d for d in Dimension.known() if d.name]
    ids = [d.name for d in fundamental]

    for exemplar in ["a", "b", "c"]:
        if exemplar in metafunc.fixturenames:
            metafunc.parametrize(exemplar, fundamental, ids=ids)

    if "dimension" in metafunc.fixturenames:
        metafunc.parametrize("dimension", fundamental, ids=ids)


@pytest.fixture
def identity() -> Dimension:
    return Number


def test_homogenous_under_addition(a: Dimension, b: Dimension):
    # https://en.wikipedia.org/wiki/Dimensional_analysis#Dimensional_homogeneity
    #
    # Only commensurable quantities (physical quantities having the same dimension) may
    # be compared, equated, added, or subtracted.
    if a is b:
        assert a + b == a
    else:
        with pytest.raises(TypeError):
            a + b


def test_homogenous_under_subtraction(a: Dimension, b: Dimension):
    # https://en.wikipedia.org/wiki/Dimensional_analysis#Dimensional_homogeneity
    #
    # Only commensurable quantities (physical quantities having the same dimension) may
    # be compared, equated, added, or subtracted.
    if a is b:
        assert a - b == a
    else:
        with pytest.raises(TypeError):
            a - b


def test_abelian_associativity(a: Dimension, b: Dimension, c: Dimension):
    # https://en.wikipedia.org/wiki/Abelian_group
    assert (a * b) * c == a * (b * c)


def test_abelian_identity(identity: Dimension, a: Dimension):
    assert identity * a == a


def test_abelian_inverse(identity: Dimension, a: Dimension):
    inverse = a**-1
    assert inverse * a == a * inverse
    assert inverse * a == identity
    assert identity / a == inverse


def test_abelian_commutativity(a: Dimension, b: Dimension):
    assert a * b == b * a


def test_no_dimensional_exponentation(dimension: Dimension):
    with pytest.raises(TypeError):
        dimension**dimension  # type: ignore


def test_no_floating_point_exponentation(dimension: Dimension):
    with pytest.raises(TypeError):
        dimension**0.5  # type: ignore


def test_no_fractional_exponentation(dimension: Dimension):
    with pytest.raises(TypeError):
        dimension ** Fraction(1, 2)  # type: ignore


def test_only_dimensional_multiplication(dimension: Dimension):
    with pytest.raises(TypeError):
        5 * dimension  # type: ignore

    with pytest.raises(TypeError):
        dimension * 5  # type: ignore


def test_only_dimensional_division(dimension: Dimension):
    with pytest.raises(TypeError):
        dimension / 5  # type: ignore

    with pytest.raises(TypeError):
        5 / dimension  # type: ignore


def test_repr(dimension: Dimension):
    r = repr(dimension)
    assert r.startswith("<measured.Dimension(exponents=array(")
    assert dimension.name and dimension.name in r
    assert dimension.symbol and dimension.symbol in r
    assert r.endswith(")>")


def test_number():
    assert isinstance(Number, Dimension)
    assert Number.name == "number"
    assert Number.symbol == "1"
    assert Number is Number * Number


def test_length():
    assert isinstance(Length, Dimension)
    assert Length.name == "length"
    assert Length.symbol == "L"
    assert Length is Number * Length


def test_area():
    assert isinstance(Area, Dimension)
    assert Area is Length * Length


def test_volume():
    assert isinstance(Area, Dimension)
    assert Volume is Length * Length * Length
    assert Volume is Length * Area
    assert Volume is Area * Length


def test_time():
    assert isinstance(Time, Dimension)
    assert Time.name == "time"
    assert Time.symbol == "T"
    assert Time is Number * Time


def test_frequency():
    assert isinstance(Frequency, Dimension)
    assert Frequency is Number / Time


def test_mass():
    assert isinstance(Mass, Dimension)
    assert Mass.name == "mass"
    assert Mass.symbol == "M"
    assert Mass is Number * Mass


def test_current():
    assert isinstance(Current, Dimension)
    assert Current.name == "current"
    assert Current.symbol == "I"
    assert Current is Number * Current


def test_temperature():
    assert isinstance(Temperature, Dimension)
    assert Temperature.name == "temperature"
    assert Temperature.symbol == "Θ"
    assert Temperature is Number * Temperature


def test_amount_of_substance():
    assert isinstance(AmountOfSubstance, Dimension)
    assert AmountOfSubstance.name == "amount of substance"
    assert AmountOfSubstance.symbol == "N"
    assert AmountOfSubstance is Number * AmountOfSubstance


def test_luminous_intensity():
    assert isinstance(LuminousIntensity, Dimension)
    assert LuminousIntensity.name == "luminous intensity"
    assert LuminousIntensity.symbol == "J"
    assert LuminousIntensity is Number * LuminousIntensity
