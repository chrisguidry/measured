from typing import Dict, Iterable, List, Tuple

__version__ = "0.0.1"


class Dimension:
    _known: Dict[Tuple, "Dimension"] = {}
    _fundamental: List["Dimension"] = []

    _skip_initialization_for: int = 0

    def __new__(cls, exponents: Tuple, **kwargs):
        self = super().__new__(cls)

        key = tuple(exponents)
        if key in cls._known:
            known = cls._known[key]
            cls._skip_initialization_for = id(known)
            return known

        cls._known[key] = self
        return self

    def __init__(self, exponents: Tuple, name: str = None, symbol: str = None):
        if self.__class__._skip_initialization_for == id(self):
            self.__class__._skip_initialization_for = 0
            return

        self.exponents = exponents
        self.name = name
        self.symbol = symbol

    @classmethod
    def fundamental(cls) -> Iterable["Dimension"]:
        """Returns the registered fundamental Dimensions"""
        return list(cls._fundamental)

    @classmethod
    def define(cls, name: str, symbol: str) -> "Dimension":
        """Defines a new fundamental Dimension"""
        index = len(cls._fundamental)
        if index == 0:
            # the first dimension must be Number, with an exponent of zero (identity)
            exponents = tuple([0])
        else:
            # other dimensions start with their exponent at one, and all others zero
            exponents = tuple(([0] * index) + [1])

        dimension = cls(exponents, name=name, symbol=symbol)

        # resize the keys for all previously known dimensions to account
        # for this new fundamental dimension
        for previous in list(cls._known.values()):
            del cls._known[previous.exponents]
            previous.exponents += (0,)
            cls._known[previous.exponents] = previous

        cls._fundamental.append(dimension)

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

        return Dimension(tuple(s + o for s, o in zip(self.exponents, other.exponents)))

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
            tuple([s - o for s, o in zip(self.exponents, other.exponents)])
        )

    def __pow__(self, power: int) -> "Dimension":
        if not isinstance(power, int):
            return NotImplemented

        return Dimension(tuple([s * power for s in self.exponents]))


# https://en.wikipedia.org/wiki/Dimensional_analysis#Definition
#
# time (T), length (L), mass (M), electric current (I),
# absolute temperature (Θ), amount of substance (N) and luminous intensity (J).

Number = Dimension.define(name="number", symbol="1")
Length = Dimension.define(name="length", symbol="L")
Time = Dimension.define(name="time", symbol="T")
Mass = Dimension.define(name="mass", symbol="M")
Current = Dimension.define(name="current", symbol="I")
Temperature = Dimension.define(name="temperature", symbol="Θ")
AmountOfSubstance = Dimension.define(name="amount of substance", symbol="N")
LuminousIntensity = Dimension.define(name="luminous intensity", symbol="J")

Area = Length * Length
Volume = Area * Length

Speed = Length / Time
Acceleration = Length / Time**2
Jerk = Length / Time**3
Snap = Length / Time**4
Crackle = Length / Time**5
Pop = Length / Time**6

Frequency = Number / Time
