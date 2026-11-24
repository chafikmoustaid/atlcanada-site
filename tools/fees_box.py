#!/usr/bin/env python3
"""Encadré « Combien ça coûte ? » (honoraires + frais du gouvernement) sur les pages de service (idempotent)."""
import os, re
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') + '/'
# page FR : (page AR, libellé honoraires FR/AR, honoraires, frais gouvernement FR/AR)
D = {
 'permis-etudes-canada-maroc/': ('ar/study-permit-morocco/', 'Permis d\'études', 'تصريح الدراسة', '900', '150', True),
 'permis-de-travail-canada/': ('ar/work-permit/', 'Prolongation ou permis postdiplôme', 'التمديد أو تصريح ما بعد التخرج', '650', '155', True),
 'visa-visiteur-super-visa-canada/': ('ar/visitor-visa-super-visa/', 'Visa de visiteur', 'تأشيرة الزيارة', '450', '100', True),
 'entree-express-canada/': ('ar/express-entry/', 'Profil et demande de résidence permanente', 'الملف وطلب الإقامة الدائمة', '2 150', '1 590', True),
 'entree-express-francophone-maroc/': ('ar/express-entry-french/', 'Profil et demande de résidence permanente', 'الملف وطلب الإقامة الدائمة', '2 150', '1 590', True),
 'candidats-provinces-canada/': ('ar/provincial-nominee/', 'Candidats des provinces', 'برامج المقاطعات', '3 000', '1 590', True),
 'residence-permanente-canada/': ('ar/permanent-residence/', 'Demande de résidence permanente', 'طلب الإقامة الدائمة', '2 150', '1 590', True),
 'parrainage-familial-canada/': ('ar/family-sponsorship/', 'Parrainage d\'un époux ou conjoint', 'كفالة الزوج أو الزوجة', '2 200', '1 260', True),
 'citoyennete-canadienne/': ('ar/canadian-citizenship/', 'Citoyenneté canadienne', 'الجنسية الكندية', '500', '653', False),
}
def box(ar, lab, hon, gov, bio):
    if not ar:
        return (f'<section class="sp"><div class="wrap"><div class="fee-box"><h2>Combien ça coûte ?</h2><div class="fee-grid">'
          f'<a class="fee-card" href="/honoraires/"><span class="fee-k">Nos honoraires</span><span class="fee-v"><small>à partir de</small> {hon} $</span><span class="fee-s">{lab} · devis final après la consultation</span></a>'
          f'<a class="fee-card" href="/frais-officiels-immigration-canada/"><span class="fee-k">Frais du gouvernement</span><span class="fee-v">{gov} $</span><span class="fee-s">payés directement à IRCC{" · biométrie 85 $ en plus" if bio else ""}</span></a>'
          f'</div><p class="fee-note">Les deux sont distincts : les frais du gouvernement ne sont pas inclus dans nos honoraires. <a href="/honoraires/">Voir les honoraires</a> · <a href="/frais-officiels-immigration-canada/">Voir les frais officiels</a></p></div></div></section>\n')
    return (f'<section class="sp"><div class="wrap"><div class="fee-box"><h2>كم التكلفة؟</h2><div class="fee-grid">'
      f'<a class="fee-card" href="/ar/fees/"><span class="fee-k">أتعابنا</span><span class="fee-v"><small>ابتداءً من</small> <bdi dir="ltr">{hon} $</bdi></span><span class="fee-s">{lab} · السعر النهائي بعد الاستشارة</span></a>'
      f'<a class="fee-card" href="/ar/official-fees/"><span class="fee-k">رسوم الحكومة</span><span class="fee-v"><bdi dir="ltr">{gov} $</bdi></span><span class="fee-s">تُدفع مباشرة إلى IRCC{" · البيومترية 85$ إضافية" if bio else ""}</span></a>'
      f'</div><p class="fee-note">الاثنان منفصلان: رسوم الحكومة غير مشمولة في أتعابنا. <a href="/ar/fees/">الأتعاب</a> · <a href="/ar/official-fees/">الرسوم الرسمية</a></p></div></div></section>\n')
n = 0
for fr, (arp, labfr, labar, hon, gov, bio) in D.items():
    for path, ar, lab in ((fr, False, labfr), (arp, True, labar)):
        f = R + path + 'index.html'
        if not os.path.exists(f): continue
        t = open(f, encoding='utf-8').read()
        if 'class="fee-box"' in t: continue
        m = re.search(r'<section class="sp alt" id="faq">', t)
        if not m: continue
        t = t[:m.start()] + box(ar, lab, hon, gov, bio) + t[m.start():]
        open(f, 'w', encoding='utf-8').write(t); n += 1
print('fees_box : modifié', n, 'fichiers')
