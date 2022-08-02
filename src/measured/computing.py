"""
Units and non-standardized conventions from the domain of computing.

Attributes: Unit

    Furman (Unit): A unit of `PlaneAngle` that divides the circle into 2¹⁶ divisions,
        making it convenient for representation and arithmetic on a commputer.

    Nibble (Unit): A unit of `Information` equal to half a byte

"""

from measured import Information, PlaneAngle
from measured.geometry import π
from measured.iec import Bit
from measured.si import Radian

# https://en.wikipedia.org/wiki/List_of_unusual_units_of_measurement
# The Furman is a unit of angular measure equal to 1/65,536 of a circle
Furman = PlaneAngle.unit("Furman", "furman")
Furman.equals(1 / 65536 * 2 * π * Radian)

# https://en.wikipedia.org/wiki/Nibble
Nibble = Information.unit("nibble", "nibble")
Nibble.equals(4 * Bit)
