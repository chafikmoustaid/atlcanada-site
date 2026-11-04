import os, subprocess, html
D = os.path.dirname(os.path.abspath(__file__))
A = os.path.abspath(os.path.join(D, "..", "..", "assets"))

def b(t):  # latin/numbers inside Arabic
    return f"<bdi>{t}</bdi>"

CSS = f"""
@font-face{{font-family:Cairo;font-weight:600;src:url(cairo-arabic-600-normal.woff2)}}
@font-face{{font-family:Cairo;font-weight:700;src:url(cairo-arabic-700-normal.woff2)}}
@font-face{{font-family:SS;font-weight:400;src:url(source-sans-3-latin-400-normal.woff2)}}
@font-face{{font-family:SS;font-weight:600;src:url(source-sans-3-latin-600-normal.woff2)}}
*{{box-sizing:border-box;margin:0}}
body{{width:1080px;height:1920px;background:#F1EBDE;font-family:SS,sans-serif;color:#16233D;position:relative;overflow:hidden}}
.top{{position:absolute;left:0;right:0;top:0;height:14px;background:#E1232B}}
.logo{{position:absolute;top:60px;left:64px;height:96px}}
.num{{position:absolute;top:70px;right:64px;font-weight:600;font-size:34px;color:#E1232B}}
.main{{position:absolute;left:64px;right:64px;top:210px;bottom:300px;display:flex;flex-direction:column;justify-content:center;gap:34px}}
.fr{{font-family:Lora,serif;font-weight:700;font-size:70px;line-height:1.15}}
.fr.s{{font-size:46px;font-weight:600}}
.ar{{font-family:Cairo,sans-serif;font-weight:700;direction:rtl;text-align:right;font-size:62px;line-height:1.5;color:#E1232B}}
.ar.s{{font-size:42px;font-weight:600;color:#16233D}}
.txt{{font-size:42px;line-height:1.35;font-weight:400}}
.card{{background:#fff;border-left:12px solid #E1232B;border-radius:18px;padding:30px 34px;display:flex;flex-direction:column;gap:12px;box-shadow:0 6px 18px rgba(22,35,61,.08)}}
.big{{font-family:Lora,serif;font-weight:700;font-size:120px;color:#E1232B;line-height:1}}
.src{{font-size:28px;color:#16233D;opacity:.8}}
.badge{{align-self:flex-start;background:#16233D;color:#F1EBDE;font-weight:600;font-size:34px;padding:10px 26px;border-radius:40px}}
.foot{{position:absolute;left:0;right:0;bottom:0;height:260px;background:#16233D;color:#F1EBDE;padding:30px 64px;display:flex;align-items:center;gap:30px}}
.foot img{{height:150px;background:#fff;border-radius:75px;padding:6px}}
.foot .t{{display:flex;flex-direction:column;gap:6px}}
.foot .a{{font-size:30px;line-height:1.3}}
.foot .a2{{font-family:Cairo;font-weight:600;font-size:28px;direction:rtl;text-align:left}}
.foot .p{{font-size:38px;font-weight:600}}
.foot .w{{font-size:30px;opacity:.9}}
ul{{list-style:none;display:flex;flex-direction:column;gap:22px}}
li{{display:flex;flex-direction:column;gap:6px}}
"""

FOOT = f"""
<div class="foot"><img src="file://{A}/ccic-logo.png">
<div class="t"><div class="a">Consultant réglementé CCIC R712906</div>
<div class="a2">مستشار معتمد · {b('CCIC R712906')}</div>
<div class="p">Tél. et WhatsApp : +1 514 295 6635</div><div class="w">atlcanada.com</div></div></div>"""

def page(body, n):
    h = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="top"></div><img class="logo" src="file://{A}/logo-b.svg"><div class="num">{n}/6</div>
