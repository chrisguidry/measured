"""
Units and non-standardized conventions relating to electronics

Attributes: LogarithmicUnits

    dBW (LogarithmicUnit): Decibels of `Power`, compared to 1 `Watt`
"""
from measured import Decibel
from measured.si import Watt

# https://en.wikipedia.org/wiki/Decibel#Suffixes_and_reference_values

dBW = Decibel[1 * Watt].alias("dbW", "dbW")
