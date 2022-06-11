from . import (
    AmountOfSubstance,
    Current,
    Length,
    LuminousIntensity,
    Mass,
    One,
    Prefix,
    Temperature,
    Time,
    Unit,
)

# https://en.wikipedia.org/wiki/Metric_prefix

Yotta = Prefix(10, 24, name="yotta", symbol="Y")
Zetta = Prefix(10, 21, name="zetta", symbol="Z")
Exa = Prefix(10, 18, name="exa", symbol="E")
Peta = Prefix(10, 15, name="peta", symbol="P")
Tera = Prefix(10, 12, name="tera", symbol="T")
Giga = Prefix(10, 9, name="giga", symbol="G")
Mega = Prefix(10, 6, name="mega", symbol="M")
Kilo = Prefix(10, 3, name="kilo", symbol="k")
Hecto = Prefix(10, 2, name="hecto", symbol="h")
Deca = Prefix(10, 1, name="deca", symbol="d")
Deci = Prefix(10, -1, name="deci", symbol="d")
Centi = Prefix(10, -2, name="centi", symbol="c")
Milli = Prefix(10, -3, name="milli", symbol="m")
Micro = Prefix(10, -6, name="micro", symbol="μ")
Nano = Prefix(10, -9, name="nano", symbol="n")
Pico = Prefix(10, -12, name="pico", symbol="p")
Femto = Prefix(10, -15, name="femto", symbol="f")
Atto = Prefix(10, -18, name="atto", symbol="a")
Zepto = Prefix(10, -21, name="zepto", symbol="z")
Yocto = Prefix(10, -24, name="yocto", symbol="y")


#
# https://en.wikipedia.org/wiki/International_System_of_Units
#


# Base Units
# https://en.wikipedia.org/wiki/SI_base_unit

Meter = Unit.define(Length, name="meter", symbol="m")
Second = Unit.define(Time, name="second", symbol="s")
Gram = Unit.define(Mass, name="gram", symbol="g")
Ampere = Unit.define(Current, name="ampere", symbol="A")
Kelvin = Unit.define(Temperature, name="kelvin", symbol="K")
Mole = Unit.define(AmountOfSubstance, name="mole", symbol="mol")
Candela = Unit.define(LuminousIntensity, name="candela", symbol="cd")


# Derived Units
# https://en.wikipedia.org/wiki/SI_derived_unit

Hertz = Unit.derive(One / Second, name="hertz", symbol="Hz")

Radian = Unit.derive(Meter / Meter, name="radian", symbol="rad")
Steradian = Unit.derive(Meter**2 / Meter**2, name="steradian", symbol="sr")

Newton = Unit.derive((Kilo * Gram) * Meter / Second**2, name="newton", symbol="N")
Joule = Unit.derive(Meter * Newton, name="joule", symbol="J")
Watt = Unit.derive(Joule / Second, name="watt", symbol="W")

Coulomb = Unit.derive(Second * Ampere, name="coulomb", symbol="C")
Volt = Unit.derive(Watt / Ampere, name="volt", symbol="V")
Farad = Unit.derive(Coulomb / Volt, name="farad", symbol="F")
Ohm = Unit.derive(Volt / Ampere, name="ohm", symbol="Ω")
Siemens = Unit.derive(Ampere / Volt, name="siemens", symbol="S")
Henry = Unit.derive(Ohm * Second, name="henry", symbol="H")

Weber = Unit.derive(Joule / Ampere, name="weber", symbol="Wb")
Tesla = Unit.derive(Weber / Meter**2, name="tesla", symbol="T")

# Celsius = Kelvin.translate(273.15)

Lumen = Unit.derive(Candela * Steradian, name="lumen", symbol="lm")
Lux = Unit.derive(Lumen / Meter**2, name="lux", symbol="lux")

Becquerel = Hertz
Gray = Unit.derive(Joule / (Kilo * Gram), name="gray", symbol="Gy")
Sievert = Unit.derive(Joule / (Kilo * Gram), name="sievert", symbol="Sv")

Katal = Unit.derive(Mole / Second, name="katal", symbol="kat")
