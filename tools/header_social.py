#!/usr/bin/env python3
"""Supprime la barre du haut et place les logos Facebook/Instagram dans la navigation, à côté de « Contact ». Idempotent."""
import re, glob, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOC = {}
for lang, f in (('fr', 'index.html'), ('ar', 'ar/index.html')):
    t = open(os.path.join(root, f), encoding='utf-8').read()
    m = re.search(r'<span class="tb-social">.*?</span>(?=\s*</div>)', t, re.S)
    if m:
        SOC[lang] = m.group(0)
cache = os.path.join(root, 'tools', '_social.json')
import json
if len(SOC) == 2:
    json.dump(SOC, open(cache, 'w', encoding='utf-8'))
else:
    SOC = json.load(open(cache, encoding='utf-8'))
n = 0
for f in glob.glob(os.path.join(root, '**/*.html'), recursive=True):
    t = o = open(f, encoding='utf-8').read()
    ar = 'dir="rtl"' in t[:400] or 'lang="ar"' in t[:200]
    soc = SOC['ar' if ar else 'fr'].replace('class="tb-social"', 'class="tb-social nav-social"')
    t = re.sub(r'<div class="topbar">(?:.*?</div>){4}\s*', '', t, count=1, flags=re.S)
    if 'nav-social' not in t and '<nav class="primary"' in t:
        t = re.sub(r'(<nav class="primary".*?)(</nav>)', lambda m: m.group(1) + soc + m.group(2), t, count=1, flags=re.S)
        t = re.sub(r'(<nav class="mobile-nav".*?)(</nav>)', lambda m: m.group(1) + soc + m.group(2), t, count=1, flags=re.S)
    if t != o:
        open(f, 'w', encoding='utf-8').write(t); n += 1
print('modifié :', n, 'fichiers')
