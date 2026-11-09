# -*- coding: utf-8 -*-
"""English (/en/) pages for nuhal.ae. Called from build.py with the Arabic build module."""
import json, os, re, html
from content_en import *

esc = lambda s: html.escape(str(s), quote=True)
MONTHS_EN = {10: "Oct", 11: "Nov", 12: "Dec"}
MONTHS_FULL = {10: "October", 11: "November", 12: "December"}
DAYS_EN = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
ST_EN = {"open": ("st-open", "Open for registration"), "live": ("st-live", "In progress"), "done": ("st-done", "Completed")}
B = None
PAGES_EN = []

def ic(n, cls=""): return f'<i data-lucide="{n}"' + (f' class="{cls}"' if cls else "") + "></i>"
def href(rel, path): return (rel + path) or "./"
def tr_en(k): return TRACKS_EN[k]
def ar_en(c): return CITY_EN[c]
def t_en(it): return TITLES_EN[it["id"]]
def date_txt(it): return f'{it["d1"]}–{it["d2"]} {MONTHS_FULL[it["m"]]} 2026'
def join_en(lst): return lst[0] if len(lst) == 1 else ", ".join(lst[:-1]) + " and " + lst[-1]
def cities_en(k): return [ar_en(c) for c in B.cities_of(k)]

def img(rel, name, alt, lazy=True, cls=""):
    w, h = B.IMG_SIZES[name]
    extra = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return f'<img src="{rel}assets/img/{name}.jpg" alt="{esc(alt)}" width="{w}" height="{h}"{extra}' + (f' class="{cls}"' if cls else "") + ">"

def pill(it):
    c, l = ST_EN[B.status(it)]
    return f'<span class="pill {c}" data-st="{it["id"]}">{l}</span>'

def chip(tr):
    T = B.TRACKS[tr]; E = tr_en(tr)
    return f'<span class="chip"><span class="leaf t-{T["t"]}">{ic(T["i"])}</span>{esc(E["s"])}</span>'

def pcard(it, with_chip=True):
    T = B.TRACKS[it["tr"]]; st = B.status(it)
    return (f'<article class="pcard{" done" if st == "done" else ""}" id="p-{it["id"]}" data-tr="{it["tr"]}" data-city="{esc(it["c"])}" data-month="{it["m"]}" data-status="{st}" style="--tone:{B.TONE[T["t"]]}">'
            f'<div class="r1"><div class="dstamp"><b>{it["d1"]}–{it["d2"]}</b><span>{MONTHS_FULL[it["m"]]} 2026</span></div>{pill(it)}</div>'
            f'{chip(it["tr"]) if with_chip else ""}<h3>{esc(t_en(it))}</h3>'
            f'<div class="r3"><span class="city">{ic("map-pin")} {ar_en(it["c"])}</span><button class="btn btn-line btn-sm" type="button" data-open="{it["id"]}">Details &amp; registration {ic("arrow-right")}</button></div></article>')

def lrow(it):
    return (f'<div class="lrow"><div class="dstamp"><b>{it["d1"]}–{it["d2"]}</b><span>{MONTHS_EN[it["m"]]} · {DAYS_EN[it["start"].weekday()]}</span></div>'
            f'<h3>{esc(t_en(it))}</h3>{chip(it["tr"])}<span class="city">{ic("map-pin")} {ar_en(it["c"])}</span>'
            f'<div class="act"><button class="btn btn-line btn-sm" type="button" data-open="{it["id"]}">Register {ic("arrow-right")}</button></div></div>')

def faq_html(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{esc(q)} {ic("plus")}</summary><p>{esc(a)}</p></details>' for q, a in faqs) + "</div>"

def sec_head(kicker, h2, lead="", link=""):
    lp = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<div class="sec-head"><div><span class="kicker">{kicker}</span><h2 class="h2">{h2}</h2>{lp}</div>{link}</div>'

def side(*pairs): return "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in pairs)

def phero(rel, crumbs, h1, lead, sd=""):
    cr = f'<a href="{href(rel, "")}">Home</a>'
    for name, path in crumbs[:-1]:
        cr += f'{ic("chevron-right")}<a href="{href(rel, path)}">{esc(name)}</a>'
    cr += f'{ic("chevron-right")}<span aria-current="page">{esc(crumbs[-1][0])}</span>'
    sdh = f'<div class="side">{sd}</div>' if sd else ""
    return (f'<div class="phero"><svg class="mark-bg" aria-hidden="true"><use href="#logo-mark"/></svg><div class="wrap">'
            f'<div><nav class="crumbs" aria-label="Breadcrumb">{cr}</nav><h1>{h1}</h1><p>{lead}</p></div>{sdh}</div></div>')

def cta_band(rel, title="Does your organization have a specific training need?", text="We design the program with the content, duration and location that suit your team, in Dubai, any other emirate or abroad."):
    return (f'<div class="cta-band"><div class="wrap"><div><h2>{title}</h2><p>{text}</p></div>'
            f'<div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-primary" href="{href(rel, "contact/")}">Request a training proposal {ic("arrow-right", "go")}</a>'
            f'<a class="btn btn-line" href="{href(rel, "programs/")}">Program calendar</a></div></div></div>')

CERT_FAQ = ("Do participants receive a certificate?", "Every participant who meets the attendance and assessment requirements receives a certificate of completion from Nuhal Almarifa, a center licensed by Dubai's Knowledge and Human Development Authority (KHDA), showing the program name, hours and dates.")

# ------------------------------------------------------------------ JSON-LD
def org_ld():
    o = B.org_ld()
    o = dict(o); o["description"] = "A KHDA-licensed training and development center in Dubai offering programs for government entities, companies and individuals across the UAE."
    o["knowsAbout"] = ["Government leadership", "Artificial intelligence", "Digital transformation", "Cybersecurity", "Customer experience", "Public finance", "English and IELTS", "Children's skills"]
    return o
def crumbs_ld(crumbs):
    items = [("Home", "en/")] + [(n, "en/" + p) for n, p in crumbs]
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": B.SITE + p} for i, (n, p) in enumerate(items)]}
def faq_ld(faqs): return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
def course_ld(it, path):
    E = tr_en(it["tr"]); en, cc = B.CITY_META[it["c"]]
    return {"@type": "Course", "name": t_en(it), "url": f'{B.SITE}en/{path}#p-{it["id"]}', "inLanguage": "ar",
            "description": f'A five-day in-person training program in the {E["n"]} track by {BRAND_FULL_EN}, held in {en} from {it["d1"]} to {it["d2"]} {MONTHS_FULL[it["m"]]} 2026.',
            "provider": {"@id": B.ORG_ID},
            "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "Onsite", "startDate": it["start"].strftime("%Y-%m-%d"), "endDate": it["end"].strftime("%Y-%m-%d"), "courseWorkload": "P5D",
                                  "location": {"@type": "Place", "name": en, "address": {"@type": "PostalAddress", "addressLocality": en, "addressCountry": cc}}}}

# ------------------------------------------------------------------ layout
NAV = [("home", "Home", ""), ("about", "About", "about/"), ("programs", "Programs", "programs/"), ("courses", "Courses", "courses/"),
       ("accreditations", "Accreditation", "accreditations/"), ("team", "Team", "team/"), ("experience", "Experience", "experience/")]
MEGA = {"about": "mAbout", "programs": "mPrograms", "experience": "mExp"}

def ticket_static(rel, kind):
    it = B.UPCOMING[0] if B.UPCOMING else B.SORTED[-1]; T = B.TRACKS[it["tr"]]; E = tr_en(it["tr"])
    if kind == "mticket":
        return (f'<span class="lab">{esc(E["s"])}</span><b>{esc(t_en(it))}</b><div class="meta"><span>{ic("calendar-days")} {date_txt(it)}</span><span>{ic("map-pin")} {ar_en(it["c"])}</span></div>'
                f'<a class="btn btn-line btn-sm" href="{href(rel, "programs/" + T["slug"] + "/")}#p-{it["id"]}" style="justify-self:start;color:#fff">Details {ic("arrow-right")}</a>')
    return (f'<div class="row1"><span class="lab">{ic("calendar-clock")} Next program</span>{pill(it)}</div><b>{esc(t_en(it))}</b>'
            f'<div class="meta"><span>{ic("calendar-days")} {date_txt(it)}</span><span>{ic("map-pin")} {ar_en(it["c"])}</span></div>'
            f'<button class="btn btn-primary btn-sm" type="button" data-open="{it["id"]}" style="justify-self:start">Details &amp; registration {ic("arrow-right")}</button>')

