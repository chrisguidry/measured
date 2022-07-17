from measured.apocrypha import Smoot
from measured.si import Meter
from measured.us import Foot


def test_smoot() -> None:
    (364.4 * Smoot).assert_approximates(2035 * Foot, within=3e-4)
    (364.4 * Smoot).assert_approximates(620.1 * Meter, within=3e-4)
