#!/usr/bin/env python3
"""Génère la section Actualités (accueil + page /actualites/, en français seulement)
à partir de data/actualites.json, puis met à jour sitemap.xml et llms.txt.
Usage : python3 tools/build_news.py   (depuis la racine du dépôt)"""
import json, re, html, os
from datetime import date

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
SITE = 'https://www.atlcanada.com'
OG = SITE + '/assets/og-image.png'
# Règle : la dernière publication ajoutée est toujours la première en haut (à date égale, l'ordre d'ajout dans le JSON décide).
_raw = json.load(open(R + 'data/actualites.json', encoding='utf-8'))
items = [it for _, it in sorted(enumerate(_raw), key=lambda t: (t[1]['date'], t[0]), reverse=True)]
MOIS_FR = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.']
MOIS_AR = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
e = html.escape
# Traductions arabes (fichier séparé : id -> tag, title, summary, impact, links). Seules les entrées traduites figurent sur /ar/actualites/.
try:
    _ar = json.load(open(R + 'data/actualites_ar.json', encoding='utf-8'))
except FileNotFoundError:
    _ar = {}
items_ar = []
for _it in items:
    _t = _ar.get(_it['id'])
    if _t:
        _m = dict(_it); _m.update(tag_ar=_t['tag'], title_ar=_t['title'], summary_ar=_t['summary'], impact_ar=_t['impact'], links_ar=_t.get('links', []))
        _m.pop('visuels', None)
        items_ar.append(_m)
OFFICIAL = ('canada.ca', 'gc.ca', 'alberta.ca', 'gov.bc.ca', 'welcomebc.ca', 'quebec.ca', 'college-ic.ca', 'atlcanada.com')

def fdate(iso, lang):
    d = date.fromisoformat(iso)
    if lang == 'ar':
        return f"{d.day} {MOIS_AR[d.month-1]} {d.year}"
    return f"{'1er' if d.day == 1 else d.day} {MOIS_FR[d.month-1]} {d.year}"

# ---------- images allégées (WebP) et thèmes de filtre ----------
def img_src(src):
    """Retourne la version WebP d'une illustration PNG (créée si besoin), si elle est plus légère."""
    if not src.lower().endswith('.png') or not src.startswith('/assets/'):
        return src
    png, webp = R + src.lstrip('/'), R + src.lstrip('/')[:-4] + '.webp'
    try:
        if not os.path.exists(webp) or os.path.getmtime(webp) < os.path.getmtime(png):
            from PIL import Image
            Image.open(png).convert('RGBA' if 'A' in Image.open(png).mode else 'RGB').save(webp, 'WEBP', quality=82, method=6)
        if os.path.getsize(webp) < os.path.getsize(png):
            return src[:-4] + '.webp'
    except Exception:
        pass
    return src

THEMES = {'ar': [('all','الكل'),('express','الدخول السريع'),('rp','الإقامة الدائمة'),('prov','المقاطعات وكيبيك'),('work','العمل والدراسة'),('autre','أخرى')], 'fr': [('all', 'Tout'), ('express', 'Entrée express'), ('rp', 'Résidence permanente'),
                 ('prov', 'Provinces et Québec'), ('work', 'Travail et études'), ('autre', 'Autres')]}
TAG_THEME = {'Entrée express': 'express', 'Résidence permanente': 'rp', "Niveaux d'immigration": 'rp', 'Parrainage': 'rp',
             'Provinces': 'prov', 'Québec': 'prov', 'Travail': 'work', 'Permis de travail': 'work'}
def theme_of(it):
    t = TAG_THEME.get(it['tag_fr'])
    if t: return t
    hay = (it['id'] + ' ' + it['title_fr']).lower()
    if 'express' in hay: return 'express'
    return 'autre'

