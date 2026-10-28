#!/usr/bin/env python3
"""Icônes de contact modernes (idempotent). À lancer APRÈS build_pages*.py puis contact_icons.py.
Ajoute assets/icons.css, les boutons flottants et les pastilles Facebook / Instagram."""
import re, glob, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
src = open(R + 'index.html', encoding='utf-8').read()
tb = re.search(r'<span class="tb-phone"><a href="tel:[^"]*" aria-label="[^"]*">(<svg.*?</svg>).*?<a class="tb-wa"[^>]*>(<svg.*?</svg>)</a>', src, re.S)
if tb is None:  # barre du haut supprimée : reprendre les icônes des boutons flottants
    class _T:
        def __init__(s, a, b): s.g = (None, a, b)
        def group(s, n): return s.g[n]
    _f = re.search(r'class="fab-tel"[^>]*>(<svg.*?</svg>)</a><a class="fab-wa"[^>]*>(<svg.*?</svg>)</a>', src, re.S)
    tb = _T(_f.group(1), _f.group(2))
PH = re.sub(r'<svg [^>]*>', '<svg viewBox="0 0 24 24" aria-hidden="true">', tb.group(1), 1)
WA = re.sub(r'<svg [^>]*>', '<svg viewBox="0 0 24 24" aria-hidden="true">', tb.group(2), 1)
FB = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.4 1.5-1.4h1.6V4.5c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21h3.1z"/></svg>'
IG = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1"/></svg>'
LINK = '<link rel="stylesheet" href="/assets/icons.css">'
n = 0
for f in glob.glob(R + '**/*.html', recursive=True):
    if '/.git/' in f or f.endswith('googled5add6c8d8050298.html'): continue
    t = open(f, encoding='utf-8').read(); o = t
    ar = '/ar/' in f.replace(R, '/')
    if LINK not in t:
        t = t.replace('</head>', LINK + '\n</head>', 1)
    if 'class="fab-contact"' not in t:
        lt, lw = ('اتصل بنا', 'واتساب') if ar else ('Appeler', 'WhatsApp')
        fab = (f'<div class="fab-contact"><a class="fab-tel" href="tel:+15142956635" aria-label="{lt}" title="{lt}">{PH}</a>'
               f'<a class="fab-wa" href="https://wa.me/15142956635" target="_blank" rel="noopener" aria-label="{lw}" title="{lw}">{WA}</a></div>\n')
        t = t.replace('</body>', fab + '</body>', 1)
    # pied de page : glyphe Facebook plein
    t = re.sub(r'(<a class="social-btn" href="https://www\.facebook\.com/atlcanada"[^>]*>)\s*<svg.*?</svg>\s*(</a>)', lambda m: m.group(1) + FB + m.group(2), t, flags=re.S)
    # section contact : pastilles
    t = t.replace('<p><a href="https://www.facebook.com/atlcanada" target="_blank" rel="noopener">Facebook</a> · <a href="https://www.instagram.com/atl_immigration_canada/" target="_blank" rel="noopener">Instagram</a></p>',
        f'<p class="social-pills"><a class="sp-btn sp-fb" href="https://www.facebook.com/atlcanada" target="_blank" rel="noopener">{FB}Facebook</a><a class="sp-btn sp-ig" href="https://www.instagram.com/atl_immigration_canada/" target="_blank" rel="noopener">{IG}Instagram</a></p>')
    # barre du haut : petits logos Facebook / Instagram à droite
    if 'class="tb-social"' not in t and 'class="topbar-right"' in t:
        lf, li = ('فيسبوك', 'إنستغرام') if ar else ('Facebook', 'Instagram')
        soc = (f'<span class="tb-social"><a class="tb-fb" href="https://www.facebook.com/atlcanada" target="_blank" rel="noopener" aria-label="{lf}" title="{lf}">{FB}</a>'
               f'<a class="tb-ig" href="https://www.instagram.com/atl_immigration_canada/" target="_blank" rel="noopener" aria-label="{li}" title="{li}">{IG}</a></span>')
        t = re.sub(r'(<div class="topbar-right"[^>]*>.*?)(\s*</div>)', lambda m: m.group(1) + soc + m.group(2), t, count=1, flags=re.S)
    if t != o:
        open(f, 'w', encoding='utf-8').write(t); n += 1
print('modifié :', n, 'fichiers')
