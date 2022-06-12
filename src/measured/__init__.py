from collections import defaultdict
from functools import total_ordering
from math import log
from typing import (
    Any,
    ClassVar,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Set,
    Tuple,
    Union,
    overload,
)

from .formatting import superscript

__version__ = "0.0.3"

NUMERIC_CLASSES = (int, float)
Numeric = Union[int, float]


class Dimension:
    _known: ClassVar[Dict[Tuple[int, ...], "Dimension"]] = {}
    _initialized: bool = False

    _fundamental: ClassVar[List["Dimension"]] = []

    exponents: Tuple[int, ...]
    name: Optional[str]
    symbol: Optional[str]

    def __new__(
        cls,
        exponents: Tuple[int, ...],
        name: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> "Dimension":
        if exponents in cls._known:
            return cls._known[exponents]

        self = super().__new__(cls)
        cls._known[exponents] = self
        return self

    def __init__(
        self,
        exponents: Tuple[int, ...],
        name: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> None:
        if self._initialized:
            return
        self.exponents = exponents
        self.name = name
        self.symbol = symbol
        self._initialized = True

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

    def __str__(self) -> str:
        if self.symbol:
            return self.symbol

        return (
            "".join(
                f"{dimension.symbol}{superscript(self.exponents[i])}"
                for i, dimension in enumerate(self._fundamental)
                if self.exponents[i] != 0
            )
            or "?"
        )

    # https://en.wikipedia.org/wiki/Dimensional_analysis#Dimensional_homogeneity
    #
    # Only commensurable quantities (physical quantities having the same dimension)
    # may be compared, equated, added, or subtracted.

    def __add__(self, other: "Dimension") -> "Dimension":
        if self is not other:
            return NotImplemented

        return self

    def __sub__(self, other: "Dimension") -> "Dimension":
        if self is not other:
            return NotImplemented

        return self

    # https://en.wikipedia.org/wiki/Dimensional_analysis#Dimensional_homogeneity
    #
    # The dimensions form an [abelian
    # group](https://en.wikipedia.org/wiki/Abelian_group) under multiplication, so:
    # One may take ratios of incommensurable quantities (quantities with different
    # dimensions), and multiply or divide them.

    def __mul__(self, other: "Dimension") -> "Dimension":
        if not isinstance(other, Dimension):
            return NotImplemented

        return Dimension(tuple(s + o for s, o in zip(self.exponents, other.exponents)))

    def __truediv__(self, other: "Dimension") -> "Dimension":
        if not isinstance(other, Dimension):
            return NotImplemented

        return Dimension(
            tuple([s - o for s, o in zip(self.exponents, other.exponents)])
        )

    def __pow__(self, power: int) -> "Dimension":
        if not isinstance(power, int):
            return NotImplemented

        return Dimension(tuple([s * power for s in self.exponents]))


class Prefix:
    _known: ClassVar[Dict[Tuple[int, Numeric], "Prefix"]] = {}
    _initialized: bool = False

    base: int
    exponent: Numeric
    name: Optional[str]
    symbol: Optional[str]

    def __new__(
        cls,
        base: int,
        exponent: Numeric,
        name: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> "Prefix":
        key = (base, exponent)
        if key in cls._known:
            return cls._known[key]

        self = super().__new__(cls)
        cls._known[key] = self
        return self

    def __init__(
        self,
        base: int,
        exponent: Numeric,
        name: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> None:
        if self._initialized:
            return

        self.base = base
        self.exponent = exponent
        self.name = name
        self.symbol = symbol
        self._initialized = True

    @classmethod
    def identity(cls) -> "Prefix":
        return Prefix(0, 0)

    def quantify(self) -> "Quantity":
        return Quantity(self.base**self.exponent, One)

    def __repr__(self) -> str:
        return f"<Prefix(base={self.base!r}, exponent={self.exponent!r}>"

    def __str__(self) -> str:
        if self.symbol:
            return self.symbol
        if self.exponent == 0:
            return ""
        return f"{self.base}{superscript(self.exponent)}"

    @overload
    def __mul__(self, other: "Prefix") -> "Prefix":
        ...  # pragma: no cover

    @overload
    def __mul__(self, other: "Unit") -> "Unit":
        ...  # pragma: no cover

    @overload
    def __mul__(self, other: Numeric) -> "Quantity":
        ...  # pragma: no cover

    def __mul__(
        self, other: Union["Prefix", "Unit", Numeric]
    ) -> Union["Prefix", "Unit", "Quantity"]:
        if isinstance(other, Prefix):
            if other.base == 0:
                return self
            elif self.base == 0:
                return other
            elif other.base == self.base:
                return Prefix(self.base, self.exponent + other.exponent)

            base, exponent = self.base, self.exponent
            exponent += other.exponent * (log(other.base) / log(self.base))

            return Prefix(base, exponent)

        if isinstance(other, Unit):
            return other.scale(self)

        if isinstance(other, NUMERIC_CLASSES):
            return (other * One) * self.quantify()

        return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other: "Prefix") -> "Prefix":
        if not isinstance(other, Prefix):
            return NotImplemented

        if other.base == 0:
            return self
        elif self.base == 0:
            return Prefix(other.base, -other.exponent)
        elif other.base == self.base:
            return Prefix(self.base, self.exponent - other.exponent)

        base, exponent = self.base, self.exponent
        exponent -= other.exponent * (log(other.base) / log(self.base))

        return Prefix(base, exponent)

    def __pow__(self, power: int) -> "Prefix":
        return Prefix(self.base, self.exponent * power)


class Unit:
    UnitKey = Tuple[Prefix, Tuple[Tuple["Unit", int], ...]]

    _known: ClassVar[Dict[UnitKey, "Unit"]] = {}
    _initialized: bool = False

    _base: ClassVar[Set["Unit"]] = set()

    prefix: Prefix
    factors: Mapping["Unit", int]
    name: Optional[str]
    symbol: Optional[str]

    def __new__(
        cls,
        prefix: Prefix,
        factors: Mapping["Unit", int],
        dimension: Dimension,
        name: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> "Unit":
        key = cls._build_key(prefix, factors)
        if key in cls._known:
            return cls._known[key]

        self = super().__new__(cls)
        key = cls._build_key(prefix, factors or {self: 1})
        cls._known[key] = self
        return self

    def __init__(
        self,
        prefix: Prefix,
        factors: Mapping["Unit", int],
        dimension: Dimension,
        name: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> None:
        if self._initialized:
            return
        self.prefix = prefix
        self.factors = factors or {self: 1}
        self.dimension = dimension
        self.name = name
        self.symbol = symbol
        self.names = [name]
        self.symbols = [symbol]
        self._initialized = True

    @classmethod
    def _build_key(cls, prefix: Prefix, factors: Mapping["Unit", int]) -> UnitKey:
        factor_key = tuple(sorted(factors.items(), key=lambda pair: id(pair[0])))
        return (prefix, factor_key)

    @classmethod
    def base(cls) -> Iterable["Unit"]:
        return list(cls._base)

    @classmethod
    def define(cls, dimension: Dimension, name: str, symbol: str) -> "Unit":
        """Defines a new base unit"""
        unit = cls(Prefix.identity(), {}, dimension, name, symbol)
        cls._base.add(unit)
        return unit

    @classmethod
    def derive(cls, unit: "Unit", name: str, symbol: str) -> "Unit":
        """Registers a new named unit derived from other units"""
        if unit.name:
            unit.names.append(name)
            unit.symbols.append(symbol)
            return unit

        unit.name = name
        unit.symbol = symbol
        return unit

    def scale(self, prefix: Prefix) -> "Unit":
        """Given a Prefix, creates a new unit scaled by that Prefix"""
        return self.__class__(self.prefix * prefix, self.factors, self.dimension)

    def quantify(self) -> "Quantity":
        return self.prefix.quantify() * Unit(
            Prefix.identity(), self.factors, self.dimension
        )

    def __repr__(self) -> str:
        return (
            "<Unit("
            f"dimension={self.dimension!r}, "
            f"prefix={self.prefix!r}, "
            f"name={self.name!r}, symbol={self.symbol!r}"
            ")>"
        )

    def __str__(self) -> str:
        if self.symbol:
            return self.symbol

        return str(self.prefix) + "".join(
            f"{unit.prefix}{unit.symbol}{superscript(exponent)}"
            for unit, exponent in self.factors.items()
        )

    @classmethod
    def _simplify(cls, factors: Mapping["Unit", int]) -> Dict["Unit", int]:
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
        prefix = self.prefix * other.prefix

        factors: Dict["Unit", int] = defaultdict(int, self.factors)
        for unit, exponent in other.factors.items():
            factors[unit] += exponent
        factors = self._simplify(factors)

        return Unit(prefix, factors, dimension)

    __rmul__ = __mul__

    def __truediv__(self, other: "Unit") -> "Unit":
        if not isinstance(other, Unit):
            return NotImplemented

        dimension = self.dimension / other.dimension
        prefix = self.prefix / other.prefix

        factors: Dict["Unit", int] = defaultdict(int, self.factors)
        for unit, exponent in other.factors.items():
            factors[unit] -= exponent
        factors = self._simplify(factors)

        return Unit(prefix, factors, dimension)

    def __pow__(self, power: int) -> "Unit":
        if not isinstance(power, int):
            return NotImplemented

        dimension = self.dimension**power
        prefix = self.prefix**power

        factors = self._simplify(
            {unit: exponent * power for unit, exponent in self.factors.items()}
        )
        return Unit(prefix, factors, dimension)


@total_ordering
class Quantity:
    def __init__(self, magnitude: Numeric, unit: Unit):
        self.magnitude = magnitude
        self.unit = unit

    def in_base_units(self) -> "Quantity":
        return (self.magnitude * One) * self.unit.quantify()

    def __repr__(self) -> str:
        return f"<Quantity(magnitude={self.magnitude!r}, unit={self.unit!r})>"

    def __str__(self) -> str:
        return f"{self.magnitude} {self.unit}"

    def __add__(self, other: "Quantity") -> "Quantity":
        if isinstance(other, Quantity):
            return Quantity(self.magnitude + other.magnitude, self.unit + other.unit)

        return NotImplemented

    def __sub__(self, other: "Quantity") -> "Quantity":
        if isinstance(other, Quantity):
            return Quantity(self.magnitude - other.magnitude, self.unit - other.unit)

        return NotImplemented

    def __mul__(self, other: Union["Quantity", "Unit", "Numeric"]) -> "Quantity":
        if isinstance(other, Unit):
            return Quantity(self.magnitude, self.unit * other)

        if isinstance(other, Quantity):
            return Quantity(self.magnitude * other.magnitude, self.unit * other.unit)

        if isinstance(other, NUMERIC_CLASSES):
            return Quantity(self.magnitude * other, self.unit)

        return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other: Union["Quantity", "Unit", "Numeric"]) -> "Quantity":
        if isinstance(other, Unit):
            return Quantity(self.magnitude, self.unit / other)

        if isinstance(other, Quantity):
            return Quantity(self.magnitude / other.magnitude, self.unit / other.unit)

        if isinstance(other, NUMERIC_CLASSES):
            return Quantity(self.magnitude / other, self.unit)

        return NotImplemented

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
            return NotImplemented

        if self.unit.dimension != other.unit.dimension:
            return NotImplemented

        this = self.in_base_units()
        other = other.in_base_units()

        return this.magnitude == other.magnitude and this.unit == other.unit

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Quantity):
            return NotImplemented

        if self.unit.dimension != other.unit.dimension:
            return NotImplemented

        this = self.in_base_units()
        other = other.in_base_units()

        if this.unit != other.unit:
            return NotImplemented

        return this.magnitude < other.magnitude

    def approximates(self, other: "Quantity", within: Numeric = 1e-9) -> bool:
        if self == other:
            return True

        if self.unit.dimension != other.unit.dimension:
            return False

        this = self.in_base_units()
        other = other.in_base_units()

        if this.unit != other.unit:
            return False

        difference = this - other
        tolerance = Quantity(within, this.unit)

        return abs(difference) <= tolerance


# https://en.wikipedia.org/wiki/Dimensional_analysis#Definition

# Fundamental physical dimensions

Number = Dimension.define(name="number", symbol="1")
Length = Dimension.define(name="length", symbol="L")
Time = Dimension.define(name="time", symbol="T")
Mass = Dimension.define(name="mass", symbol="M")
Current = Dimension.define(name="current", symbol="I")
Temperature = Dimension.define(name="temperature", symbol="Θ")
AmountOfSubstance = Dimension.define(name="amount of substance", symbol="N")
LuminousIntensity = Dimension.define(name="luminous intensity", symbol="J")
Information = Dimension.define(name="information", symbol="B")  # TODO


# Derived dimensions

Area = Length * Length
Volume = Area * Length

Angle = Length / Length
SolidAngle = Area / Area

# https://en.wikipedia.org/wiki/Fourth,_fifth,_and_sixth_derivatives_of_position

Speed = Length / Time
Acceleration = Length / Time**2
Jerk = Length / Time**3
Snap = Length / Time**4
Crackle = Length / Time**5
Pop = Length / Time**6

Frequency = Number / Time

# https://en.wikipedia.org/wiki/Newton%27s_laws_of_motion#Second

Force = Mass * Acceleration
Energy = Length * Force
Power = Energy / Time

Charge = Time * Current
Potential = Power / Charge
Capacitance = Charge / Potential
Resistance = Potential / Current
Conductance = Current / Potential
Inductance = Potential * Time / Current

MagneticFlux = Power / Current
MagneticInduction = Potential * Time / Area

Illuminance = LuminousIntensity / Area

RadioactiveDose = Power / Mass

CatalyticActivity = AmountOfSubstance / Time


# Fundamental units

One = Unit.define(Number, name="one", symbol="1")
