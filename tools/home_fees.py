#!/usr/bin/env python3
"""Bloc « Honoraires transparents » sur les pages d'accueil FR et AR (idempotent)."""
import os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') + '/'
FR = '''<section class="hf-sec"><div class="hf-wrap"><p class="hf-eyebrow">Transparence</p><h2>Des honoraires clairs, annoncés à l'avance</h2><p class="hf-lede">Un prix de départ par service, un devis final après la consultation, et une entente écrite avant tout paiement. Les frais du gouvernement sont distincts.</p>
<div class="fee-grid hf-grid"><a class="fee-card" href="/permis-etudes-canada-maroc/"><span class="fee-k">Permis d'études</span><span class="fee-v"><small>à partir de</small> 900 $</span><span class="fee-s">frais du gouvernement : 150 $</span></a><a class="fee-card" href="/visa-visiteur-super-visa-canada/"><span class="fee-k">Visa de visiteur</span><span class="fee-v"><small>à partir de</small> 450 $</span><span class="fee-s">frais du gouvernement : 100 $</span></a><a class="fee-card" href="/entree-express-canada/"><span class="fee-k">Entrée express</span><span class="fee-v"><small>à partir de</small> 2 150 $</span><span class="fee-s">frais du gouvernement : 1 590 $</span></a></div>
<p class="hf-links"><a class="btn btn-solid" href="/honoraires/">Voir tous les honoraires</a> <a class="btn" href="/frais-officiels-immigration-canada/">Frais officiels</a> <a class="btn" href="/budget-immigration-canada/">Calculer mon budget</a></p></div></section>
'''
AR = '''<section class="hf-sec"><div class="hf-wrap"><p class="hf-eyebrow">شفافية</p><h2>أتعاب واضحة تُعلن مسبقًا</h2><p class="hf-lede">سعر ابتدائي لكل خدمة، وسعر نهائي بعد الاستشارة، وعقد مكتوب قبل أي دفع. ورسوم الحكومة منفصلة.</p>
<div class="fee-grid hf-grid"><a class="fee-card" href="/ar/study-permit-morocco/"><span class="fee-k">تصريح الدراسة</span><span class="fee-v"><small>ابتداءً من</small> <bdi dir="ltr">900 $</bdi></span><span class="fee-s">رسوم الحكومة: <bdi dir="ltr">150 $</bdi></span></a><a class="fee-card" href="/ar/visitor-visa-super-visa/"><span class="fee-k">تأشيرة الزيارة</span><span class="fee-v"><small>ابتداءً من</small> <bdi dir="ltr">450 $</bdi></span><span class="fee-s">رسوم الحكومة: <bdi dir="ltr">100 $</bdi></span></a><a class="fee-card" href="/ar/express-entry/"><span class="fee-k">الدخول السريع</span><span class="fee-v"><small>ابتداءً من</small> <bdi dir="ltr">2 150 $</bdi></span><span class="fee-s">رسوم الحكومة: <bdi dir="ltr">1 590 $</bdi></span></a></div>
<p class="hf-links"><a class="btn btn-solid" href="/ar/fees/">كل الأتعاب</a> <a class="btn" href="/ar/official-fees/">الرسوم الرسمية</a> <a class="btn" href="/ar/budget-calculator/">احسب ميزانيتي</a></p></div></section>
'''
n = 0
for f, blk, anchor in (('index.html', FR, '  <section class="why" id="pourquoi">'), ('ar/index.html', AR, '<section class="sp alt" id="faq">')):
    p = R + f
    t = open(p, encoding='utf-8').read()
    if 'class="hf-sec"' in t or anchor not in t: continue
    t = t.replace(anchor, blk + anchor, 1)
    open(p, 'w', encoding='utf-8').write(t); n += 1
print('home_fees : modifié', n, 'fichiers')
