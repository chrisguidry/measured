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

    Charge (Dimension): how strongly matter [interacts with the electric field][1]

        [1]: https://en.wikipedia.org/wiki/Electric_charge

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

    Current (Dimension):

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

from collections import defaultdict
from functools import lru_cache, total_ordering
from importlib.metadata import version
from math import log, sqrt
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

from . import formatting

try:
    from icecream import ic as _ic
except ImportError:  # pragma: no cover
    _ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

ic = _ic

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

        `measured` maintains `Dimension` instances as singletons within a single
        process, so they can be used in both equality and identity tests.

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

        While using `measured`'s [JSON codecs](../serialization), Dimensions may be
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
    _initialized: bool

    _fundamental: ClassVar[List["Dimension"]] = []
    _by_name: ClassVar[Dict[str, "Dimension"]] = {}

    __slots__ = ("_initialized", "exponents", "name", "symbol")

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
        self._initialized = False
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

    def scale(self, zero: "Quantity", name: str, symbol: str) -> "Unit":
        """Define a new scale of this dimension, setting a zero point of another unit"""
        unit = self.unit(name, symbol)
        conversions.translate(unit, zero)
        return unit

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

    __repr__ = formatting.dimension_repr
    __str__ = formatting.dimension_str
    _repr_pretty_ = formatting.dimension_pretty
    _repr_html_ = formatting.mathml(formatting.dimension_mathml)

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

    @lru_cache(maxsize=None)
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
    _initialized: bool

    _by_name: ClassVar[Dict[str, "Prefix"]] = {}
    _by_symbol: ClassVar[Dict[str, "Prefix"]] = {}

    __slots__ = ("_initialized", "base", "exponent", "name", "symbol")

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
        if base != 0 and exponent == 0:
            return IdentityPrefix

        key = (base, exponent)
        if key in cls._known:
            return cls._known[key]

        self = super().__new__(cls)
        self._initialized = False
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

    @classmethod
    def resolve_symbol(cls, symbol: str) -> "Prefix":
        """Returns the Prefix with the given symbol"""
        return cls._by_symbol[symbol]

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
    def validate(cls, value: Union[str, "Prefix"]) -> "Prefix":
        if isinstance(value, str):
            if value not in cls._by_name:
                raise ValueError(f"{value!r} is not a named Prefix")

            return cls._by_name[value]

        if isinstance(value, Prefix):
            return value

        raise ValueError(f"No conversion from {value!r} to Prefix")

    __repr__ = formatting.prefix_repr
    __str__ = formatting.prefix_str
    _repr_pretty_ = formatting.prefix_pretty
    _repr_html_ = formatting.mathml(formatting.prefix_mathml)

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
            return Unit(other.prefix * self, other.factors, other.dimension)

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
    always welcome.  The SI system of units is covered in the [`measured.si`](../si)
    package.

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
    _initialized: bool

    _base: ClassVar[Set["Unit"]] = set()
    _by_name: ClassVar[Dict[str, "Unit"]] = {}
    _by_symbol: ClassVar[Dict[str, "Unit"]] = {}

    __slots__ = ("_initialized", "prefix", "factors", "dimension", "names", "symbols")

    prefix: Prefix
    factors: Mapping["Unit", int]
    dimension: Dimension
    names: Tuple[str, ...]
    symbols: Tuple[str, ...]

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
        self._initialized = False
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
        self.names = tuple()
        self.symbols = tuple()
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

    def alias(self, name: Optional[str] = None, symbol: Optional[str] = None) -> None:
        """Adds an alternative name and/or symbol to the unit"""
        if name:
            if name in self._by_name and self._by_name[name] is not self:
                raise ValueError(f"A unit named {name} is already defined")

            self.names = self.names + (name,)
            self._by_name[name] = self

        if symbol:
            if symbol in self._by_symbol and self._by_symbol[symbol] is not self:
                raise ValueError(f"A unit with symbol {symbol} is already defined")

            if symbol and " " in symbol:
                raise ValueError(f"{symbol!r} will not be parsable if it has spaces.")

            self.symbols = self.symbols + (symbol,)
            self._by_symbol[symbol] = self

    @property
    def name(self) -> Optional[str]:
        return self.names[0] if self.names else None

    @property
    def symbol(self) -> Optional[str]:
        return self.symbols[0] if self.symbols else None

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

    __repr__ = formatting.unit_repr
    __str__ = formatting.unit_str
    __format__ = formatting.unit_format
    _repr_pretty_ = formatting.unit_pretty
    _repr_html_ = formatting.mathml(formatting.unit_mathml)

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
            'C³⋅s⁻³⋅m⁻²'

            Measured can parse any unit in the same format it produces with `str`, but
            also understands easier-to-type versions:

            >>> assert Unit.parse('m^2/s') == Unit.parse('m²⋅s⁻¹')
            >>> assert Unit.parse('m^2*s') == Unit.parse('m²⋅s')
        """
        return cast(Unit, parser.parse(string, start="unit"))

    @classmethod
    def _simplify(cls, factors: Mapping["Unit", int]) -> Dict["Unit", int]:
        simplified = {
            unit: exponent
            for unit, exponent in factors.items()
            if unit is not One and exponent != 0
        }
        return simplified or {One: 1}

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

    @lru_cache(maxsize=None)
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

    __slots__ = ("magnitude", "unit")

    magnitude: Numeric
    unit: Unit

    def __init__(self, magnitude: Numeric, unit: Union[Unit, str]):
        self.magnitude = magnitude
        if isinstance(unit, str):
            unit = Unit.parse(unit)
        self.unit = unit

    def unprefixed(self) -> "Quantity":
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

    # SQLAlchemy support

    def __composite_values__(self) -> Tuple[Numeric, str]:
        """
        From the [SQLAlchemy documentation][1]:

            The requirements for the custom datatype class are that it have a
            constructor which accepts positional arguments corresponding to its column
            format, and also provides a method __composite_values__() which returns the
            state of the object as a list or tuple, in order of its column-based
            attributes. It also should supply adequate __eq__() and __ne__() methods
            which test the equality of two instances.

            [1]: https://docs.sqlalchemy.org/en/20/orm/composites.html
        """
        return self.magnitude, str(self.unit)

    __repr__ = formatting.quantity_repr
    __str__ = formatting.quantity_str
    __format__ = formatting.quantity_format
    _repr_pretty_ = formatting.quantity_pretty
    _repr_html_ = formatting.mathml(formatting.quantity_mathml)

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
            '2 C³⋅s⁻³⋅m⁻²'

            Measured can parse any unit in the same format it produces with `str`, but
            also understands easier-to-type versions:

            >>> assert Quantity.parse('2 m^2/s') == Quantity.parse('2 m²⋅s⁻¹')
            >>> assert Quantity.parse('2 m^2*s') == Quantity.parse('2 m²⋅s')
        """
        return cast(Quantity, parser.parse(string, start="quantity"))

    def __hash__(self) -> int:
        return hash((self.magnitude, self.unit))

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

    def __mul__(self, other: Union["Quantity", "Unit", Numeric]) -> "Quantity":
        if isinstance(other, Unit):
            return Quantity(self.magnitude, self.unit * other)

        if isinstance(other, Quantity):
            return Quantity(self.magnitude * other.magnitude, self.unit * other.unit)

        if isinstance(other, NUMERIC_CLASSES):
            return Quantity(self.magnitude * other, self.unit)

        return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other: Union["Quantity", "Unit", Numeric]) -> "Quantity":
        if isinstance(other, Unit):
            return Quantity(self.magnitude, self.unit / other)

        if isinstance(other, Quantity):
            return Quantity(self.magnitude / other.magnitude, self.unit / other.unit)

        if isinstance(other, NUMERIC_CLASSES):
            return Quantity(self.magnitude / other, self.unit)

        return NotImplemented

    def __rtruediv__(self, other: Numeric) -> "Quantity":
        if isinstance(other, NUMERIC_CLASSES):
            return Quantity(other / self.magnitude, self.unit)

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
        if isinstance(other, Level):
            other = other.quantify()

        if not isinstance(other, Quantity):
            return NotImplemented

        if self.unit.dimension != other.unit.dimension:
            return NotImplemented

        this = self.unprefixed()
        other = other.unprefixed()

        if this.unit == other.unit:
            return this.magnitude == other.magnitude

        try:
            return this.in_unit(other.unit) == other
        except conversions.ConversionNotFound:
            return NotImplemented

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Level):
            other = other.quantify()

        if not isinstance(other, Quantity):
            return NotImplemented

        if self.unit.dimension != other.unit.dimension:
            return NotImplemented

        this = self.unprefixed()
        other = other.unprefixed()

        if this.unit == other.unit:
            return this.magnitude < other.magnitude

        try:
            return this.in_unit(other.unit) < other
        except conversions.ConversionNotFound:
            return NotImplemented