def card(it, lang):
    base = '/ar/actualites/' if lang == 'ar' else '/actualites/'
    more = 'اقرأ المزيد ←' if lang == 'ar' else 'Lire la suite →'
    th = ''
    if it.get('visuels'):
        v0 = it['visuels'][0]
        th = f'<a href="{base}#{it["id"]}" tabindex="-1" aria-hidden="true"><img class="news-thumb" src="{e(img_src(v0["src"]))}" alt="" width="{v0["width"]}" height="{v0["height"]}" loading="lazy" decoding="async"></a>'
    return (f'<article class="news-card reveal">{th}<p class="news-meta"><span class="news-tag">{e(it["tag_"+lang])}</span>'
            f'<time datetime="{it["date"]}">{fdate(it["date"], lang)}</time></p>'
            f'<h3>{e(it["title_"+lang])}</h3><p>{e(it["summary_"+lang])}</p>'
            f'<a class="more" href="{base}#{it["id"]}">{more}</a></article>')

# ---------------- accueil ----------------
idx = open(R + 'index.html', encoding='utf-8').read()
section = ('<!-- NEWS:START (généré par tools/build_news.py) -->\n'
  '  <section class="news-section" id="actualites">\n    <div class="wrap">\n'
  '      <div class="section-head reveal">\n        <p class="eyebrow">Actualités</p>\n'
  "        <h2>L'actualité de l'immigration au Canada</h2>\n"
  '        <p>Les nouvelles qui comptent pour les candidats, avec leurs sources officielles ou reconnues.</p>\n      </div>\n'
  '      <div class="news-grid">\n        ' + '\n        '.join(card(i, 'fr') for i in items[:3]) + '\n      </div>\n'
  '      <p class="news-all reveal"><a href="/actualites/">Toutes les actualités →</a></p>\n'
  '    </div>\n  </section>\n  <!-- NEWS:END -->\n')
if '<!-- NEWS:START' in idx:
    idx = re.sub(r'<!-- NEWS:START.*?<!-- NEWS:END -->\n', lambda m: section, idx, flags=re.S)
else:
    marker = '  <section class="cabinet" id="cabinet">'
    assert marker in idx
    idx = idx.replace(marker, section + '\n' + marker, 1)
if 'news.css' not in idx:
    idx = idx.replace('</head>', '<link rel="stylesheet" href="/assets/news.css">\n</head>', 1)
if 'href="/actualites/"' not in idx.split('<footer>')[1]:
    idx = idx.replace('<li><a href="/maroc/">Immigrer depuis le Maroc</a></li>', '<li><a href="/maroc/">Immigrer depuis le Maroc</a></li>\n          <li><a href="/actualites/">Actualités</a></li>', 1)
open(R + 'index.html', 'w', encoding='utf-8').write(idx)

# ---------------- pages d'archive ----------------
T = {
 'fr': dict(path='actualites/', lang='fr-CA', loc='fr_CA', dir='ltr',
   title="Actualités de l'immigration au Canada | ATL Canada",
   desc="Nouvelles de l'immigration au Canada expliquées simplement : Entrée express, résidence permanente, permis d'études et de travail. Sources vérifiables.",
   h1="L'actualité de l'immigration au Canada", lede="Les nouvelles qui comptent pour les candidats, expliquées simplement, avec leurs sources.",
   impact="Ce que cela signifie pour vous", src="Sources", home='Accueil', crumb='Actualités', cta='Prendre rendez-vous',
   note="Ces informations sont générales et ne constituent pas un avis juridique. Elles reposent sur les sources citées et peuvent changer : vérifiez toujours les règles en vigueur sur canada.ca. Pour une évaluation de votre situation, prenez rendez-vous.",
   nav=[('/', 'Accueil'), ('/maroc/', 'Depuis le Maroc')],alt='<a href="/ar/actualites/" lang="ar" hreflang="ar">العربية</a>',
   foot='Consultant réglementé en immigration canadienne (CRIC), permis R712906 du CCIC.'),
}

