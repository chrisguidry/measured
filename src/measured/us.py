"""
Defines the [United States customary units][1] and their conversions to SI

[1]: https://en.wikipedia.org/wiki/United_States_customary_units
"""

from . import Area, Length, Mass, Volume, avoirdupois
from .si import Gram, Kilo, Liter, Meter, Micro, Milli

# Length
# https://en.wikipedia.org/wiki/United_States_customary_units#Length

Point = Length.unit(name="point", symbol="p.")
Point.equals(127 / 360 * Milli * Meter)

Pica = Length.unit(name="pica", symbol="P.")
Pica.equals(12 * Point)
Pica.equals(127 / 30 * Milli * Meter)

Inch = Length.unit(name="inch", symbol="in.")
Inch.equals(6 * Pica)
Inch.equals(25.4 * Milli * Meter)

Foot = Length.unit(name="foot", symbol="ft.")
Foot.equals(12 * Inch)
Foot.equals(0.3048 * Meter)

Yard = Length.unit(name="yard", symbol="yd.")
Yard.equals(3 * Foot)
Yard.equals(36 * Inch)
Yard.equals(0.9144 * Meter)

Mile = Length.unit(name="mile", symbol="mi.")
Mile.equals(5280 * Foot)
Mile.equals(1760 * Yard)
Mile.equals(1.609344 * Kilo * Meter)

# US Survey Units

Link = Length.unit(name="link", symbol="li.")
Link.equals(7.92 * Inch)
Link.equals(33 / 50 * Foot)
Link.equals(792 / 3937 * Meter)

SurveyFoot = Length.unit(name="US survey foot", symbol="US survey foot")
SurveyFoot.equals(1200 / 3937 * Meter)
SurveyFoot.equals(1.000002 * Foot)

Rod = Length.unit(name="rod", symbol="rd.")
Rod.equals(25 * Link)
Rod.equals(16.5 * SurveyFoot)
Rod.equals(19800 / 3937 * Meter)

Chain = Length.unit(name="chain", symbol="ch.")
Chain.equals(4 * Rod)
Chain.equals(66 * SurveyFoot)
Chain.equals(79200 / 3937 * Meter)

Furlong = Length.unit(name="furlong", symbol="fur.")
Furlong.equals(10 * Chain)
Furlong.equals(792 / 3937 * Kilo * Meter)

StatuteMile = Length.unit(name="US statute mile", symbol="US statute mile")
StatuteMile.equals(8 * Furlong)
StatuteMile.equals(6336 / 3937 * Kilo * Meter)

League = Length.unit(name="league", symbol="lea.")
League.equals(3 * StatuteMile)
League.equals(19008 / 3937 * Kilo * Meter)

# Nautical Units

Fathom = Length.unit(name="fathom", symbol="ftm.")
Fathom.equals(2 * Yard)
Fathom.equals(6 * Foot)
Fathom.equals(1143 / 625 * Meter)

Cable = Length.unit(name="cable", symbol="cb.")
Cable.equals(120 * Fathom)
Cable.equals(3429 / 15625 * Kilo * Meter)

NauticalMile = Length.unit(name="nautical mile", symbol="nmi.")
NauticalMile.equals(1852 * Meter)


# Area
# https://en.wikipedia.org/wiki/United_States_customary_units#Area

Acre = Area.unit(name="acre", symbol="acre")
Acre.equals(43560 * Foot**2)
Acre.equals(10 * Chain**2)

Section = Area.unit(name="section", symbol="section")
Section.equals(640 * Acre)
Section.equals(1 * StatuteMile**2)

SurveyTownship = Area.unit(name="survey township", symbol="twp.")
SurveyTownship.equals(36 * Section)
SurveyTownship.equals(4 * League**2)


# Volume
# https://en.wikipedia.org/wiki/United_States_customary_units#Volume

AcreFoot = Volume.unit(name="acre-foot", symbol="acre-ft.")
AcreFoot.equals(43560 * Foot**3)

# Fluid Volumes
# https://en.wikipedia.org/wiki/United_States_customary_units#Fluid_volume

Minim = Volume.unit(name="minim", symbol="min")
Minim.equals(61.611519921875 * Micro * Liter)

