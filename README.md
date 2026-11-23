# Fixed by Perri — fixedbyperri.com

Static website for Fixed by Perri, locally owned appliance repair in Pinal County, AZ (Florence, Coolidge, Casa Grande, Maricopa). Built by Building Futures AI.

## Deploy notes (Cloudflare Pages)

Folder layout:
- site/        -> the website (build output directory)
- functions/   -> Pages Function for the form (POST /api/lead)
- build.py     -> regenerates site/ from the content in this file (python3 build.py)

## Deploy
From this folder:  npx wrangler pages deploy site --project-name fixedbyperri
(Run from this folder so wrangler picks up ./functions. Dashboard drag-and-drop does NOT upload functions.)
Then add custom domain fixedbyperri.com in Pages > Custom domains and repoint DNS away from GHL.

## Form setup (Pages > Settings > Environment variables)
- LEAD_WEBHOOK_URL  CRM inbound webhook (optional)
- RESEND_API_KEY    Resend key for email alerts (optional)
- LEAD_EMAIL_TO     defaults to fixedbyperri@gmail.com
- LEAD_EMAIL_FROM   verified Resend sender, e.g. Fixed by Perri <leads@fixedbyperri.com>
At least one of webhook / Resend must be set or the form shows the "please call" fallback.

## Included
- 16 pages: home, about, services hub + 6 services, service areas hub + 4 cities, contact, privacy, 404
- LocalBusiness, Service, FAQPage and Breadcrumb schema on every relevant page
- sitemap.xml, robots.txt, _redirects (old GHL /about-us, /contact-us etc. -> new URLs), _headers

## Editing
Page copy lives in `build.py`. Edit it, run `python3 build.py`, and commit the regenerated `site/` folder. Styles are in `site/css/site.css`.

Cloudflare Pages Git settings: build command empty (or `python3 build.py`), build output directory `site`.
