import pytest

from measured import Level, Pressure, Quantity, approximately
from measured.acoustics import ABSOLUTE_THRESHOLD_OF_HEARING, dBSPL
from measured.si import Micro, Pascal


def test_auditory_threshold() -> None:
    assert ABSOLUTE_THRESHOLD_OF_HEARING.unit.dimension == Pressure
    assert ABSOLUTE_THRESHOLD_OF_HEARING == 20 * Micro * Pascal
    assert ABSOLUTE_THRESHOLD_OF_HEARING == 0 * dBSPL


# https://en.wikipedia.org/wiki/Sound_pressure#Examples_of_sound_pressure
@pytest.mark.parametrize(
    "pressure, level, within",
    [
        # Microsoft's A-weighted anechoic chamber
        (1.9e-6 * Pascal, -20.35 * dBSPL, 0.02),
        # threshold of human hearing
        (ABSOLUTE_THRESHOLD_OF_HEARING, 0 * dBSPL, 1e-7),
        # Jackhammer at 1 meter
        (2 * Pascal, 100 * dBSPL, 1e-7),
        # Chainsaw at 1 meter
        (6.32 * Pascal, 110 * dBSPL, 1e-3),
        # Jet Engine at 1 meter
        (632 * Pascal, 150 * dBSPL, 1e-3),
    ],
)
def test_examples_of_sound_pressure(
    pressure: Quantity, level: Level, within: float
) -> None:
    assert pressure == approximately(level, within=within)
    assert level == approximately(pressure, within=within)
