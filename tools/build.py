"""Builds the Frisson Writing site. Run from the repo root:  python3 tools/build.py

Edit the text and the PROJECTS list below, then run this to regenerate the HTML pages.
To add a real cover, save it as assets/covers/<slug>.jpg (or .png / .webp) and rebuild.
To add a link, fill in the "link" field of the project.
"""
import html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from logo import tremor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL = "mikhail@frissonwriting.com"
SITE = "Frisson Writing"

AR, SR, CP = "Annual Report", "Sustainability Report", "Company Profile"
LEAD, EDIT = "Content development and consultancy", "Copyediting"
# (slug, company, kind, year, exchange, role, link)
PROJECTS = [
    ("luberef-ar25", "Luberef", AR, "2025", "Saudi Exchange", LEAD, ""),
    ("dtc-ar25", "Dubai Taxi Company", AR, "2025", "DFM", LEAD, ""),
    ("burjeel-ar25", "Burjeel Holdings", AR, "2025", "ADX", LEAD, ""),
    ("jamjoom-ar25", "Jamjoom Pharma", AR, "2025", "Saudi Exchange", LEAD, ""),
    ("oqep-ar25", "OQEP", AR, "2025", "MSX", LEAD, ""),
    ("gig-ar25", "Gulf Insurance Group", AR, "2025", "Boursa Kuwait", LEAD, ""),
    ("sadafco-ar25", "SADAFCO", AR, "2025", "Saudi Exchange", LEAD, ""),
    ("milaha-ar25", "Qatar Navigation", AR, "2025", "Qatar Exchange", LEAD, ""),
    ("luberef-sr24", "Luberef", SR, "2024", "Saudi Exchange", LEAD, ""),
    ("maharah-sr24", "Maharah", SR, "2024", "Saudi Exchange", LEAD, ""),
    ("emsteel-ar25", "EMSTEEL", AR, "2025", "ADX", EDIT, ""),
    ("gulfnav-ar25", "Gulf Navigation Holding", AR, "2025", "DFM", EDIT, ""),
    ("gig-profile", "Gulf Insurance Group", CP, "", "Boursa Kuwait", "Content development", ""),
    ("dtc-ar24", "Dubai Taxi Company", AR, "2024", "DFM", LEAD, ""),
    ("burjeel-ar24", "Burjeel Holdings", AR, "2024", "ADX", LEAD, ""),
    ("gig-ar24", "Gulf Insurance Group", AR, "2024", "Boursa Kuwait", LEAD, ""),
    ("fixprice-ar24", "Fix Price", AR, "2024", "MOEX and AIX", LEAD, ""),
    ("gulfnav-ar24", "Gulf Navigation Holding", AR, "2024", "DFM", EDIT, ""),
    ("emsteel-ar24", "EMSTEEL", AR, "2024", "ADX", EDIT, ""),
    ("luberef-sr23", "Luberef", SR, "2023", "Saudi Exchange", LEAD, ""),
    ("eurochem-ar23", "EuroChem", AR, "2023", "", "Content development", ""),
    ("phosagro-ar23", "PhosAgro", AR, "2023", "", "Content development", ""),
]
AGENCY_LINE = "Delivered while at Fanda."
TONES = [("#D2C0A2", ""), ("#E6DBC8", ""), ("#6A5540", "t-dark"), ("#C3AD8B", ""), ("#2B2118", "t-dark"), ("#DCCDB4", ""), ("#A88C66", "t-dark")]

e = html.escape
NAV = [("services.html", "Services"), ("work.html", "Work"), ("approach.html", "Approach"), ("founder.html", "Founder"), ("contact.html", "Contact")]


def line(cls=""):
    return (f'<svg class="tremor {cls}" viewBox="0 0 600 24" preserveAspectRatio="none" aria-hidden="true">'
            f'<path pathLength="1" d="{tremor(0, 600, 12, amp=9)}"/></svg>')


