from measured import approximately
from measured.apocrypha import Smoot
from measured.si import Meter
from measured.us import Foot


def test_smoot() -> None:
    assert 364.4 * Smoot == approximately(2035 * Foot, within=3e-4)
    assert 364.4 * Smoot == approximately(620.1 * Meter, within=3e-4)