T['ar'] = dict(path='ar/actualites/', lang='ar-MA', loc='ar_MA', dir='rtl',
   title="أخبار الهجرة إلى كندا | ATL Canada",
   desc="مستجدات الهجرة إلى كندا مشروحة ببساطة: الدخول السريع، الإقامة الدائمة، برامج المقاطعات، تصاريح الدراسة والعمل. مع المصادر الرسمية.",
   h1="أخبار الهجرة إلى كندا", lede="أهم المستجدات للمرشحين، مشروحة ببساطة مع مصادرها الرسمية. تُنشر بالعربية مختارات من أخبارنا الأخيرة.",
   impact="ماذا يعني ذلك لك: ", src="المصادر", home='الرئيسية', crumb='الأخبار', cta='احجز موعدًا', fresh='تُحدَّث بانتظام',
   note="هذه معلومات عامة وليست استشارة قانونية. تستند إلى المصادر المذكورة وقد تتغير: تحقق دائمًا من القواعد السارية في canada.ca. ولتقييم ملفك الشخصي، اتصل بنا. النسخة الفرنسية هي المرجع الأكمل.",
   nav=[('/ar/', 'الرئيسية')], alt='<a href="/actualites/" lang="fr" hreflang="fr-CA">Français</a>',
   foot='مستشار هجرة كندية مرخَّص (CRIC)، رخصة CCIC رقم R712906.')

# liens vers la page de service concernée (ajoutés sous chaque actualité)
LIENS = [
 (('dossiers-non-finalises',), [('/dossiers-en-attente-ircc/', 'Graphique interactif des dossiers en attente'), ('/residence-permanente-canada/', 'Résidence permanente')]),
 (('visiteur', 'visa', 'super-visa'), [('/visa-visiteur-super-visa-canada/', 'Visa de visiteur')]),
 (('plan-niveaux', 'niveaux d', 'admissions'), [('/residence-permanente-canada/', 'Résidence permanente')]),
 (('peq', 'quebec', 'québec', 'csq', 'pstq'), [('/immigration-quebec-canada/', 'Immigrer au Québec')]),
 (('bc-pnp', 'pnp', 'candidats des provinces', 'colombie', 'provinc', 'ontario', 'alberta'), [('/candidats-provinces-canada/', 'Candidats des provinces')]),
 (('entree-express', 'entrée express', 'express'), [('/entree-express-canada/', 'Entrée express'), ('/calculateur-entree-express/', 'Calculateur de points')]),
 (('permis-de-travail', 'permis de travail', 'travail'), [('/permis-de-travail-canada/', 'Permis de travail')]),
 (('parrainage',), [('/parrainage-familial-canada/', 'Parrainage familial')]),
 (('etudes', 'études', 'etudiant', 'étudiant'), [('/permis-etudes-canada-maroc/', "Permis d'études")]),
 (('citoyennet',), [('/citoyennete-canadienne/', 'Citoyenneté canadienne')]),
 (('residence-permanente', 'résidence permanente'), [('/residence-permanente-canada/', 'Résidence permanente')]),
]
def liens_for(it):
    hay = (it['id'] + ' ' + it['tag_fr'] + ' ' + it['title_fr']).lower()
    for keys, links in LIENS:
        if any(k in hay for k in keys): return links
    return []

def filters(lang, L=None):
    L = items if L is None else L
    th = THEMES.get(lang, THEMES['fr'])
    counts = {k: sum(1 for i in L if k == 'all' or theme_of(i) == k) for k, _ in th}
    chips = ''.join(f'<button type="button" class="news-chip" data-theme="{k}" aria-pressed="{"true" if k == "all" else "false"}">{e(lbl)} <span>{counts[k]}</span></button>' for k, lbl in th if counts[k])
    return f'<div class="news-filters" role="group" aria-label="{'تصفية حسب الموضوع' if lang == 'ar' else 'Filtrer par thème'}" data-more="Afficher plus d\'actualités" hidden>{chips}</div>'

