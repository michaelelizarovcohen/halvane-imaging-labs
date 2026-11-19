#!/usr/bin/env python3
"""Build the Halvane Imaging Labs static site into docs/.

Usage: python3 build/build_site.py [--skip-previews]

Inputs : data/assets.json, docs/evidence/originals/*, build/content.py, build/worksheet.md
Outputs: docs/**.html, docs/assets/*, docs/evidence/{previews,thumbs}/*, docs/evidence/SHA256SUMS.txt,
         CREDITS.md, manifest.csv
Evidence originals are never written by this script; their SHA-256 is verified against data/assets.json.
"""
import csv, hashlib, html, json, os, re, sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "build"))
import content as C  # noqa: E402

DOCS = os.path.join(ROOT, "docs")
EVID = os.path.join(DOCS, "evidence")
ASSETS = json.load(open(os.path.join(ROOT, "data", "assets.json")))
BY_ID = {a["id"]: a for a in ASSETS}
FOOTER_NOTICE = "Fictional company — OSINT training environment"
RAWISH = {"cr2", "cr3", "crw", "nef", "arw", "raf", "rw2", "orf", "pef", "dng", "x3f", "erf", "dcr", "mrw", "gpr"}
NAV = [("index.html", "Home"), ("about.html", "About"), ("team.html", "Team"), ("services.html", "Services"),
       ("projects/index.html", "Projects"), ("gallery/index.html", "Gallery"), ("news/index.html", "News"),
       ("careers.html", "Careers"), ("media-kit.html", "Media kit"), ("contact.html", "Contact")]


def e(s):
    return html.escape(str(s), quote=True)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024


def write(rel, text):
    p = os.path.join(DOCS, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)


def up(depth):
    return "../" * depth


def fmt_date(s):
    d = date.fromisoformat(s)
    return d.strftime("%-d %B %Y")


# ------------------------------------------------------------------------------------------------ layout
def page(rel, title, body, active="", description=""):
    depth = rel.count("/")
    u = up(depth)
    nav = "".join(
        f'<li><a href="{u}{href}"{" aria-current=\"page\"" if active == href else ""}>{e(label)}</a></li>' for href, label in NAV)
    desc = description or C.COMPANY["short"]
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive, noimageindex">
<meta name="description" content="{e(desc)}">
<title>{e(title)} | {e(C.COMPANY['name'])}</title>
<link rel="icon" href="{u}assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{u}assets/css/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="{u}index.html" aria-label="{e(C.COMPANY['name'])} home"><img src="{u}assets/img/logo.svg" alt="" width="40" height="40"><span><strong>Halvane</strong> Imaging Labs</span></a>
    <button class="nav-toggle" aria-controls="site-nav" aria-expanded="false">Menu</button>
    <nav id="site-nav" aria-label="Main"><ul>{nav}</ul></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <a class="brand brand-footer" href="{u}index.html"><img src="{u}assets/img/logo-light.svg" alt="" width="32" height="32"><span><strong>Halvane</strong> Imaging Labs</span></a>
      <p class="muted">{e(C.COMPANY['tagline'])}. Copenhagen &middot; Florence &middot; Boulder.</p>
    </div>
    <div>
      <h2 class="footer-h">Company</h2>
      <ul class="plain"><li><a href="{u}about.html">About</a></li><li><a href="{u}team.html">Team</a></li><li><a href="{u}careers.html">Careers</a></li><li><a href="{u}contact.html">Contact</a></li></ul>
    </div>
    <div>
      <h2 class="footer-h">Work</h2>
      <ul class="plain"><li><a href="{u}projects/index.html">Projects</a></li><li><a href="{u}gallery/index.html">Gallery</a></li><li><a href="{u}kit-library.html">Field Kit Library</a></li><li><a href="{u}media-kit.html">Media kit</a></li></ul>
    </div>
  </div>
  <div class="wrap footer-note"><a href="{u}lab-notice/index.html">{e(FOOTER_NOTICE)}</a></div>
