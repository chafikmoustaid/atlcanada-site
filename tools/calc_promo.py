#!/usr/bin/env python3
"""Rend le calculateur Entrée express visible : lien dans le menu + bandeau promotionnel.
Idempotent : peut être relancé après chaque génération des pages."""
import glob, re, os

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') + '/'
FR_URL, AR_URL = '/calculateur-entree-express/', '/ar/express-entry-calculator/'

GAUGE = ('<svg class="cp-gauge" viewBox="0 0 160 160" aria-hidden="true" focusable="false" style="direction:ltr"><rect x="34" y="14" width="92" height="132" rx="14" fill="rgba(255,255,255,.08)" stroke="rgba(255,255,255,.28)" stroke-width="3"/><rect x="46" y="28" width="68" height="34" rx="7" fill="rgba(255,255,255,.14)"/><text x="80" y="52" text-anchor="middle" font-family="Lora,Georgia,serif" font-size="22" fill="#fff">CRS</text><circle cx="56" cy="82" r="8" fill="rgba(255,255,255,.4)"/><circle cx="80" cy="82" r="8" fill="rgba(255,255,255,.4)"/><circle cx="104" cy="82" r="8" fill="rgba(255,255,255,.4)"/><circle cx="56" cy="104" r="8" fill="rgba(255,255,255,.4)"/><circle cx="80" cy="104" r="8" fill="rgba(255,255,255,.4)"/><circle cx="104" cy="104" r="8" fill="rgba(255,255,255,.4)"/><circle cx="56" cy="126" r="8" fill="rgba(255,255,255,.4)"/><circle cx="80" cy="126" r="8" fill="rgba(255,255,255,.4)"/><circle cx="104" cy="126" r="8" fill="#FF5A61"/></svg>')

BAND_FR = ('<section class="calc-promo" aria-label="Calculateur de points Entrée express"><div class="wrap cp-in">'
           '<div class="cp-copy"><p class="cp-eyebrow">Outil gratuit · 2 minutes</p>'
           '<h2>Quel est votre score Entrée express ?</h2>'
           '<p>Estimez-le avec la grille d\'IRCC en vigueur depuis le 3 novembre 2026. Vos réponses restent dans votre navigateur.</p>'
           f'<a class="cp-btn" href="{FR_URL}">Calculer mon score <span aria-hidden="true">→</span></a></div>'
           f'<div class="cp-art">{GAUGE}</div></div></section>')
BAND_AR = ('<section class="calc-promo" aria-label="حاسبة نقاط الدخول السريع"><div class="wrap cp-in">'
           '<div class="cp-copy"><p class="cp-eyebrow">أداة مجانية · دقيقتان</p>'
           '<h2>كم درجتك في الدخول السريع؟</h2>'
           '<p>قدّرها وفق جدول IRCC المعمول به منذ 3 نوفمبر 2026. تبقى إجاباتك داخل متصفحك.</p>'
           f'<a class="cp-btn" href="{AR_URL}">احسب درجتي <span aria-hidden="true">←</span></a></div>'
           f'<div class="cp-art">{GAUGE}</div></div></section>')

changed = 0
for f in glob.glob(R + '**/*.html', recursive=True):
    rel = os.path.relpath(f, R).replace('\\', '/')
    if rel.startswith(('calculateur-entree-express/', 'ar/express-entry-calculator/')):
        continue
    t = s = open(f, encoding='utf-8').read()
    ar = 'dir="rtl"' in t[:400] or rel.startswith('ar/')
    url, band, label = (AR_URL, BAND_AR, 'الحاسبة') if ar else (FR_URL, BAND_FR, 'Calculateur')

    # 1) lien dans le menu (bureau + mobile), juste après le lien Actualités
    if 'class="nav-calc"' not in t:
        pat = re.compile(r'(<a class="nav-news"[^>]*>.*?</a>)', re.S)
        t = pat.sub(lambda m: m.group(1) + f'<a class="nav-calc" href="{url}">{label}</a>', t)

    # 2) bandeau promotionnel (accueil, Maroc, AR, pages Entrée express et résidence)
    if 'class="calc-promo"' not in t:
        if rel == 'index.html':
            t = t.replace('<section class="services"', band + '\n<section class="services"', 1)
        elif rel in ('maroc/index.html', 'ar/index.html') or rel in (
                'entree-express-canada/index.html', 'entree-express-francophone-maroc/index.html',
                'residence-permanente-canada/index.html', 'candidats-provinces-canada/index.html',
                'ar/express-entry/index.html', 'ar/express-entry-french/index.html',
                'ar/permanent-residence/index.html', 'ar/provincial-nominee/index.html'):
            m = re.search(r'(<section class="pg-hero">.*?</section>)', t, re.S)
            if m:
                t = t[:m.end()] + '\n' + band + t[m.end():]
    if t != s:
        open(f, 'w', encoding='utf-8').write(t)
        changed += 1
print('calc_promo : modifié', changed, 'fichiers')
