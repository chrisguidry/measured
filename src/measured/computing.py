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