FluidDram = Volume.unit(name="fluid dram", symbol="fl. dr.")
FluidDram.equals(60 * Minim)
FluidDram.equals(3.6966911953125 * Milli * Liter)

Teaspoon = Volume.unit(name="teaspoon", symbol="tsp.")
Teaspoon.equals(80 * Minim)
Teaspoon.equals(4.92892159375 * Milli * Liter)

Tablespoon = Volume.unit(name="tablespoon", symbol="tbsp.")
Tablespoon.equals(3 * Teaspoon)
Tablespoon.equals(4 * FluidDram)
Tablespoon.equals(14.78676478125 * Milli * Liter)

FluidOunce = Volume.unit(name="fluid ounce", symbol="fl. oz.")
FluidOunce.equals(2 * Tablespoon)
FluidOunce.equals(29.5735295625 * Milli * Liter)

Shot = Volume.unit(name="shot", symbol="jig.")
Shot.equals(1.5 * FluidOunce)
Shot.equals(3 * Tablespoon)
Shot.equals(44.36029434375 * Milli * Liter)

Gill = Volume.unit(name="gill", symbol="gi.")
Gill.equals(8 / 3 * Shot)
Gill.equals(4 * FluidOunce)
Gill.equals(118.29411825 * Milli * Liter)

Cup = Volume.unit(name="cup", symbol="c.")
Cup.equals(2 * Gill)
Cup.equals(8 * FluidOunce)
Cup.equals(236.5882365 * Milli * Liter)

Pint = Volume.unit(name="pint", symbol="pt.")
Pint.equals(2 * Cup)
Pint.equals(473.176473 * Milli * Liter)

Quart = Volume.unit(name="quart", symbol="qt.")
Quart.equals(2 * Pint)
Quart.equals(0.946352946 * Liter)

Pottle = Volume.unit(name="pottle", symbol="pot.")
Pottle.equals(2 * Quart)
Pottle.equals(1.892705892 * Liter)

Gallon = Volume.unit(name="gallon", symbol="gal.")
Gallon.equals(4 * Quart)
Gallon.equals(231 * Inch**3)
Gallon.equals(3.785411784 * Liter)

Barrel = Volume.unit(name="barrel", symbol="bbl.")
Barrel.equals(42 * Gallon)
Barrel.equals(158.987294928 * Liter)

Hogshead = Volume.unit(name="hogshead", symbol="hogshead")
Hogshead.equals(1.5 * Barrel)
Hogshead.equals(63 * Gallon)
Hogshead.equals(8.421875 * Foot**3)
Hogshead.equals(238.480942392 * Liter)

# Dry Volumes
# https://en.wikipedia.org/wiki/United_States_customary_units#Dry_volume

DryPint = Volume.unit(name="dry pint", symbol="dry pint")
DryPint.equals(33.6003125 * Inch**3)
DryPint.equals(0.5506104713575 * Liter)

DryQuart = Volume.unit(name="dry quart", symbol="dry quart")
DryQuart.equals(2 * DryPint)

DryGallon = Volume.unit(name="dry gallon", symbol="dry gallon")
DryGallon.equals(2 * DryQuart)

Peck = Volume.unit(name="peck", symbol="pk.")
Peck.equals(2 * DryGallon)

Bushel = Volume.unit(name="bushel", symbol="bu.")
Bushel.equals(4 * Peck)
Bushel.equals(35.23907016688 * Liter)

DryBarrel = Volume.unit(name="dry barrel", symbol="dry barrel")
DryBarrel.equals(7056 * Inch**3)


# Mass
# https://en.wikipedia.org/wiki/United_States_customary_units#Mass_and_weight

# The US uses the avoirdupois system of masses, with some adjustments
Dram = avoirdupois.Dram
Grain = avoirdupois.Grain
Ounce = avoirdupois.Ounce
Pound = avoirdupois.Pound

Hundredweight = Mass.unit("US hundredweight", "cwt.")
Hundredweight.equals(100 * Pound)
Hundredweight.equals(45.359237 * Kilo * Gram)

Ton = Mass.unit("short ton", "ton")
Ton.equals(20 * Hundredweight)
Ton.equals(907.18474 * Kilo * Gram)
