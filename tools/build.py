"""Builds the Frisson Writing site. Run from the repo root:  python3 tools/build.py

Edit the copy and the PROJECTS list below, then run this script to regenerate the pages.
Client names are deliberately left out of the published site.
"""
import html, os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL = "mikhail@frissonwriting.com"
e = html.escape

# Report types
AR, IR, SR, CP = "Annual report", "Integrated report", "Sustainability report", "Company profile"

# Industries: key -> (label, svg path data on a 24 x 24 grid)
INDUSTRIES = {
    "energy": ("Energy", "M12 3c3.6 4.5 6 7.7 6 10.6a6 6 0 0 1-12 0C6 10.7 8.4 7.5 12 3z M9.5 14.5a2.5 2.5 0 0 0 2.5 2.5"),
    "utilities": ("Utilities", "M13.5 3L5.5 13.5h6L10.5 21l8-10.5h-6z"),
    "industrials": ("Industrials", "M3 15h18l-2.6 4.5H5.6z M6 15V9.5h12V15 M9.5 9.5V6.5h5v3"),
    "health": ("Health Care", "M7 4h10a3 3 0 0 1 3 3v10a3 3 0 0 1-3 3H7a3 3 0 0 1-3-3V7a3 3 0 0 1 3-3z M12 8.5v7 M8.5 12h7"),
    "financials": ("Financials", "M3.5 9L12 4.5 20.5 9 M5.5 9.5v8 M10 9.5v8 M14 9.5v8 M18.5 9.5v8 M3.5 20h17"),
    "materials": ("Materials", "M9 3.5h6 M10 3.5v6L5.3 17.6A2 2 0 0 0 7 20.5h10a2 2 0 0 0 1.7-2.9L14 9.5v-6 M7.6 14.5h8.8"),
    "staples": ("Consumer Staples", "M5 8h14l-1.2 12H6.2z M9 8V6.5a3 3 0 0 1 6 0V8"),
    "discretionary": ("Consumer Discretionary", "M3 4.5h2.5l2.2 10.5h10.4l2-7.5H6.6 M9.5 19.5a1.2 1.2 0 1 0 0-.01 M16.5 19.5a1.2 1.2 0 1 0 0-.01"),
    "comms": ("Communication Services", "M12 11v10 M9 21h6 M8.6 7.6a4.8 4.8 0 0 0 0 6.8 M15.4 7.6a4.8 4.8 0 0 1 0 6.8 M5.8 4.8a8.8 8.8 0 0 0 0 12.4 M18.2 4.8a8.8 8.8 0 0 1 0 12.4 M12 11.2a.9.9 0 1 0 0-1.8.9.9 0 0 0 0 1.8z"),
}

# Exchanges: key -> (label, country, logo file or "")
EXCHANGES = {
    "tadawul": ("Saudi Exchange", "Saudi Arabia", "tadawul.svg"),
    "dfm": ("Dubai Financial Market", "UAE", "dfm.svg"),
    "adx": ("Abu Dhabi Securities Exchange", "UAE", "adx.png"),
    "boursa": ("Boursa Kuwait", "Kuwait", "boursa.svg"),
    "moex": ("Moscow Exchange", "Russia", "moex.svg"),
    "msx": ("Muscat Stock Exchange", "Oman", "msx.png"),
    "qse": ("Qatar Stock Exchange", "Qatar", "qse.svg"),
    "aix": ("Astana International Exchange", "Kazakhstan", "aix.png"),
    "kase": ("Kazakhstan Stock Exchange", "Kazakhstan", "kase.svg"),
}

# Size bands by market value around the time of the report (US$)
CAPS = [("large", "Large cap", "Above US$10 billion"), ("mid", "Mid cap", "US$2 to 10 billion"),
        ("small", "Small cap", "Below US$2 billion"), ("private", "Unlisted", "Privately held")]

# Awards confirmed from published results (Communicate magazine winners lists, MerComm ARC winners, company releases)
CF = "Corporate & Financial Awards"

