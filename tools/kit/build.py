import base64, pathlib, re
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "out"; OUT.mkdir(exist_ok=True)
LOGO = base64.b64encode(open(""+str(ROOT.parents[1]/"brand")+"/pulpit-logo.png","rb").read()).decode()
LOGO_W = base64.b64encode(open(""+str(ROOT.parents[1]/"brand")+"/pulpit-logo-white.png","rb").read()).decode()
ICONS = ROOT / "node_modules/lucide-static/icons"

# Premium palette (brand teal + terracotta, deepened)
C = dict(ink="#0B2A28", deep="#123D3A", teal="#21A5A0", teal2="#50A39F",
         terra="#D06350", terra2="#B63330", ivory="#F7F3EC", sand="#E9E1D3", gold="#C9A86A")

def icon(name, size, color, stroke=1.6):
    s = (ICONS / f"{name}.svg").read_text()
    s = re.sub(r'<svg([^>]*?)width="\d+"', lambda m: f'<svg{m.group(1)}width="{size}"', s, count=1)
    s = re.sub(r'<svg([^>]*?)height="\d+"', lambda m: f'<svg{m.group(1)}height="{size}"', s, count=1)
    s = s.replace('stroke="currentColor"', f'stroke="{color}"')
    s = re.sub(r'stroke-width="[\d.]+"', f'stroke-width="{stroke}"', s)
    return s

BASE = f"""<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Poppins',sans-serif;-webkit-font-smoothing:antialiased}}
.logo{{background:url(data:image/png;base64,{LOGO}) no-repeat center/contain}}
.logow{{background:url(data:image/png;base64,{LOGO_W}) no-repeat center/contain}}
</style>"""

def render(page, html, w, h, name, scale=1):
    page.set_viewport_size({"width": w, "height": h})
    page.set_content(f"<html><head>{BASE}</head><body style='width:{w}px;height:{h}px;overflow:hidden'>{html}</body></html>")
    page.wait_for_timeout(150)
    page.screenshot(path=str(OUT / name), clip={"x":0,"y":0,"width":w,"height":h})

ROUTE_SVG = lambda w,h,col: f"""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="position:absolute;inset:0">
 <path d="M -20 {h*0.78} C {w*0.25} {h*0.55}, {w*0.45} {h*1.05}, {w*0.68} {h*0.62} S {w*0.95} {h*0.25}, {w+20} {h*0.32}"
   fill="none" stroke="{col}" stroke-width="2" stroke-dasharray="2 10" stroke-linecap="round" opacity=".55"/>
</svg>"""

def linkedin(page):
    w,h = 1128,191
    html = f"""<div style="position:relative;width:{w}px;height:{h}px;background:
      radial-gradient(120% 160% at 85% 0%, {C['deep']} 0%, {C['ink']} 60%);overflow:hidden">
      {ROUTE_SVG(w,h,C['teal2'])}
      <div style="position:absolute;left:0;top:0;bottom:0;width:6px;background:{C['terra']}"></div>
      <div style="position:absolute;right:58px;top:38px;text-align:right;color:{C['ivory']}">
        <div style="font-size:11px;letter-spacing:3.5px;color:{C['gold']};font-weight:500">CORPORATE MOBILITY · GUJARAT</div>
        <div style="font-size:30px;font-weight:600;line-height:1.15;margin-top:8px">Every ride on time. <span style="color:{C['teal']}">Every rupee accounted.</span></div>
        <div style="font-size:12.5px;opacity:.78;margin-top:10px;font-weight:400">Employee transport &nbsp;·&nbsp; Airport transfers &nbsp;·&nbsp; Chauffeur services &nbsp;·&nbsp; Outstation</div>
      </div>
      <div style="position:absolute;right:58px;bottom:14px;font-size:11px;color:{C['ivory']};opacity:.6;letter-spacing:1px">pulpitcabs.com &nbsp;|&nbsp; #SupermarketOfRides</div>
      <div style="position:absolute;left:{w*0.25}px;top:{h*0.70}px;width:12px;height:12px;border-radius:50%;background:{C['terra']};box-shadow:0 0 0 6px rgba(208,99,80,.18)"></div>
    </div>"""
    page.set_viewport_size({"width":w,"height":h})
    page.set_content(f"<html><head>{BASE}</head><body style='width:{w}px;height:{h}px'>{html}</body></html>")
    page.wait_for_timeout(150)
    page.screenshot(path=str(OUT/"linkedin-cover-1128x191@3x.png"), clip={"x":0,"y":0,"width":w,"height":h}, scale="device")

