from . import (
    AmountOfSubstance,
    Current,
    Length,
    LuminousIntensity,
    Mass,
    One,
    Temperature,
    Time,
    Unit,
)

# https://en.wikipedia.org/wiki/International_System_of_Units

# https://en.wikipedia.org/wiki/SI_base_unit

Meter = Unit.define(Length, name="meter", symbol="m")
Second = Unit.define(Time, name="second", symbol="s")
Gram = Unit.define(Mass, name="gram", symbol="g")
Ampere = Unit.define(Current, name="ampere", symbol="A")
Kelvin = Unit.define(Temperature, name="kelvin", symbol="K")
Mole = Unit.define(AmountOfSubstance, name="mole", symbol="mol")
Candela = Unit.define(LuminousIntensity, name="candela", symbol="cd")

# https://en.wikipedia.org/wiki/SI_derived_unit

Hertz = Unit.derive(One / Second, name="hertz", symbol="Hz")