# year, report type, industry, size band, exchanges, awards, in progress
PROJECTS = [
    ("2026", IR, "comms", "large", ["dfm"], [], True),
    ("2026", IR, "health", "mid", ["adx"], [], True),
    ("2026", IR, "industrials", "small", ["dfm"], [], True),
    ("2026", AR, "industrials", "mid", ["tadawul"], [], True),
    ("2026", AR, "financials", "mid", ["tadawul"], [], True),
    ("2026", AR, "energy", "mid", ["tadawul"], [], True),
    ("2025", IR, "utilities", "large", ["tadawul"], ["Gold and Bronze, ARC Awards 2026"], False),
    ("2025", AR, "energy", "mid", ["tadawul"], ["Silver, ARC Awards 2026"], False),
    ("2025", IR, "industrials", "small", ["dfm"], ["Gold and Silver, ARC Awards 2026", f"Silver, {CF} 2026"], False),
    ("2025", AR, "health", "mid", ["adx"], ["Silver, ARC Awards 2026", f"Bronze, {CF} 2026"], False),
    ("2025", AR, "health", "mid", ["tadawul"], ["Honors, ARC Awards 2026"], False),
    ("2025", AR, "energy", "mid", ["msx"], ["Grand Award and Gold, ARC Awards 2026"], False),
    ("2025", AR, "financials", "small", ["boursa"], ["Gold, ARC Awards 2026"], False),
    ("2025", AR, "staples", "mid", ["tadawul"], [], False),
    ("2025", AR, "industrials", "mid", ["qse"], [], False),
    ("2025", AR, "materials", "mid", ["adx"], [], False),
    ("2025", AR, "industrials", "small", ["dfm"], [], False),
    ("2025", CP, "financials", "small", ["boursa"], [], False),
    ("2024", IR, "utilities", "large", ["tadawul"], [f"Bronze, {CF} 2025"], False),
    ("2024", IR, "industrials", "small", ["dfm"], ["Grand Award, ARC Awards 2025", f"Gold, {CF} 2025"], False),
    ("2024", AR, "health", "mid", ["adx"], [], False),
    ("2024", AR, "financials", "small", ["boursa"], [], False),
    ("2024", AR, "staples", "small", ["moex", "aix"], [], False),
    ("2024", IR, "industrials", "small", ["dfm"], [], False),
    ("2024", AR, "materials", "mid", ["adx"], [], False),
    ("2024", SR, "energy", "mid", ["tadawul"], [], False),
    ("2024", SR, "industrials", "small", ["tadawul"], [], False),
    ("2023", SR, "energy", "mid", ["tadawul"], [], False),
    ("2023", SR, "discretionary", "small", ["tadawul"], [], False),
    ("2023", AR, "materials", "large", ["moex"], [], False),
    ("2023", AR, "materials", "private", [], [], False),
    ("2022", AR, "energy", "large", ["aix", "kase"], [f"Gold, {CF} 2023", "Honors, ARC Awards 2023"], False),
    ("2022", AR, "materials", "mid", ["moex"], [], False),
    ("2022", AR, "health", "small", ["moex"], [], False),
]
N_COMPANIES = 22
N_LISTED = 21

NAV = [("index.html", "Home"), ("services.html", "Services"), ("projects.html", "Projects"), ("approach.html", "Approach"), ("founder.html", "Founder")]

ind_count = Counter(p[2] for p in PROJECTS)
cap_count = Counter(p[3] for p in PROJECTS)
exch_count = Counter(x for p in PROJECTS for x in p[4])
type_count = Counter(p[1] for p in PROJECTS)
N = len(PROJECTS)


def award_pill(a):
    top = a.startswith(("Grand", "Gold"))
    return f'<span class="award{"" if top else " short"}">{e(a)}</span>'


def award_tally(name):
    tally = {}
    for p in PROJECTS:
        for a in p[5]:
            if name in a:
                for lvl in a.split(",")[0].split(" and "):
                    lvl = lvl.strip().replace("Grand Award", "Grand")
                    tally[lvl] = tally.get(lvl, 0) + 1
    order = ["Grand", "Gold", "Silver", "Bronze", "Honors"]
    return [(l, tally[l]) for l in order if l in tally]


def recognition_cards():
    out = '<div class="recards">'
    for logo, alt, key, years in [("arc.png", "ARC Awards", "ARC Awards", "2023 and 2026"),
                                  ("cfawards.png", "Corporate &amp; Financial Awards", "Corporate & Financial", "2023 and 2026")]:
        chips = "".join(f'<li><b>{n}</b>{l}{"" if l in ("Honors",) else (" Award" if l == "Grand" else "")}</li>' for l, n in award_tally(key))
        out += f'<article class="recard"><img src="assets/badges/{logo}" alt="{alt}"><ul class="chips">{chips}</ul><p class="small-note">Awards won between {years}</p></article>'
    return out + "</div>"


