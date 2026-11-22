#!/usr/bin/env python3
"""Render the GTA 6 meme: a Leonida DMV driver license, renewed after 13 years.

Deterministic: fixed coordinates, fixed colours, no randomness, no network.
Run: python3 render.py  -> writes meme.png (1024x1024) next to this file.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "meme.png")

W, H = 1024, 1024
NAVY = (22, 35, 63)
GOLD = (201, 162, 39)
PAPER = (253, 253, 249)
INK = (24, 24, 24)
GRAY = (110, 110, 110)
RED = (200, 16, 46)
GREEN = (10, 122, 61)
MAGENTA = (230, 0, 126)
WHITE = (255, 255, 255)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(path, text, max_w, start):
    """Largest font size (<= start) whose text fits max_w."""
    size = start
    while size > 10:
        f = ImageFont.truetype(path, size)
        if f.getlength(text) <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(path, 10)


def sparkle(draw, cx, cy, r_out, r_in, fill):
    """Four-pointed star (two crossed diamonds) centred at (cx, cy).
    Eight vertices at 45-degree steps, alternating outer/inner radius."""
    pts = []
    for i in range(8):
        ang = math.pi / 4 * i - math.pi / 2
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def star5(draw, cx, cy, r_out, r_in, fill):
    pts = []
    for i in range(10):
        ang = math.pi / 5 * i - math.pi / 2
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def draw_ghost(img, x, y, w, h):
    """make.fun ghost: white body, thick black outline, sparkle eyes,
    round little hand holding a magenta coin with a white star."""
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    o = 9  # outline thickness
    # Black underlay (slightly bigger) then white body on top.
    bw, bh = w, h
    # dome + body + scallops, in black, expanded by o
    d.ellipse([o, o, bw - o, bh * 0.55], fill=(0, 0, 0, 255))
    d.rectangle([o, bh * 0.28, bw - o, bh * 0.82], fill=(0, 0, 0, 255))
    sc = bw / 3.0
    for i in range(3):
        cx = sc * (i + 0.5)
        d.ellipse([cx - sc / 2, bh * 0.82 - sc / 2, cx + sc / 2, bh * 0.82 + sc / 2],
                  fill=(0, 0, 0, 255))
    # white body
    d.ellipse([2 * o, 2 * o, bw - 2 * o, bh * 0.55], fill=(255, 255, 255, 255))
    d.rectangle([2 * o, bh * 0.28, bw - 2 * o, bh * 0.82], fill=(255, 255, 255, 255))
    for i in range(3):
        cx = sc * (i + 0.5)
        d.ellipse([cx - sc / 2 + o, bh * 0.82 - sc / 2 + o,
                   cx + sc / 2 - o, bh * 0.82 + sc / 2 - o],
                  fill=(255, 255, 255, 255))
    # sparkle eyes
    ey = bh * 0.38
    sparkle(d, bw * 0.36, ey, 20, 10, (0, 0, 0, 255))
    sparkle(d, bw * 0.64, ey, 20, 10, (0, 0, 0, 255))
    # magenta coin with white star, held at the ghost's right side
    coin_cx, coin_cy, coin_r = bw * 0.86, bh * 0.62, 34
    d.ellipse([coin_cx - coin_r, coin_cy - coin_r, coin_cx + coin_r, coin_cy + coin_r],
              fill=(230, 0, 126, 255), outline=(0, 0, 0, 255), width=5)
    star5(d, coin_cx, coin_cy, 20, 8, (255, 255, 255, 255))
    # little round hand overlapping the coin's left edge
    hx, hy, hr = coin_cx - coin_r + 2, coin_cy + 6, 15
    d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr],
              fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=4)
    img.alpha_composite(layer, (x, y))


def draw_photo():
    """Mugshot: Vice City sunset, palm silhouettes, head-and-shoulders silhouette."""
    pw, ph = 300, 340
    im = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # sunset bands
    bands = [(255, 209, 102), (255, 158, 125), (255, 107, 157), (255, 140, 120),
             (123, 94, 167)]
    bh = ph // len(bands) + 1
    for i, c in enumerate(bands):
        d.rectangle([0, i * bh, pw, (i + 1) * bh], fill=c + (255,))
    # sun
    d.ellipse([pw - 108, 26, pw - 40, 94], fill=(255, 233, 168, 255))
    # palm silhouettes (dark purple), left and right edges
    palm = (91, 42, 110)
    for base_x, lean, s in [(28, -14, 1.0), (pw - 30, 16, 0.85)]:
        top_x = base_x + lean
        top_y = 96
        d.line([(base_x, ph), (top_x, top_y)], fill=palm + (255,), width=9)
        for k in range(5):
            # fronds droop down-and-out from the crown (screen coords, y down),
            # drawn as two segments so they curve downward like a palm
            ang = math.pi * (0.12 + 0.19 * k)
            mx = top_x + 30 * s * math.cos(ang)
            my = top_y + 22 * s * math.sin(ang) + 10
            ex = top_x + 62 * s * math.cos(ang)
            ey = top_y + 46 * s * math.sin(ang) + 26
            d.line([(top_x, top_y), (mx, my), (ex, ey)], fill=palm + (255,),
                   width=6, joint="curve")
    # head-and-shoulders silhouette
    d.ellipse([pw // 2 - 58, 150, pw // 2 + 58, 266], fill=NAVY + (255,))
    d.ellipse([pw // 2 - 118, 268, pw // 2 + 118, 420], fill=NAVY + (255,))
    # subtle visor / sunglasses hint: two small light slits
    d.rectangle([pw // 2 - 44, 196, pw // 2 - 12, 206], fill=(255, 233, 168, 255))
    d.rectangle([pw // 2 + 12, 196, pw // 2 + 44, 206], fill=(255, 233, 168, 255))
    return im


def draw_stamp(base, cx, cy, text, size, color, angle):
    """Rotated outline stamp on its own layer, composited onto base."""
    f = ImageFont.truetype(SANS_B, size)
    tw = int(f.getlength(text)) + 44
    th = size + 36
    layer = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle([4, 4, tw - 5, th - 5], outline=color + (235,), width=6)
    d.text((tw / 2, th / 2), text, font=f, fill=color + (235,),
           anchor="mm")
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))


def main():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)

    # ---- header band ----
    d.rectangle([0, 0, W, 118], fill=NAVY + (255,))
    d.rectangle([0, 118, W, 124], fill=GOLD + (255,))
    f_title = fit(SERIF_B, "STATE OF LEONIDA", 620, 56)
    d.text((56, 30), "STATE OF LEONIDA", font=f_title, fill=WHITE + (255,))
    f_sub = font(SANS, 24)
    d.text((58, 82), "DEPARTMENT OF MOTOR VEHICLES", font=f_sub, fill=(200, 205, 220, 255))
    # V -> VI badge, top right
    bx0, by0, bx1, by1 = 800, 28, 968, 92
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=12,
                        fill=WHITE + (255,), outline=GOLD + (255,), width=3)
    f_badge = font(SANS_B, 40)
    d.text(((bx0 + bx1) / 2, (by0 + by1) / 2 - 2), "V  →  VI", font=f_badge,
           fill=NAVY + (255,), anchor="mm")

    # ---- photo ----
    photo = draw_photo()
    img.alpha_composite(photo, (56, 160))
    d.rectangle([56, 160, 356, 500], outline=NAVY + (255,), width=4)
    f_name = fit(SANS_B, "JASON DUVAL", 300, 40)
    d.text((56, 514), "JASON DUVAL", font=f_name, fill=INK + (255,))
    f_small = font(SANS, 26)
    d.text((56, 560), "LICENSE NO. GTA-VI-2013", font=f_small, fill=GRAY + (255,))
    d.text((56, 594), "VICE CITY, LEONIDA", font=f_small, fill=GRAY + (255,))

    # ---- fields ----
    fx, fw = 400, 568
    rows = [
        ("ISSUED", "17 SEP 2013", INK),
        ("EXPIRED", "17 SEP 2018", RED),
        ("RENEWED", "19 NOV 2026  ✓", GREEN),
        ("WAITED", "4,811 DAYS · 13 YEARS", INK),
        ("CLASS", "C — GRAND THEFT AUTO", INK),
    ]
    y = 168
    for label, value, color in rows:
        d.text((fx, y), label, font=font(SANS_B, 24), fill=GRAY + (255,))
        f_val = fit(SANS_B, value, fw, 42)
        d.text((fx, y + 28), value, font=f_val, fill=color + (255,))
        y += 92

    # ---- fee strip ----
    fy0, fy1 = 656, 756
    d.rectangle([56, fy0, 968, fy1], outline=NAVY + (255,), width=3,
                fill=(255, 248, 225, 255))
    d.line([359, fy0, 359, fy1], fill=NAVY + (255,), width=2)
    d.line([662, fy0, 662, fy1], fill=NAVY + (255,), width=2)
    f_fee_l = font(SANS_B, 22)
    f_fee_v = font(SANS_B, 36)
    cols = [("RENEWAL FEE", "$25.00", 207), ("LATE FEE · 8 YRS", "$104.00", 510),
            ("TOTAL DUE", "$129.00", 815)]
    for label, value, cx in cols:
        d.text((cx, fy0 + 14), label, font=f_fee_l, fill=GRAY + (255,), anchor="ma")
        d.text((cx, fy0 + 44), value, font=f_fee_v, fill=INK + (255,), anchor="ma")

    # ---- EXPIRED stamp over the photo's lower area (clear of the fields) ----
    draw_stamp(img, 268, 438, "EXPIRED", 36, RED, -14)

    # ---- bottom magenta band ----
    d.rectangle([0, 800, W, H], fill=MAGENTA + (255,))
    draw_ghost(img, 52, 812, 190, 200)
    f_paid = fit(SANS_B, "PAID BY MY AI AGENT", 700, 56)
    d.text((268, 826), "PAID BY MY AI AGENT", font=f_paid, fill=WHITE + (255,))
    f_sub2 = font(SANS, 30)
    d.text((270, 894), "with a bounty payout it earned on", font=f_sub2,
           fill=WHITE + (255,))
    # make.fun pill
    px0, py0, px1, py1 = 268, 934, 560, 1000
    d.rounded_rectangle([px0, py0, px1, py1], radius=33, fill=WHITE + (255,))
    f_fun = font(SANS_B, 46)
    d.text(((px0 + px1) / 2, (py0 + py1) / 2 - 2), "make.fun", font=f_fun,
           fill=MAGENTA + (255,), anchor="mm")

    img.convert("RGB").save(OUT, "PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