</footer>
<script src="{u}assets/js/site.js" defer></script>
</body>
</html>
"""


def hero(title, lead, kicker=""):
    k = f'<p class="kicker">{e(kicker)}</p>' if kicker else ""
    return f'<section class="hero"><div class="wrap">{k}<h1>{e(title)}</h1><p class="lead">{e(lead)}</p></div></section>'


def card_asset(a, depth, show_caption=False):
    u = up(depth)
    cap = f'<p class="muted small">{e(a["caption"])}</p>' if show_caption else ""
    return (f'<a class="tile" href="{u}gallery/{a["id"]}.html"><img loading="lazy" src="{u}evidence/thumbs/{a["id"]}.jpg" '
            f'alt="{e(a["title"])}" width="480" height="320"><span class="tile-meta"><span class="id">{a["id"]}</span>'
            f'<span>{e(a["title"])}</span></span>{cap}</a>')


# ------------------------------------------------------------------------------------------------ assets
def avatar_svg(name):
    h = hashlib.sha256(name.encode()).digest()
    palette = ["#0f3b57", "#14716b", "#c4582b", "#5b4a8b", "#2f6f9f", "#8a6d1d", "#a23b52", "#3d6b3a"]
    bg, fg = palette[h[0] % 8], palette[(h[1] % 7 + h[0] % 8 + 1) % 8]
    initials = "".join(p[0] for p in name.split()[:2]).upper()
    shapes = []
    for i in range(3):
        cx, cy, r = 20 + h[2 + i] % 80, 20 + h[5 + i] % 80, 18 + h[8 + i] % 26
        shapes.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fg}" opacity="{0.35 + (h[11 + i] % 30) / 100:.2f}"/>')
    tri = f'<polygon points="{h[14] % 120},120 120,{h[15] % 120} 120,120" fill="#ffffff" opacity="0.12"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" role="img" aria-label="Avatar for {e(name)}">'
            f'<rect width="120" height="120" rx="18" fill="{bg}"/>{"".join(shapes)}{tri}'
            f'<text x="60" y="73" font-family="system-ui,Segoe UI,Helvetica,Arial,sans-serif" font-size="38" font-weight="700" '
            f'text-anchor="middle" fill="#ffffff">{initials}</text></svg>')


LOGO = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Halvane Imaging Labs">
<rect width="64" height="64" rx="14" fill="{bg}"/>
<path d="M32 9 51.9 20.5v23L32 55 12.1 43.5v-23Z" fill="none" stroke="{fg}" stroke-width="3.2" stroke-linejoin="round"/>
<path d="M22 21v22M42 21v22" stroke="{fg}" stroke-width="4" stroke-linecap="round"/>
<path d="M14 33.5c4.5-3 9-3 13.5 0s9 3 13.5 0 6.8-2.6 9 -1.4" fill="none" stroke="{accent}" stroke-width="3.4" stroke-linecap="round"/>
</svg>"""


def write_static():
    write("assets/img/logo.svg", LOGO.format(bg="#0f2d44", fg="#ffffff", accent="#3fc1b0"))
    write("assets/img/logo-light.svg", LOGO.format(bg="#ffffff", fg="#0f2d44", accent="#14716b"))
    write("assets/img/favicon.svg", LOGO.format(bg="#0f2d44", fg="#ffffff", accent="#3fc1b0"))
    for p in C.PEOPLE:
        write(f"assets/img/avatars/{p['slug']}.svg", avatar_svg(p["name"]))
    write(".nojekyll", "")
    write("robots.txt", "# Fictional training site. Indexing controls are not access controls.\nUser-agent: *\nDisallow: /\n")


# ------------------------------------------------------------------------------------------------ previews
def build_previews(skip):
    import previews as P
    cache_p = os.path.join(ROOT, "data", "preview_cache.json")
    cache = json.load(open(cache_p)) if os.path.exists(cache_p) else {}
    made = 0
    for a in ASSETS:
        src = os.path.join(EVID, "originals", a["file"])
        pv, th = os.path.join(EVID, "previews", a["id"] + ".jpg"), os.path.join(EVID, "thumbs", a["id"] + ".jpg")
        if cache.get(a["id"]) == a["sha256"] and os.path.exists(pv) and os.path.exists(th):
            continue
        if skip:
            raise SystemExit(f"preview missing/stale for {a['id']} and --skip-previews given")
        P.render(src, [(pv, 1600, 84), (th, 480, 78)])
        cache[a["id"]] = a["sha256"]
        made += 1
    json.dump(cache, open(cache_p, "w"), indent=1, sort_keys=True)
    return made


# ------------------------------------------------------------------------------------------------ pages
def build_home():
    feat = ["HIL-2501", "HIL-1118", "HIL-1104", "HIL-1309", "HIL-1413", "HIL-1214"]
    tiles = "".join(card_asset(BY_ID[i], 0) for i in feat)
    news = sorted(C.NEWS, key=lambda n: n["date"], reverse=True)[:4]
    news_html = "".join(f'<li><time datetime="{n["date"]}">{fmt_date(n["date"])}</time><a href="news/{n["slug"]}.html">{e(n["title"])}</a></li>' for n in news)
    svc = "".join(f'<div class="card"><h3>{e(s["name"])}</h3><p>{e(s["text"])}</p></div>' for s in C.SERVICES[:3])
    body = f"""
<section class="hero hero-home"><div class="wrap hero-grid">
  <div><p class="kicker">Independent since {C.COMPANY['founded']}</p>
  <h1>{e(C.COMPANY['tagline'])}.</h1>
  <p class="lead">{e(C.COMPANY['short'])}</p>
  <p class="actions"><a class="btn" href="services.html">What we do</a> <a class="btn btn-ghost" href="gallery/index.html">Browse the archive</a></p></div>
  <div class="hero-figure"><img src="evidence/previews/HIL-1104.jpg" alt="Fjord walls from a coastal ferry" width="800" height="533"></div>
</div></section>
<section class="wrap section"><h2>Services</h2><div class="grid3">{svc}</div><p><a href="services.html">All services &rarr;</a></p></section>
<section class="band"><div class="wrap section"><h2>From the archive</h2><div class="tiles">{tiles}</div><p><a href="gallery/index.html">Open the gallery &rarr;</a></p></div></section>
<section class="wrap section two-col">
  <div><h2>Latest news</h2><ul class="news-list">{news_html}</ul><p><a href="news/index.html">All news &rarr;</a></p></div>
  <div><h2>Where we work</h2>{"".join(f'<div class="office"><h3>{e(o["city"])}</h3><p>{e(o["role"])}</p><p class="muted small">{e(o["detail"])}</p></div>' for o in C.OFFICES)}</div>
</section>"""
    write("index.html", page("index.html", "Home", body, "index.html"))


