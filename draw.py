#!/usr/bin/env python3
"""Draw entry.png — a newspaper front page summing up Friday 20 November 2026.

Deterministic: no randomness, no time, no network. Run: python3 draw.py
Writes entry.png (1024x1024, PNG) next to this script.
All facts verified against the day's reporting; see NOTES.md.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (28, 26, 23)
RED = (163, 22, 33)
GRAY = (96, 92, 84)
RULE = (180, 172, 152)
BLUE = (47, 111, 178)
NAVY = (22, 35, 63)
GOLD = (176, 132, 24)
TEAL = (31, 122, 92)
ORANGE = (214, 110, 30)

FD = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FD + name, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def star_points(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def flag_us(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=1)
    for i in range(0, 7, 2):
        d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7], fill=(178, 34, 52))
    cw, ch = w * 0.4, h * 4 / 7
    d.rectangle([x, y, x + cw, y + ch], fill=(60, 59, 110))
    for r in range(3):
        for c in range(3):
            d.ellipse([x + 4 + c * cw / 3.4, y + 3 + r * ch / 3.4,
                       x + 7 + c * cw / 3.4, y + 6 + r * ch / 3.4], fill=(255, 255, 255))


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=INK, width=1)
    d.polygon(star_points(x + w * 0.22, y + h * 0.28, 7, 2.8), fill=(255, 222, 0))
    for sx, sy in [(0.55, 0.18), (0.72, 0.32), (0.68, 0.55), (0.5, 0.62)]:
        d.polygon(star_points(x + w * sx, y + h * sy, 3.5, 1.4), fill=(255, 222, 0))


def flag_ru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=1)
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))


def art_summit(d, x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(220, 235, 245))
    # globe: asymmetric continents, no face-like symmetry
    cx, cy, r = x + w * 0.30, y + h * 0.46, h * 0.30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLUE, outline=(255, 255, 255), width=3)
    d.ellipse([cx - r * 0.78, cy - r * 0.55, cx - r * 0.05, cy + r * 0.05], fill=(61, 139, 64))
    d.ellipse([cx + r * 0.05, cy + r * 0.25, cx + r * 0.62, cy + r * 0.72], fill=(61, 139, 64))
    d.ellipse([cx + r * 0.30, cy - r * 0.62, cx + r * 0.72, cy - r * 0.05], fill=(61, 139, 64))
    # three flags on poles, right side
    fx = x + w * 0.58
    for i, fl in enumerate((flag_us, flag_cn, flag_ru)):
        px = fx + i * (w * 0.15)
        d.line([px + 22, y + 12, px + 22, y + h - 26], fill=INK, width=3)
        fl(d, px, y + 12, 44, 30)


def art_ukraine(d, x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=NAVY)
    for sx, sy in [(0.08, 0.15), (0.22, 0.08), (0.45, 0.2), (0.7, 0.1), (0.9, 0.22), (0.55, 0.06)]:
        d.ellipse([x + w * sx, y + h * sy, x + w * sx + 3, y + h * sy + 3], fill=(255, 255, 255))
    # bridge: two towers + deck + cables
    deck = y + h * 0.72
    d.rectangle([x + 8, deck, x + w - 8, deck + 6], fill=(120, 130, 155))
    for tx in (0.25, 0.68):
        d.rectangle([x + w * tx - 5, y + h * 0.28, x + w * tx + 5, deck], fill=(90, 100, 130))
    for t in (0.05, 0.15, 0.35, 0.45, 0.55, 0.8, 0.9):
        d.line([x + w * t, deck, x + w * (0.25 if t < 0.5 else 0.68), y + h * 0.30],
               fill=(150, 160, 185), width=1)
    # explosion starburst at right tower
    ex, ey = x + w * 0.68, y + h * 0.30
    d.polygon(star_points(ex, ey, 26, 10), fill=(255, 176, 32))
    d.polygon(star_points(ex, ey, 14, 5), fill=(255, 240, 180))
    # missile streak
    d.line([x + w * 0.55, y + h * 0.08, x + w * 0.72, y + h * 0.28], fill=(255, 255, 255), width=3)
    d.line([x + w * 0.48, y + h * 0.05, x + w * 0.55, y + h * 0.08], fill=(255, 176, 32), width=2)


def art_icj(d, x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(232, 226, 210))
    cx = x + w / 2
    base = y + h * 0.82
    d.rectangle([cx - 4, y + h * 0.22, cx + 4, base], fill=GOLD)
    d.polygon([(cx - 10, y + h * 0.18), (cx + 10, y + h * 0.18), (cx, y + h * 0.10)], fill=GOLD)
    d.line([cx - w * 0.34, y + h * 0.26, cx + w * 0.34, y + h * 0.26], fill=GOLD, width=4)
    for s in (-1, 1):
        px = cx + s * w * 0.34
        d.line([px, y + h * 0.26, px, y + h * 0.52], fill=GOLD, width=3)
        d.pieslice([px - 26, y + h * 0.52, px + 26, y + h * 0.78], 0, 180, fill=(200, 162, 39))
        d.line([px - 26, y + h * 0.65, px + 26, y + h * 0.65], fill=GOLD, width=3)
    d.rectangle([cx - 46, base, cx + 46, base + 8], fill=GOLD)
    d.rectangle([cx - 60, base + 8, cx + 60, base + 16], fill=(120, 96, 40))


def art_anthropic(d, x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(238, 243, 234))
    bars = [0.30, 0.45, 0.62, 0.85]
    bw = w * 0.13
    for i, f in enumerate(bars):
        bx = x + w * 0.08 + i * w * 0.20
        bh = h * f
        d.rectangle([bx, y + h * 0.92 - bh, bx + bw, y + h * 0.92], fill=TEAL)
    d.line([x + w * 0.06, y + h * 0.92, x + w * 0.95, y + h * 0.92], fill=INK, width=2)
    d.line([x + w * 0.10, y + h * 0.62, x + w * 0.30, y + h * 0.45,
            x + w * 0.50, y + h * 0.30, x + w * 0.88, y + h * 0.12], fill=RED, width=3)
    d.polygon([(x + w * 0.88, y + h * 0.12), (x + w * 0.80, y + h * 0.12),
               (x + w * 0.88, y + h * 0.20)], fill=RED)


def art_cop(d, x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(253, 240, 213))
    sx, sy, sr = x + w * 0.24, y + h * 0.34, h * 0.22
    for k in range(8):
        a = math.radians(k * 45)
        d.line([sx + (sr + 4) * math.cos(a), sy + (sr + 4) * math.sin(a),
                sx + (sr + 14) * math.cos(a), sy + (sr + 14) * math.sin(a)],
               fill=(240, 180, 40), width=4)
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 200, 60))
    # thermometer
    tx = x + w * 0.62
    d.rounded_rectangle([tx, y + h * 0.12, tx + 22, y + h * 0.78], radius=11, fill=(255, 255, 255),
                        outline=INK, width=2)
    d.ellipse([tx - 8, y + h * 0.68, tx + 30, y + h * 0.94], fill=RED, outline=INK, width=2)
    d.rectangle([tx + 6, y + h * 0.30, tx + 16, y + h * 0.78], fill=RED)
    # rising temperature line, bottom right
    d.line([x + w * 0.80, y + h * 0.80, x + w * 0.86, y + h * 0.66,
            x + w * 0.93, y + h * 0.58], fill=RED, width=3)


def art_gta(d, x, y, w, h):
    # dusk gradient bands
    top, bot = (58, 32, 86), (244, 140, 60)
    steps = 24
    for i in range(steps):
        t = i / (steps - 1)
        c = tuple(int(top[j] + (bot[j] - top[j]) * t) for j in range(3))
        d.rectangle([x, y + i * h / steps, x + w, y + (i + 1) * h / steps + 1], fill=c)
    # sun
    d.ellipse([x + w * 0.62, y + h * 0.12, x + w * 0.82, y + h * 0.42], fill=(255, 214, 120))
    # skyline
    base = y + h * 0.95
    for bx, bw, bh in [(0.02, 0.16, 0.42), (0.20, 0.12, 0.58), (0.34, 0.18, 0.36),
                       (0.54, 0.14, 0.52), (0.70, 0.12, 0.40), (0.84, 0.14, 0.48)]:
        d.rectangle([x + w * bx, base - h * bh, x + w * (bx + bw), base], fill=(30, 18, 48))
    # palm
    px = x + w * 0.10
    d.line([px, base, px + 8, y + h * 0.52], fill=(60, 40, 20), width=5)
    for a in (200, 240, 280, 320):
        r = math.radians(a)
        d.arc([px - 26, y + h * 0.42, px + 34, y + h * 0.72], a - 25, a + 25,
              fill=(46, 120, 60), width=4)
    d.text((x + w * 0.06, y + h * 0.05), "VI", font=SERIF_B(30), fill=(255, 255, 255),
           stroke_width=2, stroke_fill=(30, 18, 48))


def panel(d, x, y, w, h, kicker, kcolor, headline, caption, art, hsize=28, csize=19, ah=78):
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, outline=RULE, width=2)
    ax, ay, aw = x + 10, y + 10, w - 20
    art(d, ax, ay, aw, ah)
    ty = ay + ah + 8
    d.text((x + 12, ty), kicker, font=SANS_B(18), fill=kcolor)
    ty += 25
    hl = wrap(d, headline, SERIF_B(hsize), w - 24)
    ty = text_block(d, x + 12, ty, hl, SERIF_B(hsize), INK, hsize + 6)
    ty += 4
    cl = wrap(d, caption, SANS(csize), w - 24)
    text_block(d, x + 12, ty, cl, SANS(csize), (60, 56, 48), csize + 5)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 26
    # ---- masthead ----
    name = "THE WORLD TODAY"
    nf = SERIF_B(76)
    d.text(((W - d.textlength(name, font=nf)) / 2, 22), name, font=nf, fill=INK)
    d.line([M, 118, W - M, 118], fill=INK, width=3)
    d.line([M, 124, W - M, 124], fill=INK, width=1)
    date = "FRIDAY 20 NOVEMBER 2026"
    df = SANS_B(36)
    d.text(((W - d.textlength(date, font=df)) / 2, 134), date, font=df, fill=RED)
    # ---- lead: Shenzhen summit ----
    ly, lh = 186, 244
    d.rounded_rectangle([M, ly, W - M, ly + lh], radius=6, outline=RULE, width=2)
    d.text((M + 14, ly + 12), "DIPLOMACY  ·  SHENZHEN", font=SANS_B(20), fill=RED)
    hl = wrap(d, "Three powers pledge peace in Shenzhen", SERIF_B(38), 560)
    ty = text_block(d, M + 14, ly + 44, hl, SERIF_B(38), INK, 46)
    cap = wrap(d, "Trump, Xi and Putin's joint declaration agrees new nuclear-risk talks.",
               SANS(23), 560)
    text_block(d, M + 14, ty + 10, cap, SANS(23), (60, 56, 48), 30)
    art_summit(d, 612, ly + 12, W - M - 612, lh - 24)
    # ---- row 2 ----
    ry, rh = 446, 232
    pw = (W - 2 * M - 16) // 2
    panel(d, M, ry, pw, rh, "WAR IN UKRAINE", RED,
          "Mass attack on Kyiv; missiles land in Poland",
          "400+ drones and 110 missiles; 8 killed. Ukraine hits back at the Kerch Bridge.",
          art_ukraine, hsize=28, csize=19, ah=70)
    panel(d, M + pw + 16, ry, pw, rh, "WORLD COURT", (18, 90, 66),
          "Myanmar guilty of Rohingya genocide",
          "The International Court of Justice finds Myanmar responsible for genocide.",
          art_icj, hsize=28, csize=19, ah=70)
    # ---- row 3 ----
    ry2, rh2 = 694, 210
    pw3 = (W - 2 * M - 30) // 3
    panel(d, M, ry2, pw3, rh2, "TECH · MARKETS", TEAL,
          "Anthropic debut tops $2 trillion",
          "Record Nasdaq debut.",
          art_anthropic, hsize=26, csize=18, ah=60)
    panel(d, M + pw3 + 15, ry2, pw3, rh2, "CLIMATE · ANTALYA", ORANGE,
          "Climate talks stall over fossil fuels",
          "Talks run into overtime.",
          art_cop, hsize=26, csize=18, ah=60)
    panel(d, M + 2 * (pw3 + 15), ry2, pw3, rh2, "CULTURE · GAMES", (90, 40, 120),
          "GTA VI: $3.79bn in a day",
          "Biggest first-day sales ever.",
          art_gta, hsize=26, csize=18, ah=60)
    # ---- ticker ----
    ty = 920
    d.rounded_rectangle([M, ty, W - M, ty + 52], radius=6, fill=INK)
    t1 = "ALSO TODAY:  S&P 500 enters correction, down 10% from its high"
    t2 = "Court approves $7.25bn Roundup settlement  •  EU–UK summit in Brussels"
    d.text((M + 14, ty + 5), t1, font=SANS_B(18), fill=PAPER)
    d.text((M + 14, ty + 28), t2, font=SANS(18), fill=(220, 214, 196))
    # ---- footer ----
    foot = "All events of Friday 20 November 2026  ·  Drawn from the day's reporting"
    ff = SANS(16)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 984), foot, font=ff, fill=GRAY)
    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
