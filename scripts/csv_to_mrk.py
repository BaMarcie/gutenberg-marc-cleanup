#!/usr/bin/env python3
"""Convert a Project Gutenberg Dublin Core CSV into MarcEdit's text MARC format (.mrk).

Usage:  python csv_to_mrk.py data/gutenberg-clean-500.csv data/gutenberg_500.mrk

Mapping (simplified, for practice):
  dc.identifier -> 001 and 856 $u      dc.title      -> 245 $a/$b
  dc.creator    -> 100                 dc.contributor-> 700 (with $e relator)
  dc.language   -> 041 and 008         dc.subject    -> 650 (split on '||')
  dcterms.issued-> 500 note (date added to Gutenberg, NOT publication date)
Known simplifications (see docs/findings.md): places are tagged 650 not 651,
subdivisions are guessed ($v for known forms, otherwise $x), names have no $q.
"""
import csv, re, sys

LANG = {'en':'eng','fr':'fre','de':'ger','es':'spa','it':'ita','nl':'dut','fi':'fin',
        'pt':'por','la':'lat','el':'grc','sv':'swe','da':'dan','hu':'hun','tl':'tgl',
        'zh':'chi','eo':'epo','cy':'wel','ca':'cat'}
FORM = {'Fiction','Juvenile fiction','Poetry','Drama','Biography','Humor','Periodicals',
        'Juvenile literature','Correspondence','Diaries','Sources','Early works to 1800',
        'Juvenile poetry','Juvenile drama','Songs and music','Quotations','Dictionaries',
        'History','Anecdotes','Bibliography','Maps','Pictorial works','Satire','Textbooks',
        'Handbooks, manuals, etc.','Personal narratives','Addresses, essays, lectures',
        'Study and teaching','Translations into English'}

def split_name(s):
    """'Meade, L. T., 1854-1914' -> ('Meade, L. T.', '1854-1914')"""
    m = re.match(r'^(.*?),? (\d{4}-?\d{0,4}\??|\d{1,2}th century.*)$', s.strip())
    return (m.group(1).rstrip(','), m.group(2)) if m else (s.strip(), None)

def name_field(tag, s):
    s = s.strip(); relator = None
    m = re.match(r'^(.*?)\s*\[(.*?)\]$', s)          # e.g. "... [Illustrator]"
    if m: s, relator = m.group(1), m.group(2)
    a, d = split_name(s)
    f = f'={tag}  1\\$a{a}'
    if d: f += f',$d{d}'
    elif not a.endswith('.'): f += '.'
    if relator: f += f',$e{relator.lower()}.'
    elif d: f += '.'
    return f

def esc(s):                      # a literal "$" must be written {dollar} in .mrk
    return s.replace('$', '{dollar}')

def record(r):
    lang = LANG.get(r['dc.language'].strip(), 'und')
    f008 = '241120' + 's' + '    ' + '    ' + 'xx ' + '||||' + '|' + 'o' + '||||' + '||||' + ' ' + '||' + lang + ' ' + 'd'
    assert len(f008) == 40
    L = ['=LDR  00000nam  2200000 a 4500', '=001  gutenberg' + r['dc.identifier'],
         '=007  cr||||||||||||', '=008  ' + f008, f'=041  0\\$a{lang}']
    creator = r['dc.creator'].strip()
    has100 = bool(creator) and creator != 'Anonymous'
    if has100: L.append(name_field('100', esc(creator)))
    title = esc(r['dc.title'].strip())
    m = re.match(r'^(The|A|An) ', title)
    nonfiling = len(m.group(1)) + 1 if m else 0
    parts = re.split(r':\s', title, maxsplit=1)
    t245 = f'$a{parts[0]}' + (f' :$b{parts[1]}' if len(parts) > 1 else '')
    if not t245.endswith(('.', '?', '!')): t245 += '.'
    L.append(f"=245  {1 if has100 else 0}{nonfiling}{t245}")
    L += ['=336  \\\\$atext$btxt$2rdacontent', '=337  \\\\$acomputer$bc$2rdamedia',
          '=338  \\\\$aonline resource$bcr$2rdacarrier',
          f"=500  \\\\$aAdded to Project Gutenberg {r['dcterms.issued']}."]
    for subj in r['dc.subject'].split('||'):
        subj = esc(subj.strip())
        if not subj: continue
        bits = subj.split(' -- ')
        f = f'=650  \\0$a{bits[0]}'
        for b in bits[1:]:
            f += ('$v' if b in FORM else '$x') + b
        if not f.endswith(('.', ')', '?')): f += '.'
        L.append(f)
    for c in r['dc.contributor'].split('||'):
        if c.strip(): L.append(name_field('700', esc(c)))
    L.append(f"=856  40$uhttps://www.gutenberg.org/ebooks/{r['dc.identifier']}")
    return '\n'.join(L)

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    rows = list(csv.DictReader(open(src, encoding='utf-8-sig')))
    open(dst, 'w', encoding='utf-8').write('\n\n'.join(record(r) for r in rows) + '\n')
    print(f'Wrote {len(rows)} records to {dst}')
