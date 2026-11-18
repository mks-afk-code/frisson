"""Builds the Frisson Writing logo files as outlined SVG (no font needed to display them)."""
import math, sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

G = "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf"
I = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"

def text_path(font, text, size, x0, y0, track=0.0):
    gs = font.getGlyphSet(); cmap = font.getBestCmap(); upm = font["head"].unitsPerEm
    s = size / upm; x = x0; out = []
    for ch in text:
        g = cmap[ord(ch)]; pen = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}")
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x, y0)))
        out.append(pen.getCommands()); x += gs[g].width * s + track
    return " ".join(out), x - track - x0

def tremor(x0, x1, y, amp=5.0, waves=3.5, n=160):
    """A hairline that shivers once in the middle: the frisson."""
    c = (x0 + x1) / 2; w = (x1 - x0) * 0.16; pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n; d = (x - c) / w
        pts.append((x, y - amp * math.exp(-d * d) * math.sin(d * waves * 1.6)))
    return "M" + " L".join(f"{x:.2f} {yy:.2f}" for x, yy in pts)

def build(out):
    lora = instantiateVariableFont(TTFont(G), {"wght": 500}); inter = TTFont(I)
    f, fw = text_path(lora, "Frisson", 96, 0, 0)
    w, ww = text_path(inter, "WRITING", 27, 0, 0, track=7)
    W = fw + 24; ox = 12
    f, _ = text_path(lora, "Frisson", 96, ox, 92)
    w, _ = text_path(inter, "WRITING", 27, ox + (fw - ww) / 2, 162, track=7)
    line = tremor(ox, ox + fw, 120)
    for name, ink in (("logo", "#2B2118"), ("logo-light", "#F1EADD")):
        open(f"{out}/{name}.svg", "w").write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} 174" role="img" aria-label="Frisson Writing">'
            f'<path d="{f}" fill="{ink}"/><path d="{line}" fill="none" stroke="{ink}" stroke-width="1.6" stroke-linecap="round"/>'
            f'<path d="{w}" fill="{ink}"/></svg>')
    fp, fwid = text_path(lora, "F", 46, 0, 0)
    fp, _ = text_path(lora, "F", 46, (64 - fwid) / 2 + 1, 42)
    open(f"{out}/favicon.svg", "w").write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#2B2118"/>'
        f'<path d="{fp}" fill="#F1EADD"/><path d="{tremor(12, 52, 52, amp=3.2)}" fill="none" stroke="#D2C0A2" stroke-width="1.8" stroke-linecap="round"/></svg>')
    print(tremor(0, 600, 12, amp=9))

if __name__ == "__main__":
    build(sys.argv[1])
