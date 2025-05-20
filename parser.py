import xml.etree.ElementTree as ET
from typing import List, Tuple, Set
from ChordPaint import ChordPaint

KIND_SUFFIX = {
    'major':'', 'minor':'m', 'dominant':'7', 'seventh':'7',
    'major-seventh':'maj7', 'minor-seventh':'m7',
    'diminished':'dim', 'augmented':'aug',
}

def strip_ns(r: ET.Element):
    for el in r.iter():
        if '}' in el.tag:
            el.tag = el.tag.split('}',1)[1]

def auto_fingering(ch:ChordPaint, pos:List[Tuple[int,int]]):
    fretted=[(s,f) for s,f in pos if f>0]
    if not fretted: return
    low=min(f for _,f in fretted)
    strings=[s for s,f in fretted if f==low]
    if len(strings)>=3:
        start,end=min(strings),max(strings)
        ch.finger(0).edit(fret=low,string=start)
        ch.edit_barre(end-start)
        fretted=[(s,f) for s,f in fretted if not (f==low and start<=s<=end)]
    idx=1 if len(strings)>=3 else 0
    for s,f in sorted(fretted,key=lambda t:(t[1],-t[0])):
        if idx>3: break
        ch.finger(idx).edit(fret=f,string=s); idx+=1

def _harmony_to_chord(h:ET.Element)->ChordPaint:
    step=h.findtext('root/root-step','')
    alt =h.findtext('root/root-alter')
    if alt=='1': step+='#'
    elif alt=='-1': step+='b'
    kind=KIND_SUFFIX.get(h.findtext('kind','major'),'')
    name=step+kind
    first=int(h.findtext('frame/first-fret','0'))
    ch=ChordPaint(name=name,fret=first)
    for i in range(6): ch.change_string_state(i)
    pos=[]
    for fn in h.findall('frame/frame-note'):
        s=int(fn.findtext('string','0')); f=int(fn.findtext('fret','0'))
        if f==0:
            ch.change_string_state(s-1)
        else:
            pos.append((s,f))
            ch.change_string_state(s-1)
    auto_fingering(ch,pos)
    bass=h.findtext('bass/bass-step')
    if bass:
        altb=h.findtext('bass/bass-alter')
        bass += '#' if altb=='1' else 'b' if altb=='-1' else ''
        ch.change_name(f"{ch.name.name}/{bass}")
    return ch

class GPXMLParser:
    def __init__(self, path:str):
        self.xml_path = path
        root = ET.parse(path).getroot()
        strip_ns(root)
        # сколько harmony всего
        self.total_harmony = sum(1 for _ in root.iterfind('.//harmony'))

    def iter_chord_names(self):
        """Фоновый проход — только собираем имена, без draw_chord()."""
        seen: Set[str] = set()
        for _, el in ET.iterparse(self.xml_path, events=('end',)):
            if el.tag!='harmony':
                continue
            ch = _harmony_to_chord(el)
            nm = ch.name.name
            if nm not in seen:
                seen.add(nm)
                yield nm
            el.clear()

    def parse(self):
        """Полный разбор с draw_chord() — только в основном потоке!"""
        rendered: Set[str] = set()
        for _, el in ET.iterparse(self.xml_path, events=('end',)):
            if el.tag!='harmony': continue
            ch = _harmony_to_chord(el)
            nm = ch.name.name
            if nm not in rendered:
                ch.draw_chord()
                ch.save_chord()
                rendered.add(nm)
            el.clear()
