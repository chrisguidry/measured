"""
Defines the [United States customary units][1] and their conversions to SI

[1]: https://en.wikipedia.org/wiki/United_States_customary_units
"""

from . import Area, Length, Unit, Volume, conversions
from .si import Kilo, Liter, Meter, Micro, Milli

# Length
# https://en.wikipedia.org/wiki/United_States_customary_units#Length

Point = Unit.define(Length, "point", "p.")
conversions.equate(1 * Point, 127 / 360 * Milli * Meter)

Pica = Unit.define(Length, "pica", "P.")
conversions.equate(1 * Pica, 12 * Point)
conversions.equate(1 * Pica, 127 / 30 * Milli * Meter)

Inch = Unit.define(Length, "inch", "in.")
conversions.equate(1 * Inch, 6 * Pica)
conversions.equate(1 * Inch, 25.4 * Milli * Meter)

Foot = Unit.define(Length, "foot", "ft.")
conversions.equate(1 * Foot, 12 * Inch)
conversions.equate(1 * Foot, 0.3048 * Meter)

Yard = Unit.define(Length, "yard", "yd.")
conversions.equate(1 * Yard, 3 * Foot)
conversions.equate(1 * Yard, 36 * Inch)
conversions.equate(1 * Yard, 0.9144 * Meter)

Mile = Unit.define(Length, "mile", "mi.")
conversions.equate(1 * Mile, 5280 * Foot)
conversions.equate(1 * Mile, 1760 * Yard)
conversions.equate(1 * Mile, 1.609344 * Kilo * Meter)

# US Survey Units

Link = Unit.define(Length, "link", "li.")
conversions.equate(1 * Link, 7.92 * Inch)
conversions.equate(1 * Link, 33 / 50 * Foot)
conversions.equate(1 * Link, 792 / 3937 * Meter)

SurveyFoot = Unit.define(Length, "US survey foot", "US survey foot")
conversions.equate(1 * SurveyFoot, 1200 / 3937 * Meter)
conversions.equate(1 * SurveyFoot, 1.000002 * Foot)

Rod = Unit.define(Length, "rod", "rd.")
conversions.equate(1 * Rod, 25 * Link)
conversions.equate(1 * Rod, 16.5 * SurveyFoot)
conversions.equate(1 * Rod, 19800 / 3937 * Meter)

Chain = Unit.define(Length, "chain", "ch.")
conversions.equate(1 * Chain, 4 * Rod)
conversions.equate(1 * Chain, 66 * SurveyFoot)
conversions.equate(1 * Chain, 79200 / 3937 * Meter)

Furlong = Unit.define(Length, "furlong", "fur.")
conversions.equate(1 * Furlong, 10 * Chain)
conversions.equate(1 * Furlong, 792 / 3937 * Kilo * Meter)

StatuteMile = Unit.define(Length, "US statute mile", "US statute mile")
conversions.equate(1 * StatuteMile, 8 * Furlong)
conversions.equate(1 * StatuteMile, 6336 / 3937 * Kilo * Meter)

League = Unit.define(Length, "league", "lea.")
conversions.equate(1 * League, 3 * StatuteMile)
conversions.equate(1 * League, 19008 / 3937 * Kilo * Meter)

# Nautical Units

Fathom = Unit.define(Length, "fathom", "ftm.")
conversions.equate(1 * Fathom, 2 * Yard)
conversions.equate(1 * Fathom, 6 * Foot)
conversions.equate(1 * Fathom, 1143 / 625 * Meter)

Cable = Unit.define(Length, "cable", "cb.")
conversions.equate(1 * Cable, 120 * Fathom)
conversions.equate(1 * Cable, 3429 / 15625 * Kilo * Meter)

NauticalMile = Unit.define(Length, "nautical mile", "nmi.")
conversions.equate(1 * NauticalMile, 1852 * Meter)


# Area
# https://en.wikipedia.org/wiki/United_States_customary_units#Area

Acre = Unit.define(Area, name="acre", symbol="acre")
conversions.equate(1 * Acre, 43560 * Foot**2)
conversions.equate(1 * Acre, 10 * Chain**2)

Section = Unit.define(Area, name="section", symbol="section")
conversions.equate(1 * Section, 640 * Acre)
conversions.equate(1 * Section, 1 * StatuteMile**2)

SurveyTownship = Unit.define(Area, name="survey township", symbol="twp.")
conversions.equate(1 * SurveyTownship, 36 * Section)
conversions.equate(1 * SurveyTownship, 4 * League**2)


# Volume
# https://en.wikipedia.org/wiki/United_States_customary_units#Volume

AcreFoot = Unit.define(Volume, name="acre-foot", symbol="acre-ft.")
conversions.equate(1 * AcreFoot, 43560 * Foot**3)

