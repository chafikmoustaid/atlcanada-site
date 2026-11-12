#!/usr/bin/env python3
"""Relie le permis R712906 au profil public du Collège des consultants (CICC/CCIC).
Idempotent : ne touche que le texte visible (jamais les balises, scripts ni le JSON-LD)."""
import glob, os, re

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') + '/'
URL = 'https://registre.college-ic.ca/Public-Register-FR/Licensee/Profile.aspx?ID=10629'
A = f'<a class="ccic-link" href="{URL}" target="_blank" rel="noopener">'
PHRASES = ['registre public du CCIC', 'السجل العمومي للهيئة']
TOKEN = re.compile(r'(<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)', re.S)

def process(html):
    html = html.replace(
        '<span class="ccic-badge">Membre du CCIC · Permis <span class="ccic-num">R712906</span></span>',
        f'<a class="ccic-badge" href="{URL}" target="_blank" rel="noopener" title="Vérifier le permis dans le registre public du CCIC">Membre du CCIC · Permis <span class="ccic-num">R712906</span></a>')
    out, depth = [], 0
    for tok in TOKEN.split(html):
        if tok.startswith('<'):
            low = tok.lower()
            if re.match(r'<a[\s>]', low): depth += 1
            elif low.startswith('</a'): depth = max(0, depth - 1)
            out.append(tok); continue
        if depth or not tok.strip():
            out.append(tok); continue
        if any(p in tok for p in PHRASES):
            for p in PHRASES:
                tok = tok.replace(p, f'{A}{p}</a>')
        elif 'R712906' in tok:
            tok = tok.replace('R712906', f'{A}R712906</a>')
        out.append(tok)
    html = ''.join(out)
    # JSON-LD : profil public du Collège parmi les références de l'organisation
    if URL not in html.split('</head>')[0]:
        html = html.replace('"https://www.instagram.com/atl_immigration_canada/"]',
                            '"https://www.instagram.com/atl_immigration_canada/", "' + URL + '"]', 1)
    return html

n = 0
for f in glob.glob(R + '**/*.html', recursive=True):
    s = open(f, encoding='utf-8').read()
    t = process(s)
    if t != s:
        open(f, 'w', encoding='utf-8').write(t); n += 1
print('ccic_link : modifié', n, 'fichiers')
