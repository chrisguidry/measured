from measured import approximately
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
    assert 1 * AstronomicalUnit == approximately(1.495978707e11 * Meter)
    assert 1 * Siriometer == approximately(1e6 * AstronomicalUnit)


def test_parsec() -> None:
    # https://en.wikipedia.org/wiki/Parsec#Calculating_the_value_of_a_parsec
    assert π * Parsec == approximately(180 * 60 * 60 * AstronomicalUnit)
    assert 1 * Parsec == approximately(3.0856775814913673e16 * Meter)


def test_light_year() -> None:
    # https://en.wikipedia.org/wiki/Light-year
    assert 1 * LightYear == approximately(9460730472580800 * Meter)
    assert 1 * LightYear == approximately(63241.077 * AstronomicalUnit)
    assert 1 * LightYear == approximately(0.306601 * Parsec, within=2e-6)


def test_attoparsec() -> None:
    assert 1 * Atto * Parsec == approximately(3.086 * Centi * Meter, within=2e-4)
    assert 1 * Atto * Parsec == approximately(1.215 * Inch, within=2e-4)


def test_barn_megaparsec() -> None:
    assert 1 * Barn * (Mega * Parsec) == approximately(3 * Milli * Liter, within=0.03)


def test_deriving_solar_mass() -> None:
    # https://en.wikipedia.org/wiki/Solar_mass#Calculation
    calculated = (4 * π**2 * AstronomicalUnit**3) / (G * JulianYear**2)
    assert calculated == approximately(1 * SolarMass, within=1e-5)


def test_solar_system_masses() -> None:
    assert 1 * EarthMass < 1 * JupiterMass < 1 * SolarMass
    assert 1 * SolarMass == approximately(1047.348644 * JupiterMass, within=3e-4)
    assert 1 * SolarMass == approximately(332946.0487 * EarthMass, within=3e-5)
    assert 1 * JupiterMass == approximately(317.82838 * EarthMass, within=3e-6)


def test_sidereal_day() -> None:
    assert 1 * SiderealDay == approximately(86164.0905 * Second, within=0)
    assert 1 * SiderealDay == approximately(23.9344696 * Hour, within=7e-10)


def test_jansky() -> None:
    assert 1 * Jansky == 1e-26 * Watt / Meter**2 / Hertz


def test_crab() -> None:
    keV = Kilo * ElectronVolt
    cm = Centi * Meter
    s = Second

    assert 1 * Crab == 2.4e-8 * Erg / (cm**2 * s)
    assert 1 * Crab == approximately(15 * keV / (cm**2 * s), within=1e-2)


def test_hubble_constant() -> None:
    assert H0 == approximately(((67400 * Meter) / (1000000 * Parsec)) / Second)


def test_hubble_time() -> None:
    assert 1 * HubbleTime == approximately(14.4e9 * JulianYear, within=0.008)


def test_hubble_length() -> None:
    assert 1 * HubbleLength == approximately(14.4e9 * LightYear, within=0.008)


def test_hubble_volume() -> None:
    assert 1 * HubbleVolume == approximately(1e79 * Meter**3, within=0.09)
    assert 1 * HubbleVolume == approximately(1e31 * LightYear**3, within=0.28)


def test_hubble_barn() -> None:
    assert 1 * HubbleLength * Barn == approximately(13.1 * Liter, within=0.05)
