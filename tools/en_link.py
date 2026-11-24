#!/usr/bin/env python3
"""Lien « English » dans l'en-tête des pages FR/AR et hreflang en (idempotent)."""
import glob, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') + '/'
SITE = 'https://www.atlcanada.com'
EN_OF = { 'cout-permis-etudes-canada/': 'en/study-permit-cost/', 'ar/study-permit-cost/': 'en/study-permit-cost/', 'cout-visa-visiteur-canada/': 'en/visitor-visa-cost/', 'ar/visitor-visa-cost/': 'en/visitor-visa-cost/', 'documents-a-preparer-immigration-canada/': 'en/documents-checklist/', 'ar/documents-checklist/': 'en/documents-checklist/', 'demande-refusee-immigration-canada/': 'en/refused-application/', 'ar/refused-application/': 'en/refused-application/', 'ce-qui-change-immigration-canada/': 'en/whats-changing/', 'ar/whats-changing/': 'en/whats-changing/', 'evaluer-mon-dossier/': 'en/evaluate-my-case/', 'ar/evaluate-my-case/': 'en/evaluate-my-case/','': 'en/', 'ar/': 'en/', 'honoraires/': 'en/fees/', 'ar/fees/': 'en/fees/', 'frais-officiels-immigration-canada/': 'en/official-fees/', 'ar/official-fees/': 'en/official-fees/',
 'budget-immigration-canada/': 'en/budget-calculator/', 'ar/budget-calculator/': 'en/budget-calculator/', 'rendez-vous/': 'en/book-consultation/', 'ar/book-consultation/': 'en/book-consultation/',
 'deroulement-dossier-immigration/': 'en/case-process/', 'ar/case-process/': 'en/case-process/', 'a-propos/': 'en/about/', 'parrainage-familial-canada/': 'en/family-sponsorship/', 'ar/family-sponsorship/': 'en/family-sponsorship/', 'visa-visiteur-super-visa-canada/': 'en/visitor-visa/', 'ar/visitor-visa-super-visa/': 'en/visitor-visa/', 'citoyennete-canadienne/': 'en/citizenship/', 'ar/canadian-citizenship/': 'en/citizenship/', 'residence-permanente-canada/': 'en/permanent-residence/', 'ar/permanent-residence/': 'en/permanent-residence/', 'candidats-provinces-canada/': 'en/provincial-nominee/', 'ar/provincial-nominee/': 'en/provincial-nominee/', 'immigration-quebec-canada/': 'en/immigrate-to-quebec/', 'ar/immigrate-to-quebec/': 'en/immigrate-to-quebec/', 'gens-affaires-immigration-canada/': 'en/business-immigration/', 'ar/business-immigration/': 'en/business-immigration/', 'entree-express-francophone-maroc/': 'en/express-entry-french/', 'ar/express-entry-french/': 'en/express-entry-french/', 'documents-maroc-immigration-canada/': 'en/moroccan-documents/', 'ar/moroccan-documents/': 'en/moroccan-documents/', 'permis-etudes-canada-maroc/': 'en/study-permit/', 'ar/study-permit-morocco/': 'en/study-permit/', 'permis-de-travail-canada/': 'en/work-permit/', 'ar/work-permit/': 'en/work-permit/', 'entree-express-canada/': 'en/express-entry/', 'ar/express-entry/': 'en/express-entry/', 'ar/about/': 'en/about/'}
n = 0
for f in glob.glob(R + '**/index.html', recursive=True):
    rel = os.path.relpath(f, R)[:-len('index.html')]
    if rel.startswith('en/'): continue
    t = s = open(f, encoding='utf-8').read()
    en = EN_OF.get(rel)
    if en and en != 'en/' and 'href="/en/" hreflang="en" lang="en"' in t:
        t = t.replace('href="/en/" hreflang="en" lang="en"', 'href="/%s" hreflang="en" lang="en"' % en)
    if en and '<link rel="alternate" hreflang="en"' not in t and '<link rel="alternate" hreflang="x-default"' in t:
        t = t.replace('<link rel="alternate" hreflang="x-default"', '<link rel="alternate" hreflang="en" href="%s/%s">\n<link rel="alternate" hreflang="x-default"' % (SITE, en), 1)
    if 'hreflang="en" lang="en"' not in t and '<span class="lang"' in t:
        link = '<a style="color:#fff;margin:0 10px" href="/%s" lang="en" hreflang="en" hreflang="en"><span class="l-full">English</span><span class="l-short">EN</span></a>' % (en or 'en/')
        link = link.replace(' hreflang="en" hreflang="en"', ' hreflang="en"').replace('lang="en" hreflang="en"', 'hreflang="en" lang="en"')
        i = t.index('<span class="lang"'); j = t.index('>', i) + 1
        t = t[:j] + link + t[j:]
    if t != s:
        open(f, 'w', encoding='utf-8').write(t); n += 1
print('en_link : modifié', n, 'fichiers')
