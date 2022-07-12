from measured import Energy
from measured.si import Joule

# https://en.wikipedia.org/wiki/Calorie
Calorie = Energy.unit(name="calorie", symbol="cal")
Calorie.equals(4.184 * Joule)

# https://en.wikipedia.org/wiki/British_thermal_unit#Definitions
BritishThermalUnit = Energy.unit(name="British thermal unit", symbol="BTU")
BritishThermalUnit.equals(1054.350264488889 * Joule)

# https://en.wikipedia.org/wiki/TNT_equivalent
TonneOfTNT = Energy.unit(name="ton of TNT", symbol="tₜₙₜ")
TonneOfTNT.equals(4.184e9 * Joule)
TonneOfTNT.equals(1e9 * Calorie)
