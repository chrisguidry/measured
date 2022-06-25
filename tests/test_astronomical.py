from math import pi as π

from measured.astronomical import (
    AstronomicalUnit,
    EarthMass,
    JulianYear,
    JupiterMass,
    LightYear,
    Parsec,
    SolarMass,
)
from measured.fundamental import GravitationalConstant
from measured.si import Meter


def test_parsec() -> None:
    # https://en.wikipedia.org/wiki/Parsec#Calculating_the_value_of_a_parsec
    (π * Parsec).assert_approximates(180 * 60 * 60 * AstronomicalUnit)
    (1 * Parsec).assert_approximates(3.0856775814913673e16 * Meter, within=1e3)


def test_light_year() -> None:
    # https://en.wikipedia.org/wiki/Light-year
    (1 * LightYear).assert_approximates(9460730472580800 * Meter)
    (1 * LightYear).assert_approximates(63241.077 * AstronomicalUnit, within=1e3)
    (1 * LightYear).assert_approximates(0.306601 * Parsec)


def test_deriving_solar_mass() -> None:
    # https://en.wikipedia.org/wiki/Solar_mass#Calculation
    calculated = (4 * π**2 * AstronomicalUnit**3) / (
        GravitationalConstant * JulianYear**2
    )
    calculated.assert_approximates(1 * SolarMass, within=2.74e27)


def test_solar_system_masses() -> None:
    assert 1 * EarthMass < 1 * JupiterMass < 1 * SolarMass
    (1 * SolarMass).assert_approximates(1047.348644 * JupiterMass, within=1e0)
    (1 * SolarMass).assert_approximates(332946.0487 * EarthMass, within=1e1)
    (1 * JupiterMass).assert_approximates(317.82838 * EarthMass, within=1e-3)
