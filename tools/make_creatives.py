from PIL import Image, ImageDraw, ImageFont
import math, os

OUT = "/tmp/claude-0/-home-claude/8eeb75d8-59f2-52be-b132-d40eea9a72e2/scratchpad/creatives"
os.makedirs(OUT, exist_ok=True)
F = "/usr/share/fonts/truetype/google-fonts/Poppins-%s.ttf"
def font(w, s): return ImageFont.truetype(F % w, s)

TEAL=(0x50,0xA3,0x9F); DTEAL=(0x2C,0x66,0x63); TERRA=(0xD0,0x63,0x50); DTERRA=(0xB6,0x33,0x30)
WHITE=(255,255,255); INK=(0x1B,0x2A,0x2A); MIST=(0xE2,0xF1,0xEF); PALE=(0xF6,0xF9,0xF8)
S=1080

def wrap(d, text, f, maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t, font=f)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def draw_lines(d, x, y, lines, f, fill, lh):
    for ln in lines:
        d.text((x,y), ln, font=f, fill=fill); y+=lh
    return y

LOGO_C=Image.open("/tmp/claude-0/-home-claude/8eeb75d8-59f2-52be-b132-d40eea9a72e2/scratchpad/logo_color.png").convert("RGBA")
LOGO_W=Image.open("/tmp/claude-0/-home-claude/8eeb75d8-59f2-52be-b132-d40eea9a72e2/scratchpad/logo_white.png").convert("RGBA")
def place_logo(img, x, y, width, dark):
    lg=(LOGO_W if dark else LOGO_C); h=int(lg.size[1]*width/lg.size[0]); lg=lg.resize((width,h),Image.LANCZOS)
    img.paste(lg,(x,y-h),lg)
def brand(d, dark, tag=True):
    place_logo(d._image, 72, S-62, 260, dark)
    if tag:
        t="#SupermarketOfRides"; f=font("Medium",24)
        d.text((S-72-d.textlength(t,font=f), S-98), t, font=f, fill=(TERRA if not dark else (0xF2,0xB3,0xA6)))

def car(d, x, y, sc, fill):
    # simple side-profile car glyph
    d.rounded_rectangle((x, y+22*sc, x+120*sc, y+62*sc), radius=10*sc, fill=fill)
    d.rounded_rectangle((x+28*sc, y, x+92*sc, y+30*sc), radius=8*sc, fill=fill)
    d.ellipse((x+18*sc, y+50*sc, x+42*sc, y+74*sc), fill=fill)
    d.ellipse((x+78*sc, y+50*sc, x+102*sc, y+74*sc), fill=fill)

def save(img, name, q=82):
    p=os.path.join(OUT,name); img.convert("RGB").save(p, "JPEG", quality=q, optimize=True); print(name, os.path.getsize(p)//1024, "KB")

# 1. Oct 1 — 5:40 am run
img=Image.new("RGB",(S,S),DTEAL); d=ImageDraw.Draw(img)
d.text((72,88),"DRIVER SIDE",font=font("Medium",26),fill=(0x9F,0xD4,0xD0))
d.text((72,150),"5:40 am",font=font("Bold",190),fill=WHITE)
y=draw_lines(d,72,380,wrap(d,"Tyres checked. Seats wiped. Out of Sector 21 before the city wakes.",font("Regular",46),S-144),font("Regular",46),WHITE,62)
d.rectangle((72,y+30,72+90,y+36),fill=TERRA)
draw_lines(d,72,y+64,wrap(d,"Fixed fare agreed last night. No surge, no haggling, no calls. That's what a verified driver looks like at 5:40 am.",font("Light",34),S-144),font("Light",34),MIST,48)
car(d,760,720,1.8,TEAL)
brand(d,True); save(img,"01_oct1_driver_540am.jpg")

# 2. Oct 2 — Gandhi Jayanti
img=Image.new("RGB",(S,S),PALE); d=ImageDraw.Draw(img)
d.text((72,88),"2 OCTOBER",font=font("Medium",26),fill=TEAL)
d.text((72,140),"Porbandar",font=font("Bold",96),fill=INK)
d.text((72,250),"to Sabarmati",font=font("Light",96),fill=INK)
d.line((72,380,S-72,380),fill=TEAL,width=4)
d.text((72,400),"400 km by road.",font=font("Regular",48),fill=DTEAL)
draw_lines(d,72,470,wrap(d,"The distance he walked for the country was longer.",font("Light",48),S-144),font("Light",48),INK,64)
d.text((72,660),"Quiet roads today. Drive gently.",font=font("Medium",36),fill=TERRA)
# spinning wheel / charkha-like ring
cx,cy,r=830,780,110
d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=DTEAL,width=8)
for a in range(0,360,30):
    d.line((cx,cy,cx+r*math.cos(math.radians(a)),cy+r*math.sin(math.radians(a))),fill=DTEAL,width=4)
