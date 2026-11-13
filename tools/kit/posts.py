import base64, pathlib, sys, datetime
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from cal import CAL
from covers import icon_inner, sedan, plane, pin, skyline, C

ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "creatives" / "render"; OUT.mkdir(exist_ok=True)
LOGO = base64.b64encode(open(""+str(pathlib.Path(__file__).resolve().parents[2]/"brand/pulpit-logo.png")+"","rb").read()).decode()
LOGO_W = base64.b64encode(open(""+str(pathlib.Path(__file__).resolve().parents[2]/"brand/pulpit-logo-white.png")+"","rb").read()).decode()
W, Hh = 1080, 1350

def ic(name, size, col, sw=1.8):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{icon_inner(name)}</svg>'

def frame(bg, fg, logo, body, foot_col, deco=""):
    return f"""<div style="position:relative;width:{W}px;height:{Hh}px;overflow:hidden;background:{bg};color:{fg}">
      {deco}
      <img src="data:image/png;base64,{logo}" style="position:absolute;left:72px;top:64px;height:70px">
      {body}
      <div style="position:absolute;left:72px;right:72px;bottom:52px;display:flex;justify-content:space-between;font-size:24px;color:{foot_col};opacity:.8">
        <span>pulpitcabs.com</span><span>#SupermarketOfRides</span><span>@pulpit_cabs</span></div></div>"""

def kick(text, col): return f'<div style="font-size:24px;letter-spacing:6px;color:{col};font-weight:500">{text}</div>'

ICON_FOR = {"checklist":"circle-check","steps":"route"}

