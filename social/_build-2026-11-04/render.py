import os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__))
with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_page(viewport={"width": 1080, "height": 1920})
    for n in range(1, 7):
        pg.goto(f"file://{D}/s{n}.html")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(500)
        pg.screenshot(path=f"{D}/s{n}.png")
    br.close()
