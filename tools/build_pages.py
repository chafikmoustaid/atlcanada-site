#!/usr/bin/env python3
"""Génère les pages de service en français pour les candidats du Maroc
(permis d'études, Entrée express francophone, documents marocains).
Reprend l'en-tête, la barre du haut et le pied de page de /maroc/index.html.
Usage : python3 tools/build_pages.py   (depuis la racine du dépôt)"""
import json, re, html, os

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
SITE = 'https://www.atlcanada.com'
e = html.escape
UPDATED = '2026-10-26'

ref = open(R + 'maroc/index.html', encoding='utf-8').read()
head_ref = ref[:ref.index('</head>')]
topbar = ref[ref.index('<body>'):ref.index('<main>')]
topbar = topbar.replace('<a href="/#services">Services</a><a href="#faq">Questions</a><a href="#bureaux">Bureaux</a>',
                        '<a href="/#services">Services</a><a href="/maroc/">Depuis le Maroc</a><a href="#faq">Questions</a><a href="#bureaux">Bureaux</a>')
topbar = topbar.replace('href="/ar/" lang="ar" hreflang="ar"', 'href="/ar/" lang="ar" hreflang="ar"')
footer = ref[ref.index('</main>'):]
offices = re.search(r'<section class="sp" id="bureaux">.*?</section>', ref, re.S).group(0)

EXTRA_CSS = """<style>
.tbl-wrap{overflow-x:auto;margin:0 0 8px}
.tbl{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line)}
.tbl th,.tbl td{padding:14px 16px;text-align:start;vertical-align:top;border-bottom:1px solid var(--line);font-size:1rem}
.tbl th{background:var(--paper-dim);color:var(--ink);font-weight:600}
.tbl td{color:var(--ink-soft)}
.tbl a{color:var(--ink);text-decoration:underline}
.steps{max-width:none}.prose{max-width:72ch}.prose p{margin:0 0 14px;color:var(--ink-soft)}
.sources{margin:0;padding-inline-start:20px;color:var(--ink-soft)}.sources li{margin:0 0 8px}
.sources a{color:var(--ink);text-decoration:underline}
.related{display:flex;gap:14px;flex-wrap:wrap;margin:22px 0 0}
</style>
"""

LAW = "Les informations de cette page sont générales et ne remplacent pas une évaluation personnalisée. Les règles d'immigration changent souvent : contactez-nous ou appelez-nous pour une évaluation de votre situation. Aucun résultat n'est garanti."

def table(headers, rows):
    th = ''.join(f'<th scope="col">{e(h)}</th>' for h in headers)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="tbl-wrap"><table class="tbl"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'

def a(url, label):
    return f'<a href="{e(url, quote=True)}" rel="noopener" target="_blank">{e(label)}</a>'

def faq_html(items):
    out = ''
    for i, (q, ans) in enumerate(items):
        out += f'<details class="faq-item"{" open" if i == 0 else ""}><summary>{e(q)}</summary><p>{ans}</p></details>'
    return out

def strip(s):
    return re.sub(r'<[^>]+>', '', html.unescape(s))

TRUST = ('<section class="sp"><div class="wrap"><div class="trustbox"><h2>Un consultant réglementé, pas un intermédiaire</h2>'
         "<p>ATL Canada est dirigé par un consultant réglementé en immigration canadienne (CRIC), membre du Collège des consultants en immigration et en citoyenneté (CCIC), permis R712906. Le permis se vérifie dans le registre public du CCIC.</p></div></div></section>")

PAGES = []

