# Carrozzeria PRT – sito web

Static multi-page website for **CARROZZERIA P.R.T. s.r.l.s. unipersonale** (Isola della Scala, VR).
It's in Italian, inspired by carrozzeriascaligera.it, and only lets visitors **call, email or message on WhatsApp**: no forms, no cookies, no third-party scripts or fonts.

## Build

```sh
python3 build.py                         # writes the site to ./public
python3 -m http.server -d public 8000    # preview at http://localhost:8000
```

Only the Python 3 standard library is required.

## Deploy (Aruba Hosting Easy Linux – www.carrozzeriaprt.it)

1. `python3 build.py`, then zip the *contents* of `public/` (including `.htaccess`):
   `cd public && zip -qr -X ../deploy/sito-prt.zip . -x '.DS_Store'`
2. Aruba control panel → Hosting Linux → **File Manager** → folder `www.carrozzeriaprt.it` → upload `sito-prt.zip` → right-click → *Estrai Archivio* → *Qui* → *Sì* (overwrite).
3. Velocità → **Caching** → *Cancella cache*, otherwise Aruba's proxy keeps serving the old pages.

`static/.htaccess` makes `index.html` the home page (Aruba's placeholder `index.php` stays on the server but is hidden), forces HTTPS on `www.carrozzeriaprt.it`, serves `404.html`, and sets browser caching. SSL is Aruba's free certificate, already active.

Email: `assistenza@carrozzeriaprt.it` (Aruba mailbox) forwards a copy of every message to `carrozzeriaprt@autorepair.it`; manage it from Aruba Webmail → Settings → Automatic forwarding.

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
