"""Builds the one-page profile: python3 tools/brochure.py, then node tools/brochure.js"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("b", os.path.join(ROOT, "tools", "build.py"))
b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
A = "file://" + ROOT + "/assets/"

def tally(name):
    return "".join(f'<span class="ch{" hi" if l in ("Grand", "Gold") else ""}"><b>{n}</b> {l}{" Award" if l == "Grand" else ""}</span>' for l, n in b.award_tally(name))

services = [("Annual and integrated reports", "One consistent narrative across all operational, financial and other disclosures."),
            ("Sustainability reports", "Aligned with ESG ratings, disclosure rules, GRI, SASB, the UN SDGs and IFRS S1 and S2."),
            ("Governance reports", "Aligned with local listing rules as well as regional and international best practice."),
            ("Investor communications", "Presentations, equity story and FAQs with a consistent message to the market."),
            ("Leadership messaging and profiles", "Statements and key messages for the C-suite, plus company profiles."),
            ("Analysis and advisory", "Messaging proposals, gap analyses, peer reviews and materiality assessments.")]
exch = "".join(f'<img src="{A}exchanges/{b.EXCHANGES[k][2]}">' for k in b.GCC + ["moex"])
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Lora;src:url({A}fonts/lora.woff)}}
@font-face{{font-family:Lora;font-style:italic;src:url({A}fonts/lora-italic.woff)}}
@font-face{{font-family:Inter;src:url({A}fonts/inter-Regular.woff)}}
@font-face{{font-family:Inter;font-weight:500;src:url({A}fonts/inter-Medium.woff)}}
@page{{size:A4;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:210mm;height:297mm;overflow:hidden;background:#F2EDE3;color:#2B2118;font-family:Inter,sans-serif;font-size:8.4pt;line-height:1.4;display:flex;flex-direction:column}}
.top{{padding:10mm 14mm 6mm;display:grid;grid-template-columns:1fr 60mm;gap:10mm;align-items:end}}
.top img.logo{{width:36mm;margin-bottom:5mm}}
h1{{font-family:Lora;font-weight:400;font-size:18pt;line-height:1.12;margin-bottom:3mm}}
.lede{{color:#6A5540;font-size:9.2pt}}
.figs{{display:grid;grid-template-columns:1fr 1fr;gap:3mm}}
.figs div{{border-top:1.2px solid #2E4A3E;padding-top:2mm}}
.figs b{{display:block;font-family:Lora;font-weight:400;font-size:20pt;line-height:1}}
.figs span{{color:#6A5540;font-size:7.6pt}}
.mid{{background:#FAF7F1;padding:6mm 14mm;display:grid;grid-template-columns:1.25fr 1fr;gap:10mm;border-top:1px solid #E4D9C7;border-bottom:1px solid #E4D9C7}}
h2{{font-family:Lora;font-weight:400;font-size:13pt;margin-bottom:3mm}}
.svc li{{list-style:none;padding:1.5mm 0;border-top:1px solid #E4D9C7}}
.svc li b{{display:block;font-family:Lora;font-weight:500;font-size:9.6pt}}
.svc li span{{color:#6A5540}}
.aw{{background:#F2EDE3;border:1px solid #E4D9C7;border-radius:3mm;padding:3mm;margin-bottom:2.5mm}}
.aw img{{height:8mm;margin-bottom:2mm}}
.ch{{display:inline-block;padding:1.2mm 2.6mm;border-radius:2mm;background:#FAF7F1;border:1px solid #E4D9C7;margin:0 1.2mm 1.2mm 0;font-size:7.8pt}}
.ch b{{font-family:Lora;font-weight:400;font-size:11pt}}
.ch.hi{{background:#2E4A3E;border-color:#2E4A3E;color:#FAF7F1}}
.cred{{display:flex;gap:3mm;align-items:center;padding:1.4mm 0;border-top:1px solid #E4D9C7}}
.cred img{{width:9mm;height:8mm;object-fit:contain}}
.cred b{{font-weight:500;display:block}}
.cred span{{color:#6A5540;font-size:7.6pt}}
.about{{padding:6mm 14mm 5mm;display:grid;grid-template-columns:26mm 1fr;gap:7mm;align-items:start}}
.about img{{width:26mm;height:32.5mm;object-fit:cover;border-radius:2.5mm}}
.about p{{color:#3d3127;margin-bottom:2mm}}
.ex{{padding:0 14mm 5mm}}.ex p{{margin:0 0 2.5mm;font-family:Lora;font-size:11pt;color:var(--espresso,#2B2118)}}.exrow{{display:flex;align-items:center;justify-content:space-between;gap:4mm}}
.ex img{{height:8mm;max-width:24mm;object-fit:contain}}
.foot{{margin-top:auto;background:#2E4A3E;color:#FAF7F1;padding:6mm 14mm;display:flex;justify-content:space-between;align-items:center}}
.foot img{{height:12mm}}
.foot div{{text-align:right;font-size:8.4pt;line-height:1.6}}
.foot a{{color:#FAF7F1;text-decoration:none}}
</style></head><body>
<div class="top"><div><img class="logo" src="{A}logo.svg"><h1>Content development and advisory for corporate communications</h1>
<p class="lede">Frisson Writing helps shape how listed companies across the Gulf present themselves to investors and stakeholders, developing the narrative and key messages behind reports, investor presentations and leadership communications.</p></div>
<div class="figs"><div><b>{b.N}</b><span>Investor-facing reports</span></div><div><b>{b.N_LISTED}</b><span>Listed companies</span></div><div><b>{len(b.EXCHANGES)}</b><span>Exchanges</span></div><div><b>{len(b.INDUSTRIES)}</b><span>Sectors</span></div></div></div>
<div class="mid"><div><h2>Services</h2><ul class="svc">{"".join(f"<li><b>{t}</b><span>{d}</span></li>" for t, d in services)}</ul></div>
<div><h2>Project recognitions</h2>
<div class="aw"><img src="{A}badges/arc.png"><div>{tally("ARC Awards")}</div></div>
<div class="aw"><img src="{A}badges/cfawards.png"><div>{tally("Corporate & Financial")}</div></div>
<h2 style="margin-top:3mm">Expertise</h2>
<div class="cred"><img src="{A}badges/cfa.svg"><div><b>Certificate in Sustainable Investing</b><span>CFA Institute</span></div></div>
<div class="cred"><img src="{A}badges/fmva.svg"><div><b>Financial Modelling and Valuation Analyst</b><span>Corporate Finance Institute</span></div></div>
<div class="cred"><img src="{A}badges/arc.png"><div><b>Awards judge</b><span>ARC Awards and MEIRA Reporting Awards 2025</span></div></div></div></div>
<div class="about"><img src="{A}founder.jpg"><div><h2>About us</h2>
<p>Mikhail Seleznev founded Frisson Writing in 2026 after six years at a leading corporate reporting agency in London and Dubai. He has led content development on more than 30 reports for listed and pre-IPO companies, working closely with investor relations and communication teams.</p>
<p>He has interviewed more than 40 board members and senior executives, speaks at MEIRA conferences and holds a BA in History from Durham University, UK.</p></div></div>
<div class="ex"><p>Experience with companies listed on</p><div class="exrow">{exch}</div></div>
<div class="foot"><img src="{A}logo-light.svg"><div><a href="mailto:{b.EMAIL}">{b.EMAIL}</a><br><a href="https://frissonwriting.com">frissonwriting.com</a> &nbsp;·&nbsp; <a href="{b.LINKEDIN}">LinkedIn</a><br>Dubai, United Arab Emirates</div></div>
</body></html>"""
open(os.path.join(ROOT, "tools", "brochure.html"), "w").write(html)
