#!/usr/bin/env python3
"""Ajoute le lien « Évaluer mon dossier » dans les pieds de page (idempotent)."""
import glob, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') + '/'
FR = ('<a href="/calculateur-entree-express/">Calculateur Entrée express</a>', ' · <a href="/evaluer-mon-dossier/">Évaluer mon dossier</a>', '/evaluer-mon-dossier/')
AR = ('<a href="/ar/express-entry-calculator/">حاسبة الدخول السريع</a>', ' · <a href="/ar/evaluate-my-case/">قيّم ملفك</a>', '/ar/evaluate-my-case/')
LI = ('<li><a href="/calculateur-entree-express/">Calculateur de points Entrée express</a></li>', '\n          <li><a href="/evaluer-mon-dossier/">Évaluer mon dossier</a></li>', '/evaluer-mon-dossier/')
n = 0
for f in glob.glob(R + '**/*.html', recursive=True):
    t = s = open(f, encoding='utf-8').read()
    for anchor, add, mark in (FR, AR, LI):
        if anchor in t and mark not in t:
            t = t.replace(anchor, anchor + add, 1)
    if t != s:
        open(f, 'w', encoding='utf-8').write(t); n += 1
print('eval_link : modifié', n, 'fichiers')
