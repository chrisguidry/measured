def test_us_masses_are_based_on_the_avoirdupois_system() -> None:
    from measured import avoirdupois, us

    assert us.Dram is avoirdupois.Dram
    assert us.Grain is avoirdupois.Grain
    assert us.Ounce is avoirdupois.Ounce
    assert us.Pound is avoirdupois.Pound

    assert us.Hundredweight is not avoirdupois.LongHundredweight
    assert (1 * us.Hundredweight) < (1 * avoirdupois.LongHundredweight)

    assert us.Ton is not avoirdupois.LongTon
    assert (1 * us.Ton) < (1 * avoirdupois.LongTon)
