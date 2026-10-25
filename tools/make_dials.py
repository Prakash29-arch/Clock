"""Renders the analog-widget dials/hands (drawable-nodpi). All images share one size so AnalogClock's
pivot-at-centre math lines the hands up with the dial."""
import math, sys, os
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1]
S, SS = 640, 4                       # final size, supersample factor
C = S * SS / 2
WHITE, GRAY, ORANGE, RED = (255,255,255,255), (142,142,147,255), (255,159,10,255), (215,25,33,255)
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def canvas(): return Image.new("RGBA", (S*SS, S*SS), (0,0,0,0))
def finish(im, name): im.resize((S, S), Image.LANCZOS).save(os.path.join(OUT, name), optimize=True)
def pol(r, deg): a = math.radians(deg - 90); return C + r*SS*math.cos(a), C + r*SS*math.sin(a)
def line_hand(d, x0, x1, w, col):                      # rounded bar pointing at 12 from -x0 to x1 (px at final scale)
    d.rounded_rectangle([C - w*SS/2, C - x1*SS, C + w*SS/2, C + x0*SS], radius=w*SS/2, fill=col)
def dot(d, cx, cy, r, col): d.ellipse([cx-r*SS, cy-r*SS, cx+r*SS, cy+r*SS], fill=col)

# ---------------- iOS style ----------------
im = canvas(); d = ImageDraw.Draw(im)
for i in range(60):
    major = i % 5 == 0
    r0, r1, w = (292, 262, 7) if major else (292, 276, 3)
    col = WHITE if major else GRAY
    x0, y0 = pol(r0, i*6); x1, y1 = pol(r1, i*6)
    d.line([x0, y0, x1, y1], fill=col, width=int(w*SS))
font = ImageFont.truetype(BOLD, 62*SS)
for h in range(1, 13):
    x, y = pol(205, h*30)
    d.text((x, y), str(h), font=font, fill=WHITE, anchor="mm")
finish(im, "ios_clock_dial.png")
for name, back, fwd, w, col in [("ios_clock_hour.png", 36, 150, 24, WHITE), ("ios_clock_minute.png", 36, 232, 17, WHITE)]:
    im = canvas(); d = ImageDraw.Draw(im); line_hand(d, back, fwd, w, col); dot(d, C, C, 17, col); finish(im, name)
im = canvas(); d = ImageDraw.Draw(im)
line_hand(d, 62, 252, 7, ORANGE); dot(d, C, C, 17, ORANGE); dot(d, C, C, 6, (0,0,0,255)); finish(im, "ios_clock_second.png")

# ---------------- Nothing dot style ----------------
im = canvas(); d = ImageDraw.Draw(im)
for i in range(60):
    x, y = pol(290, i*6)
    if i == 0:           dot(d, x, y, 13, RED)
    elif i % 5 == 0:     dot(d, x, y, 10, WHITE)
    else:                dot(d, x, y, 4.5, (110,110,114,255))
finish(im, "nothing_clock_dial.png")
def dot_hand(name, n, step, r, col, tip=None):
    im = canvas(); d = ImageDraw.Draw(im)
    for k in range(1, n+1): dot(d, C, C - k*step*SS, r, col)
    dot(d, C, C, r + 3, col)
    finish(im, name)
dot_hand("nothing_clock_hour.png", 6, 24, 11, WHITE)
dot_hand("nothing_clock_minute.png", 10, 25, 8.5, WHITE)
im = canvas(); d = ImageDraw.Draw(im)
for k in range(-2, 12): dot(d, C, C - k*24*SS, 5, RED)
dot(d, C, C, 15, RED); dot(d, C, C, 6, (0,0,0,255)); finish(im, "nothing_clock_second.png")
print("ok")