def article(it, p, lang):
    _s = it['sources']
    if lang == 'ar':
        _s = [x for x in _s if any(d in x['url'] for d in OFFICIAL)]
    srcs = ' · '.join(f'<a href="{e(s["url"])}" rel="noopener" target="_blank">{e(s["name"])}</a>' for s in _s)
    go = ''
    if lang == 'ar' and it.get('links_ar'):
        go = '<p class="news-go">للمزيد : ' + ' · '.join(f'<a href="{u}">{e(l)}</a>' for u, l in it['links_ar']) + '</p>'
    if lang == 'fr' and liens_for(it):
        go = '<p class="news-go">Pour aller plus loin : ' + ' · '.join(f'<a href="{u}">{e(l)}</a>' for u, l in liens_for(it)) + '</p>'
    figs = '' if lang == 'ar' else ''.join((f'<h3>{e(v["heading_"+lang])}</h3><p>{e(v["text_"+lang])}</p>' if v.get('heading_'+lang) else '') + f'<figure class="news-figure"><img src="{e(img_src(v["src"]))}" decoding="async" alt="{e(v["alt_"+lang])}" width="{v["width"]}" height="{v["height"]}" loading="lazy">'
                   f'<figcaption>{e(v["caption_"+lang])}</figcaption></figure>' for v in it.get('visuels', []))
    return (f'<article class="news-item" id="{it["id"]}" data-theme="{theme_of(it)}"><p class="news-meta"><span class="news-tag">{e(it["tag_"+lang])}</span>'
            f'<time datetime="{it["date"]}">{fdate(it["date"], lang)}</time></p>'
            f'<h2>{e(it["title_"+lang])}</h2><p>{e(it["summary_"+lang])}</p>{figs}'
            f'<div class="news-impact"><strong>{p["impact"]}</strong>{e(it["impact_"+lang])}</div>'
            f'{go}'
            f'<p class="news-sources">{p["src"]} : {srcs}</p></article>')

for lang, p in T.items():
    L = items_ar if lang == 'ar' else items
    url = f'{SITE}/{p["path"]}'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url + '#webpage', "url": url, "name": p['title'], "description": p['desc'], "inLanguage": p['lang'],
         "isPartOf": {"@id": SITE + '/#website'}, "publisher": {"@id": SITE + '/#organization'}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": p['home'], "item": SITE + ('/ar/' if lang == 'ar' else '/')},
            {"@type": "ListItem", "position": 2, "name": p['crumb'], "item": url}]},
        {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": n + 1, "item": {"@type": "NewsArticle", "headline": it['title_'+lang], "datePublished": it['date'],
              "inLanguage": p['lang'], "url": f'{url}#{it["id"]}', "description": it['summary_'+lang],
              "author": {"@id": SITE + '/#organization'}, "publisher": {"@id": SITE + '/#organization'},
              "citation": [s['url'] for s in it['sources']], "image": (SITE + it["visuels"][0]["src"]) if it.get("visuels") else OG}} for n, it in enumerate(L)]}]}
    nav = ''.join(f'<a href="{h}">{t}</a>' for h, t in p['nav'])
    fonts = 'https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600&family=Source+Sans+3:wght@400;500;600;700&family=Cairo:wght@400;600;700&display=swap'
    page = f'''<!doctype html>
<html lang="{p['lang']}" dir="{p['dir']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p['title'])}</title>
<meta name="description" content="{e(p['desc'])}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="fr-CA" href="{SITE}/actualites/">
<link rel="alternate" hreflang="ar" href="{SITE}/ar/actualites/">
<link rel="alternate" hreflang="x-default" href="{SITE}/actualites/">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta name="theme-color" content="#16233D">
<link rel="icon" type="image/png" href="/assets/logo.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="ATL Canada"><meta property="og:locale" content="{p['loc']}">
<meta property="og:title" content="{e(p['title'])}"><meta property="og:description" content="{e(p['desc'])}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{OG}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(p['title'])}"><meta name="twitter:description" content="{e(p['desc'])}"><meta name="twitter:image" content="{OG}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{fonts}" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<link rel="stylesheet" href="/assets/news.css">
<style>.pg-hero{{position:relative;overflow:hidden;background:radial-gradient(900px 340px at 85% -10%,rgba(225,35,43,.28),transparent 60%),linear-gradient(160deg,#0E1A32,#1B2D52);color:#E7ECF5;padding:64px 0 58px;border-bottom:4px solid #E1232B}}.pg-hero h1{{font-family:'Lora',serif;font-weight:600;font-size:clamp(2.2rem,5vw,3.4rem);line-height:1.12;margin:0 0 16px;color:#fff}}.pg-hero .lede{{font-size:1.2rem;max-width:none;margin:0;color:#F1F4FA}}.pg-hero .eyebrow{{display:inline-flex;align-items:center;gap:10px;color:#fff;background:#E1232B;border-radius:999px;padding:6px 14px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;font-size:.8rem;margin:0 0 18px}}.pg-hero .eyebrow::before{{display:none}}.crumb{{font-size:.9rem;margin:0 0 18px;color:#AEB9CE}}.crumb a{{color:#fff}}</style>
</head>
<body>
<div class="topbar">
  <div class="wrap">
    <div class="topbar-left"><a href="/#adresses"><strong>Montréal</strong></a> <span class="sep">·</span> <a href="/maroc/#bureaux"><strong>Casablanca</strong></a></div>
    <div class="topbar-right">
    </div>
  </div>
</div>
<header class="site">
  <div class="nav-row">
    <a class="brand" href="{'/ar/' if lang == 'ar' else '/'}"><img src="/assets/logo-b-dark.svg" alt="ATL Canada, Immigration Consulting" width="286" height="68"></a>
    <nav class="primary" aria-label="Navigation">{nav}</nav>
    <div class="nav-actions"><span class="lang">{p['alt'].replace('<a ', '<a style="color:#fff;margin:0 14px" ')}</span><a class="btn btn-solid" href="/#contact">{p['cta']}</a></div>
  </div>
</header>
<main>
<section class="pg-hero"><div class="wrap">
  <p class="crumb"><a href="{'/ar/' if lang == 'ar' else '/'}">{p['home']}</a> › {p['crumb']}</p>
  <p class="eyebrow"><span class="live-dot" aria-hidden="true"></span>{p.get("fresh", "Mis à jour régulièrement")}</p>
  <h1>{p['h1']}</h1>
  <p class="lede">{p['lede']}</p>
</div></section>
<section class="news-page"><div class="wrap">
{filters(lang, L)}
<div id="news-list">
{chr(10).join(article(i, p, lang) for i in L)}
</div>
<p class="news-more-wrap" hidden><button type="button" class="news-more-btn" id="news-more"></button></p>
<p class="news-disclaimer">{p['note']}</p>
</div></section>
</main>
<footer><div class="wrap"><div class="footer-bottom"><span>© 2026 ATL Canada</span><span>{p['foot']}</span></div></div></footer>
<script src="/assets/news.js" defer></script>
</body></html>'''
    os.makedirs(R + p['path'], exist_ok=True)
    open(R + p['path'] + 'index.html', 'w', encoding='utf-8').write(page)

