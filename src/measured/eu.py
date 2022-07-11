from measured import PlaneAngle
from measured.geometry import π
from measured.si import Radian

Gradian = PlaneAngle.unit("gradian", "gon")
Gradian.equals(π / 200 * Radian)
