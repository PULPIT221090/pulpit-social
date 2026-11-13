import re, json, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).parent
ICONS = ROOT / "node_modules/lucide-static/icons"
C = dict(ink="#0B2A28", deep="#123D3A", teal="#21A5A0", teal2="#50A39F",
         terra="#D06350", terra2="#B63330", ivory="#F7F3EC", gold="#C9A86A")

def icon_inner(name):
    s = (ICONS / f"{name}.svg").read_text()
    return re.search(r"<svg[^>]*>(.*)</svg>", s, re.S).group(1)

def badge(x, y, r, name, ring=C['gold']):
    k = r * 1.1 / 24
    return f"""<g transform="translate({x},{y})">
      <circle r="{r}" fill="{C['deep']}" stroke="{ring}" stroke-width="1.5" stroke-opacity=".7"/>
      <g transform="translate({-12*k},{-12*k}) scale({k})" fill="none" stroke="{C['ivory']}" stroke-width="1.6"
         stroke-linecap="round" stroke-linejoin="round">{icon_inner(name)}</g></g>"""

def pin(x, y, s, col):
    return f"""<g transform="translate({x},{y}) scale({s})"><path d="M0 0 C -14 -18 -14 -38 0 -38 C 14 -38 14 -18 0 0Z" fill="{col}"/>
      <circle cy="-26" r="5" fill="{C['ink']}"/></g>"""

def sedan(x, y, s, body=C['teal'], accent=C['ivory']):
    # side-view premium sedan, 300 wide x ~90 high at scale 1, wheels on y=0
    return f"""<g transform="translate({x},{y}) scale({s})">
      <ellipse cx="150" cy="4" rx="150" ry="7" fill="#000" opacity=".25"/>
      <path d="M8 -18 C 8 -34 22 -40 46 -42 L 86 -46 C 108 -70 132 -82 170 -82 L 206 -82 C 228 -82 246 -70 266 -48
               L 284 -44 C 296 -42 300 -34 300 -22 L 300 -12 C 300 -6 296 -4 290 -4 L 12 -4 C 9 -4 8 -8 8 -12 Z" fill="{body}"/>
      <path d="M100 -46 C 118 -66 136 -74 166 -74 L 180 -74 L 180 -46 Z" fill="{C['ink']}" opacity=".85"/>
      <path d="M188 -74 L 204 -74 C 222 -74 238 -64 252 -46 L 188 -46 Z" fill="{C['ink']}" opacity=".85"/>
      <path d="M30 -30 L 290 -30" stroke="{accent}" stroke-opacity=".35" stroke-width="2"/>
      <rect x="282" y="-36" width="16" height="6" rx="3" fill="{C['gold']}"/>
      <rect x="8" y="-34" width="10" height="6" rx="3" fill="{C['terra']}"/>
      <g fill="{C['ink']}"><circle cx="72" cy="-6" r="22"/><circle cx="238" cy="-6" r="22"/></g>
      <g fill="#C9CFCE"><circle cx="72" cy="-6" r="11"/><circle cx="238" cy="-6" r="11"/></g>
      <g fill="{C['ink']}"><circle cx="72" cy="-6" r="4"/><circle cx="238" cy="-6" r="4"/></g>
    </g>"""

def plane(x, y, s, rot=-12):
    return f"""<g transform="translate({x},{y}) rotate({rot}) scale({s})" fill="{C['ivory']}">
      <path d="M-40 0 C -40 -5 -34 -7 -26 -7 L 30 -7 C 38 -7 44 -3 46 0 C 44 3 38 7 30 7 L -26 7 C -34 7 -40 5 -40 0Z"/>
      <path d="M2 -6 L -14 -34 L -4 -34 L 20 -6Z"/><path d="M2 6 L -14 34 L -4 34 L 20 6Z"/>
      <path d="M-30 -6 L -40 -20 L -34 -20 L -22 -6Z"/></g>"""