# ---------------- sitemap + llms.txt ----------------
last = items[0]['date']
urls = [('/', '1.0', last), ('/maroc/', '0.9', '2026-10-09'), ('/ar/', '0.9', '2026-10-09'),
        ('/actualites/', '0.8', last),
        ('/permis-etudes-canada-maroc/', '0.8', '2026-10-26'), ('/entree-express-francophone-maroc/', '0.8', '2026-10-26'),
        ('/documents-maroc-immigration-canada/', '0.8', '2026-10-26'),
        ('/visa-visiteur-super-visa-canada/', '0.8', '2026-11-05'),
        ('/parrainage-familial-canada/', '0.8', '2026-11-05'),
        ('/permis-de-travail-canada/', '0.8', '2026-11-05'),
        ('/immigration-quebec-canada/', '0.8', '2026-11-05'),
        ('/ar/visitor-visa-super-visa/', '0.8', '2026-11-05'), ('/ar/family-sponsorship/', '0.8', '2026-11-05'),
        ('/ar/work-permit/', '0.8', '2026-11-05'), ('/ar/immigrate-to-quebec/', '0.8', '2026-11-05'),
        ('/residence-permanente-canada/', '0.8', '2026-11-05'),
        ('/entree-express-canada/', '0.8', '2026-11-05'),
        ('/calculateur-entree-express/', '0.8', '2026-11-06'), ('/ar/actualites/', '0.8', last), ('/rendez-vous/', '0.8', '2026-11-23'), ('/ar/book-consultation/', '0.8', '2026-11-23'), ('/deroulement-dossier-immigration/', '0.7', '2026-11-23'), ('/ar/case-process/', '0.7', '2026-11-23'), ('/honoraires/', '0.8', '2026-11-24'), ('/budget-immigration-canada/', '0.7', '2026-11-24'), ('/ar/budget-calculator/', '0.7', '2026-11-24'), ('/cout-permis-etudes-canada/', '0.7', '2026-11-24'), ('/cout-visa-visiteur-canada/', '0.7', '2026-11-24'), ('/documents-a-preparer-immigration-canada/', '0.7', '2026-11-24'), ('/demande-refusee-immigration-canada/', '0.7', '2026-11-24'), ('/ce-qui-change-immigration-canada/', '0.7', '2026-11-24'), ('/ar/study-permit-cost/', '0.7', '2026-11-24'), ('/ar/visitor-visa-cost/', '0.7', '2026-11-24'), ('/ar/documents-checklist/', '0.7', '2026-11-24'), ('/ar/refused-application/', '0.7', '2026-11-24'), ('/ar/whats-changing/', '0.7', '2026-11-24'), ('/en/', '0.7', '2026-11-24'), ('/en/fees/', '0.7', '2026-11-24'), ('/en/official-fees/', '0.7', '2026-11-24'), ('/en/budget-calculator/', '0.7', '2026-11-24'), ('/en/book-consultation/', '0.7', '2026-11-24'), ('/en/case-process/', '0.7', '2026-11-24'), ('/en/about/', '0.7', '2026-11-24'), ('/en/study-permit/', '0.8', '2026-11-24'), ('/en/work-permit/', '0.8', '2026-11-24'), ('/en/express-entry/', '0.8', '2026-11-24'),  ('/a-propos/', '0.7', '2026-11-24'), ('/ar/about/', '0.7', '2026-11-24'), ('/ar/fees/', '0.8', '2026-11-24'), ('/frais-officiels-immigration-canada/', '0.8', '2026-11-24'), ('/ar/official-fees/', '0.8', '2026-11-24'),
        ('/evaluer-mon-dossier/', '0.8', '2026-11-23'), ('/ar/evaluate-my-case/', '0.8', '2026-11-23'),
        ('/dossiers-en-attente-ircc/', '0.7', '2026-11-18'),
        ('/candidats-provinces-canada/', '0.8', '2026-11-05'),
        ('/citoyennete-canadienne/', '0.8', '2026-11-05'),
        ('/ar/permanent-residence/', '0.8', '2026-11-05'),
        ('/ar/express-entry/', '0.8', '2026-11-05'),
        ('/ar/express-entry-calculator/', '0.8', '2026-11-06'),
        ('/ar/provincial-nominee/', '0.8', '2026-11-05'),
        ('/ar/canadian-citizenship/', '0.8', '2026-11-05'),
        ('/gens-affaires-immigration-canada/', '0.8', '2026-11-05'), ('/ar/business-immigration/', '0.8', '2026-11-05'),
        ('/confidentialite/', '0.3', '2026-11-05'),
        ('/ar/study-permit-morocco/', '0.8', '2026-10-26'), ('/ar/express-entry-french/', '0.8', '2026-10-26'),
        ('/ar/moroccan-documents/', '0.8', '2026-10-26') ]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u, pr, lm in urls:
    sm += f'  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{lm}</lastmod>\n    <priority>{pr}</priority>\n  </url>\n'
