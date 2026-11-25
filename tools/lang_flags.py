# Idempotent: renders header language links as plain codes EN / FR and العربية (no flags).
import re, glob
FL = {
 'en': '<svg class="fl" viewBox="0 0 60 30" aria-hidden="true"><clipPath id="ukc"><path d="M0 0h60v30H0z"/></clipPath><g clip-path="url(#ukc)"><path fill="#012169" d="M0 0h60v30H0z"/><path stroke="#fff" stroke-width="6" d="M0 0l60 30M60 0L0 30"/><path stroke="#C8102E" stroke-width="4" d="M0 0l60 30M60 0L0 30"/><path stroke="#fff" stroke-width="10" d="M30 0v30M0 15h60"/><path stroke="#C8102E" stroke-width="6" d="M30 0v30M0 15h60"/></g></svg>',
 'fr': '<svg class="fl" viewBox="0 0 3 2" aria-hidden="true"><path fill="#ED2939" d="M0 0h3v2H0z"/><path fill="#fff" d="M0 0h2v2H0z"/><path fill="#002395" d="M0 0h1v2H0z"/></svg>',
 'ar': '<svg class="fl" viewBox="0 0 3 2" aria-hidden="true"><path fill="#C1272D" d="M0 0h3v2H0z"/><path fill="none" stroke="#006233" stroke-width=".07" d="M1.5 .55l.22.67-.57-.41h.7l-.57.41z"/></svg>',
}
LABEL = {'en': 'EN', 'fr': 'FR', 'ar': 'العربية'}
region = re.compile(r'(<span class="lang"[^>]*>)(.*?)(</a></span>)', re.S)
anchor = re.compile(r'(<a [^>]*?\blang="(en|fr|ar)"[^>]*>)(.*?)(</a>)', re.S)
def fix_a(m):
    k = m.group(2)
    return m.group(1) + '<span class="l-code">' + LABEL[k] + '</span>' + m.group(4)
def fix_region(m):
    inner = m.group(2) + '</a>'
    inner = anchor.sub(fix_a, inner)
    return m.group(1) + inner[:-4] + m.group(3)
n = 0
for f in glob.glob('**/*.html', recursive=True):
    s = open(f, encoding='utf-8').read()
    if 'class="lang"' not in s: continue
    t = region.sub(fix_region, s)
    if t != s: open(f, 'w', encoding='utf-8').write(t); n += 1
print('lang_flags:', n, 'files')