class Logarithm:
    """A `Logarithm` forms a family of [`LogarithmicUnits`][measured.LogarithmicUnit],
    which measures the _ratio_ of a measured [`Quantity`][measured.Quantity] to a
    reference [`Quantity`][measured.Quantity] on a logarithmic scale.  Commonly used
    logarithms include the `Decibel` (base 10) and the `Neper` (base _e_)

    The logarithm is not a unit itself, but rather a family of units, each with a
    specific reference [`Quantity`][measured.Quantity].  For example, the unit `dBW`,
    commonly used in electrical and communications applications, measures the ratio of a
    `Power` quantity against the reference value 1 Watt, in increments of 10 (the base)
    to the 1/10th power (the deci- prefix).

    Examples:

        Use a `Logarithm`, like `Decibel`, to _create_ a new
        [`LogarithmicUnit`][measured.LogarithmicUnit] based on a reference value.  In
        the example below, the reference value is 1 Watt:

        >>> from measured.iec import Decibel
        >>> from measured.si import Watt
        >>> dBW = Decibel[1 * Watt]

        The `dBW` unit may now be used to produces [`Levels`][measured.Level] that may
        be used in operations with Quantities of the same dimension (`Power`, in this
        case):

        >>> assert 100 * Watt == 20 * dBW
    """

    _known: ClassVar[Dict[Tuple[float, int, Prefix], "Logarithm"]] = {}
    _initialized: bool

    base: float
    power_ratio: int
    prefix: Prefix
    name: Optional[str]
    symbol: Optional[str]

    def __new__(
        cls,
        base: float,
        power_ratio: int = 1,
        prefix: Prefix = Prefix(0, 0),
        name: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> "Logarithm":
        if (base, power_ratio, prefix) in cls._known:
            return cls._known[(base, power_ratio, prefix)]

        self = super().__new__(cls)
        self._initialized = False
        cls._known[(base, power_ratio, prefix)] = self
        return self

    def __init__(
        self,
        base: float,
        power_ratio: int = 1,
        prefix: Prefix = Prefix(0, 0),
        name: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> None:
        if self._initialized:
            return

        self.base = base
        self.power_ratio = power_ratio
        self.prefix = prefix
        self.name = name
        self.symbol = symbol
        self._initialized = True

    def alias(self, name: str, symbol: str) -> "Logarithm":
        """Gives a name and symbol to this Logarithm"""
        self.name = name
        self.symbol = symbol
        return self

    __repr__ = formatting.logarithm_repr
    __str__ = formatting.logarithm_str
    _repr_pretty_ = formatting.logarithm_pretty
    _repr_html_ = formatting.mathml(formatting.logarithm_mathml)

    def __mul__(self, other: Prefix) -> "Logarithm":
        if isinstance(other, Prefix):
            return Logarithm(self.base, prefix=self.prefix * other)

        return NotImplemented

    __rmul__ = __mul__

    def __getitem__(self, reference: Quantity) -> "LogarithmicUnit":
        return LogarithmicUnit(self, reference)


class LogarithmicUnit:
    """A `LogarithmicUnit` represents a _ratio_ of a measured
    [`Quantity`][measured.Quantity] to a reference [`Quantity`][measured.Quantity] on a
    logarithmic scale.

    Examples:

        You may construct a `LogarithmicUnit` by applying the reference quantity as a
        "suffix" (using Python's indexing operator `[]`) to the
        [`Logarithm`][measured.Logarithm] in question:

        >>> from measured.iec import Decibel
        >>> from measured.si import Watt, Milli
        >>> dBW = Decibel[1 * Watt]
        >>> dBm = Decibel[1 * Milli * Watt]
        >>> assert dBm is not dBW

        `LogarithmicUnits` create [`Levels`][measured.Level] through multiplication:

        >>> level = 20 * dBW

        A [`Level`][measured.Level] is analogous to a [`Quantity`][measured.Quantity]:

        >>> level.magnitude
        20
        >>> level.unit is dBW
        True
        >>> 100 * Watt == level
        True
    """

    _known: ClassVar[Dict[Tuple[Logarithm, Quantity], "LogarithmicUnit"]] = {}
    _initialized: bool

    logarithm: Logarithm
    reference: Quantity
    name: Optional[str]
    symbol: Optional[str]

    def __new__(
        cls,
        logarithm: Logarithm,
        reference: Quantity,
        name: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> "LogarithmicUnit":
        if (logarithm, reference) in cls._known:
            return cls._known[(logarithm, reference)]

        self = super().__new__(cls)
        self._initialized = False
        cls._known[(logarithm, reference)] = self
        return self

    def __init__(
        self,
        logarithm: Logarithm,
        reference: Quantity,
        name: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> None:
        if self._initialized:
            return

        self.logarithm = logarithm
        self.reference = reference.unprefixed()
        self.name = name
        self.symbol = symbol
        self._initialized = True

    def alias(self, name: str, symbol: str) -> "LogarithmicUnit":
        """Gives a name and symbol to this LogarithmicUnit"""
        assert not self.name and not self.symbol
        self.name = name
        self.symbol = symbol
        return self

    __repr__ = formatting.logarithmic_unit_repr
    __str__ = formatting.logarithmic_unit_str
    _repr_pretty_ = formatting.logarithmic_unit_pretty
    _repr_html_ = formatting.mathml(formatting.logarithmic_unit_mathml)

    def __mul__(self, magnitude: Numeric) -> "Level":
        return Level(magnitude, self)

    __rmul__ = __mul__


class Level:
    """A `Level` is analogous to a [`Quantity`][measured.Quantity], but represents a
    ratio of a quantity to a reference quantity.  The reference quantity is captured by
    the [`LogarithmicUnit`][measured.LogarithmicUnit].

    Attributes:

        magnitude (int | float): the quantity

        unit (LogarithmicUnit): the [`LogarithmicUnit`][measured.LogarithmicUnit]
    """

    magnitude: Numeric
    unit: LogarithmicUnit

    def __init__(self, magnitude: Numeric, unit: LogarithmicUnit) -> None:
        self.magnitude = magnitude
        self.unit = unit

    __repr__ = formatting.level_repr
    __str__ = formatting.level_str
    _repr_pretty_ = formatting.level_pretty
    _repr_html_ = formatting.mathml(formatting.level_mathml)

    def quantify(self) -> Quantity:
        """Converts this Level into a Quantity of the reference unit"""
        base = self.unit.logarithm.base
        prefix = self.unit.logarithm.prefix
        power_ratio = self.unit.logarithm.power_ratio
        reference = self.unit.reference
        exponent = self.magnitude * prefix.quantify()
        magnitude: float = base ** (exponent * power_ratio)
        return magnitude * reference

    def __add__(self, other: "Level") -> "Level":
        if isinstance(other, Level):
            if other.unit != self.unit:
                return NotImplemented

            base = self.unit.logarithm.base
            prefix = self.unit.logarithm.prefix
            power_ratio = self.unit.logarithm.power_ratio

            left_exponent = self.magnitude * prefix.quantify()
            right_exponent = other.magnitude * prefix.quantify()

            left_magnitude: float = base ** (left_exponent * power_ratio)
            right_magnitude: float = base ** (right_exponent * power_ratio)

            magnitude = base * log(left_magnitude + right_magnitude, base)

            return Level(magnitude, self.unit)

        return NotImplemented

    def __sub__(self, other: "Level") -> "Level":
        if isinstance(other, Level):
            if other.unit != self.unit:
                return NotImplemented

            base = self.unit.logarithm.base
            prefix = self.unit.logarithm.prefix
            power_ratio = self.unit.logarithm.power_ratio

            left_exponent = self.magnitude * prefix.quantify()
            right_exponent = other.magnitude * prefix.quantify()

            left_magnitude: float = base ** (left_exponent * power_ratio)
            right_magnitude: float = base ** (right_exponent * power_ratio)

            magnitude = base * log(left_magnitude - right_magnitude, base)

            return Level(magnitude, self.unit)

        return NotImplemented

    def __mul__(self, other: Numeric) -> "Level":
        if isinstance(other, NUMERIC_CLASSES):
            return Level(self.magnitude + other, self.unit)

        return NotImplemented

    def __truediv__(self, other: Numeric) -> "Level":
        if isinstance(other, NUMERIC_CLASSES):
            return Level(self.magnitude - other, self.unit)

        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Level):
            return self.quantify() == other.quantify()

        if isinstance(other, Quantity):
            return self.quantify() == other

        return NotImplemented


class Measurement:
    """Measurement represents an uncertain measurement of some Quantity, and will
    propagate that uncertainty through arithmetic operations with Quantities and other
    Measurements.

    Attributes:

        measurand (Quantity): the measured value

        uncertainty (Quantity | Numeric): the uncertainty of the measurement

    Examples:

        All of the arithmetic operations are supported with Quantities and Measurements:

        >>> from measured import Measurement
        >>> from measured.si import Meter, Second
        >>> length = Measurement(2 * Meter, uncertainty=0.1)
        >>> width = Measurement(3 * Meter, uncertainty=0.2)
        >>> depth = 4 * Meter

        The uncertainty of the measurements propagate through arithmetic operations
        assuming that they are Gaussian, normally-distributed errors.

        >>> area = length * width
        >>> assert isinstance(area, Measurement)
        >>> assert area.measurand == 6 * Meter**2
        >>> assert area.uncertainty == 0.5 * Meter**2

        Quantities are treated as if they have an uncertainty of 0:

        >>> volume = area * depth
        >>> assert isinstance(volume, Measurement)
        >>> assert volume.measurand == 24 * Meter**3
        >>> assert volume.uncertainty == 2.0 * Meter**3

        When formatting a [`Measurement`][measured.Measurement], you can specify up to
        three separate format specifiers, separated by a `:`.  The first specifier
        controls how the uncertainty will be formatted.

        >>> speed = Measurement(10.0 * Meter / Second, 0.1)

        Uncertainties can be formatted as a ± interval using either the "±" or "+"
        specifier (the default)

        >>> f"{speed}"
        '10.0±0.1 m⋅s⁻¹'

        They can also be formatted as percentages using the "%" specifier:

        >>> f"{speed:%}"
        '10.0±1.00% m⋅s⁻¹'

        In any of those cases, the significant digits of the uncertainty can also be
        specified:

        >>> f"{speed:%.4f}"
        '10.0±1.0000% m⋅s⁻¹'
        >>> f"{speed:±.4f}"
        '10.0±0.1000 m⋅s⁻¹'
        >>> f"{speed:+.4f}"
        '10.0±0.1000 m⋅s⁻¹'

        The second and third specifiers are used to format the measurand and follow the
        same conventions as with [`Quantity`][measured.Quantity].

        >>> f"{speed:%.4f:.3f:/}"
        '10.000±1.0000% m/s'
    """

    measurand: Quantity
    uncertainty: Quantity

    def __init__(
        self, measurand: Quantity, uncertainty: Union[Numeric, Quantity]
    ) -> None:
        self.measurand = measurand
        if not isinstance(uncertainty, Quantity):
            uncertainty = Quantity(uncertainty, measurand.unit)
        assert uncertainty.unit is measurand.unit
        self.uncertainty = abs(uncertainty)

    @property
    def uncertainty_ratio(self) -> float:
        """The uncertainty, expressed as a fraction of the magnitude of the measurand"""
        return self.uncertainty.magnitude / self.measurand.magnitude

    @property
    def uncertainty_percent(self) -> float:
        """The uncertainty, expressed as a percent of the magnitude of the measurand"""
        return self.uncertainty_ratio * 100

    __repr__ = formatting.measurement_repr
    __str__ = formatting.measurement_str
    __format__ = formatting.measurement_format
    _repr_pretty_ = formatting.measurement_pretty
    _repr_html_ = formatting.mathml(formatting.measurement_mathml)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Quantity):
            other = Measurement(other, 0)
        if isinstance(other, Level):
            other = Measurement(other.quantify(), 0)

        if not isinstance(other, Measurement):
            return False

        if self.measurand.unit.dimension is not other.measurand.unit.dimension:
            return False

        self_lower = self.measurand - self.uncertainty
        other_lower = other.measurand - other.uncertainty
        self_upper = self.measurand + self.uncertainty
        other_upper = other.measurand + other.uncertainty

        try:
            overlaps_lower = self_lower <= other_lower <= self_upper
            overlaps_upper = self_lower <= other_upper <= self_upper
        except TypeError:
            return False

        return overlaps_lower or overlaps_upper

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Quantity):
            other = Measurement(other, 0)
        if isinstance(other, Level):
            other = Measurement(other.quantify(), 0)

        if not isinstance(other, Measurement):
            return NotImplemented

        self_lower = self.measurand - self.uncertainty
        other_lower = other.measurand - other.uncertainty
        return self_lower < other_lower

    def __le__(self, other: object) -> bool:
        if isinstance(other, Quantity):
            other = Measurement(other, 0)
        if isinstance(other, Level):
            other = Measurement(other.quantify(), 0)

        if not isinstance(other, Measurement):
            return NotImplemented

        self_lower = self.measurand - self.uncertainty
        other_lower = other.measurand - other.uncertainty
        return self_lower <= other_lower

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Quantity):
            other = Measurement(other, 0)
        if isinstance(other, Level):
            other = Measurement(other.quantify(), 0)

        if not isinstance(other, Measurement):
            return NotImplemented

        self_upper = self.measurand + self.uncertainty
        other_upper = other.measurand + other.uncertainty
        return self_upper > other_upper

    def __ge__(self, other: object) -> bool:
        if isinstance(other, Quantity):
            other = Measurement(other, 0)
        if isinstance(other, Level):
            other = Measurement(other.quantify(), 0)

        if not isinstance(other, Measurement):
            return NotImplemented

        self_upper = self.measurand + self.uncertainty
        other_upper = other.measurand + other.uncertainty
        return self_upper >= other_upper

    def __add__(self, other: Union["Measurement", Quantity]) -> "Measurement":
        if isinstance(other, Quantity):
            other = Measurement(other, 0)

        if not isinstance(other, Measurement):
            return NotImplemented

        measurand = self.measurand + other.measurand
        uncertainty = (self.uncertainty**2 + other.uncertainty**2).root(2)
        return Measurement(measurand, uncertainty)

    __radd__ = __add__

    def __sub__(self, other: Union["Measurement", Quantity]) -> "Measurement":
        if isinstance(other, Quantity):
            other = Measurement(other, 0)

        if not isinstance(other, Measurement):
            return NotImplemented

        measurand = self.measurand - other.measurand
        uncertainty = (self.uncertainty**2 + other.uncertainty**2).root(2)
        return Measurement(measurand, uncertainty)

    def __rsub__(self, other: Union["Measurement", Quantity]) -> "Measurement":
        if isinstance(other, Quantity):
            other = Measurement(other, 0)

        if not isinstance(other, Measurement):
            return NotImplemented

        return other - self

    def __mul__(self, other: Union["Measurement", Quantity]) -> "Measurement":
        if isinstance(other, Quantity):
            other = Measurement(other, 0)

        if not isinstance(other, Measurement):
            return NotImplemented

        measurand = self.measurand * other.measurand
        uncertainty = sqrt(
            measurand.magnitude**2
            * (
                (self.uncertainty.magnitude**2 / self.measurand.magnitude**2)
                + (other.uncertainty.magnitude**2 / other.measurand.magnitude**2)
            )
        )
        return Measurement(measurand, uncertainty)

    __rmul__ = __mul__

    def __truediv__(self, other: Union["Measurement", Quantity]) -> "Measurement":
        if isinstance(other, Quantity):
            other = Measurement(other, 0)

        if not isinstance(other, Measurement):
            return NotImplemented

        measurand = self.measurand / other.measurand
        uncertainty = sqrt(
            measurand.magnitude**2
            * (
                (self.uncertainty.magnitude**2 / self.measurand.magnitude**2)
                + (other.uncertainty.magnitude**2 / other.measurand.magnitude**2)
            )
        )
        return Measurement(measurand, uncertainty)

    def __rtruediv__(self, other: Union["Measurement", Quantity]) -> "Measurement":
        if isinstance(other, Quantity):
            other = Measurement(other, 0)

        if not isinstance(other, Measurement):
            return NotImplemented

        return other / self

    def __pow__(self, exponent: int) -> "Measurement":
        if not isinstance(exponent, int):
            return NotImplemented

        measurand = self.measurand**exponent
        uncertainty = sqrt(
            (exponent * self.measurand.magnitude**2 * self.uncertainty.magnitude) ** 2
        )
        return Measurement(measurand, uncertainty)


def approximately(
    quantity: Union[Quantity, Level], within: float = 1e-7
) -> Measurement:
    """
    An approximation used mostly for making test assertions.  This special type of
    measurement uses a relative value for uncertainty and overrides its repr to be
    more useful for test assertions.

    Parameters:

        quantity (Quantity): the quantity to approximate

        within (float): An uncertainty of the measurement relative to the quantity

    Examples:

        >>> from measured import approximately
        >>> from measured.si import Meter
        >>> assert 5.2 * Meter == approximately(5 * Meter, 0.3)
        >>> assert 5.2 * Meter < approximately(6 * Meter, 0.5)
    """
    if isinstance(quantity, Level):
        quantity = quantity.quantify()

    return Measurement(quantity, uncertainty=(quantity.magnitude or 1.0) * within)


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
VolumetricFlow = Dimension.derive(Volume / Time, name="flow")

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
Pressure = Dimension.derive(Force / Area, name="pressure")
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


from . import conversions  # noqa: E402
from .parsing import parser  # noqa: E402

One.equals(1 * One)