open(R + 'sitemap.xml', 'w').write(sm + '</urlset>\n')
ll = open(R + 'llms.txt', encoding='utf-8').read()
if '/ar/study-permit-morocco/' not in ll:
    ll = ll.replace('\n## Liens', f"- [تصريح الدراسة في كندا من المغرب (العربية)]({SITE}/ar/study-permit-morocco/): المراحل ورسالة التصديق والموارد المالية والبيانات البيومترية\n- [الدخول السريع للناطقين بالفرنسية (العربية)]({SITE}/ar/express-entry-french/): النقاط الإضافية للفرنسية والبرامج والإعداد\n- [الوثائق المغربية (العربية)]({SITE}/ar/moroccan-documents/): شهادة الشرطة (البطاقة الأنتروبومترية) والبيانات البيومترية\n\n## Liens", 1)
    open(R + 'llms.txt', 'w', encoding='utf-8').write(ll)
if '/permis-etudes-canada-maroc/' not in ll:
    ll = ll.replace('\n## Liens', f"- [Permis d'études depuis le Maroc]({SITE}/permis-etudes-canada-maroc/): étapes, lettre d'attestation, preuves de fonds, biométrie\n- [Entrée express pour francophones]({SITE}/entree-express-francophone-maroc/): points pour le français, programmes, préparation\n- [Documents marocains]({SITE}/documents-maroc-immigration-canada/): certificat de police (fiche anthropométrique), biométrie VFS\n\n## Liens", 1)
    open(R + 'llms.txt', 'w', encoding='utf-8').write(ll)
