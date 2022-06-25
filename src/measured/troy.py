"""
Defines the [Troy weights][1] and their conversions to SI

[1]: https://en.wikipedia.org/wiki/Troy_weight

Attributes: Units of mass ("weight")

    Grain (Unit): The same `Grain` as the Avoirdupois system

    Pennyweight (Unit): 24 grains

    Ounce (Unit): 20 troy pennyweights

    Pound (Unit): 12 troy ounces

"""

from measured import Mass, avoirdupois
from measured.si import Gram

# https://en.wikipedia.org/wiki/Troy_weight#Troy_grain
# There is no specific 'troy grain'. All Imperial systems use the same measure of mass
# called a grain
Grain = avoirdupois.Grain

Pennyweight = Mass.unit("pennyweight", "dwt")
Pennyweight.equals(24 * Grain)

Ounce = Mass.unit("troy ounce", "oz t")
Ounce.equals(480 * Grain)
Ounce.equals(20 * Pennyweight)
Ounce.equals(31.10348 * Gram)

Pound = Mass.unit("troy pound", "lb t")
Pound.equals(12 * Ounce)
Pound.equals(240 * Pennyweight)
Pound.equals(373.24172 * Gram)