def build_about():
    tl = [("2003", "Maren Halvik and Teodor Vane start testing cameras from a kitchen table in Copenhagen. Teodor's western Norway road trip produces the first Archive Zero frames."),
          ("2006", "Halvane Imaging Labs ApS is incorporated. First paying clients: two picture agencies and a museum."),
          ("2010", "Felix Brandauer joins; the Alpine & Nordic Light Programme begins with a glacial-lake colour study."),
          ("2012", "Grace Adeyemi introduces the Field Kit Library: every checkout logged against a name and date."),
          ("2014", "Kenji Moriwaki builds the colour bench. Felix crosses the Inside Passage with a wide zoom."),
          ("2015", "The Florence Mobile Imaging Lab opens under Lucia Ferrante; the Smartphone Field Panel begins."),
          ("2016", "Dana Whitlock opens the Boulder office for aerial and action systems."),
          ("2019", "Move to the Nordhavn studio. Ingest 3.0 stamps the workstation into every file's edit history."),
          ("2021", "Provenance & Metadata Assurance becomes a service, led by Amara Osei."),
          ("2025", "TIDEMARK-25 field week for Fellstrand Mutual (May). Internal review of the report imagery opens in October."),
          ("2026", "The Field Kit Library register is made public.")]
    items = "".join(f'<li><span class="year">{y}</span><p>{e(t)}</p></li>' for y, t in tl)
    body = hero("About Halvane", "We test imaging hardware where it is actually used - and we publish the files so you can check our work.", "Company") + f"""
<section class="wrap section two-col">
  <div><h2>What we believe</h2>
  <p>A camera review that cannot be checked is an opinion. Since {C.COMPANY['founded']} Halvane has shipped every evaluation with the files behind it,
  untouched, so that clients can verify capture times, devices and settings for themselves.</p>
  <p>That habit grew into a second discipline: reading what files say about themselves. Today our Provenance &amp; Metadata Assurance
  practice audits imagery for newsrooms, insurers and legal teams.</p>
  <h2>Founders</h2>
  <p><a href="team.html#maren-halvik">Maren Halvik</a> and <a href="team.html#teodor-vane">Teodor Vane</a> met as camera service engineers.
  The company name is half of each surname.</p></div>
  <div><h2>Offices</h2>{"".join(f'<div class="office"><h3>{e(o["city"])}, {e(o["country"])}</h3><p>{e(o["role"])} &middot; since {o["since"]}</p><p class="muted small">{e(o["detail"])}</p></div>' for o in C.OFFICES)}</div>
</section>
<section class="band"><div class="wrap section"><h2>Timeline</h2><ol class="timeline">{items}</ol></div></section>"""
    write("about.html", page("about.html", "About", body, "about.html"))


def build_team():
    cards = "".join(
        f'<article class="person" id="{p["slug"]}"><img src="assets/img/avatars/{p["slug"]}.svg" alt="" width="96" height="96">'
        f'<div><h2>{e(p["name"])}</h2><p class="role">{e(p["role"])}</p><p class="muted small">{e(p["office"])} &middot; joined {p["since"]}</p>'
        f'<p>{e(p["bio"])}</p><ul class="chips">{"".join(f"<li>{e(f)}</li>" for f in p["focus"])}</ul></div></article>' for p in C.PEOPLE)
    alumni = "".join(f'<li><strong>{e(a["name"])}</strong> &mdash; {e(a["role"])}. <span class="muted">{e(a["note"])}</span></li>' for a in C.ALUMNI)
    body = hero("Team", "Engineers, scientists and one very patient librarian across three offices.", "People") + f"""
<section class="wrap section"><div class="people">{cards}</div>
<h2>Alumni and interns</h2><ul class="alumni">{alumni}</ul>
<p class="muted small">Portraits are illustrations; we do not publish staff photographs.</p></section>"""
    write("team.html", page("team.html", "Team", body, "team.html"))


def build_services():
    blocks = "".join(f'<article class="card" id="{s["slug"]}"><h2>{e(s["name"])}</h2><p>{e(s["text"])}</p></article>' for s in C.SERVICES)
    body = hero("Services", "Five practices, one rule: the files ship with the findings.", "What we do") + f"""
<section class="wrap section"><div class="grid2">{blocks}</div>
<div class="callout"><h2>How an engagement works</h2><ol><li>Scoping call and kit list (drawn from the <a href="kit-library.html">Field Kit Library</a>).</li>
<li>Field and bench capture, logged per device and per day.</li><li>Ingest on a named workstation; edit history preserved in every file.</li>
<li>Report with figures, plus the original files and their SHA-256 checksums.</li></ol></div></section>"""
    write("services.html", page("services.html", "Services", body, "services.html"))


