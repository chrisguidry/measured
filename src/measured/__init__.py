from collections import defaultdict
from typing import Any, Dict, Iterable, List, Mapping, Set, Tuple, Union, overload

__version__ = "0.0.1"

NUMERIC_CLASSES = (int, float)
Numeric = Union[int, float]


class Dimension:
    _known: Dict[Tuple, "Dimension"] = {}
    _fundamental: List["Dimension"] = []

    _skip_initialization_for: int = 0

    def __new__(cls, exponents: Tuple, **kwargs):
        key = tuple(exponents)
        if key in cls._known:
            known = cls._known[key]
            cls._skip_initialization_for = id(known)
            return known

        self = super().__new__(cls)
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
            "<Dimension("
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


class Unit:
    _known: Dict[Tuple, "Unit"] = {}
    _base: Set["Unit"] = set()

    _skip_initialization_for: int = 0

    def __new__(cls, factors: Mapping["Unit", int], *args, **kwargs):
        if factors:
            key = cls._factors_as_key(factors)
            if key in cls._known:
                known = cls._known[key]
                cls._skip_initialization_for = id(known)
                return known

        self = super().__new__(cls)
        factors = factors or {self: 1}
        key = cls._factors_as_key(factors)
        cls._known[key] = self
        return self

    def __init__(
        self,
        factors: Mapping["Unit", int],
        dimension: Dimension,
        name: str = None,
        symbol: str = None,
    ):
        if self.__class__._skip_initialization_for == id(self):
            self.__class__._skip_initialization_for = 0
            return

        self.factors = factors or {self: 1}
        self.dimension = dimension
        self.name = name
        self.symbol = symbol

    @classmethod
    def _factors_as_key(cls, factors: Mapping["Unit", int]):
        return tuple(sorted(factors.items(), key=lambda pair: id(pair[0])))

    @classmethod
    def base(cls) -> Iterable["Unit"]:
        return list(cls._base)

    @classmethod
    def define(cls, dimension: Dimension, name: str, symbol: str) -> "Unit":
        """Defines a new base unit"""
        unit = cls({}, dimension, name, symbol)
        cls._base.add(unit)
        return unit

    @classmethod
    def derive(cls, unit: "Unit", name: str, symbol: str) -> "Unit":
        """Registers a new named unit derived from other units"""
        unit.name = name
        unit.symbol = symbol
        return unit

    def __repr__(self) -> str:
        return (
            "<Unit("
            f"dimension={self.dimension!r}, "
            f"name={self.name!r}, symbol={self.symbol!r}"
            ")>"
        )

    @classmethod
    def _simplify(cls, factors: Mapping["Unit", int]) -> Mapping["Unit", int]:
        simplified = {
            unit: exponent
            for unit, exponent in factors.items()
            if unit is not One and exponent != 0
        }
        return simplified or {One: 1}

    def __add__(self, other: "Unit") -> "Unit":
        if self is not other:
            return NotImplemented

        return self

    def __sub__(self, other: "Unit") -> "Unit":
        if self is not other:
            return NotImplemented

        return self

    @overload
    def __mul__(self, other: "Unit") -> "Unit":
        ...  # pragma: no cover

    @overload
    def __mul__(self, other: Numeric) -> "Quantity":
        ...  # pragma: no cover

    def __mul__(self, other: Union["Unit", Numeric]) -> Union["Unit", "Quantity"]:
        if isinstance(other, NUMERIC_CLASSES):
            return Quantity(other, self)

        if not isinstance(other, Unit):
            return NotImplemented

        dimension = self.dimension * other.dimension

        factors: Dict["Unit", int] = defaultdict(int, self.factors)
        for unit, exponent in other.factors.items():
            factors[unit] += exponent

        return Unit(self._simplify(factors), dimension)

    __rmul__ = __mul__

    def __truediv__(self, other: "Unit") -> "Unit":
        if not isinstance(other, Unit):
            return NotImplemented

        dimension = self.dimension / other.dimension

        factors: Dict["Unit", int] = defaultdict(int, self.factors)
        for unit, exponent in other.factors.items():
            factors[unit] -= exponent

        return Unit(self._simplify(factors), dimension)

    def __pow__(self, power: int) -> "Unit":
        if not isinstance(power, int):
            return NotImplemented

        dimension = self.dimension**power
        factors = {unit: exponent * power for unit, exponent in self.factors.items()}

        return Unit(self._simplify(factors), dimension)


One = Unit.define(Number, name="one", symbol="1")

# https://en.wikipedia.org/wiki/International_System_of_Units

# https://en.wikipedia.org/wiki/SI_base_unit

Meter = Unit.define(Length, name="meter", symbol="m")
Second = Unit.define(Time, name="second", symbol="s")
Gram = Unit.define(Mass, name="gram", symbol="g")
Ampere = Unit.define(Current, name="ampere", symbol="A")
Kelvin = Unit.define(Temperature, name="kelvin", symbol="K")
Mole = Unit.define(AmountOfSubstance, name="mole", symbol="mol")
Candela = Unit.define(LuminousIntensity, name="candela", symbol="cd")

# https://en.wikipedia.org/wiki/SI_derived_unit

Hertz = Unit.derive(One / Second, name="hertz", symbol="Hz")


class Quantity:
    def __init__(self, magnitude: Numeric, unit: Unit):
        self.magnitude = magnitude
        self.unit = unit

    def __repr__(self) -> str:
        return f"<Quantity(magnitude={self.magnitude!r}, unit={self.unit!r})>"

    def __add__(self, other: "Quantity") -> "Quantity":
        return Quantity(self.magnitude + other.magnitude, self.unit + other.unit)

    def __sub__(self, other: "Quantity") -> "Quantity":
        return Quantity(self.magnitude - other.magnitude, self.unit - other.unit)

    def __mul__(self, other: Union["Quantity", "Unit"]) -> "Quantity":
        if isinstance(other, Unit):
            return Quantity(self.magnitude, self.unit * other)

        return Quantity(self.magnitude * other.magnitude, self.unit * other.unit)

    def __truediv__(self, other: Union["Quantity", "Unit"]) -> "Quantity":
        if isinstance(other, Unit):
            return Quantity(self.magnitude, self.unit / other)

        return Quantity(self.magnitude / other.magnitude, self.unit / other.unit)

    def __pow__(self, power: int) -> "Quantity":
        return Quantity(self.magnitude**power, self.unit**power)

    def __neg__(self) -> "Quantity":
        return Quantity(-self.magnitude, self.unit)

    def __pos__(self) -> "Quantity":
        return Quantity(+self.magnitude, self.unit)

    def __abs__(self) -> "Quantity":
        return Quantity(abs(self.magnitude), self.unit)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Quantity):
            return False

        return self.magnitude == other.magnitude and self.unit == other.unit
