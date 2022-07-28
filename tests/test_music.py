from measured import approximately, music
from measured.si import Hertz


def test_middle_A() -> None:
    assert music.A[4] == 440 * Hertz


def test_middle_C() -> None:
    assert music.C[4] == approximately(261.625565 * Hertz)


def test_lowest_c() -> None:
    assert music.C[-1] == approximately(8.175799 * Hertz)


def test_highest_b() -> None:
    assert music.B[10] == approximately(31608.53 * Hertz)


def test_synonyms() -> None:
    assert music.A_sharp == music.B_flat
    assert music.C_sharp == music.D_flat
    assert music.D_sharp == music.E_flat
    assert music.F_sharp == music.G_flat
    assert music.G_sharp == music.A_flat


def test_midi_notes() -> None:
    assert music.MIDI[0] == music.C[-1]
    assert music.MIDI[69] == music.A[4]
    assert music.MIDI[127] == music.G[9]