def facebook(page):
    w,h = 1640,624
    html = f"""<div style="position:relative;width:{w}px;height:{h}px;background:
      radial-gradient(90% 140% at 50% 0%, {C['deep']} 0%, {C['ink']} 70%);overflow:hidden">
      {ROUTE_SVG(w,h,C['teal2'])}
      <div style="position:absolute;left:0;right:0;top:150px;text-align:center;color:{C['ivory']}">
        <div style="font-size:20px;letter-spacing:7px;color:{C['gold']};font-weight:500">CORPORATE MOBILITY · GUJARAT</div>
        <div style="font-size:64px;font-weight:600;line-height:1.12;margin-top:18px">Every ride on time.<br><span style="color:{C['teal']}">Every rupee accounted.</span></div>
        <div style="font-size:23px;opacity:.8;margin-top:24px">Employee transport · Airport transfers · Chauffeur services · Outstation</div>
      </div>
      <div style="position:absolute;left:0;right:0;bottom:44px;text-align:center;font-size:19px;color:{C['ivory']};opacity:.6;letter-spacing:2px">pulpitcabs.com &nbsp;|&nbsp; #SupermarketOfRides</div>
      <div style="position:absolute;left:0;right:0;bottom:0;height:8px;background:linear-gradient(90deg,{C['teal']} 0 60%,{C['ivory']} 60% 90%,{C['terra']} 90%)"></div>
    </div>"""
    render(page, html, w, h, "facebook-cover-1640x624.png")

HL = [("about","info","About"),("corporate","building-2","Corporate"),("airport","plane","Airport"),
      ("outstation","route","Outstation"),("reviews","star","Reviews"),("safety","shield-check","Safety"),
      ("faqs","circle-help","FAQs"),("book","smartphone","Book a ride")]

def highlights(page):
    w,h = 1080,1920
    for slug, ic, label in HL:
        html = f"""<div style="position:relative;width:{w}px;height:{h}px;background:
          radial-gradient(70% 45% at 50% 50%, {C['deep']} 0%, {C['ink']} 100%);display:flex;align-items:center;justify-content:center">
          <div style="width:620px;height:620px;border-radius:50%;border:4px solid {C['gold']};display:flex;align-items:center;justify-content:center">
            <div style="width:560px;height:560px;border-radius:50%;background:{C['ivory']};display:flex;align-items:center;justify-content:center">
              {icon(ic, 270, C['deep'], 1.5)}
            </div>
          </div>
          <div style="position:absolute;top:calc(50% + 250px);left:calc(50% + 165px);width:64px;height:64px;border-radius:50%;background:{C['terra']};border:6px solid {C['ink']}"></div>
        </div>"""
        render(page, html, w, h, f"ig-highlight-{slug}.png")

def avatar(page):
    w=h=1080
    html = f"""<div style="width:{w}px;height:{h}px;background:{C['ivory']};display:flex;align-items:center;justify-content:center">
      <div style="width:470px;height:600px;background:url(data:image/png;base64,{LOGO}) no-repeat left center/auto 100%;
        clip-path:inset(0 0 0 0);overflow:hidden" id="m"></div></div>"""
    # crop just the "P" mark: logo is 710x255, mark ≈ first 235px
    html = f"""<div style="width:{w}px;height:{h}px;background:{C['ivory']};display:flex;align-items:center;justify-content:center">
      <div style="width:{int(235*2.6)}px;height:{int(255*2.6)}px;overflow:hidden;position:relative">
        <img src="data:image/png;base64,{LOGO}" style="height:{int(255*2.6)}px;position:absolute;left:0;top:0"></div></div>"""
    render(page, html, w, h, "profile-picture-1080.png")