def cover(p, i, shelf=False):
    slug, company, kind, year = p[0], p[1], p[2], p[3]
    for ext in ("jpg", "jpeg", "png", "webp"):
        if os.path.exists(f"{ROOT}/assets/covers/{slug}.{ext}"):
            return (f'<div class="cover photo"><img src="assets/covers/{slug}.{ext}" loading="lazy" '
                    f'alt="Cover of the {e(company)} {e(kind)} {year}"></div>')
    c, t = TONES[i % len(TONES)]
    return (f'<div class="cover {t}" style="--c:{c}"><div><div class="c-name">{e(company)}</div>'
            f'<div class="c-kind">{e(kind)}</div></div><div class="c-year">{year or "Profile"}</div></div>')


def card(p, i):
    slug, company, kind, year, exch, role, link = p
    title = f"{kind} {year}".strip()
    cv = cover(p, i)
    if link:
        cv = f'<a class="cover-link" href="{e(link)}" target="_blank" rel="noopener" aria-label="{e(company)} {e(title)}, opens the company page">{cv}</a>'
    tag = "annual" if kind == AR else "sustainability" if kind == SR else "other"
    out = f'<article data-kind="{tag}">{cv}<div class="meta"><h3>{e(company)}</h3><p>{e(title)}'
    out += f'<br>{e(exch)}</p>' if exch else '</p>'
    out += f'<p class="role">{e(role)}. {AGENCY_LINE}</p>'
    if link:
        out += f'<a href="{e(link)}" target="_blank" rel="noopener">View the report</a>'
    return out + '</div></article>'


def page(fname, title, desc, body):
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == fname else ""}>{t}</a>' for h, t in NAV)
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/lora.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<header class="site-head"><div class="wrap">
<a class="brand" href="index.html" aria-label="Frisson Writing, home"><span class="brand-f">Frisson</span><span class="brand-w">Writing</span></a>
<nav class="nav" aria-label="Main">{nav}</nav>
</div></header>
<main>
{body}
</main>
<footer class="site-foot"><div class="wrap">
<img src="assets/logo-light.svg" alt="Frisson Writing" width="170" height="54">
<span>Frisson Writing LLC. Licensed by Shams Free Zone, Sharjah, UAE. Based in Dubai.</span>
<a href="mailto:{EMAIL}">{EMAIL}</a>
</div></footer>
</body>
</html>
"""
    open(f"{ROOT}/{fname}", "w").write(doc)


def cta(heading="Planning a report?", text="Tell Frisson Writing about the report, the timeline and where the content stands today."):
    return f"""<section class="band dark"><div class="wrap">
<h2>{heading}</h2>
<p class="lede" style="margin-top:18px">{text}</p>
<div class="actions"><a class="btn" href="mailto:{EMAIL}">Email {EMAIL}</a></div>
</div></section>"""


FIGURES = """<div class="figures">
<div><b>25+</b><span>annual and sustainability reports</span></div>
<div><b>15+</b><span>C-level interviews conducted</span></div>
<div><b>6</b><span>Gulf exchanges covered</span></div>
<div><b>5</b><span>years in corporate reporting</span></div>
</div>"""

STAGES = [
    ("Consultancy", "Advice on report changes, framework selection and content gaps, with one content owner on every client call."),
    ("Analytics", "Peer reviews and gap analyses that show where current reporting stands against requirements and competitors."),
    ("Theme", "A narrative theme that gives the report its identity and guides the visual design."),
    ("Structure", "A full report structure with content flow, pagination and section-by-section information mapping."),
    ("Data gathering", "Bespoke data collection forms and interviews with management."),
    ("Drafting", "Every report section written in line with the confirmed structure."),
    ("Revisions", "The draft refined in rounds, based on client feedback."),
    ("Designer support", "Help for designers in applying client comments, plus advice on photography that fits the narrative."),
]

# ---------------------------------------------------------------- Home
shelf = "".join(cover(p, i, True) for i, p in enumerate(PROJECTS[:7]))
selected = "".join(card(p, i) for i, p in enumerate(PROJECTS[:4]))
home = f"""<section class="hero"><div class="wrap">
<h1>The writing behind annual, sustainability and integrated reports.</h1>
<p class="lede">Frisson Writing plans, writes and edits investor disclosures for listed companies across the Gulf.</p>
<div class="actions"><a class="btn solid" href="work.html">See the reports</a><a class="btn" href="contact.html">Start a conversation</a></div>
<div class="shelf"><div class="shelf-row">{shelf}</div>{line("draw")}</div>
</div></section>

