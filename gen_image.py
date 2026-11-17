#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news front page (1024x1024 PNG).

Built locally with Pillow; the entry program (main.py, stdlib only) simply
copies the finished image. Deterministic: fixed geometry, fixed text, no
randomness, no timestamps embedded.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (18, 18, 18)
RED = (178, 34, 34)
NAVY = (23, 42, 74)
SEA = (28, 68, 110)
TEAL = (16, 96, 110)
GREY = (90, 90, 88)
LIGHT = (232, 226, 210)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_BLK = "/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_BLK = "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill=INK, align="left", leading=1.15):
    x, y = xy
    for ln in lines:
        w = draw.textlength(ln, font=fnt)
        if align == "center":
            draw.text((x - w / 2, y), ln, font=fnt, fill=fill)
        elif align == "right":
            draw.text((x - w, y), ln, font=fnt, fill=fill)
        else:
            draw.text((x, y), ln, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def rule(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def explosion(draw, cx, cy, r, fill=(232, 120, 30)):
    """Starburst: alternating long/short triangles around a centre."""
    import math
    pts = []
    for i in range(24):
        ang = math.pi * 2 * i / 24
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)
    draw.ellipse([cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45],
                 fill=(250, 200, 60))


def smoke(draw, cx, cy, fill=(120, 120, 118)):
    for dx, dy, r in [(-34, 6, 26), (0, -12, 32), (34, 4, 26), (-8, -30, 24),
                      (22, -26, 20)]:
        draw.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                     fill=fill)


def flame(draw, cx, base_y, w, h):
    """Simple flame: stacked triangles, orange over yellow."""
    draw.polygon([(cx - w, base_y), (cx + w, base_y), (cx, base_y - h)],
                 fill=(232, 110, 20))
    draw.polygon([(cx - w * 0.55, base_y), (cx + w * 0.55, base_y),
                  (cx, base_y - h * 0.62)], fill=(250, 200, 60))


def bridge_scene(draw, x0, y0, x1, y1):
    """Kerch Bridge: sea, deck with a collapsed middle span, smoke, fire."""
    draw.rectangle([x0, y0, x1, y1], fill=(214, 226, 238))  # sky
    draw.rectangle([x0, y0, x1, y0 + 26], fill=(250, 214, 130))  # low sun band
    draw.ellipse([x0 + 26, y0 + 8, x0 + 78, y0 + 60], fill=(250, 190, 80))
    sea_y = y0 + int((y1 - y0) * 0.62)
    draw.rectangle([x0, sea_y, x1, y1], fill=SEA)
    for i in range(5):  # wave lines
        yy = sea_y + 14 + i * 16
        draw.line([(x0 + 12 + i * 30, yy), (x1 - 12 - i * 22, yy)],
                  fill=(120, 170, 205), width=3)
    deck_y = sea_y - 34
    mid = (x0 + x1) // 2
    # pylons
    for px in (x0 + 70, x1 - 70):
        draw.rectangle([px - 7, deck_y - 96, px + 7, deck_y], fill=(70, 70, 72))
        draw.line([(px, deck_y - 96), (max(x0, px - 90), deck_y)],
                  fill=(120, 120, 122), width=2)
        draw.line([(px, deck_y - 96), (min(x1, px + 90), deck_y)],
                  fill=(120, 120, 122), width=2)
    # deck: left and right spans, middle collapsed
    draw.rectangle([x0, deck_y, mid - 58, deck_y + 12], fill=(52, 52, 54))
    draw.rectangle([mid + 58, deck_y, x1, deck_y + 12], fill=(52, 52, 54))
    # fallen span tilted into the sea
    draw.polygon([(mid - 52, deck_y + 4), (mid + 46, deck_y + 30),
                  (mid + 40, deck_y + 44), (mid - 58, deck_y + 18)],
                 fill=(52, 52, 54))
    explosion(draw, mid, deck_y - 6, 46)
    smoke(draw, mid - 8, deck_y - 66)
    smoke(draw, mid + 40, deck_y - 52, fill=(140, 140, 138))


