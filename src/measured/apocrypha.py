from measured import Length
from measured.us import Foot, Inch

# https://en.wikipedia.org/wiki/Smoot
Smoot = Length.unit("smoot", "smoot")
Smoot.equals(5 * Foot + 7 * Inch)
