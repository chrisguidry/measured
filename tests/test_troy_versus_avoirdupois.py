from measured import One, avoirdupois, troy


def test_grain_is_the_same() -> None:
    assert avoirdupois.Grain == troy.Grain


# https://en.wikipedia.org/wiki/Troy_weight#Troy_ounce_(oz_t)


def test_troy_ounce_is_heavier() -> None:
    assert (1 * troy.Ounce) > 1 * avoirdupois.Ounce


def test_troy_ounce_ratio() -> None:
    assert (1 * troy.Ounce) == 480 / 437.5 * avoirdupois.Ounce


def test_troy_ounce_conversion() -> None:
    (1 * troy.Ounce).in_unit(
        avoirdupois.Ounce
    ) == 1.0971428571428572 * avoirdupois.Ounce

    assert (1 * avoirdupois.Ounce).in_unit(
        troy.Ounce
    ) == 0.9114583333333334 * troy.Ounce


def test_troy_ounce_percentage() -> None:
    assert (1 * troy.Ounce) / (1 * avoirdupois.Ounce) == 1.0971428571428572 * One