if '/visa-visiteur-super-visa-canada/' not in ll:
    ll = ll.replace('\n## Liens', f"- [Visa de visiteur et super visa depuis le Maroc]({SITE}/visa-visiteur-super-visa-canada/): conditions officielles, revenu de l'hôte, assurance, examen médical\n\n## Liens", 1)
    open(R + 'llms.txt', 'w', encoding='utf-8').write(ll)
if '/parrainage-familial-canada/' not in ll:
    ll = ll.replace('\n## Liens', f"- [Parrainage familial au Canada]({SITE}/parrainage-familial-canada/): qui peut être parrainé, relation authentique, déclaration de la famille\n- [Permis de travail pour le Canada]({SITE}/permis-de-travail-canada/): permis lié à un employeur, EIMT, permis ouvert\n- [Immigrer au Québec]({SITE}/immigration-quebec-canada/): sélection par le Québec, CSQ, PSTQ, état du PEQ\n\n## Liens", 1)
    open(R + 'llms.txt', 'w', encoding='utf-8').write(ll)
if '/immigration-quebec-canada/' not in ll:
    ll = ll.replace('\n## Liens', f"- [Immigrer au Québec]({SITE}/immigration-quebec-canada/): sélection par le Québec, CSQ, PSTQ, état du PEQ\n\n## Liens", 1)
    open(R + 'llms.txt', 'w', encoding='utf-8').write(ll)
if '/residence-permanente-canada/' not in ll:
    ll = ll.replace('\n## Liens', f"- [Résidence permanente : les voies possibles]({SITE}/residence-permanente-canada/): Entrée express, provinces, Québec, famille, Atlantique\n- [Calculateur de points Entrée express]({SITE}/calculateur-entree-express/): estimation du score selon la grille IRCC du 3 novembre 2026\n- [Évaluer mon dossier]({SITE}/evaluer-mon-dossier/): questionnaire de 5 questions qui oriente vers la voie d'immigration à regarder en premier\n- [Entrée express : programmes, points, changements 2026]({SITE}/entree-express-canada/): conditions, SCG, changements du 3 novembre 2026\n- [Candidats des provinces]({SITE}/candidats-provinces-canada/): deux processus, étapes\n- [Citoyenneté canadienne]({SITE}/citoyennete-canadienne/): conditions pour les adultes\n\n## Liens", 1)
    open(R + 'llms.txt', 'w', encoding='utf-8').write(ll)
if '/gens-affaires-immigration-canada/' not in ll:
    ll = ll.replace('\n## Liens', f"- [Immigration des gens d'affaires]({SITE}/gens-affaires-immigration-canada/): état des programmes fédéraux et du Québec, autres voies\n\n## Liens", 1)
    open(R + 'llms.txt', 'w', encoding='utf-8').write(ll)
if '/actualites/' not in ll:
    ll = ll.replace('\n## Liens', f"- [Actualités de l'immigration (français)]({SITE}/actualites/): nouvelles expliquées, avec sources\n\n## Liens", 1)
    open(R + 'llms.txt', 'w', encoding='utf-8').write(ll)
if '/evaluer-mon-dossier/' not in ll:
    ll = ll.replace('\n## Liens', f"- [Évaluer mon dossier]({SITE}/evaluer-mon-dossier/): questionnaire de 5 questions qui oriente vers la voie d'immigration à regarder en premier\n\n## Liens", 1)
    open(R + 'llms.txt', 'w', encoding='utf-8').write(ll)