brand(d,False); save(img,"02_oct2_gandhi_jayanti.jpg")

# 4. Oct 5 — One invoice, forty rides
img=Image.new("RGB",(S,S),WHITE); d=ImageDraw.Draw(img)
d.rectangle((0,0,S,140),fill=DTEAL)
d.text((72,44),"CORPORATE MOBILITY",font=font("Medium",26),fill=(0x9F,0xD4,0xD0))
d.text((72,180),"One invoice.",font=font("Bold",88),fill=INK)
d.text((72,280),"Forty rides.",font=font("Light",88),fill=INK)
items=["Monthly GST invoice, ride-level line items","Named account manager, one number","Late flight? Same agreed fare","Verified drivers, every trip","Console access for your admin team"]
y=430
for it in items:
    d.rounded_rectangle((72,y+6,72+34,y+40),radius=6,fill=MIST); d.text((78,y),"✓",font=font("Bold",30),fill=DTEAL) if False else d.line((80,y+22,92,y+34),fill=DTEAL,width=5); d.line((92,y+34,112,y+10),fill=DTEAL,width=5)
    d.text((130,y),it,font=font("Regular",36),fill=INK); y+=76
d.text((72,y+30),"Built for the person who books rides for everyone else.",font=font("Medium",30),fill=TERRA)
brand(d,False); save(img,"04_oct5_one_invoice.jpg")

# 5. Oct 7 — Crude above $100
img=Image.new("RGB",(S,S),TEAL); d=ImageDraw.Draw(img)
d.text((72,88),"MOBILITY DESK",font=font("Medium",26),fill=DTEAL)
d.text((72,150),"Crude is",font=font("Light",110),fill=WHITE)
d.text((72,270),"above $100.",font=font("Bold",110),fill=WHITE)
d.rectangle((72,430,S-72,660),fill=WHITE)
d.text((100,455),"Your fare isn't.",font=font("Bold",96),fill=DTERRA)
d.text((100,570),"Fixed. All-inclusive. Agreed before the ride.",font=font("Regular",34),fill=DTEAL)
draw_lines(d,72,700,wrap(d,"Brent crossed $100 last week. Pump prices are holding. Every metered cab is quietly absorbing that gap, or passing it on as surge.",font("Light",32),S-144),font("Light",32),WHITE,46)
brand(d,True); save(img,"05_oct7_crude_100.jpg")

# 6. Oct 8 — Fuel maths
img=Image.new("RGB",(S,S),PALE); d=ImageDraw.Draw(img)
d.text((72,88),"DRIVER SIDE · FUEL MATHS",font=font("Medium",26),fill=TEAL)
d.text((72,140),"A 300 km day, in litres.",font=font("Bold",70),fill=INK)
stats=[("300 km","outstation round trip"),("14 km/l","sedan, AC on, October heat"),("≈ 21 L","burned before waiting time")]
y=270
for big,small in stats:
    d.rectangle((72,y,S-72,y+150),fill=WHITE,outline=MIST,width=3)
    d.text((100,y+22),big,font=font("Bold",70),fill=DTEAL)
    d.text((100,y+100),small,font=font("Regular",30),fill=INK); y+=170
draw_lines(d,72,y+10,wrap(d,"The driver's margin lives in the last 2 km/l. Route planning and fixed fares protect that margin. That's why they matter on both sides of the seat.",font("Light",32),S-144),font("Light",32),INK,44)
brand(d,False); save(img,"06_oct8_fuel_maths.jpg")

