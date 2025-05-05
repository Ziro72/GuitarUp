
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Set
from collections import Counter

from Chord import Chord

# ─────────── Справочник kind → суффикс ───────────
KIND_SUFFIX: Dict[str, str] = {
    'major': '', 'minor': 'm',
    'dominant': '7', 'seventh': '7',
    'major-seventh': 'maj7', 'minor-seventh': 'm7',
    'diminished': 'dim', 'augmented': 'aug',
    'suspended-second': 'sus2', 'suspended-fourth': 'sus4',
    'ninth': '9', 'eleventh': '11', 'thirteenth': '13',
}

# ─────────── модели для полной структуры ───────────
@dataclass
class Note:
    string: int
    fret:   int

@dataclass
class Beat:
    number: int
    notes:  List[Note]   = field(default_factory=list)
    chords: List[Chord]  = field(default_factory=list)

@dataclass
class Measure:
    number: int
    beats:  List[Beat]   = field(default_factory=list)

@dataclass
class Track:
    name:     str
    measures: List[Measure] = field(default_factory=list)

@dataclass
class Score:
    title:  str
    tracks: List[Track]    = field(default_factory=list)

# ─────────── util ───────────
def strip_ns(root: ET.Element) -> None:
    for el in root.iter():
        if '}' in el.tag:
            el.tag = el.tag.split('}', 1)[1]

# ─────────── auto-fingering с корректным баррэ ───────────
def auto_fingering(ch: Chord, positions: list[tuple[int, int]]) -> None:
    fretted = [(s, f) for s, f in positions if f > 0]
    if not fretted:
        return

    # ─ поиск баррэ (минимальный лад, ≥2 струн) ────────────────────────
    low_fret = min(f for _, f in fretted)
    strings  = [s for s, f in fretted if f == low_fret]

    barre_applied = False
    if len(strings) >= 2:
        start, end = min(strings), max(strings)
        width = end - start                  # Δ для edit_barre
        ch.finger(0).edit(fret=low_fret, string=start)
        ch.edit_barre(width)
        barre_applied = True

        # удаляем струны, попавшие под баррэ
        fretted = [(s, f) for s, f in fretted
                   if not (f == low_fret and start <= s <= end)]

    # ─ расставляем оставшиеся пальцы ──────────────────────────────────
    idx = 1 if barre_applied else 0          # ← главный фикс
    for s, f in sorted(fretted, key=lambda t: (t[1], -t[0])):
        if idx > 3:                          # максимум до мизинца
            break
        ch.finger(idx).edit(fret=f, string=s)
        idx += 1



# ─────────── кеш-ключ ───────────
def chord_signature(ch: Chord) -> Tuple:
    fingers = tuple((f.string, f.fret) for f in ch.fingers)  # type: ignore
    barre_width = int(getattr(ch, 'barre', 0))               # ширина баррэ
    return (
        ch.name.name,
        getattr(ch, 'start_fret', 0),
        fingers,
        barre_width
    )

# ─────────── основной парсер ───────────
class GPXMLParser:
    def __init__(self, xml_path: str):
        self.xml_path = xml_path
        root = ET.parse(xml_path).getroot()
        strip_ns(root)
        self.title = (root.findtext('work/work-title', '')
                      or root.findtext('movement-title', '')
                      or '')

    # MusicXML <harmony> → Chord
    def _harmony_to_chord(self, h: ET.Element) -> Chord:
        step = h.findtext('root/root-step', '')
        alt  = h.findtext('root/root-alter')
        if alt == '1':  step += '#'
        elif alt == '-1': step += 'b'

        kind = KIND_SUFFIX.get(h.findtext('kind', 'major'),
                               h.findtext('kind', 'major'))
        name = step + kind

        for deg in h.findall('degree'):
            tp = deg.findtext('degree-type', '').lower()
            val = deg.findtext('degree-value', '')
            if tp == 'add':
                name += f'add{val}'
            elif tp in ('major', 'maj'):
                name += f'maj{val}'
            elif tp in ('minor', 'min'):
                name += f'm{val}'

        first = int(h.findtext('frame/first-fret', '0'))
        ch = Chord(name=name, fret=first)

        for i in range(6):
            ch.change_string_state(i)        # mute все

        pos: List[Tuple[int, int]] = []
        for fn in h.findall('frame/frame-note'):
            s = int(fn.findtext('string', '0'))
            f = int(fn.findtext('fret',   '0'))
            pos.append((s, f))
            ch.change_string_state(s - 1)

        auto_fingering(ch, pos)

        # slash-bass
        bass_step = h.findtext('bass/bass-step')
        if bass_step:
            altb = h.findtext('bass/bass-alter')
            bass = bass_step + ('#' if altb == '1' else 'b' if altb == '-1' else '')
            ch.change_name(f"{ch.name.name}/{bass}")

        return ch

    def parse(self):
        rendered: Set[Tuple] = set()
        for _, el in ET.iterparse(self.xml_path, events=('end',)):
            if el.tag != 'harmony':
                continue
            chord = self._harmony_to_chord(el)
            sig = chord_signature(chord)
            if sig in rendered:
                el.clear(); continue
            rendered.add(sig)
            chord.draw_chord();
            chord.save_chord()
            el.clear()

# ─────────── CLI ───────────
def main():
    xml_file = "C:/Users/t480s/Downloads/forbidden_friendship.xml"
    GPXMLParser(xml_file).parse()

if __name__ == "__main__":
    main()