def build_projects():
    cards = "".join(
        f'<article class="card project-card"><p class="kicker">{e(p["years"])} &middot; {e(p["status"])}</p><h2><a href="{p["slug"]}.html">{e(p["name"])}</a></h2>'
        f'<p>{e(p["summary"])}</p><p class="muted small">Lead: {e(p["lead"])} &middot; {sum(1 for a in ASSETS if a["project"] == p["slug"])} files</p></article>' for p in C.PROJECTS)
    body = hero("Projects", "Long-running programmes and client evaluations, each with its published files.", "Portfolio") + f'<section class="wrap section"><div class="grid2">{cards}</div></section>'
    write("projects/index.html", page("projects/index.html", "Projects", body, "projects/index.html"))
    for p in C.PROJECTS:
        files = [a for a in ASSETS if a["project"] == p["slug"]]
        if p["slug"] == "tidemark-25":
            rows = "".join(f'<tr><td>{e(a["title"].replace("TIDEMARK-25 ", ""))}</td><td><a href="../gallery/{a["id"]}.html">{a["id"]}</a></td>'
                           f'<td>{e(a["caption"])}</td><td><a href="../evidence/originals/{a["file"]}" download>{e(a["file"])}</a></td></tr>'
                           for a in sorted(files, key=lambda x: x["title"]))
            extra = f"""<h2>Report figures as delivered</h2><div class="table-wrap"><table><thead><tr><th>Figure</th><th>Asset</th><th>Caption in report</th><th>Original file</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="muted small">Client: {e(p.get("client", ""))}. Field week: 5-9 May 2025. Report v1: 30 May 2025. Report v2: 20 June 2025.
See also <a href="../news/2025-10-tidemark-statement.html">the statement of 28 October 2025</a> and the <a href="../kit-library.html">Field Kit Library</a>.</p>"""
        else:
            extra = ""
        tiles = "".join(card_asset(a, 1, show_caption=False) for a in files)
        body = hero(p["name"], p["summary"], f'{p["years"]} · {p["status"]}') + f"""
<section class="wrap section two-col"><div>{"".join(f"<p>{e(x)}</p>" for x in p["body"])}</div>
<aside class="card"><dl class="facts"><dt>Lead</dt><dd>{e(p["lead"])}</dd><dt>Years</dt><dd>{e(p["years"])}</dd><dt>Status</dt><dd>{e(p["status"])}</dd>{f'<dt>Client</dt><dd>{e(p["client"])}</dd>' if p.get("client") else ""}<dt>Files</dt><dd>{len(files)}</dd></dl></aside></section>
<section class="wrap section">{extra}<h2>Files</h2><div class="tiles">{tiles}</div></section>"""
        write(f"projects/{p['slug']}.html", page(f"projects/{p['slug']}.html", p["name"], body, "projects/index.html", p["summary"]))


def build_gallery():
    data = [dict(id=a["id"], t=a["title"], c=a["caption"], s=a["section"], p=a["project"], x=a["ext"], f=a["file"]) for a in ASSETS]
    sections = sorted({a["section"] for a in ASSETS})
    secbtn = "".join(f'<option value="{e(s)}">{e(s)}</option>' for s in sections)
    exts = sorted({a["ext"] for a in ASSETS})
    extopt = "".join(f'<option value="{x}">.{x}</option>' for x in exts)
    tiles = "".join(f'<div class="g-item" data-id="{a["id"]}">{card_asset(a, 1)}</div>' for a in ASSETS)
    body = hero("Gallery", f"{len(ASSETS)} files from our archive, published byte-for-byte as delivered. Previews are resized copies; download the original for analysis.", "Archive") + f"""
<section class="wrap section">
<form class="filters" role="search" onsubmit="return false">
  <label>Search <input type="search" id="q" placeholder="ID, title or caption"></label>
  <label>Section <select id="sec"><option value="">All sections</option>{secbtn}</select></label>
  <label>Format <select id="fmt"><option value="">All formats</option><option value="__raw">RAW formats</option>{extopt}</select></label>
  <p class="muted small" id="count" aria-live="polite"></p>
</form>
<div class="tiles" id="gallery">{tiles}</div>
<script id="gallery-data" type="application/json">{json.dumps(data, ensure_ascii=False).replace("</", "<\\/")}</script>
</section>"""
    write("gallery/index.html", page("gallery/index.html", "Gallery", body, "gallery/index.html"))
    for a in ASSETS:
        proj = next((p for p in C.PROJECTS if p["slug"] == a["project"]), None)
        cr = a["credit"]
        plink = f'<a href="../projects/{proj["slug"]}.html">{e(proj["name"])}</a>' if proj else e(a["section"])
        kind = "RAW image" if a["ext"] in RAWISH else ("HEIF image" if a["ext"] in ("heic", "heif") else "JPEG image")
        attrib = (f'{e(cr["author"])} &mdash; <a href="{e(cr["license_url"])}" rel="license noopener">{e(cr["license"])}</a>. Metadata adapted for this training environment.'
                  if "BY-SA" in cr["license"] else f'{e(cr["collection"])} &mdash; {e(cr["license"])}.')
        body = f"""
<section class="wrap section asset">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Gallery</a> / {e(a["section"])} / {a["id"]}</nav>
  <div class="asset-grid">
    <figure><img src="../evidence/previews/{a["id"]}.jpg" alt="{e(a["title"])}"><figcaption class="muted small">Preview: resized JPEG without metadata. Use the original for analysis.</figcaption></figure>
    <div>
      <p class="kicker">{a["id"]}</p><h1>{e(a["title"])}</h1><p>{e(a["caption"])}</p>
      <p><a class="btn" href="../evidence/originals/{a["file"]}" download>Download original ({e(a["ext"].upper())}, {human(a["file_size"])})</a></p>
      <dl class="facts"><dt>Collection</dt><dd>{plink}</dd><dt>File</dt><dd><code>{e(a["file"])}</code></dd><dt>Type</dt><dd>{kind} ({e(a["file_type"])})</dd>
      <dt>Pixels</dt><dd>{e(a["dimensions"])}</dd><dt>Size</dt><dd>{a["file_size"]:,} bytes</dd><dt>SHA-256</dt><dd><code class="hash">{a["sha256"]}</code></dd>
      <dt>Licence</dt><dd>{attrib} <a href="../lab-notice/index.html#credits">Full attribution</a></dd></dl>
    </div>
  </div>
</section>"""
        write(f"gallery/{a['id']}.html", page(f"gallery/{a['id']}.html", f"{a['id']} {a['title']}", body, "gallery/index.html", a["caption"]))


