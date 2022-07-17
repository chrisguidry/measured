from measured.astronomical import (
    H0,
    AstronomicalUnit,
    Crab,
    EarthMass,
    HubbleLength,
    HubbleTime,
    HubbleVolume,
    Jansky,
    JulianYear,
    JupiterMass,
    LightYear,
    Parsec,
    SiderealDay,
    Siriometer,
    SolarMass,
)
from measured.energy import Erg
from measured.geometry import π
from measured.metric import Barn
from measured.physics import G
from measured.si import (
    Atto,
    Centi,
    ElectronVolt,
    Hertz,
    Hour,
    Kilo,
    Liter,
    Mega,
    Meter,
    Milli,
    Second,
    Watt,
)
from measured.us import Inch


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


def test_attoparsec() -> None:
    (1 * Atto * Parsec).assert_approximates(3.086 * Centi * Meter, within=2e-4)
    (1 * Atto * Parsec).assert_approximates(1.215 * Inch, within=2e-4)


def test_barn_megaparsec() -> None:
    (1 * Barn * (Mega * Parsec)).assert_approximates(3 * Milli * Liter, within=0.03)


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
    (1 * SiderealDay).assert_approximates(86164.0905 * Second, within=0)
    (1 * SiderealDay).assert_approximates(23.9344696 * Hour, within=7e-10)


def test_jansky() -> None:
    assert 1 * Jansky == 1e-26 * Watt / Meter**2 / Hertz


def test_crab() -> None:
    keV = Kilo * ElectronVolt
    cm = Centi * Meter
    s = Second

    assert 1 * Crab == 2.4e-8 * Erg / (cm**2 * s)
    (1 * Crab).assert_approximates(15 * keV / (cm**2 * s), within=1e-2)


def test_hubble_constant() -> None:
    H0.assert_approximates(((67400 * Meter) / (1000000 * Parsec)) / Second)


def test_hubble_time() -> None:
    (1 * HubbleTime).assert_approximates(14.4e9 * JulianYear, within=0.008)


def test_hubble_length() -> None:
    (1 * HubbleLength).assert_approximates(14.4e9 * LightYear, within=0.008)


def test_hubble_volume() -> None:
    (1 * HubbleVolume).assert_approximates(1e79 * Meter**3, within=0.09)
    (1 * HubbleVolume).assert_approximates(1e31 * LightYear**3, within=0.28)


def test_hubble_barn() -> None:
    (1 * HubbleLength * Barn).assert_approximates(13.1 * Liter, within=0.05)