# ------------------------------------------------------------------ 1. Permis d'études
PAGES.append(dict(
    path='permis-etudes-canada-maroc/',
    title="Permis d'études Canada depuis le Maroc | ATL Canada",
    desc="Étudier au Canada depuis le Maroc : lettre d'attestation, preuves de fonds, biométrie et dépôt. Un consultant réglementé vous accompagne. Prenez rendez-vous.",
    crumb="Permis d'études depuis le Maroc",
    eyebrow="Études · Casablanca · Montréal",
    h1="Permis d'études pour le Canada depuis le Maroc",
    lede="Les citoyens marocains doivent obtenir un permis d'études avant de partir. Voici les étapes, les pièces à préparer et les points où un dossier se joue, avec un consultant réglementé à Casablanca.",
    body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>Les étapes, de l'admission au départ</h2>
<ol class="steps">
<li><span>Choisir un programme dans un établissement d'enseignement désigné : le permis d'études ne s'obtient que pour étudier dans un tel établissement.</span></li>
<li><span>Obtenir la lettre d'admission et, lorsqu'elle est exigée, la lettre d'attestation provinciale ou territoriale (LAP/LAT).</span></li>
<li><span>Réunir les preuves de fonds : frais de scolarité de la première année, frais de subsistance et frais de transport.</span></li>
<li><span>Déposer la demande en ligne auprès d'IRCC, puis donner vos données biométriques au centre VFS Global du Maroc.</span></li>
<li><span>Répondre aux demandes d'IRCC jusqu'à la décision, puis préparer votre arrivée.</span></li>
</ol></div></section>
<section class="sp"><div class="wrap"><h2>Les points à préparer avec soin</h2>
{table(['Élément', "Ce qu'il faut savoir", 'Source officielle'], [
 ['Lettre d\'attestation (LAP/LAT)', "Exigée pour la plupart des nouvelles demandes, avec des exceptions fixées par IRCC. Pour 2026, une exception vise notamment les étudiants à la maîtrise ou au doctorat dans un établissement public désigné.", a('https://www.canada.ca/fr/immigration-refugies-citoyennete/organisation/publications-guides/bulletins-guides-operationnels/mises-a-jour/2026-etudiants-lap-lat.html', 'IRCC, mise à jour du 6 février 2026')],
 ['Preuves de fonds', "Vous devez prouver vos frais de scolarité de la première année, vos frais de subsistance et vos frais de transport. Pour les demandes déposées à partir du 1er septembre 2026, IRCC exige au moins 23 448 $ CA de frais de subsistance pour une personne seule, hors frais de scolarité et de transport (hors Québec : le Québec fixe ses propres exigences avec le CAQ). IRCC révise ce montant régulièrement : nous le confirmons avec vous à la consultation.", a('https://www.canada.ca/en/immigration-refugees-citizenship/services/study-canada/study-permit/get-documents/financial-support.html', 'IRCC, preuve de soutien financier (en anglais)')],
 ['Biométrie', "Empreintes et photo se donnent sur rendez-vous au centre VFS Global du Maroc. Pour un résident temporaire, elles restent valides 10 ans.", a('https://visa.vfsglobal.com/mar/fr/can/faq', 'VFS Global Maroc, questions fréquentes')],
 ['Lettre d\'admission', "Elle doit provenir d'un établissement d'enseignement désigné et correspondre au programme indiqué dans votre demande.", 'Établissement choisi'],
])}
<p class="note" style="margin-top:18px">Pour étudier au Québec, une étape provinciale s'ajoute (le CAQ) : nous la voyons avec vous en consultation si votre projet passe par là.</p>
</div></section>
<section class="sp alt"><div class="wrap"><h2>Après les études</h2><div class="prose">
<p>Selon le programme et l'établissement, un permis de travail postdiplôme peut être possible. Cette expérience de travail canadienne peut ensuite compter dans une demande de résidence permanente, par exemple par Entrée express.</p>
<p>Si vous parlez bien français, lisez aussi notre page sur <a href="/entree-express-francophone-maroc/" style="text-decoration:underline">Entrée express pour les francophones</a>.</p></div></div></section>''',
    faq=[
        ("Un citoyen marocain a-t-il besoin d'un permis d'études ?", "En général oui, dès que le programme dure plus de six mois. Pour une formation plus courte, les règles diffèrent : nous vérifions votre cas avec vous."),
        ("Quels documents faut-il fournir ?", "La liste exacte est établie par IRCC selon votre situation. Elle comprend généralement le passeport, la lettre d'admission, la preuve de fonds et, lorsqu'elle est exigée, la LAP/LAT. Nous la validons avec vous avant le dépôt."),
        ("Combien de temps prend le traitement ?", "Les délais changent régulièrement : IRCC les publie sur son site et nous ne promettons aucun délai. Nous vous indiquons la situation à jour au moment de votre rendez-vous."),
        ("Faut-il obligatoirement passer par un consultant ?", "Non, vous pouvez déposer votre demande vous-même. Un consultant réglementé vous aide à choisir la bonne stratégie, à préparer un dossier complet et à éviter les oublis."),
        ("Garantissez-vous l'obtention du permis ?", "Non. Aucun consultant sérieux ne peut garantir une décision : elle appartient uniquement aux autorités canadiennes."),
    ],
    sources=[
        ('https://www.canada.ca/fr/immigration-refugies-citoyennete/organisation/publications-guides/bulletins-guides-operationnels/mises-a-jour/2026-etudiants-lap-lat.html', "IRCC, Permis d'études : lettres d'attestation provinciales ou territoriales (mise à jour du 6 février 2026)"),
        ('https://www.canada.ca/fr/immigration-refugies-citoyennete/organisation/publications-guides/bulletins-guides-operationnels/residents-temporaires/permis-etudes/evaluation-demande.html', "IRCC, Permis d'études : évaluation de la demande"),
        ('https://www.canada.ca/en/immigration-refugees-citizenship/services/study-canada/study-permit/get-documents/financial-support.html', "IRCC, preuve de soutien financier (en anglais)"),
        ('https://visa.vfsglobal.com/mar/fr/can/faq', "VFS Global Maroc, questions fréquentes"),
    ],
    related=[('/entree-express-francophone-maroc/', 'Entrée express pour les francophones'), ('/documents-maroc-immigration-canada/', 'Documents marocains')],
))

# ------------------------------------------------------------------ 2. Entrée express francophone
PAGES.append(dict(
    path='entree-express-francophone-maroc/',
    title="Entrée express francophone depuis le Maroc | ATL Canada",
    desc="Le français peut rapporter jusqu'à 50 points dans Entrée express. Niveau exigé, tests, tirages : un consultant réglementé vous explique. Prenez rendez-vous.",
    crumb="Entrée express francophone",
    eyebrow="Résidence permanente · Casablanca · Montréal",
    h1="Entrée express : le français, un atout pour les candidats du Maroc",
    lede="Un bon niveau de français peut rapporter jusqu'à 50 points supplémentaires dans Entrée express et donne accès à des tirages réservés aux francophones. Voici comment cela fonctionne et ce qu'il faut préparer.",
    body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>Comment le français compte dans votre score</h2>
<div class="prose"><p>Si vous obtenez au moins le niveau NCLC 7 dans les quatre compétences en français (compréhension orale, compréhension écrite, expression orale, expression écrite), vous recevez des points supplémentaires, même si le français est votre langue seconde.</p></div>
{table(['Votre français', 'Votre anglais', 'Points supplémentaires'], [
 ['NCLC 7 ou plus dans les 4 compétences', 'CLB 4 ou moins, ou aucun test d\'anglais', '+ 25 points'],
 ['NCLC 7 ou plus dans les 4 compétences', 'CLB 5 ou plus dans les 4 compétences', '+ 50 points'],
])}
<p class="note">Source : {a('https://www.canada.ca/fr/immigration-refugies-citoyennete/campagnes/immigration-francophone-hors-quebec/immigration-francophone-entree-express.html', 'IRCC, Entrée express pour les travailleurs qualifiés francophones')}. Ces points s'ajoutent à votre score, mais ne garantissent jamais une invitation.</p>
</div></section>
<section class="sp"><div class="wrap"><h2>Les trois programmes d'Entrée express</h2><div class="cards">
<div class="card"><h3>Travailleurs qualifiés (fédéral)</h3><p>Pour les candidats avec de l'expérience de travail qualifiée à l'étranger ou au Canada.</p></div>
<div class="card"><h3>Métiers spécialisés (fédéral)</h3><p>Pour les personnes qualifiées dans un métier spécialisé reconnu.</p></div>
<div class="card"><h3>Expérience canadienne</h3><p>Pour ceux qui ont déjà travaillé au Canada, par exemple après des études.</p></div>
</div>
<div class="prose" style="margin-top:22px"><p>IRCC invite aussi des candidats par catégorie, dont une catégorie dédiée à la maîtrise du français. Les seuils changent à chaque tirage : suivez-les dans nos <a href="/actualites/" style="text-decoration:underline">actualités</a>, par exemple le <a href="/actualites/#express-entree-tirage-francais-16-octobre-2026" style="text-decoration:underline">tirage francophone du 16 octobre 2026</a>.</p></div></div></section>
<section class="sp alt"><div class="wrap"><h2>Ce qu'il faut préparer</h2>
<ol class="steps">
<li><span>Passer un test de français approuvé par IRCC (TEF Canada ou TCF Canada) et, si possible, un test d'anglais : les deux langues influencent vos points.</span></li>
<li><span>Faire évaluer vos diplômes d'études étrangers par un organisme désigné, si vous voulez qu'ils comptent dans le score.</span></li>
<li><span>Créer votre profil en ligne avec votre code de référence personnel. Les documents ne se téléversent qu'après une invitation.</span></li>
<li><span>Après l'invitation, vous disposez de 60 jours pour présenter votre demande de résidence permanente.</span></li>
<li><span>Préparer vos pièces marocaines, dont le certificat de police : voir notre page sur les <a href="/documents-maroc-immigration-canada/" style="text-decoration:underline">documents marocains</a>.</span></li>
</ol>
<div class="prose" style="margin-top:22px"><p>Une désignation par un programme des candidats des provinces ajoute aussi des points. Et si votre score est trop bas, un permis de travail Mobilité francophone peut aider certains candidats à acquérir de l'expérience au Canada, sous réserve des conditions d'IRCC.</p></div>
</div></section>''',
    faq=[
        ("Quel niveau de français faut-il ?", "Le niveau NCLC 7 dans les quatre compétences ouvre droit aux points supplémentaires et à la catégorie francophone. Un test approuvé par IRCC (TEF Canada ou TCF Canada) est nécessaire."),
        ("Quel score faut-il pour être invité ?", "Il n'y a pas de seuil fixe : chaque tirage a son propre score minimal. Les derniers résultats sont publiés par IRCC et résumés dans nos actualités."),
        ("Faut-il passer par un consultant ?", "Non, vous pouvez créer votre profil et déposer vous-même. Un consultant réglementé vous aide à vérifier votre admissibilité, à optimiser votre score honnêtement et à préparer un dossier complet dans le délai de 60 jours."),
        ("Le français suffit-il pour être invité ?", "Non. Il faut aussi remplir les conditions d'un des trois programmes et figurer parmi les meilleurs scores du bassin. Une invitation n'est jamais garantie."),
        ("Garantissez-vous une invitation ou la résidence permanente ?", "Non. Les décisions appartiennent uniquement à IRCC. Notre rôle est de choisir la bonne stratégie et de préparer un dossier rigoureux."),
    ],
    sources=[
        ('https://www.canada.ca/fr/immigration-refugies-citoyennete/campagnes/immigration-francophone-hors-quebec/immigration-francophone-entree-express.html', "IRCC, Entrée express pour les travailleurs qualifiés francophones (mise à jour du 20 août 2025)"),
        ('https://www.canada.ca/en/immigration-refugees-citizenship/corporate/mandate/policies-operational-instructions-agreements/ministerial-instructions/express-entry-rounds.html', "IRCC, rondes d'invitations Entrée express"),
    ],
    related=[("/permis-etudes-canada-maroc/", "Permis d'études depuis le Maroc"), ('/documents-maroc-immigration-canada/', 'Documents marocains')],
))