def build_news():
    posts = sorted(C.NEWS, key=lambda n: n["date"], reverse=True)
    items = "".join(f'<article class="news-item"><time datetime="{n["date"]}">{fmt_date(n["date"])}</time><h2><a href="{n["slug"]}.html">{e(n["title"])}</a></h2>'
                    f'<p class="muted small">By {e(n["author"])}</p><p>{e(n["body"][0][:180])}{"..." if len(n["body"][0]) > 180 else ""}</p></article>' for n in posts)
    body = hero("News", "Announcements, field notes and statements from Halvane.", "Newsroom") + f'<section class="wrap section narrow">{items}</section>'
    write("news/index.html", page("news/index.html", "News", body, "news/index.html"))
    for i, n in enumerate(posts):
        imgs = "".join(card_asset(BY_ID[x], 1, show_caption=True) for x in n["images"])
        person = next((p for p in C.PEOPLE if p["name"] == n["author"]), None)
        by = f'<a href="../team.html#{person["slug"]}">{e(n["author"])}</a>' if person else e(n["author"])
        prev_ = f'<a href="{posts[i + 1]["slug"]}.html">&larr; {e(posts[i + 1]["title"])}</a>' if i + 1 < len(posts) else ""
        next_ = f'<a href="{posts[i - 1]["slug"]}.html">{e(posts[i - 1]["title"])} &rarr;</a>' if i > 0 else ""
        body = f"""<article class="wrap section narrow post"><p class="kicker"><time datetime="{n["date"]}">{fmt_date(n["date"])}</time></p><h1>{e(n["title"])}</h1>
<p class="muted">By {by}</p>{"".join(f"<p>{e(x)}</p>" for x in n["body"])}
{f'<div class="tiles">{imgs}</div>' if imgs else ""}<nav class="pager">{prev_}<span></span>{next_}</nav></article>"""
        write(f"news/{n['slug']}.html", page(f"news/{n['slug']}.html", n["title"], body, "news/index.html", n["body"][0][:150]))


def build_careers():
    jobs = "".join(f'<article class="card"><p class="kicker">{e(j["office"])} &middot; {e(j["type"])}</p><h2>{e(j["title"])}</h2><p>{e(j["text"])}</p>'
                   f'<p class="muted small">To apply, email <code>jobs@halvane.example</code> with the role title in the subject line.</p></article>' for j in C.CAREERS)
    body = hero("Careers", "Small teams, real field work, and files you can stand behind.", "Join us") + f"""
<section class="wrap section two-col"><div><div class="grid1">{jobs}</div></div>
<aside>{card_asset(BY_ID["HIL-1505"], 0, show_caption=True)}<div class="card"><h3>Life at Halvane</h3><p>Four-day field weeks, a lending library of more cameras than anyone needs,
and a team that argues about white balance at lunch.</p></div></aside></section>"""
    write("careers.html", page("careers.html", "Careers", body, "careers.html"))


def build_media_kit():
    body = hero("Media kit", "Logos, boilerplate and approved images for press use.", "Press") + f"""
<section class="wrap section two-col"><div>
<h2>Boilerplate</h2><p>{e(C.COMPANY["name"])} is an independent evaluation lab for cameras, phones and aerial imaging systems, founded in
Copenhagen in {C.COMPANY["founded"]}, with labs in Florence and Boulder. Halvane publishes the original files behind every evaluation and runs a
Provenance &amp; Metadata Assurance practice for newsrooms, insurers and legal teams.</p>
<h2>Brand</h2><ul class="swatches"><li style="--c:#0f2d44">Harbour navy #0F2D44</li><li style="--c:#14716b">Tidemark teal #14716B</li><li style="--c:#3fc1b0">Signal aqua #3FC1B0</li><li style="--c:#c4582b">Field orange #C4582B</li></ul>
<p>The mark combines a hexagonal aperture, the H of Halvane and a tide line.</p>
<h2>Approved images</h2><p>Use the originals from the gallery pages below; please credit &ldquo;Halvane Imaging Labs&rdquo; and respect the licence shown on each page.</p>
<div class="tiles">{"".join(card_asset(BY_ID[i], 0) for i in ["HIL-1118", "HIL-1309", "HIL-1413"])}</div>
<h2>Press contact</h2><p>Rosa Quintero, Communications &amp; Media &middot; <code>{e(C.COMPANY["press"])}</code></p></div>
<aside class="card"><h3>Logos</h3><p><img src="assets/img/logo.svg" alt="Halvane mark on navy" width="96" height="96"> <img src="assets/img/logo-light.svg" alt="Halvane mark on white" width="96" height="96" class="bordered"></p>
<ul class="plain"><li><a href="assets/img/logo.svg" download>logo.svg</a> (navy)</li><li><a href="assets/img/logo-light.svg" download>logo-light.svg</a> (white)</li></ul></aside></section>"""
    write("media-kit.html", page("media-kit.html", "Media kit", body, "media-kit.html"))