def tanker_scene(draw, x0, y0, x1, y1):
    """Oil tanker on a teal sea, a spiked naval mine, flames."""
    draw.rectangle([x0, y0, x1, y1], fill=(206, 224, 232))
    sea_y = y0 + int((y1 - y0) * 0.58)
    draw.rectangle([x0, sea_y, x1, y1], fill=TEAL)
    for i in range(4):
        yy = sea_y + 12 + i * 15
        draw.line([(x0 + 10 + i * 24, yy), (x1 - 10 - i * 18, yy)],
                  fill=(120, 190, 200), width=3)
    # tanker hull
    hx0, hx1 = x0 + 22, x1 - 60
    hy = sea_y - 8
    draw.polygon([(hx0, hy), (hx1, hy), (hx1 - 18, hy + 34), (hx0 + 6, hy + 34)],
                 fill=(32, 32, 34))
    draw.rectangle([hx0, hy - 6, hx1, hy], fill=RED)  # deck line
    draw.rectangle([hx0 + 18, hy - 44, hx0 + 58, hy - 6], fill=(220, 220, 218))
    draw.rectangle([hx0 + 24, hy - 58, hx0 + 52, hy - 44], fill=(200, 200, 198))
    # mine with spikes, right side
    mx, my = x1 - 42, sea_y + 34
    for ang in range(0, 360, 30):
        import math
        a = math.radians(ang)
        draw.line([(mx + 14 * math.cos(a), my + 14 * math.sin(a)),
                   (mx + 26 * math.cos(a), my + 26 * math.sin(a))],
                  fill=(20, 20, 20), width=4)
    draw.ellipse([mx - 15, my - 15, mx + 15, my + 15], fill=(20, 20, 20))
    flame(draw, (hx0 + hx1) // 2, hy - 4, 26, 52)
    smoke(draw, (hx0 + hx1) // 2, hy - 62)


def flags_scene(draw, x0, y0, x1, y1):
    """Three flags on poles: USA, China, Russia — the Manila / Shenzhen summit."""
    draw.rectangle([x0, y0, x1, y1], fill=(222, 232, 240))
    draw.rectangle([x0, y1 - 26, x1, y1], fill=(120, 140, 120))  # ground
    base_y = y1 - 26
    flags = [
        ("usa", (250, 250, 250)),
        ("chn", (222, 30, 30)),
        ("rus", (250, 250, 250)),
    ]
    fw, fh = 74, 46
    gap = (x1 - x0 - 3 * fw) // 4
    for i, (kind, _) in enumerate(flags):
        fx = x0 + gap + i * (fw + gap)
        fy = y0 + 22
        draw.rectangle([fx - 4, fy, fx, base_y], fill=(90, 90, 90))  # pole
        draw.rectangle([fx, fy, fx + fw, fy + fh], outline=INK, width=2)
        if kind == "usa":
            for s in range(7):
                draw.rectangle([fx, fy + s * 7, fx + fw, fy + s * 7 + 7],
                               fill=(178, 34, 34) if s % 2 == 0
                               else (250, 250, 250))
            draw.rectangle([fx, fy, fx + 30, fy + 24], fill=(30, 50, 110))
            for sx in (6, 16, 26):
                for sy in (5, 13):
                    draw.ellipse([fx + sx - 2, fy + sy - 2, fx + sx + 2,
                                  fy + sy + 2], fill=(250, 250, 250))
        elif kind == "chn":
            draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 30, 30))
            draw.ellipse([fx + 12, fy + 9, fx + 24, fy + 21], fill=(250, 210, 40))
            for sx, sy in [(34, 8), (42, 14), (42, 24), (34, 30)]:
                draw.ellipse([fx + sx - 3, fy + sy - 3, fx + sx + 3,
                              fy + sy + 3], fill=(250, 210, 40))
        else:
            draw.rectangle([fx, fy, fx + fw, fy + 15], fill=(250, 250, 250))
            draw.rectangle([fx, fy + 15, fx + fw, fy + 31], fill=(30, 80, 180))
            draw.rectangle([fx, fy + 31, fx + fw, fy + 46], fill=(200, 30, 30))


