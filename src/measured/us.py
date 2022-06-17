"""
Defines the [United States customary units][1] and their conversions to SI

[1]: https://en.wikipedia.org/wiki/United_States_customary_units
"""

from . import Length, Unit, conversions
from .si import Kilo, Meter, Milli

# https://en.wikipedia.org/wiki/United_States_customary_units#Length

Point = Unit.define(Length, "point", "p.")
conversions.equate(1 * Point, 127 / 360 * Milli * Meter)

Pica = Unit.define(Length, "pica", "P.")
conversions.equate(1 * Pica, 12 * Point)

Inch = Unit.define(Length, "inch", "in.")
conversions.equate(1 * Inch, 6 * Pica)

Foot = Unit.define(Length, "foot", "ft.")
conversions.equate(1 * Foot, 12 * Inch)
conversions.equate(1 * Foot, 0.3048 * Meter)

Yard = Unit.define(Length, "yard", "yd.")
conversions.equate(1 * Yard, 3 * Foot)
conversions.equate(1 * Yard, 0.9144 * Meter)

Mile = Unit.define(Length, "mile", "mi.")
conversions.equate(1 * Mile, 1760 * Yard)
conversions.equate(1 * Mile, 1.609344 * Kilo * Meter)

# US Survey Units

Link = Unit.define(Length, "link", "li.")
conversions.equate(1 * Link, 7.92 * Inch)
conversions.equate(1 * Link, 792 / 3937 * Meter)

SurveyFoot = Unit.define(Length, "US survey foot", "US survey foot")
conversions.equate(1 * SurveyFoot, 1200 / 3937 * Meter)

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
conversions.equate(1 * StatuteMile, 8 * StatuteMile)
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
conversions.equate(1 * Cable, 1.091 * Furlong)
conversions.equate(1 * Cable, 3429 / 15625 * Kilo * Meter)

NauticalMile = Unit.define(Length, "nautical mile", "nmi.")
conversions.equate(1 * NauticalMile, 1.151 * Mile)
conversions.equate(1 * NauticalMile, 8.439 * Cable)
conversions.equate(1 * NauticalMile, 1.852 * Kilo * Meter)