def header(rel, active, path):
    ar_link = "../" * (path.count("/") + 1) + path
    items = ""
    for key, label, p in NAV:
        cls = "top active" if key == active else "top"; cur = ' aria-current="page"' if key == active else ""
        if key in MEGA:
            items += (f'<li class="has-mega" data-mega="{MEGA[key]}"><a class="{cls}" href="{href(rel, p)}"{cur}>{label}</a>'
                      f'<button class="mt" type="button" aria-expanded="false" aria-controls="{MEGA[key]}" aria-label="Show {label} menu">{ic("chevron-down")}</button></li>')
        else:
            items += f'<li><a class="{cls}" href="{href(rel, p)}"{cur}>{label}</a></li>'
    mtracks = "".join(f'<a class="mlink" href="{href(rel, "programs/" + T["slug"] + "/")}"><span class="leaf sm t-{T["t"]}">{ic(T["i"])}</span><span><b>{esc(tr_en(k)["s"])}</b><small>{len(B.by_track[k])} programs · {", ".join(cities_en(k))}</small></span></a>' for k, T in enumerate(B.TRACKS))
    mareas = "".join(f'<a class="mlink" href="{href(rel, "courses/" + A["slug"] + "/")}"><span class="leaf sm t-{A["t"]}">{ic(A["i"])}</span><span><b>{esc(AREAS_EN[k]["n"])}</b><small>{esc(" · ".join(AREAS_EN[k]["tags"]))}</small></span></a>' for k, A in enumerate(B.AREAS))
    dtracks = "".join(f'<a href="{href(rel, "programs/" + T["slug"] + "/")}">{ic(T["i"])} {esc(tr_en(k)["s"])}</a>' for k, T in enumerate(B.TRACKS))
    dareas = "".join(f'<a href="{href(rel, "courses/" + A["slug"] + "/")}">{ic(A["i"])} {esc(AREAS_EN[k]["n"])}</a>' for k, A in enumerate(B.AREAS))
    E, P = B.EMAILS, B.PHONES
    return f'''
<div class="topbar"><div class="wrap">
  <div class="grp"><span class="it">{ic("badge-check")} Licensed by <b>Dubai's Knowledge and Human Development Authority (KHDA)</b></span><span class="it hide-sm">{ic("map-pin")} Dubai, United Arab Emirates</span></div>
  <div class="grp"><span class="it hide-sm">{ic("phone")} <span class="ltr">{P[0]}</span></span><span class="it hide-sm">{ic("mail")} <span class="ltr">{E[0]}</span></span><a class="it lang" href="{ar_link or "../"}" hreflang="ar" lang="ar">{ic("languages")} العربية</a></div>
</div></div>
<header class="site" id="siteHeader">
  <div class="wrap nav-row">
    <a class="brand" href="{href(rel, "")}" aria-label="{BRAND_EN} home"><svg role="img" aria-label="{BRAND_EN} logo"><use href="#logo-full"/></svg></a>
    <nav aria-label="Main menu" style="display:contents"><ul class="menu">{items}</ul></nav>
    <div class="nav-cta">
      <a class="btn btn-primary btn-sm" href="{href(rel, "contact/")}">Contact us {ic("arrow-right", "go")}</a>
      <button class="burger" id="burger" type="button" aria-label="Open menu" aria-expanded="false">{ic("menu")}</button>
    </div>
  </div>
  <div class="mega mega-about" id="mAbout" role="region" aria-label="About"><div class="wrap">
    <div><h4>Get to know {BRAND_EN}</h4><div class="mlinks">
      <a class="mlink" href="{href(rel, "about/")}"><span class="leaf sm t-leaf">{ic("sprout")}</span><span><b>Who we are</b><small>A licensed training center in Dubai</small></span></a>
      <a class="mlink" href="{href(rel, "about/")}#name"><span class="leaf sm t-gold">{ic("droplets")}</span><span><b>The story of our name</b><small>From the spring to growth</small></span></a>
      <a class="mlink" href="{href(rel, "about/")}#vision"><span class="leaf sm t-ink">{ic("eye")}</span><span><b>Vision &amp; mission</b><small>Where we are heading and how</small></span></a>
      <a class="mlink" href="{href(rel, "about/")}#values"><span class="leaf sm t-leaf">{ic("gem")}</span><span><b>Our values</b><small>Five principles behind our work</small></span></a>
    </div></div>
    <div><h4>Divisions &amp; initiatives</h4><div class="mlinks">
      <a class="mlink" href="{href(rel, "about/")}#ai-division"><span class="leaf sm t-gold">{ic("brain-circuit")}</span><span><b>AI &amp; AGI Readiness Division</b><small>Preparing organizations for intelligent systems</small></span></a>
      <a class="mlink" href="{href(rel, "team/")}"><span class="leaf sm t-leaf">{ic("users")}</span><span><b>Team &amp; experts</b><small>Who designs and delivers our programs</small></span></a>
      <a class="mlink" href="{href(rel, "accreditations/")}"><span class="leaf sm t-ink">{ic("badge-check")}</span><span><b>Accreditation &amp; quality</b><small>KHDA license and quality cycle</small></span></a>
    </div></div>
    <a class="mfeature" href="{href(rel, "accreditations/")}">{img("{ROOT}", "t-burj", "Dubai skyline and Burj Khalifa at sunset")}<span class="in"><span class="kicker" style="color:var(--gold)">Official license</span><b>Licensed by Dubai's Knowledge and Human Development Authority</b><small>What the license means for your organization</small></span></a>
  </div></div>
  <div class="mega mega-programs" id="mPrograms" role="region" aria-label="Programs"><div class="wrap">
    <div><h4>Government programs · 2026 calendar <span>{len(B.ITEMS)} programs</span></h4><div class="mlinks">{mtracks}</div></div>
    <div><h4>Courses for individuals &amp; companies</h4><div class="mlinks">{mareas}</div></div>
    <div style="display:grid;gap:14px;align-content:start"><h4>Next program</h4><div class="mticket" id="megaTicket">{ticket_static(rel, "mticket")}</div>
      <a class="btn btn-gold" href="{href(rel, "programs/")}#catalog">{ic("calendar-range")} Full program calendar</a></div>
  </div></div>
  <div class="mega mega-exp" id="mExp" role="region" aria-label="Experience"><div class="wrap">
    <div><h4>From our track record</h4><div class="mlinks">
      <a class="mlink" href="{href(rel, "experience/")}#case"><span class="leaf sm t-ink">{ic("building-2")}</span><span><b>Dubai Municipality</b><small>Two programs in government and digital marketing</small></span></a>
      <a class="mlink" href="{href(rel, "experience/")}#footprint"><span class="leaf sm t-gold">{ic("globe-2")}</span><span><b>Geographic reach</b><small>{", ".join(ar_en(c) for c in B.CITIES)}</small></span></a>
      <a class="mlink" href="{href(rel, "experience/")}#sectors"><span class="leaf sm t-leaf">{ic("layers")}</span><span><b>Sectors we serve</b><small>From government to children</small></span></a>
    </div></div>
    <div><h4>In numbers</h4><div class="mfacts"><div class="mfact"><b>2</b><span>programs delivered for Dubai Municipality</span></div><div class="mfact"><b>{len(B.CITIES)}</b><span>host cities in Q4 2026</span></div><div class="mfact"><b>{B.by_city.get("دبي", 0)}</b><span>programs scheduled in Dubai</span></div></div></div>
    <a class="mfeature" href="{href(rel, "experience/")}">{img("{ROOT}", "t-table", "A trainer leading a discussion with participants around a meeting table")}<span class="in"><span class="kicker" style="color:var(--gold)">Field experience</span><b>Programs built on the client's reality and measured by what changes after</b><small>View our experience</small></span></a>
  </div></div>
</header>
<div class="drawer" id="drawer" aria-hidden="true"><div class="scrim" data-close-drawer></div>
  <nav class="panel" aria-label="Mobile menu">
    <div class="dhead"><svg aria-hidden="true"><use href="#logo-full"/></svg><button class="burger" type="button" data-close-drawer aria-label="Close menu" style="display:grid">{ic("x")}</button></div>
    <a class="dlink" href="{href(rel, "")}">Home</a>
    <div class="dacc"><button type="button" aria-expanded="false">About {ic("chevron-down")}</button><div class="sub" hidden>
      <a href="{href(rel, "about/")}">{ic("sprout")} Who we are</a><a href="{href(rel, "about/")}#vision">{ic("eye")} Vision &amp; mission</a><a href="{href(rel, "about/")}#values">{ic("gem")} Our values</a><a href="{href(rel, "about/")}#ai-division">{ic("brain-circuit")} AI Readiness Division</a></div></div>
    <div class="dacc"><button type="button" aria-expanded="false">Government programs {ic("chevron-down")}</button><div class="sub" hidden><a href="{href(rel, "programs/")}">{ic("calendar-range")} All programs &amp; calendar</a>{dtracks}</div></div>
    <div class="dacc"><button type="button" aria-expanded="false">Courses {ic("chevron-down")}</button><div class="sub" hidden><a href="{href(rel, "courses/")}">{ic("grid-2x2")} All courses</a>{dareas}</div></div>
    <a class="dlink" href="{href(rel, "accreditations/")}">Accreditation</a>
    <a class="dlink" href="{href(rel, "team/")}">Team</a>
    <a class="dlink" href="{href(rel, "experience/")}">Experience</a>
    <a class="dlink" href="{ar_link or "../"}" hreflang="ar" lang="ar">العربية</a>
    <a class="btn btn-primary" href="{href(rel, "contact/")}" style="margin-top:16px">Contact us {ic("arrow-right", "go")}</a>
    <div style="margin-top:16px;font-size:14px;color:var(--muted);display:grid;gap:6px"><span class="ltr" style="justify-self:start">{P[0]}</span><span class="ltr" style="justify-self:start">{E[0]}</span></div>
  </nav>
</div>'''

def footer(rel):
    ft = "".join(f'<li><a href="{href(rel, "programs/" + T["slug"] + "/")}">{esc(tr_en(k)["s"])}</a></li>' for k, T in enumerate(B.TRACKS))
    fa = "".join(f'<li><a href="{href(rel, "courses/" + A["slug"] + "/")}">{esc(AREAS_EN[k]["s"])}</a></li>' for k, A in enumerate(B.AREAS))
    E, P = B.EMAILS, B.PHONES
    return f'''
<footer class="site"><svg class="mark-bg" aria-hidden="true"><use href="#logo-mark"/></svg><div class="wrap">
  <div class="fgrid">
    <div><svg class="flogo" role="img" aria-label="{BRAND_EN}"><use href="#logo-full"/></svg>
      <p>A training and development center in Dubai, designing programs for leaders, organizations and individuals across the UAE, from AI to public finance.</p>
      <span class="khda-mini">{ic("badge-check")} Licensed by KHDA, Dubai</span></div>
    <div><h4>Company</h4><ul><li><a href="{href(rel, "about/")}">About</a></li><li><a href="{href(rel, "accreditations/")}">Accreditation</a></li><li><a href="{href(rel, "team/")}">Team</a></li><li><a href="{href(rel, "experience/")}">Experience</a></li><li><a href="{href(rel, "contact/")}">Contact us</a></li></ul></div>
    <div><h4><a href="{href(rel, "programs/")}">Government programs</a></h4><ul>{ft}</ul></div>
    <div><h4><a href="{href(rel, "courses/")}">Courses</a></h4><ul>{fa}</ul></div>
    <div><h4>Contact</h4><ul><li>{E[0]}</li><li>{E[1]}</li><li>{P[0]}</li><li>{P[1]}</li><li>Dubai, United Arab Emirates</li></ul></div>
  </div>
  <div class="fbottom"><span>© 2026 {B.LEGAL_EN}. All rights reserved.</span><span lang="ar">{B.BRAND_FULL} ذ.م.م · دبي</span></div>
</div></footer>'''

MODAL = f'''
<div class="modal" id="modal" hidden role="dialog" aria-modal="true" aria-labelledby="mTitle"><div class="scrim" data-close-modal></div>
  <div class="box"><div class="mh"><button class="x" type="button" data-close-modal aria-label="Close">{ic("x")}</button><div id="mChip"></div><h3 id="mTitle"></h3></div>
    <div class="mb"><div class="facts" id="mFacts"></div>
      <div class="inc"><span>{ic("award")} Certificate of completion from {BRAND_EN}</span><span>{ic("clipboard-check")} Pre- and post-assessment</span><span>{ic("book-open")} Participant materials</span></div>
      <div id="regWrap"></div></div></div></div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>'''

