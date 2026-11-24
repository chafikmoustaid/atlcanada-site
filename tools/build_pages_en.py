#!/usr/bin/env python3
"""Génère les pages en anglais (phase 1 : accueil, honoraires, frais officiels, budget, rendez-vous, déroulement, à propos).
Reprend la mise en page des pages françaises (maroc/index.html) avec en-tête, pied de page et bureaux traduits.
Usage : python3 tools/build_pages_en.py   (depuis la racine du dépôt)"""
import json, re, html, os, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
SITE = 'https://www.atlcanada.com'
e = html.escape

ref = open(R + 'maroc/index.html', encoding='utf-8').read()
head_ref = ref[:ref.index('</head>')].replace('<html lang="fr-MA" dir="ltr">', '<html lang="en" dir="ltr">')
EXTRA_CSS = re.search(r'<style>\n\.tbl-wrap.*?</style>\n', open(R + 'tools/build_pages.py', encoding='utf-8').read(), re.S)
EXTRA_CSS = ('<style>\n' + re.search(r'EXTRA_CSS = """<style>\n(.*?)</style>', open(R + 'tools/build_pages.py', encoding='utf-8').read(), re.S).group(1) + '</style>\n')

WA = urllib.parse.quote("Hello ATL Canada, I would like some information about my plans to immigrate to Canada.")
topbar = ref[ref.index('<body>'):ref.index('<main>')]
social = re.search(r'<span class="tb-social nav-social">.*?</span>', topbar, re.S).group(0)
topbar = re.sub(r'<nav class="primary" aria-label="Navigation">.*?</nav>',
    lambda m: '<nav class="primary" aria-label="Navigation"><a href="/en/">Home</a><a class="nav-fees" href="/en/fees/">Fees</a><a href="/en/official-fees/">Official fees</a><a href="/en/budget-calculator/">Budget</a><a href="/en/about/">About</a>' + social + '</nav>', topbar, count=1, flags=re.S)
topbar = re.sub(r'<div class="nav-actions">.*?</div>\n  </div>',
    '<div class="nav-actions"><span class="lang" style="color:#fff"><a style="color:#fff;margin:0 10px" href="/" lang="fr" hreflang="fr"><span class="l-full">Français</span><span class="l-short">FR</span></a><a style="color:#fff;margin:0 10px" href="/ar/" lang="ar" hreflang="ar"><span class="l-full">العربية</span><span class="l-short">AR</span></a></span><a class="btn btn-solid" href="/en/book-consultation/">Book a consultation</a></div>\n  </div>', topbar, count=1, flags=re.S)
footer = ref[ref.index('</main>'):]
footer = re.sub(r'<footer>.*?</footer>',
    '<footer><div class="wrap"><p style="margin:0 0 12px;font-size:.9rem"><a href="/en/">Home</a> · <a href="/en/fees/">Fees</a> · <a href="/en/official-fees/">Official fees</a> · <a href="/en/study-permit/">Study permit</a> · <a href="/en/work-permit/">Work permit</a> · <a href="/en/express-entry/">Express Entry</a> · <a href="/en/permanent-residence/">Permanent residence</a> · <a href="/en/provincial-nominee/">Provincial nominees</a> · <a href="/en/immigrate-to-quebec/">Quebec</a> · <a href="/en/family-sponsorship/">Family sponsorship</a> · <a href="/en/visitor-visa/">Visitor visa</a> · <a href="/en/citizenship/">Citizenship</a> · <a href="/en/business-immigration/">Business</a> · <a href="/en/express-entry-french/">Express Entry (French)</a> · <a href="/en/moroccan-documents/">Moroccan documents</a> · <a href="/en/budget-calculator/">Budget calculator</a> · <a href="/en/book-consultation/">Book a consultation</a> · <a href="/en/case-process/">How a case works</a> · <a href="/en/about/">About</a> · <a href="/">Français</a> · <a href="/ar/" lang="ar">العربية</a></p><div class="footer-bottom"><a href="/confidentialite/" style="color:inherit">Privacy (French)</a> <span>© 2026 ATL Canada</span><span>Regulated Canadian immigration consultant (RCIC), licence <a class="ccic-link" href="https://registre.college-ic.ca/Public-Register-FR/Licensee/Profile.aspx?ID=10629" target="_blank" rel="noopener">R712906</a> with the CICC.</span></div></div></footer>',
    footer, count=1, flags=re.S)
footer = footer.replace('aria-label="Appeler" title="Appeler"', 'aria-label="Call" title="Call"')
footer = re.sub(r'wa\.me/15142956635\?text=[^"]*', 'wa.me/15142956635?text=' + WA, footer)

offices = re.search(r'<section class="sp" id="bureaux">.*?</section>', ref, re.S).group(0)
for fr, en in (('Nos bureaux', 'Our offices'), ('Casablanca, Maroc', 'Casablanca, Morocco'), ('Montréal (Québec) H1R 2T6, Canada', 'Montréal, Québec H1R 2T6, Canada'),
               ('Une question sur votre dossier ?', 'A question about your case?'), ('Lundi au vendredi : 10 h – 18 h · Samedi : 10 h – 12 h 30', 'Monday to Friday: 10 a.m. – 6 p.m. · Saturday: 10 a.m. – 12:30 p.m. (Montréal time)'),
               ('</svg>Appeler</a>', '</svg>Call</a>')):
    offices = offices.replace(fr, en)
offices = re.sub(r'wa\.me/15142956635\?text=[^"]*', 'wa.me/15142956635?text=' + WA, offices)
offices = re.sub(r'<p class="note" style="margin-top:22px">.*?</p>', '<p class="note" style="margin-top:22px">The information on this page is general and does not replace a personal assessment. Immigration rules change often: contact us for a review of your situation. No result is guaranteed.</p>', offices, flags=re.S)

TRUST = ('<section class="sp"><div class="wrap"><div class="trustbox"><h2>A regulated consultant, not an intermediary</h2>'
         '<p>ATL Canada is led by a regulated Canadian immigration consultant (RCIC), a member of the College of Immigration and Citizenship Consultants (CICC), licence R712906. The licence can be checked in the College\'s public register.</p></div></div></section>')

def tbl(rows, head):
    t = '<div class="tbl-wrap"><table class="tbl"><thead><tr><th>%s</th><th>%s</th></tr></thead><tbody>' % head
    for k, v in rows: t += '<tr><td>%s</td><td class="num">%s</td></tr>' % (k, v)
    return t + '</tbody></table></div>'