def post(page, kind):
    w,h = 1080,1350
    foot = lambda col: f"""<div style="position:absolute;left:72px;right:72px;bottom:56px;display:flex;justify-content:space-between;align-items:center;font-size:22px;color:{col};opacity:.75">
       <span>pulpitcabs.com</span><span>@pulpit_cabs</span></div>"""
    if kind=="insight":
        html = f"""<div style="position:relative;width:{w}px;height:{h}px;background:{C['ink']};color:{C['ivory']};overflow:hidden">
          {ROUTE_SVG(w,h,C['teal2'])}
          <div class="logow" style="position:absolute;left:72px;top:64px;width:200px;height:72px"></div>
          <div style="position:absolute;left:72px;top:330px;right:72px">
            <div style="font-size:24px;letter-spacing:5px;color:{C['gold']}">FLEET INSIGHT · 01</div>
            <div style="font-size:84px;font-weight:600;line-height:1.08;margin-top:26px">The real cost of a late pickup isn't the cab.</div>
            <div style="font-size:34px;line-height:1.45;margin-top:34px;opacity:.82">It's the missed flight, the idle team and the client meeting that starts without you.</div>
          </div>
          <div style="position:absolute;left:72px;bottom:150px;padding:18px 34px;border-radius:999px;background:{C['terra']};font-size:26px;font-weight:600">Save this for your admin team</div>
          {foot(C['ivory'])}</div>"""
    elif kind=="carousel":
        html = f"""<div style="position:relative;width:{w}px;height:{h}px;background:{C['ivory']};color:{C['ink']};overflow:hidden">
          <div class="logo" style="position:absolute;left:72px;top:64px;width:200px;height:72px"></div>
          <div style="position:absolute;right:72px;top:80px;font-size:24px;color:{C['deep']};opacity:.6">1 / 6 &nbsp;→</div>
          <div style="position:absolute;left:72px;top:300px;right:72px">
            <div style="font-size:24px;letter-spacing:5px;color:{C['terra']}">CHECKLIST</div>
            <div style="font-size:88px;font-weight:600;line-height:1.06;margin-top:24px">5 questions to ask before you sign a corporate cab vendor</div>
          </div>
          <div style="position:absolute;left:72px;right:72px;top:960px;height:4px;background:linear-gradient(90deg,{C['teal']} 0 60%,{C['sand']} 60% 90%,{C['terra']} 90%)"></div>
          <div style="position:absolute;left:72px;top:1000px;font-size:30px;opacity:.7">Swipe — #3 is where most contracts go wrong.</div>
          {foot(C['ink'])}</div>"""
    else:  # route
        html = f"""<div style="position:relative;width:{w}px;height:{h}px;background:linear-gradient(160deg,{C['teal']} 0%,{C['deep']} 70%);color:{C['ivory']};overflow:hidden">
          <div class="logow" style="position:absolute;left:72px;top:64px;width:200px;height:72px"></div>
          <div style="position:absolute;left:72px;top:300px;font-size:24px;letter-spacing:5px;color:{C['sand']}">SATURDAY ROUTE SPOTLIGHT</div>
          <div style="position:absolute;left:72px;top:360px;font-size:96px;font-weight:600;line-height:1.05">Ahmedabad<br><span style="opacity:.55;font-weight:400">to</span> Dwarka</div>
          <svg width="936" height="300" style="position:absolute;left:72px;top:760px">
            <path d="M20 240 C 250 60, 520 300, 900 50" fill="none" stroke="{C['ivory']}" stroke-width="5" stroke-dasharray="4 16" stroke-linecap="round"/>
            <circle cx="20" cy="240" r="16" fill="{C['ivory']}"/><circle cx="900" cy="50" r="20" fill="{C['terra']}" stroke="{C['ivory']}" stroke-width="6"/></svg>
          <div style="position:absolute;left:72px;bottom:150px;font-size:30px;opacity:.9">Temple darshan, sunset at Shivrajpur, one driver for the whole trip.</div>
          {foot(C['ivory'])}</div>"""
    render(page, html, w, h, f"ig-template-{kind}.png")

with sync_playwright() as p:
    b = p.chromium.launch()
    pg3 = b.new_page(device_scale_factor=3); linkedin(pg3)
    pg = b.new_page()
    facebook(pg); highlights(pg); avatar(pg)
    for k in ["insight","carousel","route"]: post(pg, k)
    b.close()
print(sorted(x.name for x in OUT.iterdir()))
