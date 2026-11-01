"""Draws the README header (light + dark variants, transparent background).
Regenerate: python3 tools/banner.py profile/assets"""
import random, sys

W, H = 1200, 300

def field():
    """Dot grid that fades in towards the right edge, with a few accent dots."""
    rng = random.Random(7)  # seeded so the pattern never reshuffles
    dots = []
    for gx in range(30):
        for gy in range(10):
            x, y = 640 + gx * 19 + 9, 30 + gy * 26 + (13 if gx % 2 else 0)
            t = (x - 640) / 560  # 0 at the left of the field, 1 at the right edge
            if rng.random() > t * 1.15:
                continue
            dots.append((x, y, round(0.15 + 0.6 * t, 2), rng.random() < 0.05))
    return dots

def svg(t):
    serif = "Iowan Old Style, Palatino Linotype, Palatino, Georgia, serif"
    mono = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Matt Beechey">']
    for x, y, a, hot in field():
        if hot:
            out.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{t["accent"]}"/>')
        else:
            out.append(f'<circle cx="{x}" cy="{y}" r="2.2" fill="{t["ink"]}" opacity="{a}"/>')
    out += [
        f'<text x="4" y="112" font-family="{mono}" font-size="15" letter-spacing="4" fill="{t["accent"]}">HELLO, I’M</text>',
        f'<text x="0" y="196" font-family="{serif}" font-size="96" fill="{t["ink"]}">Matt Beechey</text>',
        f'<rect x="4" y="226" width="44" height="3" fill="{t["accent"]}"/>',
        f'<text x="64" y="232" font-family="{serif}" font-style="italic" font-size="24" fill="{t["muted"]}">Engineer, researcher, builder of things.</text>',
        '</svg>',
    ]
    return "\n".join(out)

THEMES = {
    "light": dict(ink="#1F2328", muted="#59636E", accent="#BF3B21"),
    "dark":  dict(ink="#F0F6FC", muted="#9198A1", accent="#E2603F"),
}
if __name__ == "__main__":
    for name, t in THEMES.items():
        open(f"{sys.argv[1]}/banner-{name}.svg", "w").write(svg(t))
    # self-check: the field has dots, fades in (denser on the right), and has a few accents
    d = field()
    assert sum(x > 920 for x, *_ in d) > sum(x <= 920 for x, *_ in d)
    assert any(h for *_, h in d)
