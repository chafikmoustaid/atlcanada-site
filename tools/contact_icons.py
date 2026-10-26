#!/usr/bin/env python3
"""Ajoute icônes téléphone / WhatsApp et liens cliquables partout (idempotent).
Usage : python3 tools/contact_icons.py   (depuis la racine du dépôt ; à relancer après build_pages*.py)"""
import re, glob, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
TEL, WA = '+15142956635', 'https://wa.me/15142956635'
NUM = '+1 514 295 6635'
src = open(R + 'index.html', encoding='utf-8').read()
tb = re.search(r'<span class="tb-phone"><a href="tel:[^"]*" aria-label="[^"]*">(<svg.*?</svg>).*?<a class="tb-wa"[^>]*>(<svg.*?</svg>)</a>', src, re.S)
PH = tb.group(1).replace('<svg ', '<svg class="tel-ico" ', 1)
WAI = tb.group(2).replace('<svg ', '<svg class="wa-ico" ', 1)

def line(text=NUM, lang='fr'):
    lab = 'واتساب' if lang == 'ar' else 'WhatsApp'
    return (f'<span class="tel-line"><a class="tel" href="tel:{TEL}">{PH}<bdi dir="ltr">{text}</bdi></a>'
            f'<a class="wa" href="{WA}" target="_blank" rel="noopener" aria-label="{lab}" title="{lab}">{WAI}</a></span>')

def fix(t):
    # P1 : boutons « Appeler »
    # P1 : boutons « Appeler »
    t = re.sub(r'<a class="(btn [^"]*)" href="tel:\+15142956635">(?!<svg)(.*?)</a>(?!<a class="btn btn-wa")',
               lambda m: (lambda ar: f'<a class="{m.group(1)}" href="tel:{TEL}">{PH}{m.group(2)}</a>'
                          f'<a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener">{WAI}{"واتساب" if ar else "WhatsApp"}</a>')(bool(re.search(r"[؀-ۿ]", m.group(2)))), t)
    # P3 : lien téléphone simple
    t = re.sub(r'<a href="tel:\+15142956635">\+1 514 295 6635</a>', lambda m: line(), t)
    # P4 : numéro dans une phrase
    parts = []
    for ln in t.split('\n'):
        if 'say(' not in ln and 'application/ld+json' not in ln:
            ln = re.sub(r'(?<=Appelez le )\+1 514 295 6635', lambda m: line(), ln)
            ln = re.sub(r'(?<=appelez-nous au )\+1 514 295 6635', lambda m: line(), ln)
            ln = re.sub(r"<bdi dir='ltr'>\+1 514 295 6635</bdi>", lambda m: line(lang='ar'), ln)
        parts.append(ln)
    return '\n'.join(parts)

files = [f for f in glob.glob(R + '**/*.html', recursive=True) if '/.git/' not in f]
n = 0
for f in files:
    t = open(f, encoding='utf-8').read()
    u = fix(t)
    if u != t:
        open(f, 'w', encoding='utf-8').write(u); n += 1
print('modifié :', n, 'fichiers')
