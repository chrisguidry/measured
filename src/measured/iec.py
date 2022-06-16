"""
Defines the units of `Information` and the binary [prefixes][2] as defined by the
International Electrotechnical Commission.

[1]: https://en.wikipedia.org/wiki/Byte

[2]: https://en.wikipedia.org/wiki/Binary_prefix#Adoption_by_IEC,_NIST_and_ISO

Attributes: Base Units

    Bit (Unit):

Attributes: Derived Units

    Byte (Unit): 8 bits

Attributes: Prefixes (base 2)

    Kibi (Prefix): 2¹⁰, symbol `Ki`
    Mebi (Prefix): 2²⁰, symbol `Mi`
    Gibi (Prefix): 2³⁰, symbol `Gi`
    Tebi (Prefix): 2⁴⁰, symbol `Ti`
    Pebi (Prefix): 2⁵⁰, symbol `Pi`
    Exbi (Prefix): 2⁶⁰, symbol `Ei`
    Zebi (Prefix): 2⁷⁰, symbol `Zi`
    Yobi (Prefix): 2⁸⁰, symbol `Yi`

"""

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
Byte = Unit.derive(Bit.scale(Prefix(2, 3)), name="byte", symbol="B")
