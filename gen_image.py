#!/usr/bin/env python3
"""Render a one-page front page summing up world news of 25 November 2026.

Original artwork drawn procedurally with Pillow only (stdlib + Pillow).
Deterministic: same bytes on every run, no network, no timestamps.
Output: entry.png (1024x1024, < 1 MiB) next to this script.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)      # off-white newsprint
INK = (27, 36, 54)           # ink navy/black
RED = (179, 32, 44)          # lead accent
GREY = (110, 108, 96)
LINE = (27, 36, 54)
PANEL_BG = (255, 253, 246)
PANEL_LINE = (196, 188, 168)
BODY = (58, 58, 52)

REGION_COLORS = {
    "AMERICAS": (122, 92, 46),
    "EUROPE": (74, 107, 138),
    "MIDDLE EAST": (138, 90, 60),
    "GLOBAL": (90, 107, 82),
    "ASIA": (107, 90, 122),
    "AFRICA": (150, 110, 40),
    "TECH": (40, 110, 95),
    "SPORT": (40, 110, 95),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.load_default()


F_TITLE = font("DejaVuSans-Bold.ttf", 64)
F_DATE = font("DejaVuSans-Bold.ttf", 32)
F_LEAD_TAG = font("DejaVuSans-Bold.ttf", 20)
F_LEAD_HEAD = font("DejaVuSans-Bold.ttf", 54)
F_LEAD_DECK = font("DejaVuSans.ttf", 20)
F_TAG = font("DejaVuSans-Bold.ttf", 15)
F_HEAD = font("DejaVuSans-Bold.ttf", 28)
F_DECK = font("DejaVuSans.ttf", 20)
F_TICKER_HEAD = font("DejaVuSans-Bold.ttf", 18)
F_TICKER = font("DejaVuSans.ttf", 20)
F_FOOT = font("DejaVuSans.ttf", 20)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_spaced(draw, cx, y, text, fnt, fill, spacing=4):
    """Draw text centred on cx with extra letter spacing."""
    total = sum(draw.textlength(ch, font=fnt) for ch in text)
    total += spacing * (len(text) - 1)
    x = cx - total / 2
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + spacing


def star_points(cx, cy, r_out, r_in, n=5):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def pictogram(draw, kind, x, y, s=36):
    """Small procedural pictogram inside a s x s box at (x, y)."""
    c = INK
    if kind == "lock":  # cyberattack on CIA / ODNI
        draw.arc([x + 9, y + 2, x + s - 9, y + 22], 180, 360, fill=c, width=3)
        draw.rectangle([x + 5, y + 15, x + s - 5, y + s - 3],
                       outline=c, width=2)
        draw.ellipse([x + s / 2 - 3, y + 20, x + s / 2 + 3, y + 26],
                     fill=(179, 32, 44))
        draw.line([x + s / 2, y + 25, x + s / 2, y + 30], fill=c, width=2)
    elif kind == "ship":  # drone strike on cargo ship
        draw.polygon([(x + 3, y + 20), (x + s - 3, y + 20),
                      (x + s - 8, y + 30), (x + 8, y + 30)], fill=c)
        draw.rectangle([x + 8, y + 11, x + 16, y + 19], fill=(74, 107, 138))
        draw.rectangle([x + 18, y + 11, x + 26, y + 19], fill=(179, 32, 44))
        draw.line([x + s / 2, y + 2, x + s / 2, y + 11], fill=c, width=2)
        draw.line([x + 2, y + 33, x + s - 2, y + 33], fill=(74, 107, 138),
                  width=2)
    elif kind == "scales":  # Huawei trial verdict
        draw.line([x + s / 2, y + 4, x + s / 2, y + s - 4], fill=c, width=2)
        draw.line([x + 5, y + 9, x + s - 5, y + 9], fill=c, width=2)
        draw.polygon([(x + 5, y + 9), (x + 12, y + 22), (x - 2, y + 22)],
                     outline=c, width=2)
        draw.polygon([(x + s - 5, y + 9), (x + s - 12, y + 22),
                      (x + s + 2, y + 22)], outline=c, width=2)
        draw.line([x + 8, y + s - 4, x + s - 8, y + s - 4], fill=c, width=2)
    elif kind == "gavel":  # Sarkozy corruption trial
        draw.polygon([(x + 8, y + 4), (x + s - 4, y + 12),
                      (x + s - 10, y + 18), (x + 2, y + 10)], fill=c)
        draw.line([x + 14, y + 16, x + s - 6, y + 28], fill=c, width=3)
        draw.line([x + 6, y + 30, x + s - 2, y + 30], fill=(74, 107, 138),
                  width=3)
    elif kind == "cross":  # WHO Ebola hospital evacuation
        draw.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], outline=c, width=2)
        draw.rectangle([x + s / 2 - 3, y + 9, x + s / 2 + 3, y + s - 9],
                       fill=(179, 32, 44))
        draw.rectangle([x + 9, y + s / 2 - 3, x + s - 9, y + s / 2 + 3],
                       fill=(179, 32, 44))
    elif kind == "radar":  # AWACS early-warning aircraft
        draw.ellipse([x + 4, y + 2, x + s - 4, y + 18], outline=c, width=2)
        draw.arc([x + 8, y + 5, x + s - 8, y + 15], 180, 360, fill=c, width=2)
        draw.line([x + 6, y + 22, x + s - 6, y + 22], fill=c, width=2)
        draw.line([x + 10, y + 22, x + 8, y + 30], fill=c, width=2)
        draw.line([x + s - 10, y + 22, x + s - 8, y + 30], fill=c, width=2)
        draw.line([x + 2, y + 32, x + s - 2, y + 32], fill=(74, 107, 138),
                  width=2)
    elif kind == "flame":  # Houthi advance on Aden
        draw.polygon([(x + s / 2, y + 1), (x + s - 3, y + 16),
                      (x + s - 6, y + 27), (x + s / 2 + 4, y + 33),
                      (x + s / 2 - 5, y + 33), (x + 3, y + 24),
                      (x + 8, y + 14)], fill=(196, 74, 32))
        draw.polygon([(x + s / 2, y + 15), (x + s - 9, y + 26),
                      (x + s / 2, y + 31), (x + 9, y + 26)],
                     fill=(232, 164, 32))
    elif kind == "chip":  # Nvidia / AI chip
        draw.rectangle([x + 6, y + 8, x + s - 6, y + s - 8], outline=c, width=2)
        draw.rectangle([x + s * 0.36, y + s * 0.42, x + s * 0.64, y + s * 0.58],
                       fill=(40, 110, 95))
        for px in (x + 11, x + s // 2 - 1, x + s - 15):
            draw.line([px, y + 2, px, y + 8], fill=c, width=2)
            draw.line([px, y + s - 8, px, y + s - 2], fill=c, width=2)
    elif kind == "medal":  # Medal of Freedom
        draw.polygon([(x + 10, y + 2), (x + 14, y + 12), (x + s - 14, y + 12),
                      (x + s - 10, y + 2)], fill=(179, 32, 44))
        draw.ellipse([x + 6, y + 12, x + s - 6, y + s - 2], outline=c, width=2)
        draw.polygon(star_points(x + s / 2, y + s / 2 + 3, 7, 3),
                     fill=(122, 92, 46))
    elif kind == "bat":  # cricket
        draw.rectangle([x + 12, y + 12, x + 22, y + 30], outline=c, width=2)
        draw.line([x + 17, y + 2, x + 17, y + 12], fill=c, width=3)
        draw.ellipse([x + 24, y + 26, x + 31, y + 33], fill=RED)


STORIES = [
    # (headline, deck, region, pictogram)
    ("Ukraine hits Russian ship",
     "Gulf of Finland strike; Norway urges caution.",
     "EUROPE", "ship"),
    ("Huawei guilty on 10 of 12 counts",
     "Guilty of trade-secret theft and bank fraud.",
     "TECH", "scales"),
    ("Sarkozy sent to trial",
     "Corruption case, with wife Carla Bruni, goes to court.",
     "EUROPE", "gavel"),
    ("WHO flees Ebola hospital",
     "Staff flee Akwe after 3 days sheltering.",
     "AFRICA", "cross"),
    ("NATO sends AWACS to Poland",
     "After Russian missiles landed on Polish soil.",
     "EUROPE", "radar"),
    ("Houthis close in on Aden",
     "60 km from Yemen's capital; army holds line.",
     "MIDDLE EAST", "flame"),
    ("Huang recoups $34bn in a day",
     "Shares close +31.5% on his first day back as CEO.",
     "TECH", "chip"),
    ("Giuliani gets Medal of Freedom",
     "Trump honours him \u2014 and pardons two turkeys.",
     "AMERICAS", "medal"),
    ("England level T20 series",
     "8-wicket win over Australia in the 2nd T20I.",
     "SPORT", "bat"),
]

TICKER = [
    "5.6 quake hits Nepal's Koshi Province",
    "EU announces further Russia sanctions",
    "Sensex drops 1,484 points",
    "Fort Hood shooter Hasan seeks stay",
    "Abrego Garcia to leave US voluntarily",
    "Tedros: lift US fuel blockade on Cuba",
    "BJP\u2013Akali Dal ally for 2027 Punjab polls",
    "Nepal PM Balendra Shah visits India",
    "Trump pardons turkeys Freedom, Feathers",
    "Norway urges caution on ship strike",
    "Army: Houthis 'won't seize Aden'",
]


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28  # margin
    right = W - mx

    # ---- Masthead ----
    d.text((W / 2, 20), "THE WORLD IN ONE PAGE", font=F_TITLE,
           fill=INK, anchor="ma")
    draw_spaced(d, W / 2, 96, "WEDNESDAY 25 NOVEMBER 2026", F_DATE, RED,
                spacing=5)
    d.line([(mx, 140), (right, 140)], fill=LINE, width=3)
    d.line([(mx, 146), (right, 146)], fill=LINE, width=1)

    # ---- Lead panel: CIA / ODNI cyberattack ----
    ly0, ly1 = 158, 348
    d.rectangle([mx, ly0, right, ly1], fill=PANEL_BG, outline=RED, width=3)
    tag_txt = "LEAD \u00b7 CYBERATTACK"
    tag_w = int(d.textlength(tag_txt, font=F_LEAD_TAG)) + 16
    d.rectangle([mx + 10, ly0 + 10, mx + 10 + tag_w, ly0 + 38], fill=RED)
    d.text((mx + 16, ly0 + 13), tag_txt, font=F_LEAD_TAG,
           fill=(255, 255, 255))
    pictogram(d, "lock", right - 56, ly0 + 8, 44)
    head = "CIA, ODNI hit by cyberattack"
    lines = wrap(d, head, F_LEAD_HEAD, right - mx - 24)
    y = ly0 + 54
    for ln in lines:
        d.text((mx + 12, y), ln, font=F_LEAD_HEAD, fill=INK)
        y += 60
    deck = ("The CIA and the Office of the Director of National Intelligence "
            "are hit; classified information is affected, CNN reports.")
    for ln in wrap(d, deck, F_LEAD_DECK, right - mx - 24):
        d.text((mx + 12, y), ln, font=F_LEAD_DECK, fill=BODY)
        y += 24

    # ---- Grid of 9 story panels ----
    gx0, gy0 = mx, 360
    pw, ph, gap = 312, 136, 12
    for i, (head, deck, region, pic) in enumerate(STORIES):
        col, row = i % 3, i // 3
        x0 = gx0 + col * (pw + gap)
        y0 = gy0 + row * (ph + gap)
        x1, y1 = x0 + pw, y0 + ph
        d.rectangle([x0, y0, x1, y1], fill=PANEL_BG, outline=PANEL_LINE,
                    width=1)
        rc = REGION_COLORS[region]
        d.text((x0 + 10, y0 + 8), region, font=F_TAG, fill=rc)
        d.line([(x0 + 10, y0 + 28), (x0 + 10 + d.textlength(region, font=F_TAG),
                 y0 + 28)], fill=rc, width=2)
        pictogram(d, pic, x1 - 40, y0 + 2, 26)
        hlines = wrap(d, head, F_HEAD, pw - 20)
        assert len(hlines) <= 2, (head, hlines)
        y = y0 + 30
        for ln in hlines[:2]:
            d.text((x0 + 10, y), ln, font=F_HEAD, fill=INK)
            y += 30
        dlines = wrap(d, deck, F_DECK, pw - 20)
        assert len(dlines) <= 2, (deck, dlines)
        for ln in dlines[:2]:
            d.text((x0 + 10, y), ln, font=F_DECK, fill=BODY)
            y += 22

    # ---- Ticker strip: stories 10-20 ----
    ty0 = gy0 + 3 * ph + 2 * gap + 14  # 806
    d.line([(mx, ty0), (right, ty0)], fill=LINE, width=2)
    d.text((mx, ty0 + 8), "ALSO TODAY", font=F_TICKER_HEAD, fill=RED)
    col_w = (right - mx - 24) // 2
    left, right_col = TICKER[:6], TICKER[6:]
    assert len(TICKER) == 11, "ticker must hold exactly 11 items"
    y = ty0 + 32
    for item in left:
        assert d.textlength("\u2022  " + item, font=F_TICKER) <= col_w, item
        d.text((mx, y), "\u2022  " + item, font=F_TICKER, fill=INK)
        y += 24
    y = ty0 + 32
    for item in right_col:
        d.text((mx + col_w + 24, y), "\u2022  " + item, font=F_TICKER, fill=INK)
        y += 24

    # ---- Footer ----
    fy = 994
    d.line([(mx, fy), (right, fy)], fill=LINE, width=1)
    d.text((W / 2, fy + 8), "25 November 2026 \u00b7 21 stories",
           font=F_FOOT, fill=GREY, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG")
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    render()
