"""
Units and non-standardized conventions relating to electronics

Attributes: LogarithmicUnits

    dBSPL (LogarithmicUnit): Decibels of Sound `Pressure`, compared to 20 μPa
"""
from measured import Decibel
from measured.si import Micro, Pascal

# https://en.wikipedia.org/wiki/Sound_pressure#Sound_pressure_level

dBSPL = Decibel[20 * Micro * Pascal].alias("dBSPL", "dBSPL")