# ------------------------------------------------------------------ 3. Documents marocains
PAGES.append(dict(
    path='documents-maroc-immigration-canada/',
    title="Documents marocains pour immigrer au Canada | ATL Canada",
    desc="Certificat de police marocain (fiche anthropométrique), biométrie VFS, documents à ne pas confondre : ce qu'IRCC accepte. Un consultant réglementé vous guide.",
    crumb="Documents marocains",
    eyebrow="Dossier · Casablanca · Montréal",
    h1="Documents marocains pour votre demande d'immigration au Canada",
    lede="Le certificat de police marocain est l'une des pièces qui font le plus souvent hésiter les candidats. Voici ce qu'IRCC demande aux citoyens marocains, d'après ses pages officielles.",
    body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>Le certificat de police du Maroc</h2>
<div class="prose"><p>Une demande de résidence permanente exige un certificat de police. Pour les citoyens marocains, le document s'appelle la <strong>fiche anthropométrique</strong>. Les empreintes prises pour ce certificat sont distinctes de la biométrie que vous donnez avec votre demande.</p></div>
{table(['Votre situation', "Ce qu'IRCC indique"], [
 ['Citoyen marocain vivant au Maroc', "Présentez-vous au commissariat de votre lieu de résidence avec votre carte nationale d'identité. Vous pouvez désigner un représentant, qui doit présenter sa propre carte nationale."],
 ['Citoyen marocain vivant à l\'étranger', "Adressez-vous à l'ambassade ou au consulat du Maroc le plus proche, ou passez par le commissariat local par procuration (pas par le service central de Rabat). La procuration exige une procuration notariée, des copies de l'acte de naissance et du passeport, et des frais."],
 ['Langue du document', "Le certificat est délivré en français et en arabe : aucune traduction n'est nécessaire."],
 ['À ne pas confondre', "Le « bulletin n° 3 » délivré par le tribunal de première instance aux Marocains n'est pas accepté pour l'immigration : il ne couvre que les infractions commises dans la ville de résidence."],
 ['Durée de validité', "Les pages officielles ne la précisent pas : appelez-nous, nous la vérifions avec vous avant le dépôt de votre demande, pour ne pas perdre de temps."],
])}
<p class="note">Source : {a('https://www.canada.ca/fr/immigration-refugies-citoyennete/services/demande/medical-police/certificats-police/comment/maroc.html', 'IRCC, Comment obtenir un certificat de police : Maroc')}.</p>
</div></section>
<section class="sp"><div class="wrap"><h2>La biométrie et le centre VFS Global</h2><div class="prose">
<p>IRCC a autorisé VFS Global à recevoir les demandes de visa, de permis d'études et de permis de travail au Maroc et à enregistrer vos empreintes et votre photo. L'enregistrement se fait uniquement sur rendez-vous, réservé en ligne.</p>
<p>Un résident temporaire ne donne ses données biométriques qu'une fois tous les 10 ans. Un demandeur de résidence permanente doit les fournir à chaque demande. Vérifiez votre cas sur le site d'IRCC.</p>
<p class="note">Source : {a('https://visa.vfsglobal.com/mar/fr/can/faq', 'VFS Global Maroc, questions fréquentes')}.</p></div></div></section>
<section class="sp alt"><div class="wrap"><h2>Les autres pièces habituelles</h2><div class="prose">
<p>La liste exacte dépend de votre demande et est établie par IRCC pour votre situation. On retrouve généralement le passeport, l'acte de naissance, les diplômes et relevés de notes, les résultats de tests de langue et les preuves de fonds ou d'expérience de travail.</p>
<p>Tout document qui n'est pas en français ou en anglais doit être accompagné d'une traduction. Nous vérifions avec vous chaque pièce avant le dépôt, pour qu'aucune ne retarde votre dossier.</p></div></div></section>''',
    faq=[
        ("Comment s'appelle le certificat de police pour les Marocains ?", "Pour les citoyens marocains, IRCC parle de la « fiche anthropométrique ». Elle est délivrée par la police."),
        ("Le bulletin n° 3 est-il accepté ?", "Non, pas lorsqu'il est obtenu auprès du tribunal de première instance par un citoyen marocain : IRCC l'a écarté parce qu'il ne couvre que la ville de résidence."),
        ("Peut-on demander la fiche anthropométrique à la place du candidat ?", "Oui, IRCC indique qu'un représentant peut la demander, à condition de présenter sa propre carte nationale d'identité."),
        ("Faut-il faire traduire la fiche anthropométrique ?", "Non, elle est délivrée en français et en arabe, donc IRCC n'exige pas de traduction."),
        ("Pour quelles demandes faut-il un certificat de police ?", "Pour une demande de résidence permanente, il est exigé. Pour les autres demandes, cela dépend du cas : nous le vérifions pendant la consultation."),
    ],
    sources=[
        ('https://www.canada.ca/fr/immigration-refugies-citoyennete/services/demande/medical-police/certificats-police/comment/maroc.html', "IRCC, Comment obtenir un certificat de police : Maroc"),
        ('https://visa.vfsglobal.com/mar/fr/can/faq', "VFS Global Maroc, questions fréquentes"),
    ],
    related=[("/permis-etudes-canada-maroc/", "Permis d'études depuis le Maroc"), ('/entree-express-francophone-maroc/', 'Entrée express pour les francophones')],
))


