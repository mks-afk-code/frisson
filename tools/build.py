"""Builds the Frisson Writing site. Run from the repo root:  python3 tools/build.py

Edit the copy and the PROJECTS list below, then run this script to regenerate the pages.
Covers: save as assets/covers/<slug>.jpg (or .png / .webp) and rebuild.
Links: fill in the "link" field of a project.
"""
import html, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL = "mikhail@frissonwriting.com"
e = html.escape

AR, SR, CP = "Annual Report", "Sustainability Report", "Company Profile"
LEAD = "Content development and consultancy"
EDIT = "Copyediting"
AGENCY = "Delivered while at Fanda"

# Awards confirmed from published results. "short" marks a shortlisting.
ARC25_GRAND = ("Grand Award, ARC Awards 2025", "")
CFA25_GOLD = ("Gold, Corporate & Financial Awards 2025", "")
ARC26_GRAND = ("Grand Award, ARC Awards 2026", "")
ARC26_SILVER = ("Silver, ARC Awards 2026", "")
CFA26_SHORT = ("Shortlisted, Corporate & Financial Awards 2026", "short")

# slug, company, kind, year, exchange, role, link, awards
PROJECTS = [
    ("dtc-ar24", "Dubai Taxi Company", AR, "2024", "DFM", LEAD,
     "https://feeds.dfm.ae/documents/2025/Mar/7/73743a5a-cc45-4a22-98a8-bd352ffc6a1a/DTC%20Integrated%20Repor.pdf", [ARC25_GRAND, CFA25_GOLD]),
    ("oqep-ar25", "OQ Exploration and Production", AR, "2025", "MSX", LEAD, "", [ARC26_GRAND]),
    ("dtc-ar25", "Dubai Taxi Company", AR, "2025", "DFM", LEAD, "https://ar2025.dubaitaxi.ae/en", [ARC26_SILVER, CFA26_SHORT]),
    ("burjeel-ar25", "Burjeel Holdings", AR, "2025", "ADX", LEAD,
     "https://burjeelholdings.com/wp-content/uploads/2026/03/BH-2025-Annual-Report-ENG.pdf", [CFA26_SHORT]),
    ("luberef-ar25", "Luberef", AR, "2025", "Saudi Exchange", LEAD,
     "https://luberefapp.s3-accelerate.amazonaws.com/documents/luberef_ar2025_eng.pdf", []),
    ("jamjoom-ar25", "Jamjoom Pharma", AR, "2025", "Saudi Exchange", LEAD, "", []),
    ("gig-ar25", "Gulf Insurance Group", AR, "2025", "Boursa Kuwait", LEAD, "https://report2025.gulfinsgroup.com/", []),
    ("milaha-ar25", "Qatar Navigation (Milaha)", AR, "2025", "Qatar Exchange", LEAD,
     "https://www.milaha.com/sites/default/files/2026-02/Milaha-Annual-Report-2025-EN.pdf", []),
    ("sadafco-ar25", "SADAFCO", AR, "2025", "Saudi Exchange", LEAD, "", []),
    ("emsteel-ar25", "EMSTEEL", AR, "2025", "ADX", EDIT, "", []),
    ("gulfnav-ar25", "Gulf Navigation Holding", AR, "2025", "DFM", EDIT, "", []),
    ("luberef-sr24", "Luberef", SR, "2024", "Saudi Exchange", LEAD, "", []),
    ("maharah-sr24", "Maharah", SR, "2024", "Saudi Exchange", LEAD, "", []),
    ("burjeel-ar24", "Burjeel Holdings", AR, "2024", "ADX", LEAD,
     "https://burjeelholdings.com/wp-content/uploads/2025/03/ENG-BH-Annual-Report-2024.pdf", []),
    ("gig-ar24", "Gulf Insurance Group", AR, "2024", "Boursa Kuwait", LEAD, "https://report2024.gulfinsgroup.com/", []),
    ("fixprice-ar24", "Fix Price", AR, "2024", "MOEX and AIX", LEAD, "", []),
    ("emsteel-ar24", "EMSTEEL", AR, "2024", "ADX", EDIT, "https://ar2024.emsteel.com/en", []),
    ("gulfnav-ar24", "Gulf Navigation Holding", AR, "2024", "DFM", EDIT,
     "https://feeds.dfm.ae/documents/2025/Mar/31/d2f310cb-cd33-449b-849a-eacda0245585/GULFNAV_EN_Integrated_Report_2024.pdf", []),
    ("gig-profile", "Gulf Insurance Group", CP, "", "Boursa Kuwait", "Content development",
     "https://www.gulfinsgroup.com/media/GIG_Corporate_profile_2025_2105_2-page_view.pdf", []),
    ("luberef-sr23", "Luberef", SR, "2023", "Saudi Exchange", LEAD, "", []),
    ("phosagro-ar23", "PhosAgro", AR, "2023", "", "Content development", "https://ar2023.phosagro.com/", []),
    ("eurochem-ar23", "EuroChem", AR, "2023", "", "Content development", "", []),
]
FEATURED = ["dtc-ar24", "oqep-ar25", "dtc-ar25", "burjeel-ar25", "luberef-ar25", "jamjoom-ar25", "gig-ar25", "milaha-ar25"]
TONES = [("#D5C4A8", ""), ("#E8DECD", ""), ("#6A5540", "dark"), ("#C6B08E", ""), ("#2B2118", "dark"), ("#DDCFB8", ""), ("#A88C66", "dark")]
BY = {p[0]: p for p in PROJECTS}

