from math import pi as π

from measured.astronomical import (
    AstronomicalUnit,
    EarthMass,
    JupiterMass,
    LightYear,
    Parsec,
    SolarMass,
)
from measured.constants import GravitationalConstant
from measured.si import Day, Meter, Second


def test_parsec_to_astronomical_unit() -> None:
    # https://en.wikipedia.org/wiki/Parsec#Calculating_the_value_of_a_parsec
    (π * Parsec).assert_approximates(180 * 60 * 60 * AstronomicalUnit)


def test_light_year() -> None:
    # https://en.wikipedia.org/wiki/Light-year
    (1 * LightYear).assert_approximates(9460730472580800 * Meter)
    (1 * LightYear).assert_approximates(63241.077 * AstronomicalUnit, within=1e3)
    (1 * LightYear).assert_approximates(0.306601 * Parsec)


def test_deriving_solar_mass() -> None:
    # https://en.wikipedia.org/wiki/Solar_mass#Calculation
    year = (365 * Day).in_unit(Second)
    calculated = (4 * π**2 * AstronomicalUnit**3).in_unit(Meter**3) / (
        GravitationalConstant * year**2
    )
    calculated.assert_approximates(1 * SolarMass, within=2.74 + 27)


def test_solar_system_masses() -> None:
    assert 1 * EarthMass < 1 * JupiterMass < 1 * SolarMass
    (1 * SolarMass).assert_approximates(1047.348644 * JupiterMass, within=1e0)
    (1 * SolarMass).assert_approximates(332946.0487 * EarthMass, within=1e1)
    (1 * JupiterMass).assert_approximates(317.82838 * EarthMass, within=1e-3)
