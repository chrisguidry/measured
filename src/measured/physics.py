"""
Defines both the [fundamental _dimensionless_ constants][1], as well as the
[foundational _dimensioned_ physical constants][2] of the universe.

[1]: https://en.wikipedia.org/wiki/Dimensionless_physical_constant
[2]: https://en.wikipedia.org/wiki/Physical_constant

Attributes: Physical constants

    c (Quantity): The [speed that light travels unimpeded in a vacuum][1]

        [1]: https://en.wikipedia.org/wiki/Speed_of_light

    G (Quantity): The "strength" of the [gravitational force][1]

        [1]: https://en.wikipedia.org/wiki/Gravitational_constant

    h (Quantity): The [Planck constant][1]

        [1]: https://en.wikipedia.org/wiki/Planck_constant

    ℏ (Quantity): The ["reduced" Planck constant][1]

        [1]: https://en.wikipedia.org/wiki/Planck_constant#Reduced_Planck_constant

    k (Quantity): The [Boltzmann constant][1]

        [1]: https://en.wikipedia.org/wiki/Boltzmann_constant

    e (Quantity): The [elementary charge][1]

        [1]: https://en.wikipedia.org/wiki/Elementary_charge

    ε0 (Quantity): [Vacuum permittivity][1], the capability of an electric field to
        permeate a vacuum

        [1]: https://en.wikipedia.org/wiki/Vacuum_permittivity

    mₑ (Quantity): The [mass of an electron][1]

        [1]: https://en.wikipedia.org/wiki/Electron_mass

    kₑ (Quantity): Coulomb's [electric force constants][1]

        [1]: https://en.wikipedia.org/wiki/Coulomb_constant

    α (Quantity): The [fine-structure constant][1], quantifying the strength of
        electromagnetic interactions

        [1]: https://en.wikipedia.org/wiki/Fine-structure_constant


"""

from measured.geometry import π
from measured.si import Coulomb, Farad, Hertz, Joule, Kelvin, Kilogram, Meter, Second

# https://en.wikipedia.org/wiki/Speed_of_light
c = 299792458 * Meter / Second

# https://en.wikipedia.org/wiki/Gravitational_constant
G = 6.6743015e-11 * Meter**3 / (Kilogram * Second**2)

# https://en.wikipedia.org/wiki/Planck_constant#Value
h = 6.62607015e-34 * Joule / Hertz

# The "reduced" Planck constant, "h-bar"
ℏ = h / (2 * π)

# https://en.wikipedia.org/wiki/Boltzmann_constant
k = 1.380649e-23 * Joule / Kelvin

# https://en.wikipedia.org/wiki/Elementary_charge
e = 1.602176634e-19 * Coulomb

# https://en.wikipedia.org/wiki/Vacuum_permittivity
ε0 = 8.8541878128e-12 * Farad / Meter

# https://en.wikipedia.org/wiki/Electron_mass
mₑ = 9.1093837015e-31 * Kilogram

# https://en.wikipedia.org/wiki/Coulomb_constant
kₑ = (4 * π * ε0) ** -1

# https://en.wikipedia.org/wiki/Fine-structure_constant
α = (e**2) / (4 * π * ε0 * ħ * c)

# https://en.wikipedia.org/wiki/Standard_gravity
gₙ = 9.80665 * Meter / Second**2