NAV = [("services.html", "Services"), ("projects.html", "Projects"), ("approach.html", "Approach"), ("founder.html", "Founder")]


def is_wide(slug):
    for ext in ("jpg", "jpeg", "png", "webp"):
        f = f"{ROOT}/assets/covers/{slug}.{ext}"
        if os.path.exists(f):
            w, h = Image.open(f).size
            return w > h
    return False


def cover(p, i, eager=False):
    slug, company, kind, year = p[:4]
    for ext in ("jpg", "jpeg", "png", "webp"):
        f = f"{ROOT}/assets/covers/{slug}.{ext}"
        if os.path.exists(f):
            w, h = Image.open(f).size
            load = "" if eager else ' loading="lazy"'
            src = f"assets/covers/{slug}.{ext}"
            alt = f"Cover of the {e(company)} {e(kind)} {year}"
            if w > h:
                return (f'<div class="slot"><div class="frame has-img wide" style="aspect-ratio:{w}/{h}">'
                        f'<img src="{src}" width="{w}" height="{h}"{load} alt="{alt}"></div></div>')
            return f'<div class="frame has-img"><img src="{src}" width="{w}" height="{h}"{load} alt="{alt}"></div>'
    c, t = TONES[i % len(TONES)]
    return (f'<div class="frame"><div class="ph {t}" style="--c:{c}"><div><b>{e(company)}</b>'
            f'<small>{e(kind)}</small></div><i>{year or "Profile"}</i></div></div>')


def card(p, i, tag="article"):
    slug, company, kind, year, exch, role, link, awards = p
    title = f"{kind} {year}".strip()
    kindkey = "annual" if kind == AR else "sustainability" if kind == SR else "other"
    rec = " recognised" if awards else ""
    sub = e(title) + (f"<br>{e(exch)}" if exch else "")
    aw = ""
    if awards:
        aw = '<div class="awards">' + "".join(f'<span class="award {c}">{e(t)}</span>' for t, c in awards) + "</div>"
    inner = (f'{cover(p, i)}<h3>{e(company)}</h3><p class="sub">{sub}</p>'
             f'<p class="role">{e(role)}. {AGENCY}.</p>{aw}')
    if link:
        inner += f'<a class="link" href="{e(link)}" target="_blank" rel="noopener">View the report<span class="sr"> for {e(company)} {e(title)} (opens in a new tab)</span></a>'
    wcls = " is-wide" if is_wide(slug) else ""
    return f'<{tag} class="card{wcls}" data-kind="{kindkey}{rec}">{inner}</{tag}>'


def carousel(label, cards):
    return (f'<div class="carousel" data-carousel aria-roledescription="carousel" aria-label="{e(label)}">'
            f'<div class="car-track" aria-live="polite">{cards}</div>'
            '<div class="car-nav" hidden><button type="button" class="car-btn" data-dir="-1" aria-label="Previous projects">'
            '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M12.5 4 6.5 10l6 6"/></svg></button>'
            '<span class="car-count"></span>'
            '<button type="button" class="car-btn" data-dir="1" aria-label="Next projects">'
            '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M7.5 4l6 6-6 6"/></svg></button></div></div>')