AR_OF = {'permis-etudes-canada-maroc/': 'ar/study-permit-morocco/', 'entree-express-francophone-maroc/': 'ar/express-entry-french/', 'documents-maroc-immigration-canada/': 'ar/moroccan-documents/'}


def head_for(p):
    url = f"{SITE}/{p['path']}"
    h = head_ref
    h = re.sub(r'<title>.*?</title>', f"<title>{e(p['title'])}</title>", h, flags=re.S)
    h = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + e(p['desc'], quote=True) + m.group(2), h)
    for tag in ('og:title', 'twitter:title'):
        h = re.sub(rf'(<meta (?:property|name)="{tag}" content=")[^"]*(")', lambda m: m.group(1) + e(p['title'], quote=True) + m.group(2), h)
    for tag in ('og:description', 'twitter:description'):
        h = re.sub(rf'(<meta (?:property|name)="{tag}" content=")[^"]*(")', lambda m: m.group(1) + e(p['desc'], quote=True) + m.group(2), h)
    h = re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), h)
    h = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), h)
    h = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', '', h)
    alt = (f'<link rel="alternate" hreflang="fr-MA" href="{url}">\n<link rel="alternate" hreflang="ar-MA" href="{SITE}/{AR_OF[p["path"]]}">\n'
           f'<link rel="alternate" hreflang="x-default" href="{url}">\n')
    h = re.sub(r'(<link rel="canonical" href="[^"]*">\n?)', lambda m: m.group(1) + alt, h, count=1)
    # JSON-LD
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    g = json.loads(m.group(1))
    keep = [n for n in g['@graph'] if n['@type'] in ('ProfessionalService', 'WebSite')]
    keep += [
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": p['title'], "description": p['desc'],
         "inLanguage": "fr-MA", "dateModified": UPDATED, "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#organization"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Immigrer depuis le Maroc", "item": SITE + "/maroc/"},
            {"@type": "ListItem", "position": 3, "name": p['crumb'], "item": url}]},
        {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": "fr-MA", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a_)}} for q, a_ in p['faq']]},
    ]
    g['@graph'] = keep
    h = h[:m.start()] + '<script type="application/ld+json">' + json.dumps(g, ensure_ascii=False) + '</script>' + h[m.end():]
    h = h.replace('<link rel="stylesheet" href="/assets/news.css">', '<link rel="stylesheet" href="/assets/news.css">\n' + EXTRA_CSS, 1) if '<link rel="stylesheet" href="/assets/news.css">' in h else h + EXTRA_CSS
    return h


