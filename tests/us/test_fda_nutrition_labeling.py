# https://web.archive.org/web/20120204081321/http://edocket.access.gpo.gov/cfr_2004/aprqtr/21cfr101.9.htm
#
# (viii) For nutrition labeling purposes, a teaspoon means 5
# milliliters (mL), a tablespoon means 15 mL, a cup means 240 mL, 1 fl oz
# means 30 mL, and 1 oz in weight means 28 g.
# [pp 23]

from measured import approximately
from measured.si import Gram, Liter, Milli
from measured.us import Cup, FluidOunce, Ounce, Tablespoon, Teaspoon


def test_teaspoon_is_about_5mL() -> None:
    assert 1 * Teaspoon == approximately(5 * Milli * Liter, within=0.015)


def test_tablespoon_is_about_15mL() -> None:
    assert 1 * Tablespoon == approximately(15 * Milli * Liter, within=0.015)


def test_cup_is_about_240mL() -> None:
    assert 1 * Cup == approximately(240 * Milli * Liter, within=0.015)


def test_fluid_ounce_is_about_30mL() -> None:
    assert 1 * FluidOunce == approximately(30 * Milli * Liter, within=0.015)


def test_dry_ounce_is_about_28g() -> None:
    assert 1 * Ounce == approximately(28 * Gram, within=0.013)
