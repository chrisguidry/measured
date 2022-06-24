# https://en.wikipedia.org/wiki/Astronomical_system_of_units

from math import pi as π

from measured import Length, Mass, Time
from measured.constants import SpeedOfLight
from measured.si import Day, Kilogram, Meter, Second

JulianYear = Time.unit("Julian year", "a")
JulianYear.equals(365.25 * Day)

AstronomicalUnit = Length.unit("astronomical unit", "AU")
AstronomicalUnit.equals(149597870700 * Meter)

# https://en.wikipedia.org/wiki/Parsec#Calculating_the_value_of_a_parsec
Parsec = Length.unit("parsec", "pc")
Parsec.equals(96939420213600600 / π * Meter)

# https://en.wikipedia.org/wiki/Light-year
LightYear = Length.unit("light-year", "ly")
LightYear.equals(SpeedOfLight * (1 * JulianYear).in_unit(Second))

# https://en.wikipedia.org/wiki/Solar_mass
SolarMass = Mass.unit("solar mass", "M☉")
SolarMass.equals(1.98847e30 * Kilogram)

EarthMass = Mass.unit("earth mass", "M-earth")
EarthMass.equals(5.9722e24 * Kilogram)

JupiterMass = Mass.unit("jupiter mass", "M-jup")
JupiterMass.equals(1.89813e27 * Kilogram)