<section class="band"><div class="wrap">
<p class="statement">More than 25 reports for companies listed on the Saudi Exchange, DFM, ADX, Boursa Kuwait, MSX and Qatar Exchange.</p>
{FIGURES}
</div></section>

<section class="band oat"><div class="wrap">
<div class="head-row"><h2>Reports first, and the documents around them.</h2><a class="text-link" href="services.html">All services</a></div>
<div class="cols">
<div><h3>Reports</h3><ul><li>Annual reports</li><li>Sustainability reports</li><li>Integrated reports</li><li>Governance reports</li></ul></div>
<div><h3>Consulting</h3><ul><li>Gap analysis</li><li>Peer review and benchmarking</li><li>Materiality assessments</li></ul></div>
<div><h3>On request</h3><ul><li>Investor presentations</li><li>Corporate profiles</li><li>Leadership statements</li></ul></div>
</div>
</div></section>

<section class="band"><div class="wrap">
<div class="head-row"><h2>Selected work</h2><a class="text-link" href="work.html">All {len(PROJECTS)} projects</a></div>
<div class="work">{selected}</div>
</div></section>

<section class="band dark"><div class="wrap">
<div class="head-row"><h2>One writer from the first call to the final proof.</h2><a class="text-link" href="approach.html">How a project runs</a></div>
<ol class="stage-line">{"".join(f"<li>{s}</li>" for s, _ in STAGES)}</ol>
</div></section>

<section class="band"><div class="wrap split">
<div class="portrait">{'<img src="assets/founder.jpg" alt="Mikhail Seleznev">' if os.path.exists(ROOT + "/assets/founder.jpg") else '<span>MS</span>'}</div>
<div class="prose">
<p class="kicker" style="margin-bottom:14px">Founder</p>
<h2 style="margin-bottom:24px">Mikhail Seleznev</h2>
<p>A report writer and consultant with five years on Gulf annual and sustainability reports, and a judge at the MEIRA Reporting Awards 2025 and the ARC Awards 2026.</p>
<div class="actions"><a class="btn" href="founder.html">About the founder</a></div>
</div>
</div></section>
{cta()}"""
page("index.html", "Frisson Writing | Annual, sustainability and integrated report writing",
     "Frisson Writing is a Dubai consultancy that plans, writes and edits annual, sustainability, integrated and governance reports for listed companies across the Gulf.", home)

# ---------------------------------------------------------------- Services
services = f"""<section class="page-hero"><div class="wrap">
<h1>Content and consultancy for investor disclosures.</h1>
<p class="lede">Reports are the main work. Presentations, profiles and analysis sit around them.</p>
</div><div class="wrap">{line("soft")}</div></section>

<section class="band tight"><div class="wrap">
<div class="cols">
<div><h3>Reports</h3><ul>
<li>Annual reports</li><li>Sustainability reports</li><li>Integrated reports</li>
<li>Governance reports<small>Copyediting or full copywriting.</small></li></ul></div>
<div><h3>Consulting</h3><ul>
<li>Gap analysis<small>A review of the latest report against GRI, SASB, local exchange and IFRS S1 and S2 requirements.</small></li>
<li>Peer review and benchmarking<small>Local and international peers compared across more than 20 data points.</small></li>
<li>Materiality assessments</li></ul></div>
<div><h3>On request</h3><ul>
<li>Investor presentations</li><li>Corporate profiles</li>
<li>Leadership statements<small>Chairman, CEO and CFO statements drafted from interviews.</small></li></ul></div>
</div>
</div></section>

