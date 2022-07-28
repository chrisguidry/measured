from typing import Dict

from measured import Level, Octave, Prefix
from measured.iso import A440

Semitone = (Prefix(12, -1) * Octave).alias(name="semitone", symbol="semitone")

ConcertPitch = Semitone[A440]

# https://en.wikipedia.org/wiki/Scientific_pitch_notation

SPN_OCTAVES = range(-1, 11)
MIDDLE_A_OCTAVE = 4


def _octaves(note_offset: int) -> Dict[int, Level]:
    return {
        o: (((-MIDDLE_A_OCTAVE + o) * 12) + note_offset) * ConcertPitch
        for o in SPN_OCTAVES
    }


A_flat = _octaves(-1)
A = _octaves(0)
A_sharp = _octaves(+1)
B_flat = A_sharp
B = _octaves(+2)
C = _octaves(-9)
C_sharp = _octaves(-8)
D_flat = C_sharp
D = _octaves(-7)
D_sharp = _octaves(-6)
E_flat = D_sharp
E = _octaves(-5)
F = _octaves(-4)
F_sharp = _octaves(-3)
G_flat = F_sharp
G = _octaves(-2)
G_sharp = A_flat

MIDI = [(C[-1].magnitude + i) * ConcertPitch for i in range(128)]