def icon(key, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true"><path d="{INDUSTRIES[key][1]}"/></svg>'


def exch_logo(key):
    name, _, f = EXCHANGES[key]
    if f:
        return f'<img src="assets/exchanges/{f}" alt="{e(name)}" loading="lazy">'
    return f'<span class="xword">{e(name)}</span>'


def industries_grid():
    items = sorted(INDUSTRIES, key=lambda k: -ind_count[k])
    return '<ul class="inds">' + "".join(
        f'<li>{icon(k)}<span class="n">{ind_count[k]}</span><span class="l">{e(INDUSTRIES[k][0])}</span></li>' for k in items) + "</ul>"


GCC = ["tadawul", "dfm", "adx", "boursa", "msx", "qse"]
OTHER = ["aix", "kase"]


def listing_label(exch):
    if not exch:
        return "Unlisted"
    main = [EXCHANGES[x][0] for x in exch if x not in OTHER]
    rest = [x for x in exch if x in OTHER]
    if rest:
        main.append("Other international exchanges" if len(rest) > 1 and not main else "an international exchange" if main else "International exchange")
    return " and ".join(main)


def exchanges_grid(counts=True, keys=None):
    flat = keys
    keys = keys or (GCC if not counts else sorted([k for k in EXCHANGES if k not in OTHER], key=lambda k: -exch_count[k]))
    out = '<ul class="exch' + ('' if counts else ' gcc') + (' flat' if flat else '') + '">'
    for k in keys:
        name, country, _ = EXCHANGES[k]
        meta = f'<span class="meta"><b>{exch_count[k]}</b> {"report" if exch_count[k] == 1 else "reports"}<br>{e(country)}</span>' if counts else ""
        out += f'<li><div class="logo">{exch_logo(k)}</div>{meta}</li>'
    if counts:
        n = sum(1 for p in PROJECTS if any(x in OTHER for x in p[4]))
        out += (f'<li><div class="logo"><span class="xword">Other international exchanges</span></div>'
                f'<span class="meta"><b>{n}</b> {"report" if n == 1 else "reports"}<br>International</span></li>')
    return out + "</ul>"


def cap_bar():
    segs = "".join(f'<span class="seg {k}" style="flex:{cap_count[k]}" title="{e(l)}"></span>' for k, l, _ in CAPS if cap_count[k])
    legend = "".join(f'<li><span class="dot {k}"></span><b>{cap_count[k]}</b> {e(l)}<small>{e(d)}</small></li>' for k, l, d in CAPS if cap_count[k])
    return f'<div class="capbar" role="img" aria-label="Reports by company size">{segs}</div><ul class="caplegend">{legend}</ul>'


def type_line():
    order = [AR, IR, SR, CP]
    return ", ".join(f"{type_count[t]} {t.lower()}{'s' if type_count[t] > 1 else ''}" for t in order if type_count[t])


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
<meta property="og:url" content="https://frissonwriting.com/{fname if fname != "index.html" else ""}">
<meta property="og:image" content="https://frissonwriting.com/assets/share.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Frisson Writing">
<meta property="og:site_name" content="Frisson Writing">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://frissonwriting.com/assets/share.png">
<meta name="theme-color" content="#F3EDE2">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/lora.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head"><div class="wrap">
<a class="brand" href="index.html"><img src="assets/logo.svg" alt="Frisson Writing, home" width="104" height="52"></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
<nav class="nav" id="nav" aria-label="Main">{nav}<a class="pill" href="contact.html"{cur}>Contact</a></nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-foot"><div class="wrap">
<img src="assets/logo-light.svg" alt="Frisson Writing" width="180" height="60">
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
<div><h2>Discuss your next project</h2><p>A short note on the document and the timeline is enough to start.</p></div>
<a class="btn" href="mailto:{EMAIL}">{EMAIL}</a>
</div></section>"""

SERVICES = [
    ("Annual and integrated reports", "Reporting", [
        "Annual and integrated reports developed around one consistent narrative and set of key messages, covering all operational, financial and other relevant disclosures."]),
    ("Sustainability reports", "Reporting", [
        "People-focused sustainability reports developed in line with ESG rating requirements, disclosure rules and international frameworks such as GRI, SASB, the UN SDGs and IFRS S1 and S2."]),
    ("Governance reports", "Reporting", [
        "Governance reports developed in line with regional and international best practice and local listing rules."]),
    ("Investor communications", "Communications", [
        "Presentations, equity story development and FAQs that keep the company's message to the market consistent."]),
    ("Leadership messaging and profiles", "Communications", [
        "Statements and key messages for the chairman, CEO, CFO and other C-suite leaders, plus company profiles, drafted from interviews with leadership."]),
    ("Analysis and benchmarking", "Advisory", [
        "Messaging proposals, gap analyses, peer reviews, materiality assessments and data verification ahead of public disclosure."]),
]


def accordion(items, open_first=True):
    out = '<div class="acc">'
    for k, (t, tag, paras) in enumerate(items):
        o = " open" if open_first and k == 0 else ""
        out += f'<details{o}><summary>{e(t)}<span class="tag">{e(tag)}</span></summary><div class="body">' + "".join(f"<p>{e(x)}</p>" for x in paras) + "</div></details>"
    return out + "</div>"


PORTRAIT = '<figure><div class="portrait"><img src="assets/founder.jpg" width="299" height="299" alt="Mikhail Seleznev"></div></figure>'

FIGURES = f"""<dl class="figs">
<div><dt>Reports</dt><dd>{N}</dd></div>
<div><dt>Listed companies</dt><dd>{N_LISTED}</dd></div>
<div><dt>Exchanges</dt><dd>{len(EXCHANGES)}</dd></div>
<div><dt>Sectors</dt><dd>{len(INDUSTRIES)}</dd></div>
</dl>"""

# ---------------------------------------------------------------- Home
home = f"""<section class="hero"><div class="wrap">
<div>
<h1 class="h-home">Content development and advisory for corporate communications</h1>
<p class="lede">Frisson Writing helps shape how listed companies across the Gulf present themselves to investors and stakeholders.</p>
<p class="lede lede-2">It develops the narrative and key messages that carry through annual, integrated and sustainability reports, investor presentations, corporate profiles and leadership communications.</p>
<div class="actions"><a class="btn solid" href="projects.html">View projects</a><a class="btn ghost" href="contact.html">Get in touch</a></div>
</div>
<aside class="panel" aria-label="Exchanges">
<p class="panel-t">Experience with companies listed on</p>
{exchanges_grid(counts=False)}
</aside>
</div></section>

<section class="sec-recog"><div class="wrap">
<div class="sec-head"><div><h2>Project recognitions</h2><p class="intro">Reports developed by Frisson Writing's founder have won at two leading international competitions for corporate reporting.</p></div><a class="more" href="projects.html#awards">Award highlights</a></div>
{recognition_cards()}
</div></section>

<section><div class="wrap">
<div class="sec-head"><div><h2>Track record</h2><p class="intro">{N} investor-facing reports for {N_LISTED} listed companies across a wide range of industries.</p></div><a class="more" href="projects.html">Full breakdown</a></div>
{industries_grid()}
</div></section>

<section class="sec-paper"><div class="wrap split">
<div class="stick"><h2>Services</h2><p class="intro">Annual, integrated, sustainability and governance reports, investor communications, leadership messaging and advisory.</p><div class="actions"><a class="btn ghost" href="services.html">All services</a></div></div>
{accordion(SERVICES[:5])}
</div></section>

<section><div class="wrap">
<div class="sec-head"><div><h2>Expertise</h2><p class="intro">Qualifications in finance and sustainable investing support every report.</p></div></div>
<ul class="expertise">
<li><img src="assets/badges/cfa.svg" alt=""><div><h3>Certificate in Sustainable Investing</h3><p>CFA Institute</p></div></li>
<li><img src="assets/badges/fmva.svg" alt=""><div><h3>Financial Modelling and Valuation Analyst (FMVA)</h3><p>Corporate Finance Institute</p></div></li>
<li><img src="assets/badges/arc.png" alt=""><div><h3>Awards judge</h3><p>ARC Awards and MEIRA Reporting Awards 2025</p></div></li>
</ul>
</div></section>

<section class="sec-accent"><div class="wrap founder">
{PORTRAIT}
<div class="bio">
<h2>About us</h2>
<p>Mikhail Seleznev founded Frisson Writing in 2026 after six years at a leading corporate reporting agency in London and Dubai.</p>
<p>He has led content development on more than 30 reports for listed and pre-IPO companies, working closely with investor relations and communication teams.</p>
<div class="actions"><a class="btn ghost" href="founder.html">Read more</a><a class="btn ghost" href="approach.html">How projects run</a></div>
</div>
</div></section>
{CTA}"""
page("index.html", "Frisson Writing | Corporate communications and report writing",
     "Frisson Writing provides content and consultancy for corporate and investor communications, from annual and sustainability reports to investor presentations and corporate profiles.", home)

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
<div><h1>Services</h1><p class="lede">Frisson Writing provides the content and consultancy behind corporate disclosure and investor communications.</p></div>
</div></section>

<section class="sec-paper"><div class="wrap split">
<div class="stick"><h2>Areas of work</h2></div>
{accordion(SERVICES)}
</div></section>

<section id="competencies"><div class="wrap split">
<div class="stick"><h2>Competencies</h2><p class="intro">Each project draws on financial, sustainability and regulatory expertise.</p></div>
<div>
<ul class="list">{"".join(f"<li><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in COMP)}</ul>
<div class="taggroups">
<div><h3>Skills</h3><ul class="tags">{"".join(f"<li>{t}</li>" for t in ["Messaging", "Narrative development", "Executive interviewing", "Copywriting", "Copyediting", "Benchmarking", "Materiality assessment", "Data verification"])}</ul></div>
<div><h3>Frameworks</h3><ul class="tags">{"".join(f"<li>{t}</li>" for t in ["GRI", "SASB", "UN SDGs", "IFRS S1", "IFRS S2", "Integrated reporting", "GCC listing rules"])}</ul></div>
</div></div>
</div>
</div></section>
{CTA}"""
page("services.html", "Services | Frisson Writing",
     "Annual, integrated, sustainability and governance reports, investor communications, corporate profiles, leadership messaging and benchmarking.", services)

# ---------------------------------------------------------------- Projects
def project_row(p):
    year, kind, ind, cap, exch, awards, live = p
    listing = listing_label(exch)
    capl = dict((k, l) for k, l, _ in CAPS)[cap]
    note = ""
    if live:
        note = '<span class="status">In progress</span>'
    elif awards:
        note = "".join(award_pill(a) for a in awards)
    xkeys = " ".join(sorted({('other' if x in OTHER else x) for x in exch})) or 'unlisted'
    tkey = {AR: 'ar', IR: 'ir', SR: 'sr', CP: 'cp'}[kind]
    return (f'<tr data-type="{tkey}" data-ind="{ind}" data-exch="{xkeys}" data-award="{1 if awards else 0}"><td data-l="Year">{year}</td><td data-l="Document">{e(kind)}</td>'
            f'<td data-l="Industry"><span class="cell-ind">{icon(ind, "ico sm")}{e(INDUSTRIES[ind][0])}</span></td>'
            f'<td data-l="Listing">{e(listing)}</td><td data-l="Size">{e(capl)}</td><td data-l="Notes" class="notes">{f'<div class="nwrap">{note}</div>' if note else ''}</td></tr>')


TYPE_OPTS = [("ar", AR + "s"), ("ir", IR + "s"), ("sr", SR + "s"), ("cp", CP + "s")]
EXCH_OPTS = [(k, EXCHANGES[k][0]) for k in GCC + ["moex"]] + [("other", "Other international exchanges"), ("unlisted", "Unlisted")]
IND_OPTS = sorted(((k, v[0]) for k, v in INDUSTRIES.items()), key=lambda x: x[1])


def select(name, label, opts):
    o = "".join(f'<option value="{k}">{e(v)}</option>' for k, v in opts)
    return f'<label class="pf"><span>{label}</span><select data-f="{name}"><option value="">All</option>{o}</select></label>'


FILTERS = ('<form class="pfilters" aria-label="Filter projects" onsubmit="return false">'
           + select("type", "Document", TYPE_OPTS) + select("ind", "Industry", IND_OPTS) + select("exch", "Exchange", EXCH_OPTS)
           + '<label class="pf pf-check"><input type="checkbox" data-f="award"> <span>Awarded only</span></label>'
           + '<button type="reset" class="pf-reset">Clear</button><p class="pf-count" aria-live="polite"></p></form>')

FILTER_JS = """<script>
(function () {
  var form = document.querySelector('.pfilters'); if (!form) return;
  var rows = [].slice.call(document.querySelectorAll('.ptable tbody tr'));
  var count = form.querySelector('.pf-count'), empty = document.querySelector('.pf-empty');
  function apply() {
    var t = form.querySelector('[data-f=type]').value, i = form.querySelector('[data-f=ind]').value,
        x = form.querySelector('[data-f=exch]').value, a = form.querySelector('[data-f=award]').checked, n = 0;
    rows.forEach(function (r) {
      var ok = (!t || r.dataset.type === t) && (!i || r.dataset.ind === i) &&
               (!x || r.dataset.exch.split(' ').indexOf(x) >= 0) && (!a || r.dataset.award === '1');
      r.hidden = !ok; if (ok) n++;
    });
    count.textContent = 'Showing ' + n + ' of ' + rows.length;
    empty.hidden = n > 0;
  }
  form.addEventListener('change', apply);
  form.addEventListener('reset', function () { setTimeout(apply, 0); });
  apply();
})();
</script>"""


AWARDED = sorted([p for p in PROJECTS if p[5]], key=lambda p: (-int(p[0]), -len(p[5])))


def award_item(p):
    year, kind, ind, cap, exch, awards, _ = p
    listing = listing_label(exch)
    return (f'<li>{icon(ind)}<div><h3>{e(kind)} {year}</h3><p>{e(INDUSTRIES[ind][0])}<br><span class="muted-sm">{e(listing)}</span></p>'
            '<div class="awards">' + "".join(award_pill(a) for a in awards) + "</div></div></li>")


projects = f"""<section class="hero"><div class="wrap" style="grid-template-columns:1fr">
<div><h1>Projects</h1><p class="lede">{N} investor-facing reports for {N_LISTED} listed companies across a wide range of industries: {type_line()}.</p></div>
</div></section>

<section class="sec-paper"><div class="wrap">
{FIGURES}
</div></section>

<section><div class="wrap split">
<div class="stick"><h2>By company size</h2><p class="intro">Banded by market value around the time of each report.</p></div>
<div>{cap_bar()}</div>
</div></section>

<section class="sec-oat"><div class="wrap">
<div class="sec-head"><div><h2>By industry</h2><p class="intro">Grouped by GICS sector.</p></div></div>
{industries_grid()}
</div></section>

<section><div class="wrap">
<div class="sec-head"><div><h2>By exchange</h2><p class="intro">Two of the companies were dual-listed and one was privately held.</p></div></div>
{exchanges_grid()}
</div></section>

<section class="sec-paper" id="awards"><div class="wrap split">
<div class="stick"><h2>Award highlights</h2><p class="intro">Every report in the portfolio that won at the ARC Awards or the Corporate &amp; Financial Awards.</p></div>
<div><ul class="awardlist">{"".join(award_item(p) for p in AWARDED)}</ul>
<p class="disclaimer">Awards were made to the reports and to the full teams that produced them.</p></div>
</div></section>
{CTA}"""
page("projects.html", "Projects | Frisson Writing",
     f"{N} investor-facing reports for {N_LISTED} listed companies across {len(EXCHANGES)} exchanges and {len(INDUSTRIES)} sectors.", projects)

# ---------------------------------------------------------------- Approach
STAGES = [
    ("Consultancy", "Advice on changes, framework selection and content gaps. Frisson Writing acts as content owner on client calls."),
    ("Analysis", "Peer reviews and gap analyses that show how current disclosure compares with requirements and competitors."),
    ("Theme", "A narrative theme that gives the document a clear identity and guides the design direction."),
    ("Structure", "A full structure with content flow, pagination and a section-by-section map of the information required."),
    ("Data gathering", "Bespoke questionnaires for qualitative and quantitative data, followed by interviews with management."),
    ("Drafting", "All sections written in line with the confirmed structure."),
    ("Revisions", "The draft refined through structured rounds of client feedback."),
    ("Design support", "Support for the designers as they apply client comments, with advice on photography that fits the narrative."),
]
approach = f"""<section class="hero"><div class="wrap" style="grid-template-columns:1fr">
<div><h1>Approach</h1><p class="lede">Frisson Writing stays involved from the first advisory call until official publication.</p></div>
</div></section>

<section class="sec-paper"><div class="wrap split">
<div class="stick"><h2>How a project runs</h2><p class="intro">One writer handles every stage, so the narrative stays consistent from structure to final proof.</p></div>
<ol class="timeline">{"".join(f"<li><h3>{s}</h3><p>{d}</p></li>" for s, d in STAGES)}</ol>
</div></section>

<section class="sec-oat"><div class="wrap split">
<div class="stick"><h2>Working arrangements</h2></div>
<ul class="list">
<li><h3>Tools</h3><p>Proprietary platforms, Microsoft Teams or the client's preferred tools.</p></li>
<li><h3>Location</h3><p>Based in Dubai, with in-person interviews and meetings across the UAE and the wider region.</p></li>
<li><h3>Confidentiality</h3><p>All client materials and data stay confidential under the client's NDA or one drafted for the project.</p></li>
</ul>
</div></section>
{CTA}"""
page("approach.html", "Approach | Frisson Writing",
     "How Frisson Writing runs a project, from consultancy and structure to drafting, revisions and design support.", approach)

# ---------------------------------------------------------------- Founder
founder = f"""<section class="hero"><div class="wrap founder">
{PORTRAIT}
<div class="bio">
<h1 style="margin-bottom:24px">Mikhail Seleznev</h1>
<p>Before founding Frisson Writing in 2026, Mikhail spent six years at a leading corporate reporting agency in London and Dubai, leading content development on annual and sustainability reports for companies listed in the GCC and internationally.</p>
<p>His work brings together financial analysis, sustainability reporting and investor messaging. He has interviewed more than 40 board members and senior executives, and those conversations shape every narrative he builds.</p>
<p>He also speaks at industry events, leading workshops and panels at MEIRA conferences and chapter meetings, and has judged the ARC Awards and the MEIRA Reporting Awards.</p>
</div>
</div></section>

<section class="sec-paper"><div class="wrap split">
<div class="stick"><h2>Background</h2></div>
<div>
<dl class="facts" style="margin-top:0">
<div class="cred"><dt><img src="assets/badges/fmva.svg" alt="" width="44" height="44">Financial Modelling and Valuation Analyst (FMVA)</dt><dd>Corporate Finance Institute, 2025</dd></div>
<div class="cred"><dt><img src="assets/badges/cfa.svg" alt="" width="44" height="44">Certificate in Sustainable Investing</dt><dd>CFA Institute, 2021</dd></div>
<div class="cred"><dt><img src="assets/badges/durham.svg" alt="" width="60" height="25">BA in History</dt><dd>Durham University, UK, 2020</dd></div>
<div><dt>Corporate Reporting Consultant</dt><dd>Leading corporate reporting agency, London and Dubai, 2020 to 2026</dd></div>
<div class="cred"><dt><img src="assets/badges/arc.png" alt="" width="60" height="30">Awards judging</dt><dd>ARC Awards 2025 and MEIRA Reporting Awards 2025</dd></div>
<div><dt>Speaking</dt><dd>Workshops and panels at MEIRA conferences and chapter meetings</dd></div>
</dl>
<div class="actions"><a class="btn ghost" href="services.html#competencies">View competencies</a></div>
</div>
</div></section>

<section><div class="wrap split">
<div class="stick"><h2>Exchanges</h2><p class="intro">Experience with companies listed on these exchanges.</p></div>
<div>{exchanges_grid(counts=False, keys=GCC + ["moex"])}</div>
</div></section>
{CTA}"""
page("founder.html", "Founder | Frisson Writing",
     "Mikhail Seleznev founded Frisson Writing after six years in corporate reporting in London and Dubai.", founder)

# ---------------------------------------------------------------- Contact
contact = f"""<section class="hero" style="min-height:62vh"><div class="wrap" style="grid-template-columns:1fr">
<div>
<h1 style="margin-bottom:32px">Discuss your next project</h1>
<a class="mail" href="mailto:{EMAIL}">{EMAIL}</a>
<dl class="contact-list">
<div><dt>Helpful to include</dt><dd>The document type, the deadline and where the content stands today.</dd></div>
<div><dt>Location</dt><dd>Dubai, United Arab Emirates. Available on site across the Gulf.</dd></div>
<div><dt>Company</dt><dd>Frisson Writing LLC, licensed by Shams Free Zone, Sharjah.</dd></div>
</dl>
</div>
</div></section>"""
page("contact.html", "Contact | Frisson Writing", "Contact Frisson Writing about a report, investor presentation or other corporate communications project.", contact)
print("built", N, "projects", dict(ind_count), dict(cap_count), dict(exch_count), dict(type_count))
