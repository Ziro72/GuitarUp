import xml.etree.ElementTree as ET
from typing import List, Tuple, Set
from ChordPaint import ChordPaint  # нужен только для parse(), не в итераторе

KIND_SUFFIX = {
    'major':'', 'minor':'m', 'dominant':'7', 'seventh':'7',
    'major-seventh':'maj7','minor-seventh':'m7',
    'diminished':'dim','augmented':'aug',
    'suspended-second':'sus2','suspended-fourth':'sus4',
    'ninth':'9','eleventh':'11','thirteenth':'13',
}

def strip_ns(root: ET.Element):
    for el in root.iter():
        if '}' in el.tag:
            el.tag = el.tag.split('}',1)[1]

def _extract_name(h: ET.Element) -> str:
    # 1) root-step/alter
    step = h.findtext('root/root-step','')
    alt  = h.findtext('root/root-alter')
    if alt == '1':   step += '#'
    elif alt == '-1': step += 'b'
    # 2) kind → суффикс
    kind_tag = h.findtext('kind','major')
    kind     = KIND_SUFFIX.get(kind_tag, kind_tag if kind_tag not in KIND_SUFFIX else '')
    name = step + kind
    # 3) degree (add, maj, min)
    for deg in h.findall('degree'):
        t = deg.findtext('degree-type','').lower()
        v = deg.findtext('degree-value','')
        if t == 'add':
            name += f'add{v}'
        elif t in ('major','maj'):
            name += f'maj{v}'
        elif t in ('minor','min'):
            name += f'm{v}'
    # 4) slash-бас
    bass = h.findtext('bass/bass-step')
    if bass:
        altb = h.findtext('bass/bass-alter')
        bass += '#' if altb=='1' else 'b' if altb=='-1' else ''
        name += f"/{bass}"
    return name

class GPXMLParser:
    def __init__(self, path: str):
        self.xml_path = path
        root = ET.parse(path).getroot()
        strip_ns(root)
        # считаем сколько будет итераций
        self.total_harmony = sum(1 for _ in root.iterfind('.//harmony'))

    def iter_chord_names(self):
        """Генератор для фонового потока: отдаёт только уникальные строки-имена."""
        seen: Set[str] = set()
        for _, el in ET.iterparse(self.xml_path, events=('end',)):
            if el.tag != 'harmony':
                continue
            name = _extract_name(el)
            if name not in seen:
                seen.add(name)
                yield name
            el.clear()

    # оставляем parse() без изменений — он вызывается в GUI-потоке
    def parse(self):
        rendered: Set[Tuple] = set()
        for _, el in ET.iterparse(self.xml_path, events=('end',)):
            if el.tag != 'harmony':
                continue
            # здесь можно вызывать полный _harmony_to_chord + draw/save
            ch = ChordPaint(name=_extract_name(el), fret=int(el.findtext('frame/first-fret','0')))
            # … и дальше ваша старая логика рукопашного рендера …
            # ch.draw_chord(); ch.save_chord()
            el.clear()