CAROUSEL_JS = """<script>
(function () {
  document.querySelectorAll('[data-carousel]').forEach(function (root) {
    var track = root.querySelector('.car-track'), nav = root.querySelector('.car-nav');
    var items = [].slice.call(track.children), count = root.querySelector('.car-count');
    var prev = root.querySelector('[data-dir="-1"]'), next = root.querySelector('[data-dir="1"]');
    var pages = [], cur = 0, cols = 0;
    root.classList.add('js');
    function columns() { var w = root.clientWidth; return w >= 980 ? 4 : w >= 620 ? 3 : 2; }
    function build() {
      var c = columns(); if (c === cols && pages.length) return; cols = c;
      root.style.setProperty('--cols', c); root.classList.toggle('one', c === 1);
      pages = []; var left = items.slice();
      var units = function (it) { return c > 1 && it.classList.contains('is-wide') ? 2 : 1; };
      while (left.length) {
        var pg = [], used = 0;
        for (var i = 0; i < left.length && used < c; ) {
          if (used + units(left[i]) <= c) { used += units(left[i]); pg.push(left.splice(i, 1)[0]); } else { i++; }
        }
        pages.push(pg);
      }
      var first = items.indexOf((pages[cur] || pages[0])[0]);
      cur = 0; pages.forEach(function (p, i) { if (p.indexOf(items[first]) >= 0) cur = i; });
      show(false);
    }
    function show(anim) {
      items.forEach(function (it) { it.hidden = pages[cur].indexOf(it) < 0; });
      nav.hidden = pages.length < 2;
      count.textContent = (cur + 1) + ' / ' + pages.length;
      prev.disabled = cur === 0; next.disabled = cur === pages.length - 1;
      if (anim) { track.classList.remove('fade'); void track.offsetWidth; track.classList.add('fade'); }
    }
    function go(d) { var n = cur + d; if (n < 0 || n >= pages.length) return; cur = n; show(true); }
    prev.addEventListener('click', function () { go(-1); });
    next.addEventListener('click', function () { go(1); });
    root.addEventListener('keydown', function (ev) { if (ev.key === 'ArrowLeft') go(-1); if (ev.key === 'ArrowRight') go(1); });
    var x0 = null;
    track.addEventListener('touchstart', function (ev) { x0 = ev.touches[0].clientX; }, { passive: true });
    track.addEventListener('touchend', function (ev) { if (x0 === null) return; var dx = ev.changedTouches[0].clientX - x0; if (Math.abs(dx) > 40) go(dx < 0 ? 1 : -1); x0 = null; });
    window.addEventListener('resize', build); build();
  });
})();
</script>"""


