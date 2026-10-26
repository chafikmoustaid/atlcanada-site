#!/usr/bin/env python3
"""Bandeau de contact sombre à la place de la ligne icône + numéro des sections « bureaux » (idempotent).
À lancer après build_pages*.py et contact_icons.py."""
import re, glob, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
PH = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>'
WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>'
n = 0
for f in glob.glob(R + '**/index.html', recursive=True):
    t = open(f, encoding='utf-8').read()
    m = re.search(r'<p class="office-phone"[^>]*>.*?</span></p><p style="margin:14px 0 0">(.*?)</p>', t, re.S)
    if not m: continue
    hours = m.group(1)
    ar = '/ar/' in f.replace(R, '/')
    q, c, w = ('هل لديك سؤال حول ملفك؟', 'اتصل بنا', 'واتساب') if ar else ('Une question sur votre dossier ?', 'Appeler', 'WhatsApp')
    band = (f'<div class="contact-band"><div><span class="cb-q">{q}</span>'
            f'<a class="cb-num" href="tel:+15142956635"><bdi dir="ltr">+1 514 295 6635</bdi></a>'
            f'<div class="cb-h">{hours}</div></div>'
            f'<div class="cb-b"><a class="cb-btn cb-tel" href="tel:+15142956635">{PH}{c}</a>'
            f'<a class="cb-btn cb-wa" href="https://wa.me/15142956635" target="_blank" rel="noopener">{WA}{w}</a></div></div>')
    t = t[:m.start()] + band + t[m.end():]
    open(f, 'w', encoding='utf-8').write(t); n += 1
print('modifié :', n, 'fichiers')
