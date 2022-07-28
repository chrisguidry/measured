from measured import Length
from measured.si import Hertz, Meter

# ISO 2848:1984 - Building construction — Modular coordination — Principles and rules
# https://www.iso.org/standard/7846.html

BasicModule = Length.unit("basic module", "basic-module")
BasicModule.equals(0.1 * Meter)

MetricInch = Length.unit("metric inch", "metric-foot")
MetricInch.equals(0.25 * BasicModule)

MetricFoot = Length.unit("metric foot", "metric-inch")
MetricInch.equals(3 * BasicModule)


# ISO 16:1975 Acoustics, Standard tuning frequency (Standard musical pitch)
# http://www.iso.org/iso/iso_catalogue/catalogue_tc/catalogue_detail.htm?csnumber=3601

A440 = 440 * Hertz