def build_contact():
    offs = "".join(f'<div class="card"><h2>{e(o["city"])}</h2><p>{e(o["role"])}</p><p class="muted small">{e(o["detail"])}</p>'
                   f'<p>Email: <code>{e(o["email"])}</code>{"<br>Phone: " + e(o["phone"]) if o["phone"] else ""}</p></div>' for o in C.OFFICES)
    body = hero("Contact", "We read every message. We do not run contact forms, newsletters by stealth or tracking pixels.", "Get in touch") + f"""
<section class="wrap section"><div class="grid3">{offs}</div>
<p class="muted small">Addresses ending in <code>.example</code> and numbers in the 555-01xx range are reserved for fictional use and do not reach anyone.
This site collects no visitor data.</p></section>"""
    write("contact.html", page("contact.html", "Contact", body, "contact.html"))


def build_kit():
    rows = ""
    for tag, item, serial, holders, note in C.KIT:
        hs = "<br>".join(f"{e(h)}: {e(a)} &rarr; {e(b)}" for h, a, b in holders)
        rows += f"<tr><td>{tag}</td><td>{e(item)}</td><td><code>{e(serial)}</code></td><td>{hs}</td><td>{e(note)}</td></tr>"
    body = hero("Field Kit Library", "Every body that appears in published work, the last characters of its serial and who held it when.", "Register") + f"""
<section class="wrap section"><p>{e(C.WORKSTATIONS_NOTE)}</p>
<div class="table-wrap"><table class="kit"><thead><tr><th>Tag</th><th>Item</th><th>Serial (last 5)</th><th>Holder history</th><th>Notes</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="muted small">Dates are inclusive check-out and check-in dates (Copenhagen time). Phones and tablets under evaluation are not library kit and are not listed.
Register published 3 March 2026.</p></section>"""
    write("kit-library.html", page("kit-library.html", "Field Kit Library", body, ""))


def md_to_html(md):
    """Minimal Markdown subset: headings, paragraphs, lists, tables, code spans/blocks, bold, links."""
    out, lines, i = [], md.splitlines(), 0

    def inline(s):
        s = e(s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
        return s
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            out.append("<pre><code>" + e("\n".join(lines[i + 1:j])) + "</code></pre>")
            i = j + 1
            continue
        m = re.match(r"(#{1,4}) (.*)", ln)
        if m:
            lvl = len(m.group(1)) + (0 if len(m.group(1)) > 1 else 0)
            slug = re.sub(r"[^a-z0-9]+", "-", m.group(2).lower()).strip("-")
            out.append(f'<h{lvl} id="{slug}">{inline(m.group(2))}</h{lvl}>')
        elif ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip("|").split("|")])
                i += 1
            head, body_rows = rows[0], [r for r in rows[2:]]
            out.append('<div class="table-wrap"><table><thead><tr>' + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body_rows) + "</tbody></table></div>")
            continue
        elif re.match(r"^(\s*)([-*]|\d+\.) ", ln):
            tag = "ol" if re.match(r"^\s*\d+\.", ln) else "ul"
            items = []
            while i < len(lines) and re.match(r"^(\s*)([-*]|\d+\.) ", lines[i]):
                items.append(re.sub(r"^\s*([-*]|\d+\.) ", "", lines[i]))
                i += 1
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
            continue
        elif ln.strip():
            para = [ln]
            while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r"^(#|\||```|\s*([-*]|\d+\.) )", lines[i + 1]):
                i += 1
                para.append(lines[i])
            out.append("<p>" + inline(" ".join(para)) + "</p>")
        i += 1
    return "\n".join(out)


