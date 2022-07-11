from measured.astronomical import (
    AstronomicalUnit,
    EarthMass,
    JulianYear,
    JupiterMass,
    LightYear,
    Parsec,
    SiderealDay,
    Siriometer,
    SolarMass,
)
from measured.geometry import π
from measured.physics import G
from measured.si import Hour, Meter


def test_astronomical_unit() -> None:
    (1 * AstronomicalUnit).assert_approximates(1.495978707e11 * Meter)
    (1 * Siriometer).assert_approximates(1e6 * AstronomicalUnit)


def test_parsec() -> None:
    # https://en.wikipedia.org/wiki/Parsec#Calculating_the_value_of_a_parsec
    (π * Parsec).assert_approximates(180 * 60 * 60 * AstronomicalUnit)
    (1 * Parsec).assert_approximates(3.0856775814913673e16 * Meter)


def test_light_year() -> None:
    # https://en.wikipedia.org/wiki/Light-year
    (1 * LightYear).assert_approximates(9460730472580800 * Meter)
    (1 * LightYear).assert_approximates(63241.077 * AstronomicalUnit)
    (1 * LightYear).assert_approximates(0.306601 * Parsec, within=2e-6)


def test_deriving_solar_mass() -> None:
    # https://en.wikipedia.org/wiki/Solar_mass#Calculation
    calculated = (4 * π**2 * AstronomicalUnit**3) / (G * JulianYear**2)
    calculated.assert_approximates(1 * SolarMass, within=1e-5)


def test_solar_system_masses() -> None:
    assert 1 * EarthMass < 1 * JupiterMass < 1 * SolarMass
    (1 * SolarMass).assert_approximates(1047.348644 * JupiterMass, within=3e-4)
    (1 * SolarMass).assert_approximates(332946.0487 * EarthMass, within=3e-5)
    (1 * JupiterMass).assert_approximates(317.82838 * EarthMass, within=3e-6)


def test_sidereal_day() -> None:
    (1 * SiderealDay).assert_approximates(23.9344696 * Hour, within=7e-10)