# Fluid Volumes
# https://en.wikipedia.org/wiki/United_States_customary_units#Fluid_volume

Minim = Unit.define(Volume, name="minim", symbol="min")
conversions.equate(1 * Minim, 61.611519921875 * Micro * Liter)

FluidDram = Unit.define(Volume, name="fluid dram", symbol="fl. dr.")
conversions.equate(1 * FluidDram, 60 * Minim)
conversions.equate(1 * FluidDram, 3.6966911953125 * Milli * Liter)

Teaspoon = Unit.define(Volume, name="teaspoon", symbol="tsp.")
conversions.equate(1 * Teaspoon, 80 * Minim)
conversions.equate(1 * Teaspoon, 4.92892159375 * Milli * Liter)

Tablespoon = Unit.define(Volume, name="tablespoon", symbol="tbsp.")
conversions.equate(1 * Tablespoon, 3 * Teaspoon)
conversions.equate(1 * Tablespoon, 4 * FluidDram)
conversions.equate(1 * Tablespoon, 14.78676478125 * Milli * Liter)

FluidOunce = Unit.define(Volume, name="fluid ounce", symbol="fl. oz.")
conversions.equate(1 * FluidOunce, 2 * Tablespoon)
conversions.equate(1 * FluidOunce, 29.5735295625 * Milli * Liter)

Shot = Unit.define(Volume, name="shot", symbol="jig.")
conversions.equate(1 * Shot, 1.5 * FluidOunce)
conversions.equate(1 * Shot, 3 * Tablespoon)
conversions.equate(1 * Shot, 44.36029434375 * Milli * Liter)

Gill = Unit.define(Volume, name="gill", symbol="gi.")
conversions.equate(1 * Gill, 8 / 3 * Shot)
conversions.equate(1 * Gill, 4 * FluidOunce)
conversions.equate(1 * Gill, 118.29411825 * Milli * Liter)

Cup = Unit.define(Volume, name="cup", symbol="c.")
conversions.equate(1 * Cup, 2 * Gill)
conversions.equate(1 * Cup, 8 * FluidOunce)
conversions.equate(1 * Cup, 236.5882365 * Milli * Liter)

Pint = Unit.define(Volume, name="pint", symbol="pt.")
conversions.equate(1 * Pint, 2 * Cup)
conversions.equate(1 * Pint, 473.176473 * Milli * Liter)

Quart = Unit.define(Volume, name="quart", symbol="qt.")
conversions.equate(1 * Quart, 2 * Pint)
conversions.equate(1 * Quart, 0.946352946 * Liter)

Pottle = Unit.define(Volume, name="pottle", symbol="pot.")
conversions.equate(1 * Pottle, 2 * Quart)
conversions.equate(1 * Pottle, 1.892705892 * Liter)

Gallon = Unit.define(Volume, name="gallon", symbol="gal.")
conversions.equate(1 * Gallon, 4 * Quart)
conversions.equate(1 * Gallon, 231 * Inch**3)
conversions.equate(1 * Gallon, 3.785411784 * Liter)

Barrel = Unit.define(Volume, name="barrel", symbol="bbl.")
conversions.equate(1 * Barrel, 42 * Gallon)
conversions.equate(1 * Barrel, 158.987294928 * Liter)

Hogshead = Unit.define(Volume, name="hogshead", symbol="hogshead")
conversions.equate(1 * Hogshead, 1.5 * Barrel)
conversions.equate(1 * Hogshead, 63 * Gallon)
conversions.equate(1 * Hogshead, 8.421875 * Foot**3)
conversions.equate(1 * Hogshead, 238.480942392 * Liter)

# Dry Volumes
# https://en.wikipedia.org/wiki/United_States_customary_units#Dry_volume

DryPint = Unit.define(Volume, name="dry pint", symbol="dry pint")
conversions.equate(1 * DryPint, 33.6003125 * Inch**3)
conversions.equate(1 * DryPint, 0.5506104713575 * Liter)

DryQuart = Unit.define(Volume, name="dry quart", symbol="dry quart")
conversions.equate(1 * DryQuart, 2 * DryPint)

DryGallon = Unit.define(Volume, name="dry gallon", symbol="dry gallon")
conversions.equate(1 * DryGallon, 2 * DryQuart)

Peck = Unit.define(Volume, name="peck", symbol="pk.")
conversions.equate(1 * Peck, 2 * DryGallon)

Bushel = Unit.define(Volume, name="bushel", symbol="bu.")
conversions.equate(1 * Bushel, 4 * Peck)
conversions.equate(1 * Bushel, 35.23907016688 * Liter)

DryBarrel = Unit.define(Volume, name="dry barrel", symbol="dry barrel")
conversions.equate(1 * DryBarrel, 7056 * Inch**3)
