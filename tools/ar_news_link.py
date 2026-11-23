#!/usr/bin/env python3
"""Dans les pages arabes, le lien du menu « Actualités » pointe vers /ar/actualites/ et porte un libellé arabe (idempotent)."""
import glob, os, re
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') + '/'
pat = re.compile(r'<a class="nav-news" href="/actualites/" lang="fr" hreflang="fr-CA">(<span class="live-dot" aria-hidden="true"></span>)Actualités</a>')
n = 0
for f in glob.glob(R + 'ar/**/*.html', recursive=True):
    t = s = open(f, encoding='utf-8').read()
    t = pat.sub(r'<a class="nav-news" href="/ar/actualites/" lang="ar" hreflang="ar">\1الأخبار</a>', t)
    if t != s:
        open(f, 'w', encoding='utf-8').write(t); n += 1
print('ar_news_link : modifié', n, 'fichiers')