<section class="band oat" id="competencies"><div class="wrap">
<div class="head-row"><h2>Competencies</h2></div>
<div class="comp">
<div><h3>Investor communication</h3><p>Performance narratives and investment cases built from financial and non-financial data, peer benchmarking and market research.</p></div>
<div><h3>Stakeholder engagement</h3><p>Direct interviews with C-suite executives and Board members, and engagement for materiality assessments.</p></div>
<div><h3>Financial competency</h3><p>Financial reviews written from quarterly results and earnings calls, checked against sell-side research.</p></div>
<div><h3>Corporate reporting and copywriting</h3><p>Annual and sustainability reports led from consultancy and content through to final production.</p></div>
<div><h3>Sustainability and compliance</h3><p>Sustainability frameworks, integrated thinking and the six capitals, and listing rules across GCC markets.</p></div>
<div><h3>Public speaking</h3><p>Workshops and panels at industry events in the GCC, including MEIRA conferences and chapter meetings.</p></div>
</div>
<ul class="chips" aria-label="Frameworks and standards"><li>GRI</li><li>SASB</li><li>UN SDGs</li><li>IFRS S1</li><li>IFRS S2</li><li>Integrated reporting</li><li>UAE, KSA, Oman and Qatar listing rules</li></ul>
</div></section>
{cta()}"""
page("services.html", "Services | Frisson Writing",
     "Annual, sustainability, integrated and governance reports, with gap analysis, peer benchmarking, materiality assessments, investor presentations and corporate profiles.", services)

# ---------------------------------------------------------------- Work
cards = "".join(card(p, i) for i, p in enumerate(PROJECTS))
work = f"""<section class="page-hero"><div class="wrap">
<h1>Reports the founder has written and edited.</h1>
<p class="lede">Each entry names the company, the report and the role.</p>
</div><div class="wrap">{line("soft")}</div></section>

<section class="band tight"><div class="wrap">
<div class="filters" role="group" aria-label="Filter projects">
<button type="button" data-f="all" aria-pressed="true">All</button>
<button type="button" data-f="annual" aria-pressed="false">Annual reports</button>
<button type="button" data-f="sustainability" aria-pressed="false">Sustainability reports</button>
<button type="button" data-f="other" aria-pressed="false">Other</button>
</div>
<div class="work" id="work">{cards}</div>
<p class="note">Each report was published by the company named and belongs to it. Mikhail Seleznev worked on these projects in the role stated during his time at Fanda, before founding Frisson Writing.</p>
</div></section>
<script>
document.querySelectorAll('.filters button').forEach(function (b) {{
  b.addEventListener('click', function () {{
    document.querySelectorAll('.filters button').forEach(function (x) {{ x.setAttribute('aria-pressed', x === b); }});
    document.querySelectorAll('#work article').forEach(function (a) {{ a.hidden = b.dataset.f !== 'all' && a.dataset.kind !== b.dataset.f; }});
  }});
}});
</script>
{cta()}"""
page("work.html", "Work | Frisson Writing",
     "Annual and sustainability reports for companies listed on the Saudi Exchange, DFM, ADX, Boursa Kuwait, MSX and Qatar Exchange.", work)

# ---------------------------------------------------------------- Approach
approach = f"""<section class="page-hero"><div class="wrap">
<h1>Involved at every stage of the report.</h1>
<p class="lede">Frisson Writing owns the content from the first advisory call until the designers close the file.</p>
</div><div class="wrap">{line("soft")}</div></section>

<section class="band tight"><div class="wrap">
<ol class="stages">{"".join(f"<li><h3>{s}</h3><p>{d}</p></li>" for s, d in STAGES)}</ol>
</div></section>

<section class="band oat"><div class="wrap">
<div class="head-row"><h2>Three levels of involvement</h2></div>
<div class="cols">
<div><h3>Ground-up</h3><p>First-time and post-IPO reports, full structural rebuilds and bespoke formats.</p></div>
<div><h3>Update and uplift</h3><p>Reports in sound structural shape that need meaningful content updates, fresh copy and general refinement.</p></div>
<div><h3>Light-touch</h3><p>Review, copyediting and refinement of client content, with structural and disclosure suggestions.</p></div>
</div>
</div></section>

<section class="band"><div class="wrap">
<div class="head-row"><h2>When the deadline is tight</h2></div>
<div class="cases">
<div><b>9</b><em>working days</em><p>A complete structural rewrite of an annual report for one of the largest MSX-listed companies, from kick-off to full written draft.</p></div>
<div><b>11</b><em>working days</em><p>An annual report for a Saudi Exchange-listed pharmaceutical company, taken over mid-project and carried to final draft.</p></div>
<div><b>96</b><em>hours</em><p>Chairman and CEO statements for an MSX-listed energy company, drafted within 48 hours of the interview and confirmed within 96 hours of client feedback.</p></div>
</div>
</div></section>