if '/ar/actualites/' not in ll:
    ll = ll.replace('\n## Liens', f"- [أخبار الهجرة إلى كندا (بالعربية)]({SITE}/ar/actualites/): مختارات من أحدث الأخبار مشروحة ببساطة\n\n## Liens", 1)
    open(R + 'llms.txt', 'w', encoding='utf-8').write(ll)
if '/rendez-vous/' not in ll:
    ll = ll.replace('\n## Liens', f"- [Prendre rendez-vous]({SITE}/rendez-vous/): demande de consultation (appel, WhatsApp, Teams ou bureau)\n\n## Liens", 1)
    open(R + 'llms.txt', 'w', encoding='utf-8').write(ll)
if '/honoraires/' not in ll:
    ll = ll.replace('\n## Liens', f"- [Honoraires]({SITE}/honoraires/): prix de départ des services, devis final après consultation\n- [Frais officiels]({SITE}/frais-officiels-immigration-canada/): frais du gouvernement canadien en vigueur\n\n## Liens", 1)
    open(R + 'llms.txt', 'w', encoding='utf-8').write(ll)
if '/cout-permis-etudes-canada/' not in ll:
    ll = ll.replace('\n## Liens', f"- [Coût d'un permis d'études]({SITE}/cout-permis-etudes-canada/): frais du gouvernement et honoraires\n- [Coût d'un visa de visiteur]({SITE}/cout-visa-visiteur-canada/): frais du gouvernement et honoraires\n- [Documents à préparer]({SITE}/documents-a-preparer-immigration-canada/): liste à cocher indicative\n- [Demande refusée]({SITE}/demande-refusee-immigration-canada/): premières étapes après un refus\n- [Ce qui change]({SITE}/ce-qui-change-immigration-canada/): frais et règles\n\n## Liens", 1)
    open(R + 'llms.txt', 'w', encoding='utf-8').write(ll)
if '/en/fees/' not in ll:
    ll = ll.replace('\n## Liens', f"- [English: home]({SITE}/en/): immigration consultant in Montréal and Casablanca\n- [English: fees]({SITE}/en/fees/): starting fees and official government fees\n- [English: budget calculator]({SITE}/en/budget-calculator/): estimate of fees and government costs\n- [English: study permit]({SITE}/en/study-permit/)\n- [English: work permit]({SITE}/en/work-permit/)\n- [English: Express Entry]({SITE}/en/express-entry/)\n- [English: book a consultation]({SITE}/en/book-consultation/)\n\n## Liens", 1)
    open(R + 'llms.txt', 'w', encoding='utf-8').write(ll)
if '/en/study-permit/' not in ll:
    ll = ll.replace('\n## Liens', f"- [English: study permit]({SITE}/en/study-permit/)\n- [English: work permit]({SITE}/en/work-permit/)\n- [English: Express Entry]({SITE}/en/express-entry/)\n\n## Liens", 1)
    open(R + 'llms.txt', 'w', encoding='utf-8').write(ll)
if '/budget-immigration-canada/' not in ll:
    ll = ll.replace('\n## Liens', f"- [Calculateur de budget]({SITE}/budget-immigration-canada/): estimation des honoraires et des frais du gouvernement\n- [À propos]({SITE}/a-propos/): consultant réglementé, bureaux de Montréal et Casablanca\n\n## Liens", 1)
    open(R + 'llms.txt', 'w', encoding='utf-8').write(ll)
if '/deroulement-dossier-immigration/' not in ll:
    ll = ll.replace('\n## Liens', f"- [Déroulement d'un dossier]({SITE}/deroulement-dossier-immigration/): étapes de l'accompagnement et ce qu'un consultant ne peut pas promettre\n\n## Liens", 1)
    open(R + 'llms.txt', 'w', encoding='utf-8').write(ll)
print('ok', len(items), 'actualités')

# post-traitement automatique (design, contacts, confidentialité) : évite qu'une régénération n'écrase les ajouts
import subprocess
subprocess.run(['sh', R + 'tools/postprocess.sh'], check=False)
