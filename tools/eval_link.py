#!/usr/bin/env python3
"""Ajoute le lien « Évaluer mon dossier » dans les pieds de page (idempotent)."""
import glob, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') + '/'
FR = ('<a href="/calculateur-entree-express/">Calculateur Entrée express</a>', ' · <a href="/evaluer-mon-dossier/">Évaluer mon dossier</a> · <a href="/rendez-vous/">Prendre rendez-vous</a> · <a href="/deroulement-dossier-immigration/">Déroulement d\'un dossier</a>', '/rendez-vous/')
AR = ('<a href="/ar/express-entry-calculator/">حاسبة الدخول السريع</a>', ' · <a href="/ar/evaluate-my-case/">قيّم ملفك</a> · <a href="/ar/book-consultation/">احجز موعدًا</a>', '/ar/book-consultation/')
LI = ('<li><a href="/calculateur-entree-express/">Calculateur de points Entrée express</a></li>', '\n          <li><a href="/evaluer-mon-dossier/">Évaluer mon dossier</a></li>\n          <li><a href="/rendez-vous/">Prendre rendez-vous</a></li>', '/rendez-vous/')
n = 0
for f in glob.glob(R + '**/*.html', recursive=True):
    t = s = open(f, encoding='utf-8').read()
    for anchor, add, mark in (FR, AR, LI):
        if anchor in t and mark not in t:
            t = t.replace(anchor, anchor + add, 1)
    if t != s:
        open(f, 'w', encoding='utf-8').write(t); n += 1
print('eval_link : modifié', n, 'fichiers')

# lien « Évaluer » dans le menu (à côté du calculateur)
import re
pat = re.compile(r'(<a class="nav-calc" href="([^"]*)">[^<]*</a>)')
m = 0
for f in glob.glob(R + '**/*.html', recursive=True):
    t = s = open(f, encoding='utf-8').read()
    if 'class="nav-eval"' in t:
        continue
    def add(mo):
        ar = mo.group(2).startswith('/ar/')
        return mo.group(1) + ('<a class="nav-eval" href="/ar/evaluate-my-case/">قيّم ملفك</a>' if ar else '<a class="nav-eval" href="/evaluer-mon-dossier/">Évaluer</a>')
    t = pat.sub(add, t)
    if t != s:
        open(f, 'w', encoding='utf-8').write(t); m += 1
print('nav-eval : modifié', m, 'fichiers')

# lien « Déroulement d'un dossier » dans les pieds de page (idempotent)
k = 0
PAIRS = (
    ('<a href="/rendez-vous/">Prendre rendez-vous</a></li>', '<a href="/rendez-vous/">Prendre rendez-vous</a></li>\n          <li><a href="/deroulement-dossier-immigration/">Déroulement d\'un dossier</a></li>'),
    ('<a href="/rendez-vous/">Prendre rendez-vous</a>', '<a href="/rendez-vous/">Prendre rendez-vous</a> · <a href="/deroulement-dossier-immigration/">Déroulement d\'un dossier</a>'),
    ('<a href="/ar/book-consultation/">احجز موعدًا</a>', '<a href="/ar/book-consultation/">احجز موعدًا</a> · <a href="/ar/case-process/">سير الملف</a>'),
)
for f in glob.glob(R + '**/*.html', recursive=True):
    t = s = open(f, encoding='utf-8').read()
    if '/deroulement-dossier-immigration/' in t or '/ar/case-process/' in t:
        continue
    for a, b in PAIRS:
        if a in t:
            t = t.replace(a, b, 1)
            break
    if t != s:
        open(f, 'w', encoding='utf-8').write(t); k += 1
print('deroulement_link : modifié', k, 'fichiers')