def skyline(x0, base, w, col, op):
    # towers (GIFT City-style), a temple shikhara (Gujarat heritage), a bridge arch (Atal bridge feel)
    parts = []
    xs = [(0,40,150),(46,30,110),(82,52,210),(140,34,140),(180,26,95),(212,44,175),(262,30,120)]
    for dx, ww, hh in xs:
        parts.append(f'<rect x="{x0+dx}" y="{base-hh}" width="{ww}" height="{hh}" rx="2"/>')
        for row in range(base-hh+14, base-10, 18):
            parts.append(f'<rect x="{x0+dx+6}" y="{row}" width="{ww-12}" height="3" fill="{C["ink"]}" opacity=".35"/>')
    t = x0 + 320
    parts.append(f'<path d="M{t} {base} L{t} {base-60} L{t+14} {base-70} L{t+22} {base-118} L{t+30} {base-150} L{t+38} {base-118} L{t+46} {base-70} L{t+60} {base-60} L{t+60} {base}Z"/>')
    parts.append(f'<path d="M{t+30} {base-150} L{t+30} {base-172} L{t+44} {base-166} L{t+30} {base-160}" />')
    parts.append(f'<path d="M{t+80} {base} Q {t+170} {base-90} {t+260} {base}" fill="none" stroke="{col}" stroke-width="5"/>')
    for i in range(1, 9):
        bx = t + 80 + i * 20
        by = base - (90 * (1 - ((bx - (t + 170)) / 90) ** 2)) * 0.5 * 2 / 2 * 1.0
        parts.append(f'<line x1="{bx}" y1="{base}" x2="{bx}" y2="{by:.1f}" stroke="{col}" stroke-width="1.5"/>')
    return f'<g fill="{col}" opacity="{op}">{"".join(parts)}</g>'

FONT = "<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap'>"
BASE = "*{margin:0;padding:0;box-sizing:border-box}body{font-family:Poppins,sans-serif;-webkit-font-smoothing:antialiased}"

HEAD = "Corporate rides you can count on."
HEAD_A, HEAD_B = "Corporate rides", "you can count on."
SUB = "Employee transport · Airport transfers · Chauffeur services · Outstation"

def fb_html():
    w, h = 1640, 624
    road = h - 70
    svg = f"""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="position:absolute;inset:0">
      <defs><radialGradient id="g" cx="50%" cy="0%" r="90%"><stop offset="0" stop-color="{C['deep']}"/><stop offset=".75" stop-color="{C['ink']}"/></radialGradient>
        <linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{C['ink']}" stop-opacity="0"/><stop offset=".3" stop-color="{C['ink']}" stop-opacity=".9"/><stop offset=".7" stop-color="{C['ink']}" stop-opacity=".9"/><stop offset="1" stop-color="{C['ink']}" stop-opacity="0"/></linearGradient></defs>
      <rect width="{w}" height="{h}" fill="url(#g)"/>
      {skyline(30, road, 600, C['teal2'], .22)}
      {skyline(1020, road, 600, C['teal2'], .22)}
      
      <path d="M120 150 C 380 40, 620 80, 760 60" fill="none" stroke="{C['gold']}" stroke-width="2" stroke-dasharray="3 10" stroke-linecap="round" opacity=".7"/>
      {plane(800, 56, .9, -8)}
      {pin(118, 160, 1, C['terra'])}
      <rect x="0" y="{road}" width="{w}" height="{h-road}" fill="#071E1C"/>
      <line x1="0" y1="{road+30}" x2="{w}" y2="{road+30}" stroke="{C['ivory']}" stroke-opacity=".35" stroke-width="3" stroke-dasharray="40 30"/>
      {sedan(1180, road+18, 1.05)}
      {sedan(140, road+18, .78, C['terra'])}
      <path d="M1300 {road-120} C 1380 {road-60}, 1460 {road-200}, 1560 {road-235}" fill="none" stroke="{C['teal']}" stroke-width="2.5" stroke-dasharray="2 9" stroke-linecap="round" opacity=".8"/>
      {pin(1560, road-235, 1.1, C['teal'])}
      {badge(190, 300, 30, 'building-2')}{badge(310, 230, 26, 'plane')}{badge(1340, 210, 26, 'shield-check')}{badge(1480, 120, 30, 'route')}
    </svg>"""
    txt = f"""<div style="position:absolute;left:0;right:0;top:132px;text-align:center;color:{C['ivory']}">
      <div style="font-size:19px;letter-spacing:7px;color:{C['gold']};font-weight:500">CORPORATE MOBILITY · GUJARAT</div>
      <div style="font-size:62px;font-weight:600;line-height:1.1;margin-top:16px">{HEAD_A}<br><span style="color:{C['teal']}">{HEAD_B}</span></div>
      <div style="font-size:21px;opacity:.85;margin-top:20px">{SUB}</div>
      <div style="display:inline-block;margin-top:22px;font-size:17px;letter-spacing:1.5px;padding:8px 20px;border:1px solid rgba(201,168,106,.6);border-radius:999px;color:{C['ivory']}">On time · Verified drivers · 24/7</div></div>
      <div style="position:absolute;left:0;right:0;bottom:10px;text-align:center;font-size:16px;color:{C['ivory']};opacity:.65;letter-spacing:2px">pulpitcabs.com &nbsp;|&nbsp; #SupermarketOfRides</div>"""
    return f'<div style="position:relative;width:{w}px;height:{h}px;overflow:hidden">{svg}{txt}</div>', w, h

