"""Generates the NailBot icons and link preview image. Run by .github/workflows/assets.yml."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F='fonts/'
OUT=''
P1=np.array([0xb1,0x5c,0xff]); P2=np.array([0x5b,0x1d,0xc9])  # purple gradient

def grad(w,h,c1,c2):
    y,x=np.mgrid[0:h,0:w]; t=((x/w)+(y/h))/2
    a=(c1[None,None,:]*(1-t[...,None])+c2[None,None,:]*t[...,None]).astype(np.uint8)
    return Image.fromarray(a,'RGB')

def icon(size, rounded=True):
    S=size*4
    g=grad(S,S,P1,P2).convert('RGBA')
    # soft highlight
    hl=Image.new('L',(S,S),0); d=ImageDraw.Draw(hl); d.ellipse([-S*0.3,-S*0.6,S*1.0,S*0.45],fill=60)
    hl=hl.filter(ImageFilter.GaussianBlur(S*0.06))
    white=Image.new('RGBA',(S,S),(255,255,255,255)); g=Image.composite(white,g,hl)
    d=ImageDraw.Draw(g)
    txt='NB'; fs=int(S*0.5)
    while True:
        font=ImageFont.truetype(F+'Manrope-800.ttf', fs)
        bb=d.textbbox((0,0),txt,font=font)
        if bb[2]-bb[0] <= S*(0.74 if size<=48 else 0.62): break
        fs-=4
    tw,th=bb[2]-bb[0],bb[3]-bb[1]
    d.text(((S-tw)/2-bb[0],(S-th)/2-bb[1]),txt,font=font,fill=(255,255,255,255))
    # small cherry dot accent
    r=S*0.05; cx,cy=S*0.80,S*0.21
    if size>48: d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(255,46,99,255))
    if rounded:
        m=Image.new('L',(S,S),0); ImageDraw.Draw(m).rounded_rectangle([0,0,S-1,S-1],radius=int(S*0.22),fill=255)
        g.putalpha(m)
    return g.resize((size,size),Image.LANCZOS)

icon(180,rounded=False).convert('RGB').save(OUT+'apple-touch-icon.png')
icon(32).save(OUT+'favicon-32.png')
ico=icon(48); ico.save(OUT+'favicon.ico',sizes=[(16,16),(32,32),(48,48)])

# OG image
W,H=1200,630
bg=Image.new('RGB',(W,H),(12,9,14))
glow=Image.new('RGB',(W,H),(0,0,0)); gd=ImageDraw.Draw(glow)
gd.ellipse([780,-260,1420,380],fill=(255,46,99)); gd.ellipse([-260,260,420,900],fill=(130,50,230))
glow=glow.filter(ImageFilter.GaussianBlur(140))
bg=Image.blend(bg,Image.fromarray(np.clip(np.array(bg).astype(int)+np.array(glow).astype(int)*0.55,0,255).astype(np.uint8)),1.0)
d=ImageDraw.Draw(bg)
ic=icon(84); bg.paste(ic,(72,64),ic)
d.text((176,84),'NailBot',font=ImageFont.truetype(F+'Syne-800.ttf',40),fill=(246,240,244))
big=ImageFont.truetype(F+'Syne-800.ttf',112)
d.text((72,214),'Nails, done',font=big,fill=(246,240,244))
# gradient word
line2a='by '; x0=72; y0=330
d.text((x0,y0),line2a,font=big,fill=(246,240,244))
wa=d.textlength(line2a,font=big)
word='robot.'; bb=d.textbbox((0,0),word,font=big); ww,wh=bb[2],bb[3]
gm=Image.new('L',(ww,wh+30),0); ImageDraw.Draw(gm).text((0,0),word,font=big,fill=255)
gr=grad(ww,wh+30,np.array([0xff,0x2e,0x63]),np.array([0xb1,0x5c,0xff]))
bg.paste(gr,(int(x0+wa),y0),gm)
sub=ImageFont.truetype(F+'Manrope-600.ttf',32)
d.text((72,486),'Salon quality manicures, painted at home.',font=sub,fill=(200,188,198))
d.text((72,532),'Join the waitlist at nailbot.si',font=ImageFont.truetype(F+'Manrope-800.ttf',32),fill=(255,179,198))
# polish drops
cols=[(255,46,99),(255,179,198),(142,44,122),(217,194,167),(59,63,107)]
for i,c in enumerate(cols):
    x=900+i*52; y=520
    S=4; dr=Image.new('RGBA',(40*S,52*S),(0,0,0,0)); dd=ImageDraw.Draw(dr)
    dd.ellipse([0,0,40*S-1,52*S-1],fill=c+(255,))
    dd.ellipse([9*S,9*S,18*S,22*S],fill=(255,255,255,120))
    dr=dr.resize((40,52),Image.LANCZOS); bg.paste(dr,(x,y),dr)
bg.save(OUT+'og-image.jpg',quality=85,optimize=True,progressive=True)
print('ok')
