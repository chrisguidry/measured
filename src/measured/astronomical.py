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

    LightYear (Unit): The distance light travels through a vacuum in one `JulianYear`

    Spat (Unit): An obsolete unit of astronomical distance equaling 1 trillion meters

    Parsec (Unit): A measure of large astronomical distances defined in terms of
        [trigonometry and parallax][1]

        [1]: https://en.wikipedia.org/wiki/Parsec

    Siriometer (Unit): An obsolete unit of astronomical distance equaling 1 million AU

Attributes: Units of time

    Day (Unit): Uses the same definition of `Day` as the SI system

    SiderealDay (Unit): The `Time` it takes the Earth to make one rotation with respect
        to distant stars, approximately 86164.0905 seconds, a few minutes shorter than
        the SI Day.

    JulianYear (Unit): defined as 365.25 days of 84,600 SI `Second`

Attributes: Units of mass

    SolarMass (Unit): The mass of the Sun

    EarthMass (Unit): The mass of the Earth

    JupiterMass (Unit): The mass of Jupiter

Attributes: Units for astrophotometry

    Jansky (Unit): A unit of spectral flux density

    Crab (Unit): A unit for measuring the intensity of astromonical X-ray sources, based
        on the intensity of the Crab Nebula

Attributes: Hubble's Law

    H0 (Quantity): Today's estimate of the Hubble Parameter representing the observed
        expansion rate of the universe

    HubbleTime (Unit): An approximation of the age of the universe, if the expansion
        rate had been linear

    HubbleLength (Unit): The distance at which galaxies are receding from us at the
        speed of light

    HubbleVolume (Unit): The sphere within which galaxies are receding from us below
        the speed of light

"""

from measured import Area, Length, Mass, Power, Time, Volume, si
from measured.geometry import π
from measured.physics import c
from measured.si import Kilogram, Mega, Meter, Second, Watt

# Measures of Time

Day = si.Day

# https://en.wikipedia.org/wiki/Sidereal_day
SiderealDay = Time.unit("sidereal day", "SD")
SiderealDay.equals(86164.0905 * Second)

# https://en.wikipedia.org/wiki/Julian_year_(astronomy)
JulianYear = Time.unit("Julian year", "a")
JulianYear.equals(365.25 * Day)


# Measures of Length

AstronomicalUnit = Length.unit("astronomical unit", "AU")
AstronomicalUnit.equals(149597870700 * Meter)

# https://en.wikipedia.org/wiki/Light-year
LightYear = Length.unit("light-year", "ly")
LightYear.equals((c * JulianYear).in_unit(Meter))

# https://en.wikipedia.org/wiki/Spat_(distance_unit)
Spat = Length.unit("spat", "spat")
Spat.equals(1e12 * Meter)

# https://en.wikipedia.org/wiki/Parsec#Calculating_the_value_of_a_parsec
Parsec = Length.unit("parsec", "pc")
Parsec.equals(96939420213600600 / π * Meter)

# https://en.wikipedia.org/wiki/Siriometer
Siriometer = Length.unit("seriometer", "sir")
Siriometer.equals(1000000 * AstronomicalUnit)


# Measures of Mass

# https://en.wikipedia.org/wiki/Solar_mass
SolarMass = Mass.unit("solar mass", "M☉")
SolarMass.equals(1.98847e30 * Kilogram)

EarthMass = Mass.unit("earth mass", "M-earth")
EarthMass.equals(5.9722e24 * Kilogram)

JupiterMass = Mass.unit("jupiter mass", "M-jup")
JupiterMass.equals(1.89813e27 * Kilogram)


# Derived

# https://en.wikipedia.org/wiki/Jansky
Jansky = (Power * Time / Area).unit("jansky", "Jy")
Jansky.equals(1e-26 * Watt * Second / Meter**2)

# https://en.wikipedia.org/wiki/Crab_(unit)
Crab = (Power / Area).unit("crab", "crab")
Crab.equals(2.4e-11 * Watt / Meter**2)


# Hubble's Law

# https://en.wikipedia.org/wiki/Hubble%27s_law#Time-dependence_of_Hubble_parameter
# H0 is today's value of the Hubble parameter
H0 = 67400 * ((Meter / Second) / (Mega * Parsec))

# https://en.wikipedia.org/wiki/Hubble%27s_law#Units_derived_from_the_Hubble_constant
HubbleTime = Time.unit("hubble time", "hubble-time")
HubbleTime.equals(H0**-1)
HubbleTime.equals((H0**-1).in_unit(Second))

HubbleLength = Length.unit("hubble length", "hubble-length")
HubbleLength.equals(c / H0)
HubbleLength.equals(c * HubbleTime)

HubbleVolume = Volume.unit("hubble volume", "hubble-volume")
HubbleVolume.equals(4 / 3 * π * (1 * HubbleLength) ** 3)
