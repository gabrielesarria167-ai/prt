# Carrozzeria PRT – sito web

Static multi-page website for **CARROZZERIA P.R.T. s.r.l.s. unipersonale** (Isola della Scala, VR).
It's in Italian, inspired by carrozzeriascaligera.it, and only lets visitors **call, email or message on WhatsApp**: no forms, no cookies, no third-party scripts or fonts.

## Build

```sh
python3 build.py                         # writes the site to ./public
python3 -m http.server -d public 8000    # preview at http://localhost:8000
```

Only the Python 3 standard library is required. Deploy the contents of `public/` to any static host (Netlify, Cloudflare Pages, GitHub Pages, shared hosting…). Configure the host to serve `404.html` for missing pages.

## Structure

```
build.py            # tiny static-site builder + business data (phone, email, VAT…)
src/layout.html     # shared <head>, top bar, header/nav, footer, mobile action bar
src/partials/       # reusable blocks: icons, services cards, partner logos, CTA bands
src/pages/*.html    # one file per page, with a short front-matter block (title, description, nav)
static/             # css, js, fonts (self-hosted Roboto), images, partner logos – copied as-is
prt_assets/         # original material supplied by the client
```

- **Contact details** live in `SITE` inside `build.py`. Change them there and rebuild.
- In pages and partials, `{{ key }}` inserts a value from `SITE` and `{% include name %}` inserts `src/partials/name.html`.
- Photos are Unsplash stock images (see `static/img/CREDITS.md`). Replace them with real workshop photos and keep the same filenames.
- `site_url` in `build.py` (used for canonical/OG tags) is a placeholder: set it to the real domain.