def page(fname, title, desc, body):
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == fname else ""}>{t}</a>' for h, t in NAV)
    cur = ' aria-current="page"' if fname == "contact.html" else ""
    foot = "".join(f'<a href="{h}">{t}</a>' for h, t in NAV + [("contact.html", "Contact")])
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
<meta name="theme-color" content="#F3EDE2">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/lora.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head"><div class="wrap">
<a class="brand-text" href="index.html" aria-label="Frisson Writing, home"><span class="bf">Frisson</span><span class="bw">Writing</span></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
<nav class="nav" id="nav" aria-label="Main">{nav}<a class="pill" href="contact.html"{cur}>Contact</a></nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-foot"><div class="wrap">
<img src="assets/logo-light.svg" alt="Frisson Writing" width="160" height="50">
<nav aria-label="Footer">{foot}</nav>
<span>Frisson Writing LLC, licensed by Shams Free Zone, Sharjah. Based in Dubai.</span>
</div></footer>
<script>
(function () {{
  var h = document.querySelector('.site-head'), b = document.querySelector('.menu-btn'), n = document.getElementById('nav');
  var on = function () {{ h.classList.toggle('scrolled', window.scrollY > 8); }}; on(); window.addEventListener('scroll', on, {{ passive: true }});
  b.addEventListener('click', function () {{ var o = n.classList.toggle('open'); b.setAttribute('aria-expanded', o); b.textContent = o ? 'Close' : 'Menu'; }});
}})();
</script>
{CAROUSEL_JS if "data-carousel" in body else ""}
</body>
</html>
"""
    open(f"{ROOT}/{fname}", "w").write(doc)


CTA = f"""<section class="cta"><div class="wrap">
<div><h2>Discuss your next report</h2><p>Share the report type, the timeline and where the content stands today.</p></div>
<a class="btn" href="mailto:{EMAIL}">{EMAIL}</a>
</div></section>"""

SERVICES = [
    ("Annual reports", "Core service", [
        "Full content for the front section of the annual report. This covers the theme, structure and leadership statements, then the strategic, operational and financial reviews.",
        "Suitable for first reports after an IPO, full rebuilds and yearly updates."]),
    ("Sustainability reports", "Core service", [
        "Sustainability and ESG reports aligned with GRI, SASB, the UN SDGs, IFRS S1 and S2 and local exchange guidance.",
        "Includes support with materiality assessments and data collection."]),
    ("Integrated reports", "Core service", [
        "Reports that connect financial and non-financial performance through integrated thinking and the six capitals."]),
    ("Governance reports", "Core service", [
        "Copyediting or full drafting of corporate governance reports against the listing rules of the relevant GCC market."]),
    ("Investor presentations and profiles", "On request", [
        "Investor presentations, corporate profiles and leadership statements that draw on the same equity story as the report."]),
    ("Analysis and benchmarking", "Consulting", [
        "Gap analysis of the latest report against reporting frameworks and exchange requirements.",
        "Peer review of local and international peers across more than 20 data points."]),
]


def accordion(items, open_first=True):
    out = '<div class="acc">'
    for k, (t, tag, paras) in enumerate(items):
        o = " open" if open_first and k == 0 else ""
        out += f'<details{o}><summary>{e(t)}<span class="tag">{e(tag)}</span></summary><div class="body">' + "".join(f"<p>{e(x)}</p>" for x in paras) + "</div></details>"
    return out + "</div>"


PORTRAIT = '<figure><div class="portrait"><img src="assets/founder.jpg" width="299" height="299" alt="Mikhail Seleznev"></div></figure>'

# ---------------------------------------------------------------- Home
fan = "".join(cover(BY[s], i, eager=True) for i, s in enumerate(["luberef-ar25", "oqep-ar25", "gig-ar25"]))
rail = "".join(card(BY[s], i) for i, s in enumerate(FEATURED))

home = f"""<section class="hero"><div class="wrap">
<div>
<h1>Content and consultancy for corporate reports</h1>
<p class="lede">Frisson Writing develops the content of annual, sustainability, integrated and governance reports for listed companies across the Gulf, from structure and interviews to the final draft.</p>
<div class="actions"><a class="btn solid" href="projects.html">View projects</a><a class="btn ghost" href="contact.html">Get in touch</a></div>
</div>
<div class="fan" aria-hidden="true">{fan}</div>
</div></section>

<div class="recog"><div class="wrap">
<p>Projects recognised at</p>
<ul>
<li>ARC Awards<span>Grand Award 2025 and 2026</span></li>
<li>Corporate &amp; Financial Awards<span>Gold 2025</span></li>
</ul>
</div></div>

<section><div class="wrap">
<div class="sec-head"><div><h2>Selected projects</h2><p class="intro">Reports for companies listed on the Saudi Exchange, DFM, ADX, Boursa Kuwait, MSX and Qatar Exchange.</p></div><a class="more" href="projects.html">All {len(PROJECTS)} projects</a></div>
{carousel("Selected projects", rail)}
</div></section>

<section class="sec-paper"><div class="wrap split">
<div class="stick"><h2>Services</h2><p class="intro">Reports are the main focus. Presentations, profiles and analysis support them.</p><div class="actions"><a class="btn ghost" href="services.html">All services</a></div></div>
{accordion(SERVICES[:4] + SERVICES[4:5])}
</div></section>

<section><div class="wrap founder">
{PORTRAIT}
<div class="bio">
<h2>About the founder</h2>
<p>Mikhail Seleznev founded Frisson Writing in 2026 after five years as a corporate reporting consultant at Fanda in London and Dubai.</p>
<p>He has led content on more than 25 annual and sustainability reports for listed and pre-IPO companies across the GCC, working directly with boards, executive teams and investor relations teams.</p>
<div class="actions"><a class="btn ghost" href="founder.html">Read more</a><a class="btn ghost" href="approach.html">How projects run</a></div>
</div>
</div></section>
{CTA}"""
page("index.html", "Frisson Writing | Corporate report writing and consultancy",
     "Frisson Writing develops the content of annual, sustainability, integrated and governance reports for listed companies across the Gulf.", home)

# ---------------------------------------------------------------- Services
COMP = [
    ("Investor communication", "Performance narratives and investment cases built from financial and non-financial data, peer benchmarking and market research."),
    ("Stakeholder engagement", "Interviews with board members and executives, and engagement with internal and external stakeholders for materiality assessments."),
    ("Financial analysis", "Financial reviews written from quarterly results, earnings calls and sell-side research."),
    ("Sustainability reporting", "Working knowledge of GRI, SASB, the UN SDGs and IFRS S1 and S2, with integrated thinking across the six capitals."),
    ("Governance and compliance", "Listing rules and disclosure requirements in the UAE, Saudi Arabia, Oman, Qatar and Kuwait, plus gap analyses of governance reports."),
    ("Copywriting and editing", "Leadership statements, financial summaries, market reviews and investor materials written to a consistent standard."),
]
services = f"""<section class="hero"><div class="wrap" style="grid-template-columns:1fr">
<div><h1>Services</h1><p class="lede">Frisson Writing covers the full content of a report and the advisory work that shapes it.</p></div>
</div></section>

