import pytest
from pytest import approx

from measured import Decibel, Level, Pressure, Quantity, approximately
from measured.acoustics import ABSOLUTE_THRESHOLD_OF_HEARING, dBSPL, dBSWL
from measured.geometry import π
from measured.si import Meter, Micro, Pascal


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


def test_sound_power_from_sound_pressure() -> None:
    # https://en.wikipedia.org/wiki/Sound_power#Relationship_with_sound_pressure_level
    # https://en.wikipedia.org/wiki/Sound_pressure#Sound_pressure_level

    # cross-checked with
    # https://www.wkcgroup.com/tools-room/sound-power-sound-pressure-converter/

    distance = 2 * Meter
    area = 4 * π * distance**2
    assert area == approximately(50.265482 * Meter**2)

    surface_area_level = area.level(Decibel[1 * Meter**2])
    assert surface_area_level == approximately(17.01269855 * Decibel[1 * Meter**2])

    pressure = 50 * dBSPL
    power = 67.0127 * dBSWL

    assert pressure.magnitude + surface_area_level.magnitude == approx(power.magnitude)
