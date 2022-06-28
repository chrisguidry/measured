"""
Defines the [International System of Units][1] ("SI") and [prefixes][2].

[1]: https://en.wikipedia.org/wiki/International_System_of_Units

[2]: https://en.wikipedia.org/wiki/Metric_prefix

Attributes: Base units

    Meter (Unit): The distance travelled by light in a vacuum in 1/299792458 seconds.

    Second (Unit): The duration of 9192631770 periods of the radiation corresponding to
        the transition between the two hyperfine levels of the ground state of the
        caesium-133 atom.

    Gram (Unit): The kilogram is defined by setting the Planck constant _h_ exactly
        to 6.62607015×10⁻³⁴ J⋅s (J = kg⋅m²⋅s⁻²), given the definitions of the metre
        and the second.  Note that `measured` uses `Gram` as the base unit, for
        simplicity.

    Ampere (Unit): The flow of exactly 1/1.602176634×10⁻¹⁹ times the elementary charge
        _e_ per second.

    Kelvin (Unit): The kelvin is defined by setting the fixed numerical value of the
        Boltzmann constant _k_ to 1.380649×10⁻²3 J⋅K⁻¹, (J = kg⋅m²⋅s⁻²), given the
        definition of the kilogram, the metre, and the second.

    Mole (Unit): The amount of substance of exactly 6.02214076×10²³ elementary entities.

    Candela (Unit): The luminous intensity, in a given direction, of a source that emits
        monochromatic radiation of frequency 5.4×10¹⁴ hertz and that has a radiant
        intensity in that direction of 1/683 watt per steradian.

Attributes: Derived units

    Hertz (Unit): measures `Frequency`

    Radian (Unit): measures `PlaneAngle`, a dimensionless `Number`

    Steradian (Unit): measures `SolidAngle`, a dimensionless `Number`

    Newton (Unit): measures `Force`
    Joule (Unit): measures `Energy`
    Watt (Unit): measures `Power`

    Coulomb (Unit): measures `Charge`
    Volt (Unit): measures `Potential`
    Farad (Unit): measures `Capacitance`
    Ohm (Unit): measures `Resistance`
    Siemens (Unit): measures `Conductance`
    Henry (Unit): measures `Inductance`

    Weber (Unit): measures `MagneticFlux`
    Tesla (Unit): measures `MagneticBField`

    Lumen (Unit): measures `LuminousFlux`
    Lux (Unit): measures `Illuminance`

    Becquerel (Unit): Radioactive decays per unit time (alias for `Hertz`)
    Gray (Unit): absorbed dose of ionizing radiation (measures `RadioactiveDose`)
    Sievert (Unit): equivalent dose of ionizing radiation (measures `RadioactiveDose`)

    Katal (Unit): measures `Catalysis`


Attributes: Prefixes (base 10)

    Yotta (Prefix): 10 ²⁴, symbol `Y`
    Zetta (Prefix): 10²¹, symbol `Z`
    Exa (Prefix): 10¹⁸, symbol `E`
    Peta (Prefix): 10¹⁵, symbol `P`
    Tera (Prefix): 10¹², symbol `T`
    Giga (Prefix): 10⁹, symbol `G`
    Mega (Prefix): 10⁶, symbol `M`
    Kilo (Prefix): 10³, symbol `k`
    Hecto (Prefix): 10 ², symbol `h`
    Deca (Prefix): 10¹, symbol `d`
    Deci (Prefix): 10⁻¹, symbol `d`
    Centi (Prefix): 10⁻², symbol `c`
    Milli (Prefix): 10⁻³, symbol `m`
    Micro (Prefix): 10⁻⁶, symbol `μ`
    Nano (Prefix): 10⁻⁹, symbol `n`
    Pico (Prefix): 10⁻¹², symbol `p`
    Femto (Prefix): 10⁻¹⁵, symbol `f`
    Atto (Prefix): 10⁻¹⁸, symbol `a`
    Zepto (Prefix): 10⁻²¹, symbol `z`
    Yocto (Prefix): 10⁻²⁴, symbol `y`

"""

from math import pi as π

from . import (
    AmountOfSubstance,
    Current,
    Length,
    LuminousIntensity,
    Mass,
    One,
    PlaneAngle,
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

Meter = Length.unit(name="meter", symbol="m")
Second = Time.unit(name="second", symbol="s")
Gram = Mass.unit(name="gram", symbol="g")
Ampere = Current.unit(name="ampere", symbol="A")
Kelvin = Temperature.unit(name="kelvin", symbol="K")
Mole = AmountOfSubstance.unit(name="mole", symbol="mol")
Candela = LuminousIntensity.unit(name="candela", symbol="cd")

# Technically, it's the kilogram that's the SI base unit, and the other derived units
# are derived in terms of the kilogram.
Kilogram = Mass.unit("kilogram", "kg")
Kilogram.equals(1000 * Gram)


# Derived Units
# https://en.wikipedia.org/wiki/SI_derived_unit

Hertz = Unit.derive(One / Second, name="hertz", symbol="Hz")

Radian = PlaneAngle.unit(name="radian", symbol="rad")
Steradian = PlaneAngle.unit(name="steradian", symbol="sr")

Newton = Unit.derive((Kilogram) * Meter / Second**2, name="newton", symbol="N")
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

Celsius = Temperature.unit(name="celsius", symbol="°C")
Celsius.alias(symbol="degC")
Celsius.zero(273.15 * Kelvin)

Lumen = Unit.derive(Candela * Steradian, name="lumen", symbol="lm")
Lux = Unit.derive(Lumen / Meter**2, name="lux", symbol="lux")

Becquerel = Hertz
Gray = Unit.derive(Joule / (Kilo * Gram), name="gray", symbol="Gy")
Sievert = Unit.derive(Joule / (Kilo * Gram), name="sievert", symbol="Sv")

Katal = Unit.derive(Mole / Second, name="katal", symbol="kat")


# SI Accepted units
# https://en.wikipedia.org/wiki/Non-SI_units_mentioned_in_the_SI

Liter = Unit.derive((Deci * Meter) ** 3, name="liter", symbol="L")

Minute = Time.unit("minute", "min")
Minute.equals(60 * Second)

Hour = Time.unit("hour", "h")
Hour.equals(3600 * Second)
Hour.equals(60 * Minute)

# This is the SI-compatible "day" as a unit of measure, defined as 86,400 seconds.
# https://en.wikipedia.org/wiki/Day#International_System_of_Units_(SI)
Day = Time.unit("day", "d")
Day.equals(86400 * Second)
Day.equals(1440 * Minute)
Day.equals(24 * Hour)

Degree = PlaneAngle.unit("degree", "°")
Degree.alias(symbol="deg")
Degree.equals(π / 180 * Radian)

Arcminute = PlaneAngle.unit("arcminute", "arcmin")
Arcminute.equals(π / 10800 * Radian)
Arcminute.equals(1 / 60 * Degree)

Arcsecond = PlaneAngle.unit("arcsecond", "arcsec")
Arcsecond.equals(π / (180 * 3600) * Radian)
Arcsecond.equals(1 / 3600 * Degree)
Arcsecond.equals(1 / 60 * Arcminute)
