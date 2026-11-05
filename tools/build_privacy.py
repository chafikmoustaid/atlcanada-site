#!/usr/bin/env python3
"""Génère /confidentialite/index.html (politique de confidentialité) à partir de l'en-tête de la page Actualités."""
import re, os, html
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
SITE = 'https://www.atlcanada.com'
src = open(R + 'actualites/index.html', encoding='utf-8').read()
head, rest = src.split('<main>', 1)
foot = rest[rest.index('</main>'):]
TITLE = 'Politique de confidentialité | ATL Canada'
DESC = "Comment ATL Canada recueille, utilise et protège vos renseignements personnels (Loi 25 du Québec) : formulaire de contact, téléphone, WhatsApp."
url = SITE + '/confidentialite/'
e = html.escape
head = re.sub(r'<title>.*?</title>', f'<title>{e(TITLE)}</title>', head, flags=re.S)
head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + e(DESC), head)
head = head.replace(f'{SITE}/actualites/', url)
head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + e(TITLE), head)
head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + e(DESC), head)
head = re.sub(r'(<meta name="twitter:title" content=")[^"]*', lambda m: m.group(1) + e(TITLE), head)
head = re.sub(r'(<meta name="twitter:description" content=")[^"]*', lambda m: m.group(1) + e(DESC), head)
head = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', '', head)
head = re.sub(r'<script type="application/ld\+json">.*?</script>',
  '<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebPage","name":"Politique de confidentialité","url":"%s","inLanguage":"fr-CA","isPartOf":{"@id":"%s/#website"}}</script>' % (url, SITE), head, flags=re.S)
body = '''<main>
<section class="pg-hero"><div class="wrap">
  <p class="crumbs"><a href="/">Accueil</a> › Confidentialité</p>
  <h1>Politique de confidentialité</h1>
  <p class="lede">Ce que nous recueillons, pourquoi, et comment vous gardez le contrôle de vos renseignements. Dernière mise à jour : 5 novembre 2026.</p>
</div></section>
<section class="news-page"><div class="wrap legal">
<h2>Qui sommes-nous</h2>
<p>ATL Canada est un cabinet de consultation en immigration canadienne, dont le consultant réglementé est titulaire du permis R712906 du Collège des consultants en immigration et en citoyenneté (CCIC), avec des bureaux à Montréal et à Casablanca. Pour toute question sur vos renseignements personnels, écrivez à <a href="mailto:contact@atlcanada.com">contact@atlcanada.com</a> ou appelez le <a href="tel:+15142956635">+1 514 295 6635</a>.</p>
<h2>Ce que nous recueillons</h2>
<ul>
<li><strong>Formulaire de contact</strong> : votre prénom, votre nom, votre courriel et le message que vous écrivez. Nous vous demandons de ne pas y joindre de documents d'identité ni de détails sensibles : nous vous les demanderons au besoin par un canal approprié.</li>
<li><strong>Téléphone, courriel et WhatsApp</strong> : les renseignements que vous choisissez de nous communiquer en nous écrivant ou en nous appelant.</li>
</ul>
<h2>Pourquoi nous les utilisons</h2>
<p>Uniquement pour répondre à votre demande, vous proposer un rendez-vous et, si vous devenez client, ouvrir et gérer votre dossier. Nous ne vendons pas vos renseignements et nous ne les utilisons pas pour de la publicité.</p>
<h2>Services tiers</h2>
<ul>
<li><strong>FormSubmit</strong> (formsubmit.co) transmet les messages du formulaire à notre boîte courriel.</li>
<li><strong>Google Fonts</strong> et <strong>Pexels</strong> fournissent les polices et certaines photos du site : votre navigateur contacte leurs serveurs, qui peuvent voir votre adresse IP.</li>
<li><strong>WhatsApp, Facebook et Instagram</strong> : si vous cliquez sur ces liens, vous quittez notre site et leurs propres politiques s'appliquent.</li>
</ul>
<p>Ce site n'utilise actuellement ni témoin (cookie) de publicité ni outil de suivi des visiteurs.</p>
<h2>Conservation et sécurité</h2>
<p>Nous conservons vos renseignements le temps nécessaire pour traiter votre demande et assurer le suivi de votre dossier, puis nous les supprimons ou les anonymisons. Le site est servi en HTTPS avec des en-têtes de sécurité, et l'accès à notre boîte courriel est limité à l'équipe d'ATL Canada.</p>
<h2>Vos droits</h2>
<p>Vous pouvez nous demander d'accéder à vos renseignements, de les corriger, de les supprimer ou de retirer votre consentement, en nous écrivant à <a href="mailto:contact@atlcanada.com">contact@atlcanada.com</a>. Au Québec, la Loi sur la protection des renseignements personnels dans le secteur privé (Loi 25) s'applique; vous pouvez aussi vous adresser à la <a href="https://www.cai.gouv.qc.ca/" rel="noopener" target="_blank">Commission d'accès à l'information du Québec</a>.</p>
<p class="news-sources">Cette politique est une information générale et peut être mise à jour : la date en haut de page indique la dernière version.</p>
</div></section>
'''
open(R + 'confidentialite/index.html', 'w', encoding='utf-8').write(head + body + foot) if os.makedirs(R + 'confidentialite', exist_ok=True) is None else None
print('ok confidentialite')
