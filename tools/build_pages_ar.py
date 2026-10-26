#!/usr/bin/env python3
"""Génère les versions arabes des pages de service (candidats du Maroc).
Reprend l'en-tête, la barre du haut, les bureaux et le pied de page de /ar/index.html.
Usage : python3 tools/build_pages_ar.py   (depuis la racine du dépôt)"""
import json, re, html, os

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
SITE = 'https://www.atlcanada.com'
e = html.escape
UPDATED = '2026-10-26'

ref = open(R + 'ar/index.html', encoding='utf-8').read()
head_ref = ref[:ref.index('</head>')]
topbar = ref[ref.index('<body>'):ref.index('<main>')]
footer = ref[ref.index('</main>'):]
offices = re.search(r'<section class="sp" id="bureaux">.*?</section>', ref, re.S).group(0)

EXTRA_CSS = """<style>
.tbl-wrap{overflow-x:auto;margin:0 0 8px}
.tbl{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line)}
.tbl th,.tbl td{padding:14px 16px;text-align:start;vertical-align:top;border-bottom:1px solid var(--line);font-size:1rem}
.tbl th{background:var(--paper-dim);color:var(--ink);font-weight:600}
.tbl td{color:var(--ink-soft)}
.tbl a{color:var(--ink);text-decoration:underline}
.steps{max-width:none}.steps{max-width:none}.prose{max-width:72ch}.prose p{margin:0 0 14px;color:var(--ink-soft)}
.sources{margin:0;padding-inline-start:20px;color:var(--ink-soft)}.sources li{margin:0 0 8px}
.sources a{color:var(--ink);text-decoration:underline}
.related{display:flex;gap:14px;flex-wrap:wrap;margin:22px 0 0}
</style>
"""

LAW = "المعلومات الواردة في هذه الصفحة عامة، ولا تغني عن تقييم شخصي لملفك. قوانين الهجرة تتغير كثيرًا، فاعتمد دائمًا على المصادر الرسمية (canada.ca). لا نضمن أي نتيجة."


def table(headers, rows):
    th = ''.join(f'<th scope="col">{e(h)}</th>' for h in headers)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="tbl-wrap"><table class="tbl"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def a(url, label):
    return f'<a href="{e(url, quote=True)}" rel="noopener" target="_blank">{e(label)}</a>'


def faq_html(items):
    return ''.join(f'<details class="faq-item"{" open" if i == 0 else ""}><summary>{e(q)}</summary><p>{ans}</p></details>'
                   for i, (q, ans) in enumerate(items))


def strip(s):
    return re.sub(r'<[^>]+>', '', html.unescape(s))


TRUST = ('<section class="sp"><div class="wrap"><div class="trustbox"><h2>مستشار هجرة مرخَّص، وليس وسيطًا</h2>'
         '<p>يديره مستشار هجرة كندي مرخَّص (CRIC)، عضو في الهيئة الكندية لمستشاري الهجرة والمواطنة (CICC/CCIC)، ترخيص رقم R712906. ويمكن التحقق من الترخيص في السجل العمومي للهيئة.</p></div></div></section>')

PAGES = []