def build_lab_notice():
    by_coll = {}
    for a in ASSETS:
        by_coll.setdefault(a["credit"]["collection"], []).append(a)
    rows = "".join(
        f'<tr><td><a href="../gallery/{a["id"]}.html">{a["id"]}</a></td><td>{e(a["credit"]["collection"])}</td><td><code>{e(a["credit"]["original_name"])}</code></td>'
        f'<td>{e(a["credit"]["author"])}</td><td><a href="{e(a["credit"]["license_url"])}" rel="license noopener">{e(a["credit"]["license"])}</a></td>'
        f'<td><a href="{e(a["credit"]["source_url"])}" rel="noopener">source</a></td></tr>' for a in ASSETS)
    counts = ", ".join(f"{k}: {len(v)}" for k, v in sorted(by_coll.items()))
    body = hero("Lab notice", "Halvane Imaging Labs is a fictional company. This website is an OSINT and digital-forensics training environment.", "Read me first") + f"""
<section class="wrap section narrow">
<h2>What this site is</h2>
<p>Every person, office address, project, client, workstation, register entry and announcement on this site is invented for teaching. The people
have no connection to any real individual, and Halvane, Fellstrand Mutual and the European Imaging Assurance Forum are not real organisations.
Staff portraits are generated geometric illustrations.</p>
<p>The photographs are real files made by real cameras, contributed to public test collections under open licences (listed below). They show
real, public places. Their authentic camera metadata is largely preserved; for the training scenario, descriptive and other metadata in some
files from every collection has been added or edited. Do not treat any in-world statement on this site, or any embedded description, owner,
copyright or history field, as a fact about the real photographers.</p>
<h2>How to use the evidence</h2>
<ul><li>Each gallery page links to the <strong>original file</strong> under <code>evidence/originals/</code>. These are the investigation files; they are served
byte-for-byte as published. Check them against <a href="../evidence/SHA256SUMS.txt">SHA256SUMS.txt</a>.</li>
<li>Previews and thumbnails are resized JPEG derivatives with <strong>no metadata</strong>. Never analyse a preview.</li>
<li>Recommended tool: <a href="https://exiftool.org/" rel="noopener">ExifTool</a>, for example <code>exiftool -a -G1 -s FILE</code>.</li>
<li>Exercises are listed on the <a href="worksheet.html">student worksheet</a>. Work from the published files and pages. Comparing files with upstream
originals from the source collections is outside the intended scope of the exercises.</li></ul>
<h2>What this site does not do</h2>
<p>No contact forms, accounts, payments, analytics, cookies, trackers or third-party scripts. Email addresses use the reserved <code>.example</code> domain.
<code>robots.txt</code> disallows crawling and every page carries a <code>noindex</code> directive; these are indexing requests, not access controls.</p>
<h2 id="licences">Sources and licences</h2>
<p>Published files by collection &mdash; {e(counts)}.</p>
<ul>
<li><strong>raw.pixls.us</strong> &mdash; individually verified CC0 1.0 samples (<a href="https://raw.pixls.us/" rel="noopener">raw.pixls.us</a>). No attribution required; credited as a courtesy.</li>
<li><strong>Immich test-assets</strong> &mdash; the repository README states that all assets are public domain; the repository itself is licensed AGPL-3.0
(<a href="https://github.com/immich-app/test-assets" rel="noopener">github.com/immich-app/test-assets</a>). Where AGPL-3.0 applies, each file's corresponding source is the
file itself, served here unmodified in pixel content; files with edited metadata are listed with this notice.</li>
<li><strong>metadata-extractor-images</strong> &mdash; README: &ldquo;You are free to use these media files however you wish.&rdquo; Only files with a traceable contributor
commit are used (<a href="https://github.com/drewnoakes/metadata-extractor-images" rel="noopener">github.com/drewnoakes/metadata-extractor-images</a>).</li>
<li><strong>ianare/exif-samples</strong> &mdash; user-contributed images released under CC BY-SA 4.0; files by Antti Ketola (<a href="https://github.com/ianare/exif-samples" rel="noopener">github.com/ianare/exif-samples</a>).
Changes: rights and descriptive XMP metadata added; pixel data unchanged. Adapted files are licensed CC BY-SA 4.0.</li>
<li><strong>VISION dataset</strong> &mdash; &copy; CSP Lab, Dept. of Information Engineering, University of Florence, 2017, licensed CC BY-SA 4.0
(<a href="https://lesc.dinfo.unifi.it/VISION/" rel="noopener">lesc.dinfo.unifi.it/VISION</a>). Only original images from the <code>nat</code> folders are used.
Changes: rights and descriptive XMP metadata added; pixel data unchanged. Adapted files are licensed CC BY-SA 4.0.
Citation: D. Shullani, M. Fontani, M. Iuliani, O. Al Shaya, A. Piva, &ldquo;VISION: a video and image dataset for source identification,&rdquo;
<em>EURASIP Journal on Information Security</em>, 2017:15, 2017. <a href="https://doi.org/10.1186/s13635-017-0067-2" rel="noopener">doi:10.1186/s13635-017-0067-2</a>.</li>
<li><strong>ExifTool Meta Information Repository</strong> &mdash; used only as an external reference; nothing from it is hosted here
(<a href="https://exiftool.org/sample_images.html" rel="noopener">exiftool.org/sample_images.html</a>).</li></ul>
<p>Licence texts: <a href="https://creativecommons.org/publicdomain/zero/1.0/" rel="license noopener">CC0 1.0</a>,
<a href="https://creativecommons.org/licenses/by-sa/4.0/" rel="license noopener">CC BY-SA 4.0</a>, <a href="https://www.gnu.org/licenses/agpl-3.0.html" rel="license noopener">AGPL-3.0</a>.
The licensors provide the material as-is, without warranties. Site code and text are released under CC BY-SA 4.0.</p>
<h2 id="credits">Per-file attribution</h2>
<div class="table-wrap"><table class="credits"><thead><tr><th>Asset</th><th>Collection</th><th>Original file name</th><th>Author / contributor</th><th>Licence</th><th>Source</th></tr></thead><tbody>{rows}</tbody></table></div>
</section>"""
    write("lab-notice/index.html", page("lab-notice/index.html", "Lab notice", body, ""))
    md = open(os.path.join(ROOT, "build", "worksheet.md"), encoding="utf-8").read()
    write("lab-notice/worksheet.html", page("lab-notice/worksheet.html", "Student worksheet",
                                            f'<section class="wrap section narrow worksheet">{md_to_html(md)}</section>', ""))


