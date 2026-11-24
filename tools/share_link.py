#!/usr/bin/env python3
"""Bouton « Envoyer à un proche » (WhatsApp) dans l'encadré des coûts et les pages de coût (idempotent)."""
import glob, os, re, urllib.parse
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') + '/'
SITE = 'https://www.atlcanada.com'
n = 0
for f in glob.glob(R + '**/index.html', recursive=True):
    t = s = open(f, encoding='utf-8').read()
    if 'class="fee-share"' in t or 'class="fee-note"' not in t: continue
    rel = os.path.relpath(f, R)[:-len('index.html')]
    ar = rel.startswith('ar/')
    txt = ('ATL Canada : %s ' if not ar else 'ATL Canada: %s ') % ('combien coûte ce dossier' if not ar else 'كم تكلفة هذا الملف') + SITE + '/' + rel
    a = '<a class="fee-share" target="_blank" rel="noopener" href="https://wa.me/?text=%s">%s</a>' % (urllib.parse.quote(txt), 'أرسل إلى قريب عبر واتساب' if ar else 'Envoyer à un proche (WhatsApp)')
    t = re.sub(r'(<p class="fee-note">.*?)(</p>)', lambda m: m.group(1) + ' · ' + a + m.group(2), t, count=1, flags=re.S)
    if t != s:
        open(f, 'w', encoding='utf-8').write(t); n += 1
print('share_link : modifié', n, 'fichiers')
