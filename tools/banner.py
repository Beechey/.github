"""Draws the README header (light + dark). Figure echoes the portfolio's Figure 1:
two classes, a decision boundary, and a band where an evidential classifier declines."""
# Regenerate: python3 tools/banner.py profile/assets
import random, math, sys

W, H = 1200, 400
FX, FY, FW, FH = 770, 56, 370, 262  # figure box

def points():
    rng = random.Random(7)  # seeded so the figure never reshuffles
    pts = []
    for cls, (cx, cy) in ((0, (0.28, 0.68)), (1, (0.72, 0.32))):
        for _ in range(34):
            x = min(max(rng.gauss(cx, 0.17), 0.04), 0.96)
            y = min(max(rng.gauss(cy, 0.17), 0.04), 0.96)
            pts.append((x, y, cls))
    return pts

def dist(x, y):  # signed distance to boundary y = x (unit square)
    return (x - y) / math.sqrt(2)

BAND = 0.11

def svg(t):
    P = lambda x, y: (FX + x * FW, FY + (1 - y) * FH)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Dr Matt Beechey. Lead AI Engineer. Machine learning, evidence theory, and systems that survive the real world.">',
           f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>',
           '<defs>'
           f'<pattern id="h" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="{t["accent"]}" stroke-width="1.2" opacity=".55"/></pattern>'
           f'<clipPath id="c"><rect x="{FX}" y="{FY}" width="{FW}" height="{FH}"/></clipPath>'
           '</defs>']
    serif = "Iowan Old Style, Palatino Linotype, Palatino, Georgia, serif"
    mono = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    # left: type
    out += [
        f'<text x="64" y="104" font-family="{mono}" font-size="15" letter-spacing="3" fill="{t["accent"]}">§ README — LOUGHBOROUGH, UK</text>',
        f'<text x="60" y="186" font-family="{serif}" font-size="72" fill="{t["ink"]}">Dr Matt Beechey</text>',
        f'<text x="64" y="232" font-family="{serif}" font-style="italic" font-size="26" fill="{t["muted"]}">Lead AI Engineer at TransHumanity.</text>',
        f'<line x1="64" y1="268" x2="664" y2="268" stroke="{t["rule"]}"/>',
        f'<text x="64" y="304" font-family="{serif}" font-size="21" fill="{t["ink"]}">I build machine learning systems that have to survive</text>',
        f'<text x="64" y="334" font-family="{serif}" font-size="21" fill="{t["ink"]}">contact with the real world, and say when they don’t know.</text>',
    ]
    # right: figure
    (bx0, by0), (bx1, by1) = P(0, 0), P(1, 1)
    off = BAND * math.sqrt(2)
    band = [P(0, -off), P(1, 1 - off), P(1, 1 + off), P(0, off)]
    out.append(f'<g clip-path="url(#c)"><polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in band)}" fill="url(#h)"/>'
               f'<line x1="{bx0}" y1="{by0}" x2="{bx1}" y2="{by1}" stroke="{t["ink"]}" stroke-width="1.2" stroke-dasharray="5 4"/></g>')
    out.append(f'<rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" fill="none" stroke="{t["rule"]}"/>')
    for x, y, cls in points():
        px, py = P(x, y)
        if abs(dist(x, y)) < BAND:
            out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.6" fill="none" stroke="{t["accent"]}" stroke-width="1.6"/>')
        elif cls == 0:
            out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="{t["ink"]}"/>')
        else:
            out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="{t["blue"]}"/>')
    out.append(f'<text x="{FX}" y="{FY + FH + 30}" font-family="{mono}" font-size="13" fill="{t["muted"]}"><tspan fill="{t["accent"]}">FIG. 1</tspan>  Declines rather than guesses.</text>')
    out.append('</svg>')
    return "\n".join(out)

THEMES = {
    "light": dict(bg="#F7F4ED", ink="#191713", muted="#6B645A", rule="#D9D2C3", accent="#BF3B21", blue="#2B4C7E"),
    "dark":  dict(bg="#151412", ink="#EFEAE0", muted="#A39B8E", rule="#3A362F", accent="#E2603F", blue="#7FA3D9"),
}
if __name__ == "__main__":
    outdir = sys.argv[1]
    for name, t in THEMES.items():
        open(f"{outdir}/header-{name}.svg", "w").write(svg(t))
    # self-check: some points land in the band, and both classes appear outside it
    pts = points()
    assert any(abs(dist(x, y)) < BAND for x, y, _ in pts)
    assert {c for x, y, c in pts if abs(dist(x, y)) >= BAND} == {0, 1}