def render_one(p, n):
    t = p["t"]
    if t == "insight":
        deco = f"""<svg width="{W}" height="{Hh}" style="position:absolute;inset:0"><defs><radialGradient id="r" cx="85%" cy="0%" r="90%"><stop offset="0" stop-color="{C['deep']}"/><stop offset=".8" stop-color="{C['ink']}"/></radialGradient></defs>
          <rect width="{W}" height="{Hh}" fill="url(#r)"/>
          <g transform="translate(560,0) scale(.85)">{skyline(0, 1430, 600, C['teal2'], .16)}</g>
          <rect x="0" y="1215" width="{W}" height="135" fill="#071E1C"/>
          <line x1="0" y1="1242" x2="{W}" y2="1242" stroke="{C['ivory']}" stroke-opacity=".25" stroke-width="3" stroke-dasharray="36 26"/>
          {sedan(640, 1232, .95)}
          <path d="M80 1120 C 300 1000, 520 1180, 760 1060" fill="none" stroke="{C['gold']}" stroke-width="2.5" stroke-dasharray="3 12" stroke-linecap="round" opacity=".7"/>
          {pin(80, 1125, 1.3, C['terra'])}</svg>"""
        body = f"""<div style="position:absolute;left:72px;right:72px;top:300px">{kick(p['kicker'], C['gold'])}
          <div style="font-size:80px;font-weight:600;line-height:1.08;margin-top:28px;text-wrap:balance">{p['title']}</div>
          <div style="font-size:34px;line-height:1.45;margin-top:34px;opacity:.82;max-width:880px">{p['sub']}</div></div>"""
        return frame(C['ink'], C['ivory'], LOGO_W, body, C['ivory'], deco)
    if t in ("checklist", "steps"):
        rows = "".join(f"""<div style="display:flex;align-items:center;gap:28px;padding:22px 0;border-bottom:1px solid rgba(11,42,40,.12)">
            <div style="flex:none;width:64px;height:64px;border-radius:50%;background:{C['deep'] if t=='checklist' else C['teal']};color:{C['ivory']};display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:600">{'✓' if t=='checklist' else i+1}</div>
            <div style="font-size:36px;font-weight:500;line-height:1.25">{x}</div></div>""" for i, x in enumerate(p["points"]))
        body = f"""<div style="position:absolute;left:72px;right:72px;top:230px">{kick(p['kicker'], C['terra'])}
          <div style="font-size:66px;font-weight:600;line-height:1.08;margin-top:22px;text-wrap:balance">{p['title']}</div>
          <div style="height:4px;margin:36px 0 10px;background:linear-gradient(90deg,{C['teal']} 0 60%,#E9E1D3 60% 90%,{C['terra']} 90%)"></div>
          {rows}</div>"""
        deco = f'<div style="position:absolute;right:-60px;top:-60px;width:300px;height:300px;border-radius:50%;border:2px solid {C["gold"]};opacity:.35"></div>'
        return frame(C['ivory'], C['ink'], LOGO, body, C['ink'], deco)
    if t == "route":
        deco = f"""<svg width="{W}" height="{Hh}" style="position:absolute;inset:0"><defs><linearGradient id="g" x1="0" y1="0" x2=".4" y2="1"><stop offset="0" stop-color="{C['teal']}"/><stop offset=".75" stop-color="{C['deep']}"/></linearGradient></defs>
          <rect width="{W}" height="{Hh}" fill="url(#g)"/>
          <g transform="translate(0,0)">{skyline(40, 1180, 600, C['ivory'], .10)}</g>
          <rect x="0" y="1180" width="{W}" height="170" fill="#0B2A28" opacity=".55"/>
          <line x1="0" y1="1212" x2="{W}" y2="1212" stroke="{C['ivory']}" stroke-opacity=".35" stroke-width="3" stroke-dasharray="36 26"/>
          {sedan(80, 1200, .9, C['ivory'])}
          <path d="M120 900 C 380 640, 640 1000, 960 620" fill="none" stroke="{C['ivory']}" stroke-width="5" stroke-dasharray="4 16" stroke-linecap="round"/>
          <circle cx="120" cy="900" r="18" fill="{C['ivory']}"/>{pin(960, 620, 2.0, C['terra'])}
          {plane(860, 470, .9, -14)}</svg>"""
        a, b = p['title'].split(" to ", 1)
        body = f"""<div style="position:absolute;left:72px;right:72px;top:230px">{kick(p['kicker'], C['ivory'])}
          <div style="font-size:{92 if len(b)<=9 else 70}px;font-weight:600;line-height:1.05;margin-top:22px">{a}<br><span style="opacity:.6;font-weight:400;font-size:64px">to</span> {b}</div>
          <div style="display:flex;gap:18px;margin-top:30px">
            <div style="padding:14px 26px;border-radius:999px;background:rgba(11,42,40,.35);font-size:30px;font-weight:500">{p['stat1']}</div>
            <div style="padding:14px 26px;border-radius:999px;background:rgba(11,42,40,.35);font-size:30px;font-weight:500">{p['stat2']}</div></div></div>
          <div style="position:absolute;left:72px;right:72px;top:680px;font-size:32px;line-height:1.4;opacity:.92">{p['sub']}</div>"""
        return frame(C['teal'], C['ivory'], LOGO_W, body, C['ivory'], deco)
    if t == "poll":
        opts = "".join(f"""<div style="display:flex;align-items:center;gap:24px;padding:26px 32px;margin-top:20px;border-radius:20px;background:{C['ivory']};color:{C['ink']};font-size:38px;font-weight:500">
            <span style="flex:none;width:58px;height:58px;border-radius:50%;border:3px solid {C['teal']};display:flex;align-items:center;justify-content:center;font-size:28px;color:{C['teal']};font-weight:600">{'ABC'[i]}</span>{o}</div>""" for i, o in enumerate(p['options']))
        deco = f"""<svg width="{W}" height="{Hh}" style="position:absolute;inset:0"><rect width="{W}" height="{Hh}" fill="{C['deep']}"/>
          <circle cx="980" cy="160" r="260" fill="{C['terra']}" opacity=".12"/></svg>"""
        body = f"""<div style="position:absolute;left:72px;right:72px;top:250px">{kick(p['kicker'], C['gold'])}
          <div style="font-size:76px;font-weight:600;line-height:1.08;margin-top:24px;text-wrap:balance">{p['title']}</div>
          <div style="margin-top:48px">{opts}</div>
          <div style="margin-top:40px;font-size:30px;opacity:.75">Comment your answer 👇</div></div>"""
        return frame(C['deep'], C['ivory'], LOGO_W, body, C['ivory'], deco)
    if t == "review":
        stars = "".join(f'<span style="display:inline-block;margin-right:8px">{ic("star", 52, C["gold"], 2).replace('fill="none"','fill="'+C["gold"]+'"')}</span>' for _ in range(5))
        body = f"""<div style="position:absolute;left:72px;right:72px;top:300px">{kick(p['kicker'], C['terra'])}
          <div style="margin-top:36px">{stars}</div>
          <div style="font-size:72px;font-weight:600;line-height:1.15;margin-top:34px;text-wrap:balance">{p['title']}</div>
          <div style="font-size:32px;margin-top:34px;opacity:.7">{p['sub']}</div></div>"""
        deco = f'<div style="position:absolute;left:52px;top:180px;font-size:420px;line-height:1;color:{C["teal"]};opacity:.12;font-family:Georgia,serif">“</div>'
        return frame(C['ivory'], C['ink'], LOGO, body, C['ink'], deco)
    # occasion
    deco = f"""<svg width="{W}" height="{Hh}" style="position:absolute;inset:0">
      <rect width="{W}" height="{Hh}" fill="{C['ivory']}"/>
      <circle cx="540" cy="820" r="170" fill="none" stroke="{C['gold']}" stroke-width="2" opacity=".6"/>
      <circle cx="540" cy="820" r="145" fill="{C['teal']}" opacity=".10"/>
      <g transform="translate(468,748) scale(6)" fill="none" stroke="{C['deep']}" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">{icon_inner('sparkles')}</g>
      <g transform="translate(0,-40)">{skyline(-40, 1150, 600, C['teal'], .14)}{skyline(560, 1150, 600, C['teal'], .14)}</g>
      <rect x="0" y="1110" width="{W}" height="240" fill="{C['deep']}"/>
      <line x1="0" y1="1140" x2="{W}" y2="1140" stroke="{C['ivory']}" stroke-opacity=".3" stroke-width="3" stroke-dasharray="36 26"/>
      {sedan(390, 1130, .95)}</svg>"""
    body = f"""<div style="position:absolute;left:72px;right:72px;top:290px;text-align:center">{kick(p['kicker'], C['terra'])}
      <div style="font-size:78px;font-weight:600;line-height:1.1;margin-top:26px;text-wrap:balance;color:{C['ink']}">{p['title']}</div>
      <div style="font-size:32px;margin-top:28px;color:{C['deep']};opacity:.85">{p['sub']}</div></div>"""
    return frame(C['ivory'], C['ink'], LOGO, body, C['ivory'], deco)

if __name__ == "__main__":
    only = sys.argv[1:]
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": Hh})
        for n, p in enumerate(CAL, 1):
            if only and str(n) not in only: continue
            html = render_one(p, n)
            pg.set_content(f"<html><head><style>*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:Poppins,sans-serif;-webkit-font-smoothing:antialiased}}</style></head><body>{html}</body></html>")
            pg.wait_for_timeout(120)
            name = f"{n:02d}_{p['d'][5:].replace('-','')}_{p['t']}.jpg"
            pg.screenshot(path=str(OUT / name), type="jpeg", quality=90)
            p["file"] = name
        b.close()
    print(sorted(x.name for x in OUT.iterdir())[:40])
