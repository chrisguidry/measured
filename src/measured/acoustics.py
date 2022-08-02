"""
Units and non-standardized conventions relating to acoustics.

Attributes: LogarithmicUnits

    dBSPL (LogarithmicUnit): Decibels of Sound `Pressure`, compared to 20 μPa

    dBSWL (LogarithmicUnit): Decibels of Sound `Power`, compared to 1 pW

    dBSIL (LogarithmicUnit): Decibels of Sound intensity, compared to 1 pW/m²

Attributes: Constants

    ABSOLUTE_THRESHOLD_OF_HEARING (Quantity, Pressure): 20 μPa, an approximation of the
        [minimum sound pressure][1] that can be heard by an average human ear

        [1]: https://en.wikipedia.org/wiki/Absolute_threshold_of_hearing
"""

from measured import Decibel
from measured.si import Meter, Micro, Pascal, Pico, Watt

# https://en.wikipedia.org/wiki/Absolute_threshold_of_hearing
ABSOLUTE_THRESHOLD_OF_HEARING = 20 * Micro * Pascal

# https://en.wikipedia.org/wiki/Sound_pressure#Sound_pressure_level
dBSPL = Decibel[ABSOLUTE_THRESHOLD_OF_HEARING].alias("dBSPL", "dBSPL")

# https://en.wikipedia.org/wiki/Sound_power#Sound_power_level
dBSWL = Decibel[1 * Pico * Watt].alias("dBSWL", "dBSWL")

# https://en.wikipedia.org/wiki/Sound_intensity#Sound_intensity_level
dBSIL = Decibel[1 * (Pico * Watt) / Meter**2].alias("dBSIL", "dBSIL")