for p in PAGES:
    related = ''.join(f'<a class="btn btn-outline" style="color:var(--ink);border-color:var(--ink)" href="{u}">{e(l)}</a>' for u, l in p['related'])
    src = ''.join(f'<li>{a(u, l)}</li>' for u, l in p['sources'])
    page = f'''{head_for(p)}</head>
{topbar}<main>
<section class="pg-hero"><div class="wrap">
  <p class="crumb"><a href="/">Accueil</a> › <a href="/maroc/">Immigrer depuis le Maroc</a> › {e(p['crumb'])}</p>
  <p class="eyebrow">{e(p['eyebrow'])}</p>
  <h1>{e(p['h1'])}</h1>
  <p class="lede">{e(p['lede'])}</p>
  <div class="cta-row"><a class="btn btn-solid" href="/#contact">Prendre rendez-vous</a><a class="btn btn-outline" href="tel:+15142956635">Appeler · <bdi dir="ltr">+1 514 295 6635</bdi></a></div>
</div></section>
{p['body']}
<section class="sp alt" id="faq"><div class="wrap"><h2>Questions fréquentes</h2><div class="faq-list">{faq_html(p['faq'])}</div></div></section>
<section class="sp"><div class="wrap"><h2>Sources officielles</h2><ul class="sources">{src}</ul>
<p class="note" style="margin-top:18px">Dernière mise à jour : 26 octobre 2026.</p>
<div class="related">{related}</div></div></section>
{offices}
{footer}'''
    os.makedirs(R + p['path'], exist_ok=True)
    open(R + p['path'] + 'index.html', 'w', encoding='utf-8').write(page)
    print('ok', p['path'], len(page), 'octets')
