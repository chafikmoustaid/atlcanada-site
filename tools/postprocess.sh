#!/bin/sh
# À lancer après build_news.py / build_pages.py / build_pages_ar.py, dans cet ordre.
cd "$(dirname "$0")/.." || exit 1
python3 tools/build_privacy.py
python3 tools/contact_icons.py
python3 tools/icons_v2.py
python3 tools/contact_band.py
python3 tools/cta_circles.py
python3 tools/header_social.py
python3 tools/site_extras.py
python3 tools/calc_promo.py
