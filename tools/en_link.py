#!/usr/bin/env python3
"""Lien « English » dans l'en-tête des pages FR/AR et hreflang en (idempotent)."""
import glob, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') + '/'
SITE = 'https://www.atlcanada.com'
EN_OF = {'': 'en/', 'ar/': 'en/', 'honoraires/': 'en/fees/', 'ar/fees/': 'en/fees/', 'frais-officiels-immigration-canada/': 'en/official-fees/', 'ar/official-fees/': 'en/official-fees/',
 'budget-immigration-canada/': 'en/budget-calculator/', 'ar/budget-calculator/': 'en/budget-calculator/', 'rendez-vous/': 'en/book-consultation/', 'ar/book-consultation/': 'en/book-consultation/',
 'deroulement-dossier-immigration/': 'en/case-process/', 'ar/case-process/': 'en/case-process/', 'a-propos/': 'en/about/', 'ar/about/': 'en/about/'}
n = 0
for f in glob.glob(R + '**/index.html', recursive=True):
    rel = os.path.relpath(f, R)[:-len('index.html')]
    if rel.startswith('en/'): continue
    t = s = open(f, encoding='utf-8').read()
    en = EN_OF.get(rel)
    if en and 'hreflang="en"' not in t and '<link rel="alternate" hreflang="x-default"' in t:
        t = t.replace('<link rel="alternate" hreflang="x-default"', '<link rel="alternate" hreflang="en" href="%s/%s">\n<link rel="alternate" hreflang="x-default"' % (SITE, en), 1)
    if 'hreflang="en" lang="en"' not in t and '<span class="lang"' in t:
        link = '<a style="color:#fff;margin:0 10px" href="/%s" lang="en" hreflang="en" hreflang="en"><span class="l-full">English</span><span class="l-short">EN</span></a>' % (en or 'en/')
        link = link.replace(' hreflang="en" hreflang="en"', ' hreflang="en"').replace('lang="en" hreflang="en"', 'hreflang="en" lang="en"')
        i = t.index('<span class="lang"'); j = t.index('>', i) + 1
        t = t[:j] + link + t[j:]
    if t != s:
        open(f, 'w', encoding='utf-8').write(t); n += 1
print('en_link : modifié', n, 'fichiers')