<section class="band dark"><div class="wrap">
<div class="cols">
<div style="border-color:var(--bark)"><h3>Any working format</h3><p style="color:var(--sand)">Proprietary platforms, Microsoft Teams or the tools the client prefers.</p></div>
<div style="border-color:var(--bark)"><h3>On site when needed</h3><p style="color:var(--sand)">Based in Dubai, with in-person interviews and meetings in the UAE and across the region.</p></div>
<div style="border-color:var(--bark)"><h3>Confidential</h3><p style="color:var(--sand)">Client materials, data and report content stay confidential, under the client's NDA or a tailored one.</p></div>
</div>
<div class="actions"><a class="btn" href="mailto:{EMAIL}">Email {EMAIL}</a></div>
</div></section>"""
page("approach.html", "Approach | Frisson Writing",
     "How Frisson Writing runs a report: consultancy, analytics, theme, structure, data gathering, drafting, revisions and designer support.", approach)

# ---------------------------------------------------------------- Founder
founder = f"""<section class="page-hero"><div class="wrap split">
<div class="portrait">{'<img src="assets/founder.jpg" alt="Mikhail Seleznev">' if os.path.exists(ROOT + "/assets/founder.jpg") else '<span>MS</span>'}</div>
<div class="prose">
<p class="kicker" style="margin-bottom:14px">Founder</p>
<h1 style="margin-bottom:32px">Mikhail Seleznev</h1>
<p>Mikhail founded Frisson Writing in 2026 after five years as a corporate reporting consultant at Fanda, working from London and Dubai.</p>
<p>He has led content on more than 25 annual and sustainability reports for listed and pre-IPO companies across the GCC, and has interviewed over 15 C-level executives and Board members along the way.</p>
<div class="creds">
<div><h3>Credentials</h3><ul>
<li><b>Financial Modelling and Valuation Analyst (FMVA)</b>Corporate Finance Institute, 2025</li>
<li><b>Certificate in Sustainable Investing</b>CFA Institute, 2021</li>
<li><b>BA in History</b>Durham University, 2020</li></ul></div>
<div><h3>Recognition</h3><ul>
<li><b>Judge, ARC Awards 2026</b>Annual Reports</li>
<li><b>Judge, MEIRA Reporting Awards 2025</b>ESG judging panel</li>
<li><b>Speaker and panel moderator</b>MEIRA conferences and chapter meetings</li></ul></div>
</div>
</div>
</div></section>

<section class="band dark"><div class="wrap">
<p class="statement">Finance training, sustainability training and five reporting seasons, held by the person who writes the report.</p>
{FIGURES}
<div class="actions"><a class="btn" href="services.html#competencies">See the competencies</a><a class="btn" href="mailto:{EMAIL}">Email Mikhail</a></div>
</div></section>"""
page("founder.html", "Founder | Frisson Writing",
     "Mikhail Seleznev is the founder of Frisson Writing, a report writer and consultant with five years on Gulf annual and sustainability reports.", founder)

# ---------------------------------------------------------------- Contact
contact = f"""<section class="band dark" style="min-height:70vh"><div class="wrap">
<p class="kicker" style="margin-bottom:20px">Contact</p>
<h1 style="margin-bottom:40px">Start with an email.</h1>
<a class="mail" href="mailto:{EMAIL}">{EMAIL}</a>
<div class="contact-grid">
<div><h3>Useful to include</h3><p>The type of report, the reporting year, the deadline and where the content stands today.</p></div>
<div><h3>Location</h3><p>Dubai, United Arab Emirates. Available on site across the Gulf.</p></div>
<div><h3>Company</h3><p>Frisson Writing LLC, licensed by Shams Free Zone, Sharjah, UAE.</p></div>
</div>
</div></section>"""
page("contact.html", "Contact | Frisson Writing", "Contact Frisson Writing about an annual, sustainability, integrated or governance report.", contact)
print("built", len(PROJECTS), "projects")
