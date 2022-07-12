from measured import Area, Energy, Power
from measured.si import Hour, Joule, Kilo, Meter, Watt

# https://en.wikipedia.org/wiki/Calorie
Calorie = Energy.unit(name="calorie", symbol="cal")
Calorie.equals(4.184 * Joule)

# https://en.wikipedia.org/wiki/British_thermal_unit#Definitions
BritishThermalUnit = Energy.unit(name="British thermal unit", symbol="BTU")
BritishThermalUnit.equals(1054.350264488889 * Joule)

# https://en.wikipedia.org/wiki/Ton_of_refrigeration
TonOfRefrigeration = Power.unit(name="ton of refrigeration", symbol="TR")
TonOfRefrigeration.equals(12000 * BritishThermalUnit / Hour)
TonOfRefrigeration.equals(3.51685 * Kilo * Watt)

# https://en.wikipedia.org/wiki/TNT_equivalent
TonneOfTNT = Energy.unit(name="ton of TNT", symbol="tₜₙₜ")
TonneOfTNT.equals(4.184e9 * Joule)
TonneOfTNT.equals(1e9 * Calorie)

# https://en.wikipedia.org/wiki/Langley_(unit)
Langley = (Energy / Area).unit("langley", "Ly")
Langley.equals(41840 * Joule / Meter**2)
