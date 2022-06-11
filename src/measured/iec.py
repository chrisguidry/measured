# https://en.wikipedia.org/wiki/Binary_prefix#Adoption_by_IEC,_NIST_and_ISO

from . import Information, Prefix, Unit

Kibi = Prefix(2, 10, name="kibi", symbol="Ki")
Mebi = Prefix(2, 20, name="mebi", symbol="Mi")
Gibi = Prefix(2, 30, name="gibi", symbol="Gi")
Tebi = Prefix(2, 40, name="tebi", symbol="Ti")
Pebi = Prefix(2, 50, name="pebi", symbol="Pi")
Exbi = Prefix(2, 60, name="exbi", symbol="Ei")
Zebi = Prefix(2, 70, name="zebi", symbol="Zi")
Yobi = Prefix(2, 80, name="yobi", symbol="Yi")

Bit = Unit.define(Information, name="bit", symbol="b")
# Byte = Unit.derive(Bit.scale(8), name="byte", symbol="byte")
