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
    '<footer><div class="wrap"><p style="margin:0 0 12px;font-size:.9rem"><a href="/en/">Home</a> · <a href="/en/fees/">Fees</a> · <a href="/en/official-fees/">Official fees</a> · <a href="/en/study-permit/">Study permit</a> · <a href="/en/work-permit/">Work permit</a> · <a href="/en/express-entry/">Express Entry</a> · <a href="/en/budget-calculator/">Budget calculator</a> · <a href="/en/book-consultation/">Book a consultation</a> · <a href="/en/case-process/">How a case works</a> · <a href="/en/about/">About</a> · <a href="/">Français</a> · <a href="/ar/" lang="ar">العربية</a></p><div class="footer-bottom"><a href="/confidentialite/" style="color:inherit">Privacy (French)</a> <span>© 2026 ATL Canada</span><span>Regulated Canadian immigration consultant (RCIC), licence <a class="ccic-link" href="https://registre.college-ic.ca/Public-Register-FR/Licensee/Profile.aspx?ID=10629" target="_blank" rel="noopener">R712906</a> with the CICC.</span></div></div></footer>',
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
    return '<div class="info-grid">' + ''.join('<div class="info"><h3>%s</h3><p>%s</p></div>' % (r[0], r[1]) for r in rows) + '</div>'

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
<p>Read more: <a href="/en/study-permit/">study permit</a>, <a href="/en/work-permit/">work permit</a> and <a href="/en/express-entry/">Express Entry</a>. Other service pages are currently available in <a href="/">French</a> and <a href="/ar/" lang="ar">Arabic</a>.</p>
<p><a class="btn btn-solid" href="/en/book-consultation/">Book a consultation</a> <a class="btn" href="/en/case-process/">How a case works</a> <a class="btn" href="/en/about/">About us</a></p></div></div></section>''',
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
<p class="note">No result is guaranteed: the decision belongs solely to IRCC and the Quebec authorities.</p></div></div></section>''',
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
<p><a class="btn btn-solid" href="/en/book-consultation/">Book a consultation</a> <a class="btn" href="/en/fees/">Our fees</a></p></div></div></section>''',
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
<p>See also <a href="/en/express-entry/" style="text-decoration:underline">our Express Entry page</a> and <a href="/en/work-permit/" style="text-decoration:underline">work permits</a>.</p></div></div></section>''',
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
