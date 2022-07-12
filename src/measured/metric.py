# Units based on the meter, gram, and second, but not part of the SI system of units
# https://en.wikipedia.org/wiki/List_of_metric_units
#
# Includes specialized units compatible with SI and accepted for use with it by either
# the BIPM or NIST
# https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-5-units-outside-si

from measured import Area, Frequency, Length, Time, Volume, VolumetricFlow
from measured.si import Femto, Hertz, Liter, Meter, Micro, Second, Tera

# Length, Area, and Volume

Ångström = Length.unit("Ångström", "Å")
Ångström.equals(1e-10 * Meter)

Fermi = Length.unit("fermi", "fermi")
Fermi.equals(1 * Femto * Meter)

Micron = Length.unit("micron", "μ")
Micron.equals(1 * Micro * Meter)

MetricMile = Length.unit("metric mile", "metric-mile")
MetricMile.equals(1500 * Meter)

Lieue = Length.unit("lieue", "lieue")
Lieue.equals(4000 * Meter)

Lambda = Volume.unit("lambda", "λ")
Lambda.equals(1 * Micro * Liter)

Stere = Volume.unit("stere", "st")
Stere.equals(1 * Meter**3)

# From the domain of high-energy and atomic physics
# https://en.wikipedia.org/wiki/Barn_(unit)
# https://en.wikipedia.org/wiki/Shake_(unit)

Barn = Area.unit("barn", "barn")
Barn.equals(1e-28 * Meter**2)

Outhouse = Area.unit("outhouse", "outhouse")
Outhouse.equals(1e-34 * Meter**2)

Shed = Area.unit("shed", "shed")
Shed.equals(1e-52 * Meter**2)


# Time

Svedberg = Time.unit("svedberg", "svedberg")
Svedberg.equals(100 * Femto * Second)

Shake = Time.unit("shake", "shake")
Shake.equals(1e-8 * Second)

Fresnel = Frequency.unit("fresnel", "fresnel")
Fresnel.equals(1 * Tera * Hertz)


# Derived

Sverdrup = VolumetricFlow.unit("sverdrup", "sverdrup")
Sverdrup.equals(1000000 * Meter**3 / Second)
