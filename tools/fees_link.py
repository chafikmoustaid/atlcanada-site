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

# budget + à propos dans les pieds de page (idempotent)
PAIRS2 = (
 ('<a href="/frais-officiels-immigration-canada/">Frais officiels</a></li>', '\n          <li><a href="/budget-immigration-canada/">Calculateur de budget</a></li>\n          <li><a href="/a-propos/">À propos</a></li>'),
 ('<a href="/frais-officiels-immigration-canada/">Frais officiels</a>', ' · <a href="/budget-immigration-canada/">Calculateur de budget</a> · <a href="/a-propos/">À propos</a>'),
 ('<a href="/ar/official-fees/">الرسوم الرسمية</a>', ' · <a href="/ar/budget-calculator/">حاسبة الميزانية</a> · <a href="/ar/about/">من نحن</a>'),
)
k = 0
for f in glob.glob(R + '**/*.html', recursive=True):
    t = s0 = open(f, encoding='utf-8').read()
    if '/budget-immigration-canada/' in t.split('Frais officiels</a>')[-1][:300] or '/ar/budget-calculator/' in t.split('الرسوم الرسمية</a>')[-1][:300]:
        continue
    for a, b in PAIRS2:
        if a in t and 'class="fee-box"' not in a:
            idx = t.find(a)
            # ne pas toucher au texte des encadrés / pages de frais : seulement le pied de page
            if t.rfind('<footer', 0, idx) == -1: continue
            t = t[:idx + len(a)] + b + t[idx + len(a):]
            break
    if t != s0:
        open(f, 'w', encoding='utf-8').write(t); k += 1
print('budget_about_link : modifié', k, 'fichiers')

# pages à menu minimal (actualités, confidentialité) : lien Honoraires après « Accueil »
m = 0
for f in glob.glob(R + '**/*.html', recursive=True):
    t = s0 = open(f, encoding='utf-8').read()
    if 'class="nav-fees"' in t: continue
    for a, b in (('<nav class="primary" aria-label="Navigation"><a href="/">Accueil</a>', '<a class="nav-fees" href="/honoraires/">Honoraires</a>'),
                 ('<nav class="primary" aria-label="Navigation"><a href="/ar/">الرئيسية</a>', '<a class="nav-fees" href="/ar/fees/">الأتعاب</a>')):
        if a in t:
            t = t.replace(a, a + b, 1); break
    if t != s0:
        open(f, 'w', encoding='utf-8').write(t); m += 1
print('nav minimal : modifié', m, 'fichiers')
