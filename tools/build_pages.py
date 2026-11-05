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
                        '<a href="/#services">Services</a><a href="/maroc/">Maroc</a><a href="#faq">Questions</a><a href="#bureaux">Bureaux</a>')
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
.cmp{display:grid;grid-template-columns:repeat(2,1fr);gap:22px;margin:0 0 8px}
.cmp-card{background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden;box-shadow:0 8px 24px rgba(22,35,61,.07)}
.cmp-card h3{margin:0;padding:18px 24px;background:var(--ink);color:#fff;font-family:'Lora',serif;font-size:1.3rem;font-weight:600}
.cmp-card.b h3{background:var(--rust)}
.cmp-row{padding:16px 24px;border-top:1px solid var(--line)}
.cmp-row:first-of-type{border-top:0}
.cmp-row b{display:block;font-size:.76rem;letter-spacing:.07em;text-transform:uppercase;color:var(--rust);margin-bottom:5px}
.cmp-row span{color:var(--ink-soft);line-height:1.6}
.info-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin:0 0 8px}
.info{background:#fff;border:1px solid var(--line);border-top:4px solid #E1232B;border-radius:10px;padding:20px 24px;box-shadow:0 6px 18px rgba(22,35,61,.05)}
.info h3{margin:0 0 8px;font-family:'Lora',serif;font-size:1.12rem;font-weight:600;color:var(--ink)}
.info p{margin:0;color:var(--ink-soft);line-height:1.65}
.info-link{display:block;text-decoration:none;color:inherit;transition:transform .15s ease,box-shadow .15s ease}.info-link:hover{transform:translateY(-3px);box-shadow:0 12px 26px rgba(22,35,61,.12)}.info-link .go{display:inline-block;margin-top:12px;color:#E1232B;font-weight:700;font-size:.9rem;letter-spacing:.02em}
.info-grid .info:last-child:nth-child(odd){grid-column:1/-1}
@media (max-width:760px){.cmp,.info-grid{grid-template-columns:1fr}}
</style>
"""

LAW = "Les informations de cette page sont générales et ne remplacent pas une évaluation personnalisée. Les règles d'immigration changent souvent : contactez-nous ou appelez-nous pour une évaluation de votre situation. Aucun résultat n'est garanti."

def table(headers, rows):
    th = ''.join(f'<th scope="col">{e(h)}</th>' for h in headers)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="tbl-wrap"><table class="tbl"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'

def rich(headers, rows):
    """Présentation en cartes : 3 colonnes = comparaison côte à côte, 2 colonnes = cartes d'information."""
    if len(headers) == 3:
        out = ''
        for k in (1, 2):
            rws = ''.join(f'<div class="cmp-row"><b>{r[0]}</b><span>{r[k]}</span></div>' for r in rows)
            out += f'<div class="cmp-card{" b" if k == 2 else ""}"><h3>{e(headers[k])}</h3>{rws}</div>'
        return f'<div class="cmp">{out}</div>'
    def card(r):
        if len(r) > 2:
            return f'<a class="info info-link" href="{r[2]}"><h3>{r[0]}</h3><p>{r[1]}</p><span class="go">En savoir plus →</span></a>'
        return f'<div class="info"><h3>{r[0]}</h3><p>{r[1]}</p></div>'
    return '<div class="info-grid">' + ''.join(card(r) for r in rows) + '</div>'


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


# ------------------------------------------------------------------ 4. Visa de visiteur et super visa
PAGES.append(dict(
    path='visa-visiteur-super-visa-canada/',
    updated='5 novembre 2026', updated_iso='2026-11-05',
    title="Visa de visiteur et super visa pour le Canada depuis le Maroc | ATL Canada",
    desc="Visa de visiteur ou super visa pour vos parents et grands-parents : conditions, revenu minimal de l'hôte, assurance, examen médical. Un consultant réglementé vous accompagne.",
    crumb="Visa de visiteur et super visa",
    eyebrow="Visiteurs · Casablanca · Montréal",
    h1="Visa de visiteur et super visa pour le Canada depuis le Maroc",
    lede="Rendre visite à un proche, voyager ou venir voir vos enfants et petits-enfants : le visa de visiteur couvre la plupart des séjours, et le super visa est conçu pour les parents et grands-parents. Voici les conditions officielles et les pièces à préparer.",
    body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>Visa de visiteur ou super visa : lequel choisir ?</h2>
{rich(['', 'Visa de visiteur', 'Super visa'], [
 ['Pour qui', "Toute personne qui vient visiter le Canada (famille, tourisme, affaires)", "Les parents et grands-parents d'un citoyen canadien, d'un résident permanent ou d'une personne inscrite au registre des Indiens"],
 ['Séjour', "Convient aux séjours de 6 mois ou moins, d'après IRCC", "Pour des séjours plus longs : l'agent peut autoriser un séjour de 5 ans, selon IRCC"],
 ['Invitation', "Une lettre d'invitation peut être utile, voire demandée selon le cas", "Lettre d'invitation signée par votre enfant ou petit-enfant, obligatoire"],
 ['Assurance médicale', "Non exigée par la liste de conditions d'IRCC", "Assurance privée valide au moins 1 an, obligatoire"],
])}
</div></section>
<section class="sp"><div class="wrap"><h2>Visa de visiteur : ce qu'IRCC vérifie</h2>
<ol class="steps">
<li><span>Vous avez un document de voyage valide, comme un passeport (IRCC recommande qu'il soit valide au moins 6 mois à partir de la date prévue du voyage).</span></li>
<li><span>Vous êtes en bonne santé. Un examen médical peut être exigé.</span></li>
<li><span>Vous n'avez pas de condamnation criminelle ni de condamnation liée à l'immigration.</span></li>
<li><span>Vous avez des attaches dans votre pays (emploi, logement, avoirs financiers, famille) qui vous donnent une raison d'y retourner.</span></li>
<li><span>Vous montrez que vous quitterez le Canada à la fin de votre séjour.</span></li>
<li><span>Vous avez assez d'argent pour votre séjour : le montant dépend de la durée et du type d'hébergement (hôtel ou chez des proches).</span></li>
</ol>
<div class="prose" style="margin-top:22px"><p>Pour un séjour touristique, IRCC recommande notamment de joindre : une lettre d'invitation et la preuve de votre lien avec la personne qui vous invite, vos antécédents de voyage, un itinéraire, des relevés bancaires couvrant au moins 6 mois et une lettre de votre employeur datée d'au plus 3 mois.</p></div>
{rich(['Élément', "Ce qu'indique IRCC"], [
 ['Frais de traitement', "100 $ CA par personne, ou 500 $ CA pour une famille de 5 personnes ou plus."],
 ['Biométrie', "85 $ CA par personne, ou jusqu'à 170 $ CA pour une famille admissible. Attendez la lettre d'instructions, puis réservez rapidement votre rendez-vous."],
 ['Dépôt', "En ligne, par le portail d'IRCC. La demande sur papier n'est permise que dans des cas précis."],
 ['Validité', "Un visa peut être délivré pour une durée maximale de 10 ans, ou jusqu'à l'expiration du passeport ou des données biométriques si elle survient avant. L'agent peut fixer une autre date."],
])}
</div></section>
<section class="sp alt"><div class="wrap"><h2>Super visa : les conditions</h2>
{rich(['Condition', "Ce qu'indique IRCC"], [
 ["Votre enfant ou petit-enfant (l'hôte)", "Citoyen canadien, résident permanent ou personne inscrite au registre des Indiens, âgé d'au moins 18 ans et vivant au Canada. Le lien (enfant ou petit-enfant biologique ou adopté) doit être prouvé, par exemple avec son acte de naissance."],
 ['Lettre d\'invitation', "Signée par l'hôte, elle doit montrer qu'il atteint le revenu minimal nécessaire et lister toutes les personnes comptées dans sa famille, avec nom et date de naissance. Son conjoint ou conjoint de fait peut cosigner s'il est citoyen, résident permanent ou inscrit au registre des Indiens."],
 ['Revenu minimal de l\'hôte', "Il est fixé à partir des seuils de faible revenu de Statistique Canada. L'hôte le prouve par ses avis de cotisation de l'Agence du revenu du Canada pour l'une des deux années d'imposition précédant la demande, ou par d'autres documents prévus par IRCC. Le montant dépend de la taille de la famille : consultez le tableau à jour sur la page d'IRCC, car il est mis à jour."],
 ['Assurance médicale', "Assurance privée valide au moins 1 an à partir de la date d'entrée et pour chaque entrée au Canada, d'un assureur canadien ou d'un assureur étranger autorisé par le BSIF et inscrit sur sa liste. Elle couvre les soins de santé, l'hospitalisation et le rapatriement, avec une protection d'urgence d'au moins 100 000 $. Elle doit être payée, en totalité ou par versements avec un dépôt : une simple soumission n'est pas acceptée."],
 ['Examen médical', "Un examen médical d'immigration, passé auprès d'un médecin désigné, est exigé."],
 ['Vous (le demandeur)', "Vous devez être hors du Canada lorsque vous présentez la demande et être admissible. IRCC évalue aussi que vous êtes un véritable visiteur qui quittera le Canada à la fin de la visite (attaches, objet du séjour, famille, finances)."],
])}
<div class="prose" style="margin-top:18px"><p>Depuis le 28 janvier 2025, une assurance émise par un assureur établi à l'étranger est acceptée s'il est autorisé par le BSIF. Si une demande de parrainage est en cours, vous pouvez demander un super visa en attendant la décision. Après l'approbation, le visa est imprimé par un bureau des visas hors du Canada : attendez ses instructions.</p></div>
</div></section>
<section class="sp"><div class="wrap"><h2>Comment nous vous accompagnons</h2><div class="prose">
<p>Nous vérifions avec vous quel visa correspond à votre situation, nous passons en revue le revenu de votre enfant ou petit-enfant et son calcul de famille, la lettre d'invitation, l'assurance et les pièces justificatives, puis nous préparons un dossier complet avant le dépôt. Toute pièce qui n'est pas en français ou en anglais doit être traduite par un traducteur qualifié.</p>
<p class="note">La décision appartient uniquement à IRCC : nous ne pouvons ni garantir un visa ni promettre un délai.</p></div></div></section>''',
    faq=[
        ("Ai-je besoin d'un visa pour venir au Canada ?", "Cela dépend de votre nationalité et de votre moyen de transport. IRCC propose un outil « Vérifier si vous avez besoin d'un visa ou d'une AVE » : nous le vérifions avec vous."),
        ("Quelle est la différence entre le visa de visiteur et le super visa ?", "Le visa de visiteur convient à la plupart des séjours de 6 mois ou moins. Le super visa est réservé aux parents et grands-parents d'un citoyen canadien ou d'un résident permanent et permet des séjours plus longs."),
        ("Mon enfant doit-il gagner un revenu minimum pour mon super visa ?", "Oui. L'hôte doit atteindre le revenu minimal nécessaire fixé par IRCC selon la taille de sa famille, et le prouver, par exemple avec ses avis de cotisation."),
        ("L'assurance médicale est-elle obligatoire ?", "Pour le super visa, oui : au moins 1 an de couverture à partir de l'entrée, avec une protection d'urgence d'au moins 100 000 $. Pour le visa de visiteur, la liste de conditions d'IRCC n'en fait pas une exigence."),
        ("Une lettre d'invitation garantit-elle le visa ?", "Non. Elle est obligatoire pour le super visa et peut être utile pour un visa de visiteur, mais la décision repose sur l'ensemble du dossier."),
        ("Garantissez-vous l'obtention du visa ?", "Non. Aucun consultant sérieux ne peut garantir une décision : elle appartient uniquement aux autorités canadiennes."),
    ],
    sources=[],
    related=[("/permis-etudes-canada-maroc/", "Permis d'études depuis le Maroc"), ('/documents-maroc-immigration-canada/', 'Documents marocains')],
))


PAGES.append(dict(
    path='parrainage-familial-canada/',
    updated='5 novembre 2026', updated_iso='2026-11-05',
    title="Parrainage familial au Canada depuis le Maroc : conjoint, enfants, parents | ATL Canada",
    desc="Réunir votre famille au Canada : qui peut être parrainé, preuves de la relation, déclaration des membres de la famille. Un consultant réglementé prépare votre dossier.",
    crumb="Parrainage familial",
    eyebrow="Famille · Casablanca · Montréal",
    h1="Parrainage familial : réunir votre famille au Canada",
    lede="Conjoint, enfants à charge, parents ou grands-parents : le parrainage permet à votre famille de venir vivre au Canada. Voici qui peut être parrainé et les points où un dossier se joue.",
    body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>Qui peut être parrainé ?</h2>
{rich(['Lien avec vous', "Ce qu'indique IRCC"], [
 ['Époux ou épouse', "Légalement marié, âgé d'au moins 18 ans, dans une relation authentique (et non conclue uniquement pour obtenir un statut de résident permanent)."],
 ['Conjoint de fait', "Âgé d'au moins 18 ans, dans une relation authentique, et ayant vécu avec vous au moins 12 mois consécutifs dans une relation conjugale."],
 ['Partenaire conjugal', "Âgé d'au moins 18 ans, dans une relation exclusive d'au moins 1 an, vivant hors du Canada et dans l'impossibilité de vivre avec vous ou de vous épouser pour des raisons précises."],
 ['Enfant à charge', "Votre enfant, ou celui de votre conjoint ou partenaire, de moins de 22 ans et sans conjoint, ou d'au moins 22 ans mais dépendant financièrement en raison d'une condition physique ou mentale (ou dépendant depuis avant 22 ans)."],
 ['Parents et grands-parents', "Vos parents et grands-parents, par le sang ou par adoption, avec leurs enfants à charge. Les parents de votre conjoint ne peuvent pas être parrainés par vous."],
])}
<p class="note" style="margin-top:18px">Dans tous les cas, la personne parrainée ne doit pas être interdite de territoire au Canada.</p>
</div></section>
<section class="sp"><div class="wrap"><h2>Les points à préparer avec soin</h2>
<ol class="steps">
<li><span>Vérifier que le répondant et la personne parrainée remplissent les conditions d'IRCC, notamment le statut du répondant au Canada.</span></li>
<li><span>Montrer une relation authentique : IRCC examine si le lien est réel et pas seulement un moyen d'obtenir la résidence permanente.</span></li>
<li><span>Déclarer tous les membres de la famille, y compris les enfants qui ne viennent pas ou dont l'autre parent a la garde exclusive. Une omission peut compromettre le dossier.</span></li>
<li><span>Réunir les formulaires et pièces demandés, puis répondre aux demandes en cours de traitement (examen médical, certificat de police, biométrie).</span></li>
<li><span>Suivre le dossier jusqu'à la décision, sans changer les informations déclarées sans en parler avec nous.</span></li>
</ol>
<div class="prose" style="margin-top:22px"><p>Une politique d'IRCC qui permettait de parrainer certains membres de la famille non déclarés ne s'applique pas aux demandes déposées après le 10 septembre 2026 : la déclaration complète de la famille est donc essentielle. Pour les pièces marocaines (acte de naissance, certificat de police), voyez aussi notre page sur les <a href="/documents-maroc-immigration-canada/" style="text-decoration:underline">documents marocains</a>.</p></div>
</div></section>
<section class="sp alt"><div class="wrap"><h2>Comment nous vous accompagnons</h2><div class="prose">
<p>En consultation, nous vérifions avec vous quelle catégorie de parrainage correspond à votre famille, si les conditions sont réunies et quelles preuves de la relation sont les plus solides. Nous préparons ensuite un dossier complet et cohérent avant le dépôt. Le programme pour les parents et les grands-parents a ses propres règles d'accès, qu'IRCC fait évoluer : nous vérifions avec vous où il en est au moment de votre demande.</p>
<p class="note">La décision appartient uniquement à IRCC : nous ne pouvons ni garantir un résultat ni promettre un délai.</p></div></div></section>''',
    faq=[
        ("Qui peut parrainer un membre de sa famille ?", "Le répondant doit remplir les conditions fixées par IRCC, notamment concernant son statut au Canada. Nous les vérifions avec vous en consultation."),
        ("Quelle est la différence entre conjoint et conjoint de fait ?", "Le conjoint est légalement marié avec vous. Le conjoint de fait ne l'est pas, mais a vécu avec vous au moins 12 mois consécutifs dans une relation conjugale."),
        ("Jusqu'à quel âge un enfant est-il à charge ?", "Un enfant de moins de 22 ans sans conjoint est considéré à charge. Au-delà, il faut qu'il dépende financièrement de ses parents en raison d'une condition physique ou mentale, ou depuis avant 22 ans."),
        ("Dois-je déclarer un enfant qui ne vient pas au Canada ?", "Oui. IRCC exige que tous les enfants soient déclarés, même ceux qui ne viennent pas ou dont l'autre parent a la garde exclusive."),
        ("Pouvez-vous garantir l'approbation du parrainage ?", "Non. Aucun consultant sérieux ne peut garantir une décision : elle appartient uniquement aux autorités canadiennes."),
    ],
    sources=[],
    related=[("/visa-visiteur-super-visa-canada/", "Visa de visiteur et super visa"), ('/documents-maroc-immigration-canada/', 'Documents marocains')],
))

PAGES.append(dict(
    path='permis-de-travail-canada/',
    updated='5 novembre 2026', updated_iso='2026-11-05',
    title="Permis de travail au Canada : demande, prolongation, changement d'employeur | ATL Canada",
    desc="Permis de travail au Canada, de l'étranger ou depuis le Canada : permis lié à un employeur ou ouvert, EIMT, prolongation, statut maintenu, permis postdiplôme. Un consultant réglementé vous accompagne.",
    crumb="Permis de travail", neutral=True,
    eyebrow="Travail · Casablanca · Montréal",
    h1="Permis de travail au Canada : demande, prolongation, changement",
    lede="Que vous soyez à l'étranger ou déjà au Canada, de toute nationalité : travailler au Canada demande presque toujours un permis. Voici les deux grands types de permis, le rôle de l'employeur, et ce qu'il faut savoir pour prolonger ou modifier votre permis.",
    body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>Deux grands types de permis</h2>
{rich(['', 'Permis lié à un employeur', 'Permis ouvert'], [
 ["Principe", "Il vous permet de travailler seulement selon ses conditions : l'employeur, le lieu et la profession sont inscrits sur le permis, jusqu'à sa date d'expiration.", "Il vous permet de travailler pour la plupart des employeurs conformes au Canada, sans être lié à un seul."],
 ["Offre d'emploi", "Une offre d'un employeur qui ne figure pas sur la liste des employeurs non conformes est nécessaire.", "Aucune offre d'emploi n'est nécessaire."],
 ["Pour qui", "C'est le type le plus courant.", "Seulement dans des situations particulières prévues par IRCC."],
])}
<p class="note" style="margin-top:18px">Certaines personnes n'ont pas besoin de permis de travail : IRCC propose un questionnaire en ligne pour le vérifier.</p>
</div></section>
<section class="sp"><div class="wrap"><h2>Vous êtes déjà au Canada ?</h2>
{rich(['Situation', 'Ce qu\'indique IRCC'], [
 ["Prolonger son permis", "Il faut déposer la demande avant l'expiration du permis : une demande en ligne doit être envoyée avant minuit (temps universel) à la date d'expiration. Vous ne pouvez pas prolonger au-delà de la date d'expiration de votre passeport."],
 ["Statut maintenu", "Si vous avez demandé à temps, vous pouvez rester au Canada pendant le traitement. Avec un permis lié à un employeur, vous continuez de travailler seulement pour le même employeur, dans le même poste et au même lieu. Avec un permis ouvert, vous pouvez changer d'employeur."],
 ["Pendant le traitement", "Vous ne pouvez pas renouveler certains documents provinciaux, comme le permis de conduire ou la carte d'assurance maladie : renouvelez-les avant l'expiration du permis. Une demande en ligne donne généralement une lettre (WP-EXT) qui prouve à votre employeur que vous pouvez continuer à travailler."],
 ["Changer les conditions du permis", "Un changement d'employeur, de poste ou de lieu pour un permis lié à un employeur passe par une demande de modification des conditions. Parlez-nous-en avant de changer quoi que ce soit."],
 ["Permis de travail postdiplôme", "À déposer dans les 180 jours suivant la confirmation de la fin des études. Il faut avoir terminé un programme d'au moins 8 mois (900 heures au Québec) dans un établissement admissible, avoir étudié à temps plein, et, pour les demandes déposées depuis le 1er novembre 2024, répondre aux exigences de langue (NCLC 7 pour l'université, NCLC 5 pour le collège) et, pour certains programmes, de domaine d'études."],
 ["Permis déjà expiré", "Si votre permis expire pendant le traitement ou est déjà expiré, vérifiez avec nous si vous pouvez continuer à travailler : les règles dépendent de votre situation."],
])}
<p class="note" style="margin-top:18px">Les frais et les règles changent : IRCC en tient la liste à jour, et nous la vérifions avec vous avant de déposer.</p>
</div></section>
<section class="sp alt"><div class="wrap"><h2>Le permis lié à un employeur, étape par étape</h2>
<ol class="steps">
<li><span>Obtenir une offre d'emploi d'un employeur qui n'est pas sur la liste des employeurs non conformes.</span></li>
<li><span>Votre employeur confirme si le poste exige une évaluation de l'impact sur le marché du travail (EIMT) ou s'il en est exempté. « La plupart des emplois exigent une EIMT », indique IRCC.</span></li>
<li><span>Si une EIMT est exigée, l'employeur la demande et vous remet la lettre d'EIMT et l'annexe A avant votre demande.</span></li>
<li><span>Vous déposez votre demande de permis : de l'extérieur du Canada, de l'intérieur, à un point d'entrée ou pour une prolongation, selon votre situation.</span></li>
<li><span>Une fois le permis délivré, vous respectez ses conditions (employeur, lieu, profession, date d'expiration).</span></li>
</ol>
<div class="prose" style="margin-top:22px"><p>Sans permis, vous ne pouvez pas travailler légalement au Canada, ni indiquer dans une candidature que vous y êtes autorisé. IRCC propose aussi des voies particulières, comme Expérience internationale Canada (Jeunes professionnels), la Stratégie en matière de compétences mondiales et le travail agricole.</p>
<p>Un permis de travail peut aussi être une étape vers la résidence permanente : voyez notre page sur l'<a href="/entree-express-francophone-maroc/" style="text-decoration:underline">Entrée express pour les francophones</a>.</p></div>
</div></section>
<section class="sp alt"><div class="wrap"><h2>Comment nous vous accompagnons</h2><div class="prose">
<p>En consultation, que vous soyez à l'étranger ou déjà au Canada, nous déterminons avec vous quel type de permis correspond à votre situation (nouvelle demande, prolongation, changement de conditions, permis postdiplôme), nous vérifions les documents que votre employeur doit vous fournir et nous préparons votre demande avant le dépôt. Si vous n'avez pas encore d'offre, nous voyons ensemble les pistes réalistes.</p>
<p class="note">La décision appartient uniquement à IRCC : nous ne pouvons ni garantir un permis ni promettre un délai.</p></div></div></section>''',
    faq=[
        ("Ai-je besoin d'un permis de travail ?", "Dans la plupart des cas, oui. Certaines personnes en sont exemptées : IRCC propose un questionnaire en ligne pour le vérifier, et nous le faisons avec vous."),
        ("Qu'est-ce qu'une EIMT ?", "L'évaluation de l'impact sur le marché du travail montre qu'il y a un besoin d'embaucher un travailleur étranger. Votre employeur doit confirmer si votre poste en exige une ou en est exempté."),
        ("Puis-je changer d'employeur avec un permis lié à un employeur ?", "Ce permis est lié à l'employeur, au lieu et à la profession indiqués. Avant tout changement, parlez-nous-en pour connaître les démarches à suivre."),
        ("Que se passe-t-il si je travaille sans permis ?", "Vous ne pouvez pas travailler légalement au Canada sans le permis requis. Il ne faut pas non plus indiquer dans une candidature que vous y êtes autorisé si ce n'est pas le cas."),
        ("Que se passe-t-il si mon permis expire pendant le traitement de ma prolongation ?", "Si vous avez déposé votre demande avant l'expiration, vous avez le statut maintenu et pouvez rester au Canada. Avec un permis lié à un employeur, vous continuez de travailler seulement pour le même employeur, dans le même poste et au même lieu."),
        ("Quand demander le permis postdiplôme ?", "Dans les 180 jours suivant la confirmation de la fin de votre programme, selon IRCC. Votre permis d'études doit avoir été valide à un moment pendant ces 180 jours."),
        ("Garantissez-vous l'obtention du permis de travail ?", "Non. Aucun consultant sérieux ne peut garantir une décision : elle appartient uniquement aux autorités canadiennes."),
    ],
    sources=[],
    related=[("/entree-express-francophone-maroc/", "Entrée express pour les francophones"), ('/visa-visiteur-super-visa-canada/', 'Visa de visiteur et super visa')],
))


PAGES.append(dict(
    path='immigration-quebec-canada/',
    updated='5 novembre 2026', updated_iso='2026-11-05',
    title="Immigrer au Québec depuis le Maroc : sélection du Québec, PSTQ, CSQ | ATL Canada",
    desc="Immigrer au Québec : la sélection par le Québec (CSQ), le Programme de sélection des travailleurs qualifiés, l'état du PEQ. Un consultant réglementé vous explique la marche à suivre.",
    crumb="Immigrer au Québec",
    eyebrow="Québec · Casablanca · Montréal",
    h1="Immigrer au Québec depuis le Maroc",
    lede="Le Québec choisit lui-même une partie de ses immigrants économiques. Voici comment fonctionne ce parcours en deux temps et où en sont les programmes principaux.",
    body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>Un parcours en deux temps</h2>
<ol class="steps">
<li><span>La sélection par le Québec : le ministère de l'Immigration du Québec examine votre dossier et, s'il est favorable, délivre un Certificat de sélection du Québec (CSQ).</span></li>
<li><span>La demande de résidence permanente : une fois le CSQ obtenu, vous déposez ensuite votre demande auprès d'IRCC, qui vérifie notamment l'admissibilité (médicale, sécurité, criminalité).</span></li>
</ol>
<div class="prose" style="margin-top:22px"><p>Pour étudier au Québec, une étape provinciale s'ajoute aussi avant le permis d'études : le CAQ. Voyez notre page sur le <a href="/permis-etudes-canada-maroc/" style="text-decoration:underline">permis d'études depuis le Maroc</a>.</p></div>
</div></section>
<section class="sp"><div class="wrap"><h2>Où en sont les programmes ?</h2>
{rich(['Programme', "Ce qu'indique le gouvernement du Québec"], [
 ['Programme de sélection des travailleurs qualifiés (PSTQ)', "On déclare d'abord son intérêt. Si vous êtes invité, vous devez accepter l'invitation dans les 30 jours, sinon votre déclaration devient nulle. Vous déposez ensuite votre demande de sélection permanente avec les documents requis, dans un délai de 60 jours après l'acceptation pour la plupart des volets (un délai différent s'applique à un volet précis). Le Québec examine ensuite le dossier, puis délivre le CSQ s'il est favorable."],
 ["Programme de l'expérience québécoise (PEQ)", "Pour les travailleurs étrangers temporaires et les diplômés étrangers d'un établissement du Québec. Les demandes étaient acceptées à partir du 2 juillet 2026 et la période de réception est fermée depuis le 31 octobre 2026. Aucune décision n'a été annoncée sur une future période de réception."],
])}
<p class="note" style="margin-top:18px">Ces programmes changent souvent : l'état indiqué est celui du 5 novembre 2026. Avant toute décision, vérifiez avec nous leur situation à jour.</p>
</div></section>
<section class="sp alt"><div class="wrap"><h2>Comment nous vous accompagnons</h2><div class="prose">
<p>En consultation, nous regardons avec vous si votre profil correspond à un parcours de sélection par le Québec ou à une voie fédérale comme Entrée express, quels documents préparer et dans quel ordre agir. Les délais d'une invitation sont courts : préparer son dossier à l'avance fait souvent la différence. Le recours à un professionnel de l'immigration ne donne aucune priorité de traitement.</p>
<p>Si vous parlez bien français, lisez aussi notre page sur l'<a href="/entree-express-francophone-maroc/" style="text-decoration:underline">Entrée express pour les francophones</a>.</p>
<p class="note">La décision appartient uniquement aux autorités du Québec et à IRCC : nous ne pouvons ni garantir un résultat ni promettre un délai.</p></div></div></section>''',
    faq=[
        ("Quelle est la différence entre le CSQ et la résidence permanente ?", "Le CSQ est la sélection faite par le Québec. La résidence permanente est accordée ensuite par IRCC, à partir de la demande que vous déposez après avoir obtenu le CSQ."),
        ("Le PEQ est-il encore ouvert ?", "Au 5 novembre 2026, le gouvernement du Québec indique que la période de réception des demandes est fermée depuis le 31 octobre 2026 et qu'aucune décision n'a été prise sur une prochaine période."),
        ("Comment fonctionne une invitation du PSTQ ?", "Vous déclarez d'abord votre intérêt. Si vous êtes invité, vous devez accepter dans les 30 jours, puis déposer votre demande de sélection permanente dans les délais indiqués dans l'invitation."),
        ("Faut-il parler français pour immigrer au Québec ?", "Le français pèse beaucoup dans la sélection québécoise. Nous regardons avec vous ce qui s'applique à votre profil lors de la consultation."),
        ("Garantissez-vous l'obtention du CSQ ou de la résidence permanente ?", "Non. Aucun consultant sérieux ne peut garantir une décision : elle appartient uniquement aux autorités du Québec et du Canada."),
    ],
    sources=[],
    related=[("/permis-etudes-canada-maroc/", "Permis d'études depuis le Maroc"), ('/entree-express-francophone-maroc/', 'Entrée express pour les francophones')],
))


D = dict(updated='5 novembre 2026', updated_iso='2026-11-05')
NOTE_FR = '<p class="note">La décision appartient uniquement à IRCC{x} : nous ne pouvons ni garantir un résultat ni promettre un délai.</p>'

PAGES.append(dict(
    path='residence-permanente-canada/', **D,
    title="Résidence permanente au Canada depuis le Maroc : les voies possibles | ATL Canada",
    desc="Quelles voies mènent à la résidence permanente : Entrée express, candidats des provinces, Québec, parrainage familial, Atlantique. Un consultant réglementé vous aide à choisir.",
    crumb="Résidence permanente",
    eyebrow="Résidence permanente · Casablanca · Montréal",
    h1="Résidence permanente au Canada : quelle voie choisir ?",
    lede="Il n'existe pas une seule porte d'entrée vers la résidence permanente, mais plusieurs voies, avec chacune ses règles. Voici les principales et comment choisir la plus réaliste pour votre profil.",
    body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>Les principales voies</h2>
{rich(['Voie', 'En bref'], [
 ['Entrée express', "Système en ligne de gestion des demandes de trois programmes fédéraux : travailleurs qualifiés (fédéral), travailleurs de métiers spécialisés (fédéral) et catégorie de l'expérience canadienne. Les candidats sont classés par points et les mieux classés sont invités à présenter une demande.", '/entree-express-canada/'],
 ['Candidats des provinces', "Chaque province ou territoire nomme des personnes dont il a besoin, selon ses propres volets. Le Québec et le Nunavut n'ont pas ce programme.", '/candidats-provinces-canada/'],
 ['Québec', "Le Québec sélectionne lui-même une partie de ses immigrants économiques (CSQ), puis IRCC traite la résidence permanente.", '/immigration-quebec-canada/'],
 ['Parrainage familial', "Un citoyen canadien ou un résident permanent peut parrainer certains membres de sa famille : conjoint, enfants à charge, parents et grands-parents.", '/parrainage-familial-canada/'],
 ['Programme d\'immigration au Canada atlantique', "Pour les travailleurs qualifiés et les diplômés récents d'un établissement de l'Atlantique, avec une offre d'emploi d'un employeur désigné au Nouveau-Brunswick, en Nouvelle-Écosse, à l'Île-du-Prince-Édouard ou à Terre-Neuve-et-Labrador."],
])}
</div></section>
<section class="sp"><div class="wrap"><h2>Comment choisir ?</h2>
<ol class="steps">
<li><span>Faire le point sur votre profil : âge, études, expérience de travail, niveau de français et d'anglais, famille au Canada.</span></li>
<li><span>Vérifier si vous êtes admissible à un programme fédéral d'Entrée express, et à quel rang vous pourriez être classé.</span></li>
<li><span>Regarder les volets des provinces et du Québec qui correspondent à votre métier ou à votre projet.</span></li>
<li><span>Préparer les documents à l'avance (évaluation des diplômes, tests de langue, preuves d'expérience) : les délais d'une invitation sont courts.</span></li>
</ol>
<div class="prose" style="margin-top:22px"><p>Pour le détail de chaque voie, consultez nos pages sur l'<a href="/entree-express-canada/" style="text-decoration:underline">Entrée express</a>, les <a href="/candidats-provinces-canada/" style="text-decoration:underline">candidats des provinces</a>, <a href="/immigration-quebec-canada/" style="text-decoration:underline">immigrer au Québec</a> et le <a href="/parrainage-familial-canada/" style="text-decoration:underline">parrainage familial</a>. Une fois résident permanent, voyez aussi la <a href="/citoyennete-canadienne/" style="text-decoration:underline">citoyenneté canadienne</a>.</p></div>
</div></section>
<section class="sp alt"><div class="wrap"><h2>Comment nous vous accompagnons</h2><div class="prose">
<p>En consultation, nous comparons avec vous les voies possibles, nous identifions celle qui correspond le mieux à votre profil, puis nous préparons un dossier complet et cohérent avant le dépôt. Le recours à un professionnel de l'immigration ne donne aucune priorité de traitement.</p>
{NOTE_FR.format(x=', aux provinces ou au Québec selon la voie')}</div></div></section>''',
    faq=[
        ("Quelle est la meilleure voie vers la résidence permanente ?", "Cela dépend de votre profil : âge, études, expérience, langues, famille au Canada, projet de vie. C'est précisément ce que nous analysons avec vous en consultation."),
        ("Peut-on déposer dans plusieurs voies à la fois ?", "Dans certains cas oui, par exemple être dans le bassin Entrée express et obtenir une nomination provinciale. Nous regardons avec vous ce qui est possible pour votre situation."),
        ("Faut-il déjà être au Canada ?", "Pas toujours. Certaines voies s'adressent à des candidats qui vivent à l'étranger, d'autres exigent une expérience de travail au Canada, comme la catégorie de l'expérience canadienne."),
        ("La résidence permanente est-elle garantie par un consultant ?", "Non. Aucun consultant sérieux ne peut garantir une décision : elle appartient uniquement aux autorités canadiennes et québécoises."),
    ],
    sources=[],
    related=[('/entree-express-canada/', 'Entrée express'), ('/candidats-provinces-canada/', 'Candidats des provinces')],
))

PAGES.append(dict(
    path='entree-express-canada/', **D,
    title="Entrée express Canada depuis le Maroc : programmes, points et changements 2026 | ATL Canada",
    desc="Entrée express : les trois programmes, les conditions, le classement par points (SRG) et les changements officiels du 3 novembre 2026. Un consultant réglementé vous accompagne.",
    crumb="Entrée express",
    eyebrow="Entrée express · Casablanca · Montréal",
    h1="Entrée express : programmes, points et changements 2026",
    lede="Entrée express gère les demandes de résidence permanente de trois programmes fédéraux. Voici les conditions de base, comment fonctionne le classement et ce qui change depuis le 3 novembre 2026.",
    body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>Comment ça fonctionne</h2>
<ol class="steps">
<li><span>Vous créez un profil en ligne et entrez dans le bassin de candidats.</span></li>
<li><span>Vous recevez un score selon le Système de classement global (SCG), calculé à partir de points.</span></li>
<li><span>IRCC invite les candidats les mieux classés à présenter une demande de résidence permanente, par rondes d'invitations.</span></li>
<li><span>Si vous êtes invité, vous remplissez la demande, téléversez vos documents et payez les frais, puis IRCC rend sa décision.</span></li>
</ol>
</div></section>
<section class="sp"><div class="wrap"><h2>Les trois programmes</h2>
{rich(['Programme', 'Ce qu\'indique IRCC'], [
 ['Travailleurs qualifiés (fédéral)', "Au moins 1 an (ou 1 560 heures) de travail qualifié (TEER 0, 1, 2 ou 3) dans la même profession au cours des 10 dernières années ; résultats de test de langue approuvé (NCLC 7 minimum pour la première langue officielle) ; études canadiennes terminées ou diplôme étranger avec évaluation (ECA) ; 67 points sur 100 sur les facteurs de sélection ; fonds suffisants, sauf exception."],
 ['Métiers spécialisés (fédéral)', "Au moins 2 ans de travail à temps plein (ou 3 120 heures) dans un métier spécialisé au cours des 5 dernières années ; une offre d'emploi à temps plein d'au moins 1 an ou un certificat de qualification canadien dans le métier ; test de langue approuvé."],
 ["Catégorie de l'expérience canadienne", "Au moins 1 an (ou 1 560 heures) de travail qualifié (TEER 0, 1, 2 ou 3) au Canada au cours des 3 dernières années, avec un statut temporaire qui permettait de travailler ; test de langue approuvé. Aucune exigence de scolarité."],
])}
<p class="note" style="margin-top:18px">Dans tous les cas, vous devez être admissible au Canada et prévoir vivre hors du Québec (le Québec a sa propre sélection).</p>
</div></section>
<section class="sp alt"><div class="wrap"><h2>Ce qui change depuis le 3 novembre 2026</h2><div class="prose">
<p>Selon IRCC (annonce du 16 octobre 2026), le système donne désormais des points supplémentaires pour une expérience de travail canadienne admissible ou une offre d'emploi admissible dans une profession à salaire élevé (une profession dont le salaire médian est au moins 1,3 fois celui de l'ensemble des travailleurs canadiens). Une EIMT n'est plus nécessaire pour qu'une offre d'emploi donne ces points ou réponde aux exigences d'offre d'emploi des programmes fédéral des travailleurs qualifiés et fédéral des métiers spécialisés.</p>
<p>Les scores des candidats déjà dans le bassin sont recalculés automatiquement. IRCC précise que le recalcul peut prendre jusqu'à deux semaines et que les rondes d'invitations sont suspendues pendant ce temps. Pour recevoir les points d'offre d'emploi, il fallait mettre son profil à jour avant le 3 novembre.</p>
</div>
<div style="margin-top:22px"></div>
{rich(['Barème IRCC', 'Points'], [
 ["Offre d'emploi admissible", "100 points si la profession a un salaire médian d'au moins 2 fois le salaire médian moyen ; 70 points entre 1,5 et 2 fois ; 50 points entre 1,3 et 1,5 fois ; 0 point pour une profession qui n'est pas à salaire élevé."],
 ["Expérience canadienne dans une profession à salaire élevé", "En plus des points de durée de travail, au moins 12 mois (1 560 heures) d'expérience admissible donnent 70 points (au moins 2 fois), 40 points (au moins 1,5 fois) ou 20 points (au moins 1,3 fois)."],
 ["EIMT", "N'est plus nécessaire et ne donne plus de points supplémentaires ni de priorité."],
])}
<div class="prose" style="margin-top:18px"><p class="note">Ces règles évoluent : l'état indiqué est celui du 5 novembre 2026. Vérifiez avec nous votre situation à jour.</p></div>
</div></section>
<section class="sp"><div class="wrap"><h2>Comment nous vous accompagnons</h2><div class="prose">
<p>En consultation, nous vérifions à quels programmes vous êtes admissible, nous estimons votre classement, nous identifions les points faciles à améliorer (langues, évaluation des diplômes, offre d'emploi) et nous préparons votre profil et vos documents. Si vous parlez bien français, lisez aussi notre page sur l'<a href="/entree-express-francophone-maroc/" style="text-decoration:underline">Entrée express pour les francophones</a>.</p>
{NOTE_FR.format(x='')}</div></div></section>''',
    faq=[
        ("Quels programmes sont gérés par Entrée express ?", "Le programme des travailleurs qualifiés (fédéral), le programme des travailleurs de métiers spécialisés (fédéral) et la catégorie de l'expérience canadienne. Une partie du Programme des candidats des provinces y est aussi liée."),
        ("Faut-il avoir travaillé au Canada ?", "Pas pour les travailleurs qualifiés (fédéral), qui peuvent compter l'expérience acquise à l'étranger. C'est en revanche obligatoire pour la catégorie de l'expérience canadienne."),
        ("Une EIMT est-elle toujours nécessaire pour une offre d'emploi ?", "Selon IRCC, depuis le 3 novembre 2026, une EIMT n'est plus nécessaire pour qu'une offre d'emploi donne les nouveaux points ou satisfasse aux exigences d'offre d'emploi des programmes fédéral des travailleurs qualifiés et fédéral des métiers spécialisés."),
        ("Que signifie « profession à salaire élevé » ?", "Selon IRCC, c'est une profession dont le salaire médian est au moins 1,3 fois celui de l'ensemble des travailleurs canadiens. IRCC publie et tient à jour la liste."),
        ("Garantissez-vous une invitation ?", "Non. IRCC invite les candidats les mieux classés lors des rondes : personne ne peut garantir une invitation ni un résultat."),
    ],
    sources=[],
    related=[('/entree-express-francophone-maroc/', 'Entrée express pour les francophones'), ('/residence-permanente-canada/', 'Résidence permanente')],
))

PAGES.append(dict(
    path='candidats-provinces-canada/', **D,
    title="Candidats des provinces au Canada depuis le Maroc : comment ça marche | ATL Canada",
    desc="Le Programme des candidats des provinces : deux processus (Entrée express ou non), rôle de chaque province, étapes. Un consultant réglementé vous explique.",
    crumb="Candidats des provinces",
    eyebrow="Provinces · Casablanca · Montréal",
    h1="Programme des candidats des provinces",
    lede="Chaque province ou territoire peut nommer des personnes qui ont les compétences dont elle a besoin et qui veulent s'y établir. Voici comment fonctionne cette voie vers la résidence permanente.",
    body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>Ce qu'il faut savoir</h2>
{rich(['Point', 'Ce qu\'indique IRCC'], [
 ['Qui décide ?', "Chaque province ou territoire fixe ses propres critères et ses propres volets, ainsi que le nombre de personnes qu'il peut nommer chaque année."],
 ['Où ?', "Vous devez prévoir vous établir dans la province ou le territoire qui vous nomme. Le Québec et le Nunavut n'ont pas de programme : voyez notre page sur l'<a href=\"/immigration-quebec-canada/\" style=\"text-decoration:underline\">immigration au Québec</a>."],
 ['Deux processus', "Le processus lié à Entrée express : vous répondez à la fois aux critères d'un volet provincial et d'un programme fédéral d'Entrée express. Le processus hors Entrée express : vous répondez à un volet provincial, mais pas à un programme fédéral d'Entrée express."],
 ['Après la nomination', "Dans le processus lié à Entrée express, une fois nommé, vous créez un profil Entrée express et recevez 600 points supplémentaires, ce qui vous aide à être invité à présenter une demande de résidence permanente."],
])}
</div></section>
<section class="sp"><div class="wrap"><h2>Les étapes</h2>
<ol class="steps">
<li><span>Choisir une province ou un territoire et consulter ses volets.</span></li>
<li><span>Identifier votre voie : selon que vous êtes aussi admissible à un programme fédéral d'Entrée express ou non.</span></li>
<li><span>Déposer votre demande selon la procédure de la province, qui vous indique si elle passe par Entrée express ou non.</span></li>
<li><span>Une fois nommé, déposer votre demande de résidence permanente auprès d'IRCC, qui vérifie notamment l'admissibilité (médicale, sécurité, criminalité).</span></li>
</ol>
<div class="prose" style="margin-top:22px"><p>Les délais varient selon le type de demande, la complétude du dossier et la rapidité de vos réponses. Voyez aussi la page de la <a href="/residence-permanente-canada/" style="text-decoration:underline">résidence permanente</a> pour comparer les voies.</p></div>
</div></section>
<section class="sp alt"><div class="wrap"><h2>Comment nous vous accompagnons</h2><div class="prose">
<p>En consultation, nous regardons avec vous quelles provinces correspondent à votre métier et à votre projet, quelle voie est la plus réaliste, et quels documents préparer d'avance. Le recours à un professionnel de l'immigration ne donne aucune priorité de traitement.</p>
{NOTE_FR.format(x=' et à la province concernée')}</div></div></section>''',
    faq=[
        ("Peut-on choisir n'importe quelle province ?", "Chaque province a ses propres volets et critères. Vous devez prévoir vous établir dans la province qui vous nomme. Le Québec et le Nunavut n'ont pas de programme."),
        ("Que sont les 600 points supplémentaires ?", "Dans le processus lié à Entrée express, une personne nommée par une province reçoit 600 points supplémentaires une fois son profil créé. Cela l'aide à être invitée à présenter une demande."),
        ("Une nomination garantit-elle la résidence permanente ?", "Non. La nomination est une étape. C'est ensuite IRCC qui décide de la résidence permanente."),
        ("Et le Programme d'immigration au Canada atlantique ?", "C'est un programme distinct pour les travailleurs qualifiés et les diplômés récents des quatre provinces de l'Atlantique, avec une offre d'emploi d'un employeur désigné."),
    ],
    sources=[],
    related=[('/entree-express-canada/', 'Entrée express'), ('/residence-permanente-canada/', 'Résidence permanente')],
))

PAGES.append(dict(
    path='citoyennete-canadienne/', **D,
    title="Citoyenneté canadienne : conditions pour les résidents permanents | ATL Canada",
    desc="Devenir citoyen canadien : 1 095 jours de présence, impôts, langue. Les conditions officielles pour les adultes résidents permanents.",
    crumb="Citoyenneté canadienne",
    eyebrow="Citoyenneté · Casablanca · Montréal",
    h1="Citoyenneté canadienne : les conditions pour les adultes",
    lede="Après la résidence permanente, la citoyenneté est l'étape suivante pour beaucoup de familles. Voici les conditions officielles à vérifier avant de présenter une demande.",
    body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>Les conditions pour un adulte (18 ans et plus)</h2>
{rich(['Condition', 'Ce qu\'indique IRCC'], [
 ['Statut de résident permanent', "Vous devez être résident permanent, sans condition non remplie, et votre statut ne doit pas faire l'objet d'un examen en matière d'immigration ou de fraude ni d'une mesure de renvoi."],
 ['Présence physique', "1 095 jours au Canada comme résident permanent au cours des 5 ans précédant la demande. Le temps passé comme résident temporaire ou personne protégée avant la résidence permanente compte pour une demi-journée, jusqu'à un maximum de 365 jours. Le temps passé en prison, en probation ou en libération conditionnelle au Canada ne compte généralement pas."],
 ['Impôts', "Avoir produit ses déclarations de revenus pour 3 années d'imposition situées en tout ou en partie dans les 5 ans précédant la demande."],
 ['Langue', "Les 18 à 54 ans doivent prouver une capacité en français ou en anglais au niveau NCLC 4 ou plus. Les 55 ans et plus et les 17 ans et moins en sont exemptés, de même que les personnes sourdes qui ne peuvent fournir de preuve. Une dispense pour motifs d'ordre humanitaire est possible."],
])}
<p class="note" style="margin-top:18px">D'autres motifs peuvent empêcher une demande, par exemple des accusations criminelles en cours, certaines condamnations, ou un refus ou une révocation antérieurs de la citoyenneté.</p>
</div></section>
<section class="sp"><div class="wrap"><h2>Comment nous vous accompagnons</h2><div class="prose">
<p>Avant de déposer, nous vérifions avec vous le calcul de vos jours de présence, vos déclarations de revenus et votre preuve de langue, et nous préparons une demande complète. Les règles de citoyenneté ont changé en 2025 : nous vérifions avec vous ce qui s'applique à votre cas, notamment si vous êtes parent ou enfant d'un citoyen.</p>
<p>Si vous n'êtes pas encore résident permanent, voyez notre page sur la <a href="/residence-permanente-canada/" style="text-decoration:underline">résidence permanente</a>.</p>
{NOTE_FR.format(x='')}</div></div></section>''',
    faq=[
        ("Combien de jours faut-il avoir passé au Canada ?", "1 095 jours comme résident permanent au cours des 5 ans précédant la demande, avec une possibilité de crédit partiel pour le temps passé comme résident temporaire ou personne protégée avant la résidence permanente."),
        ("Faut-il avoir payé des impôts ?", "Oui. Vous devez avoir produit vos déclarations de revenus pour 3 années d'imposition situées en tout ou en partie dans les 5 ans précédant la demande."),
        ("Quel niveau de langue faut-il ?", "Les 18 à 54 ans doivent prouver le niveau NCLC 4 ou plus en français ou en anglais. Les 55 ans et plus en sont exemptés."),
        ("Garantissez-vous l'obtention de la citoyenneté ?", "Non. Aucun consultant sérieux ne peut garantir une décision : elle appartient uniquement à IRCC."),
    ],
    sources=[],
    related=[('/residence-permanente-canada/', 'Résidence permanente'), ('/parrainage-familial-canada/', 'Parrainage familial')],
))


PAGES.append(dict(
    path='gens-affaires-immigration-canada/', updated='5 novembre 2026', updated_iso='2026-11-05',
    title="Immigration des gens d'affaires au Canada et au Québec : où en sont les programmes | ATL Canada",
    desc="Visa pour démarrage d'entreprise, travailleurs autonomes, programmes d'affaires du Québec : l'état officiel des programmes et les autres voies possibles. Un consultant réglementé vous aide à choisir.",
    crumb="Gens d'affaires",
    eyebrow="Gens d'affaires · Casablanca · Montréal",
    h1="Immigration des gens d'affaires : où en sont les programmes ?",
    lede="Les programmes d'immigration pour entrepreneurs et investisseurs changent beaucoup. Voici l'état indiqué par les gouvernements du Canada et du Québec, et les autres voies à envisager.",
    body=f'''{TRUST}
<section class="sp alt"><div class="wrap"><h2>Au niveau fédéral</h2>
{rich(['Programme', "Ce qu'indique IRCC"], [
 ["Visa pour démarrage d'entreprise", "IRCC a cessé d'accepter les nouvelles demandes le 31 décembre 2025, sauf pour les personnes qui avaient reçu en 2025 un engagement valide d'un organisme désigné. La page du programme indique aussi une date limite au 30 juin 2026 pour ces personnes : vérifiez l'état à jour avant d'agir. L'entreprise doit être située hors Québec."],
 ['Travailleurs autonomes', "La suspension de la réception des demandes est prolongée « jusqu'à nouvel ordre »."],
 ['Et ensuite ?', "IRCC prévoit remplacer ces programmes par un nouveau programme pilote ciblé pour les entrepreneurs immigrants. Les détails doivent être publiés en 2026."],
])}
</div></section>
<section class="sp"><div class="wrap"><h2>Au Québec</h2><div class="prose">
<p>Le Québec choisit lui-même les gens d'affaires qui s'y établissent : il faut d'abord obtenir un Certificat de sélection du Québec (CSQ), puis IRCC traite la résidence permanente. Depuis le 1er janvier 2024, la réforme des programmes d'investisseurs, d'entrepreneurs et de travailleurs autonomes exige notamment une connaissance satisfaisante du français pour s'établir au Québec. Voyez aussi notre page sur <a href="/immigration-quebec-canada/" style="text-decoration:underline">immigrer au Québec</a>.</p>
</div></div></section>
<section class="sp alt"><div class="wrap"><h2>Les autres voies à envisager</h2>
{rich(['Voie', 'En bref'], [
 ['Permis de travail', "Selon votre situation, un permis de travail peut permettre de travailler au Canada.", '/permis-de-travail-canada/'],
 ["Entrée express", "Si votre profil de travailleur qualifié le permet, c'est souvent une voie plus réaliste.", '/entree-express-canada/'],
 ['Candidats des provinces', "Chaque province fixe ses propres volets et critères.", '/candidats-provinces-canada/'],
])}
</div></section>
<section class="sp"><div class="wrap"><h2>Comment nous vous accompagnons</h2><div class="prose">
<p>En consultation, nous faisons le point sur votre projet, nous vérifions l'état à jour des programmes avant toute dépense, et nous comparons les voies réalistes pour votre profil. Le recours à un professionnel de l'immigration ne donne aucune priorité de traitement.</p>
<p class="note">La décision appartient uniquement à IRCC et aux autorités du Québec : nous ne pouvons ni garantir un résultat ni promettre un délai.</p></div></div></section>''',
    faq=[
        ("Le visa pour démarrage d'entreprise est-il encore ouvert ?", "Selon IRCC, les nouvelles demandes ne sont plus acceptées depuis le 31 décembre 2025, sauf pour les personnes qui avaient reçu un engagement valide en 2025. Vérifiez l'état à jour avec nous."),
        ("Le programme des travailleurs autonomes est-il ouvert ?", "Selon IRCC, la réception des demandes est suspendue jusqu'à nouvel ordre."),
        ("Que remplacera ces programmes ?", "IRCC prévoit un nouveau programme pilote ciblé pour les entrepreneurs immigrants, dont les détails doivent être publiés en 2026."),
        ("Faut-il parler français pour immigrer au Québec comme gens d'affaires ?", "Oui : depuis la réforme du 1er janvier 2024, une connaissance satisfaisante du français est exigée pour s'établir au Québec comme investisseur, entrepreneur ou travailleur autonome."),
        ("Garantissez-vous un résultat ?", "Non. Aucun consultant sérieux ne peut garantir une décision : elle appartient uniquement aux autorités canadiennes et québécoises."),
    ],
    sources=[],
    related=[('/residence-permanente-canada/', 'Résidence permanente'), ('/immigration-quebec-canada/', 'Immigrer au Québec')],
))


AR_OF = {'gens-affaires-immigration-canada/': 'ar/business-immigration/', 'residence-permanente-canada/': 'ar/permanent-residence/', 'entree-express-canada/': 'ar/express-entry/', 'candidats-provinces-canada/': 'ar/provincial-nominee/', 'citoyennete-canadienne/': 'ar/canadian-citizenship/', 'visa-visiteur-super-visa-canada/': 'ar/visitor-visa-super-visa/', 'parrainage-familial-canada/': 'ar/family-sponsorship/', 'permis-de-travail-canada/': 'ar/work-permit/', 'immigration-quebec-canada/': 'ar/immigrate-to-quebec/', 'permis-etudes-canada-maroc/': 'ar/study-permit-morocco/', 'entree-express-francophone-maroc/': 'ar/express-entry-french/', 'documents-maroc-immigration-canada/': 'ar/moroccan-documents/'}


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
    alt = f'<link rel="alternate" hreflang="fr-MA" href="{url}">\n'
    if AR_OF.get(p['path']): alt += f'<link rel="alternate" hreflang="ar-MA" href="{SITE}/{AR_OF[p["path"]]}">\n'
    alt += f'<link rel="alternate" hreflang="x-default" href="{url}">\n'
    h = re.sub(r'(<link rel="canonical" href="[^"]*">\n?)', lambda m: m.group(1) + alt, h, count=1)
    # JSON-LD
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    g = json.loads(m.group(1))
    keep = [n for n in g['@graph'] if n['@type'] in ('ProfessionalService', 'WebSite')]
    keep += [
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": p['title'], "description": p['desc'],
         "inLanguage": "fr-MA", "dateModified": p.get("updated_iso", UPDATED), "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#organization"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
            *([] if p.get("neutral") else [
            {"@type": "ListItem", "position": 2, "name": "Immigrer depuis le Maroc", "item": SITE + "/maroc/"}]),
            {"@type": "ListItem", "position": 2 if p.get("neutral") else 3, "name": p['crumb'], "item": url}]},
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
  <p class="crumb"><a href="/">Accueil</a> › {'' if p.get('neutral') else '<a href="/maroc/">Immigrer depuis le Maroc</a> › '}{e(p['crumb'])}</p>
  <p class="eyebrow">{e(p['eyebrow'])}</p>
  <h1>{e(p['h1'])}</h1>
  <p class="lede">{e(p['lede'])}</p>
</div></section>
{p['body'].replace(TRUST, '', 1)}
{TRUST}
<section class="sp alt" id="faq"><div class="wrap"><h2>Questions fréquentes</h2><div class="faq-list">{faq_html(p['faq'])}</div></div></section>
<section class="sp"><div class="wrap">{('<h2>Sources officielles</h2><ul class="sources">' + src + '</ul>') if src else ''}
<p class="note" style="margin-top:18px">Dernière mise à jour : {p.get('updated', '26 octobre 2026')}.</p>
<div class="related">{related}</div></div></section>
{offices}
{footer}'''
    os.makedirs(R + p['path'], exist_ok=True)
    open(R + p['path'] + 'index.html', 'w', encoding='utf-8').write(page)
    print('ok', p['path'], len(page), 'octets')