def page(path, active, title, desc, body, ld=None, og_img="og"):
    rel = "../" * (path.count("/") + 1)  # pages live under en/
    canonical = B.SITE + "en/" + path; ar_url = B.SITE + path
    graph = [org_ld()] + (ld or [])
    ldjson = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    og_url = B.SITE + ("assets/og.jpg" if og_img == "og" else f"assets/img/{og_img}.jpg")
    doc = f'''<!doctype html>
<html lang="en-AE" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="ar-AE" href="{ar_url}">
<link rel="alternate" hreflang="en-AE" href="{canonical}">
<link rel="alternate" hreflang="x-default" href="{ar_url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND_FULL_EN}">
<meta property="og:locale" content="en_AE">
<meta property="og:locale:alternate" content="ar_AE">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_url}">
<meta property="og:image:alt" content="{BRAND_FULL_EN}, Dubai">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{og_url}">
<meta name="geo.region" content="AE-DU">
<meta name="geo.placename" content="Dubai">
<meta name="theme-color" content="#0B2A3A">
<link rel="icon" type="image/svg+xml" href="{rel}assets/favicon.svg">
<link rel="apple-touch-icon" href="{rel}assets/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alexandria:wght@400;500;600;700;800&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{rel}assets/css/site.css">
<script type="application/ld+json">{ldjson}</script>
</head>
<body data-rel="{rel}en/" data-root="{rel}" data-page="{active}">
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="logo-full" viewBox="40 46 654 350">{B.LOGO_FULL}</symbol><symbol id="logo-mark" viewBox="44 50 280 297">{B.LOGO_MARK}</symbol></svg>
<a class="sr" href="#main">Skip to content</a>
{header(rel + "en/", active, path)}
<main id="main">
{body}
</main>
{footer(rel + "en/")}
{MODAL}
{B.whatsapp_btn("en")}
<script src="https://unpkg.com/lucide@0.344.0/dist/umd/lucide.min.js" defer></script>
<script src="{rel}assets/js/site.js" defer></script>
</body>
</html>
'''
    out = os.path.join(B.OUT, "en", path, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    doc = doc.replace("{ROOT}", rel)
    open(out, "w").write(doc)
    PAGES_EN.append(dict(path="en/" + path, title=title, desc=desc, h1=re.search(r"<h1[^>]*>(.*?)</h1>", doc, re.S).group(1)))

# ------------------------------------------------------------------ sections
def tracks_grid(rel):
    out = []
    for idx, k in enumerate([5, 0, 1, 2, 3, 4, 6]):
        T = B.TRACKS[k]; E = tr_en(k); n = len(B.by_track[k]); url = href(rel, "programs/" + T["slug"] + "/")
        if idx == 0:
            tags = "".join(f"<span>{esc(t)}</span>" for t in E["tags"])
            out.append(f'<a class="track feature" href="{url}"><svg class="mark-bg" aria-hidden="true"><use href="#logo-mark"/></svg><span class="leaf lg t-gold">{ic(T["i"])}</span><h3>{esc(E["n"])}</h3><p>{esc(E["card"])}</p><div class="tags">{tags}</div><div class="foot"><span><b>{n}</b> programs · {len(B.cities_of(k))} cities</span>{ic("arrow-right", "go")}</div></a>')
        else:
            out.append(f'<a class="track" href="{url}"><span class="leaf t-{T["t"]}">{ic(T["i"])}</span><h3>{esc(E["n"])}</h3><p>{esc(E["card"])}</p><div class="foot"><span><b>{n}</b> programs</span>{ic("arrow-right", "go")}</div></a>')
    return '<div class="tracks">' + "".join(out) + "</div>"

def areas_grid(rel):
    return '<div class="areas">' + "".join(
        f'<a class="area" href="{href(rel, "courses/" + A["slug"] + "/")}"><div class="ph">{img("{ROOT}", A["img"], AREAS_EN[k]["n"] + " in Dubai")}</div><div class="bd"><span class="leaf t-{A["t"]}">{ic(A["i"])}</span><h3>{esc(AREAS_EN[k]["n"])}</h3><p>{esc(AREAS_EN[k]["card"])}</p><span class="more">Course details {ic("arrow-right")}</span></div></a>' for k, A in enumerate(B.AREAS)) + "</div>"

WHY = [("badge-check", "leaf", "KHDA licensed", "Licensed by Dubai's Knowledge and Human Development Authority and committed to UAE education standards."),
       ("user-check", "gold", "Trainers from the field", "Experts who combine academic qualifications with hands-on experience in the sector they teach."),
       ("users", "ink", "Learner-centered", "Flexible schedules, small groups and individual attention for every participant."),
       ("monitor-smartphone", "leaf", "Modern facilities", "Training rooms, computer labs and learning resources for a comfortable environment."),
       ("layers", "gold", "Comprehensive portfolio", "Programs for every stage of development, from children to senior executives."),
       ("target", "ink", "Measurable results", "We focus on skills applied at work and career progress you can track.")]
def why_section(title="What makes training with us different", photo="t-board"):
    items = "".join(f'<div class="why-item"><span class="leaf sm t-{t}">{ic(i)}</span><div><h3>{a}</h3><p>{b}</p></div></div>' for i, t, a, b in WHY)
    return (f'<section class="section on-surface why"><div class="wrap"><div class="framed">{img("{ROOT}", photo, "A trainer explaining to a group of participants in a Dubai training room")}<span class="tag">{ic("badge-check")} KHDA licensed</span></div>'
            f'<div><span class="kicker">Why Nuhal Almarifa</span><h2 class="h2">{title}</h2><div class="why-list">{items}</div></div></div></section>')

def related_tracks(rel, skip):
    return '<div class="related">' + "".join(f'<a class="rel" href="{href(rel, "programs/" + T["slug"] + "/")}"><span class="leaf sm t-{T["t"]}">{ic(T["i"])}</span><span><b>{esc(tr_en(k)["s"])}</b><small>{len(B.by_track[k])} programs</small></span>{ic("arrow-right", "go")}</a>' for k, T in enumerate(B.TRACKS) if k != skip) + "</div>"
def related_areas(rel, skip):
    return '<div class="related">' + "".join(f'<a class="rel" href="{href(rel, "courses/" + A["slug"] + "/")}"><span class="leaf sm t-{A["t"]}">{ic(A["i"])}</span><span><b>{esc(AREAS_EN[k]["n"])}</b><small>{esc(" · ".join(AREAS_EN[k]["tags"][:2]))}</small></span>{ic("arrow-right", "go")}</a>' for k, A in enumerate(B.AREAS) if k != skip) + "</div>"

# ================================================================== pages
def home():
    rel = ""  # links relative to /en/
    up = B.UPCOMING[:5] or B.SORTED[-5:]
    stats = "".join(f'<div class="stat"><b>{n}</b><span>{l}</span></div>' for n, l in [(len(B.ITEMS), "programs in the Q4 2026 calendar"), (len(B.TRACKS), "specialized government and corporate tracks"), (len(B.CITIES), "host cities in Dubai and abroad"), (len(B.AREAS), "course areas for individuals and companies")])
    others = [ar_en(c) for c in B.CITIES if c != "دبي"]
    faqs = [("Is Nuhal Almarifa a licensed training center in Dubai?", "Yes. Nuhal Almarifa Training & Development is licensed by Dubai's Knowledge and Human Development Authority (KHDA), the regulator of private education in the emirate."),
            ("What programs does the center offer?", f"The Q4 2026 calendar includes {len(B.ITEMS)} specialized government programs across {len(B.TRACKS)} tracks, including leadership, AI, digital transformation, cybersecurity and public finance, plus courses for individuals and companies in management, IT, languages, professional skills and kids programs."),
            ("Where are the programs held?", f"Most programs run in Dubai, and some in {join_en(others)}. Any program can also be delivered at your organization's premises in any emirate."),
            ("How do I register or request a custom program?", f"Choose a program from the calendar and click Details & registration, or contact us at {B.EMAILS[0]} or {B.PHONES[0]}. We reply within one working day.")]
    body = f'''
<div class="hero"><div class="wrap">
  <div class="hero-copy">
    <span class="badge-line"><span class="dot">{ic("badge-check")}</span>A <b>KHDA-licensed</b> training center in Dubai</span>
    <h1><span class="h1-kw">Training &amp; development center in Dubai, UAE</span>We nurture knowledge,<br>so <em>capability<svg viewBox="0 0 200 20" preserveAspectRatio="none" aria-hidden="true"><path d="M3 15 C 50 4, 120 4, 197 10" fill="none" stroke="var(--gold)" stroke-width="5" stroke-linecap="round"/></svg></em> grows</h1>
    <p class="lead">{BRAND_FULL_EN} designs training for government entities, companies and individuals in Dubai and the UAE: leadership, AI, innovation, cybersecurity and public finance, alongside language, IT, professional skills and kids programs.</p>
    <div class="hero-ctas"><a class="btn btn-primary" href="programs/">{ic("calendar-days")} Browse the program calendar</a><a class="btn btn-line" href="contact/">Request a custom program {ic("arrow-right", "go")}</a></div>
    <div class="hero-meta"><div>{ic("landmark")} Government programs</div><div>{ic("building")} Corporate solutions</div><div>{ic("graduation-cap")} Courses for individuals</div></div>
  </div>
  <div class="media"><span class="blk b-gold"></span><span class="blk b-leaf"></span>
    <div class="photo">{img("{ROOT}", "hero", "Government leaders in a training session overlooking the Dubai skyline", lazy=False)}</div>
    <svg class="arrow" viewBox="0 0 160 170" aria-hidden="true"><path class="draw" d="M8 162 C 40 140, 70 110, 92 70 S 128 18, 140 12"/><path class="head" d="M112 10 L 142 10 L 140 40"/></svg>
    <div class="ticket" id="heroTicket">{ticket_static(rel, "ticket")}</div>
  </div>
</div></div>
<div class="wrap"><div class="stats">{stats}</div></div>
<section class="section"><div class="wrap">
  {sec_head("Coming up", "Seats available in upcoming programs", "Dates from the Q4 2026 calendar (October to December) in Dubai and international destinations. Pick a program and send your registration in a minute.", f'<a class="link-go" href="programs/#catalog">Full calendar {ic("arrow-right")}</a>')}
  <div class="ledger" id="upcoming">{"".join(lrow(x) for x in up)}</div>
</div></section>
<section class="section on-surface"><div class="wrap">
  {sec_head("Government programs", "Seven tracks covering UAE government priorities", "Each track is a set of connected programs that start with strategy and end with practical tools participants use at work the next day.", f'<a class="link-go" href="programs/">All programs {ic("arrow-right")}</a>')}
  {tracks_grid(rel)}
</div></section>
<section class="section"><div class="wrap">
  {sec_head("Courses for individuals &amp; companies", "Training courses in Dubai for every stage of growth", "From management, IT and languages to professional skills and kids programs, at a licensed center in Dubai.", f'<a class="link-go" href="courses/">All courses {ic("arrow-right")}</a>')}
  {areas_grid(rel)}
</div></section>
<section class="section on-dark ai-band"><div class="wrap">
  <div><span class="kicker">AI &amp; AGI Readiness Division</span>
    <h2 class="h2">Preparing UAE organizations to work alongside intelligent systems</h2>
    <p class="lead">A division dedicated entirely to artificial intelligence and the transition toward artificial general intelligence. We don't just teach tools; we prepare organizations to govern intelligent systems and lead alongside them.</p>
    <div class="pillars">
      <div class="pillar"><span class="leaf t-gold">{ic("map")}</span><div><h3>Strategy &amp; readiness</h3><p>2030 roadmaps and readiness assessments across governance, people and technology.</p></div></div>
      <div class="pillar"><span class="leaf t-leaf">{ic("shield-check")}</span><div><h3>Governance &amp; responsible use</h3><p>Safe-use policies, data protection and model risk management.</p></div></div>
      <div class="pillar"><span class="leaf t-ink">{ic("workflow")}</span><div><h3>Everyday application</h3><p>Prompt engineering, Copilot, process automation and Agentic AI.</p></div></div>
    </div>
    <div style="margin-top:28px"><a class="btn btn-gold" href="programs/government-ai/">Government AI courses {ic("arrow-right", "go")}</a></div>
  </div>
  <div class="ai-media"><span class="frame"></span>{img("{ROOT}", "ai", "A glowing AI chip on an electronic circuit board")}<div class="count"><b>{B.AI_COUNT}</b><span>AI-related programs in this quarter's calendar</span></div></div>
</div></section>
<section class="section"><div class="wrap">
  {sec_head("Who we design for", "From leadership boards to kids' classrooms")}
  <div class="aud">
    <div><span class="leaf t-ink">{ic("landmark")}</span><h3>Government entities</h3><p>Leadership and specialist programs tied to performance indicators and UAE government transformation targets.</p></div>
    <div><span class="leaf t-leaf">{ic("building-2")}</span><h3>Companies</h3><p>Raising team capability in management, technology, sales and customer service.</p></div>
    <div><span class="leaf t-gold">{ic("briefcase")}</span><h3>Professionals</h3><p>Paths for career growth, languages, digital skills and IELTS preparation.</p></div>
    <div><span class="leaf t-leaf">{ic("blocks")}</span><h3>Students &amp; children</h3><p>Academic support and age-appropriate skills programs in a safe environment.</p></div>
  </div>
</div></section>
{why_section()}
<section class="section"><div class="wrap">
  {sec_head("Our method", "From need to impact in four stages")}
  <div class="steps">
    <div class="step"><span class="n">01</span><h3>Diagnose</h3><p>We analyze the organization's needs and performance gaps before proposing any content.</p></div>
    <div class="step"><span class="n">02</span><h3>Design</h3><p>We build clear learning outcomes and practical cases from the sector.</p></div>
    <div class="step"><span class="n">03</span><h3>Deliver</h3><p>Interactive training led by field experts, in Dubai or abroad.</p></div>
    <div class="step"><span class="n">04</span><h3>Measure</h3><p>Pre- and post-assessment and an impact report delivered after the program.</p></div>
  </div>
</div></section>
<section class="section on-surface"><div class="wrap two-col">
  <article class="seo-article"><span class="kicker">Training in Dubai</span><h2 class="h2">Why choose a licensed training center in Dubai?</h2>
    <p>Dubai is one of the region's biggest investors in human capital, and its government entities and companies work to high performance standards that require continuous skills development. Choosing a training center licensed by the <a href="accreditations/">Knowledge and Human Development Authority</a> means the program runs within a clear regulatory framework and the certificate comes from an authorized provider.</p>
    <p>At Nuhal Almarifa we combine that regulatory commitment with a deep understanding of the UAE market: <a href="programs/">government programs</a> tied to transformation and excellence targets, practical <a href="programs/government-ai/">AI courses</a> aligned with national direction, and <a href="courses/">courses for individuals and companies</a> in management, IT and <a href="courses/languages/">English and IELTS</a>.</p>
  </article>
  <div>{sec_head("FAQ", "Before you start")}{faq_html(faqs)}</div>
</div></section>
{cta_band(rel)}'''
    page("", "home", "Nuhal Almarifa | KHDA-Licensed Training Center in Dubai",
         "KHDA-licensed training center in Dubai, UAE: programs for government, companies and individuals in AI, leadership, finance and languages.",
         body, ld=[{"@type": "WebSite", "@id": B.SITE + "en/#website", "url": B.SITE + "en/", "name": BRAND_FULL_EN, "inLanguage": "en-AE", "publisher": {"@id": B.ORG_ID}}, faq_ld(faqs)])

def about():
    rel = "../"; crumbs = [("About", "about/")]
    body = f'''
{phero(rel, crumbs, "About Nuhal Almarifa: a Training &amp; Development Center in Dubai", "A licensed training and development center in Dubai serving professionals, students, children and teams in government and private organizations across the UAE.", side(("KHDA", "Official license"), (len(B.AREAS) + len(B.TRACKS), "Tracks &amp; areas")))}
<section class="section"><div class="wrap split">
  <div class="prose"><span class="kicker">Who we are</span><h2 class="h2">A learning partner that understands Dubai and the UAE</h2>
    <p>{BRAND_FULL_EN} is a training and development center based in Dubai and licensed by the Knowledge and Human Development Authority (KHDA), ensuring our programs meet the highest standards of quality in education and professional training.</p>
    <p>We empower individuals and organizations through high-quality programs that support continuous growth, skills development and lifelong learning. We believe knowledge is the foundation of progress, and we are committed to innovative, practical, results-oriented learning experiences.</p>
    <p>With experienced trainers and educators, modern facilities and a learner-centered approach, we serve a wide audience of professionals, students, children, corporate teams and government entities, with flexible learning options that match the needs of Dubai and the UAE.</p>
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:26px"><a class="btn btn-primary" href="../programs/">Government programs</a><a class="btn btn-line" href="../courses/">Courses for individuals &amp; companies</a></div></div>
  <div class="framed">{img("{ROOT}", "t-monitor", "Two participants working at a computer screen in a hands-on training session in Dubai")}<span class="tag">{ic("map-pin")} Dubai, UAE</span></div>
</div></section>
<section class="section tight" id="name"><div class="wrap"><div class="name-card">
  <div class="word" lang="ar">نُهال<small lang="en">NUHAL · Seekers of knowledge</small></div>
  <dl><div><dt>Where does the name come from?</dt><dd>In Arabic, <i>nahala</i> means to drink from a <i>manhal</i>, a spring. <i>Nuhhal</i> are those who come to the spring to drink. That is how we see our learners: people who seek knowledge at its source.</dd></div>
  <div><dt>And what does the logo say?</dt><dd>Green leaves that are watered and grow, and a golden arrow rising between them. Knowledge nurtured, then performance that rises and can be measured.</dd></div></dl>
</div></div></section>
<section class="section on-surface" id="vision"><div class="wrap">
  {sec_head("Vision &amp; mission", "Where we are heading, and how we get there")}
  <div class="vm"><div class="v"><h3><span class="leaf t-leaf">{ic("eye")}</span>Our vision</h3><p>To be the premier strategic beacon in professional training and human capital development, empowering individuals and organizations through innovative, smart and sustainable learning ecosystems, and shaping a competitive, future-ready workforce.</p></div>
  <div class="m"><h3><span class="leaf t-ink">{ic("target")}</span>Our mission</h3><p>To deliver world-class training and development solutions through innovative methodologies, expert facilitation and customized programs, fostering a culture of continuous learning, enhancing professional competencies and providing measurable value that drives sustainable growth for our clients and partners.</p></div></div>
</div></section>
<section class="section" id="values"><div class="wrap">
  {sec_head("Our values", "Five principles behind every program")}
  <div class="values">
    <div><span class="leaf t-gold">{ic("award")}</span><h3>Excellence</h3><p>The highest standards in curriculum design, training delivery and client engagement.</p></div>
    <div><span class="leaf t-leaf">{ic("lightbulb")}</span><h3>Innovation</h3><p>Continuously integrating modern learning technologies, smart ecosystems and creative methods.</p></div>
    <div><span class="leaf t-ink">{ic("heart-handshake")}</span><h3>Empowerment</h3><p>Equipping individuals and teams with the practical tools and confidence to lead in their fields.</p></div>
    <div><span class="leaf t-leaf">{ic("sprout")}</span><h3>Sustainability</h3><p>Championing long-term professional growth and practices that meet tomorrow's demands.</p></div>
    <div><span class="leaf t-gold">{ic("scale")}</span><h3>Integrity</h3><p>Full transparency, professionalism and ethical responsibility in all our partnerships.</p></div>
  </div>
</div></section>
<section class="section on-dark ai-band" id="ai-division"><div class="wrap">
  <div class="ai-media"><span class="frame"></span>{img("{ROOT}", "ai", "A glowing AI chip on an electronic circuit board")}</div>
  <div><span class="kicker">AI &amp; AGI Readiness Division</span><h2 class="h2">Pioneering the horizon instead of chasing it</h2>
    <p class="lead">In an era of hyper-acceleration and technological disruption, Nuhal Almarifa breaks away from conventional training with a division dedicated to artificial intelligence and the transition toward artificial general intelligence (AGI). We prepare organizations to co-exist with, govern and lead alongside autonomous intelligent systems.</p>
    <div style="margin-top:28px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-gold" href="../programs/government-ai/">Government AI courses {ic("arrow-right", "go")}</a><a class="btn btn-line" href="../programs/digital-transformation/">Digital transformation</a></div></div>
</div></section>
<section class="section" id="gallery"><div class="wrap">
  {sec_head("Learning in action", "Interactive rooms, not silent lectures")}
  <div class="gallery">
    <figure>{img("{ROOT}", "act-1", "A training room full of participants facing a presentation screen")}<figcaption>Large plenary sessions</figcaption></figure>
    <figure>{img("{ROOT}", "act-2", "A design thinking workshop with colorful sticky notes on the wall")}<figcaption>Design thinking workshops</figcaption></figure>
    <figure>{img("{ROOT}", "t-present", "A trainer presenting on leadership and strategy")}<figcaption>Leadership &amp; strategy</figcaption></figure>
    <figure>{img("{ROOT}", "act-3", "Participants discussing around a laptop")}<figcaption>Hands-on tool practice</figcaption></figure>
    <figure>{img("{ROOT}", "t-laptop", "A participant working on a laptop in a training room")}<figcaption>Digital labs</figcaption></figure>
  </div>
</div></section>
{cta_band(rel, "Start your development journey with Nuhal Almarifa", "Tell us what your organization or team needs, and we will suggest the right program within one working day.")}'''
    page("about/", "about", "About Nuhal Almarifa | KHDA-Licensed Training in Dubai",
         "About Nuhal Almarifa, a KHDA-licensed training center in Dubai: our story, vision, mission, values and AI Readiness Division.",
         body, ld=[crumbs_ld(crumbs), {"@type": "AboutPage", "name": "About Nuhal Almarifa", "url": B.SITE + "en/about/", "about": {"@id": B.ORG_ID}, "inLanguage": "en-AE"}])

def programs_hub():
    rel = "../"; crumbs = [("Programs", "programs/")]
    chips = f'<button class="fchip" type="button" data-tr="-1" aria-pressed="true">{ic("layout-grid")} All tracks <b>{len(B.ITEMS)}</b></button>' + "".join(f'<button class="fchip" type="button" data-tr="{k}" aria-pressed="false">{ic(T["i"])} {esc(tr_en(k)["s"])} <b>{len(B.by_track[k])}</b></button>' for k, T in enumerate(B.TRACKS))
    city_opts = "".join(f'<option value="{esc(c)}">{ar_en(c)} ({B.by_city[c]})</option>' for c in B.CITIES)
    all_c = [ar_en(c) for c in B.CITIES]
    faqs = [("How long are the government training programs?", "Each program in the calendar runs for five training days, Sunday to Thursday. Duration can be adjusted for custom programs delivered to a single entity."),
            ("Where are the programs held?", f"Programs are held in {join_en(all_c)}. Dubai is our home base and hosts {B.by_city.get('دبي', 0)} of the {len(B.ITEMS)} programs in the Q4 2026 calendar."),
            ("Can you deliver a program that is not in the calendar?", "Yes. We design fully custom programs around your entity's needs, in Dubai, any other emirate or abroad. Send us your requirements from the contact page."),
            ("How do I register myself or a team?", "Open the program, click Details & registration and enter the number of participants in the request form. We confirm seats and fees by email within one working day."),
            CERT_FAQ]
    body = f'''
{phero(rel, crumbs, "Government Training Programs in Dubai &amp; the UAE 2026", f"{len(B.ITEMS)} programs for government entities and organizations across {len(B.TRACKS)} specialized tracks, held in Dubai and international destinations in Q4 2026.", side((len(B.ITEMS), "programs"), (len(B.TRACKS), "tracks"), (len(B.CITIES), "cities")))}
<section class="section"><div class="wrap"><div class="intro-grid">
  <div class="prose seo-article"><span class="kicker">Government training</span><h2 class="h2">Programs built around UAE government priorities</h2>
    <p>Government entities in Dubai and across the UAE work toward clear targets in digital transformation, customer experience, financial efficiency and future readiness. Nuhal Almarifa built its program calendar around exactly these priorities, in seven complementary tracks from <a href="government-leadership/">government leadership</a> and <a href="government-ai/">artificial intelligence</a> to <a href="finance-accounting/">finance and auditing</a>.</p>
    <p>Each program is five practical days led by field experts and ends with tools participants use in their entity. You can register individually for any program, or request it for your entire team.</p></div>
  <aside class="facts-card"><h2>The calendar at a glance</h2>
    <div class="row"><span class="leaf sm t-leaf">{ic("calendar-range")}</span><div><small>Period</small><b>October – December 2026</b></div></div>
    <div class="row"><span class="leaf sm t-gold">{ic("clock")}</span><div><small>Program length</small><b>5 days (Sunday – Thursday)</b></div></div>
    <div class="row"><span class="leaf sm t-ink">{ic("map-pin")}</span><div><small>Host cities</small><b>{", ".join(all_c)}</b></div></div>
    <div class="row"><span class="leaf sm t-leaf">{ic("award")}</span><div><small>Certificate</small><b>Completion certificate from a KHDA-licensed center</b></div></div>
    <a class="btn btn-primary" href="#catalog">{ic("calendar-days")} Go to the calendar</a>
  </aside></div>
</div></section>
<section class="section on-surface"><div class="wrap">
  {sec_head("Tracks", "Choose the right track for your entity", "Each track has its own page with learning outcomes, target audience and program dates.")}
  {tracks_grid(rel)}
</div></section>
<section class="section" id="catalog" style="padding-top:72px"><div class="wrap">
  {sec_head("Q4 2026 calendar", "All programs and dates", "Filter by track, city or month, then open a program to send your registration request.")}
</div>
<div class="toolbar"><div class="wrap">
  <div class="tb-row">
    <div class="field">{ic("search")}<label for="q" class="sr">Search programs</label><input class="input" id="q" type="search" placeholder="Search by program title, e.g. governance, Copilot, budgets"></div>
    <label for="fCity" class="sr">City</label><select class="select" id="fCity"><option value="">All cities</option>{city_opts}</select>
    <label for="fMonth" class="sr">Month</label><select class="select" id="fMonth"><option value="">All months</option><option value="10">October</option><option value="11">November</option><option value="12">December</option></select>
    <label class="check"><input type="checkbox" id="fPast"> Show completed programs</label>
  </div>
  <div class="chips" id="trackChips" role="group" aria-label="Filter by track">{chips}</div>
</div></div>
<div class="wrap">
  <div class="result-line"><span id="resultCount"><b>{len(B.ITEMS)}</b> programs</span><button class="copy-btn" type="button" id="resetFilters">{ic("rotate-ccw")} Reset filters</button></div>
  <div class="pgrid" id="pgrid">{"".join(pcard(x) for x in B.SORTED)}</div>
  <div class="empty" id="emptyState" hidden>{ic("search-x")}<b style="color:var(--heading);font-family:var(--f-display)">No matching programs</b><span>Try another track or city, or turn on "Show completed programs".</span></div>
</div></section>
<section class="section on-surface"><div class="wrap two-col">
  <div>{sec_head("FAQ", "About government programs")}{faq_html(faqs)}</div>
  <div><span class="kicker">Courses for individuals &amp; companies</span><h2 class="h2">Looking for a course for yourself or your team?</h2><p class="lead">Alongside government programs, we run courses in Dubai in management, IT, languages, professional skills and kids programs.</p>
    <div class="related" style="grid-template-columns:1fr;margin-top:24px">{"".join(f'<a class="rel" href="../courses/{A["slug"]}/"><span class="leaf sm t-{A["t"]}">{ic(A["i"])}</span><span><b>{esc(AREAS_EN[k]["n"])}</b><small>{esc(" · ".join(AREAS_EN[k]["tags"]))}</small></span>{ic("arrow-right", "go")}</a>' for k, A in enumerate(B.AREAS[:4]))}</div>
    <a class="link-go" href="../courses/" style="margin-top:18px">All courses {ic("arrow-right")}</a></div>
</div></section>
{cta_band(rel)}'''
    page("programs/", "programs", "Government Training Programs in Dubai 2026 | Nuhal Almarifa",
         f"{len(B.ITEMS)} government training programs in Dubai and the UAE: leadership, AI, innovation, cybersecurity and finance. View 2026 dates and register.",
         body, ld=[crumbs_ld(crumbs), faq_ld(faqs), {"@type": "ItemList", "name": "Government training program tracks", "itemListElement": [{"@type": "ListItem", "position": k + 1, "url": B.SITE + "en/programs/" + T["slug"] + "/", "name": tr_en(k)["n"]} for k, T in enumerate(B.TRACKS)]}])

def track(k):
    T = B.TRACKS[k]; E = tr_en(k); rel = "../../"; path = f'programs/{T["slug"]}/'
    crumbs = [("Programs", "programs/"), (E["s"], path)]
    items = B.by_track[k]; cs = B.cities_of(k)
    cnt = {c: sum(1 for x in items if x["c"] == c) for c in cs}
    open_n = sum(1 for x in items if B.status(x) != "done")
    faqs = list(E["faq"]) + [
        (f"Where and when are the {E['s']} programs held?", f"Programs in this track run in Q4 2026 in {join_en([ar_en(c) for c in cs])}, and each program lasts five days, Sunday to Thursday. Detailed dates are listed on this page."),
        (f"Can {E['s']} programs be delivered at our entity?", "Yes. Any program in this track can be designed as a custom program for a single entity, with suitable content, duration and dates, at your premises in any emirate or abroad."),
        CERT_FAQ]
    aud = "".join(f'<li>{ic("user-round-check")}<span>{esc(a)}</span></li>' for a in E["audience"])
    outc = "".join(f'<li>{ic("check")}<span>{esc(o)}</span></li>' for o in E["outcomes"])
    city_line = ", ".join(f"{ar_en(c)} ({cnt[c]})" for c in cs)
    body = f'''
{phero(rel, crumbs, esc(E["h1"]), esc(E["lead"]), side((len(items), "programs"), (len(cs), "cities" if len(cs) > 1 else "city"), (5, "days per program")))}
<section class="section"><div class="wrap"><div class="intro-grid">
  <div class="prose"><span class="kicker">About the track</span><h2 class="h2">{esc(E["n"])}</h2>{"".join(f"<p>{esc(p)}</p>" for p in E["intro"])}
    <div class="tags" style="margin-top:22px">{"".join(f"<span>{esc(t)}</span>" for t in E["tags"])}</div></div>
  <aside class="facts-card"><h2>The track at a glance</h2>
    <div class="row"><span class="leaf sm t-{T["t"]}">{ic(T["i"])}</span><div><small>Programs</small><b>{len(items)} programs · {open_n} open or in progress</b></div></div>
    <div class="row"><span class="leaf sm t-ink">{ic("map-pin")}</span><div><small>Host cities</small><b>{city_line}</b></div></div>
    <div class="row"><span class="leaf sm t-gold">{ic("clock")}</span><div><small>Program length</small><b>5 days (Sunday – Thursday)</b></div></div>
    <div class="row"><span class="leaf sm t-leaf">{ic("award")}</span><div><small>Certificate</small><b>Completion certificate from a KHDA-licensed center</b></div></div>
    <a class="btn btn-primary" href="#dates">{ic("calendar-days")} Dates &amp; registration</a>
  </aside></div>
</div></section>
<section class="section on-surface"><div class="wrap two-col">
  <div><span class="kicker">Target audience</span><h2 class="h2">Who this track is for</h2><ul class="checklist gold" style="margin-top:22px">{aud}</ul></div>
  <div><span class="kicker">Learning outcomes</span><h2 class="h2">What participants gain</h2><ul class="checklist" style="margin-top:22px">{outc}</ul></div>
</div></section>
<section class="section" id="dates"><div class="wrap">
  {sec_head("2026 dates", f"{esc(E['s'])} programs and dates", "Open a program to view details and send an individual or group registration request.")}
  <div class="pgrid">{"".join(pcard(x, with_chip=False) for x in items)}</div>
</div></section>
<section class="section on-surface"><div class="wrap">{sec_head("FAQ", f"Questions about {esc(E['s'])}")}{faq_html(faqs)}</div></section>
<section class="section tight"><div class="wrap">
  {sec_head("Other tracks", "Explore the other tracks", "", f'<a class="link-go" href="../#catalog">Full calendar {ic("arrow-right")}</a>')}
  {related_tracks(rel, k)}
</div></section>
{cta_band(rel, f"Want a {esc(E['s'])} program for your team?", "We design the program for your entity with suitable content, duration and dates, in Dubai or at your premises.")}'''
    page(path, "programs", E["title"], E["desc"], body,
         ld=[crumbs_ld(crumbs), faq_ld(faqs), {"@type": "ItemList", "name": f"{E['n']} programs 2026", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": course_ld(x, path)} for i, x in enumerate(items)]}],
         og_img=T["img"])

def courses_hub():
    rel = "../"; crumbs = [("Courses", "courses/")]
    faqs = [("What training courses does Nuhal Almarifa offer in Dubai?", "Courses in six areas: management and leadership, computer and IT, languages with IELTS and TOEFL preparation, educational services for students, professional skills and customer service, and children's skills development."),
            ("Are the courses for individuals or companies?", "Both. Individuals can join open courses, and companies and schools can request courses tailored to their teams with suitable content and dates."),
            ("Is the center licensed?", "Yes. Nuhal Almarifa Training & Development is licensed by Dubai's Knowledge and Human Development Authority (KHDA)."),
            ("How do I find out the next course date and fee?", f"Contact us at {B.EMAILS[0]} or {B.PHONES[0]} with the course you are interested in, and we will send dates, fees and registration details.")]
    body = f'''
{phero(rel, crumbs, "Training Courses in Dubai for Individuals &amp; Companies", "Six training areas at a KHDA-licensed center in Dubai, from management, IT and languages to professional skills and kids programs.", side((len(B.AREAS), "areas"), ("KHDA", "licensed")))}
<section class="section"><div class="wrap"><div class="intro-grid">
  <div class="prose seo-article"><span class="kicker">Courses in Dubai</span><h2 class="h2">Skills for every stage, from children to managers</h2>
    <p>The job market in Dubai and the UAE is fast and multinational, and it rewards people who keep developing their skills. That is why our course portfolio covers the needs of families, individuals and companies together: <a href="management-leadership/">management and leadership courses</a> for managers, <a href="computer-it/">computer courses</a> for digital skills, <a href="languages/">English and IELTS courses</a> for study and work, and <a href="kids/">kids programs</a> that build curiosity and a love of learning.</p>
    <p>Courses run at our Dubai center with flexible schedules and small groups, and any course can be tailored for a company or school team.</p></div>
  <aside class="facts-card"><h2>Ways to join</h2>
    <div class="row"><span class="leaf sm t-leaf">{ic("user")}</span><div><small>Individuals</small><b>Open courses at our Dubai center</b></div></div>
    <div class="row"><span class="leaf sm t-gold">{ic("building-2")}</span><div><small>Companies &amp; schools</small><b>Custom courses at our center or your premises</b></div></div>
    <div class="row"><span class="leaf sm t-ink">{ic("calendar-clock")}</span><div><small>Schedules</small><b>Flexible timings for employees and students</b></div></div>
    <a class="btn btn-primary" href="../contact/">Ask about the next course</a>
  </aside></div>
</div></section>
<section class="section on-surface"><div class="wrap">{sec_head("Training areas", "Choose an area to see course details")}{areas_grid(rel)}</div></section>
{why_section("Why individuals and companies in Dubai choose us", "t-laptop")}
<section class="section"><div class="wrap">{sec_head("FAQ", "About training courses in Dubai")}{faq_html(faqs)}</div></section>
{cta_band(rel, "Need a course for your company team?", "Tell us the area and the number of participants, and we will suggest a course with the right content and schedule.")}'''
    page("courses/", "courses", "Training Courses in Dubai for Individuals & Companies",
         "Courses in Dubai at a KHDA-licensed center: management, computer skills, English and IELTS, tutoring, professional skills and kids programs.",
         body, ld=[crumbs_ld(crumbs), faq_ld(faqs), {"@type": "ItemList", "name": "Training course areas in Dubai", "itemListElement": [{"@type": "ListItem", "position": k + 1, "url": B.SITE + "en/courses/" + A["slug"] + "/", "name": AREAS_EN[k]["n"]} for k, A in enumerate(B.AREAS)]}])

def area(k):
    A = B.AREAS[k]; E = AREAS_EN[k]; rel = "../../"; path = f'courses/{A["slug"]}/'
    crumbs = [("Courses", "courses/"), (E["s"], path)]
    faqs = list(E["faq"]) + [
        (f"Are the {E['s']} courses held in person in Dubai?", "Yes. Courses run in person at our licensed center in Dubai with flexible schedules, and can be delivered for company and school teams at their premises."),
        (f"How do I register for {E['s']} courses?", f"Contact us at {B.EMAILS[0]} or {B.PHONES[0]}, or send a request from the contact page, and we will send the upcoming dates, fees and registration details."),
        ("Do learners receive a certificate?", "Yes. Every learner who meets the attendance and assessment requirements receives a certificate of completion from Nuhal Almarifa, a center licensed by Dubai's Knowledge and Human Development Authority.")]
    topics = "".join(f'<div class="topic"><span class="leaf sm t-{A["t"]}">{ic("check")}</span><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in E["topics"])
    aud = "".join(f'<li>{ic("user-round-check")}<span>{esc(a)}</span></li>' for a in E["audience"])
    body = f'''
{phero(rel, crumbs, esc(E["h1"]), esc(E["lead"]), side(("KHDA", "licensed center"), (len(E["topics"]), "training topics")))}
<section class="section"><div class="wrap split">
  <div class="prose"><span class="kicker">{esc(E["n"])}</span><h2 class="h2">{esc(E["lead"].split(":")[0].split(",")[0])}</h2>{"".join(f"<p>{esc(p)}</p>" for p in E["intro"])}
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:26px"><a class="btn btn-primary" href="../../contact/">Ask about the next date {ic("arrow-right", "go")}</a><a class="btn btn-line" href="#topics">Course topics</a></div></div>
  <div class="framed">{img("{ROOT}", A["img"], E["n"] + " in Dubai")}<span class="tag">{ic(A["i"])} {esc(E["s"])}</span></div>
</div></section>
<section class="section on-surface" id="topics"><div class="wrap">{sec_head("What you will learn", f"{esc(E['s'])} course topics")}<div class="topics{" n7" if len(E["topics"]) == 7 else ""}">{topics}</div></div></section>
<section class="section"><div class="wrap two-col">
  <div><span class="kicker">Who it is for</span><h2 class="h2">Target audience</h2><ul class="checklist gold" style="margin-top:22px">{aud}</ul></div>
  <div><span class="kicker">Delivery formats</span><h2 class="h2">Choose the format that suits you</h2>
    <ul class="checklist" style="margin-top:22px">
      <li>{ic("map-pin")}<span><b>Open courses in Dubai:</b> join a small group at our licensed center.</span></li>
      <li>{ic("building-2")}<span><b>Custom courses:</b> for your company or school team with content and timing that suit you.</span></li>
      <li>{ic("calendar-clock")}<span><b>Flexible schedules:</b> timings that work for employees and students.</span></li>
      <li>{ic("award")}<span><b>Certificate of completion:</b> from a center licensed by the Knowledge and Human Development Authority.</span></li>
    </ul></div>
</div></section>
<section class="section on-surface"><div class="wrap">{sec_head("FAQ", f"Questions about {esc(E['s'])} courses in Dubai")}{faq_html(faqs)}</div></section>
<section class="section tight"><div class="wrap">{sec_head("Other areas", "Other courses you may like", "", f'<a class="link-go" href="../">All courses {ic("arrow-right")}</a>')}{related_areas(rel, k)}</div></section>
{cta_band(rel, f"Ready to start {esc(E['s'])}?", "Send us the course name and number of participants, and we will reply with dates and details within one working day.")}'''
    service = {"@type": "Service", "name": E["h1"], "serviceType": E["n"], "description": E["desc"], "provider": {"@id": B.ORG_ID},
               "areaServed": [{"@type": "City", "name": "Dubai"}, {"@type": "Country", "name": "United Arab Emirates"}], "url": B.SITE + "en/" + path,
               "hasOfferCatalog": {"@type": "OfferCatalog", "name": E["n"] + " courses", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Course", "name": a, "description": b, "provider": {"@id": B.ORG_ID}}} for a, b in E["topics"]]}}
    page(path, "courses", E["title"], E["desc"], body, ld=[crumbs_ld(crumbs), faq_ld(faqs), service], og_img=A["img"])

def accreditations():
    rel = "../"; crumbs = [("Accreditation", "accreditations/")]
    faqs = [("Is Nuhal Almarifa licensed by KHDA?", "Yes. Nuhal Almarifa Training & Development L.L.C is licensed by Dubai's Knowledge and Human Development Authority (KHDA)."),
            ("What is the Knowledge and Human Development Authority?", "It is the government authority that regulates private education in Dubai, including training centers, and sets the frameworks and standards licensed institutions follow."),
            ("How can I verify a training center's license in Dubai?", "Licensed education providers can be checked through the official channels of the Knowledge and Human Development Authority at khda.gov.ae."),
            ("What does the certificate of completion include?", "The certificate shows the participant's name, program title, training hours and dates, and is awarded to everyone who meets the attendance and assessment requirements.")]
    body = f'''
{phero(rel, crumbs, "A KHDA-Licensed Training Center in Dubai", "An official license from Dubai's private education regulator, and a quality framework that follows every program from diagnosis to impact report.")}
<section class="section"><div class="wrap"><div class="khda">
  <div class="seal" aria-hidden="true"><svg viewBox="0 0 220 220"><circle cx="110" cy="110" r="104" fill="none" stroke="var(--gold)" stroke-width="2"/><circle cx="110" cy="110" r="94" fill="none" stroke="var(--gold)" stroke-width="1" stroke-dasharray="2 5"/><circle cx="110" cy="110" r="78" fill="var(--night)"/><path d="M110 46 l7 14 15 2 -11 11 3 15 -14 -7 -14 7 3 -15 -11 -11 15 -2z" fill="var(--gold)"/><text x="110" y="128" text-anchor="middle" font-family="Alexandria, sans-serif" font-weight="800" font-size="30" fill="#fff" letter-spacing="2">KHDA</text><text x="110" y="152" text-anchor="middle" font-family="Alexandria, sans-serif" font-weight="600" font-size="13" fill="#9FBDC2">LICENSED · DUBAI</text></svg></div>
  <div><span class="kicker">Official license</span><h2 class="h2">Licensed by Dubai's Knowledge and Human Development Authority</h2>
    <p class="lead">The Knowledge and Human Development Authority (KHDA) is the government body that regulates private education in Dubai, including training centers. Our license means our programs, facilities and practices operate within its regulatory framework and standards.</p></div>
</div></div></section>
<section class="section tight on-surface"><div class="wrap">
  {sec_head("What the license means for you", "Assurances for the organization and the participant")}
  <div class="means">
    <div class="mean"><span class="leaf t-leaf">{ic("clipboard-check")}</span><h3>Program quality</h3><p>Content and learning outcomes that follow quality standards in education and professional training.</p></div>
    <div class="mean"><span class="leaf t-gold">{ic("scale")}</span><h3>Regulatory compliance</h3><p>Operating within UAE education regulations and the authority's requirements in Dubai.</p></div>
    <div class="mean"><span class="leaf t-ink">{ic("school")}</span><h3>Suitable environment</h3><p>Rooms, labs and learning resources prepared for effective, safe training.</p></div>
    <div class="mean"><span class="leaf t-leaf">{ic("file-text")}</span><h3>Clear contracting</h3><p>Transparency on program details, fees and registration from first contact.</p></div>
  </div>
</div></section>
<section class="section"><div class="wrap ent">
  <div class="ent-card"><svg aria-hidden="true" style="position:absolute;right:-30px;bottom:-40px;width:200px;opacity:.1"><use href="#logo-mark"/></svg>
    <span class="kicker">Legal entity</span><h2 style="font-size:22px">Company details</h2>
    <dl><div><dt>Legal name</dt><dd>{B.LEGAL_EN}</dd></div><div><dt>Arabic name</dt><dd lang="ar">{B.BRAND_FULL} ذ.م.م</dd></div><div><dt>Headquarters</dt><dd>Dubai, United Arab Emirates</dd></div><div><dt>Licensing authority</dt><dd>Knowledge and Human Development Authority (KHDA)</dd></div><div><dt>Website</dt><dd>www.nuhal.ae</dd></div></dl></div>
  <div class="cert"><span class="note">Sample design</span><div class="sheet"><svg aria-hidden="true"><use href="#logo-full"/></svg><span class="t">Certificate of Completion</span><span class="d">{BRAND_FULL_EN} certifies that</span><span class="n">Participant name</span><span class="d">has completed the requirements of the training program "Program title" for the stated hours and dates, and passed its assessment.</span><div class="sig"><span>General Manager</span><span>Programs Director</span></div></div>
    <p style="font-size:14px;color:var(--muted);padding:14px 8px 4px">Every participant who meets the attendance and assessment requirements receives a certificate showing the program name, hours and dates.</p></div>
</div></section>
<section class="section on-surface"><div class="wrap">
  {sec_head("Quality cycle", "Six stages every program goes through")}
  <div class="cycle">
    <div class="cyc"><span class="n">01</span><span class="leaf sm t-leaf">{ic("search-check")}</span><h3>Needs analysis</h3><p>Interviews and surveys to identify the real performance gap.</p></div>
    <div class="cyc"><span class="n">02</span><span class="leaf sm t-gold">{ic("pencil-ruler")}</span><h3>Outcome design</h3><p>Measurable learning objectives and content built on real cases.</p></div>
    <div class="cyc"><span class="n">03</span><span class="leaf sm t-ink">{ic("clipboard-list")}</span><h3>Pre-assessment</h3><p>Measuring participants' level before starting to set depth and examples.</p></div>
    <div class="cyc"><span class="n">04</span><span class="leaf sm t-leaf">{ic("presentation")}</span><h3>Interactive delivery</h3><p>Exercises, workshops and simulations led by specialist trainers.</p></div>
    <div class="cyc"><span class="n">05</span><span class="leaf sm t-gold">{ic("clipboard-check")}</span><h3>Post-assessment</h3><p>Measuring what participants learned against the pre-assessment.</p></div>
    <div class="cyc"><span class="n">06</span><span class="leaf sm t-ink">{ic("file-bar-chart")}</span><h3>Impact report</h3><p>A report for the entity with results, recommendations and a follow-up plan.</p></div>
  </div>
</div></section>
<section class="section"><div class="wrap">
  {sec_head("Measuring impact", "Four levels we use to measure success", "An evaluation framework inspired by the Kirkpatrick model, linking what happens in the room to what changes at work.")}
  <div class="levels">
    <div class="lvl" style="--w:25%"><h3><span class="leaf sm t-leaf">{ic("smile")}</span>1. Reaction</h3><p>Participant satisfaction with content, trainer and environment, through an end-of-day survey.</p></div>
    <div class="lvl" style="--w:50%"><h3><span class="leaf sm t-gold">{ic("brain")}</span>2. Learning</h3><p>The difference between pre- and post-assessment results in the targeted knowledge and skills.</p></div>
    <div class="lvl" style="--w:75%"><h3><span class="leaf sm t-ink">{ic("repeat")}</span>3. Application</h3><p>How far participants apply what they learned at work in the weeks after the program.</p></div>
    <div class="lvl" style="--w:100%"><h3><span class="leaf sm t-leaf">{ic("trending-up")}</span>4. Impact</h3><p>The program's effect on the entity's performance indicators agreed during diagnosis.</p></div>
  </div>
</div></section>
<section class="section on-surface"><div class="wrap">{sec_head("FAQ", "About licensing and certificates")}{faq_html(faqs)}</div></section>
{cta_band(rel)}'''
    page("accreditations/", "accreditations", "KHDA-Licensed Training Center in Dubai | Accreditation",
         "Nuhal Almarifa is licensed by Dubai's Knowledge and Human Development Authority. See what the license means, our certificates and quality cycle.",
         body, ld=[crumbs_ld(crumbs), faq_ld(faqs)])

def team():
    rel = "../"; crumbs = [("Team", "team/")]
    fac = "".join(f'<a class="frow" href="../programs/{T["slug"]}/"><div class="who"><span class="leaf t-{T["t"]}">{ic(T["i"])}</span><h3>{esc(tr_en(k)["n"])} experts</h3></div><div class="tags">{"".join(f"<span>{esc(t)}</span>" for t in tr_en(k)["tags"])}</div><div class="num"><b>{len(B.by_track[k])}</b><span>programs led</span></div></a>' for k, T in enumerate(B.TRACKS))
    body = f'''
{phero(rel, crumbs, "Our Team: Trainers &amp; Experts in Dubai", "A management team that leads design, quality and coordination, and a network of specialist experts and consultants for every training track.", side((len(B.TRACKS), "expert groups"), (4, "management units")))}
<section class="section"><div class="wrap split">
  <div><span class="kicker">How we work</span><h2 class="h2">A lean management team, and a wide network of experts in the room</h2>
    <p class="lead">For each program we select the trainer closest to its subject and sector, supported by the programs team from diagnosis to the impact report. Your organization gets deep specialization with a single point of contact in Dubai.</p></div>
  <div class="framed">{img("{ROOT}", "t-present", "A trainer presenting to a group of participants in Dubai")}<span class="tag">{ic("users")} Experts from the field</span></div>
</div></section>
<section class="section tight on-surface"><div class="wrap">
  {sec_head("Management team", "Four units that lead the work")}
  <div class="roles">
    <div class="role"><span class="av t-ink">{ic("compass")}</span><h3>General Management</h3><p>Sets the center's strategic direction and oversees program quality and partnerships with government and private entities.</p></div>
    <div class="role"><span class="av t-leaf">{ic("pencil-ruler")}</span><h3>Programs &amp; Instructional Design</h3><p>Turns each client's needs into curricula, learning outcomes and assessment tools, and follows delivery day by day.</p></div>
    <div class="role"><span class="av t-gold">{ic("headset")}</span><h3>Client Relations &amp; Coordination</h3><p>One point of contact for each entity: scheduling, registration, arrangements in the UAE and abroad, and certificates.</p><span class="contact">{ic("mail")}<span class="ltr">{B.EMAILS[1]}</span></span></div>
    <div class="role"><span class="av t-ink">{ic("line-chart")}</span><h3>Quality &amp; Evaluation</h3><p>Measures participant satisfaction and learning before and after each program, and prepares impact reports.</p></div>
  </div>
</div></section>
<section class="section"><div class="wrap">
  {sec_head("Expert network", "Experts and consultants for every track", "Each track is led by trainers who combine executive experience in the sector with academic and professional qualifications.")}
  <div class="faculty">{fac}</div>
  <div style="margin-top:64px" class="split">
    <div><span class="kicker">Selection criteria</span><h2 class="h2">How we choose our trainers</h2>
      <ul class="criteria">
        <li>{ic("check")}Practical experience in the government or corporate sector related to the program</li>
        <li>{ic("check")}Academic and professional qualifications in the specialty</li>
        <li>{ic("check")}Ability to train in Arabic and English</li>
        <li>{ic("check")}A strong record of evaluations from participants and clients</li>
        <li>{ic("check")}Continuous content updates with the latest tools and practices</li>
        <li>{ic("check")}A practical style built on cases and exercises, not lecturing</li>
      </ul></div>
    <div class="framed">{img("{ROOT}", "t-table", "A trainer in discussion with participants around a meeting table")}<span class="tag">{ic("star")} Evaluated after every program</span></div>
  </div>
  <div class="join"><div><h3>Are you a trainer or expert in one of our tracks?</h3><p>We welcome trainers and consultants from the UAE and the region to join our network. Send your CV and areas of expertise.</p></div>
    <div style="display:grid;gap:8px;justify-items:start"><span class="mail">{ic("mail")}<span class="ltr">{B.EMAILS[0]}</span></span><button class="copy-btn" type="button" data-copy="{B.EMAILS[0]}" style="color:var(--gold)">{ic("copy")} Copy email</button></div></div>
</div></section>
{cta_band(rel)}'''
    page("team/", "team", "Our Team | Trainers & Experts in Dubai | Nuhal Almarifa",
         "Meet the Nuhal Almarifa team in Dubai: management, instructional design and quality units, and experts in leadership, AI and finance.",
         body, ld=[crumbs_ld(crumbs)])

def experience():
    rel = "../"; crumbs = [("Experience", "experience/")]
    mc = max(B.by_city.values()); mt = max(len(v) for v in B.by_track.values()); mm = max(B.by_month.values())
    chc = "".join(f'<div class="bar" style="--tone:{"var(--ink)" if i == 0 else "var(--leaf)"}"><span class="lab">{ic("map-pin")} {ar_en(c)}</span><span class="trk"><span class="fill" style="display:block;width:{B.by_city[c] / mc * 100:.1f}%"></span></span><span class="v">{B.by_city[c]}</span></div>' for i, c in enumerate(B.CITIES))
    cht = "".join(f'<div class="bar" style="--tone:{B.TONE[B.TRACKS[k]["t"]]}"><a class="lab" href="../programs/{B.TRACKS[k]["slug"]}/" title="{esc(tr_en(k)["n"])}">{esc(tr_en(k)["s"])}</a><span class="trk"><span class="fill" style="display:block;width:{len(B.by_track[k]) / mt * 100:.1f}%"></span></span><span class="v">{len(B.by_track[k])}</span></div>' for k in sorted(range(len(B.TRACKS)), key=lambda k: -len(B.by_track[k])))
    chm = "".join(f'<div class="mcol"><b>{B.by_month[m]}</b><span class="col" style="height:{B.by_month[m] / mm * 150:.0f}px"></span></div>' for m in (10, 11, 12))
    intl = "".join(f"<span>{ar_en(c)} · {B.by_city[c]}</span>" for c in B.CITIES if c != "دبي")
    body = f'''
{phero(rel, crumbs, "Our Government &amp; Corporate Training Experience in Dubai", "Programs delivered for government entities in Dubai, a calendar spanning five cities, and a portfolio serving governments, companies and individuals across the UAE.", side((len(B.ITEMS), "scheduled programs"), (len(B.CITIES), "cities"), (len(B.TRACKS), "tracks")))}
<section class="section" id="case"><div class="wrap">
  {sec_head("Delivered projects", "Dubai Municipality: two programs for the corporate marketing department")}
  <div class="case">
    <div class="cside"><svg aria-hidden="true" style="position:absolute;right:-30px;bottom:-40px;width:210px;opacity:.1"><use href="#logo-mark"/></svg><span class="leaf lg t-gold">{ic("building-2")}</span><h3>Dubai Municipality</h3>
      <p>We designed and delivered two in-person programs in Dubai for the corporate marketing department team, in Arabic with English terminology, within our government and digital marketing track.</p>
      <div class="kv"><div><b>2</b><span>programs delivered</span></div><div><b>31</b><span>training hours</span></div><div><b>7</b><span>training days</span></div><div><b>2026</b><span>year delivered</span></div></div></div>
    <div class="cmain">
      <div class="prog"><div class="top"><h4>Advanced Professionalism &amp; Innovation in Government Marketing</h4><span class="pill st-open">Delivered</span></div>
        <div class="meta"><span>{ic("calendar-days")} 4 days × 4 hours</span><span>{ic("map-pin")} In person, Dubai</span><span>{ic("languages")} Arabic with English terms</span></div>
        <p style="color:var(--muted);font-size:15px">A strategic program linking government marketing to the entity's goals and customer experience, with innovation tools for campaigns and institutional messaging.</p></div>
      <div class="prog"><div class="top"><h4>Advanced Performance Development in Digital Marketing</h4><span class="pill st-open">Delivered</span></div>
        <div class="meta"><span>{ic("calendar-days")} 3 days × 5 hours</span><span>{ic("map-pin")} In person, Dubai</span><span>{ic("file-text")} Fully Arabic materials</span></div>
        <div class="mods"><div><small>Day 1</small>Social ads, channels and content</div><div><small>Day 2</small>Search visibility: SEO and GEO</div><div><small>Day 3</small>AI in digital marketing</div></div></div>
    </div>
  </div>
</div></section>
<section class="section on-surface" id="footprint"><div class="wrap">
  {sec_head("Reach &amp; distribution", "Where and when our programs run", "Figures calculated from the Q4 2026 program calendar.")}
  <div class="charts">
    <div class="chart"><h3>Programs by city</h3><p class="sub">Scheduled programs in each city</p><div class="bars">{chc}</div></div>
    <div class="chart"><h3>Programs by track</h3><p class="sub">Programs in each specialized track</p><div class="bars">{cht}</div></div>
    <div class="chart" style="grid-column:1/-1"><h3>Monthly rhythm</h3><p class="sub">Programs starting each month</p><div class="months">{chm}</div><div class="mlabels"><span>October</span><span>November</span><span>December</span></div></div>
  </div>
</div></section>
<section class="section" id="sectors"><div class="wrap">
  {sec_head("Sectors", "Who we serve in the UAE")}
  <div class="sectors">
    <div class="sector"><span class="leaf t-ink">{ic("landmark")}</span><h3>Government</h3><p>Leadership, digital transformation, public finance, customer experience.</p></div>
    <div class="sector"><span class="leaf t-leaf">{ic("building-2")}</span><h3>Companies</h3><p>Management, sales, customer service, technical skills.</p></div>
    <div class="sector"><span class="leaf t-gold">{ic("briefcase")}</span><h3>Professionals</h3><p>Career growth, languages, digital tools.</p></div>
    <div class="sector"><span class="leaf t-ink">{ic("graduation-cap")}</span><h3>Students</h3><p>Academic support, exam preparation, study skills.</p></div>
    <div class="sector"><span class="leaf t-leaf">{ic("blocks")}</span><h3>Children</h3><p>STEM, critical thinking, arts, confidence.</p></div>
  </div>
  {sec_head("Delivery formats", "Three ways to deliver a program").replace('class="sec-head"', 'class="sec-head" style="margin-top:72px"')}
  <div class="formats">
    <div class="format"><span class="leaf t-leaf">{ic("map-pin")}</span><h3>In person in Dubai</h3><p>Programs in our licensed Dubai rooms, the largest share of this quarter's calendar.</p><div class="cities"><span>Dubai · {B.by_city.get("دبي", 0)} programs</span></div></div>
    <div class="format"><span class="leaf t-gold">{ic("plane")}</span><h3>International programs</h3><p>Programs that combine training with exposure to institutional practice in destinations outside the UAE.</p><div class="cities">{intl}</div></div>
    <div class="format"><span class="leaf t-ink">{ic("settings-2")}</span><h3>Custom programs</h3><p>Content, duration and dates designed for a single entity, at the location it chooses.</p><div class="cities"><span>On request</span></div></div>
  </div>
</div></section>
{cta_band(rel, "Add your organization to our track record", "We design a program with clear objectives and measure its impact after delivery.")}'''
    page("experience/", "experience", "Our Training Experience in Dubai & the UAE | Nuhal Almarifa",
         "Our training record: programs delivered for Dubai Municipality and a 2026 calendar across Dubai, Cairo, Istanbul, Madrid and France.",
         body, ld=[crumbs_ld(crumbs)])

def contact():
    rel = "../"; crumbs = [("Contact", "contact/")]
    opts = "".join(f"<option>{esc(tr_en(k)['n'])}</option>" for k in range(len(B.TRACKS))) + "".join(f"<option>{esc(E['n'])}</option>" for E in AREAS_EN)
    faqs = [("How quickly do you reply to requests?", "Our client relations team contacts you within one working day of receiving your request."),
            ("Do you send proposals to government entities and companies?", "Yes. After understanding the entity's needs and number of participants, we send a detailed training proposal with content, duration, dates and fees."),
            ("Can training be delivered outside Dubai?", "Yes. We deliver programs in any emirate and in international destinations such as Cairo, Istanbul, Madrid and France.")]
    E, P = B.EMAILS, B.PHONES
    body = f'''
{phero(rel, crumbs, "Contact Nuhal Almarifa in Dubai", "Tell us what your organization needs or which course interests you, and our client relations team will reply within one working day.")}
<section class="section on-surface contact" id="contact"><div class="wrap">
  <div><span class="kicker">Contact details</span><h2 class="h2">Based in Dubai, serving the UAE and the region</h2>
    <div class="cinfo">
      <div class="cline"><span class="leaf sm t-leaf">{ic("mail")}</span><div><small>Email</small><div class="two"><b class="ltr">{E[0]}</b><b class="ltr">{E[1]}</b></div></div></div>
      <div class="cline"><span class="leaf sm t-gold">{ic("phone")}</span><div><small>Phone &amp; WhatsApp</small><div class="two"><b class="ltr">{P[0]}</b><b class="ltr">{P[1]}</b></div></div></div>
      <div class="cline"><span class="leaf sm t-ink">{ic("map-pin")}</span><div><small>Headquarters</small><b>Dubai, United Arab Emirates</b></div></div>
      <div class="cline"><span class="leaf sm t-leaf">{ic("globe")}</span><div><small>Website</small><b class="ltr">www.nuhal.ae</b></div></div>
    </div></div>
  <div class="cform" id="cformBox"><h3>Request a training program or course</h3><p>Fill in your details and we will receive your request directly.</p>
    <form class="form" id="cform" novalidate>
      <label>Full name <span class="req">*</span><input class="input" id="c-name" required autocomplete="name"></label>
      <label>Organization / company <span class="req">*</span><input class="input" id="c-org" required autocomplete="organization"></label>
      <label>Email <span class="req">*</span><input class="input" id="c-email" type="email" required autocomplete="email"></label>
      <label>Phone <span class="req">*</span><input class="input" id="c-phone" type="tel" required autocomplete="tel" placeholder="+971"></label>
      <label>Area of interest<select class="select" id="c-track" style="width:100%;flex:none"><option value="">Choose an area</option>{opts}<option>Other custom program</option></select></label>
      <label>Expected participants<input class="input" id="c-count" type="number" min="1" value="10"></label>
      <label class="full">Details of your need<textarea id="c-msg" placeholder="Example: a three-day program for our digital transformation team, in Dubai, in January"></textarea></label>
      <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <div class="full form-actions"><button class="btn btn-primary" type="submit">{ic("send")} Send request</button><span class="form-note">Fields marked * are required</span></div>
    </form></div>
</div></section>
<section class="section"><div class="wrap two-col">
  <div>{sec_head("FAQ", "Before you get in touch")}{faq_html(faqs)}</div>
  <div><span class="kicker">Quick links</span><h2 class="h2">Find the right program</h2>
    <div class="related" style="grid-template-columns:1fr;margin-top:24px">
      <a class="rel" href="../programs/"><span class="leaf sm t-ink">{ic("calendar-range")}</span><span><b>2026 government program calendar</b><small>{len(B.ITEMS)} programs in {len(B.TRACKS)} tracks</small></span>{ic("arrow-right", "go")}</a>
      <a class="rel" href="../courses/"><span class="leaf sm t-leaf">{ic("grid-2x2")}</span><span><b>Courses for individuals &amp; companies</b><small>{len(B.AREAS)} training areas in Dubai</small></span>{ic("arrow-right", "go")}</a>
      <a class="rel" href="../programs/government-ai/"><span class="leaf sm t-gold">{ic("brain-circuit")}</span><span><b>Government AI courses</b><small>{len(B.by_track[5])} programs</small></span>{ic("arrow-right", "go")}</a>
    </div></div>
</div></section>'''
    page("contact/", "contact", "Contact Nuhal Almarifa | Training Center in Dubai",
         f"Contact Nuhal Almarifa in Dubai to request a training program or course: {E[0]} · {P[0]}. We reply within one working day.",
         body, ld=[crumbs_ld(crumbs), faq_ld(faqs), {"@type": "ContactPage", "name": "Contact Nuhal Almarifa", "url": B.SITE + "en/contact/", "about": {"@id": B.ORG_ID}}])

def run(b):
    global B
    B = b
    home(); about(); programs_hub()
    for k in range(len(B.TRACKS)): track(k)
    courses_hub()
    for k in range(len(B.AREAS)): area(k)
    accreditations(); team(); experience(); contact()
    return PAGES_EN
