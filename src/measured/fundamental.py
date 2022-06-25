"""
Defines both the [fundamental _dimensionless_ constants][1], as well as the
[foundational _dimensioned_ physical constants][2] of the universe.

[1]: https://en.wikipedia.org/wiki/Dimensionless_physical_constant
[2]: https://en.wikipedia.org/wiki/Physical_constant

Attributes: Physical constants

    SpeedOfLight (Quantity): The speed that light travels unimpeded in a vacuum

    GravitationalConstant (Quantity): The "strength" of the gravitational force
"""

from measured.si import Kilogram, Meter, Second

SpeedOfLight = 299792458 * Meter / Second
GravitationalConstant = 6.6743015e-11 * Meter**3 / (Kilogram * Second**2)