# ------------------------------------------------------------------ 1. تصريح الدراسة
PAGES.append(dict(
    path='ar/study-permit-morocco/', fr='permis-etudes-canada-maroc/',
    title="تصريح الدراسة في كندا من المغرب | ATL Canada",
    desc="الدراسة في كندا انطلاقًا من المغرب: رسالة التصديق، إثبات الموارد المالية، البيانات البيومترية وإيداع الطلب. مستشار مرخَّص يرافقك. احجز موعدًا.",
    crumb="تصريح الدراسة",
    eyebrow="الدراسة · الدار البيضاء · مونتريال",
    h1="تصريح الدراسة في كندا انطلاقًا من المغرب",
    lede="على المواطنين المغاربة الحصول على تصريح دراسة قبل السفر. إليك المراحل، والوثائق التي ينبغي إعدادها، والنقاط التي يتحدد فيها مصير الملف، مع مستشار هجرة مرخَّص في الدار البيضاء.",
    body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>المراحل، من القبول إلى السفر</h2>
<ol class="steps">
<li><span>اختيار برنامج دراسي في مؤسسة تعليمية معتمدة (DLI): فلا يُمنح تصريح الدراسة إلا للدراسة في مؤسسة من هذا النوع.</span></li>
<li><span>الحصول على رسالة القبول، وعند اشتراطها، رسالة التصديق من المقاطعة أو الإقليم (PAL/TAL).</span></li>
<li><span>جمع ما يثبت الموارد المالية: مصاريف الدراسة للسنة الأولى، ومصاريف المعيشة، وتكاليف السفر.</span></li>
<li><span>إيداع الطلب عبر الإنترنت لدى IRCC، ثم تقديم البيانات البيومترية (البصمات والصورة) في مركز VFS Global بالمغرب.</span></li>
<li><span>الرد على طلبات IRCC إلى حين صدور القرار، ثم التحضير للوصول إلى كندا.</span></li>
</ol></div></section>
<section class="sp"><div class="wrap"><h2>النقاط التي تستحق عناية خاصة</h2>
{table(['العنصر', 'ما ينبغي معرفته', 'المصدر الرسمي'], [
 ['رسالة التصديق (PAL/TAL)', "تُشترط في معظم الطلبات الجديدة، مع استثناءات تحددها IRCC. ومن بينها في 2026 طلبة الماستر والدكتوراه في مؤسسة عمومية معتمدة.", a('https://www.canada.ca/fr/immigration-refugies-citoyennete/organisation/publications-guides/bulletins-guides-operationnels/mises-a-jour/2026-etudiants-lap-lat.html', 'IRCC، تحديث 6 فبراير 2026')],
 ['إثبات الموارد المالية', "عليك إثبات مصاريف الدراسة للسنة الأولى ومصاريف المعيشة وتكاليف السفر. وتحدّث IRCC المبالغ كل سنة، فاعتمد دائمًا جدولها الساري.", a('https://www.canada.ca/fr/immigration-refugies-citoyennete/organisation/publications-guides/bulletins-guides-operationnels/residents-temporaires/permis-etudes/evaluation-demande.html', 'IRCC، تقييم الطلب')],
 ['البيانات البيومترية', "تُقدَّم البصمات والصورة بموعد مسبق في مركز VFS Global بالمغرب، وتبقى صالحة 10 سنوات بالنسبة للمقيم المؤقت.", a('https://visa.vfsglobal.com/mar/fr/can/faq', 'VFS Global المغرب، الأسئلة الشائعة')],
 ['رسالة القبول', "يجب أن تصدر عن مؤسسة تعليمية معتمدة، وأن تطابق البرنامج المذكور في طلبك.", 'المؤسسة المختارة'],
])}
<p class="note" style="margin-top:18px">للدراسة في كيبيك تُضاف خطوة إقليمية (شهادة قبول كيبيك، CAQ)، نشرحها معك خلال الاستشارة إذا كان مشروعك يمر عبرها.</p>
</div></section>
<section class="sp alt"><div class="wrap"><h2>بعد الدراسة</h2><div class="prose">
<p>بحسب البرنامج والمؤسسة، قد يكون ممكنًا الحصول على تصريح عمل بعد التخرج. وقد تُحتسب هذه التجربة المهنية في كندا لاحقًا ضمن طلب الإقامة الدائمة، مثلًا عبر الدخول السريع.</p>
<p>وإذا كنت تتقن الفرنسية، فاقرأ أيضًا صفحتنا حول <a href="/ar/express-entry-french/" style="text-decoration:underline">الدخول السريع للناطقين بالفرنسية</a>.</p></div></div></section>''',
    faq=[
        ("هل يحتاج المواطن المغربي إلى تصريح دراسة؟", "عمومًا نعم، متى زادت مدة البرنامج عن ستة أشهر. أما التكوينات الأقصر فقواعدها مختلفة، ونتحقق من حالتك معك."),
        ("ما هي الوثائق المطلوبة؟", "تحدد IRCC اللائحة الدقيقة حسب وضعك. وتشمل عادةً جواز السفر ورسالة القبول وإثبات الموارد المالية، ورسالة PAL/TAL عند اشتراطها. نراجعها معك قبل الإيداع."),
        ("كم تستغرق معالجة الطلب؟", "تتغير الآجال باستمرار وتنشرها IRCC على موقعها، ولا نَعِد بأي أجل. نطلعك على الوضع المحدَّث خلال موعدك."),
        ("هل يجب المرور عبر مستشار؟", "لا، يمكنك إيداع طلبك بنفسك. ويساعدك المستشار المرخَّص على اختيار الاستراتيجية المناسبة، وإعداد ملف كامل، وتفادي الإغفالات."),
        ("هل تضمنون الحصول على التصريح؟", "لا. لا يمكن لأي مستشار جاد أن يضمن قرارًا، فالقرار يعود حصريًا للسلطات الكندية."),
    ],
    sources=[
        ('https://www.canada.ca/fr/immigration-refugies-citoyennete/organisation/publications-guides/bulletins-guides-operationnels/mises-a-jour/2026-etudiants-lap-lat.html', "IRCC، تصريح الدراسة: رسائل التصديق من المقاطعات والأقاليم (تحديث 6 فبراير 2026، بالفرنسية)"),
        ('https://www.canada.ca/fr/immigration-refugies-citoyennete/organisation/publications-guides/bulletins-guides-operationnels/residents-temporaires/permis-etudes/evaluation-demande.html', "IRCC، تصريح الدراسة: تقييم الطلب (بالفرنسية)"),
        ('https://visa.vfsglobal.com/mar/fr/can/faq', "VFS Global المغرب، الأسئلة الشائعة (بالفرنسية)"),
    ],
    related=[('/ar/express-entry-french/', 'الدخول السريع للناطقين بالفرنسية'), ('/ar/moroccan-documents/', 'الوثائق المغربية')],
))

# ------------------------------------------------------------------ 2. الدخول السريع
PAGES.append(dict(
    path='ar/express-entry-french/', fr='entree-express-francophone-maroc/',
    title="الدخول السريع للناطقين بالفرنسية من المغرب | ATL Canada",
    desc="قد تمنحك الفرنسية حتى 50 نقطة إضافية في الدخول السريع. المستوى المطلوب والاختبارات والسحوبات: مستشار مرخَّص يشرح لك. احجز موعدًا.",
    crumb="الدخول السريع",
    eyebrow="الإقامة الدائمة · الدار البيضاء · مونتريال",
    h1="الدخول السريع: الفرنسية ميزة للمرشحين من المغرب",
    lede="قد يمنحك مستوى جيد في الفرنسية حتى 50 نقطة إضافية في نظام الدخول السريع (Express Entry)، ويفتح لك سحوبات مخصصة للناطقين بالفرنسية. إليك كيف يعمل ذلك وما ينبغي إعداده.",
    body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>كيف تُحتسب الفرنسية في نتيجتك</h2>
<div class="prose"><p>إذا حصلت على المستوى NCLC 7 على الأقل في المهارات الأربع بالفرنسية (فهم المسموع، فهم المقروء، التعبير الشفهي، التعبير الكتابي)، تحصل على نقاط إضافية حتى لو كانت الفرنسية لغتك الثانية.</p></div>
{table(['فرنسيتك', 'إنجليزيتك', 'النقاط الإضافية'], [
 ['NCLC 7 فأكثر في المهارات الأربع', 'CLB 4 أو أقل، أو دون اختبار في الإنجليزية', '+ 25 نقطة'],
 ['NCLC 7 فأكثر في المهارات الأربع', 'CLB 5 فأكثر في المهارات الأربع', '+ 50 نقطة'],
])}
<p class="note">المصدر: {a('https://www.canada.ca/fr/immigration-refugies-citoyennete/campagnes/immigration-francophone-hors-quebec/immigration-francophone-entree-express.html', 'IRCC، الدخول السريع للعمال المهرة الناطقين بالفرنسية (بالفرنسية)')}. تُضاف هذه النقاط إلى نتيجتك، لكنها لا تضمن أبدًا الحصول على دعوة.</p>
</div></section>
<section class="sp"><div class="wrap"><h2>البرامج الثلاثة للدخول السريع</h2><div class="cards">
<div class="card"><h3>العمال المهرة (فدرالي)</h3><p>للمرشحين الذين لديهم تجربة عمل مؤهلة في الخارج أو في كندا.</p></div>
<div class="card"><h3>المهن المتخصصة (فدرالي)</h3><p>للأشخاص المؤهلين في مهنة متخصصة معترف بها.</p></div>
<div class="card"><h3>التجربة الكندية</h3><p>لمن سبق له العمل في كندا، مثلًا بعد الدراسة.</p></div>
</div>
<div class="prose" style="margin-top:22px"><p>تدعو IRCC أيضًا مرشحين حسب الفئة، ومنها فئة مخصصة لإتقان الفرنسية. وتتغير العتبات في كل سحب، فتابعها في <a href="/actualites/" style="text-decoration:underline" lang="fr">صفحة الأخبار (بالفرنسية)</a>، مثل <a href="/actualites/#express-entree-tirage-francais-16-octobre-2026" style="text-decoration:underline" lang="fr">سحب الناطقين بالفرنسية بتاريخ 16 أكتوبر 2026</a>.</p></div></div></section>
<section class="sp alt"><div class="wrap"><h2>ما ينبغي إعداده</h2>
<ol class="steps">
<li><span>اجتياز اختبار في الفرنسية معتمد لدى IRCC (TEF Canada أو TCF Canada)، وإن أمكن اختبار في الإنجليزية، فاللغتان تؤثران في نقاطك.</span></li>
<li><span>تقييم شهاداتك الدراسية الأجنبية لدى جهة معتمدة، إن أردت احتسابها في نتيجتك.</span></li>
<li><span>إنشاء ملفك الشخصي عبر الإنترنت برمز الإحالة الشخصي. ولا تُرفع الوثائق إلا بعد تلقي دعوة.</span></li>
<li><span>بعد الدعوة، تتوفر على 60 يومًا لتقديم طلب الإقامة الدائمة.</span></li>
<li><span>تجهيز وثائقك المغربية، ومنها شهادة الشرطة: انظر صفحتنا حول <a href="/ar/moroccan-documents/" style="text-decoration:underline">الوثائق المغربية</a>.</span></li>
</ol>
<div class="prose" style="margin-top:22px"><p>كما أن الترشيح من أحد برامج المقاطعات يضيف نقاطًا. وإذا كانت نتيجتك ضعيفة، فقد يساعد تصريح عمل «التنقل الفرنكوفوني» بعض المرشحين على اكتساب تجربة عمل في كندا، وفق شروط IRCC.</p></div>
</div></section>''',
    faq=[
        ("ما مستوى الفرنسية المطلوب؟", "المستوى NCLC 7 في المهارات الأربع يمنحك النقاط الإضافية ويتيح لك الفئة المخصصة للناطقين بالفرنسية. ويلزم اختبار معتمد لدى IRCC (TEF Canada أو TCF Canada)."),
        ("ما النتيجة اللازمة للحصول على دعوة؟", "لا توجد عتبة ثابتة: فلكل سحب نتيجة دنيا خاصة به. تنشر IRCC النتائج الأخيرة ونلخصها في صفحة الأخبار."),
        ("هل يجب المرور عبر مستشار؟", "لا، يمكنك إنشاء ملفك وإيداع طلبك بنفسك. ويساعدك المستشار المرخَّص على التحقق من أهليتك، وتحسين نتيجتك بشكل نزيه، وإعداد ملف كامل ضمن أجل الستين يومًا."),
        ("هل تكفي الفرنسية للحصول على دعوة؟", "لا. يجب أيضًا استيفاء شروط أحد البرامج الثلاثة، والبقاء ضمن أعلى النتائج في المجموعة. والدعوة غير مضمونة أبدًا."),
        ("هل تضمنون دعوة أو إقامة دائمة؟", "لا. القرارات تعود حصريًا إلى IRCC. ودورنا اختيار الاستراتيجية المناسبة وإعداد ملف دقيق."),
    ],
    sources=[
        ('https://www.canada.ca/fr/immigration-refugies-citoyennete/campagnes/immigration-francophone-hors-quebec/immigration-francophone-entree-express.html', "IRCC، الدخول السريع للعمال المهرة الناطقين بالفرنسية (تحديث 20 غشت 2025، بالفرنسية)"),
        ('https://www.canada.ca/en/immigration-refugees-citizenship/corporate/mandate/policies-operational-instructions-agreements/ministerial-instructions/express-entry-rounds.html', "IRCC، جولات الدعوات في الدخول السريع (بالإنجليزية)"),
    ],
    related=[('/ar/study-permit-morocco/', 'تصريح الدراسة'), ('/ar/moroccan-documents/', 'الوثائق المغربية')],
))

