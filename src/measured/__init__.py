"""
The goal of the `measured` library is to provide a sound foundation for recording and
converting physical quantities, while maintaining the integrity of their units and
dimensions.

While it aims to be the fastest library of its kind, automatically tracking the units
and dimensions of quantities introduces significant overhead.  You can use `measured`
for applications where the accuracy of the units is more important than raw numerical
computing speed.

The value classes of `measured` should generally be treated as immutable.  Rather than
setting the `magnitude` of a [`Quantity`][measured.Quantity], consider instantiating a
new one, or performing arithmetic on an existing one to produce new values.  Instances
of [`Dimension`][measured.Dimension], [`Prefix`][measured.Prefix], and
[`Unit`][measured.Unit] are always singletons within a Python process.

For more background on the approach taken by this library, please see the material on
[quantity calculus][1] and [dimensional analysis][2].  `measured` uses the terms
"dimension", "unit", "prefix", and "quantity" in the same way.


[1]: https://en.wikipedia.org/wiki/Quantity_calculus

[2]: https://en.wikipedia.org/wiki/Dimensional_analysis


Examples:

    >>> from measured.si import Meter, Second
    >>> distance = 10 * Meter
    >>> time = 2 * Second
    >>> speed = distance / time
    >>> assert speed == 5 * Meter / Second

Attributes: Fundamental dimensions

    Number (Dimension): the basis of [counting and measuring][1], used to define
        [dimensionless quantities][2]

        [1]: https://en.wikipedia.org/wiki/Number

        [2]: https://en.wikipedia.org/wiki/Dimensionless_quantity

    Length (Dimension): [distance][1] or extent through space

        [1]: https://en.wikipedia.org/wiki/Length

    Time (Dimension): [what clocks read][1], the intervals between events

        [1]: https://en.wikipedia.org/wiki/Time

    Mass (Dimension): how much [matter][1] is in a physical body

        [1]: https://en.wikipedia.org/wiki/Mass

    Current (Dimension): the net rate of [flow of electrical charge][1] through a
        conductor

        [1]: https://en.wikipedia.org/wiki/Electric_current

    Temperature (Dimension): the average amount of [kinetic energy][1] in a system

        [1]: https://en.wikipedia.org/wiki/Temperature

    AmountOfSubstance (Dimension): how many [elementary entities][1] are in an object

        [1]: https://en.wikipedia.org/wiki/Mole_(unit)

    LuminousIntensity (Dimension): how strong a [light source][1] is over a volume

        [1]: https://en.wikipedia.org/wiki/Luminous_intensity

    Information (Dimension): how much [entropy][1] is present in a random variable

        [1]: https://en.wikipedia.org/wiki/Information#Information_theory

Attributes: Derived dimensions

    Area (Dimension):

    Volume (Dimension):

    PlaneAngle (Dimension):

    SolidAngle (Dimension):

    Speed (Dimension):

    Acceleration (Dimension):

    Jerk (Dimension):

    Snap (Dimension):

    Crackle (Dimension):

    Pop (Dimension):

    Frequency (Dimension):

    Force (Dimension):

    Energy (Dimension):

    Power (Dimension):

    Charge (Dimension):

    Potential (Dimension):

    Capacitance (Dimension):

    Resistance (Dimension):

    Conductance (Dimension):

    Inductance (Dimension):

    MagneticFlux (Dimension):

    MagneticBField (Dimension):

    LuminousFlux (Dimension):

    Illuminance (Dimension):

    RadioactiveDose (Dimension):

    Catalysis (Dimension):



Attributes: Base Prefixes

    IdentityPrefix (Prefix): represents the number 1, expressed as the prefix 0⁰


Attributes: Base Units

    One (Unit): represents the number 1, expressed as a unit of dimension `Number`

"""

import functools
import operator
import sys
from collections import defaultdict
from functools import lru_cache, reduce, total_ordering
from importlib.metadata import version
from math import log
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    Generator,
    Iterable,
    List,
    Mapping,
    Optional,
    Set,
    Tuple,
    Union,
    cast,
    overload,
)

from . import _parser
from .formatting import from_superscript, superscript

if sys.version_info < (3, 9):  # pragma: no cover
    # math.gcd changed in Python 3.8 from a two-argument for to a variable argument form
    import math

    from typing_extensions import SupportsIndex

    def recursive_gcd(*integers: SupportsIndex) -> int:
        if len(integers) <= 2:
            return math.gcd(*integers)
        return math.gcd(integers[0], gcd(*integers[1:]))

    gcd = recursive_gcd

else:  # pragma: no cover
    from math import gcd


try:
    from icecream import ic
except ImportError:  # pragma: no cover
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa


__version__ = version("measured")

NUMERIC_CLASSES = (int, float)
Numeric = Union[int, float]


class FractionalDimensionError(ValueError):
    """Raised when computing the nth root of a Dimension, Prefix, or Unit would result
    in a non-integer dimesion"""

    def __init__(self, degree: int, value: Union["Dimension", "Prefix", "Unit"]):
        super().__init__(
            f"Taking the root of degree {degree} of {value} would "
            "result in a fractional exponent"
        )