def build_404():
    body = hero("Page not found", "That page is not in the archive. Try the gallery or the news index.", "404")
    html_ = page("404.html", "Not found", body, "").replace("<head>\n", '<head>\n<base href="/halvane-imaging-labs/">\n', 1)
    write("404.html", html_)


# ------------------------------------------------------------------------------------------------ public manifests
def build_manifests():
    with open(os.path.join(EVID, "SHA256SUMS.txt"), "w") as f:
        for a in ASSETS:
            f.write(f"{a['sha256']}  originals/{a['file']}\n")
    with open(os.path.join(ROOT, "manifest.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["filename", "published_path", "source_collection", "source_url", "original_filename", "license", "license_tier",
                    "format", "dimensions", "file_size_bytes", "sha256", "metadata_available", "intended_usage"])
        for a in ASSETS:
            cr = a["credit"]
            w.writerow([a["file"], f"docs/evidence/originals/{a['file']}", cr["collection"], cr["source_url"], cr["original_name"],
                        cr["license"], "PUBLIC", a["file_type"], a["dimensions"], a["file_size"], a["sha256"],
                        "EXIF/MakerNotes; XMP/IPTC where present", f"investigation evidence; {a['section']}"])
    lines = ["# Credits and attribution", "",
             "Halvane Imaging Labs is a **fictional company**. This repository is an OSINT / digital-forensics training environment.", "",
             "All photographs are real files from open test collections. Metadata in some files has been added or edited for the training",
             "scenario; pixel data is unchanged. Previews under `docs/evidence/previews` and `thumbs` are resized derivatives without metadata.", "",
             "## Collections", "",
             "- **raw.pixls.us** - CC0 1.0 samples, individually verified. https://raw.pixls.us/",
             "- **Immich test-assets** - README: all assets are public domain; repository licence AGPL-3.0. https://github.com/immich-app/test-assets",
             "- **metadata-extractor-images** - README: \"You are free to use these media files however you wish.\" https://github.com/drewnoakes/metadata-extractor-images",
             "- **ianare/exif-samples** - user contributions under CC BY-SA 4.0 (files by Antti Ketola). Changes: rights/descriptive XMP added. https://github.com/ianare/exif-samples",
             "- **VISION dataset** - (c) CSP Lab, Dept. of Information Engineering, University of Florence, 2017, CC BY-SA 4.0. Changes: rights/descriptive XMP added.",
             "  Cite: D. Shullani, M. Fontani, M. Iuliani, O. Al Shaya, A. Piva, \"VISION: a video and image dataset for source identification\",",
             "  EURASIP Journal on Information Security, 2017. doi:10.1186/s13635-017-0067-2. https://lesc.dinfo.unifi.it/VISION/",
             "- **ExifTool Meta Information Repository** - external reference only; nothing rehosted. https://exiftool.org/sample_images.html", "",
             "Adapted CC BY-SA files are licensed CC BY-SA 4.0. Site code and original text: CC BY-SA 4.0.", "",
             "## Per-file attribution", "", "| Asset | Collection | Original file | Author / contributor | Licence | Source |", "|---|---|---|---|---|---|"]
    for a in ASSETS:
        cr = a["credit"]
        lines.append(f"| {a['id']} | {cr['collection']} | `{cr['original_name']}` | {cr['author']} | {cr['license']} | {cr['source_url']} |")
    open(os.path.join(ROOT, "CREDITS.md"), "w").write("\n".join(lines) + "\n")


def verify_originals():
    bad = []
    for a in ASSETS:
        p = os.path.join(EVID, "originals", a["file"])
        if not os.path.exists(p) or sha256(p) != a["sha256"]:
            bad.append(a["file"])
    if bad:
        raise SystemExit(f"evidence integrity failure: {bad}")
    extra = set(os.listdir(os.path.join(EVID, "originals"))) - {a["file"] for a in ASSETS}
    if extra:
        raise SystemExit(f"unexpected files in originals/: {sorted(extra)}")


def main():
    skip = "--skip-previews" in sys.argv
    verify_originals()
    write_static()
    made = build_previews(skip)
    build_home(); build_about(); build_team(); build_services(); build_projects(); build_gallery(); build_news()
    build_careers(); build_media_kit(); build_contact(); build_kit(); build_lab_notice(); build_404(); build_manifests()
    verify_originals()
    print(f"built site: {len(ASSETS)} assets, {made} previews regenerated")


if __name__ == "__main__":
    main()
