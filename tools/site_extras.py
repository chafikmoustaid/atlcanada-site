#!/usr/bin/env python3
"""Ajouts transversaux (idempotent) : lien Confidentialité en pied de page, consentement sur le formulaire,
bandeau « dernier tirage » automatique à l'accueil, messages WhatsApp préremplis."""
import re, glob, os, json, html
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
e = html.escape
files = [f for f in glob.glob(R + '**/*.html', recursive=True) if '/social/' not in f]
WA_FR = 'Bonjour ATL Canada, j\'aimerais avoir des informations sur mon projet d\'immigration au Canada.'
WA_AR = 'مرحبا ATL Canada، أرغب في الحصول على معلومات حول مشروع الهجرة إلى كندا.'
from urllib.parse import quote
items = sorted(json.load(open(R + 'data/actualites.json', encoding='utf-8')), key=lambda x: x['date'], reverse=True)
draws = [i for i in items if i['tag_fr'] == 'Entrée express' and 'tirage' in i['id']][:3]
n = 0
for f in files:
    t = o = open(f, encoding='utf-8').read()
    ar = 'lang="ar"' in t[:200]
    rel = f[len(R):]
    # 0. statistiques Vercel Web Analytics (sans témoin, anonymes)
    if '/_vercel/insights/script.js' not in t and '</body>' in t:
        t = t.replace('</body>', '<script>window.va=window.va||function(){(window.vaq=window.vaq||[]).push(arguments)}</script>\n<script defer src="/_vercel/insights/script.js"></script>\n</body>', 1)
    # 1. lien Confidentialité
    if '/confidentialite/' not in t and rel != 'confidentialite/index.html':
        lab = 'سياسة الخصوصية' if ar else 'Confidentialité'
        href = '/confidentialite/'
        if '<footer' in t:
            if '<li><a href="/actualites/">Actualités</a></li>' in t:
                t = t.replace('<li><a href="/actualites/">Actualités</a></li>', f'<li><a href="/actualites/">Actualités</a></li>\n          <li><a href="{href}">{lab}</a></li>', 1)
            else:
                t = re.sub(r'(<div class="footer-bottom">)', lambda m: m.group(1) + f'<a href="{href}" style="color:inherit">{lab}</a> ', t, count=1) if 'footer-bottom' in t else t
    elif rel == 'confidentialite/index.html' and '<footer' in t and 'href="/confidentialite/"' not in t.split('<footer')[1]:
        pass
    # 2. consentement formulaire
    if 'name="_honey"' in t and 'class="consent"' not in t:
        txt = ('قرأت <a href="/confidentialite/" target="_blank">سياسة الخصوصية</a> وأوافق على استخدام معلوماتي للرد على طلبي.' if ar else
               'J\'ai lu la <a href="/confidentialite/" target="_blank">politique de confidentialité</a> et j\'accepte que mes renseignements servent à répondre à ma demande.')
        box = f'<label class="consent"><input type="checkbox" name="consentement" value="oui" required><span>{txt}</span></label>\n        '
        t = t.replace('<button class="btn btn-solid" type="submit"', box + '<button class="btn btn-solid" type="submit"', 1)
    # 3. bandeau « dernier tirage » défilant, sous l'en-tête de l'accueil
    if rel == 'index.html' and draws:
        def item(it):
            d = it['date'].split('-')
            mois = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.'][int(d[1]) - 1]
            return (f'<a class="ls-item" href="/actualites/#{it["id"]}">{e(it["title_fr"])}'
                    f'<span class="ls-date">{int(d[2])} {mois} {d[0]}</span></a>')
        once = ''.join(item(it) for it in draws)
        strip = ('<!-- LIVE:START -->\n  <section class="live-strip" aria-label="Derniers tirages Entrée express"><div class="ls-inner">'
                 '<span class="ls-tag"><span class="live-dot" aria-hidden="true"></span>Dernier tirage</span>'
                 f'<div class="ls-track"><div class="ls-move">{once}<span class="ls-dup" aria-hidden="true">{once.replace("<a ", "<a tabindex=\"-1\" ")}</span></div></div>'
                 '</div></section>\n  <!-- LIVE:END -->\n')
        t = re.sub(r'\s*<!-- LIVE:START.*?<!-- LIVE:END -->\n', '\n', t, flags=re.S)
        t = t.replace('  <section class="hero">', strip + '\n  <section class="hero">', 1)
    # 4. WhatsApp préremplis
    msg = quote(WA_AR if ar else WA_FR, safe='')
    t = t.replace('https://wa.me/15142956635"', f'https://wa.me/15142956635?text={msg}"')
    if t != o:
        open(f, 'w', encoding='utf-8').write(t); n += 1
print('modifié :', n, 'fichiers')
