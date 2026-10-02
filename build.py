#!/usr/bin/env python3
"""Build the static PRT website into ./public.

Pages live in src/pages/*.html. Each starts with a small front-matter block:

    ---
    title: Titolo della pagina
    description: Meta description
    nav: servizi
    ---

and is wrapped in src/layout.html. Inside pages, partials and layout:
  {% include name %}  -> contents of src/partials/name.html
  {{ key }}           -> value from SITE below (or the page's front matter)

Only the Python standard library is used:  python3 build.py
"""
import hashlib
import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
STATIC = ROOT / "static"
OUT = ROOT / "public"

# Single source of truth for business data (from prt_assets/data.md).
SITE = {
    "name": "Carrozzeria P.R.T.",
    "legal_name": "CARROZZERIA P.R.T. s.r.l.s. unipersonale",
    "street": "Via Alessandro Pompei 5",
    "zip": "37063",
    "city": "Isola della Scala",
    "province": "VR",
    "vat": "04430910234",
    "phone": "045 730 1121",
    "phone_href": "tel:+390457301121",
    "mobile": "348 248 6842",
    "mobile_href": "tel:+393482486842",
    # WhatsApp links with a pre-filled first message
    "whatsapp_href": "https://wa.me/393482486842?text="
    + "Buongiorno%20Carrozzeria%20PRT%2C%20vorrei%20alcune%20informazioni.",
    "whatsapp_repair_href": "https://wa.me/393482486842?text="
    + "Buongiorno%20Carrozzeria%20PRT%2C%20vorrei%20informazioni%20per%20una%20riparazione.",
    "whatsapp_sos_href": "https://wa.me/393482486842?text="
    + "Buongiorno%20Carrozzeria%20PRT%2C%20ho%20bisogno%20del%20soccorso%20stradale.",
    "fax": "045 664 0099",
    "email": "carrozzeriaprt@autorepair.it",
    "email_href": "mailto:carrozzeriaprt@autorepair.it"
    + "?subject=Richiesta%20informazioni%20dal%20sito",
    "maps_href": "https://www.google.com/maps/search/?api=1&query="
    + "Carrozzeria+PRT+Via+Alessandro+Pompei+5+37063+Isola+della+Scala+VR",
    "site_url": "https://www.carrozzeriaprt.it",
    "year": str(date.today().year),
}

FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
INCLUDE = re.compile(r"{%\s*include\s+([\w-]+)\s*%}")
VAR = re.compile(r"{{\s*([\w-]+)\s*}}")


def expand_includes(text, depth=0):
    if depth > 5:
        raise RuntimeError("include nesting too deep")
    return INCLUDE.sub(
        lambda m: expand_includes((SRC / "partials" / f"{m[1]}.html").read_text(), depth + 1),
        text,
    )


def render(text, ctx, source):
    def sub(m):
        if m[1] not in ctx:
            raise KeyError(f"{source}: unknown variable {{{{ {m[1]} }}}}")
        return ctx[m[1]]

    return VAR.sub(sub, text)


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(STATIC, OUT, ignore=shutil.ignore_patterns(".DS_Store", "*.md"))

    layout = (SRC / "layout.html").read_text()
    # Cache-busting: append a content hash to the stylesheet and script URLs
    for asset in ("css/style.css", "js/main.js"):
        digest = hashlib.sha1((STATIC / asset).read_bytes()).hexdigest()[:8]
        layout = layout.replace(f'"{asset}"', f'"{asset}?v={digest}"')
    pages = sorted((SRC / "pages").glob("*.html"))
    for page in pages:
        raw = page.read_text()
        m = FRONT_MATTER.match(raw)
        if not m:
            raise ValueError(f"{page.name}: missing front matter")
        meta = dict(
            line.split(":", 1) for line in m[1].splitlines() if line.strip()
        )
        meta = {k.strip(): v.strip() for k, v in meta.items()}
        slug = page.stem
        ctx = {
            **SITE,
            "nav": "",
            **meta,
            "slug": slug,
            "canonical": SITE["site_url"] + ("/" if slug == "index" else f"/{slug}.html"),
        }
        # Mark the active nav item: {{ nav_servizi }} -> ' aria-current="page"'
        for key in ("home", "chi-siamo", "servizi", "convenzioni", "contatti"):
            ctx[f"nav_{key}"] = ' aria-current="page"' if ctx["nav"] == key else ""
        # ...and the current page in sub-lists: {{ cur_lucidatura }}
        for other in pages:
            ctx[f"cur_{other.stem}"] = ' aria-current="page"' if other.stem == slug else ""
        body = expand_includes(raw[m.end():])
        html = expand_includes(layout).replace("{% content %}", body)
        (OUT / page.name).write_text(render(html, ctx, page.name))
    print(f"Built {len(pages)} pages into {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    build()
