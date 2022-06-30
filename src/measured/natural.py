# https://en.wikipedia.org/wiki/Natural_units

# https://en.wikipedia.org/wiki/Planck_units

from math import pi as π

from measured import Charge, Length, Mass, Temperature, Time
from measured.fundamental import G, c, e, k, mₑ, ε0, ℏ
from measured.si import Coulomb, Kilogram, Meter, Second

PlanckLength = Length.unit("planck length", "lₚ")
PlanckLength.equals(((ℏ * G) / c**3).root(2))

PlanckMass = Mass.unit("planck mass", "mₚ")
PlanckMass.equals(((ℏ * c) / G).root(2))

PlanckTime = Time.unit("planck time", "tₚ")
PlanckTime.equals(((ℏ * G) / c**5).root(2))

PlanckTemperature = Temperature.unit("planck temperature", "Tₚ")
PlanckTemperature.equals(((ℏ * c**5) / (G * k**2)).root(2))


# https://en.wikipedia.org/wiki/Stoney_units

# The Coulomb constant
# https://en.wikipedia.org/wiki/Coulomb_constant
kₑ = 8.9875517923e9 * (Kilogram * Meter**3) / (Second**2 * Coulomb**2)

StoneyLength = Length.unit("stoney length", "lₛ")
StoneyLength.equals(((G * kₑ * e**2) / c**4).root(2))

StoneyMass = Mass.unit("stoney mass", "mₛ")
StoneyMass.equals(((kₑ * e**2) / G).root(2))

StoneyTime = Time.unit("stoney time", "tₛ")
StoneyTime.equals(((G * kₑ * e**2) / c**6).root(2))

StoneyCharge = Charge.unit("stoney charge", "qₛ")
StoneyCharge.equals(e)


# https://en.wikipedia.org/wiki/Natural_units#Atomic_units

AtomicLength = Length.unit("atomic length", "lₐ")
AtomicLength.equals(((4 * π * ε0) * ℏ**2) / (mₑ * e**2))

AtomicMass = Mass.unit("atomic mass", "mₐ")
AtomicMass.equals(mₑ)

AtomicTime = Time.unit("atomic time", "tₐ")
AtomicTime.equals(((4 * π * ε0) ** 2 * ℏ**3) / (mₑ * e**4))

AtomicCharge = Charge.unit("atomic charge", "qₐ")
AtomicCharge.equals(e)
