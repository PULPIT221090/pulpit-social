# Pulpit creative kit

Renders brand-consistent 1080x1350 post creatives, covers and highlight icons with Playwright + Lucide icons.

Setup (fresh container):
    cd tools/kit && npm i lucide-static@latest
    pip install playwright pillow  (Playwright + Chromium are preinstalled in Claude sessions)

Usage:
    python3 posts.py            # renders every entry in cal.py to creatives/render/
    python3 posts.py 3 7        # only entries 3 and 7
    python3 covers.py           # LinkedIn + Facebook covers
    python3 build.py            # highlight covers, profile picture, templates

Templates (cal.py `t` field): insight (ink), checklist / steps (ivory), route (teal gradient), poll (deep), review (ivory + quote), occasion (ivory + badge).
Fields: d (date), t, kicker, title, sub | points[] | options[] | stat1/stat2, ig, fb, li (None = skip LinkedIn), tags.
Rules: real Pulpit logo always; no prices/₹/discounts; max ~20 words on-creative; Poppins only.
Publish: copy renders to creatives/YYYY-MM/, git push, then Zoho uploadSocialMediaFromUrl with the raw.githubusercontent.com URL.
