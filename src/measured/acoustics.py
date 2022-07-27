"""
Units and non-standardized conventions relating to electronics

Attributes: LogarithmicUnits

    dBSPL (LogarithmicUnit): Decibels of Sound `Pressure`, compared to 20 μPa
"""
from measured import Decibel
from measured.si import Micro, Pascal

# https://en.wikipedia.org/wiki/Absolute_threshold_of_hearing

ABSOLUTE_THRESHOLD_OF_HEARING = 20 * Micro * Pascal

# https://en.wikipedia.org/wiki/Sound_pressure#Sound_pressure_level

dBSPL = Decibel[ABSOLUTE_THRESHOLD_OF_HEARING].alias("dBSPL", "dBSPL")
