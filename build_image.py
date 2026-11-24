#!/usr/bin/env python3
"""Draw THE WORLD TODAY for Tuesday 24 November 2026, 1024x1024 PNG.

Deterministic front page generator summing up world news of 24 Nov 2026.
Uses only fixed values: fixed palette, local DejaVu fonts, no randomness,
no clock, and no network access.
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PAGE_SIZE = 1024

# Fixed palette
PAPER = (248, 243, 232)
INK = (24, 24, 24)
RED = (168, 24, 34)
NAVY = (30, 56, 94)
GREY = (105, 105, 105)
HAIRLINE = (212, 206, 196)

# DejaVu fonts
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FONT_SERIF_BOLD = f"{FONT_DIR}/DejaVuSerif-Bold.ttf"
FONT_SERIF_REG = f"{FONT_DIR}/DejaVuSerif.ttf"
FONT_SANS_BOLD = f"{FONT_DIR}/DejaVuSans-Bold.ttf"
FONT_SANS_REG = f"{FONT_DIR}/DejaVuSans.ttf"


def wrap_text(draw, text, font, max_width):
    """Word-wrap text into lines fitting within max_width."""
    words = text.split()
    lines = []
    current = ""
    for w in words:
        test = f"{current} {w}".strip()
        if draw.textlength(test, font=font) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def fit_headline_font(draw, text, font_path, max_width, start_size=24, min_size=10):
    """Shrink headline font size until the text fits within max_width."""
    size = start_size
    font = ImageFont.truetype(font_path, size)
    while size > min_size and draw.textlength(text, font=font) > max_width:
        size -= 1
        font = ImageFont.truetype(font_path, size)
    return font


def draw_illustration(draw, box):
    """Draw dusk over the Antalya shore:

    Sky gradient from dark slate blue at top through burnt orange to pale gold at horizon,
    a low sun half hidden behind a dark cloud bank, calm sea with horizontal lines,
    dark hills and a small minaret silhouette on the left, and caption at bottom left.
    """
    x0, y0, x1, y1 = box
    horizon_y = y0 + 190

    # 1. Sky gradient
    c_top = (28, 42, 68)       # dark slate blue
    c_mid = (204, 82, 34)      # burnt orange
    c_horiz = (244, 196, 114)  # pale gold
    y_mid = y0 + 115

    for yy in range(y0, horizon_y):
        if yy < y_mid:
            t = (yy - y0) / max(1, y_mid - y0)
            col = tuple(int(c_top[i] + t * (c_mid[i] - c_top[i])) for i in range(3))
        else:
            t = (yy - y_mid) / max(1, horizon_y - y_mid)
            col = tuple(int(c_mid[i] + t * (c_horiz[i] - c_mid[i])) for i in range(3))
        draw.line([(x0, yy), (x1, yy)], fill=col)

    # 2. Low sun
    sun_x = x0 + 245
    sun_y = horizon_y - 20
    r = 24
    draw.ellipse([sun_x - r - 6, sun_y - r - 6, sun_x + r + 6, sun_y + r + 6], fill=(248, 185, 95))
    draw.ellipse([sun_x - r, sun_y - r, sun_x + r, sun_y + r], fill=(255, 240, 175))

    # 3. Dark cloud bank half hiding sun
    cloud_col = (36, 40, 50)
    draw.ellipse([sun_x - 75, sun_y + 2, sun_x + 55, sun_y + 26], fill=cloud_col)
    draw.ellipse([sun_x - 35, sun_y - 2, sun_x + 80, sun_y + 22], fill=cloud_col)
    draw.ellipse([sun_x + 25, sun_y + 4, sun_x + 95, sun_y + 28], fill=cloud_col)
    draw.ellipse([sun_x - 85, sun_y + 8, sun_x - 15, sun_y + 26], fill=cloud_col)
    draw.ellipse([sun_x - 50, sun_y - 12, sun_x + 30, sun_y - 7], fill=(52, 48, 58))

    # 4. Calm sea gradient
    c_sea_top = (22, 42, 66)
    c_sea_bot = (14, 24, 38)
    for yy in range(horizon_y, y1):
        t = (yy - horizon_y) / max(1, y1 - horizon_y)
        col = tuple(int(c_sea_top[i] + t * (c_sea_bot[i] - c_sea_top[i])) for i in range(3))
        draw.line([(x0, yy), (x1, yy)], fill=col)

    # 5. Calm sea horizontal lines (amber reflection under sun & cool ripples)
    ref_lines = [
        (horizon_y + 4, sun_x - 18, sun_x + 18, (235, 185, 100)),
        (horizon_y + 10, sun_x - 30, sun_x + 25, (215, 165, 85)),
        (horizon_y + 18, sun_x - 42, sun_x + 38, (190, 140, 70)),
        (horizon_y + 28, sun_x - 52, sun_x + 48, (160, 115, 60)),
        (horizon_y + 42, sun_x - 60, sun_x + 50, (130, 95, 55)),
        (horizon_y + 58, sun_x - 45, sun_x + 35, (105, 80, 50)),
        (horizon_y + 76, sun_x - 30, sun_x + 22, (80, 65, 45)),
        (horizon_y + 14, x0 + 175, x0 + 205, (45, 68, 95)),
        (horizon_y + 36, x0 + 125, x0 + 175, (40, 60, 85)),
        (horizon_y + 54, x0 + 285, x0 + 345, (36, 54, 78)),
        (horizon_y + 72, x0 + 145, x0 + 215, (32, 48, 70)),
    ]
    for y_pos, rx0, rx1, col in ref_lines:
        draw.line([(rx0, y_pos), (rx1, y_pos)], fill=col, width=1)

    # 6. Dark hills and small minaret silhouette on the left
    hill_col = (16, 20, 26)
    hill_pts = [
        (x0, y1),
        (x0, horizon_y - 48),
        (x0 + 30, horizon_y - 58),
        (x0 + 65, horizon_y - 52),
        (x0 + 100, horizon_y - 36),
        (x0 + 135, horizon_y - 18),
        (x0 + 165, horizon_y + 4),
        (x0 + 185, horizon_y + 22),
        (x0 + 185, y1),
    ]
    draw.polygon(hill_pts, fill=hill_col)

    # Mosque dome & minaret silhouette
    draw.ellipse([x0 + 72, horizon_y - 68, x0 + 96, horizon_y - 48], fill=hill_col)
    mx = x0 + 58
    draw.rectangle([mx - 3, horizon_y - 92, mx + 3, horizon_y - 52], fill=hill_col)
    draw.rectangle([mx - 6, horizon_y - 84, mx + 6, horizon_y - 80], fill=hill_col)
    draw.rectangle([mx - 2, horizon_y - 100, mx + 2, horizon_y - 92], fill=hill_col)
    draw.polygon([(mx - 3, horizon_y - 100), (mx + 3, horizon_y - 100), (mx, horizon_y - 112)], fill=hill_col)
    draw.line([(mx, horizon_y - 112), (mx, horizon_y - 116)], fill=hill_col, width=1)

    # 7. Caption ANTALYA, TURKIYE in white bold sans at bottom left
    caption_font = ImageFont.truetype(FONT_SANS_BOLD, 11)
    draw.rectangle([x0 + 12, y1 - 25, x0 + 140, y1 - 9], fill=(16, 20, 26))
    draw.text((x0 + 16, y1 - 23), "ANTALYA, TURKIYE", font=caption_font, fill=(255, 255, 255))

    # Frame
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=1)


def generate_page(output_path):
    """Draw and save the 1024x1024 front page."""
    im = Image.new("RGB", (PAGE_SIZE, PAGE_SIZE), PAPER)
    draw = ImageDraw.Draw(im)

    # Outer subtle border
    draw.rectangle([16, 16, PAGE_SIZE - 16, PAGE_SIZE - 16], outline=HAIRLINE, width=1)

    # 1. Nameplate centered at top
    name = "THE WORLD TODAY"
    f_name = ImageFont.truetype(FONT_SERIF_BOLD, 56)
    w_name = draw.textlength(name, font=f_name)
    draw.text(((PAGE_SIZE - w_name) / 2, 22), name, font=f_name, fill=INK)

    # Double rule below nameplate
    draw.line([(32, 84), (PAGE_SIZE - 32, 84)], fill=INK, width=3)
    draw.line([(32, 90), (PAGE_SIZE - 32, 90)], fill=INK, width=1)

    # Dateline in red bold sans
    dateline = "TUESDAY, 24 NOVEMBER 2026 | ONE DAY, ONE IMAGE"
    f_date = ImageFont.truetype(FONT_SANS_BOLD, 13)
    w_date = draw.textlength(dateline, font=f_date)
    draw.text(((PAGE_SIZE - w_date) / 2, 95), dateline, font=f_date, fill=RED)

    # Dividing rule below dateline
    draw.line([(32, 114), (PAGE_SIZE - 32, 114)], fill=NAVY, width=1)

    # 2. Lead story top-left (width 560) and illustration top-right (368 wide, 300 tall)
    y_lead = 124
    lead_col_w = 560

    # Lead kicker
    f_kicker = ImageFont.truetype(FONT_SANS_BOLD, 13)
    draw.text((32, y_lead), "CLIMATE", font=f_kicker, fill=RED)
    y_lead += 13 + 6

    # Lead headline (shrunk until it fits column width)
    lead_head = "COP31 COLLAPSES WITH NO DEAL"
    f_lead_head = fit_headline_font(draw, lead_head, FONT_SERIF_BOLD, lead_col_w, start_size=32)
    draw.text((32, y_lead), lead_head, font=f_lead_head, fill=INK)
    y_lead += f_lead_head.size + 8

    # Lead deck
    lead_deck = "Antalya talks end with no pact as fossil-fuel language is stripped out."
    f_lead_deck = ImageFont.truetype(FONT_SANS_BOLD, 15)
    for line in wrap_text(draw, lead_deck, f_lead_deck, lead_col_w):
        draw.text((32, y_lead), line, font=f_lead_deck, fill=NAVY)
        y_lead += 15 + 4
    y_lead += 4

    # Red accent bar
    draw.line([(32, y_lead), (32 + 80, y_lead)], fill=RED, width=2)
    y_lead += 10

    # Lead body
    lead_body = (
        "After more than two weeks in Antalya, Turkiye, COP31 ended on Sunday 22 November "
        "with no agreement, the longest climate conference in history. The final Antalya Pact draft "
        "mentioned fossil fuels not at all, so the EU, Britain and Pacific island nations rejected it. "
        "UN chief Antonio Guterres said he was deeply disappointed."
    )
    f_lead_body = ImageFont.truetype(FONT_SERIF_REG, 13.5)
    for line in wrap_text(draw, lead_body, f_lead_body, lead_col_w):
        draw.text((32, y_lead), line, font=f_lead_body, fill=INK)
        y_lead += 13.5 + 6.5

    # Vertical hairline rule separating lead story and illustration panel
    draw.line([(608, 124), (608, 424)], fill=HAIRLINE, width=1)

    # Illustration panel: top-right (368 wide, 300 tall)
    draw_illustration(draw, (624, 124, 992, 424))

    # Double rule below lead section
    draw.line([(32, 434), (PAGE_SIZE - 32, 434)], fill=INK, width=2)
    draw.line([(32, 438), (PAGE_SIZE - 32, 438)], fill=NAVY, width=1)

    # 3. Six story cards in a 2 column by 3 row grid below
    cards = [
        ("MARKETS", "HUANG IS BACK; NVIDIA SOARS 31%",
         "Jensen Huang is reinstated as Nvidia chief executive 11 days after resigning. Shares jump 31 percent on Monday 23 November, the best day since 2003, adding about 950 billion dollars in value. The Nasdaq rises 6.5 percent and the S and P 500 rises 4.7 percent."),
        ("BALTIC SEA", "RUSSIAN SHIP ABLAZE AFTER DRONE HIT",
         "The cargo ship Sparta II catches fire in the Gulf of Finland after a reported drone attack and drifts toward Finnish waters. Ukraine also claims it sank a Russian warship off the coast of Libya."),
        ("UKRAINE", "KYIV REGION HIT IN OVERNIGHT STRIKES",
         "Russian drone and missile attacks strike the Kyiv region, damaging a home in Dymer, with several people missing, as the war keeps spilling across borders."),
        ("INDONESIA", "FACTORY FIRE KILLS AT LEAST 24",
         "A fire at a candy factory in Banten province kills at least 24 workers, with rescuers still searching for the missing."),
        ("PORTUGAL", "THOUSANDS MARCH OVER LIVING COSTS",
         "Thousands take to the streets of Lisbon to protest against rising living costs."),
        ("SPORT", "ALCARAZ WINS FIRST ATP FINALS TITLE",
         "Carlos Alcaraz beats Alexander Zverev in Turin for his maiden ATP Finals crown, while world chess champion Gukesh begins his title defence against Sindarov in Geneva."),
    ]

    # Vertical dividing rule between columns
    draw.line([(512, 448), (512, 936)], fill=HAIRLINE, width=1)

    # Horizontal dividing rules between rows
    draw.line([(32, 606), (PAGE_SIZE - 32, 606)], fill=HAIRLINE, width=1)
    draw.line([(32, 772), (PAGE_SIZE - 32, 772)], fill=HAIRLINE, width=1)

    f_card_kicker = ImageFont.truetype(FONT_SANS_BOLD, 12)
    f_card_body = ImageFont.truetype(FONT_SERIF_REG, 12.5)

    row_ys = [448, 614, 780]
    col_xs = [32, 532]
    col_w = 460

    for idx, (kicker, head, body) in enumerate(cards):
        r = idx // 2
        c = idx % 2
        bx = col_xs[c]
        by = row_ys[r] + 4

        # Red kicker
        draw.text((bx, by), kicker, font=f_card_kicker, fill=RED)
        by += 12 + 6

        # Bold serif headline shrunk to fit column width
        f_head = fit_headline_font(draw, head, FONT_SERIF_BOLD, col_w, start_size=21, min_size=11)
        draw.text((bx, by), head, font=f_head, fill=INK)
        by += f_head.size + 7

        # 2 to 3 lines of body text wrapped to column width
        for line in wrap_text(draw, body, f_card_body, col_w):
            draw.text((bx, by), line, font=f_card_body, fill=INK)
            by += 12.5 + 5.5

    # 4. Divider above footer
    draw.line([(32, 942), (PAGE_SIZE - 32, 942)], fill=INK, width=2)
    draw.line([(32, 946), (PAGE_SIZE - 32, 946)], fill=HAIRLINE, width=1)

    # 5. Footer with three short one-line items in small grey text
    f_footer = ImageFont.truetype(FONT_SANS_REG, 11)
    footer_items = [
        "• Rishabh Pant hits 128 as India draw the first Test with New Zealand in Wellington.",
        "• Max Verstappen wins the Las Vegas Grand Prix.",
        "• India and Nepal open the Saryu-Kamala Express rail link between Ayodhya and Janakpur.",
    ]
    fy = 956
    for item in footer_items:
        draw.text((32, fy), item, font=f_footer, fill=GREY)
        fy += 11 + 7

    # Save PNG with optimize=True
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, format="PNG", optimize=True)
    print(f"Wrote {out} ({out.stat().st_size} bytes)")


def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("entry.png")
    generate_page(target)


if __name__ == "__main__":
    main()