<section class="sec-paper"><div class="wrap split">
<div class="stick"><h2>What Frisson Writing delivers</h2></div>
{accordion(SERVICES)}
</div></section>

<section id="competencies"><div class="wrap split">
<div class="stick"><h2>Competencies</h2><p class="intro">Each report draws on financial, sustainability and regulatory expertise.</p></div>
<div>
<ul class="list">{"".join(f"<li><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in COMP)}</ul>
<ul class="tags" aria-label="Frameworks">{"".join(f"<li>{t}</li>" for t in ["GRI", "SASB", "UN SDGs", "IFRS S1", "IFRS S2", "Integrated reporting", "GCC listing rules"])}</ul>
</div>
</div></section>
{CTA}"""
page("services.html", "Services | Frisson Writing",
     "Annual, sustainability, integrated and governance reports, with investor presentations, corporate profiles, gap analysis and peer benchmarking.", services)

# ---------------------------------------------------------------- Projects
cards = "".join(card(p, i) for i, p in enumerate(PROJECTS))
projects = f"""<section class="hero"><div class="wrap" style="grid-template-columns:1fr">
<div><h1>Projects</h1><p class="lede">Annual, sustainability and other reports for listed companies, with the role on each one.</p></div>
</div></section>

<section class="sec-paper" style="padding-top:56px"><div class="wrap">
<div class="filters" role="group" aria-label="Filter projects">
<button type="button" data-f="all" aria-pressed="true">All</button>
<button type="button" data-f="recognised" aria-pressed="false">Recognised</button>
<button type="button" data-f="annual" aria-pressed="false">Annual reports</button>
<button type="button" data-f="sustainability" aria-pressed="false">Sustainability reports</button>
<button type="button" data-f="other" aria-pressed="false">Other</button>
</div>
<div class="grid" id="grid">{cards}</div>
<p class="disclaimer">All reports are published by the companies named, and the cover designs belong to them and their agencies. Mikhail Seleznev contributed to these reports in the role stated while at Fanda, before founding Frisson Writing. Awards were given to the reports and the teams that produced them.</p>
</div></section>
<script>
document.querySelectorAll('.filters button').forEach(function (b) {{
  b.addEventListener('click', function () {{
    document.querySelectorAll('.filters button').forEach(function (x) {{ x.setAttribute('aria-pressed', x === b); }});
    document.querySelectorAll('#grid > .card').forEach(function (a) {{ a.hidden = b.dataset.f !== 'all' && a.dataset.kind.split(' ').indexOf(b.dataset.f) < 0; }});
  }});
}});
</script>
{CTA}"""
page("projects.html", "Projects | Frisson Writing",
     "Annual and sustainability reports for companies listed on the Saudi Exchange, DFM, ADX, Boursa Kuwait, MSX and Qatar Exchange.", projects)

# ---------------------------------------------------------------- Approach
STAGES = [
    ("Consultancy", "Advice on report changes, framework selection and content gaps. Frisson Writing acts as content owner on client calls."),
    ("Analysis", "Peer reviews and gap analyses that show how current reporting compares with requirements and competitors."),
    ("Theme", "A narrative theme that gives the report a clear identity and guides the design direction."),
    ("Structure", "A full report structure with content flow, pagination and a section-by-section map of the information required."),
    ("Data gathering", "Bespoke questionnaires for qualitative and quantitative data, followed by interviews with management."),
    ("Drafting", "All sections written in line with the confirmed structure."),
    ("Revisions", "The draft refined through structured rounds of client feedback."),
    ("Design support", "Support for the designers as they apply client comments, with advice on photography that fits the narrative."),
]
approach = f"""<section class="hero"><div class="wrap" style="grid-template-columns:1fr">
<div><h1>Approach</h1><p class="lede">Frisson Writing stays involved from the first advisory call until the designers close the file.</p></div>
</div></section>

<section class="sec-paper"><div class="wrap split">
<div class="stick"><h2>How a project runs</h2><p class="intro">One writer handles every stage, so the narrative stays consistent from structure to final proof.</p></div>
<ol class="timeline">{"".join(f"<li><h3>{s}</h3><p>{d}</p></li>" for s, d in STAGES)}</ol>
</div></section>

<section><div class="wrap">
<div class="sec-head"><div><h2>Recognised reports</h2><p class="intro">Award-winning and shortlisted reports that Mikhail Seleznev contributed to.</p></div><a class="more" href="projects.html">All projects</a></div>
{carousel("Recognised reports", "".join(card(p, i) for i, p in enumerate(PROJECTS) if p[7]))}
</div></section>

<section class="sec-oat"><div class="wrap split">
<div class="stick"><h2>Working arrangements</h2></div>
<ul class="list">
<li><h3>Tools</h3><p>Proprietary platforms, Microsoft Teams or the client's preferred tools.</p></li>
<li><h3>Location</h3><p>Based in Dubai, with in-person interviews and meetings across the UAE and the wider region.</p></li>
<li><h3>Confidentiality</h3><p>All client materials and data stay confidential under the client's NDA or one drafted for the project.</p></li>
<li><h3>Capacity</h3><p>Up to 15 reports of varying size during the reporting season.</p></li>
</ul>
</div></section>
{CTA}"""
page("approach.html", "Approach | Frisson Writing",
     "How Frisson Writing runs a report project, from consultancy and structure to drafting, revisions and design support.", approach)

# ---------------------------------------------------------------- Founder
founder = f"""<section class="hero"><div class="wrap founder">
{PORTRAIT}
<div class="bio">
<h1 style="margin-bottom:24px">Mikhail Seleznev</h1>
<p>Mikhail founded Frisson Writing in 2026. He spent the previous five years as a corporate reporting consultant at Fanda in London and Dubai, where he led content on annual and sustainability reports for companies listed across the GCC.</p>
<p>His work combines financial analysis with sustainability reporting. He has interviewed more than 15 board members and senior executives and writes directly from those conversations.</p>
</div>
</div></section>

<section class="sec-paper"><div class="wrap split">
<div class="stick"><h2>Background</h2></div>
<div>
<dl class="facts" style="margin-top:0">
<div><dt>Financial Modelling and Valuation Analyst (FMVA)</dt><dd>Corporate Finance Institute, 2025</dd></div>
<div><dt>Certificate in Sustainable Investing</dt><dd>CFA Institute, 2021</dd></div>
<div><dt>BA in History</dt><dd>Durham University, 2020</dd></div>
<div><dt>Corporate Reporting Consultant</dt><dd>Fanda, London and Dubai, 2020 to 2026</dd></div>
<div><dt>Awards judging</dt><dd>ARC Awards 2025 and MEIRA Reporting Awards 2025</dd></div>
<div><dt>Speaking</dt><dd>Workshops and panels at MEIRA conferences and chapter meetings</dd></div>
</dl>
<div class="actions"><a class="btn ghost" href="services.html#competencies">View competencies</a></div>
</div>
</div></section>
{CTA}"""
page("founder.html", "Founder | Frisson Writing",
     "Mikhail Seleznev founded Frisson Writing after five years as a corporate reporting consultant on Gulf annual and sustainability reports.", founder)

# ---------------------------------------------------------------- Contact
contact = f"""<section class="hero" style="min-height:62vh"><div class="wrap" style="grid-template-columns:1fr">
<div>
<h1 style="margin-bottom:32px">Discuss your next report</h1>
<a class="mail" href="mailto:{EMAIL}">{EMAIL}</a>
<dl class="contact-list">
<div><dt>Helpful to include</dt><dd>The report type and year, the deadline and where the content stands today.</dd></div>
<div><dt>Location</dt><dd>Dubai, United Arab Emirates. Available on site across the Gulf.</dd></div>
<div><dt>Company</dt><dd>Frisson Writing LLC, licensed by Shams Free Zone, Sharjah.</dd></div>
</dl>
</div>
</div></section>"""
page("contact.html", "Contact | Frisson Writing", "Contact Frisson Writing about an annual, sustainability, integrated or governance report.", contact)
print("built", len(PROJECTS), "projects")