# ------------------------------------------------------------------ 3. الوثائق المغربية
PAGES.append(dict(
    path='ar/moroccan-documents/', fr='documents-maroc-immigration-canada/',
    title="الوثائق المغربية للهجرة إلى كندا | ATL Canada",
    desc="شهادة الشرطة المغربية (البطاقة الأنتروبومترية)، البيانات البيومترية في VFS، وما لا تقبله IRCC: مستشار هجرة مرخَّص يرشدك.",
    crumb="الوثائق المغربية",
    eyebrow="الملف · الدار البيضاء · مونتريال",
    h1="الوثائق المغربية لطلب الهجرة إلى كندا",
    lede="شهادة الشرطة المغربية من أكثر الوثائق التي تثير حيرة المرشحين. إليك ما تطلبه IRCC من المواطنين المغاربة، استنادًا إلى صفحاتها الرسمية.",
    body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>شهادة الشرطة المغربية</h2>
<div class="prose"><p>تشترط طلبات الإقامة الدائمة شهادة شرطة. وبالنسبة للمواطنين المغاربة تسمى هذه الوثيقة <strong>«البطاقة الأنتروبومترية»</strong> (fiche anthropométrique). والبصمات المأخوذة لهذه الشهادة منفصلة عن البيانات البيومترية التي تقدمها مع طلبك.</p></div>
{table(['وضعيتك', 'ما تذكره IRCC'], [
 ['مواطن مغربي مقيم بالمغرب', "توجه إلى مقر الشرطة التابع لمحل إقامتك ومعك بطاقتك الوطنية للتعريف. ويمكنك تعيين من ينوب عنك، على أن يدلي ببطاقته الوطنية الخاصة."],
 ['مواطن مغربي مقيم بالخارج', "توجه إلى أقرب سفارة أو قنصلية للمغرب، أو قدّم الطلب عبر مقر الشرطة المحلي بالوكالة (وليس عبر المصلحة المركزية بالرباط). وتتطلب الوكالة وكالة موثَّقة، ونسخًا من عقد الازدياد وجواز السفر، إضافة إلى الرسوم."],
 ['لغة الوثيقة', "تصدر الشهادة بالفرنسية والعربية، ولا حاجة إلى ترجمتها."],
 ['ما لا ينبغي الخلط به', "«بطاقة السجل العدلي رقم 3» (Bulletin n° 3) التي تسلمها المحكمة الابتدائية للمغاربة غير مقبولة في ملفات الهجرة، لأنها لا تشمل إلا المخالفات المرتكبة في مدينة الإقامة."],
 ['مدة الصلاحية', "لا تحددها الصفحة الرسمية: تحقق منها لدى IRCC قبل تقديم طلبك حتى لا تضيع وقتك."],
])}
<p class="note">المصدر: {a('https://www.canada.ca/fr/immigration-refugies-citoyennete/services/demande/medical-police/certificats-police/comment/maroc.html', 'IRCC، كيف تحصل على شهادة شرطة: المغرب (بالفرنسية)')}.</p>
</div></section>
<section class="sp"><div class="wrap"><h2>البيانات البيومترية ومركز VFS Global</h2><div class="prose">
<p>رخّصت IRCC لشركة VFS Global باستقبال طلبات التأشيرة وتصاريح الدراسة والعمل بالمغرب، وبتسجيل بصماتك وصورتك. ولا يتم التسجيل إلا بموعد مسبق يُحجز عبر الإنترنت.</p>
<p>ولا يقدم المقيم المؤقت بياناته البيومترية إلا مرة كل 10 سنوات، بينما يلزم طالب الإقامة الدائمة بتقديمها عند كل طلب. تحقق من حالتك في موقع IRCC.</p>
<p class="note">المصدر: {a('https://visa.vfsglobal.com/mar/fr/can/faq', 'VFS Global المغرب، الأسئلة الشائعة (بالفرنسية)')}.</p></div></div></section>
<section class="sp alt"><div class="wrap"><h2>الوثائق الأخرى المعتادة</h2><div class="prose">
<p>تختلف اللائحة الدقيقة حسب طلبك، وتحددها IRCC لوضعك. وتشمل عادةً جواز السفر وعقد الازدياد والشهادات وكشوف النقط ونتائج اختبارات اللغة وإثباتات الموارد المالية أو التجربة المهنية.</p>
<p>وكل وثيقة غير محررة بالفرنسية أو الإنجليزية يجب أن تُرفق بترجمة. نراجع معك كل وثيقة قبل الإيداع حتى لا تؤخر ملفك.</p></div></div></section>''',
    faq=[
        ("ما اسم شهادة الشرطة بالنسبة للمغاربة؟", "تتحدث IRCC عن «البطاقة الأنتروبومترية» (fiche anthropométrique)، وتسلمها الشرطة."),
        ("هل «بطاقة السجل العدلي رقم 3» مقبولة؟", "لا، حين يحصل عليها المواطن المغربي من المحكمة الابتدائية، لأن IRCC ترى أنها محدودة بمدينة الإقامة."),
        ("هل يمكن طلب البطاقة نيابةً عن المرشح؟", "نعم، تذكر IRCC أنه يمكن لنائب أن يطلبها، بشرط الإدلاء ببطاقته الوطنية للتعريف الخاصة."),
        ("هل تجب ترجمة البطاقة؟", "لا، فهي تصدر بالفرنسية والعربية، ولا تشترط IRCC ترجمتها."),
        ("متى تلزم شهادة الشرطة؟", "تُشترط في طلب الإقامة الدائمة. أما الطلبات الأخرى فيرجع الأمر إلى كل حالة، ونتحقق منه خلال الاستشارة."),
    ],
    sources=[
        ('https://www.canada.ca/fr/immigration-refugies-citoyennete/services/demande/medical-police/certificats-police/comment/maroc.html', "IRCC، كيف تحصل على شهادة شرطة: المغرب (بالفرنسية)"),
        ('https://visa.vfsglobal.com/mar/fr/can/faq', "VFS Global المغرب، الأسئلة الشائعة (بالفرنسية)"),
    ],
    related=[('/ar/study-permit-morocco/', 'تصريح الدراسة'), ('/ar/express-entry-french/', 'الدخول السريع للناطقين بالفرنسية')],
))


def head_for(p):
    url = f"{SITE}/{p['path']}"
    fr_url = f"{SITE}/{p['fr']}"
    h = head_ref
    h = re.sub(r'<title>.*?</title>', f"<title>{e(p['title'], quote=False)}</title>", h, flags=re.S)
    h = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + e(p['desc'], quote=True) + m.group(2), h)
    for tag in ('og:title', 'twitter:title'):
        h = re.sub(rf'(<meta (?:property|name)="{tag}" content=")[^"]*(")', lambda m: m.group(1) + e(p['title'], quote=True) + m.group(2), h)
    for tag in ('og:description', 'twitter:description'):
        h = re.sub(rf'(<meta (?:property|name)="{tag}" content=")[^"]*(")', lambda m: m.group(1) + e(p['desc'], quote=True) + m.group(2), h)
    h = re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), h)
    h = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), h)
    h = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', '', h)
    alt = (f'<link rel="alternate" hreflang="fr-MA" href="{fr_url}">\n<link rel="alternate" hreflang="ar-MA" href="{url}">\n'
           f'<link rel="alternate" hreflang="x-default" href="{fr_url}">\n')
    h = re.sub(r'(<link rel="canonical" href="[^"]*">\n?)', lambda m: m.group(1) + alt, h, count=1)
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    g = json.loads(m.group(1))
    keep = [n for n in g['@graph'] if n['@type'] in ('ProfessionalService', 'WebSite')]
    keep += [
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": p['title'], "description": p['desc'],
         "inLanguage": "ar-MA", "dateModified": UPDATED, "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#organization"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "الرئيسية", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "الهجرة من المغرب", "item": SITE + "/ar/"},
            {"@type": "ListItem", "position": 3, "name": p['crumb'], "item": url}]},
        {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": "ar-MA", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a_)}} for q, a_ in p['faq']]},
    ]
    g['@graph'] = keep
    h = h[:m.start()] + '<script type="application/ld+json">' + json.dumps(g, ensure_ascii=False) + '</script>' + h[m.end():]
    if '<link rel="stylesheet" href="/assets/news.css">' in h:
        h = h.replace('<link rel="stylesheet" href="/assets/news.css">', '<link rel="stylesheet" href="/assets/news.css">\n' + EXTRA_CSS, 1)
    else:
        h += EXTRA_CSS
    return h


for p in PAGES:
    related = ''.join(f'<a class="btn btn-outline" style="color:var(--ink);border-color:var(--ink)" href="{u}">{e(l)}</a>' for u, l in p['related'])
    src = ''.join(f'<li>{a(u, l)}</li>' for u, l in p['sources'])
    page = f'''{head_for(p)}</head>
{topbar}<main>
<section class="pg-hero"><div class="wrap">
  <p class="crumb"><a href="/">الرئيسية</a> › <a href="/ar/">الهجرة من المغرب</a> › {e(p['crumb'])}</p>
  <p class="eyebrow">{e(p['eyebrow'])}</p>
  <h1>{e(p['h1'])}</h1>
  <p class="lede">{e(p['lede'])}</p>
  <div class="cta-row"><a class="btn btn-solid" href="/#contact">احجز موعدًا</a><a class="btn btn-outline" href="tel:+212633331715">اتصل بالدار البيضاء · <bdi dir="ltr">+212 633-331715</bdi></a></div>
</div></section>
{p['body']}
<section class="sp alt" id="faq"><div class="wrap"><h2>أسئلة شائعة</h2><div class="faq-list">{faq_html(p['faq'])}</div></div></section>
<section class="sp"><div class="wrap"><h2>المصادر الرسمية</h2><ul class="sources">{src}</ul>
<p class="note" style="margin-top:18px">آخر تحديث: 26 أكتوبر 2026.</p>
<div class="related">{related}</div></div></section>
{offices}
{footer}'''
    os.makedirs(R + p['path'], exist_ok=True)
    open(R + p['path'] + 'index.html', 'w', encoding='utf-8').write(page)
    print('ok', p['path'], len(page), 'octets')