def li_html():
    w, h = 1128, 191
    road = h - 26
    svg = f"""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="position:absolute;inset:0">
      <defs><radialGradient id="gl" cx="80%" cy="0%" r="110%"><stop offset="0" stop-color="{C['deep']}"/><stop offset=".7" stop-color="{C['ink']}"/></radialGradient></defs>
      <rect width="{w}" height="{h}" fill="url(#gl)"/>
      <g transform="translate(250,0) scale(.42)">{skyline(0, int(road/.42), 600, C['teal2'], .25)}</g>
      <rect x="0" y="{road}" width="{w}" height="{h-road}" fill="#071E1C"/>
      <line x1="0" y1="{road+12}" x2="{w}" y2="{road+12}" stroke="{C['ivory']}" stroke-opacity=".3" stroke-width="1.5" stroke-dasharray="18 14"/>
      {sedan(300, road+8, .42)}
      <path d="M250 70 C 330 20, 400 40, 470 30" fill="none" stroke="{C['gold']}" stroke-width="1.5" stroke-dasharray="2 7" stroke-linecap="round" opacity=".8"/>
      {plane(492, 27, .42, -8)}
      {pin(248, 76, .55, C['terra'])}
      {badge(560, 70, 15, 'building-2')}{badge(560, 118, 15, 'shield-check')}
      <line x1="610" y1="36" x2="610" y2="150" stroke="{C['gold']}" stroke-opacity=".4"/>
      <rect x="0" y="0" width="5" height="{h}" fill="{C['terra']}"/>
    </svg>"""
    txt = f"""<div style="position:absolute;left:640px;right:40px;top:30px;color:{C['ivory']}">
      <div style="font-size:10.5px;letter-spacing:3.5px;color:{C['gold']};font-weight:500">CORPORATE MOBILITY · GUJARAT</div>
      <div style="font-size:25px;font-weight:600;line-height:1.15;margin-top:7px;white-space:nowrap">{HEAD_A} <span style="color:{C['teal']}">{HEAD_B}</span></div>
      <div style="font-size:11.5px;opacity:.82;margin-top:9px">{SUB}</div>
      <div style="font-size:10.5px;opacity:.6;margin-top:12px;letter-spacing:1px">pulpitcabs.com &nbsp;|&nbsp; On time · Verified drivers · 24/7</div></div>"""
    return f'<div style="position:relative;width:{w}px;height:{h}px;overflow:hidden">{svg}{txt}</div>', w, h

if __name__ == "__main__":
    out = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, fn, sc in [("fb-cover", fb_html, 2), ("li-cover", li_html, 3)]:
            html, w, h = fn()
            out[name] = html
            pg = b.new_page(device_scale_factor=sc, viewport={"width": w, "height": h})
            pg.set_content(f"<html><head><style>{BASE}</style></head><body>{html}</body></html>")
            pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(300)
            pg.screenshot(path=str(ROOT / f"{name}-v2.png"))
        b.close()
    json.dump(out, open(ROOT / "covers.json", "w"))
    print("ok")
