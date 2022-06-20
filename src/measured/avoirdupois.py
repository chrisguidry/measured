# https://en.wikipedia.org/wiki/Avoirdupois_system

from measured import Mass
from measured.si import Gram, Kilo, Milli

Grain = Mass.unit("grain", "gr.")
Grain.equals(64.79891 * Milli * Gram)

Dram = Mass.unit("dram", "dr.")
Dram.equals((27 + (11 / 32)) * Grain)
Dram.equals(1.7718451953125 * Gram)

Ounce = Mass.unit("ounce", "oz")
Ounce.equals(16 * Dram)
Ounce.equals(28.349523125 * Gram)

Pound = Mass.unit("pound", "lb.")
Pound.equals(16 * Ounce)
Pound.equals(453.59237 * Gram)

LongHundredweight = Mass.unit("long hundredweight", "long hundredweight")
LongHundredweight.equals(112 * Pound)
LongHundredweight.equals(50.80234544 * Kilo * Gram)

LongTon = Mass.unit("long ton", "long ton")
LongTon.equals(20 * LongHundredweight)
LongTon.equals(2240 * Pound)
LongTon.equals(1016.0469088 * Kilo * Gram)
