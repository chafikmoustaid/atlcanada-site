#!/usr/bin/env python3
"""Lien « Honoraires » visible : menu + pieds de page (idempotent)."""
import glob, os, re
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') + '/'
pat = re.compile(r'(<a class="nav-eval" href="([^"]*)">[^<]*</a>)')
FOOT = (
 ('<a href="/deroulement-dossier-immigration/">Déroulement d\'un dossier</a>', ' · <a href="/honoraires/">Honoraires</a> · <a href="/frais-officiels-immigration-canada/">Frais officiels</a>'),
 ('<a href="/ar/case-process/">سير الملف</a>', ' · <a href="/ar/fees/">الأتعاب</a> · <a href="/ar/official-fees/">الرسوم الرسمية</a>'),
 ('<li><a href="/deroulement-dossier-immigration/">Déroulement d\'un dossier</a></li>', '\n          <li><a href="/honoraires/">Honoraires</a></li>\n          <li><a href="/frais-officiels-immigration-canada/">Frais officiels</a></li>'),
)
n = 0
for f in glob.glob(R + '**/*.html', recursive=True):
    t = s = open(f, encoding='utf-8').read()
    if 'class="nav-fees"' not in t:
        def add(mo):
            ar = mo.group(2).startswith('/ar/')
            return mo.group(1) + ('<a class="nav-fees" href="/ar/fees/">الأتعاب</a>' if ar else '<a class="nav-fees" href="/honoraires/">Honoraires</a>')
        t = pat.sub(add, t)
    for a, b in FOOT:
        if a in t and b.strip(' ·\n') not in t and '/honoraires/' not in t.split(a)[1][:200] and '/ar/fees/' not in t.split(a)[1][:200]:
            t = t.replace(a, a + b, 1)
    if t != s:
        open(f, 'w', encoding='utf-8').write(t); n += 1
print('fees_link : modifié', n, 'fichiers')
