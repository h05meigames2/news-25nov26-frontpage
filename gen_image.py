#!/usr/bin/env python3
"""Render a 1024x1024 newspaper front page for 25 November 2026.

Deterministic: no timestamps, no randomness, fixed layout and fonts.
Run:  python3 gen_image.py   -> writes entry.png next to this file.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 34
CONTENT_W = W - 2 * MARGIN

PAPER = (253, 252, 246)
INK = (18, 18, 18)
RULE = (18, 18, 18)
ACCENT = (158, 27, 27)
MUTED = (90, 86, 78)
PANEL_BG = (255, 255, 255)
PANEL_EDGE = (205, 200, 188)
TICKER_BG = (24, 24, 24)
TICKER_FG = (240, 238, 230)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def fit_lines(draw, text, font, max_w, max_lines=None):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if max_lines is not None:
        lines = lines[:max_lines]
    return lines


def draw_block(draw, lines, font, x, y, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def story_card(draw, box, kicker, headline, deck):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=PANEL_BG, outline=PANEL_EDGE, width=1)
    draw.rectangle([x0, y0, x1, y0 + 4], fill=ACCENT)
    pad = 12
    inner_w = (x1 - x0) - 2 * pad
    cx = x0 + pad
    cy = y0 + 14
    k_font = load(SANS_B, 11)
    h_font = load(SERIF_B, 17)
    d_font = load(SANS, 14)
    draw.text((cx, cy), kicker.upper(), font=k_font, fill=ACCENT)
    cy += 20
    h_lines = fit_lines(draw, headline, h_font, inner_w, max_lines=2)
    cy = draw_block(draw, h_lines, h_font, cx, cy, INK, 21)
    cy += 4
    d_lines = fit_lines(draw, deck, d_font, inner_w, max_lines=3)
    draw_block(draw, d_lines, d_font, cx, cy, MUTED, 18)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead ----
    title_font = load(SERIF_B, 52)
    title = "THE WORLD IN ONE PAGE"
    tw = draw.textlength(title, font=title_font)
    draw.text(((W - tw) / 2, 26), title, font=title_font, fill=INK)

    date_font = load(SANS, 16)
    dateline = "Wednesday 25 November 2026  •  One page, the whole world"
    dw = draw.textlength(dateline, font=date_font)
    draw.text(((W - dw) / 2, 96), dateline, font=date_font, fill=MUTED)

    draw.line([(MARGIN, 128), (W - MARGIN, 128)], fill=RULE, width=3)
    draw.line([(MARGIN, 134), (W - MARGIN, 134)], fill=RULE, width=1)

    # ---- Lead story ----
    lead = (MARGIN, 150, W - MARGIN, 330)
    draw.rectangle(lead, fill=PANEL_BG, outline=PANEL_EDGE, width=1)
    draw.rectangle([lead[0], lead[1], lead[2], lead[1] + 5], fill=ACCENT)
    lx = MARGIN + 16
    ly = 168
    kick_font = load(SANS_B, 13)
    draw.text((lx, ly), "LEAD STORY  —  CYBERATTACK  •  CNN", font=kick_font,
              fill=ACCENT)
    ly += 26
    head_font = load(SERIF_B, 29)
    head = ("CIA and spy chief's office hit by cyberattack "
            "affecting classified information")
    h_lines = fit_lines(draw, head, head_font, CONTENT_W - 32, max_lines=2)
    ly = draw_block(draw, h_lines, head_font, lx, ly, INK, 35)
    ly += 8
    deck_font = load(SANS, 16)
    deck = ("The CIA and the Office of the Director of National Intelligence "
            "were hit by a cyberattack affecting classified information, "
            "CNN reported on 25 November.")
    d_lines = fit_lines(draw, deck, deck_font, CONTENT_W - 32, max_lines=2)
    draw_block(draw, d_lines, deck_font, lx, ly, MUTED, 21)

    # ---- Nine story panels, 3 x 3 ----
    stories = [
        ("World", "Ukraine drone strike hits Russian ship",
         "Zelenskiy confirms the attack in the Gulf of Finland; Norway urges caution."),
        ("Business", "Huawei guilty on 10 of 12 counts",
         "US jury convicts on trade-secret theft and bank fraud."),
        ("Europe", "Sarkozy corruption case goes to trial",
         "French officials order the ex-president to face trial."),
        ("Health", "WHO flees Ebola hospital in Congo",
         "Staff evacuated from Akwe after three days sheltering from fighting."),
        ("Security", "NATO sends AWACS to Poland",
         "Early-warning jets deploy after Russian missiles landed."),
        ("Middle East", "Houthis close in on Aden",
         "Fighters push to within 60 km of the southern port city."),
        ("Markets", "Huang recoups $34bn in a day",
         "Nvidia shares jump 31.5% as Jensen Huang is reinstated as CEO."),
        ("USA", "Giuliani awarded Medal of Freedom",
         "Trump honours the former New York mayor."),
        ("Sport", "England crush Australia by 8 wickets",
         "Visitors win the 2nd T20I with ease."),
    ]
    gap = 12
    cell_w = (CONTENT_W - 2 * gap) // 3
    cell_h = 170
    top = 346
    for idx, (kicker, headline, deck) in enumerate(stories):
        row, col = divmod(idx, 3)
        x0 = MARGIN + col * (cell_w + gap)
        y0 = top + row * (cell_h + gap)
        story_card(draw, (x0, y0, x0 + cell_w, y0 + cell_h),
                   kicker, headline, deck)

    # ---- "Also today" ticker ----
    tick = (MARGIN, 896, W - MARGIN, 994)
    draw.rectangle(tick, fill=TICKER_BG)
    tx = MARGIN + 14
    ty = 908
    label_font = load(SANS_B, 13)
    draw.text((tx, ty), "ALSO TODAY", font=label_font, fill=(232, 184, 84))
    ty += 22
    ticker_font = load(SANS, 13)
    items = [
        "5.6 quake in Nepal's Koshi Province",
        "EU adds Russia sanctions",
        "Sensex down 1,484 points",
        "Fort Hood shooter Hasan seeks stay of execution",
        "Abrego Garcia to leave US voluntarily",
        "Tedros: lift US fuel blockade on Cuba",
        "BJP-Akali Dal pact for 2027 Punjab polls",
        "Nepal PM Shah's India visit",
        "Trump pardons turkeys Freedom and Feathers",
    ]
    ticker = "  •  ".join(items)
    t_lines = fit_lines(draw, ticker, ticker_font, CONTENT_W - 28, max_lines=3)
    draw_block(draw, t_lines, ticker_font, tx, ty, TICKER_FG, 16)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    build()
