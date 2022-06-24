"""
Defines units and constants of use in the field of astronomy, which requires measuring
extremely large distances, masses, and periods of time.

> The [astronomical system of units][1] is a tridimensional system, in that it defines
> units of length, mass and time.  The associated astronomical constants also fix the
> different frames of reference that are needed to report observations.

[1]: https://en.wikipedia.org/wiki/Astronomical_system_of_units

Attributes: Units of length

    AstronomicalUnit (Unit): A unit representing the average distance between the Earth
        and the Sun; it is now defined precisely as 149,597,870,700 meters

    LightYear (Unit): the distance light travels through a vacuum in one `JulianYear`

    Parsec (Unit): A measure of large astronomical distances defined in terms of
        [trigonometry and parallax][1]

        [1]: https://en.wikipedia.org/wiki/Parsec

Attributes: Units of time

    Day (Unit): Uses the same definition of `Day` as the SI system

    JulianYear (Unit): defined as 365.25 days

Attributes: Units of mass

    SolarMass (Unit): The mass of the Sun

    EarthMass (Unit): The mass of the Earth

    JupiterMass (Unit): The mass of Jupiter
"""

from math import pi as π

from measured import Length, Mass, Time, Unit, si
from measured.fundamental import SpeedOfLight
from measured.si import Kilogram, Meter, Second

# Measures of Time

Day = Unit.derive(si.Day, name="day", symbol="D")

JulianYear = Time.unit("Julian year", "a")
JulianYear.equals(365.25 * Day)

# Measures of Length

AstronomicalUnit = Length.unit("astronomical unit", "AU")
AstronomicalUnit.equals(149597870700 * Meter)

# https://en.wikipedia.org/wiki/Light-year
LightYear = Length.unit("light-year", "ly")
LightYear.equals(SpeedOfLight * (1 * JulianYear).in_unit(Second))

# https://en.wikipedia.org/wiki/Parsec#Calculating_the_value_of_a_parsec
Parsec = Length.unit("parsec", "pc")
Parsec.equals(96939420213600600 / π * Meter)

# Measures of Mass

# https://en.wikipedia.org/wiki/Solar_mass
SolarMass = Mass.unit("solar mass", "M☉")
SolarMass.equals(1.98847e30 * Kilogram)

EarthMass = Mass.unit("earth mass", "M-earth")
EarthMass.equals(5.9722e24 * Kilogram)

JupiterMass = Mass.unit("jupiter mass", "M-jup")
JupiterMass.equals(1.89813e27 * Kilogram)
