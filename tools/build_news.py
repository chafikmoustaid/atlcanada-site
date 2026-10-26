#!/usr/bin/env python3
"""Génère la section Actualités (accueil + page /actualites/, en français seulement)
à partir de data/actualites.json, puis met à jour sitemap.xml et llms.txt.
Usage : python3 tools/build_news.py   (depuis la racine du dépôt)"""
import json, re, html, os
from datetime import date

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
SITE = 'https://www.atlcanada.com'
OG = SITE + '/assets/og-image.png'
items = sorted(json.load(open(R + 'data/actualites.json', encoding='utf-8')), key=lambda x: x['date'], reverse=True)
MOIS_FR = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.']
MOIS_AR = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
e = html.escape

def fdate(iso, lang):
    d = date.fromisoformat(iso)
    if lang == 'ar':
        return f"{d.day} {MOIS_AR[d.month-1]} {d.year}"
    return f"{'1er' if d.day == 1 else d.day} {MOIS_FR[d.month-1]} {d.year}"

def card(it, lang):
    base = '/ar/actualites/' if lang == 'ar' else '/actualites/'
    more = 'اقرأ المزيد ←' if lang == 'ar' else 'Lire la suite →'
    return (f'<article class="news-card reveal"><p class="news-meta"><span class="news-tag">{e(it["tag_"+lang])}</span>'
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
   nav=[('/', 'Accueil'), ('/maroc/', 'Depuis le Maroc')],alt='',
   foot='Consultant réglementé en immigration canadienne (CRIC), permis R712906 du CCIC.'),
}

def article(it, p, lang):
    srcs = ' · '.join(f'<a href="{e(s["url"])}" rel="noopener" target="_blank">{e(s["name"])}</a>' for s in it['sources'])
    figs = ''.join(f'<figure class="news-figure"><img src="{e(v["src"])}" alt="{e(v["alt_"+lang])}" width="{v["width"]}" height="{v["height"]}" loading="lazy">'
                   f'<figcaption>{e(v["caption_"+lang])}</figcaption></figure>' for v in it.get('visuels', []))
    return (f'<article class="news-item" id="{it["id"]}"><p class="news-meta"><span class="news-tag">{e(it["tag_"+lang])}</span>'
            f'<time datetime="{it["date"]}">{fdate(it["date"], lang)}</time></p>'
            f'<h2>{e(it["title_"+lang])}</h2><p>{e(it["summary_"+lang])}</p>{figs}'
            f'<div class="news-impact"><strong>{p["impact"]}</strong>{e(it["impact_"+lang])}</div>'
            f'<p class="news-sources">{p["src"]} : {srcs}</p></article>')

for lang, p in T.items():
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
              "citation": [s['url'] for s in it['sources']], "image": (SITE + it["visuels"][0]["src"]) if it.get("visuels") else OG}} for n, it in enumerate(items)]}]}
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
    <div class="topbar-left"><a href="/#adresses"><strong>Montréal</strong></a> <span class="sep">·</span> <a href="/maroc/#bureaux"><strong>Casablanca</strong></a> <span class="sep">|</span> Service en français, anglais et arabe</div>
    <div class="topbar-right">
    </div>
  </div>
</div>
<header class="site">
  <div class="nav-row">
    <a class="brand" href="{'/ar/' if lang == 'ar' else '/'}"><img src="/assets/logo-b-dark.svg" alt="ATL Canada — Immigration Consulting" width="286" height="68"></a>
    <nav class="primary" aria-label="Navigation">{nav}</nav>
    <div class="nav-actions"><span class="lang">{p['alt'].replace('<a ', '<a style="color:#fff;margin:0 14px" ')}</span><a class="btn btn-solid" href="/#contact">{p['cta']}</a></div>
  </div>
</header>
<main>
<section class="pg-hero"><div class="wrap">
  <p class="crumb"><a href="{'/ar/' if lang == 'ar' else '/'}">{p['home']}</a> › {p['crumb']}</p>
  <p class="eyebrow"><span class="live-dot" aria-hidden="true"></span>Mis à jour régulièrement</p>
  <h1>{p['h1']}</h1>
  <p class="lede">{p['lede']}</p>
</div></section>
<section class="news-page"><div class="wrap">
{chr(10).join(article(i, p, lang) for i in items)}
<p class="news-disclaimer">{p['note']}</p>
</div></section>
</main>
<footer><div class="wrap"><div class="footer-bottom"><span>© 2026 ATL Canada</span><span>{p['foot']}</span></div></div></footer>
</body></html>'''
    os.makedirs(R + p['path'], exist_ok=True)
    open(R + p['path'] + 'index.html', 'w', encoding='utf-8').write(page)

# ---------------- sitemap + llms.txt ----------------
last = items[0]['date']
urls = [('/', '1.0', last), ('/maroc/', '0.9', '2026-10-09'), ('/ar/', '0.9', '2026-10-09'),
        ('/actualites/', '0.8', last),
        ('/permis-etudes-canada-maroc/', '0.8', '2026-10-26'), ('/entree-express-francophone-maroc/', '0.8', '2026-10-26'),
        ('/documents-maroc-immigration-canada/', '0.8', '2026-10-26'),
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
if '/actualites/' not in ll:
    ll = ll.replace('\n## Liens', f"- [Actualités de l'immigration (français)]({SITE}/actualites/): nouvelles expliquées, avec sources\n\n## Liens", 1)
    open(R + 'llms.txt', 'w', encoding='utf-8').write(ll)
print('ok', len(items), 'actualités')
