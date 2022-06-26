import cProfile
import functools
import os
from pathlib import Path
from typing import Callable

import typer

from measured import One, Quantity
from measured.astronomical import JulianYear
from measured.si import Ampere, Meter, Ohm, Second, Volt
from measured.us import Ounce, Ton

app = typer.Typer()
options = {"baseline": False}

profiles = Path(".profiles")


@app.callback()
def main(baseline: bool = False) -> None:
    options["baseline"] = baseline


def profiled(func: Callable[[], None]) -> Callable[[], None]:
    @functools.wraps(func)
    def inner() -> None:
        os.makedirs(profiles, exist_ok=True)
        filename = f"{'baseline-' if options['baseline'] else ''}{func.__name__}.prof"
        cProfile.runctx("func()", {"func": func}, {}, str(profiles / filename))

    return inner


@app.command()
@profiled
def quantity_construction() -> None:
    """Tests for constructing Quantities"""
    for a in range(1, 1000001):
        Quantity(a, Meter)


@app.command()
@profiled
def low_equality() -> None:
    """Tests for equality for low-dimensional quantities"""
    for a in (Quantity(a, Meter) for a in range(1, 1001)):
        for b in (Quantity(b, Meter) for b in range(1, 1001)):
            bool(a == b)


@app.command()
@profiled
def high_equality() -> None:
    """Tests for equality for high-dimensional quantities"""
    for a in (Quantity(a, Ohm) for a in range(1, 1001)):
        for b in (Quantity(b, Ohm) for b in range(1, 1001)):
            bool(a == b)


@app.command()
@profiled
def resistances() -> None:
    """Computes a whole lot of Ohms"""
    for a in (Quantity(a, Ampere) for a in range(1, 1001)):
        for v in (Quantity(v, Volt) for v in range(1, 1001)):
            assert v / a == (v.magnitude / a.magnitude) * Ohm


@app.command()
@profiled
def conversions() -> None:
    for o in (Quantity(o, Ounce) for o in range(1, 1001)):
        for t in (Quantity(t, Ton) for t in range(1, 1001)):
            divided = (t / o).in_unit(One)
            assert divided.unit == One
            assert round(divided.magnitude) == round(
                t.magnitude / o.magnitude * 20 * 100 * 16
            )


@app.command()
@profiled
def complex_conversions() -> None:
    for o in (Quantity(o, Ounce / (JulianYear * Ampere)) for o in range(1, 1001)):
        for t in (Quantity(t, Ton / (Second * Ampere)) for t in range(1, 1001)):
            divided = (t / o).in_unit(One)
            assert divided.unit == One


if __name__ == "__main__":
    app()
