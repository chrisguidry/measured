# https://en.wikipedia.org/wiki/FFF_system

from measured import Mass, Time, us
from measured.si import Day

Furlong = us.Furlong

Firkin = Mass.unit("firkin", "fir")
Firkin.equals(90 * us.Pound)

Fortnight = Time.unit("fortnight", "ftn")
Fortnight.equals(14 * Day)