def faq_html(items):
    return ''.join(f'<details class="faq-item"{" open" if i == 0 else ""}><summary>{e(q)}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(items))
def strip(s): return re.sub(r'<[^>]+>', '', html.unescape(s))


def rich(headers, rows):
    if len(headers) == 3:
        out = ''
        for k in (1, 2):
            rws = ''.join('<div class="cmp-row"><b>%s</b><span>%s</span></div>' % (r[0], r[k]) for r in rows)
            out += '<div class="cmp-card%s"><h3>%s</h3>%s</div>' % (' b' if k == 2 else '', e(headers[k]), rws)
        return '<div class="cmp">%s</div>' % out
    def card(r):
        if len(r) > 2: return '<a class="info info-link" href="%s"><h3>%s</h3><p>%s</p><span class="go">Learn more \u2192</span></a>' % (r[2], r[0], r[1])
        return '<div class="info"><h3>%s</h3><p>%s</p></div>' % (r[0], r[1])
    return '<div class="info-grid">' + ''.join(card(r) for r in rows) + '</div>'

HON = [("Initial consultation (30 min), deducted from the price if you hire us", "100"), ("Study permit", "900"), ("Work permit: extension or post-graduation work permit", "650"),
 ("LMIA-exempt work permit", "1,100"), ("Visitor visa", "450"), ("Super visa (per applicant)", "800"), ("Express Entry: profile and permanent residence application", "2,150"),
 ("Provincial nominee, outside Express Entry", "3,000"), ("Sponsorship of a spouse or partner", "2,200"), ("Sponsorship of parents or grandparents", "2,500"),
 ("Canadian citizenship", "500"), ("Permanent resident card renewal", "600"), ("Extra family member in a permanent residence application", "400")]
OFF = [("Visitors", [("Visitor visa, per person", "100"), ("Visitor visa, family maximum (5 people or more)", "500"), ("Extending your stay as a visitor", "100"), ("Temporary resident permit", "246.25"), ("Electronic travel authorization (eTA)", "7")]),
 ("Study and work", [("Study permit (extension included)", "150"), ("Work permit (extension included)", "155"), ("Open work permit holder", "100"), ("Employer compliance fee", "230"), ("International Experience Canada", "184.75"), ("Biometrics, per person", "85"), ("Biometrics, family of 2 or more (maximum)", "170")]),
 ("Permanent residence", [("Economic (Express Entry, provincial), principal applicant: with the right of permanent residence fee", "1,590"), ("Same category, without the right of permanent residence fee", "990"), ("Business, principal applicant: with the right of permanent residence fee", "2,495"), ("Business, without the right of permanent residence fee", "1,895"), ("Accompanying spouse or partner (economic), with the right of permanent residence fee", "1,590"), ("Dependent child (economic)", "270"), ("Right of permanent residence fee alone", "600")]),
 ("Family sponsorship", [("Spouse, partner, parent, grandparent or relative aged 22 or over: with the right of permanent residence fee", "1,260"), ("Same categories, without the right of permanent residence fee", "660"), ("Dependent, adopted or orphaned child", "180")]),
 ("Documents and citizenship", [("Permanent resident card", "50"), ("Permanent resident travel document", "50"), ("Citizenship, adult (processing and right of citizenship included)", "653"), ("Citizenship, minor", "100"), ("Proof of citizenship", "75"), ("Authorization to return to Canada", "492.50")])]
usd = lambda rows: [(k, '$' + v) for k, v in rows]
HON_T = tbl(usd(HON), ("Service", "Starting from (CAD)"))
OFF_T = ''.join('<h3>%s</h3>%s' % (h, tbl(usd(rows), ("Application", "Fee (CAD)"))) for h, rows in OFF)

PAGES = []
def P(**k): PAGES.append(k)

P(path='en/', fr='/', ar='ar/', title="Immigration consultant in Montréal and Casablanca | ATL Canada",
  desc="ATL Canada is led by a regulated Canadian immigration consultant (RCIC R712906), with offices in Montréal and Casablanca. Clear fees, a written agreement before any payment and no promised results.",
  crumb=None, eyebrow="Montréal · Casablanca", h1="Immigration to Canada with a regulated consultant",
  lede="Study permits, work permits, permanent residence, family sponsorship, visits and citizenship. Clear fees, a written agreement before any payment, and honest advice about what is realistic for your profile.",
  body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>Clear fees, announced in advance</h2>
<p class="lede" style="max-width:720px">A starting price per service, a final quote after the consultation, and a written agreement before you pay anything. Government fees are separate.</p>
<div class="fee-grid hf-grid"><a class="fee-card" href="/en/fees/"><span class="fee-k">Study permit</span><span class="fee-v"><small>from</small> $900</span><span class="fee-s">government fee: $150</span></a><a class="fee-card" href="/en/fees/"><span class="fee-k">Visitor visa</span><span class="fee-v"><small>from</small> $450</span><span class="fee-s">government fee: $100</span></a><a class="fee-card" href="/en/fees/"><span class="fee-k">Express Entry</span><span class="fee-v"><small>from</small> $2,150</span><span class="fee-s">government fee: $1,590</span></a></div>
<p style="margin-top:20px"><a class="btn btn-solid" href="/en/fees/">See all fees</a> <a class="btn" href="/en/official-fees/">Official fees</a> <a class="btn" href="/en/budget-calculator/">Estimate my budget</a></p></div></section>
<section class="sp"><div class="wrap"><h2>What we help with</h2>
<div class="prose"><ul><li>Study permits: applications, extensions and changes of school.</li><li>Work permits: extensions, post-graduation and employer-supported permits.</li><li>Permanent residence: Express Entry, provincial nominee programs and Quebec.</li><li>Family sponsorship of a spouse, partner, parents or grandparents.</li><li>Visitor visas, super visas and Canadian citizenship.</li></ul>
<p>Read more: <a href="/en/study-permit/">study permit</a>, <a href="/en/work-permit/">work permit</a>, <a href="/en/permanent-residence/">permanent residence</a>, <a href="/en/express-entry/">Express Entry</a>, <a href="/en/provincial-nominee/">provincial nominees</a>, <a href="/en/immigrate-to-quebec/">Quebec</a>, <a href="/en/family-sponsorship/">family sponsorship</a>, <a href="/en/visitor-visa/">visitor visa and super visa</a>, <a href="/en/citizenship/">citizenship</a>, <a href="/en/business-immigration/">business immigration</a>, <a href="/en/express-entry-french/">Express Entry for French speakers</a> and <a href="/en/moroccan-documents/">Moroccan documents</a>.</p>
<p><a class="btn btn-solid" href="/en/book-consultation/">Book a consultation</a> <a class="btn" href="/en/case-process/">How a case works</a> <a class="btn" href="/en/about/">About us</a></p></div><p><a class="btn" href="/en/evaluate-my-case/">Assess my case in 5 questions</a></p></div></section>''',
  faq=[("Who is behind ATL Canada?", "ATL Canada is led by a regulated Canadian immigration consultant (RCIC), licence R712906 with the College of Immigration and Citizenship Consultants. The licence can be checked in the College's public register."),
       ("Can I get a consultation in English?", "Yes. Consultations are offered in English, French and Arabic."),
       ("Do you serve only people in Morocco?", "No. We help people from other countries and people already in Canada, for example to extend a work permit. We have offices in Montréal and Casablanca."),
       ("Can you guarantee my application will be approved?", "No. Only IRCC and the Quebec authorities decide. We tell you honestly which options are realistic for your profile."),
       ("How much do you charge?", "Starting prices are on our fees page. The final price is set after the consultation and written in a service agreement that you sign before paying anything.")])

P(path='en/fees/', fr='honoraires/', ar='ar/fees/', title="Immigration consulting fees in Canada | ATL Canada",
  desc="Our starting fees for study and work permits, Express Entry, sponsorship, citizenship and more. Final quote after the consultation, written agreement before any payment.",
  crumb="Fees", eyebrow="Transparency · Montréal · Casablanca", h1="Our fees",
  lede="Clear starting prices, a final quote after the consultation based on the complexity of your case, and a written agreement before you pay anything.",
  body=f'''{TRUST}
<section class="sp"><div class="wrap"><h2>Fees starting from</h2>{HON_T}
<p class="note">Amounts in Canadian dollars. Applicable taxes are extra. Our fees cover the preparation and follow-up of your application, but not government fees, biometrics, language tests, credential assessments, medical exams or translations.</p></div></section>
<section class="sp alt"><div class="wrap"><h2>How the final price is set</h2><div class="prose">
<p>The "from" price is for a simple case. After the consultation we give you a precise quote: a complex case (a previous refusal, a special situation, many documents) may cost more, and we tell you before we start. The services and fees are written in a service agreement that you sign before any payment.</p>
<p>The <a href="/en/official-fees/">official government fees</a> are paid directly to the authorities: they are not included in our fees.</p>
<p><a class="btn btn-solid" href="/en/book-consultation/">Book a consultation</a> <a class="btn" href="/en/budget-calculator/">Estimate my budget</a> <a class="btn" href="/en/case-process/">How a case works</a></p>
<p class="note">No result is guaranteed: the decision belongs solely to IRCC and the Quebec authorities.</p></div><p style="margin-top:14px"><a class="btn" href="/en/study-permit-cost/">Study permit cost</a> <a class="btn" href="/en/visitor-visa-cost/">Visitor visa cost</a> <a class="btn" href="/en/evaluate-my-case/">Assess my case</a></p></div></section>''',
  faq=[("Why "+"“from”"+" prices?", "Every case is different. The starting price is for a simple case; the final quote is set after the consultation and written in the service agreement."),
       ("Are government fees included?", "No. They are paid directly to IRCC or the Quebec authorities. See the official fees page."),
       ("Is the initial consultation deducted?", "Yes. If you hire us, the $100 initial consultation is deducted from the price of your case."),
       ("Are taxes included?", "No. Applicable taxes are added to our starting fees."),
       ("Can I get an exact price before the consultation?", "The starting price gives the order of magnitude. The exact price depends on your situation and we give it to you in writing after the consultation. You can also try our <a href=\"/en/budget-calculator/\">budget calculator</a>."),
       ("What happens if my application is refused?", "Our fees pay for our work, not for the result, which nobody can guarantee. The exact terms are in the service agreement.")])

P(path='en/official-fees/', fr='frais-officiels-immigration-canada/', ar='ar/official-fees/', title="Official Canadian immigration fees (IRCC) in force | ATL Canada",
  desc="Current Canadian government fees: visitor visa, study and work permits, permanent residence, sponsorship, citizenship, biometrics. Updated November 24, 2026.",
  crumb="Official fees", eyebrow="Government fees · as of November 24, 2026", h1="Official Canadian immigration fees",
  lede="Canadian government (IRCC) fees for the most common applications, in Canadian dollars, as displayed on November 24, 2026.",
  body=f'''{TRUST}
<section class="sp"><div class="wrap">{OFF_T}
<p class="note">These fees are paid directly to the government and are in addition to our fees. They can change: the official list on the IRCC website (canada.ca) prevails. Quebec fees (acceptance certificate, selection), language tests, VFS and translation fees are not listed here.</p>
<p><a class="btn btn-solid" href="/en/book-consultation/">Book a consultation</a> <a class="btn" href="/en/budget-calculator/">Estimate my budget</a> <a class="btn" href="/en/fees/">Our fees</a></p></div></section>''',
  faq=[("Are these fees added to your fees?", "Yes. Government fees are paid directly to the authorities; our fees pay for our work."),
       ("When do these fees change?", "IRCC publishes its changes in advance on its website. The last increase in permanent residence fees was on April 30, 2026."),
       ("What is the right of permanent residence fee?", "It is a $600 fee added to the processing of a permanent residence application for the principal applicant and spouse. It does not apply to dependent children.")])

P(path='en/budget-calculator/', fr='budget-immigration-canada/', ar='ar/budget-calculator/', title="Canada immigration budget calculator | ATL Canada",
  desc="Estimate the budget of your case: starting fees, government fees and biometrics by service and family size. Free indicative estimate.",
  crumb="Budget calculator", eyebrow="Free tool · estimate in 30 seconds", h1="Budget calculator",
  lede="Choose your service to estimate the cost of your case: our fees, government fees and biometrics. Nothing is sent or saved.",
  body=f'''{TRUST}
<section class="sp"><div class="wrap">
<link rel="stylesheet" href="/assets/budget.css">
<div id="budget-app" data-lang="en"></div>
<noscript><p class="note">This calculator needs JavaScript. See our <a href="/en/fees/">fees</a> and the <a href="/en/official-fees/">official fees</a> instead.</p></noscript>
<script src="/assets/budget.js" defer></script>
</div></section>''',
  faq=[("Is this amount final?", "No. It is an estimate based on our starting prices and the official fees. The final price is set after the consultation according to the complexity of the case."),
       ("Are taxes included?", "No. Applicable taxes are added to our fees."),
       ("Why is biometrics shown as “if required”?", "It is not required of everyone: a person who gave biometrics recently may be exempt. We check this with you.")])

P(path='en/book-consultation/', fr='rendez-vous/', ar='ar/book-consultation/', title="Book a consultation with an immigration consultant | ATL Canada",
  desc="Request a consultation with a regulated Canadian immigration consultant: phone, WhatsApp, Teams or in person in Montréal and Casablanca. We confirm the time with you.",
  crumb="Book a consultation", eyebrow="Consultation · Montréal · Casablanca", h1="Book a consultation",
  lede="Choose the day, time slot and format that suit you. We contact you to confirm the exact time.",
  body=f'''{TRUST}
<section class="sp"><div class="wrap">
<link rel="stylesheet" href="/assets/rdv.css">
<div id="rdv-app" data-lang="en"></div>
<noscript><p class="note">This form needs JavaScript. Email us at contact@atlcanada.com or call +1 514 295 6635.</p></noscript>
<script src="/assets/rdv.js" defer></script>
</div></section>
<section class="sp alt"><div class="wrap"><h2>How does the consultation work?</h2><div class="prose">
<p>We review your plans and your situation, check the current state of the programs before you spend anything, and compare the realistic options for your profile.</p>
<p>Consultations are offered in English, French and Arabic.</p>
<p>Office hours: Monday to Friday, 10 a.m. to 6 p.m., and Saturday, 10 a.m. to 12:30 p.m. (Montréal time).</p>
<p class="note">The decision belongs solely to IRCC and the Quebec authorities: we cannot guarantee a result or promise a timeline.</p></div></div></section>''',
  faq=[("Does the request confirm the appointment?", "No. It tells us your preferences; we contact you to confirm the exact time."),
       ("Can I consult from Morocco or another country?", "Yes. Consultations are held by phone, WhatsApp or video call, and also in person in Montréal or Casablanca."),
       ("Is my information protected?", "It is used only to answer your request. See our privacy policy (in French).")])

P(path='en/case-process/', fr='deroulement-dossier-immigration/', ar='ar/case-process/', title="How an immigration case works with ATL Canada | ATL Canada",
  desc="The steps of our support: consultation, choosing the route, written agreement, document preparation, filing and follow-up. What a regulated consultant does, and what no consultant can promise.",
  crumb="How a case works", eyebrow="Support · Montréal · Casablanca", h1="How a case works with ATL Canada",
  lede="From the first consultation to the follow-up of your application: the steps, what we do for you, and what no serious consultant can promise.",
  body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>The steps</h2>
<ol class="steps">
<li><span><b>Consultation.</b> We review your plans, your current situation and your application history.</span></li>
<li><span><b>Choosing the route.</b> We check the current state of the programs and compare the realistic routes for your profile, before you spend anything.</span></li>
<li><span><b>Written service agreement.</b> It states the planned services and fees before you pay anything.</span></li>
<li><span><b>Document preparation.</b> We tell you which documents to gather, check that they are consistent and prepare the application with you.</span></li>
<li><span><b>Filing.</b> The application is filed with IRCC or the Quebec authorities, depending on the route.</span></li>
<li><span><b>Follow-up.</b> We follow your file and help you respond to the authorities until a decision is made.</span></li>
</ol></div></section>
<section class="sp"><div class="wrap"><h2>What we cannot promise</h2><div class="prose">
<p>The decision belongs solely to IRCC and the Quebec authorities. We cannot guarantee a result, promise a timeline or obtain priority processing: using a consultant gives no priority. Be wary of anyone who promises otherwise.</p>
<p>You remain responsible for the accuracy of the information and documents you provide. Our role is to guide you, to check, and to avoid the mistakes that cost time and money.</p>
<p><a class="btn btn-solid" href="/en/book-consultation/">Book a consultation</a> <a class="btn" href="/en/fees/">Our fees</a></p></div><p><a class="btn" href="/en/documents-checklist/">Documents checklist</a> <a class="btn" href="/en/refused-application/">Refused application</a> <a class="btn" href="/en/whats-changing/">What is changing</a></p></div></section>''',
  faq=[("How much does support cost?", "Fees depend on the type of case and are written in the service agreement before any payment. See our <a href=\"/en/fees/\">fees</a> and the <a href=\"/en/official-fees/\">official fees</a>, or ask us for a consultation."),
       ("Can you speed up my case?", "No. Timelines depend on the authorities. A complete and consistent file from the day it is filed is the best preparation."),
       ("What happens if my application is refused?", "We analyze the decision letter with you and look at the possible options. A refusal is not automatically solved by filing again."),
       ("Can I be supported from Morocco?", "Yes. We have an office in Casablanca and we also work remotely, by phone, WhatsApp or video call.")])

P(path='en/about/', fr='a-propos/', ar='ar/about/', title="About ATL Canada: a regulated immigration consultant | ATL Canada",
  desc="ATL Canada is led by a regulated Canadian immigration consultant (RCIC R712906), with offices in Montréal and Casablanca. Who we are, what we do and what we do not promise.",
  crumb="About", eyebrow="Montréal · Casablanca", h1="About ATL Canada",
  lede="An immigration firm led by a regulated consultant, with offices in Montréal and Casablanca, serving candidates from Morocco and elsewhere and people already in Canada.",
  body=f'''{TRUST}
<section class="sp"><div class="wrap"><h2>Who we are</h2><div class="prose">
<p>ATL Canada supports people who want to study, work, settle or bring their family to Canada, and people already in Canada who need to extend or change their status.</p>
<p>The firm is led by a regulated Canadian immigration consultant, a member of the College of Immigration and Citizenship Consultants (CICC), licence number R712906. You can check this licence in the <a href="https://registre.college-ic.ca/Public-Register-FR/Licensee/Profile.aspx?ID=10629" target="_blank" rel="noopener">College's public register</a>.</p></div></div></section>
<section class="sp alt"><div class="wrap"><h2>What we do</h2><div class="prose"><ul><li>A consultation to understand your situation and tell you which routes are realistic.</li><li>Preparing, checking and filing your application, then following it up.</li><li>A price announced in advance and written in a service agreement signed before any payment.</li><li>Consultations in English, French and Arabic.</li></ul></div></div></section>
<section class="sp"><div class="wrap"><h2>What we do not do</h2><div class="prose">
<p>We do not guarantee a result or a timeline: the decision belongs solely to IRCC and the Quebec authorities. We do not promise job offers and we do not buy documents. If a route is not realistic for you, we tell you honestly.</p>
<p><a class="btn btn-solid" href="/en/book-consultation/">Book a consultation</a> <a class="btn" href="/en/fees/">Our fees</a> <a class="btn" href="/en/case-process/">How a case works</a></p></div></div></section>''',
  faq=[("Is ATL Canada a regulated firm?", "Yes. It is led by a regulated Canadian immigration consultant (RCIC R712906), whose licence can be checked in the College's public register."),
       ("Where are your offices?", "In Montréal (8405 Viau, Québec H1R 2T6) and Casablanca (325 Emile Zola). Consultations are also held by phone, WhatsApp or Teams."),
       ("Do you serve only candidates from Morocco?", "No. We also support people from other countries and people already in Canada.")])

LAWNOTE = '<p class="note">The decision belongs solely to IRCC: we cannot guarantee a result or promise a timeline.</p>'

P(path='en/study-permit/', fr='permis-etudes-canada-maroc/', ar='ar/study-permit-morocco/', title="Study permit in Canada: application, extension, change of school | ATL Canada",
  desc="Study permit for Canada, from abroad (including Morocco) or from inside Canada: attestation letter, proof of funds, extension, change of institution. A regulated consultant supports you.",
  crumb="Study permit", eyebrow="Study · Montréal · Casablanca", h1="Study permit in Canada: application, extension, change",
  lede="Whether you are applying from abroad or already studying in Canada: the steps, the documents to prepare, what to know to extend your permit or change schools, and the points where a case is won or lost.",
  body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>The steps, from admission to departure</h2>
<ol class="steps">
<li><span>Choose a program at a designated learning institution: a study permit is only issued to study at one.</span></li>
<li><span>Get your letter of acceptance and, when required, the provincial or territorial attestation letter (PAL/TAL).</span></li>
<li><span>Gather proof of funds: first-year tuition, living costs and transportation costs.</span></li>
<li><span>File the application online with IRCC, then give your biometrics (from Morocco: at a VFS Global centre).</span></li>
<li><span>Respond to IRCC's requests until a decision is made, then prepare your arrival.</span></li>
</ol></div></section>
<section class="sp"><div class="wrap"><h2>Points to prepare carefully</h2>
{rich(['Item', 'What to know'], [
 ['Attestation letter (PAL/TAL)', "Required for most new applications, with exceptions set by IRCC. For 2026, one exception covers master's and doctoral students at a designated public institution."],
 ['Proof of funds', "You must prove your first-year tuition, living costs and transportation costs. For applications filed from September 1, 2026, IRCC requires at least $23,448 CAD in living costs for a single person, excluding tuition and transportation (outside Quebec: Quebec sets its own requirements with the CAQ). IRCC reviews this amount regularly: we confirm it with you at the consultation."],
 ['Biometrics', "Fingerprints and a photo are given by appointment; from Morocco, at a VFS Global centre. For a temporary resident, they stay valid for 10 years."],
 ['Letter of acceptance', "It must come from a designated learning institution and match the program named in your application."],
])}
<p class="note" style="margin-top:18px">To study in Quebec, a provincial step is added (the CAQ): we go through it with you at the consultation if your plan goes that way.</p>
</div></section>
<section class="sp"><div class="wrap"><h2>Already in Canada?</h2>
{rich(['Situation', 'What IRCC says'], [
 ["Extending your study permit", "To stay at the same institution, file the application at least 30 days before the permit expires. If you stay in Canada, you can keep studying under the same conditions until a decision is made. The permit cannot be extended beyond your passport's expiry date."],
 ["Changing institution", "Apply for the extension before finishing your current program. In general, you cannot start at the new school before the extended permit is approved, with some exceptions."],
 ["Studies longer than planned", "File the application at least 30 days before the permit's original expiry date."],
 ["Studies finished early", "The permit expires on the earlier of two dates: the date on the permit, or 90 days after the end of your studies (from the school's first notice or the issue of your degree)."],
 ["The school loses its designated status", "You can keep studying until the permit expires or move to another designated institution. To extend, you must be enrolled at a designated institution."],
])}
<p class="note" style="margin-top:18px">Is your study permit expired, or are you unsure? Talk to us before acting: the rules depend on your situation.</p>
</div></section>
<section class="sp alt"><div class="wrap"><h2>After your studies</h2><div class="prose">
<p>Depending on the program and the institution, a post-graduation work permit may be possible. That Canadian work experience can then count toward a permanent residence application, for example through Express Entry.</p>
<p>See also <a href="/en/express-entry/" style="text-decoration:underline">our Express Entry page</a> and <a href="/en/work-permit/" style="text-decoration:underline">work permits</a>.</p></div><p><a class="btn" href="/en/study-permit-cost/">How much does it cost?</a> <a class="btn" href="/en/documents-checklist/">Documents checklist</a></p></div></section>''',
  faq=[("Do I need a study permit?", "Generally yes (this is the case for Moroccan citizens) when the program lasts more than six months. For a shorter course the rules differ: we check your case with you."),
       ("Which documents do I need to provide?", "The exact list is set by IRCC according to your situation. It usually includes the passport, the letter of acceptance, proof of funds and, when required, the PAL/TAL. We validate it with you before filing."),
       ("How long does processing take?", "Timelines change regularly: IRCC publishes them on its website and we promise no timeline. We tell you the current situation at your appointment."),
       ("When should I apply to extend my study permit?", "At least 30 days before it expires, according to IRCC. If you stay in Canada, you can keep studying under the same conditions until a decision is made."),
       ("Do I have to use a consultant?", "No, you can file your application yourself. A regulated consultant helps you choose the right strategy, prepare a complete file and avoid omissions."),
       ("Do you guarantee that I will get the permit?", "No. No serious consultant can guarantee a decision: it belongs solely to the Canadian authorities.")])

P(path='en/work-permit/', fr='permis-de-travail-canada/', ar='ar/work-permit/', title="Work permit in Canada: application, extension, change of employer | ATL Canada",
  desc="Work permit for Canada, from abroad or from inside Canada: employer-specific or open permit, LMIA, extension, maintained status, post-graduation work permit. A regulated consultant supports you.",
  crumb="Work permit", eyebrow="Work · Montréal · Casablanca", h1="Work permit in Canada: application, extension, change",
  lede="Whether you are abroad or already in Canada, of any nationality: working in Canada almost always requires a permit. Here are the two main types of permit, the employer's role, and what to know to extend or change your permit.",
  body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>Two main types of permit</h2>
{rich(['', 'Employer-specific permit', 'Open permit'], [
 ["Principle", "It lets you work only under its conditions: the employer, location and occupation are written on the permit, until its expiry date.", "It lets you work for most compliant employers in Canada, without being tied to a single one."],
 ["Job offer", "An offer from an employer that is not on the list of non-compliant employers is needed.", "No job offer is needed."],
 ["Who it is for", "This is the most common type.", "Only in specific situations set out by IRCC."],
])}
<p class="note" style="margin-top:18px">Some people do not need a work permit: IRCC offers an online questionnaire to check.</p>
</div></section>
<section class="sp"><div class="wrap"><h2>Already in Canada?</h2>
{rich(['Situation', 'What IRCC says'], [
 ["Extending your permit", "The application must be filed before the permit expires: an online application must be sent before midnight (universal time) on the expiry date. You cannot extend beyond your passport's expiry date."],
 ["Maintained status", "If you applied in time, you can stay in Canada while the application is processed. With an employer-specific permit, you can keep working only for the same employer, in the same position and at the same location. With an open permit, you can change employers."],
 ["While processing", "You cannot renew some provincial documents, such as a driver's licence or health insurance card: renew them before the permit expires. An online application generally gives you a letter (WP-EXT) that shows your employer you can keep working."],
 ["Changing the permit's conditions", "A change of employer, position or location for an employer-specific permit goes through an application to change conditions. Talk to us before changing anything."],
 ["Post-graduation work permit", "To be filed within 180 days of confirmation that your studies are complete. You must have completed a program of at least 8 months (900 hours in Quebec) at an eligible institution, have studied full time and, for applications filed since November 1, 2024, meet the language requirements (CLB 7 for university, CLB 5 for college) and, for some programs, the field-of-study requirements."],
 ["Permit already expired", "If your permit expires during processing or has already expired, check with us whether you can keep working: the rules depend on your situation."],
])}
<p class="note" style="margin-top:18px">Fees and rules change: IRCC keeps the list up to date, and we check it with you before filing.</p>
</div></section>
<section class="sp alt"><div class="wrap"><h2>The employer-specific permit, step by step</h2>
<ol class="steps">
<li><span>Get a job offer from an employer that is not on the list of non-compliant employers.</span></li>
<li><span>Your employer confirms whether the position requires a Labour Market Impact Assessment (LMIA) or is exempt. "Most jobs require an LMIA," says IRCC.</span></li>
<li><span>If an LMIA is required, the employer applies for it and gives you the LMIA letter and Appendix A before your application.</span></li>
<li><span>You file your permit application: from outside Canada, from inside, at a port of entry, or for an extension, depending on your situation.</span></li>
<li><span>Once the permit is issued, you follow its conditions (employer, location, occupation, expiry date).</span></li>
</ol>
<div class="prose" style="margin-top:22px"><p>Without a permit, you cannot legally work in Canada, or state in an application that you are authorized to. IRCC also offers specific routes, such as International Experience Canada (Young Professionals), the Global Skills Strategy and agricultural work.</p>
<p>A work permit can also be a step toward permanent residence: see our <a href="/en/express-entry/" style="text-decoration:underline">Express Entry page</a>.</p></div>
</div></section>
<section class="sp"><div class="wrap"><h2>How we support you</h2><div class="prose">
<p>At the consultation, whether you are abroad or already in Canada, we work out with you which type of permit fits your situation (new application, extension, change of conditions, post-graduation permit), we check the documents your employer must give you and we prepare your application before filing. If you do not yet have an offer, we look at the realistic options together.</p>
{LAWNOTE}</div></div></section>''',
  faq=[("Do I need a work permit?", "In most cases, yes. Some people are exempt: IRCC offers an online questionnaire to check, and we do it with you."),
       ("What is an LMIA?", "The Labour Market Impact Assessment shows that there is a need to hire a foreign worker. Your employer must confirm whether your position requires one or is exempt."),
       ("Can I change employer with an employer-specific permit?", "This permit is tied to the employer, location and occupation shown. Before any change, talk to us to learn the steps to follow."),
       ("What happens if I work without a permit?", "You cannot legally work in Canada without the required permit. You also must not state in an application that you are authorized to if you are not."),
       ("What if my permit expires while my extension is processed?", "If you filed before the expiry, you have maintained status and can stay in Canada. With an employer-specific permit, you can keep working only for the same employer, in the same position and at the same location."),
       ("When should I apply for the post-graduation work permit?", "Within 180 days of confirmation that your program is complete, according to IRCC. Your study permit must have been valid at some point during those 180 days."),
       ("Do you guarantee that I will get the work permit?", "No. No serious consultant can guarantee a decision: it belongs solely to the Canadian authorities.")])

P(path='en/express-entry/', fr='entree-express-canada/', ar='ar/express-entry/', title="Express Entry Canada: programs, points and 2026 changes | ATL Canada",
  desc="Express Entry: the three programs, the requirements, the points ranking (CRS) and the official changes of November 3, 2026. A regulated consultant supports you.",
  crumb="Express Entry", eyebrow="Express Entry · Montréal · Casablanca", h1="Express Entry: programs, points and 2026 changes",
  lede="Express Entry manages permanent residence applications for three federal programs. Here are the basic requirements, how the ranking works and what has changed since November 3, 2026.",
  body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>How it works</h2>
<ol class="steps">
<li><span>You create an online profile and enter the pool of candidates.</span></li>
<li><span>You receive a score under the Comprehensive Ranking System (CRS), calculated from points.</span></li>
<li><span>IRCC invites the top-ranked candidates to apply for permanent residence, in draws.</span></li>
<li><span>If you are invited, you complete the application, upload your documents and pay the fees, then IRCC makes its decision.</span></li>
</ol>
</div></section>
<section class="sp"><div class="wrap"><h2>The three programs</h2>
{rich(['Program', 'What IRCC says'], [
 ['Federal Skilled Worker', "At least 1 year (or 1,560 hours) of skilled work (TEER 0, 1, 2 or 3) in the same occupation within the last 10 years; approved language test results (CLB 7 minimum for the first official language); completed Canadian education or a foreign credential with an assessment (ECA); 67 points out of 100 on the selection factors; sufficient funds, unless exempt."],
 ['Federal Skilled Trades', "At least 2 years of full-time work (or 3,120 hours) in a skilled trade within the last 5 years; a full-time job offer of at least 1 year or a Canadian certificate of qualification in the trade; approved language test."],
 ["Canadian Experience Class", "At least 1 year (or 1,560 hours) of skilled work (TEER 0, 1, 2 or 3) in Canada within the last 3 years, with a temporary status that allowed you to work; approved language test. No education requirement."],
])}
<p class="note" style="margin-top:18px">In all cases, you must be admissible to Canada and plan to live outside Quebec (Quebec has its own selection).</p>
</div></section>
<section class="sp alt"><div class="wrap"><h2>What has changed since November 3, 2026</h2><div class="prose">
<p>According to IRCC (announcement of October 16, 2026), the system now gives additional points for eligible Canadian work experience or an eligible job offer in a high-wage occupation (an occupation whose median wage is at least 1.3 times that of all Canadian workers). An LMIA is no longer needed for a job offer to give these points or to meet the job offer requirements of the Federal Skilled Worker and Federal Skilled Trades programs.</p>
<p>Scores of candidates already in the pool are recalculated automatically. IRCC states that the recalculation can take up to two weeks and that draws are paused during that time. To receive the job offer points, the profile had to be updated before November 3.</p>
</div>
<div style="margin-top:22px"></div>
{rich(['IRCC scale', 'Points'], [
 ["Eligible job offer", "100 points if the occupation's median wage is at least 2 times the average median wage; 70 points between 1.5 and 2 times; 50 points between 1.3 and 1.5 times; 0 points for an occupation that is not high-wage."],
 ["Canadian experience in a high-wage occupation", "In addition to the points for length of work, at least 12 months (1,560 hours) of eligible experience gives 70 points (at least 2 times), 40 points (at least 1.5 times) or 20 points (at least 1.3 times)."],
 ["LMIA", "No longer needed and no longer gives extra points or priority."],
])}
<div class="prose" style="margin-top:18px"><p class="note">These rules evolve: the state described is that of November 5, 2026. Check your current situation with us.</p></div>
</div></section>
<section class="sp"><div class="wrap"><h2>How we support you</h2><div class="prose">
<p>At the consultation, we check which programs you qualify for, estimate your ranking, identify the easy points to improve (languages, credential assessment, job offer) and prepare your profile and documents. See also our <a href="/en/work-permit/" style="text-decoration:underline">work permit page</a>.</p>
{LAWNOTE}</div></div></section>''',
  faq=[("Which programs does Express Entry manage?", "The Federal Skilled Worker Program, the Federal Skilled Trades Program and the Canadian Experience Class. Part of the Provincial Nominee Program is also linked to it."),
       ("Do I need to have worked in Canada?", "Not for the Federal Skilled Worker Program, which can count experience gained abroad. It is however required for the Canadian Experience Class."),
       ("Is an LMIA always needed for a job offer?", "According to IRCC, since November 3, 2026, an LMIA is no longer needed for a job offer to give the new points or meet the job offer requirements of the Federal Skilled Worker and Federal Skilled Trades programs."),
       ("What does “high-wage occupation” mean?", "According to IRCC, it is an occupation whose median wage is at least 1.3 times that of all Canadian workers. IRCC publishes and updates the list."),
       ("Do you guarantee an invitation?", "No. IRCC invites the top-ranked candidates in draws: nobody can guarantee an invitation or a result.")])

P(path='en/family-sponsorship/', fr='parrainage-familial-canada/', ar='ar/family-sponsorship/', title="Family sponsorship in Canada: spouse, children, parents | ATL Canada",
  desc="Reunite your family in Canada: who can be sponsored, proof of the relationship, declaring family members. A regulated consultant prepares your file.",
  crumb="Family sponsorship", eyebrow="Family · Montréal · Casablanca", h1="Family sponsorship: reuniting your family in Canada",
  lede="Spouse, dependent children, parents or grandparents: sponsorship lets your family come to live in Canada. Here is who can be sponsored and the points where a case is won or lost.",
  body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>Who can be sponsored?</h2>
{rich(['Relationship to you', 'What IRCC says'], [
 ['Spouse', "Legally married, at least 18 years old, in a genuine relationship (not entered into only to gain permanent resident status)."],
 ['Common-law partner', "At least 18 years old, in a genuine relationship, and having lived with you for at least 12 consecutive months in a conjugal relationship."],
 ['Conjugal partner', "At least 18 years old, in an exclusive relationship of at least 1 year, living outside Canada and unable to live with you or marry you for specific reasons."],
 ['Dependent child', "Your child, or your spouse's or partner's child, under 22 and without a spouse, or 22 or older but financially dependent because of a physical or mental condition (or dependent since before age 22)."],
 ['Parents and grandparents', "Your parents and grandparents, by blood or adoption, with their dependent children. Your spouse's parents cannot be sponsored by you."],
])}
<p class="note" style="margin-top:18px">In all cases, the sponsored person must not be inadmissible to Canada.</p>
</div></section>
<section class="sp"><div class="wrap"><h2>Points to prepare carefully</h2>
<ol class="steps">
<li><span>Check that the sponsor and the sponsored person meet IRCC's conditions, notably the sponsor's status in Canada.</span></li>
<li><span>Show a genuine relationship: IRCC examines whether the bond is real and not just a way to obtain permanent residence.</span></li>
<li><span>Declare all family members, including children who are not coming or whose other parent has sole custody. An omission can compromise the case.</span></li>
<li><span>Gather the requested forms and documents, then respond to requests during processing (medical exam, police certificate, biometrics).</span></li>
<li><span>Follow the case until the decision, without changing the declared information without talking to us.</span></li>
</ol>
<div class="prose" style="margin-top:22px"><p>An IRCC policy that allowed sponsoring some undeclared family members does not apply to applications filed after September 10, 2026: a complete declaration of the family is therefore essential. For Moroccan documents (birth certificate, police certificate), see also our page on <a href="/en/moroccan-documents/" style="text-decoration:underline">Moroccan documents</a>.</p></div>
</div></section>
<section class="sp alt"><div class="wrap"><h2>How we support you</h2><div class="prose">
<p>At the consultation, we check with you which sponsorship category fits your family, whether the conditions are met and which proof of the relationship is strongest. We then prepare a complete, consistent file before filing. The program for parents and grandparents has its own access rules, which IRCC changes over time: we check with you where it stands at the time of your application.</p>
{LAWNOTE}</div></div></section>''',
  faq=[("Who can sponsor a family member?", "The sponsor must meet the conditions set by IRCC, notably regarding their status in Canada. We check them with you at the consultation."),
       ("What is the difference between a spouse and a common-law partner?", "A spouse is legally married to you. A common-law partner is not, but has lived with you for at least 12 consecutive months in a conjugal relationship."),
       ("Up to what age is a child dependent?", "A child under 22 without a spouse is considered dependent. Beyond that, the child must be financially dependent on their parents because of a physical or mental condition, or since before age 22."),
       ("Must I declare a child who is not coming to Canada?", "Yes. IRCC requires all children to be declared, even those who are not coming or whose other parent has sole custody."),
       ("Can you guarantee that the sponsorship will be approved?", "No. No serious consultant can guarantee a decision: it belongs solely to the Canadian authorities.")])

P(path='en/visitor-visa/', fr='visa-visiteur-super-visa-canada/', ar='ar/visitor-visa-super-visa/', title="Visitor visa, super visa and extending your stay in Canada | ATL Canada",
  desc="Visitor visa or super visa for your parents and grandparents: requirements, host's minimum income, insurance, medical exam. A regulated consultant supports you.",
  crumb="Visitor visa and super visa", eyebrow="Visitors · Montréal · Casablanca", h1="Visitor visa, super visa and extending your stay",
  lede="Visiting a relative, travelling or coming to see your children and grandchildren: the visitor visa covers most stays, and the super visa is designed for parents and grandparents. Here are the official requirements and the documents to prepare.",
  body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>Visitor visa or super visa: which to choose?</h2>
{rich(['', 'Visitor visa', 'Super visa'], [
 ['Who it is for', "Anyone coming to visit Canada (family, tourism, business)", "Parents and grandparents of a Canadian citizen, a permanent resident or a person registered under the Indian Act"],
 ['Stay', "Suitable for stays of 6 months or less, according to IRCC", "For longer stays: the officer may authorize a stay of 5 years, according to IRCC"],
 ['Invitation', "An invitation letter can be useful, even requested in some cases", "Invitation letter signed by your child or grandchild, mandatory"],
 ['Medical insurance', "Not required by IRCC's list of requirements", "Private insurance valid for at least 1 year, mandatory"],
])}
</div></section>
<section class="sp"><div class="wrap"><h2>Already in Canada?</h2>
{rich(['Situation', 'What IRCC says'], [
 ['Extending your stay', "Visitors, but also workers and students authorized to work or study without a permit, can apply for an extension. File the application at least 30 days before your status expires."],
 ['Which date counts?', "Check the stamp in your passport (not the date on the visitor visa); with no stamp, the limit is 6 months after your date of entry. For a study or work permit, it is the permit's date; for an extension already granted, the visitor record."],
 ['Switching to visitor status', "A holder of a study or work permit can also apply to become a visitor. Your original entry document (visa, eTA) does not matter."],
])}
<p class="note" style="margin-top:18px">Is your status already expired or close to it? Talk to us quickly: the rules depend on your situation.</p>
</div></section>
<section class="sp alt"><div class="wrap"><h2>Visitor visa: what IRCC checks</h2>
<ol class="steps">
<li><span>You have a valid travel document, such as a passport (IRCC recommends it be valid for at least 6 months from the planned travel date).</span></li>
<li><span>You are in good health. A medical exam may be required.</span></li>
<li><span>You have no criminal conviction or immigration-related conviction.</span></li>
<li><span>You have ties to your home country (job, home, financial assets, family) that give you a reason to return.</span></li>
<li><span>You show that you will leave Canada at the end of your stay.</span></li>
<li><span>You have enough money for your stay: the amount depends on the length and type of accommodation (hotel or with relatives).</span></li>
</ol>
<div class="prose" style="margin-top:22px"><p>For a tourist stay, IRCC notably recommends including: an invitation letter and proof of your relationship with the person inviting you, your travel history, an itinerary, bank statements covering at least 6 months and a letter from your employer dated no more than 3 months ago.</p></div>
{rich(['Item', 'What IRCC says'], [
 ['Processing fee', "$100 CAD per person, or $500 CAD for a family of 5 or more."],
 ['Biometrics', "$85 CAD per person, or up to $170 CAD for an eligible family. Wait for the instruction letter, then book your appointment quickly."],
 ['Filing', "Online, through the IRCC portal. Paper applications are allowed only in specific cases."],
 ['Validity', "A visa can be issued for a maximum of 10 years, or until the passport or biometrics expire if that happens first. The officer may set another date."],
])}
</div></section>
<section class="sp alt"><div class="wrap"><h2>Super visa: the requirements</h2>
{rich(['Requirement', 'What IRCC says'], [
 ["Your child or grandchild (the host)", "A Canadian citizen, permanent resident or person registered under the Indian Act, at least 18 years old and living in Canada. The relationship (biological or adopted child or grandchild) must be proven, for example with their birth certificate."],
 ['Invitation letter', "Signed by the host, it must show that they meet the minimum necessary income and list everyone counted in their family, with name and date of birth. Their spouse or common-law partner may co-sign if they are a citizen, permanent resident or registered under the Indian Act."],
 ["Host's minimum income", "It is set from Statistics Canada's low-income cut-offs. The host proves it with their Canada Revenue Agency notices of assessment for one of the two tax years before the application, or with other documents set by IRCC. The amount depends on family size: see the up-to-date table on IRCC's page, as it is updated."],
 ['Medical insurance', "Private insurance valid for at least 1 year from the date of entry and for each entry into Canada, from a Canadian insurer or a foreign insurer authorized by OSFI and on its list. It covers health care, hospitalization and repatriation, with emergency coverage of at least $100,000. It must be paid, in full or in instalments with a deposit: a mere quote is not accepted."],
 ['Medical exam', "An immigration medical exam, taken with a designated physician, is required."],
 ['You (the applicant)', "You must be outside Canada when you apply and be admissible. IRCC also assesses whether you are a genuine visitor who will leave Canada at the end of the visit (ties, purpose of the stay, family, finances)."],
])}
<div class="prose" style="margin-top:18px"><p>Since January 28, 2025, insurance issued by an insurer established abroad is accepted if it is authorized by OSFI. If a sponsorship application is in progress, you can apply for a super visa while waiting for the decision. After approval, the visa is printed by a visa office outside Canada: wait for its instructions.</p></div>
</div></section>
<section class="sp"><div class="wrap"><h2>How we support you</h2><div class="prose">
<p>We check with you which visa fits your situation, we review your child's or grandchild's income and family calculation, the invitation letter, the insurance and the supporting documents, then we prepare a complete file before filing. Any document that is not in French or English must be translated by a qualified translator.</p>
{LAWNOTE}</div><p><a class="btn" href="/en/visitor-visa-cost/">How much does it cost?</a> <a class="btn" href="/en/documents-checklist/">Documents checklist</a></p></div></section>''',
  faq=[("Do I need a visa to come to Canada?", "It depends on your nationality and your means of transport. IRCC offers a tool, \u201cFind out if you need a visa or an eTA\u201d: we check it with you."),
       ("What is the difference between the visitor visa and the super visa?", "The visitor visa suits most stays of 6 months or less. The super visa is reserved for parents and grandparents of a Canadian citizen or permanent resident and allows longer stays."),
       ("Does my child need a minimum income for my super visa?", "Yes. The host must meet the minimum necessary income set by IRCC according to family size, and prove it, for example with notices of assessment."),
       ("Is medical insurance mandatory?", "For the super visa, yes: at least 1 year of coverage from entry, with emergency coverage of at least $100,000. For the visitor visa, IRCC's list of requirements does not make it a requirement."),
       ("Does an invitation letter guarantee the visa?", "No. It is mandatory for the super visa and can be useful for a visitor visa, but the decision rests on the whole file."),
       ("Do you guarantee that I will get the visa?", "No. No serious consultant can guarantee a decision: it belongs solely to the Canadian authorities.")])

P(path='en/citizenship/', fr='citoyennete-canadienne/', ar='ar/canadian-citizenship/', title="Canadian citizenship: requirements for permanent residents | ATL Canada",
  desc="Becoming a Canadian citizen: 1,095 days of presence, taxes, language. The official requirements for adult permanent residents.",
  crumb="Canadian citizenship", eyebrow="Citizenship · Montréal · Casablanca", h1="Canadian citizenship: requirements for adults",
  lede="After permanent residence, citizenship is the next step for many families. Here are the official requirements to check before applying.",
  body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>Requirements for an adult (18 and over)</h2>
{rich(['Requirement', 'What IRCC says'], [
 ['Permanent resident status', "You must be a permanent resident with no unfulfilled condition, and your status must not be under immigration or fraud review or subject to a removal order."],
 ['Physical presence', "1,095 days in Canada as a permanent resident in the 5 years before applying. Time spent as a temporary resident or protected person before permanent residence counts as half a day, up to a maximum of 365 days. Time spent in prison, on probation or on parole in Canada generally does not count."],
 ['Taxes', "Having filed income tax returns for 3 tax years falling wholly or partly within the 5 years before applying."],
 ['Language', "People aged 18 to 54 must prove ability in French or English at CLB level 4 or higher. People aged 55 and over and 17 and under are exempt, as are deaf people who cannot provide proof. A waiver on humanitarian grounds is possible."],
])}
<p class="note" style="margin-top:18px">Other grounds can prevent an application, for example pending criminal charges, certain convictions, or a previous refusal or revocation of citizenship.</p>
</div></section>
<section class="sp"><div class="wrap"><h2>How we support you</h2><div class="prose">
<p>Before filing, we check with you the calculation of your days of presence, your tax returns and your language proof, and we prepare a complete application. The citizenship rules changed in 2025: we check with you what applies to your case, notably if you are the parent or child of a citizen.</p>
<p>If you are not yet a permanent resident, see our page on <a href="/en/permanent-residence/" style="text-decoration:underline">permanent residence</a>.</p>
{LAWNOTE}</div></div></section>''',
  faq=[("How many days must I have spent in Canada?", "1,095 days as a permanent resident in the 5 years before applying, with possible partial credit for time spent as a temporary resident or protected person before permanent residence."),
       ("Do I need to have paid taxes?", "Yes. You must have filed income tax returns for 3 tax years falling wholly or partly within the 5 years before applying."),
       ("What language level is required?", "People aged 18 to 54 must prove CLB level 4 or higher in French or English. People aged 55 and over are exempt."),
       ("Do you guarantee that I will get citizenship?", "No. No serious consultant can guarantee a decision: it belongs solely to IRCC.")])

P(path='en/permanent-residence/', fr='residence-permanente-canada/', ar='ar/permanent-residence/', title="Permanent residence in Canada: the possible routes | ATL Canada",
  desc="Which routes lead to permanent residence: Express Entry, provincial nominees, Quebec, family sponsorship, Atlantic. A regulated consultant helps you choose.",
  crumb="Permanent residence", eyebrow="Permanent residence · Montréal · Casablanca", h1="Permanent residence in Canada: which route to choose?",
  lede="There is not one single door to permanent residence, but several routes, each with its own rules. Here are the main ones and how to choose the most realistic for your profile.",
  body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>The main routes</h2>
{rich(['Route', 'In brief'], [
 ['Express Entry', "An online system that manages applications for three federal programs: Federal Skilled Worker, Federal Skilled Trades and the Canadian Experience Class. Candidates are ranked by points and the top-ranked are invited to apply.", '/en/express-entry/'],
 ['Provincial nominees', "Each province or territory nominates people it needs, under its own streams. Quebec and Nunavut do not have this program.", '/en/provincial-nominee/'],
 ['Quebec', "Quebec itself selects part of its economic immigrants (CSQ), then IRCC processes permanent residence.", '/en/immigrate-to-quebec/'],
 ['Family sponsorship', "A Canadian citizen or permanent resident can sponsor certain family members: spouse, dependent children, parents and grandparents.", '/en/family-sponsorship/'],
 ['Atlantic Immigration Program', "For skilled workers and recent graduates of an Atlantic institution, with a job offer from a designated employer in New Brunswick, Nova Scotia, Prince Edward Island or Newfoundland and Labrador."],
])}
</div></section>
<section class="sp"><div class="wrap"><h2>How to choose?</h2>
<ol class="steps">
<li><span>Take stock of your profile: age, education, work experience, French and English level, family in Canada.</span></li>
<li><span>Check whether you qualify for a federal Express Entry program, and where you might rank.</span></li>
<li><span>Look at the provincial and Quebec streams that match your occupation or your plan.</span></li>
<li><span>Prepare documents in advance (credential assessment, language tests, proof of experience): the time frame after an invitation is short.</span></li>
</ol>
<div class="prose" style="margin-top:22px"><p>For the detail of each route, see our pages on <a href="/en/express-entry/" style="text-decoration:underline">Express Entry</a>, <a href="/en/provincial-nominee/" style="text-decoration:underline">provincial nominees</a>, <a href="/en/immigrate-to-quebec/" style="text-decoration:underline">immigrating to Quebec</a> and <a href="/en/family-sponsorship/" style="text-decoration:underline">family sponsorship</a>. Once you are a permanent resident, see also <a href="/en/citizenship/" style="text-decoration:underline">Canadian citizenship</a>.</p></div>
</div></section>
<section class="sp alt"><div class="wrap"><h2>How we support you</h2><div class="prose">
<p>At the consultation, we compare the possible routes with you, identify the one that best fits your profile, then prepare a complete, consistent file before filing. Using an immigration professional gives no processing priority.</p>
<p class="note">The decision belongs solely to IRCC, the provinces or Quebec depending on the route: we cannot guarantee a result or promise a timeline.</p></div></div></section>''',
  faq=[("What is the best route to permanent residence?", "It depends on your profile: age, education, experience, languages, family in Canada, life plan. That is exactly what we analyze with you at the consultation."),
       ("Can I apply under several routes at once?", "In some cases yes, for example being in the Express Entry pool and obtaining a provincial nomination. We look with you at what is possible for your situation."),
       ("Do I need to be in Canada already?", "Not always. Some routes are for candidates living abroad, others require Canadian work experience, such as the Canadian Experience Class."),
       ("Does a consultant guarantee permanent residence?", "No. No serious consultant can guarantee a decision: it belongs solely to the Canadian and Quebec authorities.")])

P(path='en/provincial-nominee/', fr='candidats-provinces-canada/', ar='ar/provincial-nominee/', title="Provincial Nominee Program in Canada: how it works | ATL Canada",
  desc="The Provincial Nominee Program: two processes (Express Entry or not), each province's role, steps. A regulated consultant explains.",
  crumb="Provincial nominee", eyebrow="Provinces · Montréal · Casablanca", h1="Provincial Nominee Program",
  lede="Each province or territory can nominate people who have the skills it needs and want to settle there. Here is how this route to permanent residence works.",
  body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>What to know</h2>
{rich(['Point', 'What IRCC says'], [
 ['Who decides?', "Each province or territory sets its own criteria and streams, and the number of people it can nominate each year."],
 ['Where?', "You must plan to settle in the province or territory that nominates you. Quebec and Nunavut have no program: see our page on <a href=\"/en/immigrate-to-quebec/\" style=\"text-decoration:underline\">immigrating to Quebec</a>."],
 ['Two processes', "The Express Entry-linked process: you meet the criteria of a provincial stream and of a federal Express Entry program. The non-Express Entry process: you meet a provincial stream but not a federal Express Entry program."],
 ['After the nomination', "In the Express Entry-linked process, once nominated you create an Express Entry profile and receive 600 additional points, which helps you get invited to apply for permanent residence."],
])}
</div></section>
<section class="sp"><div class="wrap"><h2>The steps</h2>
<ol class="steps">
<li><span>Choose a province or territory and review its streams.</span></li>
<li><span>Identify your route: depending on whether you also qualify for a federal Express Entry program or not.</span></li>
<li><span>File your application following the province's procedure, which tells you whether it goes through Express Entry or not.</span></li>
<li><span>Once nominated, file your permanent residence application with IRCC, which checks admissibility (medical, security, criminality) among other things.</span></li>
</ol>
<div class="prose" style="margin-top:22px"><p>Timelines vary with the type of application, the completeness of the file and how fast you respond. See also the <a href="/en/permanent-residence/" style="text-decoration:underline">permanent residence</a> page to compare routes.</p></div>
</div></section>
<section class="sp alt"><div class="wrap"><h2>How we support you</h2><div class="prose">
<p>At the consultation, we look with you at which provinces match your occupation and plan, which route is the most realistic, and which documents to prepare in advance. Using an immigration professional gives no processing priority.</p>
<p class="note">The decision belongs solely to IRCC and the province concerned: we cannot guarantee a result or promise a timeline.</p></div></div></section>''',
  faq=[("Can I choose any province?", "Each province has its own streams and criteria. You must plan to settle in the province that nominates you. Quebec and Nunavut have no program."),
       ("What are the 600 additional points?", "In the Express Entry-linked process, a person nominated by a province receives 600 additional points once their profile is created. This helps them get invited to apply."),
       ("Does a nomination guarantee permanent residence?", "No. The nomination is a step. IRCC then decides on permanent residence."),
       ("What about the Atlantic Immigration Program?", "It is a separate program for skilled workers and recent graduates in the four Atlantic provinces, with a job offer from a designated employer.")])

P(path='en/immigrate-to-quebec/', fr='immigration-quebec-canada/', ar='ar/immigrate-to-quebec/', title="Immigrating to Quebec: Quebec selection, PSTQ, CSQ | ATL Canada",
  desc="Immigrating to Quebec: selection by Quebec (CSQ), the Skilled Worker Selection Program (PSTQ), the state of the PEQ. A regulated consultant explains the steps.",
  crumb="Immigrate to Quebec", eyebrow="Quebec · Montréal · Casablanca", h1="Immigrating to Quebec",
  lede="Quebec itself chooses part of its economic immigrants. Here is how this two-stage path works and where the main programs stand.",
  body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>A two-stage path</h2>
<ol class="steps">
<li><span>Selection by Quebec: the Quebec Ministry of Immigration reviews your file and, if favourable, issues a Quebec Selection Certificate (CSQ).</span></li>
<li><span>The permanent residence application: once you have the CSQ, you then file your application with IRCC, which checks admissibility (medical, security, criminality) among other things.</span></li>
</ol>
<div class="prose" style="margin-top:22px"><p>To study in Quebec, a provincial step is also added before the study permit: the CAQ. See our page on the <a href="/en/study-permit/" style="text-decoration:underline">study permit</a>.</p></div>
</div></section>
<section class="sp"><div class="wrap"><h2>Where do the programs stand?</h2>
{rich(['Program', 'What the Quebec government says'], [
 ['Skilled Worker Selection Program (PSTQ)', "You first declare your interest. If you are invited, you must accept the invitation within 30 days, otherwise your declaration becomes void. You then file your permanent selection application with the required documents, within 60 days of acceptance for most streams (a different deadline applies to one specific stream). Quebec then examines the file and issues the CSQ if favourable."],
 ["Quebec Experience Program (PEQ)", "For temporary foreign workers and international graduates of a Quebec institution. Applications were accepted from July 2, 2026 and the intake period has been closed since October 31, 2026. No decision has been announced on a future intake period."],
])}
<p class="note" style="margin-top:18px">These programs change often: the state shown is that of November 5, 2026. Before any decision, check their current status with us.</p>
</div></section>
<section class="sp alt"><div class="wrap"><h2>How we support you</h2><div class="prose">
<p>At the consultation, we look with you at whether your profile fits a Quebec selection path or a federal route such as Express Entry, which documents to prepare and in what order to act. The time frame after an invitation is short: preparing your file in advance often makes the difference. Using an immigration professional gives no processing priority.</p>
<p>If you speak French well, see also our page on <a href="/en/express-entry-french/" style="text-decoration:underline">Express Entry for French speakers</a>.</p>
<p class="note">The decision belongs solely to the Quebec authorities and IRCC: we cannot guarantee a result or promise a timeline.</p></div></div></section>''',
  faq=[("What is the difference between the CSQ and permanent residence?", "The CSQ is the selection made by Quebec. Permanent residence is then granted by IRCC, based on the application you file after obtaining the CSQ."),
       ("Is the PEQ still open?", "As of November 5, 2026, the Quebec government states that the intake period has been closed since October 31, 2026 and that no decision has been made on a next period."),
       ("How does a PSTQ invitation work?", "You first declare your interest. If you are invited, you must accept within 30 days, then file your permanent selection application within the deadlines stated in the invitation."),
       ("Do I need to speak French to immigrate to Quebec?", "French weighs heavily in Quebec selection. We look with you at what applies to your profile at the consultation."),
       ("Do you guarantee the CSQ or permanent residence?", "No. No serious consultant can guarantee a decision: it belongs solely to the Quebec and Canadian authorities.")])

P(path='en/business-immigration/', fr='gens-affaires-immigration-canada/', ar='ar/business-immigration/', title="Business immigration to Canada and Quebec: where the programs stand | ATL Canada",
  desc="Start-up visa, self-employed persons, Quebec business programs: the official state of the programs and other possible routes. A regulated consultant helps you choose.",
  crumb="Business immigration", eyebrow="Business · Montréal · Casablanca", h1="Business immigration: where do the programs stand?",
  lede="Immigration programs for entrepreneurs and investors change a lot. Here is the state indicated by the Canadian and Quebec governments, and the other routes to consider.",
  body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>At the federal level</h2>
{rich(['Program', 'What IRCC says'], [
 ["Start-up Visa", "IRCC stopped accepting new applications on December 31, 2025, except for people who had received a valid commitment from a designated organization in 2025. The program page also shows a deadline of June 30, 2026 for those people: check the current status before acting. The business must be located outside Quebec."],
 ['Self-employed persons', "The pause on receiving applications is extended \u201cuntil further notice\u201d."],
 ['What next?', "IRCC plans to replace these programs with a new targeted pilot program for immigrant entrepreneurs. Details are due to be published in 2026."],
])}
</div></section>
<section class="sp"><div class="wrap"><h2>In Quebec</h2><div class="prose">
<p>Quebec itself chooses the business people who settle there: you must first obtain a Quebec Selection Certificate (CSQ), then IRCC processes permanent residence. Since January 1, 2024, the reform of the investor, entrepreneur and self-employed programs notably requires satisfactory knowledge of French to settle in Quebec. See also our page on <a href="/en/immigrate-to-quebec/" style="text-decoration:underline">immigrating to Quebec</a>.</p>
</div></div></section>
<section class="sp alt"><div class="wrap"><h2>Other routes to consider</h2>
{rich(['Route', 'In brief'], [
 ['Work permit', "Depending on your situation, a work permit may let you work in Canada.", '/en/work-permit/'],
 ["Express Entry", "If your skilled worker profile allows it, this is often a more realistic route.", '/en/express-entry/'],
 ['Provincial nominees', "Each province sets its own streams and criteria.", '/en/provincial-nominee/'],
])}
</div></section>
<section class="sp"><div class="wrap"><h2>How we support you</h2><div class="prose">
<p>At the consultation, we review your plan, check the current state of the programs before you spend anything, and compare the realistic routes for your profile. Using an immigration professional gives no processing priority.</p>
<p class="note">The decision belongs solely to IRCC and the Quebec authorities: we cannot guarantee a result or promise a timeline.</p></div></div></section>''',
  faq=[("Is the Start-up Visa still open?", "According to IRCC, new applications have no longer been accepted since December 31, 2025, except for people who had received a valid commitment in 2025. Check the current status with us."),
       ("Is the self-employed program open?", "According to IRCC, receipt of applications is paused until further notice."),
       ("What will replace these programs?", "IRCC plans a new targeted pilot program for immigrant entrepreneurs, with details due to be published in 2026."),
       ("Do I need to speak French to immigrate to Quebec as a business person?", "Yes: since the reform of January 1, 2024, satisfactory knowledge of French is required to settle in Quebec as an investor, entrepreneur or self-employed person."),
       ("Do you guarantee a result?", "No. No serious consultant can guarantee a decision: it belongs solely to the Canadian and Quebec authorities.")])

P(path='en/express-entry-french/', fr='entree-express-francophone-maroc/', ar='ar/express-entry-french/', title="Express Entry for French speakers: French is an asset | ATL Canada",
  desc="French can earn up to 50 points in Express Entry. Required level, tests, draws: a regulated consultant explains. Book a consultation.",
  crumb="Express Entry for French speakers", eyebrow="Permanent residence · Montréal · Casablanca", h1="Express Entry: French is an asset for candidates",
  lede="A good level of French can earn up to 50 additional points in Express Entry and gives access to draws reserved for French speakers. Here is how it works and what to prepare.",
  body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>How French counts in your score</h2>
<div class="prose"><p>If you reach at least CLB 7 in all four French skills (listening, reading, speaking, writing), you receive additional points, even if French is your second language.</p></div>
{tbl([('CLB 7 or more in all 4 skills / CLB 4 or less, or no English test', '+ 25 points'), ('CLB 7 or more in all 4 skills / CLB 5 or more in all 4 skills', '+ 50 points')], ('Your French / your English', 'Additional points'))}
<p class="note">These points are added to your score, but never guarantee an invitation.</p>
</div></section>
<section class="sp"><div class="wrap"><h2>The three Express Entry programs</h2><div class="cards">
<div class="card"><h3>Federal Skilled Worker</h3><p>For candidates with skilled work experience abroad or in Canada.</p></div>
<div class="card"><h3>Federal Skilled Trades</h3><p>For people qualified in a recognized skilled trade.</p></div>
<div class="card"><h3>Canadian Experience Class</h3><p>For those who have already worked in Canada, for example after studies.</p></div>
</div>
<div class="prose" style="margin-top:22px"><p>IRCC also invites candidates by category, including one dedicated to French proficiency. The cut-offs change with each draw: follow them in our <a href="/actualites/" style="text-decoration:underline">news</a> (in French), for example the <a href="/actualites/#express-entree-tirage-francais-16-octobre-2026" style="text-decoration:underline">French-language draw of October 16, 2026</a>.</p></div></div></section>
<section class="sp alt"><div class="wrap"><h2>What to prepare</h2>
<ol class="steps">
<li><span>Take a French test approved by IRCC (TEF Canada or TCF Canada) and, if possible, an English test: both languages influence your points.</span></li>
<li><span>Have your foreign credentials assessed by a designated organization, if you want them to count in the score.</span></li>
<li><span>Create your online profile with your personal reference code. Documents are uploaded only after an invitation.</span></li>
<li><span>After the invitation, you have 60 days to submit your permanent residence application.</span></li>
<li><span>Prepare your Moroccan documents, including the police certificate: see our page on <a href="/en/moroccan-documents/" style="text-decoration:underline">Moroccan documents</a>.</span></li>
</ol>
<div class="prose" style="margin-top:22px"><p>A nomination by a provincial nominee program also adds points. And if your score is too low, a Francophone Mobility work permit can help some candidates gain experience in Canada, subject to IRCC's conditions.</p></div>
</div></section>''',
  faq=[("What French level is needed?", "CLB 7 in all four skills gives access to the additional points and to the French-language category. A test approved by IRCC (TEF Canada or TCF Canada) is required."),
       ("What score is needed to be invited?", "There is no fixed cut-off: each draw has its own minimum score. The latest results are published by IRCC and summarized in our news."),
       ("Do I have to use a consultant?", "No, you can create your profile and file yourself. A regulated consultant helps you check your eligibility, optimize your score honestly and prepare a complete file within the 60-day deadline."),
       ("Is French enough to be invited?", "No. You must also meet the requirements of one of the three programs and be among the top scores in the pool. An invitation is never guaranteed."),
       ("Do you guarantee an invitation or permanent residence?", "No. Decisions belong solely to IRCC. Our role is to choose the right strategy and prepare a rigorous file.")])

P(path='en/moroccan-documents/', fr='documents-maroc-immigration-canada/', ar='ar/moroccan-documents/', title="Moroccan documents for immigrating to Canada | ATL Canada",
  desc="Moroccan police certificate (fiche anthropom\u00e9trique), VFS biometrics, documents not to be confused: what IRCC accepts. A regulated consultant guides you.",
  crumb="Moroccan documents", eyebrow="File · Montréal · Casablanca", h1="Moroccan documents for your Canadian immigration application",
  lede="The Moroccan police certificate is one of the documents that most often make candidates hesitate. Here is what IRCC asks of Moroccan citizens, according to its official pages.",
  body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>The Moroccan police certificate</h2>
<div class="prose"><p>A permanent residence application requires a police certificate. For Moroccan citizens, the document is called the <strong>fiche anthropom\u00e9trique</strong>. The fingerprints taken for this certificate are separate from the biometrics you give with your application.</p></div>
{rich(['Your situation', 'What IRCC says'], [
 ['Moroccan citizen living in Morocco', "Go to the police station of your place of residence with your national identity card. You may appoint a representative, who must present their own national card."],
 ['Moroccan citizen living abroad', "Contact the nearest Moroccan embassy or consulate, or go through the local police station by proxy (not through the central service in Rabat). The proxy requires a notarized power of attorney, copies of the birth certificate and passport, and a fee."],
 ['Language of the document', "The certificate is issued in French and Arabic: no translation is needed."],
 ['Not to be confused', "The \u201cBulletin No. 3\u201d issued by the court of first instance to Moroccans is not accepted for immigration: it covers only offences committed in the city of residence."],
 ['Period of validity', "The official pages do not specify it: call us, we check it with you before you file your application, so you do not lose time."],
])}
</div></section>
<section class="sp"><div class="wrap"><h2>Biometrics and the VFS Global centre</h2><div class="prose">
<p>IRCC has authorized VFS Global to receive visa, study permit and work permit applications in Morocco and to record your fingerprints and photo. Recording is by appointment only, booked online.</p>
<p>A temporary resident gives biometrics only once every 10 years. A permanent residence applicant must provide them with each application. Check your case on the IRCC website.</p>
</div></div></section>
<section class="sp alt"><div class="wrap"><h2>The other usual documents</h2><div class="prose">
<p>The exact list depends on your application and is set by IRCC for your situation. It generally includes the passport, birth certificate, diplomas and transcripts, language test results and proof of funds or work experience.</p>
<p>Any document that is not in French or English must be accompanied by a translation. We check each document with you before filing, so that none delays your case.</p></div></div></section>''',
  faq=[("What is the police certificate called for Moroccans?", "For Moroccan citizens, IRCC refers to the \u201cfiche anthropom\u00e9trique\u201d. It is issued by the police."),
       ("Is the Bulletin No. 3 accepted?", "No, not when obtained from the court of first instance by a Moroccan citizen: IRCC has ruled it out because it covers only the city of residence."),
       ("Can someone request the fiche anthropom\u00e9trique on the candidate's behalf?", "Yes, IRCC states that a representative can request it, provided they present their own national identity card."),
       ("Does the fiche anthropom\u00e9trique need to be translated?", "No, it is issued in French and Arabic, so IRCC does not require a translation."),
       ("For which applications is a police certificate needed?", "For a permanent residence application, it is required. For other applications, it depends on the case: we check it during the consultation.")])

P(path='en/study-permit-cost/', fr='cout-permis-etudes-canada/', ar='ar/study-permit-cost/', title="How much does a study permit for Canada cost? | ATL Canada",
  desc="Government fees, biometrics and our starting fees for a Canadian study permit, with what is not included. Up to date as of November 24, 2026.",
  crumb="Study permit cost", eyebrow="Budget · up to date as of November 24, 2026", h1="How much does a study permit for Canada cost?",
  lede="The cost of the application has two separate parts: the government fees and our fees. Here is the breakdown, with no surprises.",
  body=f'''{TRUST}
<section class="sp"><div class="wrap"><h2>The cost of the application</h2>
<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Item</th><th>Amount</th></tr></thead><tbody><tr><td>Government fee: study permit (extension included)</td><td class="num">$150</td></tr><tr><td>Biometrics, per person (if required)</td><td class="num">$85</td></tr><tr><td>Our fees, starting from</td><td class="num">$900</td></tr></tbody></table></div>
<p class="note">Starting total for one person: about $1,135 (900 + 150 + 85), taxes on our fees extra. Biometrics are not requested from everyone. All amounts in CAD.</p></div></section>
<section class="sp alt"><div class="wrap"><h2>What is not included</h2><div class="prose"><ul><li>Tuition and housing, paid to the institution and on site.</li><li>Language tests, translations and the medical exam, if requested.</li><li>To study in Quebec, the Quebec procedures and fees linked to the Quebec Acceptance Certificate (CAQ).</li></ul>
<p>For an estimate adapted to your situation, use the <a href="/en/budget-calculator/">budget calculator</a>. The final price is set after the consultation.</p>
<p><a class="btn btn-solid" href="/en/book-consultation/">Book a consultation</a> <a class="btn" href="/en/budget-calculator/">Calculate my budget</a> <a class="btn" href="/en/study-permit/">Study permit</a></p></div></div></section>''',
  faq=[("Is the fee different to extend a study permit?", "The $150 fee includes extensions: it also applies to an extension application."),
       ("Are the fees refunded if the application is refused?", "As a general rule, no. Processing fees are paid when you file. The exact conditions are on IRCC's official page."),
       ("Are your fees included in the $150?", "No. The $150 is the government fee. Our fees are separate and shown in <a href=\"/en/fees/\">our fee schedule</a>.")])

P(path='en/visitor-visa-cost/', fr='cout-visa-visiteur-canada/', ar='ar/visitor-visa-cost/', title="How much does a visitor visa or super visa for Canada cost? | ATL Canada",
  desc="Government fees, biometrics and our starting fees for a visitor visa or a super visa. Up to date as of November 24, 2026.",
  crumb="Visitor visa cost", eyebrow="Budget · up to date as of November 24, 2026", h1="How much does a visitor visa or super visa cost?",
  lede="The government fees and our fees are two separate amounts. Here is what the application costs, person by person.",
  body=f'''{TRUST}
<section class="sp"><div class="wrap"><h2>The cost of the application</h2>
<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Item</th><th>Amount</th></tr></thead><tbody><tr><td>Government fee: visitor visa, per person</td><td class="num">$100</td></tr><tr><td>Government fee: super visa</td><td class="num">$100</td></tr><tr><td>Biometrics, per person (if required)</td><td class="num">$85</td></tr><tr><td>Our fees: visitor visa, starting from</td><td class="num">$450</td></tr><tr><td>Our fees: super visa, starting from</td><td class="num">$800</td></tr></tbody></table></div>
<p class="note">Visitor visa, one person: about $635 (450 + 100 + 85). Super visa, one applicant: about $985 (800 + 100 + 85). Taxes on our fees extra. All amounts in CAD.</p></div></section>
<section class="sp alt"><div class="wrap"><h2>What is not included</h2><div class="prose"><ul><li>The plane ticket and living costs during the stay.</li><li>For the super visa, the mandatory medical insurance, bought separately.</li><li>Translations and the medical exam, if requested.</li></ul>
<p>For an estimate adapted to your situation, use the <a href="/en/budget-calculator/">budget calculator</a>.</p>
<p><a class="btn btn-solid" href="/en/book-consultation/">Book a consultation</a> <a class="btn" href="/en/budget-calculator/">Calculate my budget</a> <a class="btn" href="/en/visitor-visa/">Visitor visa and super visa</a></p></div></div></section>''',
  faq=[("Does a family pay less?", "Yes. The government fee for a visitor visa is capped at $500 for a family, and biometrics are capped at $170 per family."),
       ("Is super visa insurance included?", "No. It is mandatory for the super visa and bought separately."),
       ("Are the fees refunded if the application is refused?", "As a general rule, no. Processing fees are paid when you file.")])

P(path='en/documents-checklist/', fr='documents-a-preparer-immigration-canada/', ar='ar/documents-checklist/', title="Documents to prepare for a Canadian immigration application | ATL Canada",
  desc="A checklist of documents to prepare for a study permit, visitor visa, work permit or spousal sponsorship. Indicative list.",
  crumb="Documents to prepare", eyebrow="Checklist · indicative", h1="Documents to prepare before your consultation",
  lede="Tick what you already have. It makes the consultation more useful and speeds up the preparation of your application.",
  body=f'''{TRUST}
<section class="sp"><div class="wrap">
<p class="note">Indicative list: every case is different. The official list that comes with your application prevails, and we tell you at the consultation which documents to add.</p>
<h3>For every case</h3><ul class="chk"><li><label><input type="checkbox"> <span>Valid passport (copy of every used page)</span></label></li><li><label><input type="checkbox"> <span>Recent photo meeting the requirements</span></label></li><li><label><input type="checkbox"> <span>ID card and birth certificate</span></label></li><li><label><input type="checkbox"> <span>Proof of your current situation (job, studies or other)</span></label></li><li><label><input type="checkbox"> <span>Proof of funds (recent bank statements)</span></label></li></ul><h3>Study permit</h3><ul class="chk"><li><label><input type="checkbox"> <span>Letter of acceptance from a designated learning institution</span></label></li><li><label><input type="checkbox"> <span>Quebec Acceptance Certificate (CAQ), if you will study in Quebec</span></label></li><li><label><input type="checkbox"> <span>Diplomas and transcripts</span></label></li><li><label><input type="checkbox"> <span>Language test results, if requested</span></label></li><li><label><input type="checkbox"> <span>Letter explaining your study plan</span></label></li></ul><h3>Visitor visa</h3><ul class="chk"><li><label><input type="checkbox"> <span>Itinerary and purpose of the trip</span></label></li><li><label><input type="checkbox"> <span>Letter of invitation, if you are invited</span></label></li><li><label><input type="checkbox"> <span>Proof of your ties (job, family, property)</span></label></li><li><label><input type="checkbox"> <span>Travel history (previous visas and stamps)</span></label></li></ul><h3>Work permit (extension)</h3><ul class="chk"><li><label><input type="checkbox"> <span>Current work permit</span></label></li><li><label><input type="checkbox"> <span>Job offer or employment contract</span></label></li><li><label><input type="checkbox"> <span>Recent pay stubs</span></label></li><li><label><input type="checkbox"> <span>Proof of valid status in Canada</span></label></li></ul><h3>Sponsoring a spouse or partner</h3><ul class="chk"><li><label><input type="checkbox"> <span>Marriage certificate or proof of the relationship</span></label></li><li><label><input type="checkbox"> <span>ID documents of both spouses</span></label></li><li><label><input type="checkbox"> <span>Evidence of the relationship (photos, messages, trips)</span></label></li><li><label><input type="checkbox"> <span>Proof of the sponsor's status (permanent resident or citizen)</span></label></li><li><label><input type="checkbox"> <span>Police certificates and medical exam, if requested</span></label></li></ul>
<p><button type="button" class="btn" onclick="window.print()">Print the list</button> <a class="btn btn-solid" href="/en/book-consultation/">Book a consultation</a></p></div></section>''',
  faq=[("Do I need everything before the consultation?", "No. Bring what you have: we tell you what is missing and in which order to gather it."),
       ("Do I have to translate my documents?", "Documents that are neither in French nor in English generally need an accompanying translation. We tell you what applies to your case."),
       ("Where can I find the official list?", "On IRCC's website (canada.ca), in the application guide for the relevant program.")])

P(path='en/refused-application/', fr='demande-refusee-immigration-canada/', ar='ar/refused-application/', title="Canadian immigration application refused: what to do | ATL Canada",
  desc="Application refused or procedural fairness letter received? The first things to do, the deadlines to watch and how a consultant can help.",
  crumb="Refused application", eyebrow="Refusal · procedural fairness letter", h1="Your application was refused: what to do",
  lede="A refusal is not always the end of the road, but the first days matter. Here are the first steps, with no promises.",
  body=f'''{TRUST}
<section class="sp"><div class="wrap"><h2>The first steps</h2>
<ol class="steps"><li><span><b>Read the whole letter.</b> It gives the reasons for the refusal and sometimes a deadline to respond.</span></li><li><span><b>Note the dates.</b> A procedural fairness letter sets a deadline to answer: do not let it pass.</span></li><li><span><b>Do not refile too fast.</b> An identical new application with the same weaknesses may be refused again.</span></li><li><span><b>Have the file analyzed.</b> We compare the reasons for the refusal with your situation and documents.</span></li><li><span><b>Choose what comes next.</b> Respond to the letter, refile a better-prepared application, or look at other routes.</span></li></ol></div></section>
<section class="sp alt"><div class="wrap"><h2>What we can do, and what we do not promise</h2><div class="prose">
<p>At the consultation, we read the letter, identify what may have caused the problem and tell you honestly which options are realistic. In some cases a Federal Court challenge exists, with very short deadlines: a lawyer is then needed, and we tell you so.</p>
<p>We do not guarantee that a new application will be accepted: the decision belongs solely to IRCC and the Quebec authorities.</p>
<p><a class="btn btn-solid" href="/en/book-consultation/">Book a consultation</a> <a class="btn" href="/en/evaluate-my-case/">Assess my case</a></p></div></div></section>''',
  faq=[("What is a procedural fairness letter?", "It is a letter informing you of a concern of the officer and giving you the chance to respond before the decision. It contains a deadline."),
       ("How long do I have to react?", "It depends on the letter and the decision. Deadlines are stated in the letter or the instructions that come with it, and they can be short."),
       ("Can I file my application again?", "Often yes, but what caused the refusal must be corrected. That is what we analyze with you."),
       ("Is a court challenge possible?", "In some cases, before the Federal Court, with very short deadlines. That remedy is a matter for a lawyer.")])

P(path='en/whats-changing/', fr='ce-qui-change-immigration-canada/', ar='ar/whats-changing/', title="What is changing in Canadian immigration | ATL Canada",
  desc="Recent changes to Canadian immigration fees and rules, and where to follow the news. Last checked on November 24, 2026.",
  crumb="What is changing", eyebrow="Fees and rules · checked November 24, 2026", h1="What is changing in Canadian immigration",
  lede="A quick look at what has changed recently in fees, and where to follow the rest day by day.",
  body=f'''{TRUST}
<section class="sp"><div class="wrap"><h2>Government fees</h2><div class="prose">
<p>IRCC fees were last changed on April 30, 2026. At the date of our check (November 24, 2026), no change is announced for 2027 on the official fees page.</p>
<p>See the up-to-date list on our <a href="/en/official-fees/">Official fees</a> page.</p></div></div></section>
<section class="sp alt"><div class="wrap"><h2>Following the news</h2><div class="prose">
<p>Express Entry draws, provincial news and IRCC announcements are summarized in our <a href="/actualites/">news section</a> (in French), updated every day.</p>
<p>Does a change concern you? <a class="btn btn-solid" href="/en/book-consultation/">Book a consultation</a> <a class="btn" href="/actualites/">See the news (in French)</a></p></div></div></section>''',
  faq=[("Can fees change without notice?", "IRCC generally announces fee changes in advance on its website. We update our page at every check."),
       ("Where can I find the latest Express Entry draws?", "In our news section (in French), updated every day.")])

P(path='en/evaluate-my-case/', fr='evaluer-mon-dossier/', ar='ar/evaluate-my-case/', title="Assess my case in 5 questions | ATL Canada",
  desc="Answer five simple questions to find out which immigration route to look at first. Free, takes one minute, nothing is sent or saved.",
  crumb="Assess my case", eyebrow="Free tool · 1 minute", h1="Assess my case in 5 questions",
  lede="Answer five simple questions to find out which immigration route to look at first. The result is general guidance: your answers are neither sent nor saved.",
  body=f'''{TRUST}
<section class="sp"><div class="wrap">
<link rel="stylesheet" href="/assets/eval.css">
<div id="eval-app" data-lang="en"></div>
<noscript><p class="note">This questionnaire needs JavaScript. You can also call us at +1 514 295 6635.</p></noscript>
<script src="/assets/eval.js" defer></script>
</div></section>
<section class="sp alt"><div class="wrap"><h2>Why a consultation afterwards?</h2><div class="prose">
<p>This questionnaire does not replace a consultant's analysis. Every case has its particulars: current status, application history, documents, deadlines. At the consultation, we check the current state of the programs and compare the realistic routes for your profile.</p>
<p class="note">The decision belongs solely to IRCC and the Quebec authorities: we cannot guarantee a result or promise a timeline.</p></div></div></section>''',
  faq=[("Is this questionnaire an official assessment?", "No. It is general guidance pointing you to the most useful page. Only a full analysis of your case allows a route to be chosen."),
       ("Are my answers saved?", "No. Everything happens in your browser and nothing is sent to ATL Canada."),
       ("Is the service reserved for candidates from Morocco?", "No. We also support people of other nationalities and people already in Canada, for example to extend a work permit."),
       ("Can you tell me my chances of being accepted?", "Nobody can guarantee a decision. At the consultation, we tell you honestly which routes are realistic for your profile.")])

def head_for(p):
    url = SITE + '/' + p['path']
    h = head_ref
    h = re.sub(r'<title>.*?</title>', '<title>%s</title>' % e(p['title']), h, flags=re.S)
    h = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + e(p['desc'], quote=True) + m.group(2), h)
    for tag in ('og:title', 'twitter:title'):
        h = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*(")' % tag, lambda m: m.group(1) + e(p['title'], quote=True) + m.group(2), h)
    for tag in ('og:description', 'twitter:description'):
        h = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*(")' % tag, lambda m: m.group(1) + e(p['desc'], quote=True) + m.group(2), h)
    h = re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), h)
    h = re.sub(r'(<meta property="og:locale" content=")[^"]*(")', lambda m: m.group(1) + 'en_CA' + m.group(2), h)
    h = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), h)
    h = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', '', h)
    fr = SITE + '/' + p['fr'].lstrip('/')
    alt = f'<link rel="alternate" hreflang="fr" href="{fr}">\n<link rel="alternate" hreflang="ar" href="{SITE}/{p["ar"]}">\n<link rel="alternate" hreflang="en" href="{url}">\n<link rel="alternate" hreflang="x-default" href="{fr}">\n'
    h = re.sub(r'(<link rel="canonical" href="[^"]*">\n?)', lambda m: m.group(1) + alt, h, count=1)
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    g = json.loads(m.group(1))
    keep = [n for n in g['@graph'] if n['@type'] in ('ProfessionalService', 'WebSite')]
    crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/en/"}]
    if p['crumb']: crumbs.append({"@type": "ListItem", "position": 2, "name": p['crumb'], "item": url})
    keep += [{"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": p['title'], "description": p['desc'], "inLanguage": "en", "dateModified": "2026-11-24", "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#organization"}},
             {"@type": "BreadcrumbList", "itemListElement": crumbs},
             {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": "en", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a_)}} for q, a_ in p['faq']]}]
    g['@graph'] = keep
    h = h[:m.start()] + '<script type="application/ld+json">' + json.dumps(g, ensure_ascii=False) + '</script>' + h[m.end():]
    h = h.replace('<link rel="stylesheet" href="/assets/news.css">', '<link rel="stylesheet" href="/assets/news.css">\n' + EXTRA_CSS, 1) if '<link rel="stylesheet" href="/assets/news.css">' in h else h + EXTRA_CSS
    return h

for p in PAGES:
    crumb = '<p class="crumb"><a href="/en/">Home</a> › %s</p>' % e(p['crumb']) if p['crumb'] else ''
    page = f'''{head_for(p)}</head>
{topbar}<main>
<section class="pg-hero"><div class="wrap">
  {crumb}
  <p class="eyebrow">{e(p['eyebrow'])}</p>
  <h1>{e(p['h1'])}</h1>
  <p class="lede">{e(p['lede'])}</p>
</div></section>
{p['body'].replace(TRUST, '', 1)}
{TRUST}
<section class="sp alt" id="faq"><div class="wrap"><h2>Frequently asked questions</h2><div class="faq-list">{faq_html(p['faq'])}</div></div></section>
<section class="sp"><div class="wrap"><p class="note">Last updated: November 24, 2026.</p></div></section>
{offices}
{footer}'''
    os.makedirs(R + p['path'], exist_ok=True)
    open(R + p['path'] + 'index.html', 'w', encoding='utf-8').write(page)
    print('ok', p['path'], len(page), 'octets')