<div class="main">{body}</div>{FOOT}</body></html>"""
    open(os.path.join(D, f"s{n}.html"), "w", encoding="utf-8").write(h)

page(f"""<div class="badge">Actualité IRCC · 28 octobre 2026 · {b('IRCC')}</div>
<div class="fr">Faux consultants : les sanctions sont désormais en vigueur</div>
<div class="ar">المستشارون غير المرخّصين: العقوبات أصبحت سارية</div>
<div class="src">Source : canada.ca (IRCC), communiqué du 28 octobre 2026</div>""", 1)

page(f"""<div class="fr s">Depuis le 28 octobre 2026, IRCC peut sanctionner financièrement les représentants en immigration non autorisés ou frauduleux.</div>
<div class="ar s">منذ 28 أكتوبر 2026، يمكن لوزارة الهجرة الكندية ({b('IRCC')}) فرض غرامات مالية على الممثلين غير المرخّصين أو المحتالين.</div>
<div class="card"><div class="txt">Règlement final : publication à la Gazette du Canada prévue le 4 novembre 2026.</div>
<div class="ar s" style="font-size:36px">النشر النهائي للّائحة في الجريدة الرسمية الكندية مقرّر في 4 نونبر 2026.</div></div>
<div class="src">Source : canada.ca (IRCC)</div>""", 2)

page(f"""<div class="card"><div class="big">5 000 $</div><div class="txt">Conseils ou représentation payés sans autorisation</div>
<div class="ar s" style="font-size:38px">تقديم استشارة أو تمثيل مقابل أجر دون ترخيص</div></div>
<div class="card"><div class="big">15 000 $</div><div class="txt">Information fausse ou trompeuse fournie sciemment</div>
<div class="ar s" style="font-size:38px">تقديم معلومات كاذبة أو مضلّلة عن قصد</div></div>
<div class="card"><div class="big" style="font-size:84px">1,5 M$</div><div class="txt">Plafond pour l’ensemble des violations ; montants plus élevés en cas de récidive</div>
<div class="ar s" style="font-size:38px">السقف الإجمالي {b('1,5')} مليون دولار، والمبالغ ترتفع عند التكرار</div></div>
<div class="src">Montants en dollars canadiens · Source : canada.ca (IRCC)</div>""", 3)

page(f"""<div class="fr">Avant de payer, vérifiez</div>
<div class="ar">قبل أن تدفع، تحقّق</div>
<ul>
<li><div class="txt">✔ Votre représentant est-il autorisé : consultant réglementé, avocat ?</div><div class="ar s" style="font-size:36px">هل الممثل مرخّص: مستشار معتمد أو محامٍ؟</div></li>
<li><div class="txt">✔ Consultez le registre officiel du Collège : college-ic.ca</div><div class="ar s" style="font-size:36px">راجع السجل الرسمي للكلية: {b('college-ic.ca')}</div></li>
<li><div class="txt">✔ Lisez et vérifiez vous-même chaque information de votre demande.</div><div class="ar s" style="font-size:36px">اقرأ كل معلومة في ملفك وتأكّد منها بنفسك.</div></li></ul>
<div class="src">Source : canada.ca (IRCC) · college-ic.ca</div>""", 4)

page(f"""<div class="fr">Signaux d’alerte</div>
<div class="ar">علامات تستدعي الحذر</div>
<ul>
<li><div class="txt">✖ On vous promet un visa ou un résultat garanti</div><div class="ar s" style="font-size:36px">وعد بتأشيرة أو نتيجة مضمونة</div></li>
<li><div class="txt">✖ Paiement sans contrat écrit ni reçu</div><div class="ar s" style="font-size:36px">دفع دون عقد مكتوب أو وصل</div></li>
<li><div class="txt">✖ On vous demande d’« arranger » des documents ou des informations</div><div class="ar s" style="font-size:36px">طلب «تعديل» وثائق أو معلومات</div></li>
<li><div class="txt">✖ Impossible de vérifier son inscription</div><div class="ar s" style="font-size:36px">تعذّر التحقق من تسجيله</div></li></ul>
<div class="src">Conseils de prudence générale · Aucun résultat n’est garanti</div>""", 5)

page(f"""<div class="fr">Un doute ? Posez la question avant de signer.</div>
<div class="ar">عندك شك؟ اسأل قبل أن توقّع.</div>
<div class="card"><div class="txt">Un représentant douteux peut être signalé à IRCC (page « Déposer une plainte contre un représentant »).</div>
<div class="ar s" style="font-size:36px">يمكن التبليغ عن ممثل مشبوه لدى {b('IRCC')}.</div></div>
<div class="card"><div class="txt">ATL Canada : consultation à Montréal et à Casablanca.</div>
<div class="ar s" style="font-size:36px">استشارة في مونتريال والدار البيضاء.</div></div>
<div class="src">Sources : canada.ca (IRCC) · college-ic.ca</div>""", 6)

subprocess.run(["python3", os.path.join(D, "render.py")], check=True)
