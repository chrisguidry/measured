"""
Units and non-standardized conventions for representing `Energy` and `Power`.

Attributes: Units of Energy

    Erg (Unit):

    Calorie (Unit):

    BritishThermalUnit (Unit):

    TonOfRefrigeration (Unit):

    TonneOfTNT (Unit):


Attributes: Units of Power

    Horsepower (Unit):

    Donkeypower (Unit):

    MetricHorsepower (Unit):

    ElectricalHorsepower (Unit):

    BoilerHorsepower (Unit):


Attributes: Other units

    Langley (Unit): A unit of heat transmission (`Energy/Area`), often used to express
        insolation (the amount of solar energy reaching the surface of the Earth)

"""

from measured import Area, Energy, Power
from measured.si import Hour, Joule, Kilo, Meter, Second, Watt
from measured.us import Foot, PoundForce

# https://en.wikipedia.org/wiki/Erg
Erg = Energy.unit(name="erg", symbol="erg")
Erg.equals(1e-7 * Joule)

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


# https://en.wikipedia.org/wiki/Horsepower#Definitions
Horsepower = Power.unit("horsepower", "hp")
Horsepower.equals(550 * Foot * PoundForce / Second)

Donkeypower = Power.unit("donkeypower", "donkeypower")
Donkeypower.equals(1 / 3 * Horsepower)

MetricHorsepower = Power.unit("metric horsepower", "hp(M)")
MetricHorsepower.equals(735.49875 * Watt)

ElectricalHorsepower = Power.unit("electrical horsepower", "hp(E)")
ElectricalHorsepower.equals(746 * Watt)

BoilerHorsepower = Power.unit("boiler horsepower", "hp(S)")
BoilerHorsepower.equals(33475 * BritishThermalUnit / Hour)


# https://en.wikipedia.org/wiki/Langley_(unit)
Langley = (Energy / Area).unit("langley", "Ly")
Langley.equals(41840 * Joule / Meter**2)
