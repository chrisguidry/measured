# https://en.wikipedia.org/wiki/Natural_units

# https://en.wikipedia.org/wiki/Planck_units

from math import pi as π

from measured import Charge, Length, Mass, Temperature, Time
from measured.fundamental import G, c, e, k, kₑ, mₑ, ε0, ℏ

PlanckLength = Length.unit("planck length", "lₚ")
PlanckLength.equals(((ℏ * G) / c**3).root(2))

PlanckMass = Mass.unit("planck mass", "mₚ")
PlanckMass.equals(((ℏ * c) / G).root(2))

PlanckTime = Time.unit("planck time", "tₚ")
PlanckTime.equals(((ℏ * G) / c**5).root(2))

PlanckTemperature = Temperature.unit("planck temperature", "Tₚ")
PlanckTemperature.equals(((ℏ * c**5) / (G * k**2)).root(2))


# https://en.wikipedia.org/wiki/Stoney_units

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


# https://en.wikipedia.org/wiki/Natural_units#Natural_units_(particle_and_atomic_physics)

NaturalLength = Length.unit("natural length", "lₙ")
NaturalLength.equals((ℏ / (mₑ * c)))

NaturalMass = Mass.unit("natural mass", "mₙ")
NaturalMass.equals(mₑ)

NaturalTime = Time.unit("natural time", "tₙ")
NaturalTime.equals((ℏ / (mₑ * c**2)))

NaturalCharge = Charge.unit("natural charge", "qₙ")
NaturalCharge.equals((ε0 * ℏ * c).root(2))