class Dimension:
    """Dimension represents the kind of physical quantity being measured.

    Unless you're doing something really cool, you probably won't instantiate new
    dimensions directly.  Instead, you'll import the base dimensions and combine them
    through multiplication, division, or exponentation.

    Attributes:
        name (Optional[str]): The name of this dimension, which may not be set in the
            case of complex dimensions

        symbol (Optional[str]): The conventional [dimensional
            analysis](https://en.wikipedia.org/wiki/Dimensional_analysis#Definition)
            symbol of this dimension

        exponents (Tuple[int, ...]): The exponents that define this dimension in terms
            of the fundamental dimensions

    Examples:

        >>> from measured import (
        ...     Number,
        ...     Length,
        ...     Time,
        ...     Mass,
        ...     Current,
        ...     Temperature,
        ...     AmountOfSubstance,
        ...     LuminousIntensity,
        ...     Information
        ... )
        >>> Length.symbol
        'L'
        >>> Length.name
        'length'

        These dimensions form the basis for more complex dimensions, which can be
        produced through multiplication, exponentation, and division.

        >>> from measured import Area, Volume, Frequency, Speed
        >>> assert Area == Length * Length
        >>> assert Volume == Length**3
        >>> assert Speed == Length / Time
        >>> assert Frequency == Number / Time

        `measured` attempts to maintain Dimensions as singletons, so they can be used in
        both equality and identity tests.

        >>> assert Volume is Length**3

        Dimensions are hashable and may be used as keys in dictionaries.

        >>> lookup = {Volume: 'spacious'}
        >>> lookup[Volume]
        'spacious'

        Dimensions can be serialized in a number of ways, preserving their identity.

        >>> import pickle
        >>> assert pickle.loads(pickle.dumps(Volume)) is Volume

        >>> import json
        >>> from measured.json import MeasuredJSONEncoder, MeasuredJSONDecoder
        >>> json.dumps(Length, cls=MeasuredJSONEncoder)
        '{"__measured__": "Dimension", "name": "length", "symbol": "L", ...}'

        While using `measured`'s [JSON codecs][measured.json], Dimensions may be
        deserialized directly from that JSON representation.

        >>> encoded = json.dumps(Length, cls=MeasuredJSONEncoder)
        >>> json.loads(encoded, cls=MeasuredJSONDecoder)
        Dimension(exponents=(0, 1, 0, 0, 0, 0, 0, 0, 0, 0), name='length', symbol='L')

        With measured's JSON codecs installed, you can omit passing the encoder and
        decoder.

        >>> from measured.json import codecs_installed
        >>> with codecs_installed():
        ...     assert json.loads(json.dumps(Volume)) is Volume
    """

    _known: ClassVar[Dict[Tuple[int, ...], "Dimension"]] = {}
    _initialized: bool = False

    _fundamental: ClassVar[List["Dimension"]] = []
    _by_name: ClassVar[Dict[str, "Dimension"]] = {}

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

        if name:
            self._by_name[name] = self

    @classmethod
    def fundamental(cls) -> Iterable["Dimension"]:
        """Returns the registered fundamental dimensions

        Fundamental dimensions are not derived from other dimensions, and they will
        always have an `exponents` tuple with a single `1`, like `[0, 0, 1, 0, 0...]`
        (except for `Number`, which is all `0`s).

        The fundamental dimensions are those defined directly using
        [`Dimension.define`][measured.Dimension.define], like those provided by
        `measured`.  The length and order of these Dimensions is also the length and
        order of each Dimensions `exponents` tuple.
        """
        return list(cls._fundamental)

    @classmethod
    def define(cls, name: str, symbol: str) -> "Dimension":
        """Defines a new fundamental Dimension

        Used by `measured` itself to define the fundamental Dimensions.  You may define
        additional dimensions, but be aware that doing so will change the cardinality of
        the `exponents` tuple for _all_ defined Dimensions.
        """
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

    @classmethod
    def derive(
        cls, dimension: "Dimension", name: str, symbol: Optional[str] = None
    ) -> "Dimension":
        """Registers a new named dimension derived from other dimension"""
        dimension.name = name
        dimension.symbol = symbol or str(dimension)
        cls._by_name[name] = dimension
        return dimension

    def unit(self, name: str, symbol: str) -> "Unit":
        """Define a new unit of this dimension"""
        return Unit.define(self, name, symbol)

    # Pickle support

    def __getnewargs_ex__(self) -> Tuple[Tuple[Tuple[int, ...]], Dict[str, Any]]:
        return (self.exponents,), {}

    # JSON support

    def __json__(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "symbol": self.symbol,
            "exponents": list(self.exponents),
        }

    @classmethod
    def __from_json__(cls, json_object: Dict[str, Any]) -> "Dimension":
        return Dimension(tuple(json_object["exponents"]))

    # Pydantic support

    @classmethod
    def __get_validators__(
        cls,
    ) -> Generator[Callable[[Union[str, "Dimension"]], "Dimension"], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: Union[str, "Dimension"]) -> "Dimension":
        if isinstance(value, str):
            if value not in cls._by_name:
                raise ValueError(f"{value!r} is not a named Dimension")

            return cls._by_name[value]

        if isinstance(value, Dimension):
            return value

        raise ValueError(f"No conversion from {value!r} to Dimension")

    def __repr__(self) -> str:
        return (
            "Dimension("
            f"exponents={self.exponents!r}, "
            f"name={self.name!r}, symbol={self.symbol!r}"
            ")"
        )

    def __str__(self) -> str:
        if self.symbol:
            return self.symbol

        return (
            "⋅".join(
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

    @staticmethod
    @lru_cache(maxsize=None)
    def _multiply(self: "Dimension", other: "Dimension") -> "Dimension":
        return Dimension(tuple(s + o for s, o in zip(self.exponents, other.exponents)))

    def __mul__(self, other: "Dimension") -> "Dimension":
        if not isinstance(other, Dimension):
            return NotImplemented

        return Dimension._multiply(self, other)

    @staticmethod
    @lru_cache(maxsize=None)
    def _divide(self: "Dimension", other: "Dimension") -> "Dimension":
        return Dimension(tuple(s - o for s, o in zip(self.exponents, other.exponents)))

    def __truediv__(self, other: "Dimension") -> "Dimension":
        if not isinstance(other, Dimension):
            return NotImplemented

        return Dimension._divide(self, other)

    def __pow__(self, power: int) -> "Dimension":
        if not isinstance(power, int):
            return NotImplemented

        return Dimension(tuple(s * power for s in self.exponents))

    def root(self, degree: int) -> "Dimension":
        """Returns the nth root of this Dimension"""
        if not isinstance(degree, int):
            raise TypeError(f"degree should be an integer, not {type(degree)}")

        if degree == 0:
            return Number

        if any(s // degree != s / degree for s in self.exponents):
            raise FractionalDimensionError(degree, self)

        return Dimension(tuple(s // degree for s in self.exponents))

    @functools.lru_cache(maxsize=None)
    def as_ratio(self) -> Tuple["Dimension", "Dimension"]:
        """Returns this dimension, split into a numerator and denominator"""
        numerator = tuple(e if e >= 0 else 0 for e in self.exponents)
        denominator = tuple(-e if e < 0 else 0 for e in self.exponents)
        return Dimension(numerator), Dimension(denominator)

    def is_factor(self, other: "Dimension") -> bool:
        """Returns true if this dimension is a factor of the other dimension"""
        if self is other or self is Number:
            return True

        exponents = [
            i
            for i, (mine, theirs) in enumerate(zip(self.exponents, other.exponents))
            if (theirs and mine) and theirs >= mine
        ]
        return bool(exponents)


class Prefix:
    """Prefixes scale a [`Unit`][measured.Unit] up or down by a constant factor.

    Prefixes are defined in systems of factors with a common integer base, and
    successive positive and/or negative exponents, like the SI system of prefixes using
    base 10 (micro, milli, kilo, mega, etc) or the IEC system of binary prefixes (kibi,
    mebi, gibi, etc).

    Attributes:

        base (int): The base of the system, like `10` for the SI system
        exponent (int | float): The exponent that the base is raised to

    Examples:

        Prefixes have a base and an exponent:

        >>> from measured.si import Milli, Kilo
        >>> Milli.symbol, Milli.base, Milli.exponent
        ('m', 10, -3)
        >>> Kilo.symbol, Kilo.base, Kilo.exponent
        ('k', 10, 3)

        Prefixes can be multiplied by numbers, Prefixes, and Units:

        >>> from measured.si import Kilo, Mega, Meter
        >>> assert 1 * Kilo * Meter == 1000 * Meter
        >>> assert 1 * (Kilo * Kilo * Meter) == 1 * Mega * Meter

        Prefixes can be divided by Prefixes and other prefixed units:

        >>> from measured.si import Kilo, Mega, Meter, Second
        >>> assert (1 * Mega * Meter) / (1 * Kilo * Second) == 1000 * Meter / Second

        Prefixes can be raised to an exponent:

        >>> from measured.si import Kilo, Mega, Meter
        >>> assert (2 * Kilo * Meter)**2 == 4 * Mega * Meter**2

        Prefixes can translate between bases, although be careful with the loss of
        precision during this conversion:

        >>> from measured.si import Kilo
        >>> from measured.iec import Mebi, Bit
        >>> assert 1 * Mebi * Bit == 1048.576 * Kilo * Bit

    """

    _known: ClassVar[Dict[Tuple[int, Numeric], "Prefix"]] = {}
    _initialized: bool = False

    _by_name: ClassVar[Dict[str, "Prefix"]] = {}
    _by_symbol: ClassVar[Dict[str, "Prefix"]] = {}

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

        if name:
            self._by_name[name] = self
        if symbol:
            self._by_symbol[symbol] = self

    # Pickle support

    def __getnewargs_ex__(self) -> Tuple[Tuple[int, Numeric], Dict[str, Any]]:
        return (self.base, self.exponent), {}

    # JSON support

    def __json__(self) -> Dict[str, Any]:
        return {
            "base": self.base,
            "exponent": self.exponent,
            "name": self.name,
            "symbol": self.symbol,
        }

    @classmethod
    def __from_json__(cls, json_object: Dict[str, Any]) -> "Prefix":
        return Prefix(json_object["base"], json_object["exponent"])

    # Pydantic support

    @classmethod
    def __get_validators__(
        cls,
    ) -> Generator[Callable[[Union[str, "Prefix"]], "Prefix"], None, None]:
        yield cls.validate

    @classmethod
    def resolve_symbol(cls, symbol: str) -> "Prefix":
        """Returns the Prefix with the given symbol"""
        return cls._by_symbol[symbol]

    @classmethod
    def validate(cls, value: Union[str, "Prefix"]) -> "Prefix":
        if isinstance(value, str):
            if value not in cls._by_name:
                raise ValueError(f"{value!r} is not a named Prefix")

            return cls._by_name[value]

        if isinstance(value, Prefix):
            return value

        raise ValueError(f"No conversion from {value!r} to Prefix")

    def __repr__(self) -> str:
        return f"Prefix(base={self.base!r}, exponent={self.exponent!r})"

    def __str__(self) -> str:
        if self.symbol:
            return self.symbol
        if self.exponent == 0:
            return ""
        return f"{self.base}{superscript(self.exponent)}"

    def quantify(self) -> Numeric:
        return cast(Numeric, self.base**self.exponent)

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

    def root(self, degree: int) -> "Prefix":
        """Returns the nth root of this Prefix"""
        if not isinstance(degree, int):
            raise TypeError(f"degree should be an integer, not {type(degree)}")

        if degree == 0:
            return IdentityPrefix

        if self.exponent // degree != self.exponent / degree:
            raise FractionalDimensionError(degree, self)

        return Prefix(self.base, int(self.exponent // degree))


class Unit:
    """Unit is a predetermined reference amount or definition for a measurable quantity

    `measured` includes a number of well-known units, and additional contributions are
    always welcome.  The SI system of units is covered in the [`measured.si`][] package.

    Attributes:

        name (Optional[str]): the name of this unit, which may not be set in the case
            of complex derived units

        symbol (Optional[str]): the symbol of this unit, which may not be set in the
            case of complex derived units

        prefix (Prefix): the prefix to multiply this unit by (`IdentityPrefix` for
            unprefixed units)

        factors (Mapping["Unit", int]): a mapping of the base units and their powers
            that make up a compound unit, or `{self: 1}` for base units

    Examples:

        >>> from measured import Length, Time, Speed
        >>> from measured.si import Meter, Second
        >>> Meter.name, Meter.symbol
        ('meter', 'm')

        >>> meter_per_second = Meter / Second
        >>> assert meter_per_second.dimension is Speed
        >>> assert meter_per_second.dimension is Length / Time
        >>> meter_per_second.name, meter_per_second.symbol
        (None, None)

        >>> back_to_meter = (meter_per_second * Second)
        >>> back_to_meter.name, back_to_meter.symbol
        ('meter', 'm')

        >>> assert Meter.factors == {Meter: 1}
        >>> assert Second.factors == {Second: 1}
        >>> assert meter_per_second.factors == {Meter: 1, Second: -1}


        [`Unit`][measured.Unit] values define format specifiers to control how they are
        formatted as strings:

        >>> from measured.si import Meter, Second
        >>> str(Meter / Second)
        'm⋅s⁻¹'
        >>> f"{Meter / Second}"
        'm⋅s⁻¹'
        >>> f"{Meter**2 / Second**2}"
        'm²⋅s⁻²'

        The `/` format specifier presents the unit as a ratio:

        >>> f"{Meter / Second:/}"
        'm/s'
        >>> f"{Meter**2/Second:/}"
        'm²/s'
        >>> f"{Meter**2/Second**2:/}"
        'm²/s²'
    """

    UnitKey = Tuple[Prefix, Tuple[Tuple["Unit", int], ...]]

    _known: ClassVar[Dict[UnitKey, "Unit"]] = {}
    _initialized: bool = False

    _base: ClassVar[Set["Unit"]] = set()
    _by_name: ClassVar[Dict[str, "Unit"]] = {}
    _by_symbol: ClassVar[Dict[str, "Unit"]] = {}

    prefix: Prefix
    factors: Mapping["Unit", int]
    name: Optional[str]
    names: List[str]
    symbol: Optional[str]
    symbols: List[str]

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

        if name and name in cls._by_name:
            return cls._by_name[name]

        self = super().__new__(cls)
        if not factors:
            key = cls._build_key(prefix, {self: 1})
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
        self.name = None
        self.symbol = None
        self.names = []
        self.symbols = []
        self.alias(name=name, symbol=symbol)
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
        if name in cls._by_name:
            raise ValueError(f"A unit named {name} is already defined")

        if symbol in cls._by_symbol:
            raise ValueError(f"A unit with symbol {symbol} is already defined")

        unit = cls(IdentityPrefix, {}, dimension, name, symbol)
        cls._base.add(unit)
        return unit

    @classmethod
    def derive(cls, unit: "Unit", name: str, symbol: str) -> "Unit":
        """Registers a new named unit derived from other units"""
        unit.alias(name=name, symbol=symbol)
        return unit

    @classmethod
    def named(cls, name: str) -> "Unit":
        """Returns the unit with the given name"""
        return cls._by_name[name]

    @classmethod
    def resolve_symbol(cls, symbol: str) -> "Unit":
        """Returns the unit with the given (possibly prefixed) symbol"""
        if symbol in cls._by_symbol:
            return cls._by_symbol[symbol]

        for i in range(1, len(symbol)):
            try:
                prefix = Prefix.resolve_symbol(symbol[:i])
                unit = cls._by_symbol[symbol[i:]]
            except KeyError:
                continue

            return prefix * unit

        if symbol in cls._by_name:
            return cls._by_name[symbol]

        raise KeyError(f"No unit (or prefixed unit) matching {symbol!r}")

    def equals(self, other: "Quantity") -> None:
        """Defines a conversion between this Unit and another"""
        if other.unit == self and self is not One:
            raise ValueError("No need to define conversions for a unit and itself")
        conversions.equate(1 * self, other)

    def zero(self, zero: "Quantity") -> None:
        """Defines this unit as a scale with a zero point at another Quantity"""
        if zero.unit == self:
            raise ValueError("No need to define conversions for a unit and itself")
        conversions.translate(self, zero)

    def alias(self, name: Optional[str] = None, symbol: Optional[str] = None) -> None:
        """Adds an alternative name and/or symbol to the unit"""
        if name:
            if name in self._by_name and self._by_name[name] is not self:
                raise ValueError(f"A unit named {name} is already defined")

            if not self.name:
                self.name = name

            self.names.append(name)
            self._by_name[name] = self

        if symbol:
            if symbol in self._by_symbol and self._by_symbol[symbol] is not self:
                raise ValueError(f"A unit with symbol {symbol} is already defined")

            if symbol and " " in symbol:
                raise ValueError(f"{symbol!r} will not be parsable if it has spaces.")

            if not self.symbol:
                self.symbol = symbol

            self.symbols.append(symbol)
            self._by_symbol[symbol] = self

    # Pickle support

    def __getnewargs_ex__(
        self,
    ) -> Tuple[Tuple[Prefix, Mapping["Unit", int], Dimension], Dict[str, Any]]:
        factors = {} if self.factors == {self: 1} else self.factors
        args = (self.prefix, factors, self.dimension)
        kwargs = {"name": self.name, "symbol": self.symbol}
        return args, kwargs

    # JSON support

    def __json__(self) -> Dict[str, Any]:
        prefix, factors = self._build_key(self.prefix, self.factors)
        return {
            "name": self.name,
            "symbol": self.symbol,
            "dimension": self.dimension,
            "prefix": prefix if prefix.quantify() != 1 else None,
            "factors": None if factors == ((self, 1),) else factors,
        }

    @classmethod
    def __from_json__(cls, json_object: Dict[str, Any]) -> "Unit":
        if not json_object["factors"]:
            return cls._by_name[json_object["name"]]
        prefix = json_object["prefix"] or Prefix(0, 0)
        factors = dict(json_object["factors"])
        dimension = json_object["dimension"]
        return Unit(prefix, factors, dimension)

    # Pydantic support

    @classmethod
    def __get_validators__(
        cls,
    ) -> Generator[Callable[[Union[str, "Unit"]], "Unit"], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: Union[str, "Unit"]) -> "Unit":
        if isinstance(value, str):
            if value not in cls._by_name:
                raise ValueError(f"{value!r} is not a named Unit")

            return cls._by_name[value]

        if isinstance(value, Unit):
            return value

        raise ValueError(f"No conversion from {value!r} to Unit")

    def scale(self, prefix: Prefix) -> "Unit":
        """Given a Prefix, creates a new unit scaled by that Prefix"""
        return self.__class__(self.prefix * prefix, self.factors, self.dimension)

    @lru_cache(maxsize=None)
    def quantify(self) -> "Quantity":
        """Produce a Quantity of this Unit, including the Prefix.

        Examples:

            >>> from measured.si import Kilo, Meter
            >>> assert Kilo * Meter != 1000 * Meter
            >>> assert 1 * Kilo * Meter == 1000 * Meter
            >>> assert (Kilo * Meter).quantify() == 1000 * Meter
        """
        return self.prefix.quantify() * Unit(
            IdentityPrefix, self.factors, self.dimension
        )

    def __repr__(self) -> str:
        if self.name:
            return f"Unit.named({self.name!r})"

        return (
            "Unit("
            f"prefix={self.prefix!r}, "
            f"factors={self.factors!r}, "
            f"dimension={self.dimension!r}, "
            f"name={self.name!r}, symbol={self.symbol!r}"
            ")"
        )

    @classmethod
    def parse(cls, string: str) -> "Unit":
        """
        Parses a unit from a string.

        Examples:

            It is important to import any modules of units you will be parsing.  Units
            and their symbols are registered when they are first imported and created.

            >>> from measured import Unit, si

            Integer and floating point quantities can be parsed, along with units of
            any complexity.

            >>> meter_per_second = Unit.parse('m/s')
            >>> meter_per_second.dimension is Speed
            True
            >>> amperes_cubed_per_area = Unit.parse('A³/m²')
            >>> from measured.si import Meter, Ampere
            >>> amperes_cubed_per_area is Ampere**3/Meter**2
            True
            >>> str(amperes_cubed_per_area)
            'A³⋅m⁻²'

            Measured can parse any unit in the same format it produces with `str`, but
            also understands easier-to-type versions:

            >>> assert Unit.parse('m^2/s') == Unit.parse('m²⋅s⁻¹')
            >>> assert Unit.parse('m^2*s') == Unit.parse('m²⋅s')
        """
        return cast(Unit, parser.parse(string, start="unit"))

    def __str__(self) -> str:
        if self.symbol:
            return f"{self.prefix}{self.symbol}"

        return str(self.prefix) + "⋅".join(
            f"{unit.prefix}{unit.symbol}{superscript(exponent)}"
            for unit, exponent in self.factors.items()
        )

    def __format__(self, format_specifier: str) -> str:
        if not format_specifier:
            return str(self)

        if format_specifier == "/":
            numerator, denominator = self.as_ratio()
            if denominator == One:
                return str(self)
            return str(numerator) + "/" + str(denominator)

        raise ValueError(f"Unrecognized format specifier {format_specifier!r}")

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

    @staticmethod
    @lru_cache(maxsize=None)
    def _multiply(self: "Unit", other: "Unit") -> "Unit":
        dimension = self.dimension * other.dimension
        prefix = self.prefix * other.prefix

        factors: Dict["Unit", int] = defaultdict(int, self.factors)
        for unit, exponent in other.factors.items():
            factors[unit] += exponent
        factors = self._simplify(factors)

        return Unit(prefix, factors, dimension)

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

        return Unit._multiply(self, other)

    __rmul__ = __mul__

    @staticmethod
    @lru_cache(maxsize=None)
    def _divide(self: "Unit", other: "Unit") -> "Unit":
        dimension = self.dimension / other.dimension
        prefix = self.prefix / other.prefix

        factors: Dict["Unit", int] = defaultdict(int, self.factors)
        for unit, exponent in other.factors.items():
            factors[unit] -= exponent
        factors = self._simplify(factors)

        return Unit(prefix, factors, dimension)

    def __truediv__(self, other: "Unit") -> "Unit":
        if not isinstance(other, Unit):
            return NotImplemented

        return Unit._divide(self, other)

    def __pow__(self, power: int) -> "Unit":
        if not isinstance(power, int):
            return NotImplemented

        dimension = self.dimension**power
        prefix = self.prefix**power

        factors = self._simplify(
            {unit: exponent * power for unit, exponent in self.factors.items()}
        )
        return Unit(prefix, factors, dimension)

    def root(self, degree: int) -> "Unit":
        """Returns the nth root of this Unit"""
        if not isinstance(degree, int):
            raise TypeError(f"degree should be an integer, not {type(degree)}")

        if degree == 0:
            return One

        dimension = self.dimension.root(degree)
        prefix = self.prefix.root(degree)

        if any(
            exponent // degree != exponent / degree
            for unit, exponent in self.factors.items()
            if exponent > 0 and unit is not One
        ):
            raise FractionalDimensionError(degree, self)

        factors = self._simplify(
            {unit: int(exponent // degree) for unit, exponent in self.factors.items()}
        )
        return Unit(prefix, factors, dimension)

    @functools.lru_cache(maxsize=None)
    def as_ratio(self) -> Tuple["Unit", "Unit"]:
        """Returns this unit, split into a numerator and denominator"""
        numerator, denominator = self.dimension.as_ratio()
        return (
            Unit(
                self.prefix,
                {u: e for u, e in self.factors.items() if e >= 0} or {One: 1},
                numerator,
            ),
            Unit(
                IdentityPrefix,
                {u: -e for u, e in self.factors.items() if e < 0} or {One: 1},
                denominator,
            ),
        )


class ConversionNotFound(ValueError):
    pass


@total_ordering
class Quantity:
    """Quantity represents a quantity of some Unit

    Attributes:

        magnitude (int | float): the quantity

        unit (Unit): the [`Unit`][measured.Unit]

    Examples:

        All of the arithmetic operations are supported between Quantities.
        Multiplication and division with [`Unit`][measured.Unit], `int`, and `float`
        are also supported.

        >>> from measured.si import Meter, Second
        >>> assert 2 * Meter + 3 * Meter == 5 * Meter
        >>> assert 3 * Meter - 1 * Meter == 2 * Meter
        >>> assert (2 * Meter) / (1 * Second) == 2 * Meter / Second
        >>> assert 10 * Meter / 2 == 5 * Meter
        >>> assert 10 * Meter * 2 == 20 * Meter
        >>> assert (10 * Meter)**2 == 100 * Meter**2

        Keep an eye on Python's operator precedence, which may lead to surprising
        results.  Consider the following:

        >>> assert (2 * Meter / 1 * Second) != (2 * Meter) / (1 * Second)

        In the above example, the order of operations on the left is:

        * `2 * Meter` → `Quantity(2, Meter)`
        * `Quantity(2, Meter) / 1` → `Quantity(2, Meter)`
        * `Quantity(2, Meter) * Second` → `Quantity(2, Meter * Second)`

        But on the right, the order is:

        * `2 * Meter` → `Quantity(2, Meter)`
        * `1 * Second` → `Quantity(1, Second)`
        * `Quantity(2, Meter) / Quantity(1, Second)` → `Quantity(2, Meter / Second)`

        [`Quantity`][measured.Quantity] values define format specifiers to control how
        they are formatted as strings:

        >>> from measured.si import Meter, Second
        >>> str(5 * Meter / Second)
        '5 m⋅s⁻¹'
        >>> f"{5 * Meter / Second}"
        '5 m⋅s⁻¹'
        >>> f"{5 * Meter**2 / Second**2}"
        '5 m²⋅s⁻²'

        When formatting a [`Quantity`][measured.Quantity], you can specify two separate
        format specifiers, separated by a `:`.  The first specifier is used to format
        the `magnitude`, and the second is used to format the `unit` (see
        [`Unit`][measured.Unit] for more information about the available specifiers).

        Specifying both the magnitude and unit format:

        >>> f"{5.1234 * Meter / Second:.2f:/}"
        '5.12 m/s'

        Specifying only the magnitude's format:

        >>> f"{5.1234 * Meter / Second:.2f}"
        '5.12 m⋅s⁻¹'

        Specifying only the unit's format:

        >>> f"{5.1234 * Meter / Second::/}"
        '5.1234 m/s'

    """

    def __init__(self, magnitude: Numeric, unit: Unit):
        self.magnitude = magnitude
        self.unit = unit

    def in_base_units(self) -> "Quantity":
        """Reduces this Quantity into a new Quantity expressed only in base units
        without any Prefixes"""
        return self.magnitude * self.unit.quantify()

    def in_unit(self, other: Unit) -> "Quantity":
        """Convert this Quantity into another unit"""
        return conversions.convert(self, other)

    # JSON support

    def __json__(self) -> Dict[str, Any]:
        return {
            "magnitude": self.magnitude,
            "unit": self.unit,
        }

    @classmethod
    def __from_json__(cls, json_object: Dict[str, Any]) -> "Quantity":
        return Quantity(json_object["magnitude"], json_object["unit"])

    # Pydantic support

    @classmethod
    def __get_validators__(
        cls,
    ) -> Generator[Callable[["Quantity"], "Quantity"], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: Union[str, "Quantity"]) -> "Quantity":
        if isinstance(value, Quantity):
            return value

        raise ValueError(f"No conversion from {value!r} to Quantity")

    def __repr__(self) -> str:
        return f"Quantity(magnitude={self.magnitude!r}, unit={self.unit!r})"

    @classmethod
    def parse(cls, string: str) -> "Quantity":
        """
        Parses a quantity from a string.

        Examples:

            It is important to import any modules of units you will be parsing.  Units
            and their symbols are registered when they are first imported and created.

            >>> from measured import Quantity, si

            Integer and floating point quantities can be parsed, along with units of
            any complexity.

            >>> distance = Quantity.parse('5200 m')
            >>> speed = Quantity.parse('5.2e2 m/s')
            >>> time = distance / speed
            >>> str(time)
            '10.0 s'
            >>> amperes_cubed_per_area = Quantity.parse('2 A³/m²')
            >>> str(amperes_cubed_per_area)
            '2 A³⋅m⁻²'

            Measured can parse any unit in the same format it produces with `str`, but
            also understands easier-to-type versions:

            >>> assert Quantity.parse('2 m^2/s') == Quantity.parse('2 m²⋅s⁻¹')
            >>> assert Quantity.parse('2 m^2*s') == Quantity.parse('2 m²⋅s')
        """
        return cast(Quantity, parser.parse(string, start="quantity"))

    def __str__(self) -> str:
        return f"{self.magnitude} {self.unit}"

    def __format__(self, format_specifier: str) -> str:
        magnitude_format, _, unit_format = format_specifier.partition(":")
        return (
            self.magnitude.__format__(magnitude_format)
            + " "
            + self.unit.__format__(unit_format)
        )

    def __add__(self, other: "Quantity") -> "Quantity":
        if isinstance(other, Quantity):
            other = other.in_unit(self.unit)
            return Quantity(self.magnitude + other.magnitude, self.unit)

        return NotImplemented

    def __sub__(self, other: "Quantity") -> "Quantity":
        if isinstance(other, Quantity):
            other = other.in_unit(self.unit)
            return Quantity(self.magnitude - other.magnitude, self.unit)

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

    def root(self, degree: int) -> "Quantity":
        """Returns the nth root of this Quantity"""
        if degree == 0:
            return 1 * One
        return Quantity(self.magnitude ** (1 / degree), self.unit.root(degree))

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

        if this.unit == other.unit:
            return this.magnitude == other.magnitude

        try:
            return this.in_unit(other.unit) == other
        except ConversionNotFound:
            return NotImplemented

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Quantity):
            return NotImplemented

        if self.unit.dimension != other.unit.dimension:
            return NotImplemented

        this = self.in_base_units()
        other = other.in_base_units()

        if this.unit == other.unit:
            return this.magnitude < other.magnitude

        try:
            return this.in_unit(other.unit) < other
        except ConversionNotFound:
            return NotImplemented

    def _approximation(self, other: "Quantity") -> Union[Numeric, bool]:
        if self == other:
            return True

        if self.unit.dimension != other.unit.dimension:
            return False

        this = self.in_base_units()
        other = other.in_base_units()

        if this.unit != other.unit:
            try:
                this = this.in_unit(other.unit)
            except ConversionNotFound:
                return False

        if other.magnitude == 0:
            ratio = this.magnitude
        else:
            ratio = 1 - this.magnitude / other.magnitude

        return abs(ratio)

    def approximates(self, other: "Quantity", within: float = 1e-6) -> bool:
        """Indicates whether this Quantity and another Quantity are close enough to
        each other to be considered equal.

        Parameters:
            other (Quantity): the other quantity to compare this quantity to
            within (float): the tolerance as a ratio; e.g. 5% would be within=0.05

        Examples:

            >>> from measured.si import Meter
            >>> assert (0.001 * Meter).approximates(0.002 * Meter, within=0.5)
            >>> assert not (0.001 * Meter).approximates(0.002 * Meter, within=0.01)
        """
        approximation = self._approximation(other)
        if approximation is True or approximation is False:
            return approximation

        return bool(approximation <= within)

    def assert_approximates(self, other: "Quantity", within: float = 1e-6) -> None:
        """Asserts whether this Quantity and another Quantity are close enough to
        each other to be considered equal, with a helpful assertion message

        Parameters:
            other (Quantity): the other quantity to compare this quantity to
            within (float): the tolerance as a ratio; e.g. 5% would be within=0.05

        Examples:

            >>> from measured.si import Meter
            >>> (0.001 * Meter).assert_approximates(0.002 * Meter, within=0.5)
        """
        left = self.in_base_units()
        right = other.in_base_units()

        approximation = self._approximation(other)
        if approximation is True:
            return

        assert approximation

        message = " or ".join(
            [
                f"{left} !~ {right.in_unit(left.unit)}",
                f"{right} !~ {left.in_unit(right.unit)}",
            ]
        )

        message += f" (off by {approximation})"
        assert approximation <= within, message


ParseError = _parser.LarkError


class QuantityTransformer(_parser.Transformer[Any, "Quantity"]):
    inline = _parser.v_args(inline=True)

    @inline
    def unit(self, numerator: Unit, denominator: Optional[Unit] = None) -> Unit:
        return numerator / (denominator or One)

    @inline
    def unit_sequence(self, *terms: Unit) -> Unit:
        return reduce(operator.mul, terms)

    @inline
    def term(self, symbol: str, exponent: int = 1) -> Unit:
        return Unit.resolve_symbol(symbol) ** exponent

    @inline
    def carat_exponent(self, exponent: str) -> int:
        return int(exponent[1:])

    @inline
    def superscript_exponent(self, exponent: str) -> int:
        value = from_superscript(exponent)
        assert isinstance(value, int)
        return value

    @inline
    def quantity(self, magnitude: Numeric, unit: Unit) -> "Quantity":
        return Quantity(magnitude, unit)

    int = inline(int)
    float = inline(float)


parser: _parser.Lark = _parser.Parser(transformer=QuantityTransformer())  # type: ignore


Ratio = Numeric
Offset = Numeric


class ConversionTable:
    _ratios: Dict[Unit, Dict[Unit, Ratio]]
    _offsets: Dict[Unit, Dict[Unit, Offset]]

    def __init__(self) -> None:
        self._ratios = defaultdict(dict)
        self._offsets = defaultdict(dict)

    def equate(self, a: Quantity, b: Quantity) -> None:
        """Defines a conversion between one Unit and another, expressed as a ratio
        between the two."""

        if a.unit == b.unit and a.unit is not One:
            raise ValueError("No need to define conversions for a unit and itself")

        a = a.in_base_units()
        b = b.in_base_units()

        self._ratios[a.unit][b.unit] = b.magnitude / a.magnitude
        self._ratios[b.unit][a.unit] = a.magnitude / b.magnitude

    def translate(self, scale: Unit, zero: Quantity) -> None:
        """Defines a unit as a scale starting from the given zero point in another
        unit"""
        if scale == zero.unit:
            raise ValueError("No need to define conversions for a unit and itself")

        degree = zero.unit
        offset = zero.magnitude

        self._ratios[degree][scale] = 1
        self._ratios[scale][degree] = 1

        self._offsets[degree][scale] = -offset
        self._offsets[scale][degree] = +offset

    def convert(self, quantity: Quantity, other_unit: Unit) -> Quantity:
        """Converts the given quantity into another unit, if possible"""
        if quantity.unit.dimension != other_unit.dimension:
            raise ConversionNotFound(
                "No conversion from "
                f"{quantity.unit} ({quantity.unit.dimension}) to "
                f"{other_unit} ({other_unit.dimension})"
            )

        this = quantity.in_base_units()
        other = (1 * other_unit).in_base_units()

        this = this.magnitude * self._collapse_by_dimension(this.unit)
        other = other.magnitude * self._collapse_by_dimension(other.unit)

        this_numerator, this_denominator = this.unit.as_ratio()
        other_numerator, other_denominator = other.unit.as_ratio()

        numerator_path = self._find(this_numerator, other_numerator)
        if not numerator_path:
            raise ConversionNotFound(
                f"No conversion from {this_numerator!r} to {other_numerator!r}"
            )

        denominator_path = self._find(this_denominator, other_denominator)
        if not denominator_path:
            raise ConversionNotFound(
                f"No conversion from {this_denominator!r} to {other_denominator!r}"
            )

        numerator = this.magnitude
        for scale, offset, _ in numerator_path:
            numerator *= scale
            numerator += offset

        denominator = other.magnitude
        for scale, offset, _ in denominator_path:
            denominator *= scale
            denominator += offset

        return Quantity(numerator / denominator, other_unit)

    @lru_cache(maxsize=None)
    def _find(
        self,
        start: Unit,
        end: Unit,
    ) -> Optional[Iterable[Tuple[Ratio, Offset, Unit]]]:
        start_terms = self._terms_by_dimension(start)
        end_terms = self._terms_by_dimension(end)

        assert (
            start_terms.keys() == end_terms.keys()
        ), f"{start_terms.keys()} != {end_terms.keys()}"

        path: List[Tuple[Ratio, Offset, Unit]] = []
        for dimension in start_terms:
            for s, e in zip(start_terms[dimension], end_terms[dimension]):
                this_path = self._find_path(s, e)
                if not this_path:
                    return None
                path += this_path
        return path

    @classmethod
    def _terms_by_dimension(cls, unit: Unit) -> Dict[Dimension, List[Unit]]:
        terms = defaultdict(list)
        for factor, exponent in unit.factors.items():
            factor = factor**exponent
            terms[factor.dimension].append(factor)
        return terms

    @functools.lru_cache(maxsize=None)
    def _collapse_by_dimension(self, unit: Unit) -> Quantity:
        """Return a new quantity with at most a single unit in each dimension, by
        converting individual terms"""
        magnitude: Numeric = 1
        by_dimension: Dict[Dimension, Tuple[Unit, int]] = {}

        # Convert units until there is only one for each dimension
        for unit, exponent in unit.factors.items():
            dimension = unit.dimension
            quantified = unit.quantify()

            if dimension not in by_dimension:
                magnitude *= quantified.magnitude**exponent
                by_dimension[dimension] = (quantified.unit, exponent)
                continue

            current_unit, current_exponent = by_dimension[dimension]

            path = self._find_path(quantified.unit, current_unit)
            if not path:
                raise ConversionNotFound(
                    f"No conversion between {dimension} units {quantified.unit} "
                    f"and {current_unit}"
                )

            for scale, offset, _ in path:
                magnitude *= scale**exponent
                magnitude += offset

            by_dimension[dimension] = (current_unit, current_exponent + exponent)

        # Find any units whose dimensions cancel and try to combine them.  For example,
        # if the factors here are Ampere/Second, that's the same as Coulomb.
        factors = {
            unit: exponent for unit, exponent in by_dimension.values() if exponent != 0
        } or {One: 1}

        to_check = set(factors.keys())

        while to_check:
            this = to_check.pop()
            this_exponent = factors[this]
            for other in to_check:
                other_exponent = factors[other]

                this_term = this**this_exponent
                other_term = other**other_exponent

                if (Number / other_term.dimension).is_factor(this_term.dimension):
                    del factors[this]
                    del factors[other]
                    to_check.discard(other)

                    factors[this_term * other_term] = 1
                    break

        final_dimension = Number
        for dimension in by_dimension.keys():
            final_dimension *= dimension

        return Quantity(magnitude, Unit(IdentityPrefix, factors, final_dimension))

    @lru_cache(maxsize=None)
    def _find_path(
        self,
        start: Unit,
        end: Unit,
    ) -> Optional[List[Tuple[Ratio, Offset, Unit]]]:
        return self._find_path_recursive(start, end)

    def _find_path_recursive(
        self,
        start: Unit,
        end: Unit,
        visited: Optional[Set[Unit]] = None,
    ) -> Optional[List[Tuple[Ratio, Offset, Unit]]]:

        if start is end:
            return [(1, 0, end)]

        if visited is None:
            visited = {start}
        elif start in visited:
            return None
        else:
            visited.add(start)

        exponent, start, end = self._reduce_dimension(start, end)

        if sum(start.factors.values()) > sum(end.factors.values()):
            # This is a conversion like m² -> acre, where the end dimension is defined
            # directly in the higher exponent and there isn't a lower-power unit (e.g.
            # there's no unit that represents the square root of an acre that we can
            # compare the meter to); in this case, perform the search in reverse and it
            # should be able to find available conversions
            backtracked = self._backtrack(self._find_path(end, start), exponent, end)
            return backtracked

        best_path = None

        for intermediate, scale in self._ratios[start].items():
            offset = self._offsets[start].get(intermediate, 0)
            if intermediate == end:
                return [(scale**exponent, offset**exponent, end**exponent)]

            path = self._find_path_recursive(intermediate, end, visited=visited)
            if not path:
                continue

            path = [(scale, offset, intermediate)] + list(path)
            path = [
                (scale**exponent, offset**exponent, unit**exponent)
                for scale, offset, unit in path
            ]
            if not best_path or len(path) < len(best_path):
                best_path = path

        if best_path:
            return best_path

        return None

    @classmethod
    def _reduce_dimension(cls, start: Unit, end: Unit) -> Tuple[int, Unit, Unit]:
        """Reduce the dimension of the given units to their lowest common exponents"""
        assert (
            start.dimension is end.dimension
        ), f"{start} and {end} measure different dimensions"

        if start.dimension is Number:
            return 1, start, end

        exponent = gcd(*start.dimension.exponents)

        try:
            start_root = start.root(exponent)
            end_root = end.root(exponent)
        except FractionalDimensionError:
            return 1, start, end

        return exponent, start_root, end_root

    @classmethod
    def _backtrack(
        cls,
        path: Optional[Iterable[Tuple[Ratio, Offset, Unit]]],
        exponent: int,
        end: Unit,
    ) -> Optional[List[Tuple[Ratio, Offset, Unit]]]:
        """Given a path to convert a start unit to an end unit, produce the reverse
        path, which would convert the end unit to the start unit"""
        if path is None:
            return None

        path = list(reversed(list(path)))

        units = [u for _, _, u in path[1:]] + [end]
        scales_and_offsets = [(s, o) for s, o, _ in path]

        backtracked = [
            (1 / (scale**exponent), -(offset**exponent), unit**exponent)
            for (scale, offset), unit in zip(scales_and_offsets, units)
        ]
        return backtracked


conversions = ConversionTable()


# https://en.wikipedia.org/wiki/Dimensional_analysis#Definition

# Fundamental physical dimensions

Number = Dimension.define(name="number", symbol="1")
Length = Dimension.define(name="length", symbol="L")
Time = Dimension.define(name="time", symbol="T")
Mass = Dimension.define(name="mass", symbol="M")
Temperature = Dimension.define(name="temperature", symbol="Θ")
Charge = Dimension.define(name="charge", symbol="Q")
AmountOfSubstance = Dimension.define(name="amount of substance", symbol="N")
LuminousIntensity = Dimension.define(name="luminous intensity", symbol="J")
Information = Dimension.define(name="information", symbol="B")  # TODO


# Derived dimensions

Area = Dimension.derive(Length * Length, name="area")
Volume = Dimension.derive(Area * Length, name="volume")

PlaneAngle = Length / Length
SolidAngle = Area / Area

# https://en.wikipedia.org/wiki/Fourth,_fifth,_and_sixth_derivatives_of_position

Speed = Dimension.derive(Length / Time, name="speed")
Acceleration = Dimension.derive(Length / Time**2, name="acceleration")
Jerk = Dimension.derive(Length / Time**3, name="jerk")
Snap = Dimension.derive(Length / Time**4, name="snap")
Crackle = Dimension.derive(Length / Time**5, name="crackle")
Pop = Dimension.derive(Length / Time**6, name="pop")

Frequency = Dimension.derive(Number / Time, name="frequency")

# https://en.wikipedia.org/wiki/Newton%27s_laws_of_motion#Second

Force = Dimension.derive(Mass * Acceleration, name="force")
Energy = Dimension.derive(Length * Force, name="energy")
Power = Dimension.derive(Energy / Time, name="power")

Current = Dimension.derive(Charge / Time, name="current")
Potential = Dimension.derive(Energy / Charge, name="potential")
Capacitance = Dimension.derive(Charge / Potential, name="capacitance")
Resistance = Dimension.derive(Potential / Current, name="resistance")
Conductance = Dimension.derive(Current / Potential, name="conductance")
Inductance = Dimension.derive(Potential * Time / Current, name="inductance")

MagneticFlux = Dimension.derive(Potential * Time, name="magnetic flux")
MagneticBField = Dimension.derive(Potential * Time / Area, name="magnetic B-field")

LuminousFlux = LuminousIntensity * SolidAngle
Illuminance = Dimension.derive(LuminousIntensity / Area, name="illuminance")

RadioactiveDose = Dimension.derive(Power / Mass, name="radioactivedose")

Catalysis = Dimension.derive(AmountOfSubstance / Time, name="catalysis")


# Fundamental prefixes

IdentityPrefix = Prefix(0, 0)


# Fundamental units

One = Number.unit(name="one", symbol="1")
One.equals(1 * One)
