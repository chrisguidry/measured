from array import array
from typing import Dict, Iterable

__version__ = "0.0.1"


class Dimension:
    _known: Dict[bytes, "Dimension"] = {}
    _skip_initialization_for: int = 0

    def __new__(cls, exponents: array, **kwargs):
        self = super().__new__(cls)

        key = exponents.tobytes()
        if key in cls._known:
            known = cls._known[key]
            cls._skip_initialization_for = id(known)
            return known

        cls._known[key] = self
        return self

    def __init__(self, exponents: array, name: str = None, symbol: str = None):
        if self.__class__._skip_initialization_for == id(self):
            self.__class__._skip_initialization_for = 0
            return

        self.exponents = exponents
        self.name = name
        self.symbol = symbol

    @classmethod
    def known(cls) -> Iterable["Dimension"]:
        return list(cls._known.values())

    @classmethod
    def fundamental(cls, name: str, symbol: str) -> "Dimension":
        """Registers a new fundamental Dimension"""
        index = len(cls._known)
        if index == 0:
            exponents = array("b", [0])
        else:
            exponents = array("b", ([0] * index) + [1])

        dimension = cls(exponents, name=name, symbol=symbol)

        for key, previous in list(cls._known.items()):
            previous.exponents.append(0)
            del cls._known[key]
            key = previous.exponents.tobytes()
            cls._known[key] = previous

        return dimension

    def __repr__(self) -> str:
        return (
            "<measured.Dimension("
            f"exponents={self.exponents!r}, "
            f"name={self.name!r}, symbol={self.symbol!r}"
            ")>"
        )

    def __add__(self, other: "Dimension") -> "Dimension":
        # https://en.wikipedia.org/wiki/Dimensional_analysis#Dimensional_homogeneity
        #
        # Only commensurable quantities (physical quantities having the same dimension)
        # may be compared, equated, added, or subtracted.
        if self is not other:
            return NotImplemented
        return self

    def __sub__(self, other: "Dimension") -> "Dimension":
        # https://en.wikipedia.org/wiki/Dimensional_analysis#Dimensional_homogeneity
        #
        # Only commensurable quantities (physical quantities having the same dimension)
        # may be compared, equated, added, or subtracted.
        if self is not other:
            return NotImplemented
        return self

    def __mul__(self, other: "Dimension") -> "Dimension":
        # https://en.wikipedia.org/wiki/Dimensional_analysis#Dimensional_homogeneity
        #
        # The dimensions form an [abelian
        # group](https://en.wikipedia.org/wiki/Abelian_group) under multiplication, so:
        # One may take ratios of incommensurable quantities (quantities with different
        # dimensions), and multiply or divide them.
        if not isinstance(other, Dimension):
            return NotImplemented

        return Dimension(
            array("b", [s + o for s, o in zip(self.exponents, other.exponents)])
        )

    def __truediv__(self, other: "Dimension") -> "Dimension":
        # https://en.wikipedia.org/wiki/Dimensional_analysis#Dimensional_homogeneity
        #
        # The dimensions form an abelian group
        # (https://en.wikipedia.org/wiki/Abelian_group) under multiplication, so: One
        # may take ratios of incommensurable quantities (quantities with different
        # dimensions), and multiply or divide them.
        if not isinstance(other, Dimension):
            return NotImplemented

        return Dimension(
            array("b", [s - o for s, o in zip(self.exponents, other.exponents)])
        )

    def __pow__(self, power: int) -> "Dimension":
        if not isinstance(power, int):
            return NotImplemented

        return Dimension(array("b", [s * power for s in self.exponents]))


# https://en.wikipedia.org/wiki/Dimensional_analysis#Definition
#
# time (T), length (L), mass (M), electric current (I),
# absolute temperature (Θ), amount of substance (N) and luminous intensity (J).

Number = Dimension.fundamental(name="number", symbol="1")
Length = Dimension.fundamental(name="length", symbol="L")
Time = Dimension.fundamental(name="time", symbol="T")
Mass = Dimension.fundamental(name="mass", symbol="M")
Current = Dimension.fundamental(name="current", symbol="I")
Temperature = Dimension.fundamental(name="temperature", symbol="Θ")
AmountOfSubstance = Dimension.fundamental(name="amount of substance", symbol="N")
LuminousIntensity = Dimension.fundamental(name="luminous intensity", symbol="J")

Area = Length * Length
Volume = Area * Length

Speed = Length / Time
Acceleration = Length / Time**2
Jerk = Length / Time**3
Snap = Length / Time**4
Crackle = Length / Time**5
Pop = Length / Time**6

Frequency = Number / Time