def rocket_scene(draw, x0, y0, x1, y1):
    """Vulcan rocket breaking up: dark sky, rocket, debris, satellites."""
    draw.rectangle([x0, y0, x1, y1], fill=(16, 24, 48))
    for sx, sy in [(14, 14), (60, 30), (150, 10), (210, 40), (30, 70),
                   (250, 22), (120, 52), (190, 66)]:
        draw.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3],
                     fill=(240, 240, 220))
    cx = (x0 + x1) // 2
    # rocket body, tilted, breaking apart
    draw.polygon([(cx - 16, y0 + 96), (cx + 16, y0 + 96), (cx + 8, y0 + 30),
                  (cx - 8, y0 + 30)], fill=(235, 235, 230))
    draw.polygon([(cx - 8, y0 + 30), (cx + 8, y0 + 30), (cx, y0 + 8)],
                 fill=(200, 40, 40))
    draw.rectangle([cx - 16, y0 + 62, cx + 16, y0 + 74], fill=(30, 90, 160))
    # detached booster falling away
    draw.polygon([(cx + 52, y0 + 118), (cx + 66, y0 + 118), (cx + 62, y0 + 76),
                  (cx + 56, y0 + 76)], fill=(180, 180, 175))
    explosion(draw, cx, y0 + 108, 30)
    flame(draw, cx, y0 + 100, 12, 26)
    # debris + lost satellites
    for dx, dy, r in [(x0 + 26, y0 + 130, 4), (x1 - 34, y0 + 120, 5),
                      (x0 + 60, y1 - 30, 4), (x1 - 70, y1 - 22, 3)]:
        draw.ellipse([dx - r, dy - r, dx + r, dy + r], fill=(250, 200, 60))
    for sx, sy in [(x0 + 24, y1 - 52), (x1 - 62, y1 - 58)]:
        draw.rectangle([sx, sy, sx + 22, sy + 12], fill=(200, 200, 195),
                       outline=(120, 120, 120))
        draw.rectangle([sx - 12, sy + 2, sx, sy + 10], fill=(40, 90, 180))
        draw.rectangle([sx + 22, sy + 2, sx + 34, sy + 10], fill=(40, 90, 180))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24  # margin
    X0, X1 = M, W - M

    # ---- masthead ----
    d.rectangle([X0, M, X1, 118], fill=INK)
    d.text(((X0 + X1) // 2, 30), "THE WORLD IN ONE DAY",
           font=font(SERIF_BLK, 58), fill=(250, 248, 240), anchor="ma")
    d.text(((X0 + X1) // 2, 92), "ONE IMAGE  •  EVERY STORY THAT MATTERED",
           font=font(SANS_B, 17), fill=(200, 160, 60), anchor="ma")
    rule(d, X0, X1, 128, fill=RED, width=5)

    # ---- dateline ----
    d.text((X0, 138), "TUESDAY, 17 NOVEMBER 2026",
           font=font(SANS_BLK, 26), fill=INK)
    d.text((X1, 138), "WORLD NEWS",
           font=font(SANS_B, 26), fill=RED, anchor="ra")
    rule(d, X0, X1, 172, width=2)

    # ---- lead story: Kerch Bridge ----
    ly0, ly1 = 184, 512
    d.rectangle([X0, ly0, X1, ly1], outline=INK, width=3)
    bridge_scene(d, X0 + 3, ly0 + 3, X1 - 3, ly0 + 208)
    hy = ly0 + 214
    for ln in wrap(d, "UKRAINE STRIKES KERCH BRIDGE AGAIN",
                   font(SERIF_BLK, 40), X1 - X0 - 28):
        d.text((X0 + 14, hy), ln, font=font(SERIF_BLK, 40), fill=INK)
        hy += 48
    d.text((X0 + 14, ly0 + 266),
           "Road span collapses in second attack in under 24 hours",
           font=font(SANS_R, 23), fill=(60, 60, 60))
    d.text((X0 + 14, ly0 + 294),
           "Kyiv hits the link to occupied Crimea as Russian strikes damage bridges in Kyiv.",
           font=font(SANS_R, 20), fill=(60, 60, 60))

    # ---- three panels ----
    py0, py1 = 528, 852
    pw = (X1 - X0 - 2 * 16) // 3
    panels = [
        ("TANKERS HIT BY MINES OFF HORMUZ",
         "Two vessels ablaze in the Strait; a third US carrier arrives.",
         tanker_scene),
        ("TRUMP LANDS IN MANILA",
         "ASEAN summit opens; Xi–Trump–Putin talks set for Thursday.",
         flags_scene),
        ("VULCAN ROCKET FAILS",
         "40 Amazon internet satellites destroyed after launch.",
         rocket_scene),
    ]
    for i, (head, sub, scene) in enumerate(panels):
        px0 = X0 + i * (pw + 16)
        px1 = px0 + pw
        d.rectangle([px0, py0, px1, py1], outline=INK, width=3)
        scene(d, px0 + 3, py0 + 3, px1 - 3, py0 + 158)
        y = py0 + 168
        for ln in wrap(d, head, font(SERIF_B, 27), px1 - px0 - 20):
            d.text((px0 + 10, y), ln, font=font(SERIF_B, 27), fill=INK)
            y += 32
        for ln in wrap(d, sub, font(SANS_R, 19), px1 - px0 - 20):
            d.text((px0 + 10, y), ln, font=font(SANS_R, 19), fill=(60, 60, 60))
            y += 24

    # ---- ticker: also today ----
    ty0, ty1 = 868, 946
    d.rectangle([X0, ty0, X1, ty1], fill=(232, 226, 210), outline=INK, width=2)
    d.text((X0 + 12, ty0 + 6), "ALSO TODAY",
           font=font(SANS_BLK, 20), fill=RED)
    ticker = ("JPMorgan blames a software bug for Monday's banking outage  •  "
              "Nvidia reports first earnings since Jensen Huang's exit  •  "
              "Estonia to shut Russia border crossings on 1 December")
    y = ty0 + 30
    for ln in wrap(d, ticker, font(SANS_R, 18), X1 - X0 - 24):
        d.text((X0 + 12, y), ln, font=font(SANS_R, 18), fill=INK)
        y += 22

    # ---- footer ----
    rule(d, X0, X1, 962, fill=RED, width=3)
    d.text(((X0 + X1) // 2, 972), "17 NOVEMBER 2026  •  THE DAY IN ONE IMAGE",
           font=font(SANS_B, 18), fill=INK, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "assets", "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