# 7. Oct 9 — Types of Navratri passengers
img=Image.new("RGB",(S,S),DTERRA); d=ImageDraw.Draw(img)
d.text((72,80),"NAVRATRI · 9 NIGHTS",font=font("Medium",26),fill=(0xF2,0xB3,0xA6))
d.text((72,130),"Types of garba passengers",font=font("Bold",66),fill=WHITE)
types=[("The dandiya-in-the-boot one","'Bhai, gently on the speed breakers.'"),("The CG Road stopper","'Bas ek shop, 5 minute.'"),("The 2 am return booker","Already asleep before the seatbelt clicks.")]
y=260
for t,s in types:
    d.rounded_rectangle((72,y,S-72,y+170),radius=14,fill=WHITE)
    d.text((100,y+26),t,font=font("Bold",40),fill=DTERRA)
    d.text((100,y+90),s,font=font("Light",32),fill=INK); y+=195
d.text((72,y+10),"We know all of you. Nine nights, we're up.",font=font("Medium",34),fill=WHITE)
brand(d,True); save(img,"07_oct9_garba_passengers.jpg")

# Route GIFs
def route_gif(name, frm, to, km, hrs, via, note, frames=16, size=800):
    imgs=[]
    ax,ay=150,size-360; bx,by=size-150,290
    for i in range(frames):
        t=i/(frames-1)
        img=Image.new("RGB",(size,size),PALE); d=ImageDraw.Draw(img)
        d.text((60,60),"SATURDAY ROUTE",font=font("Medium",24),fill=TEAL)
        d.text((60,100),frm,font=font("Bold",64),fill=INK)
        d.text((60,170),"to "+to,font=font("Light",64),fill=DTEAL)
        # dashed guide
        pts=[(ax+(bx-ax)*k/40, ay+(by-ay)*k/40 - 120*math.sin(math.pi*k/40)) for k in range(41)]
        for k in range(0,40,2): d.line((pts[k],pts[k+1]),fill=MIST,width=6)
        n=int(t*40)
        if n>0: d.line(pts[:n+1],fill=TEAL,width=10,joint="curve")
        d.ellipse((ax-16,ay-16,ax+16,ay+16),fill=DTEAL)
        d.ellipse((bx-16,by-16,bx+16,by+16),fill=DTEAL if t>=1 else MIST,outline=DTEAL,width=4)
        px,py=pts[n]; car(d,px-48,py-70,0.8,TERRA)
        d.text((ax-30,ay+30),frm.split()[0],font=font("Medium",26),fill=DTEAL)
        d.text((bx-d.textlength(to,font=font("Medium",26))/2,by+28),to,font=font("Medium",26),fill=DTEAL)
        # stats
        d.text((60,size-300),f"{km} km · {hrs}",font=font("Bold",44),fill=INK)
        d.text((60,size-245),via,font=font("Regular",24),fill=DTEAL)
        d.text((60,size-203),note,font=font("Light",26),fill=INK)
        place_logo(img, 60, size-50, 210, False)
        f2=font("Medium",22); tg="#SupermarketOfRides"; d.text((size-60-d.textlength(tg,font=f2),size-72),tg,font=f2,fill=TERRA)
        imgs.append(img.quantize(colors=32, method=Image.Quantize.MEDIANCUT))
    imgs += [imgs[-1]]*8
    p=os.path.join(OUT,name); imgs[0].save(p,save_all=True,append_images=imgs[1:],duration=90,loop=0,optimize=True)
    print(name, os.path.getsize(p)//1024,"KB")

route_gif("03_oct3_route_dwarka.gif","Ahmedabad","Dwarka","≈ 440","7.5 hrs","via Rajkot · Jamnagar · Sudarshan Setu to Beyt Dwarka","Leave by 5 am, reach for evening aarti. Two chai stops.")
route_gif("08_oct10_route_somnath.gif","Ahmedabad","Somnath","≈ 410","7 hrs","via Rajkot · Junagadh · add Gir (65 km) + Diu (85 km)","3-day loop, one driver stays with you the whole way.")
