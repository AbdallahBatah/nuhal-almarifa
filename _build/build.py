# -*- coding: utf-8 -*-
"""Static site generator for nuhal.ae — writes a multi-page Arabic site with SEO metadata."""
import json, os, re, shutil, sys, datetime, html
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from content import *

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = HERE  # data files live next to this script
OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else ROOT
BUILD_DATE = datetime.date(2026, 11, 9)
NOW = datetime.datetime(2026, 11, 9, 12, 0)

esc = lambda s: html.escape(str(s), quote=True)
ic = lambda n, cls="": f'<i data-lucide="{n}"{" class=%s" % chr(34)+cls+chr(34) if cls else ""}></i>'
MONTHS = {10: "أكتوبر", 11: "نوفمبر", 12: "ديسمبر"}
DAYS = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]  # python weekday()
TONE = {"ink": "var(--ink)", "leaf": "var(--leaf)", "gold": "var(--gold)"}

# ------------------------------------------------------------------ data
ITEMS = json.load(open(os.path.join(SRC, "items.json")))
for k, it in enumerate(ITEMS):
    it["id"] = k
    it["start"] = datetime.datetime(2026, it["m"], it["d1"])
    it["end"] = datetime.datetime(2026, it["m"], it["d2"], 23, 59)
SORTED = sorted(ITEMS, key=lambda x: (x["start"], x["tr"]))
def status(it): return "done" if NOW > it["end"] else ("live" if NOW >= it["start"] else "open")
ST = {"open": ("st-open", "متاح للتسجيل"), "live": ("st-live", "قيد الانعقاد"), "done": ("st-done", "منعقد")}
by_track = {k: [x for x in SORTED if x["tr"] == k] for k in range(len(TRACKS))}
by_city = {}
for x in ITEMS: by_city[x["c"]] = by_city.get(x["c"], 0) + 1
CITIES = sorted(by_city, key=lambda c: -by_city[c])
by_month = {m: sum(1 for x in ITEMS if x["m"] == m) for m in (10, 11, 12)}
UPCOMING = [x for x in SORTED if x["start"] > NOW]
AI_COUNT = sum(1 for x in ITEMS if re.search(r"الذكاء الاصطناعي|AI|Copilot|Prompt", x["t"]))
def cities_of(k): return list(dict.fromkeys(x["c"] for x in by_track[k]))
def date_txt(it): return f'{it["d1"]}–{it["d2"]} {MONTHS[it["m"]]} 2026'
def ar_join(lst): return "، ".join(lst[:-1]) + " و" + lst[-1] if len(lst) > 1 else lst[0]

IMG_SIZES = {}
for f in os.listdir(os.path.join(SRC, "img")):
    IMG_SIZES[f[:-4]] = Image.open(os.path.join(SRC, "img", f)).size

LOGO_FULL = open(os.path.join(SRC, "logo_full.txt")).read()
LOGO_MARK = open(os.path.join(SRC, "logo_mark.txt")).read()
BASE_CSS = re.search(r"<style>(.*?)</style>", open(os.path.join(SRC, "template.html")).read(), re.S).group(1)
BASE_CSS = BASE_CSS.replace(".page{display:none}\n.page.show{display:block;animation:pagein .45s ease both}\n@keyframes pagein{from{opacity:.4;transform:translateY(8px)}to{opacity:1;transform:none}}\n", "")
BASE_CSS = BASE_CSS.replace(".track.feature .tags span{font-size:12.5px;padding:4px 10px;border:1px solid", ".track.feature .tags span{font-size:12.5px;padding:4px 10px;background:transparent;border:1px solid")

EXTRA_CSS = r"""
/* ---------- multi-page additions ---------- */
.menu .has-mega{display:flex;align-items:stretch}
.menu .has-mega .top{padding-inline-end:2px}
.menu .mt{display:flex;align-items:center;padding:0 10px 0 6px;color:var(--muted)}
.menu .mt .lucide{width:15px;height:15px;transition:transform .25s}
.menu .mt[aria-expanded="true"] .lucide{transform:rotate(180deg)}
.menu .has-mega.open .top::after{transform:scaleX(1)}
.h1-kw{display:block;font-size:15px!important;font-weight:600;color:var(--leaf);margin-bottom:14px;letter-spacing:0;line-height:1.5}
.intro-grid{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(0,1fr);gap:56px;align-items:start}
.intro-grid .prose p{font-size:17.5px;line-height:1.95}
.facts-card{background:var(--surface);border:1px solid var(--line);border-top:4px solid var(--gold);border-radius:6px;padding:10px 26px 18px;position:sticky;top:110px}
.facts-card h2{font-size:17px;padding:16px 0 6px}
.facts-card .row{display:grid;grid-template-columns:auto minmax(0,1fr);gap:14px;align-items:start;padding:14px 0;border-bottom:1px dashed var(--line)}
.facts-card .row:last-of-type{border-bottom:0}
.facts-card small{display:block;font-size:12.5px;color:var(--muted)}
.facts-card b{font-family:var(--f-display);font-weight:600;color:var(--heading);font-size:15px;line-height:1.6}
.facts-card .btn{width:100%;margin-top:8px}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:56px}
.checklist{display:grid}
.checklist li{display:flex;gap:12px;align-items:flex-start;padding:13px 0;border-bottom:1px dashed var(--line);font-size:16px;line-height:1.7}
.checklist .lucide{color:var(--leaf);margin-top:5px}
.checklist.gold .lucide{color:var(--gold-deep)}
.faq{display:grid;gap:10px;max-width:920px}
.faq details{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:0 22px;transition:border-color .2s}
.faq details[open]{border-color:var(--leaf)}
.faq summary{cursor:pointer;list-style:none;padding:18px 0;font-family:var(--f-display);font-weight:600;font-size:16.5px;color:var(--heading);display:flex;justify-content:space-between;gap:16px;align-items:center}
.faq summary::-webkit-details-marker{display:none}
.faq summary .lucide{transition:transform .25s;color:var(--leaf);flex:none}
.faq details[open] summary .lucide{transform:rotate(45deg)}
.faq details p{padding:0 0 20px;color:var(--muted);font-size:15.5px;line-height:1.9;max-width:75ch}
.related{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.rel{display:flex;gap:14px;align-items:center;padding:16px 18px;border:1px solid var(--line);border-radius:6px;background:var(--surface);transition:border-color .2s,transform .2s;min-width:0}
.rel:hover{border-color:var(--leaf);transform:translateY(-2px)}
.rel b{display:block;font-family:var(--f-display);font-size:15px;color:var(--heading);line-height:1.5}
.rel small{display:block;font-size:12.5px;color:var(--muted)}
.rel .go{margin-inline-start:auto;color:var(--leaf)}
.topics{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.topics.n7{grid-template-columns:repeat(4,minmax(0,1fr))}
.topics.n7 .topic:first-child{grid-column:span 2}
.topic{padding:24px;border:1px solid var(--line);background:var(--surface);border-radius:6px;display:grid;gap:10px;align-content:start;min-width:0}
.topic h3{font-size:17px}
.topic p{font-size:14.5px;color:var(--muted);line-height:1.75}
a.area{transition:box-shadow .25s,transform .25s}
a.area:hover{box-shadow:var(--shadow);transform:translateY(-3px)}
a.area .more{display:inline-flex;gap:6px;align-items:center;font-family:var(--f-display);font-weight:600;font-size:14px;color:var(--leaf);margin-top:4px}
.seo-article{max-width:860px}
.seo-article h2{margin-bottom:6px}
.seo-article p{font-size:17px;line-height:1.95;margin-top:16px;color:var(--fg)}
.seo-article a{color:var(--ink);text-decoration:underline;text-decoration-color:color-mix(in srgb,var(--gold) 70%,transparent);text-underline-offset:4px}
.formats3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.err404{min-height:60vh;display:grid;place-items:center;text-align:center}
.err404 b{font-family:var(--f-display);font-size:120px;color:var(--leaf);line-height:1}
.fgrid{grid-template-columns:1.3fr 1fr 1fr 1fr 1fr}
.fgrid h4 a:hover{color:var(--gold)}
a.frow{transition:background .15s}
a.frow:hover{background:var(--surface)}
a.frow:hover h3{color:var(--leaf)}
.bar a.lab:hover{color:var(--leaf)}
@media (max-width:1024px){
  .intro-grid,.two-col{grid-template-columns:1fr;gap:40px}
  .facts-card{position:static}
  .related,.formats3{grid-template-columns:repeat(2,minmax(0,1fr))}
  .fgrid{grid-template-columns:1fr 1fr}
  .topics,.topics.n7{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width:680px){
  .related,.formats3,.topics,.topics.n7{grid-template-columns:1fr}
  .topics.n7 .topic:first-child{grid-column:auto}
  .fgrid{grid-template-columns:1fr}
}
"""

# ------------------------------------------------------------------ helpers
def href(rel, path): return (rel + path) or "./"

def img(rel, name, alt, cls="", lazy=True, extra=""):
    w, h = IMG_SIZES[name]
    return f'<img src="{rel}assets/img/{name}.jpg" alt="{esc(alt)}" width="{w}" height="{h}"{" loading=%slazy%s decoding=%sasync%s" % ((chr(34),)*4) if lazy else " fetchpriority=%shigh%s" % ((chr(34),)*2)}{(" class=%s%s%s" % (chr(34), cls, chr(34))) if cls else ""}{extra}>'

def pill(it):
    c, l = ST[status(it)]
    return f'<span class="pill {c}" data-st="{it["id"]}">{l}</span>'

def chip(tr):
    T = TRACKS[tr]
    return f'<span class="chip"><span class="leaf t-{T["t"]}">{ic(T["i"])}</span>{esc(T["s"])}</span>'

def pcard(it, rel, with_chip=True):
    T = TRACKS[it["tr"]]
    done = " done" if status(it) == "done" else ""
    return (f'<article class="pcard{done}" id="p-{it["id"]}" data-tr="{it["tr"]}" data-city="{esc(it["c"])}" data-month="{it["m"]}" data-status="{status(it)}" style="--tone:{TONE[T["t"]]}">'
            f'<div class="r1"><div class="dstamp"><b>{it["d1"]}–{it["d2"]}</b><span>{MONTHS[it["m"]]} 2026</span></div>{pill(it)}</div>'
            f'{chip(it["tr"]) if with_chip else ""}<h3>{esc(it["t"])}</h3>'
            f'<div class="r3"><span class="city">{ic("map-pin")} {esc(it["c"])}</span><button class="btn btn-line btn-sm" type="button" data-open="{it["id"]}">التفاصيل والتسجيل {ic("arrow-left")}</button></div></article>')

def lrow(it):
    return (f'<div class="lrow"><div class="dstamp"><b>{it["d1"]}–{it["d2"]}</b><span>{MONTHS[it["m"]]} · {DAYS[it["start"].weekday()]}</span></div>'
            f'<h3>{esc(it["t"])}</h3>{chip(it["tr"])}<span class="city">{ic("map-pin")} {esc(it["c"])}</span>'
            f'<div class="act"><button class="btn btn-line btn-sm" type="button" data-open="{it["id"]}">سجّل {ic("arrow-left")}</button></div></div>')

def faq_html(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{esc(q)} {ic("plus")}</summary><p>{esc(a)}</p></details>' for q, a in faqs) + "</div>"

def sec_head(kicker, h2, lead="", link=""):
    return (f'<div class="sec-head"><div><span class="kicker">{kicker}</span><h2 class="h2">{h2}</h2>'
            f'{f"<p class=%slead%s>{lead}</p>" % (chr(34), chr(34)) if lead else ""}</div>{link}</div>')

def phero(rel, crumbs, h1, lead, side=""):
    cr = f'<a href="{href(rel, "")}">الرئيسية</a>'
    for name, path in crumbs[:-1]:
        cr += f'{ic("chevron-left")}<a href="{href(rel, path)}">{esc(name)}</a>'
    cr += f'{ic("chevron-left")}<span aria-current="page">{esc(crumbs[-1][0])}</span>'
    return (f'<div class="phero"><svg class="mark-bg" aria-hidden="true"><use href="#logo-mark"/></svg><div class="wrap">'
            f'<div><nav class="crumbs" aria-label="مسار التنقل">{cr}</nav><h1>{h1}</h1><p>{lead}</p></div>'
            f'{f"<div class=%sside%s>{side}</div>" % (chr(34), chr(34)) if side else ""}</div></div>')

def side(*pairs): return "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in pairs)

def cta_band(rel, title="هل لدى جهتك احتياج تدريبي محدد؟", text="نصمّم البرنامج بالمحتوى والمدة والمكان الذي يناسب فريقكم، في دبي أو في أي إمارة أو خارج الدولة."):
    return (f'<div class="cta-band"><div class="wrap"><div><h2>{title}</h2><p>{text}</p></div>'
            f'<div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-primary" href="{href(rel, "contact/")}">اطلب عرضاً تدريبياً {ic("arrow-left", "go")}</a>'
            f'<a class="btn btn-line" href="{href(rel, "programs/")}">تقويم البرامج</a></div></div></div>')

# ------------------------------------------------------------------ JSON-LD
ORG_ID = SITE + "#org"
def org_ld():
    return {
        "@type": "EducationalOrganization", "@id": ORG_ID, "name": BRAND_FULL,
        "alternateName": [LEGAL_EN, "Nuhal Al Marifa", "نهال المعرفة"], "url": SITE,
        "logo": SITE + "assets/logo.png", "image": SITE + "assets/og.jpg",
        "description": "مركز تدريب وتطوير مرخّص من هيئة المعرفة والتنمية البشرية في دبي، يقدّم برامج للجهات الحكومية والشركات والأفراد في الإمارات.",
        "email": EMAILS[0], "telephone": PHONES_E164[0],
        "address": {"@type": "PostalAddress", "addressLocality": "Dubai", "addressRegion": "Dubai", "addressCountry": "AE"},
        "areaServed": [{"@type": "City", "name": "Dubai"}, {"@type": "Country", "name": "United Arab Emirates"}],
        "contactPoint": [{"@type": "ContactPoint", "telephone": p, "email": e, "contactType": "customer service", "areaServed": "AE", "availableLanguage": ["ar", "en"]} for p, e in zip(PHONES_E164, EMAILS)],
        "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "license",
                          "recognizedBy": {"@type": "GovernmentOrganization", "name": "Knowledge and Human Development Authority (KHDA)", "url": "https://www.khda.gov.ae/"}},
        "knowsAbout": ["القيادة الحكومية", "الذكاء الاصطناعي", "التحول الرقمي", "الأمن السيبراني", "تجربة المتعامل", "المالية الحكومية", "اللغة الإنجليزية وIELTS", "مهارات الأطفال"],
    }
def crumbs_ld(crumbs):
    items = [("الرئيسية", "")] + list(crumbs)
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(items)]}
def faq_ld(faqs):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
def course_ld(it, page_path):
    T = TRACKS[it["tr"]]; en, cc = CITY_META[it["c"]]
    return {"@type": "Course", "name": it["t"], "url": f'{SITE}{page_path}#p-{it["id"]}', "inLanguage": "ar",
            "description": f'برنامج تدريبي حضوري لمدة خمسة أيام ضمن مسار {T["n"]} من {BRAND_FULL}، ينعقد في {it["c"]} من {it["d1"]} إلى {it["d2"]} {MONTHS[it["m"]]} 2026.',
            "provider": {"@id": ORG_ID},
            "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "Onsite", "startDate": it["start"].strftime("%Y-%m-%d"), "endDate": it["end"].strftime("%Y-%m-%d"),
                                  "courseWorkload": "P5D", "location": {"@type": "Place", "name": it["c"], "address": {"@type": "PostalAddress", "addressLocality": en, "addressCountry": cc}}}}

# ------------------------------------------------------------------ layout
NAV = [("home", "الرئيسية", ""), ("about", "عن الشركة", "about/"), ("programs", "البرامج التدريبية", "programs/"), ("courses", "الدورات", "courses/"),
       ("accreditations", "الاعتمادات", "accreditations/"), ("team", "الفريق", "team/"), ("experience", "الخبرات", "experience/")]
MEGA = {"about": "mAbout", "programs": "mPrograms", "experience": "mExp"}

def ticket_static(rel, cls):
    it = UPCOMING[0] if UPCOMING else SORTED[-1]; T = TRACKS[it["tr"]]
    if cls == "mticket":
        return (f'<span class="lab">{esc(T["s"])}</span><b>{esc(it["t"])}</b><div class="meta"><span>{ic("calendar-days")} {date_txt(it)}</span><span>{ic("map-pin")} {esc(it["c"])}</span></div>'
                f'<a class="btn btn-line btn-sm" href="{href(rel, "programs/" + T["slug"] + "/")}#p-{it["id"]}" style="justify-self:start;color:#fff">التفاصيل {ic("arrow-left")}</a>')
    return (f'<div class="row1"><span class="lab">{ic("calendar-clock")} البرنامج القادم</span>{pill(it)}</div><b>{esc(it["t"])}</b>'
            f'<div class="meta"><span>{ic("calendar-days")} {date_txt(it)}</span><span>{ic("map-pin")} {esc(it["c"])}</span></div>'
            f'<button class="btn btn-primary btn-sm" type="button" data-open="{it["id"]}" style="justify-self:start">التفاصيل والتسجيل {ic("arrow-left")}</button>')

def header(rel, active):
    items = ""
    for key, label, path in NAV:
        cls = "top active" if key == active else "top"
        cur = ' aria-current="page"' if key == active else ""
        if key in MEGA:
            items += (f'<li class="has-mega" data-mega="{MEGA[key]}"><a class="{cls}" href="{href(rel, path)}"{cur}>{label}</a>'
                      f'<button class="mt" type="button" aria-expanded="false" aria-controls="{MEGA[key]}" aria-label="عرض قائمة {label}">{ic("chevron-down")}</button></li>')
        else:
            items += f'<li><a class="{cls}" href="{href(rel, path)}"{cur}>{label}</a></li>'
    mtracks = "".join(f'<a class="mlink" href="{href(rel, "programs/" + T["slug"] + "/")}"><span class="leaf sm t-{T["t"]}">{ic(T["i"])}</span><span><b>{esc(T["s"])}</b><small>{len(by_track[k])} برنامجاً · {"، ".join(cities_of(k))}</small></span></a>' for k, T in enumerate(TRACKS))
    mareas = "".join(f'<a class="mlink" href="{href(rel, "courses/" + A["slug"] + "/")}"><span class="leaf sm t-{A["t"]}">{ic(A["i"])}</span><span><b>{esc(A["n"])}</b><small>{esc(" · ".join(A["tags"]))}</small></span></a>' for A in AREAS)
    dtracks = "".join(f'<a href="{href(rel, "programs/" + T["slug"] + "/")}">{ic(T["i"])} {esc(T["s"])}</a>' for T in TRACKS)
    dareas = "".join(f'<a href="{href(rel, "courses/" + A["slug"] + "/")}">{ic(A["i"])} {esc(A["n"])}</a>' for A in AREAS)
    return f'''
<div class="topbar"><div class="wrap">
  <div class="grp"><span class="it">{ic("badge-check")} مرخّص من <b>هيئة المعرفة والتنمية البشرية KHDA</b></span><span class="it hide-sm">{ic("map-pin")} دبي، الإمارات العربية المتحدة</span></div>
  <div class="grp"><span class="it hide-sm">{ic("phone")} <span class="ltr">{PHONES[0]}</span></span><span class="it">{ic("mail")} <span class="ltr">{EMAILS[0]}</span></span></div>
</div></div>
<header class="site" id="siteHeader">
  <div class="wrap nav-row">
    <a class="brand" href="{href(rel, "")}" aria-label="{BRAND} — الصفحة الرئيسية"><svg role="img" aria-label="شعار {BRAND}"><use href="#logo-full"/></svg></a>
    <nav aria-label="القائمة الرئيسية" style="display:contents"><ul class="menu">{items}</ul></nav>
    <div class="nav-cta">
      <a class="btn btn-primary btn-sm" href="{href(rel, "contact/")}">تواصل معنا {ic("arrow-left", "go")}</a>
      <button class="burger" id="burger" type="button" aria-label="فتح القائمة" aria-expanded="false">{ic("menu")}</button>
    </div>
  </div>
  <div class="mega mega-about" id="mAbout" role="region" aria-label="عن الشركة"><div class="wrap">
    <div><h4>تعرّف على {BRAND}</h4><div class="mlinks">
      <a class="mlink" href="{href(rel, "about/")}"><span class="leaf sm t-leaf">{ic("sprout")}</span><span><b>من نحن</b><small>مركز تدريب وتطوير مرخّص في دبي</small></span></a>
      <a class="mlink" href="{href(rel, "about/")}#name"><span class="leaf sm t-gold">{ic("droplets")}</span><span><b>قصة الاسم</b><small>من المنهل إلى النمو</small></span></a>
      <a class="mlink" href="{href(rel, "about/")}#vision"><span class="leaf sm t-ink">{ic("eye")}</span><span><b>الرؤية والرسالة</b><small>إلى أين نتجه وكيف نصل</small></span></a>
      <a class="mlink" href="{href(rel, "about/")}#values"><span class="leaf sm t-leaf">{ic("gem")}</span><span><b>قيمنا</b><small>خمسة مبادئ تحكم عملنا</small></span></a>
    </div></div>
    <div><h4>أقسام ومبادرات</h4><div class="mlinks">
      <a class="mlink" href="{href(rel, "about/")}#ai-division"><span class="leaf sm t-gold">{ic("brain-circuit")}</span><span><b>قسم جاهزية الذكاء الاصطناعي</b><small>AI &amp; AGI Readiness Division</small></span></a>
      <a class="mlink" href="{href(rel, "team/")}"><span class="leaf sm t-leaf">{ic("users")}</span><span><b>فريق العمل والخبراء</b><small>من يصمّم وينفّذ برامجنا</small></span></a>
      <a class="mlink" href="{href(rel, "accreditations/")}"><span class="leaf sm t-ink">{ic("badge-check")}</span><span><b>الاعتمادات والجودة</b><small>ترخيص KHDA ودورة الجودة</small></span></a>
    </div></div>
    <a class="mfeature" href="{href(rel, "accreditations/")}">{img(rel, "t-burj", "أفق دبي وبرج خليفة عند الغروب")}<span class="in"><span class="kicker" style="color:var(--gold)">ترخيص رسمي</span><b>مرخّصون من هيئة المعرفة والتنمية البشرية في دبي</b><small>ما الذي يعنيه الترخيص لجهتك ولمشاركيك</small></span></a>
  </div></div>
  <div class="mega mega-programs" id="mPrograms" role="region" aria-label="البرامج التدريبية"><div class="wrap">
    <div><h4>البرامج الحكومية · تقويم 2026 <span>{len(ITEMS)} برنامجاً</span></h4><div class="mlinks">{mtracks}</div></div>
    <div><h4>دورات للأفراد والشركات</h4><div class="mlinks">{mareas}</div></div>
    <div style="display:grid;gap:14px;align-content:start"><h4>البرنامج القادم</h4><div class="mticket" id="megaTicket">{ticket_static(rel, "mticket")}</div>
      <a class="btn btn-gold" href="{href(rel, "programs/")}#catalog">{ic("calendar-range")} التقويم الكامل للبرامج</a></div>
  </div></div>
  <div class="mega mega-exp" id="mExp" role="region" aria-label="الخبرات"><div class="wrap">
    <div><h4>من سجل الخبرات</h4><div class="mlinks">
      <a class="mlink" href="{href(rel, "experience/")}#case"><span class="leaf sm t-ink">{ic("building-2")}</span><span><b>بلدية دبي</b><small>برنامجان في التسويق الحكومي والرقمي</small></span></a>
      <a class="mlink" href="{href(rel, "experience/")}#footprint"><span class="leaf sm t-gold">{ic("globe-2")}</span><span><b>الانتشار الجغرافي</b><small>{"، ".join(CITIES)}</small></span></a>
      <a class="mlink" href="{href(rel, "experience/")}#sectors"><span class="leaf sm t-leaf">{ic("layers")}</span><span><b>القطاعات التي نخدمها</b><small>من الحكومات إلى الأطفال</small></span></a>
    </div></div>
    <div><h4>بالأرقام</h4><div class="mfacts"><div class="mfact"><b>2</b><span>برنامجان منفّذان لبلدية دبي</span></div><div class="mfact"><b>{len(CITIES)}</b><span>مدن انعقاد في الربع الرابع</span></div><div class="mfact"><b>{by_city.get("دبي", 0)}</b><span>برنامجاً مجدولاً في دبي</span></div></div></div>
    <a class="mfeature" href="{href(rel, "experience/")}">{img(rel, "t-table", "مدرب يقود نقاشاً مع مشاركين حول طاولة اجتماعات")}<span class="in"><span class="kicker" style="color:var(--gold)">خبرة ميدانية</span><b>برامج تُبنى على واقع الجهة وتُقاس بما يتغيّر بعدها</b><small>استعرض سجل الخبرات</small></span></a>
  </div></div>
</header>
<div class="drawer" id="drawer" aria-hidden="true"><div class="scrim" data-close-drawer></div>
  <nav class="panel" aria-label="قائمة الجوال">
    <div class="dhead"><svg aria-hidden="true"><use href="#logo-full"/></svg><button class="burger" type="button" data-close-drawer aria-label="إغلاق القائمة" style="display:grid">{ic("x")}</button></div>
    <a class="dlink" href="{href(rel, "")}">الرئيسية</a>
    <div class="dacc"><button type="button" aria-expanded="false">عن الشركة {ic("chevron-down")}</button><div class="sub" hidden>
      <a href="{href(rel, "about/")}">{ic("sprout")} من نحن</a><a href="{href(rel, "about/")}#vision">{ic("eye")} الرؤية والرسالة</a><a href="{href(rel, "about/")}#values">{ic("gem")} قيمنا</a><a href="{href(rel, "about/")}#ai-division">{ic("brain-circuit")} قسم جاهزية الذكاء الاصطناعي</a></div></div>
    <div class="dacc"><button type="button" aria-expanded="false">البرامج الحكومية {ic("chevron-down")}</button><div class="sub" hidden><a href="{href(rel, "programs/")}">{ic("calendar-range")} كل البرامج والتقويم</a>{dtracks}</div></div>
    <div class="dacc"><button type="button" aria-expanded="false">الدورات {ic("chevron-down")}</button><div class="sub" hidden><a href="{href(rel, "courses/")}">{ic("grid-2x2")} كل الدورات</a>{dareas}</div></div>
    <a class="dlink" href="{href(rel, "accreditations/")}">الاعتمادات</a>
    <a class="dlink" href="{href(rel, "team/")}">الفريق</a>
    <a class="dlink" href="{href(rel, "experience/")}">الخبرات</a>
    <a class="btn btn-primary" href="{href(rel, "contact/")}" style="margin-top:16px">تواصل معنا {ic("arrow-left", "go")}</a>
    <div style="margin-top:16px;font-size:14px;color:var(--muted);display:grid;gap:6px"><span class="ltr" style="justify-self:start">{PHONES[0]}</span><span class="ltr" style="justify-self:start">{EMAILS[0]}</span></div>
  </nav>
</div>'''

def footer(rel):
    ft = "".join(f'<li><a href="{href(rel, "programs/" + T["slug"] + "/")}">{esc(T["s"])}</a></li>' for T in TRACKS)
    fa = "".join(f'<li><a href="{href(rel, "courses/" + A["slug"] + "/")}">{esc(A["s"])}</a></li>' for A in AREAS)
    return f'''
<footer class="site"><svg class="mark-bg" aria-hidden="true"><use href="#logo-mark"/></svg><div class="wrap">
  <div class="fgrid">
    <div><svg class="flogo" role="img" aria-label="{BRAND}"><use href="#logo-full"/></svg>
      <p>مركز تدريب وتطوير في دبي، يصمّم برامج للقيادات والمؤسسات والأفراد في الإمارات، من الذكاء الاصطناعي إلى المالية الحكومية.</p>
      <span class="khda-mini">{ic("badge-check")} مرخّص من هيئة المعرفة والتنمية البشرية KHDA</span></div>
    <div><h4>الشركة</h4><ul><li><a href="{href(rel, "about/")}">عن الشركة</a></li><li><a href="{href(rel, "accreditations/")}">الاعتمادات</a></li><li><a href="{href(rel, "team/")}">الفريق</a></li><li><a href="{href(rel, "experience/")}">الخبرات</a></li><li><a href="{href(rel, "contact/")}">تواصل معنا</a></li></ul></div>
    <div><h4><a href="{href(rel, "programs/")}">البرامج الحكومية</a></h4><ul>{ft}</ul></div>
    <div><h4><a href="{href(rel, "courses/")}">الدورات</a></h4><ul>{fa}</ul></div>
    <div><h4>تواصل</h4><ul><li class="ltr">{EMAILS[0]}</li><li class="ltr">{EMAILS[1]}</li><li class="ltr">{PHONES[0]}</li><li class="ltr">{PHONES[1]}</li><li>دبي، الإمارات العربية المتحدة</li></ul></div>
  </div>
  <div class="fbottom"><span>© 2026 {BRAND_FULL} ذ.م.م. جميع الحقوق محفوظة.</span><span class="ltr">{LEGAL_EN} · Dubai, UAE</span></div>
</div></footer>'''

MODAL = f'''
<div class="modal" id="modal" hidden role="dialog" aria-modal="true" aria-labelledby="mTitle"><div class="scrim" data-close-modal></div>
  <div class="box"><div class="mh"><button class="x" type="button" data-close-modal aria-label="إغلاق">{ic("x")}</button><div id="mChip"></div><h3 id="mTitle"></h3></div>
    <div class="mb"><div class="facts" id="mFacts"></div>
      <div class="inc"><span>{ic("award")} شهادة إتمام من {BRAND}</span><span>{ic("clipboard-check")} تقييم قبلي وبعدي</span><span>{ic("book-open")} مادة تدريبية للمشارك</span></div>
      <div id="regWrap"></div></div></div></div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>'''

def page(path, active, title, desc, body, ld=None, og_img="og", og_type="website"):
    depth = path.count("/")
    rel = "../" * depth
    canonical = SITE + path
    graph = [org_ld()] + (ld or [])
    ldjson = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    og_url = SITE + ("assets/og.jpg" if og_img == "og" else f"assets/img/{og_img}.jpg")
    doc = f'''<!doctype html>
<html lang="ar-AE" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="ar-AE" href="{canonical}">
<link rel="alternate" hreflang="x-default" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{BRAND_FULL}">
<meta property="og:locale" content="ar_AE">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_url}">
<meta property="og:image:alt" content="{esc(BRAND_FULL)} — دبي">
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
<body data-rel="{rel}" data-page="{active}">
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="logo-full" viewBox="40 46 654 350">{LOGO_FULL}</symbol><symbol id="logo-mark" viewBox="44 50 280 297">{LOGO_MARK}</symbol></svg>
<a class="sr" href="#main">تخطَّ إلى المحتوى</a>
{header(rel, active)}
<main id="main">
{body.replace("{REL}", rel)}
</main>
{footer(rel)}
{MODAL}
<script src="https://unpkg.com/lucide@0.344.0/dist/umd/lucide.min.js" defer></script>
<script src="{rel}assets/js/site.js" defer></script>
</body>
</html>
'''
    out = os.path.join(OUT, path, "index.html") if path.endswith("/") or path == "" else os.path.join(OUT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(doc)
    PAGES.append(dict(path=path, title=title, desc=desc, h1=re.search(r"<h1[^>]*>(.*?)</h1>", doc, re.S).group(1)))

PAGES = []
SHARED_FAQ_CERT = ("هل يحصل المشارك على شهادة؟", "يحصل كل مشارك يستوفي متطلبات الحضور والتقييم على شهادة إتمام من نُهال المعرفة، المركز المرخّص من هيئة المعرفة والتنمية البشرية في دبي (KHDA)، تحمل اسم البرنامج وعدد ساعاته وتاريخ انعقاده.")

# ------------------------------------------------------------------ section builders
def tracks_grid(rel, feature=True):
    order = [5, 0, 1, 2, 3, 4, 6]
    out = []
    for idx, k in enumerate(order):
        T = TRACKS[k]; n = len(by_track[k]); cs = cities_of(k)
        url = href(rel, "programs/" + T["slug"] + "/")
        if idx == 0 and feature:
            out.append(f'<a class="track feature" href="{url}"><svg class="mark-bg" aria-hidden="true"><use href="#logo-mark"/></svg><span class="leaf lg t-gold">{ic(T["i"])}</span><h3>{esc(T["n"])}</h3><p>{esc(T["card"])}</p><div class="tags">{"".join(f"<span>{esc(t)}</span>" for t in T["tags"])}</div><div class="foot"><span><b>{n}</b> برنامجاً · {len(cs)} مدن</span>{ic("arrow-left", "go")}</div></a>')
        else:
            out.append(f'<a class="track" href="{url}"><span class="leaf t-{T["t"]}">{ic(T["i"])}</span><h3>{esc(T["n"])}</h3><p>{esc(T["card"])}</p><div class="foot"><span><b>{n}</b> برنامجاً</span>{ic("arrow-left", "go")}</div></a>')
    return '<div class="tracks">' + "".join(out) + "</div>"

def areas_grid(rel):
    return '<div class="areas">' + "".join(
        f'<a class="area" href="{href(rel, "courses/" + A["slug"] + "/")}"><div class="ph">{img(rel, A["img"], A["n"] + " في دبي")}</div><div class="bd"><span class="leaf t-{A["t"]}">{ic(A["i"])}</span><h3>{esc(A["n"])}</h3><p>{esc(A["card"])}</p><span class="more">تفاصيل الدورات {ic("arrow-left")}</span></div></a>' for A in AREAS) + "</div>"

WHY = [("badge-check", "leaf", "ترخيص من KHDA", "مرخّصون من هيئة المعرفة والتنمية البشرية في دبي، ونلتزم بمعايير التعليم في الدولة."),
       ("user-check", "gold", "مدربون من الميدان", "خبراء يجمعون بين التأهيل الأكاديمي والخبرة العملية في القطاع الذي يدرّبون فيه."),
       ("users", "ink", "المتعلّم في المركز", "جداول مرنة ومجموعات صغيرة واهتمام فردي بكل مشارك."),
       ("monitor-smartphone", "leaf", "مرافق حديثة", "قاعات تدريب ومختبرات حاسوب وموارد تعلّم مجهّزة لبيئة تعلّم مريحة."),
       ("layers", "gold", "محفظة شاملة", "برامج تغطي كل مراحل التطوير، من الأطفال إلى القيادات التنفيذية."),
       ("target", "ink", "نتائج قابلة للقياس", "نركّز على مهارات تُطبَّق في العمل وتقدّم وظيفي يمكن رصده.")]
def why_section(rel, title="ما الذي يجعل التدريب معنا مختلفاً", photo="t-board"):
    items = "".join(f'<div class="why-item"><span class="leaf sm t-{t}">{ic(i)}</span><div><h3>{a}</h3><p>{b}</p></div></div>' for i, t, a, b in WHY)
    return (f'<section class="section on-surface why"><div class="wrap"><div class="framed">{img(rel, photo, "مدرب يشرح لمجموعة من المشاركين في قاعة تدريب في دبي")}<span class="tag">{ic("badge-check")} ترخيص KHDA</span></div>'
            f'<div><span class="kicker">لماذا نُهال المعرفة</span><h2 class="h2">{title}</h2><div class="why-list">{items}</div></div></div></section>')

def related_tracks(rel, skip):
    return '<div class="related">' + "".join(f'<a class="rel" href="{href(rel, "programs/" + T["slug"] + "/")}"><span class="leaf sm t-{T["t"]}">{ic(T["i"])}</span><span><b>{esc(T["s"])}</b><small>{len(by_track[k])} برنامجاً</small></span>{ic("arrow-left", "go")}</a>' for k, T in enumerate(TRACKS) if k != skip) + "</div>"

def related_areas(rel, skip):
    return '<div class="related">' + "".join(f'<a class="rel" href="{href(rel, "courses/" + A["slug"] + "/")}"><span class="leaf sm t-{A["t"]}">{ic(A["i"])}</span><span><b>{esc(A["n"])}</b><small>{esc(" · ".join(A["tags"][:2]))}</small></span>{ic("arrow-left", "go")}</a>' for k, A in enumerate(AREAS) if k != skip) + "</div>"

# ================================================================== PAGES
def build_home():
    rel = ""
    up = UPCOMING[:5] or SORTED[-5:]
    stats = "".join(f'<div class="stat"><b>{n}</b><span>{l}</span></div>' for n, l in [(len(ITEMS), "برنامجاً في تقويم الربع الرابع 2026"), (len(TRACKS), "مسارات تخصصية حكومية ومؤسسية"), (len(CITIES), "مدن انعقاد بين دبي ووجهات دولية"), (len(AREAS), "مجالات دورات للأفراد والشركات")])
    faqs = [
        ("هل نُهال المعرفة مركز تدريب مرخّص في دبي؟", "نعم، نُهال المعرفة للتدريب والتطوير مرخّصة من هيئة المعرفة والتنمية البشرية في دبي (KHDA)، الجهة المنظّمة لقطاع التعليم الخاص في الإمارة."),
        ("ما البرامج التي يقدّمها المركز؟", f"نقدّم {len(ITEMS)} برنامجاً حكومياً متخصصاً في تقويم الربع الرابع 2026 ضمن {len(TRACKS)} مسارات، منها القيادة والذكاء الاصطناعي والتحول الرقمي والأمن السيبراني والمالية الحكومية، إلى جانب دورات للأفراد والشركات في الإدارة والحاسوب واللغات والمهارات المهنية وبرامج الأطفال."),
        ("أين تُعقد البرامج التدريبية؟", f"تُعقد معظم البرامج في دبي، وبعضها في {ar_join([c for c in CITIES if c != 'دبي'])}. ويمكن تنفيذ أي برنامج داخل مقر الجهة في أي إمارة."),
        ("كيف أسجّل في برنامج أو أطلب برنامجاً مخصصاً؟", f"اختر البرنامج من التقويم واضغط «التفاصيل والتسجيل»، أو تواصل معنا على {EMAILS[0]} أو {PHONES[0]}، وسنعود إليك خلال يوم عمل."),
    ]
    body = f'''
<div class="hero"><div class="wrap">
  <div class="hero-copy">
    <span class="badge-line"><span class="dot">{ic("badge-check")}</span>مركز تدريب <b>مرخّص من KHDA</b> في دبي</span>
    <h1><span class="h1-kw">مركز تدريب وتطوير في دبي، الإمارات</span>نروي المعرفة،<br>فتنمو <em>الكفاءات<svg viewBox="0 0 200 20" preserveAspectRatio="none" aria-hidden="true"><path d="M3 15 C 50 4, 120 4, 197 10" fill="none" stroke="var(--gold)" stroke-width="5" stroke-linecap="round"/></svg></em></h1>
    <p class="lead">{BRAND_FULL} تصمّم برامج تدريبية للجهات الحكومية والشركات والأفراد في دبي والإمارات: القيادة، والذكاء الاصطناعي، والابتكار، والأمن السيبراني، والمالية الحكومية، إلى جانب دورات اللغات والحاسوب والمهارات المهنية وبرامج الأطفال.</p>
    <div class="hero-ctas"><a class="btn btn-primary" href="programs/">{ic("calendar-days")} تصفّح تقويم البرامج</a><a class="btn btn-line" href="contact/">اطلب برنامجاً مخصصاً لجهتك {ic("arrow-left", "go")}</a></div>
    <div class="hero-meta"><div>{ic("landmark")} برامج للقطاع الحكومي</div><div>{ic("building")} حلول للشركات</div><div>{ic("graduation-cap")} دورات للأفراد والطلاب</div></div>
  </div>
  <div class="media"><span class="blk b-gold"></span><span class="blk b-leaf"></span>
    <div class="photo">{img(rel, "hero", "جلسة تدريبية لقيادات حكومية في قاعة تطل على أفق دبي", lazy=False)}</div>
    <svg class="arrow" viewBox="0 0 160 170" aria-hidden="true"><path class="draw" d="M8 162 C 40 140, 70 110, 92 70 S 128 18, 140 12"/><path class="head" d="M112 10 L 142 10 L 140 40"/></svg>
    <div class="ticket" id="heroTicket">{ticket_static(rel, "ticket")}</div>
  </div>
</div></div>
<div class="wrap"><div class="stats">{stats}</div></div>

<section class="section"><div class="wrap">
  {sec_head("القادم في التقويم", "مقاعد متاحة في البرامج القادمة", "مواعيد من خطة برامج الربع الرابع (أكتوبر – ديسمبر 2026) في دبي ووجهات دولية. اختر البرنامج وأرسل طلب التسجيل خلال دقيقة.", f'<a class="link-go" href="programs/#catalog">التقويم الكامل {ic("arrow-left")}</a>')}
  <div class="ledger" id="upcoming">{"".join(lrow(x) for x in up)}</div>
</div></section>

<section class="section on-surface"><div class="wrap">
  {sec_head("البرامج الحكومية", "سبعة مسارات تغطي أولويات العمل الحكومي في الإمارات", "كل مسار مجموعة برامج مترابطة، تبدأ من المفاهيم الاستراتيجية وتنتهي بأدوات تطبيقية يستخدمها المشارك في عمله في اليوم التالي.", f'<a class="link-go" href="programs/">كل البرامج {ic("arrow-left")}</a>')}
  {tracks_grid(rel)}
</div></section>

<section class="section"><div class="wrap">
  {sec_head("دورات للأفراد والشركات", "دورات تدريبية في دبي لكل مرحلة من مراحل التطوير", "من الإدارة والحاسوب واللغات إلى المهارات المهنية وبرامج الأطفال، في مركز مرخّص بدبي.", f'<a class="link-go" href="courses/">كل الدورات {ic("arrow-left")}</a>')}
  {areas_grid(rel)}
</div></section>

<section class="section on-dark ai-band"><div class="wrap">
  <div><span class="kicker">AI &amp; AGI Readiness Division</span>
    <h2 class="h2">نُعدّ المؤسسات في الإمارات للعمل جنباً إلى جنب مع الأنظمة الذكية</h2>
    <p class="lead">قسم متخصص بالكامل للذكاء الاصطناعي وللمرحلة الانتقالية نحو الذكاء الاصطناعي العام. لا نكتفي بتعليم الأدوات؛ نُعدّ الجهات لحوكمة الأنظمة الذكية وقيادة العمل معها.</p>
    <div class="pillars">
      <div class="pillar"><span class="leaf t-gold">{ic("map")}</span><div><h3>الاستراتيجية والجاهزية</h3><p>خرائط طريق 2030 وتقييم جاهزية الجهة في الحوكمة والموارد البشرية والتقنية.</p></div></div>
      <div class="pillar"><span class="leaf t-leaf">{ic("shield-check")}</span><div><h3>الحوكمة والاستخدام المسؤول</h3><p>سياسات الاستخدام الآمن وحماية البيانات وإدارة مخاطر النماذج.</p></div></div>
      <div class="pillar"><span class="leaf t-ink">{ic("workflow")}</span><div><h3>التطبيق في العمل اليومي</h3><p>هندسة الأوامر وCopilot وأتمتة العمليات والوكلاء الأذكياء Agentic AI.</p></div></div>
    </div>
    <div style="margin-top:28px"><a class="btn btn-gold" href="programs/government-ai/">دورات الذكاء الاصطناعي الحكومي {ic("arrow-left", "go")}</a></div>
  </div>
  <div class="ai-media"><span class="frame"></span>{img(rel, "ai", "رقاقة ذكاء اصطناعي مضيئة على لوحة دوائر إلكترونية")}<div class="count"><b>{AI_COUNT}</b><span>برنامجاً مرتبطاً بالذكاء الاصطناعي في تقويم هذا الربع</span></div></div>
</div></section>

<section class="section"><div class="wrap">
  {sec_head("لمن نصمّم برامجنا", "من مجالس القيادة إلى قاعات الأطفال")}
  <div class="aud">
    <div><span class="leaf t-ink">{ic("landmark")}</span><h3>الجهات الحكومية</h3><p>برامج قيادية وتخصصية مرتبطة بمؤشرات الأداء ومستهدفات التحول الحكومي في الإمارات.</p></div>
    <div><span class="leaf t-leaf">{ic("building-2")}</span><h3>الشركات والمؤسسات</h3><p>رفع كفاءة الفرق في الإدارة والتقنية والمبيعات وخدمة العملاء.</p></div>
    <div><span class="leaf t-gold">{ic("briefcase")}</span><h3>المهنيون والأفراد</h3><p>مسارات للتقدّم الوظيفي واللغات والمهارات الرقمية والتحضير لـ IELTS.</p></div>
    <div><span class="leaf t-leaf">{ic("blocks")}</span><h3>الطلاب والأطفال</h3><p>دعم أكاديمي وبرامج تنمية مهارات مناسبة للعمر في بيئة آمنة.</p></div>
  </div>
</div></section>

{why_section(rel)}

<section class="section"><div class="wrap">
  {sec_head("منهجية العمل", "من الاحتياج إلى الأثر في أربع مراحل")}
  <div class="steps">
    <div class="step"><span class="n">01</span><h3>التشخيص</h3><p>نحلّل احتياج الجهة وفجوات الأداء قبل اقتراح أي محتوى.</p></div>
    <div class="step"><span class="n">02</span><h3>التصميم</h3><p>نبني مخرجات تعلّم واضحة وحالات عملية من واقع القطاع.</p></div>
    <div class="step"><span class="n">03</span><h3>التنفيذ</h3><p>تدريب تفاعلي يقوده خبراء ميدانيون، في دبي أو خارجها.</p></div>
    <div class="step"><span class="n">04</span><h3>القياس</h3><p>تقييم قبلي وبعدي وتقرير أثر يُسلَّم للجهة بعد البرنامج.</p></div>
  </div>
</div></section>

<section class="section on-surface"><div class="wrap two-col">
  <article class="seo-article">
    <span class="kicker">التدريب في دبي</span>
    <h2 class="h2">لماذا تختار مركز تدريب مرخّصاً في دبي؟</h2>
    <p>دبي من أكثر مدن المنطقة استثماراً في رأس المال البشري، وتعمل جهاتها الحكومية وشركاتها وفق معايير أداء عالية تتطلب تطويراً مستمراً للمهارات. اختيار مركز تدريب مرخّص من <a href="accreditations/">هيئة المعرفة والتنمية البشرية</a> يمنحك ضماناً بأن البرنامج يخضع لإطار تنظيمي واضح، وأن الشهادة صادرة عن جهة معتمدة للعمل في القطاع.</p>
    <p>في نُهال المعرفة نجمع بين هذا الالتزام التنظيمي وفهم عميق لاحتياجات السوق الإماراتي: <a href="programs/">برامج حكومية</a> مرتبطة بمستهدفات التحول والتميز، و<a href="programs/government-ai/">دورات ذكاء اصطناعي</a> عملية تواكب توجه الدولة، و<a href="courses/">دورات للأفراد والشركات</a> في الإدارة والحاسوب و<a href="courses/languages/">اللغة الإنجليزية وIELTS</a>.</p>
  </article>
  <div>{sec_head("أسئلة شائعة", "قبل أن تبدأ")}{faq_html(faqs)}</div>
</div></section>
{cta_band(rel)}'''
    page("", "home", "نُهال المعرفة | مركز تدريب وتطوير مرخّص في دبي",
         "مركز تدريب مرخّص من KHDA في دبي. برامج للجهات الحكومية والشركات والأفراد في الذكاء الاصطناعي والقيادة والمالية واللغات. تصفّح تقويم 2026 وسجّل.",
         body, ld=[{"@type": "WebSite", "@id": SITE + "#website", "url": SITE, "name": BRAND_FULL, "inLanguage": "ar-AE", "publisher": {"@id": ORG_ID}}, faq_ld(faqs)])

def build_about():
    rel = "../"
    crumbs = [("عن الشركة", "about/")]
    body = f'''
{phero(rel, crumbs, "عن نُهال المعرفة: مركز تدريب وتطوير في دبي", "مركز تدريب وتطوير مرخّص في دبي، يخدم المهنيين والطلاب والأطفال وفرق العمل في الجهات الحكومية والخاصة في الإمارات.", side(("KHDA", "ترخيص رسمي"), (len(AREAS) + len(TRACKS), "مسارات ومجالات")))}
<section class="section"><div class="wrap split">
  <div class="prose"><span class="kicker">من نحن</span><h2 class="h2">شريك تعلّم يفهم احتياجات سوق دبي والإمارات</h2>
    <p>{BRAND_FULL} مركز تدريب وتطوير مقرّه دبي، ومرخّص من هيئة المعرفة والتنمية البشرية (KHDA)، بما يضمن أن تلتزم برامجنا بأعلى معايير الجودة في التعليم والتدريب المهني.</p>
    <p>نعمل على تمكين الأفراد والمؤسسات عبر برامج عالية الجودة تدعم النمو المستمر وتطوير المهارات والتعلّم مدى الحياة. نؤمن أن المعرفة أساس التقدّم، ونلتزم بتجارب تعلّم مبتكرة وعملية تقود إلى نتائج.</p>
    <p>بفريق من المدربين والتربويين ذوي الخبرة، ومرافق حديثة، ونهج يضع المتعلّم أولاً، نخدم شريحة واسعة تشمل المهنيين والطلاب والأطفال وفرق الشركات والجهات الحكومية، مع خيارات تعلّم مرنة تواكب احتياجات سوق دبي والإمارات.</p>
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:26px"><a class="btn btn-primary" href="{rel}programs/">البرامج الحكومية</a><a class="btn btn-line" href="{rel}courses/">دورات الأفراد والشركات</a></div>
  </div>
  <div class="framed">{img(rel, "t-monitor", "مشاركان يعملان على شاشة حاسوب خلال جلسة تدريب عملية في دبي")}<span class="tag">{ic("map-pin")} دبي، الإمارات</span></div>
</div></section>
<section class="section tight" id="name"><div class="wrap"><div class="name-card">
  <div class="word">نُهال<small>NUHAL · نُهّال المعرفة</small></div>
  <dl><div><dt>من أين جاء الاسم؟</dt><dd>«نَهِلَ» في العربية تعني شرب من المَنهَل، وهو مورد الماء. والنُّهّال هم من يَرِدون المنهل ليشربوا منه. وهكذا نرى المتدربين: باحثين يقصدون منابع المعرفة الأولى.</dd></div>
  <div><dt>وماذا يقول الشعار؟</dt><dd>أوراق خضراء ترتوي فتنمو، وسهم ذهبي يصعد من بينها. معرفة تُروى، ثم أداء يرتفع ويمكن قياسه.</dd></div></dl>
</div></div></section>
<section class="section on-surface" id="vision"><div class="wrap">
  {sec_head("الرؤية والرسالة", "إلى أين نتجه، وكيف نصل")}
  <div class="vm"><div class="v"><h3><span class="leaf t-leaf">{ic("eye")}</span>رؤيتنا</h3><p>أن نكون المنارة الاستراتيجية الرائدة في التدريب المهني وتنمية رأس المال البشري، نمكّن الأفراد والمؤسسات عبر منظومات تعلّم مبتكرة وذكية ومستدامة، ونسهم في بناء كوادر تنافسية جاهزة للمستقبل.</p></div>
  <div class="m"><h3><span class="leaf t-ink">{ic("target")}</span>رسالتنا</h3><p>تقديم حلول تدريب وتطوير بمعايير عالمية عبر منهجيات مبتكرة وتيسير احترافي وبرامج مصممة حسب الاحتياج، مع ترسيخ ثقافة التعلّم المستمر وتعزيز الكفاءات المهنية وتحقيق قيمة قابلة للقياس تدفع النمو المستدام لعملائنا وشركائنا.</p></div></div>
</div></section>
<section class="section" id="values"><div class="wrap">
  {sec_head("قيمنا", "خمسة مبادئ تحكم كل برنامج نقدّمه")}
  <div class="values">
    <div><span class="leaf t-gold">{ic("award")}</span><h3>التميّز</h3><p>أعلى المعايير في تصميم المناهج وتقديم التدريب والتعامل مع العملاء.</p></div>
    <div><span class="leaf t-leaf">{ic("lightbulb")}</span><h3>الابتكار</h3><p>دمج مستمر لتقنيات التعلّم الحديثة والمنظومات الذكية والمنهجيات الإبداعية.</p></div>
    <div><span class="leaf t-ink">{ic("heart-handshake")}</span><h3>التمكين</h3><p>نزوّد الأفراد والفرق بالأدوات العملية والثقة اللازمة للقيادة في مجالاتهم.</p></div>
    <div><span class="leaf t-leaf">{ic("sprout")}</span><h3>الاستدامة</h3><p>ندعم النمو المهني طويل المدى والممارسات التي تلبّي متطلبات الغد.</p></div>
    <div><span class="leaf t-gold">{ic("scale")}</span><h3>النزاهة</h3><p>شفافية كاملة واحترافية ومسؤولية أخلاقية في كل شراكاتنا.</p></div>
  </div>
</div></section>
<section class="section on-dark ai-band" id="ai-division"><div class="wrap">
  <div class="ai-media"><span class="frame"></span>{img(rel, "ai", "رقاقة ذكاء اصطناعي مضيئة على لوحة دوائر إلكترونية")}</div>
  <div><span class="kicker">قسم جاهزية الذكاء الاصطناعي والذكاء الاصطناعي العام</span><h2 class="h2">استباق الأفق بدل اللحاق به</h2>
    <p class="lead">في مرحلة يتسارع فيها التغيير التقني، خرجت نُهال المعرفة عن نماذج التدريب التقليدية بقسم مخصّص للذكاء الاصطناعي ولمرحلة الانتقال نحو الذكاء الاصطناعي العام (AGI). نُعدّ المؤسسات للتعايش مع الأنظمة الذكية المستقلة، وحوكمتها، وقيادة العمل إلى جانبها.</p>
    <div style="margin-top:28px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-gold" href="{rel}programs/government-ai/">دورات الذكاء الاصطناعي الحكومي {ic("arrow-left", "go")}</a><a class="btn btn-line" href="{rel}programs/digital-transformation/">التحول الرقمي</a></div>
  </div>
</div></section>
<section class="section" id="gallery"><div class="wrap">
  {sec_head("التعلّم في الميدان", "قاعات تفاعلية، لا محاضرات صامتة")}
  <div class="gallery">
    <figure>{img(rel, "act-1", "قاعة تدريب ممتلئة بالمشاركين أمام شاشة عرض")}<figcaption>جلسات عامة بمشاركة واسعة</figcaption></figure>
    <figure>{img(rel, "act-2", "ورشة تفكير تصميمي بأوراق ملاحظات ملوّنة على الجدار")}<figcaption>ورش تفكير تصميمي</figcaption></figure>
    <figure>{img(rel, "t-present", "مدربة تقدّم عرضاً عن القيادة والاستراتيجية")}<figcaption>القيادة والاستراتيجية</figcaption></figure>
    <figure>{img(rel, "act-3", "نقاش بين مشاركين حول حاسوب محمول")}<figcaption>تطبيق عملي على الأدوات</figcaption></figure>
    <figure>{img(rel, "t-laptop", "مشاركة تعمل على حاسوب محمول في قاعة تدريب")}<figcaption>مختبرات رقمية</figcaption></figure>
  </div>
</div></section>
{cta_band(rel, "ابدأ رحلة التطوير مع نُهال المعرفة", "أخبرنا بما تحتاجه جهتك أو فريقك، وسنقترح البرنامج المناسب خلال يوم عمل.")}'''
    page("about/", "about", "عن نُهال المعرفة | مركز تدريب في دبي مرخّص من KHDA",
         "تعرّف على نُهال المعرفة للتدريب والتطوير في دبي: قصتنا ورؤيتنا ورسالتنا وقيمنا وقسم جاهزية الذكاء الاصطناعي، وكيف نخدم الأفراد والمؤسسات في الإمارات.",
         body, ld=[crumbs_ld(crumbs), {"@type": "AboutPage", "name": "عن نُهال المعرفة", "url": SITE + "about/", "about": {"@id": ORG_ID}, "inLanguage": "ar-AE"}])

def build_programs_hub():
    rel = "../"
    crumbs = [("البرامج التدريبية", "programs/")]
    chips = f'<button class="fchip" type="button" data-tr="-1" aria-pressed="true">{ic("layout-grid")} كل المسارات <b>{len(ITEMS)}</b></button>' + "".join(f'<button class="fchip" type="button" data-tr="{k}" aria-pressed="false">{ic(T["i"])} {esc(T["s"])} <b>{len(by_track[k])}</b></button>' for k, T in enumerate(TRACKS))
    city_opts = "".join(f'<option value="{esc(c)}">{esc(c)} ({by_city[c]})</option>' for c in CITIES)
    faqs = [
        ("ما مدة البرامج التدريبية الحكومية؟", "مدة كل برنامج في التقويم خمسة أيام تدريبية من الأحد إلى الخميس، ويمكن تعديل المدة في البرامج المخصصة لجهة واحدة."),
        ("أين تُعقد البرامج؟", f"تُعقد البرامج في {ar_join(CITIES)}. دبي هي المقر الرئيسي وتستضيف {by_city.get('دبي', 0)} برنامجاً من أصل {len(ITEMS)} في تقويم الربع الرابع 2026."),
        ("هل يمكن تنفيذ برنامج غير موجود في التقويم؟", "نعم، نصمّم برامج مخصصة بالكامل حسب احتياج الجهة، في دبي أو أي إمارة أو خارج الدولة. أرسل لنا احتياجك من صفحة التواصل."),
        ("كيف أسجّل أو أسجّل فريقاً من جهتي؟", "افتح البرنامج واضغط «التفاصيل والتسجيل»، واكتب عدد المشاركين في نموذج الطلب. نؤكد المقاعد والرسوم بالبريد خلال يوم عمل."),
        SHARED_FAQ_CERT,
    ]
    body = f'''
{phero(rel, crumbs, "برامج تدريبية حكومية في دبي والإمارات 2026", f"{len(ITEMS)} برنامجاً للجهات الحكومية والمؤسسات في {len(TRACKS)} مسارات تخصصية، تُعقد في دبي ووجهات دولية خلال الربع الرابع من 2026.", side((len(ITEMS), "برنامجاً"), (len(TRACKS), "مسارات"), (len(CITIES), "مدن")))}
<section class="section"><div class="wrap">
  <div class="intro-grid"><div class="prose seo-article">
    <span class="kicker">التدريب الحكومي</span><h2 class="h2">برامج مصممة لأولويات العمل الحكومي في الإمارات</h2>
    <p>تعمل الجهات الحكومية في دبي والإمارات على مستهدفات واضحة في التحول الرقمي، وتجربة المتعامل، والكفاءة المالية، والجاهزية للمستقبل. صمّمت نُهال المعرفة تقويم برامجها لهذه الأولويات تحديداً، فجاء في سبعة مسارات يكمل بعضها بعضاً، من <a href="government-leadership/">القيادة الحكومية</a> و<a href="government-ai/">الذكاء الاصطناعي</a> إلى <a href="finance-accounting/">المالية والتدقيق</a>.</p>
    <p>كل برنامج خمسة أيام تطبيقية، يقودها خبراء من الميدان، وتنتهي بأدوات يستخدمها المشارك في جهته. يمكنك التسجيل الفردي في أي برنامج، أو طلب تنفيذه لفريق جهتك بالكامل.</p>
  </div>
  <aside class="facts-card"><h2>التقويم في سطور</h2>
    <div class="row"><span class="leaf sm t-leaf">{ic("calendar-range")}</span><div><small>الفترة</small><b>أكتوبر – ديسمبر 2026</b></div></div>
    <div class="row"><span class="leaf sm t-gold">{ic("clock")}</span><div><small>مدة البرنامج</small><b>5 أيام (الأحد – الخميس)</b></div></div>
    <div class="row"><span class="leaf sm t-ink">{ic("map-pin")}</span><div><small>مدن الانعقاد</small><b>{"، ".join(CITIES)}</b></div></div>
    <div class="row"><span class="leaf sm t-leaf">{ic("award")}</span><div><small>الشهادة</small><b>شهادة إتمام من مركز مرخّص من KHDA</b></div></div>
    <a class="btn btn-primary" href="#catalog">{ic("calendar-days")} انتقل إلى التقويم</a>
  </aside></div>
</div></section>
<section class="section on-surface"><div class="wrap">
  {sec_head("المسارات", "اختر المسار المناسب لجهتك", "لكل مسار صفحة مفصّلة بالمخرجات والفئات المستهدفة ومواعيد برامجه.")}
  {tracks_grid(rel)}
</div></section>
<section class="section" id="catalog" style="padding-top:72px"><div class="wrap">
  {sec_head("تقويم الربع الرابع 2026", "كل البرامج والمواعيد", "صفِّ حسب المسار أو المدينة أو الشهر، ثم افتح البرنامج لإرسال طلب التسجيل.")}
</div>
<div class="toolbar"><div class="wrap">
  <div class="tb-row">
    <div class="field">{ic("search")}<label for="q" class="sr">ابحث في البرامج</label><input class="input" id="q" type="search" placeholder="ابحث بعنوان البرنامج، مثل: الحوكمة، Copilot، الموازنات"></div>
    <label for="fCity" class="sr">المدينة</label><select class="select" id="fCity"><option value="">كل المدن</option>{city_opts}</select>
    <label for="fMonth" class="sr">الشهر</label><select class="select" id="fMonth"><option value="">كل الأشهر</option><option value="10">أكتوبر</option><option value="11">نوفمبر</option><option value="12">ديسمبر</option></select>
    <label class="check"><input type="checkbox" id="fPast"> إظهار البرامج المنعقدة</label>
  </div>
  <div class="chips" id="trackChips" role="group" aria-label="تصفية حسب المسار">{chips}</div>
</div></div>
<div class="wrap">
  <div class="result-line"><span id="resultCount"><b>{len(ITEMS)}</b> برنامجاً</span><button class="copy-btn" type="button" id="resetFilters">{ic("rotate-ccw")} إعادة ضبط التصفية</button></div>
  <div class="pgrid" id="pgrid">{"".join(pcard(x, rel) for x in SORTED)}</div>
  <div class="empty" id="emptyState" hidden>{ic("search-x")}<b style="color:var(--heading);font-family:var(--f-display)">لا توجد برامج مطابقة</b><span>جرّب مساراً أو مدينة أخرى، أو فعّل «إظهار البرامج المنعقدة».</span></div>
</div></section>
<section class="section on-surface"><div class="wrap two-col">
  <div>{sec_head("أسئلة شائعة", "عن البرامج الحكومية")}{faq_html(faqs)}</div>
  <div><span class="kicker">دورات للأفراد والشركات</span><h2 class="h2">تبحث عن دورة لك أو لفريق شركتك؟</h2><p class="lead">إلى جانب البرامج الحكومية، نقدّم في دبي دورات في الإدارة والحاسوب واللغات والمهارات المهنية وبرامج الأطفال.</p>
    <div class="related" style="grid-template-columns:1fr;margin-top:24px">{"".join(f'<a class="rel" href="{rel}courses/{A["slug"]}/"><span class="leaf sm t-{A["t"]}">{ic(A["i"])}</span><span><b>{esc(A["n"])}</b><small>{esc(" · ".join(A["tags"]))}</small></span>{ic("arrow-left", "go")}</a>' for A in AREAS[:4])}</div>
    <a class="link-go" href="{rel}courses/" style="margin-top:18px">كل الدورات {ic("arrow-left")}</a></div>
</div></section>
{cta_band(rel)}'''
    ld = [crumbs_ld(crumbs), faq_ld(faqs), {"@type": "ItemList", "name": "مسارات البرامج التدريبية الحكومية", "itemListElement": [{"@type": "ListItem", "position": k + 1, "url": SITE + "programs/" + T["slug"] + "/", "name": T["n"]} for k, T in enumerate(TRACKS)]}]
    page("programs/", "programs", "برامج تدريبية حكومية في دبي 2026 | نُهال المعرفة",
         f"{len(ITEMS)} برنامجاً تدريبياً للجهات الحكومية في دبي والإمارات: القيادة، الذكاء الاصطناعي، الابتكار، الأمن السيبراني والمالية. اطّلع على مواعيد 2026 وسجّل.",
         body, ld=ld)

def build_track(k):
    T = TRACKS[k]; rel = "../../"; path = f'programs/{T["slug"]}/'
    crumbs = [("البرامج التدريبية", "programs/"), (T["s"], path)]
    items = by_track[k]; cs = cities_of(k)
    cnt_city = {c: sum(1 for x in items if x["c"] == c) for c in cs}
    open_n = sum(1 for x in items if status(x) != "done")
    faqs = list(T["faq"]) + [
        (f"أين ومتى تُعقد برامج {T['s']}؟", f"تُعقد برامج المسار خلال الربع الرابع من 2026 في {ar_join(cs)}، ومدة كل برنامج خمسة أيام من الأحد إلى الخميس. المواعيد التفصيلية لكل برنامج منشورة في هذه الصفحة."),
        (f"هل يمكن تنفيذ برامج {T['s']} داخل جهتنا؟", "نعم، يمكن تصميم أي برنامج من هذا المسار كبرنامج مخصص لجهة واحدة بالمحتوى والمدة والموعد المناسب، في مقر الجهة بأي إمارة أو خارج الدولة."),
        SHARED_FAQ_CERT,
    ]
    aud = "".join(f'<li>{ic("user-round-check")}<span>{esc(a)}</span></li>' for a in T["audience"])
    outc = "".join(f'<li>{ic("check")}<span>{esc(o)}</span></li>' for o in T["outcomes"])
    city_line = "، ".join(f"{c} ({cnt_city[c]})" for c in cs)
    body = f'''
{phero(rel, crumbs, esc(T["h1"]), esc(T["lead"]), side((len(items), "برنامجاً"), (len(cs), "مدن" if len(cs) > 2 else "مدينة"), (5, "أيام لكل برنامج")))}
<section class="section"><div class="wrap"><div class="intro-grid">
  <div class="prose"><span class="kicker">عن المسار</span><h2 class="h2">{esc(T["n"])}</h2>{"".join(f"<p>{esc(p)}</p>" for p in T["intro"])}
    <div class="tags" style="margin-top:22px">{"".join(f"<span>{esc(t)}</span>" for t in T["tags"])}</div></div>
  <aside class="facts-card"><h2>المسار في سطور</h2>
    <div class="row"><span class="leaf sm t-{T["t"]}">{ic(T["i"])}</span><div><small>عدد البرامج</small><b>{len(items)} برنامجاً · {open_n} متاح أو قيد الانعقاد</b></div></div>
    <div class="row"><span class="leaf sm t-ink">{ic("map-pin")}</span><div><small>مدن الانعقاد</small><b>{city_line}</b></div></div>
    <div class="row"><span class="leaf sm t-gold">{ic("clock")}</span><div><small>مدة كل برنامج</small><b>5 أيام (الأحد – الخميس)</b></div></div>
    <div class="row"><span class="leaf sm t-leaf">{ic("award")}</span><div><small>الشهادة</small><b>شهادة إتمام من مركز مرخّص من KHDA</b></div></div>
    <a class="btn btn-primary" href="#dates">{ic("calendar-days")} المواعيد والتسجيل</a>
  </aside>
</div></div></section>
<section class="section on-surface"><div class="wrap two-col">
  <div><span class="kicker">الفئات المستهدفة</span><h2 class="h2">لمن صُمّم هذا المسار</h2><ul class="checklist gold" style="margin-top:22px">{aud}</ul></div>
  <div><span class="kicker">مخرجات التعلّم</span><h2 class="h2">ماذا يكتسب المشارك</h2><ul class="checklist" style="margin-top:22px">{outc}</ul></div>
</div></section>
<section class="section" id="dates"><div class="wrap">
  {sec_head("المواعيد 2026", f"برامج {esc(T['s'])} ومواعيد انعقادها", "افتح البرنامج لعرض التفاصيل وإرسال طلب التسجيل الفردي أو الجماعي.")}
  <div class="pgrid">{"".join(pcard(x, rel, with_chip=False) for x in items)}</div>
</div></section>
<section class="section on-surface"><div class="wrap">
  {sec_head("أسئلة شائعة", f"أسئلة عن {esc(T['s'])}")}
  {faq_html(faqs)}
</div></section>
<section class="section tight"><div class="wrap">
  {sec_head("مسارات أخرى", "استكشف بقية المسارات", "", f'<a class="link-go" href="{rel}programs/#catalog">التقويم الكامل {ic("arrow-left")}</a>')}
  {related_tracks(rel, k)}
</div></section>
{cta_band(rel, f"تريد برنامج {T['s']} لفريق جهتك؟", "نصمّم البرنامج لجهتك بالمحتوى والمدة والموعد المناسب، في دبي أو في مقر الجهة.")}'''
    ld = [crumbs_ld(crumbs), faq_ld(faqs),
          {"@type": "ItemList", "name": f"برامج {T['n']} 2026", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": course_ld(x, path)} for i, x in enumerate(items)]}]
    page(path, "programs", T["title"], T["desc"], body, ld=ld, og_img=T["img"])

def build_courses_hub():
    rel = "../"
    crumbs = [("الدورات", "courses/")]
    faqs = [
        ("ما الدورات التدريبية المتاحة في نُهال المعرفة بدبي؟", "نقدّم دورات في ستة مجالات: الإدارة والقيادة، والحاسوب وتقنية المعلومات، واللغات والتحضير لـ IELTS وTOEFL، والخدمات التعليمية للطلاب، والمهارات المهنية وخدمة العملاء، وتنمية مهارات الأطفال."),
        ("هل الدورات للأفراد أم للشركات؟", "للاثنين. يمكن للأفراد التسجيل في الدورات العامة، ويمكن للشركات والمدارس طلب دورات مخصصة لفرقها بمحتوى وموعد يناسبها."),
        ("هل المركز مرخّص؟", "نعم، نُهال المعرفة للتدريب والتطوير مرخّصة من هيئة المعرفة والتنمية البشرية في دبي (KHDA)."),
        ("كيف أعرف موعد الدورة القادمة وسعرها؟", f"تواصل معنا على {EMAILS[0]} أو {PHONES[0]} وأخبرنا بالدورة التي تهمك، وسنرسل لك المواعيد والرسوم وتفاصيل التسجيل."),
    ]
    body = f'''
{phero(rel, crumbs, "دورات تدريبية في دبي للأفراد والشركات", "ستة مجالات تدريب في مركز مرخّص من KHDA في دبي: من الإدارة والحاسوب واللغات إلى المهارات المهنية وبرامج الأطفال.", side((len(AREAS), "مجالات"), ("KHDA", "ترخيص")))}
<section class="section"><div class="wrap"><div class="intro-grid">
  <div class="prose seo-article"><span class="kicker">دورات في دبي</span><h2 class="h2">مهارات لكل مرحلة، من الطفل إلى المدير</h2>
    <p>سوق العمل في دبي والإمارات سريع ومتعدد الجنسيات، ويكافئ من يطوّر مهاراته باستمرار. لهذا صمّمنا محفظة دورات تغطي احتياجات الأسرة والفرد والشركة معاً: <a href="management-leadership/">دورات الإدارة والقيادة</a> للمديرين، و<a href="computer-it/">دورات الحاسوب</a> للمهارات الرقمية، و<a href="languages/">دورات الإنجليزية وIELTS</a> للدراسة والعمل، و<a href="kids/">برامج الأطفال</a> لبناء الفضول وحب التعلّم.</p>
    <p>تُقدَّم الدورات في مركزنا بدبي بجداول مرنة ومجموعات صغيرة، ويمكن تخصيص أي دورة لفريق شركة أو مدرسة.</p></div>
  <aside class="facts-card"><h2>طرق الالتحاق</h2>
    <div class="row"><span class="leaf sm t-leaf">{ic("user")}</span><div><small>للأفراد</small><b>دورات عامة في مركزنا بدبي</b></div></div>
    <div class="row"><span class="leaf sm t-gold">{ic("building-2")}</span><div><small>للشركات والمدارس</small><b>دورات مخصصة في المركز أو في مقركم</b></div></div>
    <div class="row"><span class="leaf sm t-ink">{ic("calendar-clock")}</span><div><small>المواعيد</small><b>جداول مرنة تناسب الموظفين والطلاب</b></div></div>
    <a class="btn btn-primary" href="{rel}contact/">اسأل عن الدورة القادمة</a>
  </aside>
</div></div></section>
<section class="section on-surface"><div class="wrap">
  {sec_head("مجالات التدريب", "اختر المجال واطّلع على تفاصيل الدورات")}
  {areas_grid(rel)}
</div></section>
{why_section(rel, "لماذا يختارنا الأفراد والشركات في دبي", "t-laptop")}
<section class="section"><div class="wrap">
  {sec_head("أسئلة شائعة", "عن الدورات التدريبية في دبي")}
  {faq_html(faqs)}
</div></section>
{cta_band(rel, "تريد دورة لفريق شركتك؟", "أخبرنا بالمجال وعدد المشاركين، وسنقترح دورة بالمحتوى والموعد المناسب.")}'''
    ld = [crumbs_ld(crumbs), faq_ld(faqs), {"@type": "ItemList", "name": "مجالات الدورات التدريبية في دبي", "itemListElement": [{"@type": "ListItem", "position": k + 1, "url": SITE + "courses/" + A["slug"] + "/", "name": A["n"]} for k, A in enumerate(AREAS)]}]
    page("courses/", "courses", "دورات تدريبية في دبي للأفراد والشركات | نُهال المعرفة",
         "دورات تدريبية في دبي من مركز مرخّص من KHDA: الإدارة والقيادة، الحاسوب، اللغة الإنجليزية وIELTS، الدعم الأكاديمي، المهارات المهنية وبرامج الأطفال.",
         body, ld=ld)

def build_area(k):
    A = AREAS[k]; rel = "../../"; path = f'courses/{A["slug"]}/'
    crumbs = [("الدورات", "courses/"), (A["s"], path)]
    faqs = list(A["faq"]) + [
        (f"هل دورات {A['s']} حضورية في دبي؟", "نعم، تُقدَّم الدورات حضورياً في مركزنا المرخّص في دبي بجداول مرنة، ويمكن تنفيذها لفرق الشركات والمدارس في مقرها."),
        (f"كيف أسجّل في دورات {A['s']}؟", f"تواصل معنا على {EMAILS[0]} أو {PHONES[0]}، أو أرسل طلبك من صفحة التواصل، وسنرسل لك المواعيد القادمة والرسوم وتفاصيل التسجيل."),
        ("هل يحصل المتدرب على شهادة؟", "نعم، يحصل كل متدرب يستوفي متطلبات الحضور والتقييم على شهادة إتمام من نُهال المعرفة، المركز المرخّص من هيئة المعرفة والتنمية البشرية في دبي."),
    ]
    topics = "".join(f'<div class="topic"><span class="leaf sm t-{A["t"]}">{ic("check")}</span><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in A["topics"])
    aud = "".join(f'<li>{ic("user-round-check")}<span>{esc(a)}</span></li>' for a in A["audience"])
    body = f'''
{phero(rel, crumbs, esc(A["h1"]), esc(A["lead"]), side(("KHDA", "مركز مرخّص"), (len(A["topics"]), "محاور تدريب")))}
<section class="section"><div class="wrap split">
  <div class="prose"><span class="kicker">{esc(A["n"])}</span><h2 class="h2">{esc(A["lead"].split("،")[0].split(":")[0])}</h2>{"".join(f"<p>{esc(p)}</p>" for p in A["intro"])}
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:26px"><a class="btn btn-primary" href="{rel}contact/">اسأل عن الموعد القادم {ic("arrow-left", "go")}</a><a class="btn btn-line" href="#topics">محاور الدورات</a></div></div>
  <div class="framed">{img(rel, A["img"], A["n"] + " في دبي")}<span class="tag">{ic(A["i"])} {esc(A["s"])}</span></div>
</div></section>
<section class="section on-surface" id="topics"><div class="wrap">
  {sec_head("ماذا ستتعلم", f"محاور دورات {esc(A['s'])}")}
  <div class="topics{" n7" if len(A["topics"]) == 7 else ""}">{topics}</div>
</div></section>
<section class="section"><div class="wrap two-col">
  <div><span class="kicker">لمن هذه الدورات</span><h2 class="h2">الفئات المستهدفة</h2><ul class="checklist gold" style="margin-top:22px">{aud}</ul></div>
  <div><span class="kicker">صيغ التنفيذ</span><h2 class="h2">اختر الطريقة التي تناسبك</h2>
    <ul class="checklist" style="margin-top:22px">
      <li>{ic("map-pin")}<span><b>دورات عامة في دبي:</b> انضم إلى مجموعة صغيرة في مركزنا المرخّص.</span></li>
      <li>{ic("building-2")}<span><b>دورات مخصصة:</b> لفريق شركتك أو مدرستك بمحتوى وموعد يناسبكم.</span></li>
      <li>{ic("calendar-clock")}<span><b>جداول مرنة:</b> مواعيد تناسب الموظفين والطلاب.</span></li>
      <li>{ic("award")}<span><b>شهادة إتمام:</b> من مركز مرخّص من هيئة المعرفة والتنمية البشرية.</span></li>
    </ul></div>
</div></section>
<section class="section on-surface"><div class="wrap">
  {sec_head("أسئلة شائعة", f"أسئلة عن دورات {esc(A['s'])} في دبي")}
  {faq_html(faqs)}
</div></section>
<section class="section tight"><div class="wrap">
  {sec_head("مجالات أخرى", "دورات أخرى قد تهمك", "", f'<a class="link-go" href="{rel}courses/">كل الدورات {ic("arrow-left")}</a>')}
  {related_areas(rel, k)}
</div></section>
{cta_band(rel, f"جاهز للبدء في {A['s']}؟", "أرسل لنا اسم الدورة وعدد المشاركين، وسنعود إليك بالمواعيد والتفاصيل خلال يوم عمل.")}'''
    service = {"@type": "Service", "name": A["h1"], "serviceType": A["n"], "description": A["desc"], "provider": {"@id": ORG_ID},
               "areaServed": [{"@type": "City", "name": "Dubai"}, {"@type": "Country", "name": "United Arab Emirates"}], "url": SITE + path,
               "hasOfferCatalog": {"@type": "OfferCatalog", "name": f"دورات {A['n']}", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Course", "name": a, "description": b, "provider": {"@id": ORG_ID}, "inLanguage": "ar"}} for a, b in A["topics"]]}}
    page(path, "courses", A["title"], A["desc"], body, ld=[crumbs_ld(crumbs), faq_ld(faqs), service], og_img=A["img"])

def build_accreditations():
    rel = "../"; crumbs = [("الاعتمادات", "accreditations/")]
    faqs = [
        ("هل نُهال المعرفة مرخّصة من KHDA؟", "نعم، نُهال المعرفة للتدريب والتطوير ذ.م.م مرخّصة من هيئة المعرفة والتنمية البشرية في دبي (KHDA)."),
        ("ما هيئة المعرفة والتنمية البشرية؟", "هي الجهة الحكومية المسؤولة عن تنظيم قطاع التعليم الخاص في دبي، ومنه مراكز التدريب، وتضع الأطر والمعايير التي تعمل وفقها المؤسسات المرخّصة."),
        ("كيف أتحقق من ترخيص مركز تدريب في دبي؟", "يمكن التحقق من المؤسسات التعليمية المرخّصة عبر القنوات الرسمية لهيئة المعرفة والتنمية البشرية على موقعها khda.gov.ae."),
        ("ماذا تتضمن شهادة الإتمام؟", "تحمل الشهادة اسم المشارك واسم البرنامج وعدد ساعاته وتاريخ انعقاده، وتُمنح لكل من يستوفي متطلبات الحضور والتقييم."),
    ]
    body = f'''
{phero(rel, crumbs, "مركز تدريب مرخّص من KHDA في دبي", "ترخيص رسمي من الجهة المنظّمة للتعليم الخاص في دبي، وإطار جودة يرافق كل برنامج من التشخيص حتى تقرير الأثر.")}
<section class="section"><div class="wrap"><div class="khda">
  <div class="seal" aria-hidden="true"><svg viewBox="0 0 220 220"><circle cx="110" cy="110" r="104" fill="none" stroke="var(--gold)" stroke-width="2"/><circle cx="110" cy="110" r="94" fill="none" stroke="var(--gold)" stroke-width="1" stroke-dasharray="2 5"/><circle cx="110" cy="110" r="78" fill="var(--night)"/><path d="M110 46 l7 14 15 2 -11 11 3 15 -14 -7 -14 7 3 -15 -11 -11 15 -2z" fill="var(--gold)"/><text x="110" y="128" text-anchor="middle" font-family="Alexandria, sans-serif" font-weight="800" font-size="30" fill="#fff" letter-spacing="2">KHDA</text><text x="110" y="152" text-anchor="middle" font-family="IBM Plex Sans Arabic, sans-serif" font-weight="600" font-size="15" fill="#9FBDC2">مرخّص · دبي</text></svg></div>
  <div><span class="kicker">الترخيص الرسمي</span><h2 class="h2">مرخّصون من هيئة المعرفة والتنمية البشرية في دبي</h2>
    <p class="lead">هيئة المعرفة والتنمية البشرية (KHDA) هي الجهة الحكومية المسؤولة عن تنظيم قطاع التعليم الخاص في دبي، ومنه مراكز التدريب. ترخيصنا يعني أن برامجنا ومرافقنا وممارساتنا تخضع لإطارها التنظيمي ومعاييرها.</p>
    <div class="tags" style="margin-top:22px"><span>Knowledge and Human Development Authority</span><span>Dubai, UAE</span></div></div>
</div></div></section>
<section class="section tight on-surface"><div class="wrap">
  {sec_head("ماذا يعني الترخيص لكم", "ضمانات تحصل عليها الجهة والمشارك")}
  <div class="means">
    <div class="mean"><span class="leaf t-leaf">{ic("clipboard-check")}</span><h3>جودة البرامج</h3><p>محتوى ومخرجات تعلّم تلتزم بمعايير الجودة في التعليم والتدريب المهني.</p></div>
    <div class="mean"><span class="leaf t-gold">{ic("scale")}</span><h3>امتثال تنظيمي</h3><p>عمل ضمن الأنظمة التعليمية في الإمارات ومتطلبات الهيئة في دبي.</p></div>
    <div class="mean"><span class="leaf t-ink">{ic("school")}</span><h3>بيئة تدريب مناسبة</h3><p>قاعات ومختبرات وموارد تعلّم مهيّأة لتجربة تدريب فعّالة وآمنة.</p></div>
    <div class="mean"><span class="leaf t-leaf">{ic("file-text")}</span><h3>وضوح في التعاقد</h3><p>شفافية في تفاصيل البرامج والرسوم والتسجيل منذ أول تواصل.</p></div>
  </div>
</div></section>
<section class="section"><div class="wrap ent">
  <div class="ent-card"><svg aria-hidden="true" style="position:absolute;left:-30px;bottom:-40px;width:200px;opacity:.1"><use href="#logo-mark"/></svg>
    <span class="kicker">الكيان القانوني</span><h2 style="font-size:22px">بيانات المنشأة</h2>
    <dl><div><dt>الاسم التجاري</dt><dd>{BRAND_FULL} ذ.م.م</dd></div><div><dt>Legal name</dt><dd class="ltr" style="display:block;text-align:left">{LEGAL_EN}</dd></div><div><dt>المقر</dt><dd>دبي، الإمارات العربية المتحدة</dd></div><div><dt>جهة الترخيص</dt><dd>هيئة المعرفة والتنمية البشرية (KHDA)</dd></div><div><dt>الموقع الإلكتروني</dt><dd class="ltr" style="display:block;text-align:left">www.nuhal.ae</dd></div></dl></div>
  <div class="cert"><span class="note">نموذج توضيحي</span><div class="sheet"><svg aria-hidden="true"><use href="#logo-full"/></svg><span class="t">شهادة إتمام برنامج تدريبي</span><span class="d">تشهد {BRAND_FULL} بأن</span><span class="n">اسم المشارك</span><span class="d">قد أتمّ متطلبات البرنامج التدريبي «عنوان البرنامج» بعدد ساعات وتاريخ انعقاد محدّدين، واجتاز تقييمه بنجاح.</span><div class="sig"><span>المدير العام</span><span>مدير البرامج</span></div></div>
    <p style="font-size:14px;color:var(--muted);padding:14px 8px 4px">يحصل كل مشارك يستوفي متطلبات الحضور والتقييم على شهادة إتمام تحمل اسم البرنامج وعدد ساعاته وتاريخ انعقاده.</p></div>
</div></section>
<section class="section on-surface"><div class="wrap">
  {sec_head("دورة الجودة", "ست محطات يمرّ بها كل برنامج")}
  <div class="cycle">
    <div class="cyc"><span class="n">01</span><span class="leaf sm t-leaf">{ic("search-check")}</span><h3>تحليل الاحتياج</h3><p>مقابلات واستبيانات لتحديد الفجوة الفعلية في الأداء.</p></div>
    <div class="cyc"><span class="n">02</span><span class="leaf sm t-gold">{ic("pencil-ruler")}</span><h3>تصميم المخرجات</h3><p>أهداف تعلّم قابلة للقياس ومحتوى مبني على حالات حقيقية.</p></div>
    <div class="cyc"><span class="n">03</span><span class="leaf sm t-ink">{ic("clipboard-list")}</span><h3>تقييم قبلي</h3><p>قياس مستوى المشاركين قبل البدء لضبط العمق والأمثلة.</p></div>
    <div class="cyc"><span class="n">04</span><span class="leaf sm t-leaf">{ic("presentation")}</span><h3>تنفيذ تفاعلي</h3><p>تمارين وورش ومحاكاة بقيادة مدربين متخصصين.</p></div>
    <div class="cyc"><span class="n">05</span><span class="leaf sm t-gold">{ic("clipboard-check")}</span><h3>تقييم بعدي</h3><p>قياس ما تعلّمه المشارك ومقارنته بنتيجة التقييم القبلي.</p></div>
    <div class="cyc"><span class="n">06</span><span class="leaf sm t-ink">{ic("file-bar-chart")}</span><h3>تقرير الأثر</h3><p>تقرير للجهة بالنتائج والتوصيات وخطة المتابعة.</p></div>
  </div>
</div></section>
<section class="section"><div class="wrap">
  {sec_head("قياس الأثر", "أربعة مستويات نقيس عليها نجاح البرنامج", "إطار تقييم مستوحى من نموذج كيركباتريك، يربط ما يحدث في القاعة بما يتغيّر في العمل.")}
  <div class="levels">
    <div class="lvl" style="--w:25%"><h3><span class="leaf sm t-leaf">{ic("smile")}</span>1. التفاعل</h3><p>رضا المشاركين عن المحتوى والمدرب وبيئة التدريب، عبر استبيان في نهاية كل يوم.</p></div>
    <div class="lvl" style="--w:50%"><h3><span class="leaf sm t-gold">{ic("brain")}</span>2. التعلّم</h3><p>الفرق بين نتائج التقييم القبلي والبعدي في المعارف والمهارات المستهدفة.</p></div>
    <div class="lvl" style="--w:75%"><h3><span class="leaf sm t-ink">{ic("repeat")}</span>3. التطبيق</h3><p>مدى استخدام المشاركين لما تعلّموه في عملهم خلال الأسابيع التالية للبرنامج.</p></div>
    <div class="lvl" style="--w:100%"><h3><span class="leaf sm t-leaf">{ic("trending-up")}</span>4. الأثر</h3><p>انعكاس البرنامج على مؤشرات أداء الجهة التي تم الاتفاق عليها في مرحلة التشخيص.</p></div>
  </div>
</div></section>
<section class="section on-surface"><div class="wrap">{sec_head("أسئلة شائعة", "عن الترخيص والشهادات")}{faq_html(faqs)}</div></section>
{cta_band(rel)}'''
    page("accreditations/", "accreditations", "مركز تدريب مرخّص من KHDA في دبي | الاعتمادات والجودة",
         "نُهال المعرفة مركز تدريب مرخّص من هيئة المعرفة والتنمية البشرية في دبي. تعرّف على ما يعنيه الترخيص، وشهادات الإتمام، ودورة الجودة وقياس أثر التدريب.",
         body, ld=[crumbs_ld(crumbs), faq_ld(faqs)])

def build_team():
    rel = "../"; crumbs = [("الفريق", "team/")]
    fac = "".join(f'<a class="frow" href="{rel}programs/{T["slug"]}/"><div class="who"><span class="leaf t-{T["t"]}">{ic(T["i"])}</span><h3>خبراء {esc(T["n"])}</h3></div><div class="tags">{"".join(f"<span>{esc(t)}</span>" for t in T["tags"])}</div><div class="num"><b>{len(by_track[k])}</b><span>برنامجاً يقودونها</span></div></a>' for k, T in enumerate(TRACKS))
    body = f'''
{phero(rel, crumbs, "فريق نُهال المعرفة: مدربون وخبراء في دبي", "فريق إدارة يقود التصميم والجودة والتنسيق، وشبكة خبراء ومستشارين متخصصين في كل مسار من مسارات التدريب.", side((len(TRACKS), "مجموعات خبرة"), (4, "وحدات إدارية")))}
<section class="section"><div class="wrap split">
  <div><span class="kicker">كيف نعمل</span><h2 class="h2">فريق صغير في الإدارة، وشبكة واسعة من الخبراء في القاعة</h2>
    <p class="lead">نختار لكل برنامج المدرب الأقرب إلى موضوعه وقطاعه، ويرافقه فريق البرامج من التشخيص حتى تسليم تقرير الأثر. بهذا تحصل الجهة على عمق التخصص مع نقطة تواصل واحدة في دبي.</p></div>
  <div class="framed">{img(rel, "t-present", "مدربة تقدّم عرضاً لمجموعة من المشاركين في دبي")}<span class="tag">{ic("users")} خبراء من الميدان</span></div>
</div></section>
<section class="section tight on-surface"><div class="wrap">
  {sec_head("فريق الإدارة", "أربع وحدات تقود العمل")}
  <div class="roles">
    <div class="role"><span class="av t-ink">{ic("compass")}</span><h3>الإدارة العامة</h3><p>تحدد التوجه الاستراتيجي للمركز، وتشرف على جودة البرامج والشراكات مع الجهات الحكومية والخاصة.</p></div>
    <div class="role"><span class="av t-leaf">{ic("pencil-ruler")}</span><h3>إدارة البرامج والتصميم التدريبي</h3><p>تحوّل احتياج الجهة إلى مناهج ومخرجات تعلّم وأدوات تقييم، وتتابع التنفيذ يوماً بيوم.</p></div>
    <div class="role"><span class="av t-gold">{ic("headset")}</span><h3>علاقات العملاء والتنسيق</h3><p>نقطة تواصل واحدة لكل جهة: الجدولة والتسجيل والترتيبات داخل الدولة وخارجها والشهادات.</p><span class="contact">{ic("mail")}<span class="ltr">{EMAILS[1]}</span></span></div>
    <div class="role"><span class="av t-ink">{ic("line-chart")}</span><h3>الجودة والتقييم</h3><p>تقيس رضا المشاركين ومستوى التعلّم قبل البرنامج وبعده، وتُعدّ تقارير الأثر للجهات.</p></div>
  </div>
</div></section>
<section class="section"><div class="wrap">
  {sec_head("شبكة الخبراء", "خبراء ومستشارون لكل مسار", "يقود برامج كل مسار مدربون يجمعون بين الخبرة التنفيذية في القطاع والتأهيل الأكاديمي والمهني.")}
  <div class="faculty">{fac}</div>
  <div style="margin-top:64px" class="split">
    <div><span class="kicker">معايير الاختيار</span><h2 class="h2">كيف نختار مدربينا</h2>
      <ul class="criteria">
        <li>{ic("check")}خبرة عملية في القطاع الحكومي أو المؤسسي المرتبط بالبرنامج</li>
        <li>{ic("check")}تأهيل أكاديمي ومهني في مجال التخصص</li>
        <li>{ic("check")}قدرة على التدريب بالعربية مع المصطلحات الإنجليزية</li>
        <li>{ic("check")}سجل تقييمات مرتفع من المشاركين والجهات</li>
        <li>{ic("check")}تحديث مستمر للمحتوى بأحدث الأدوات والممارسات</li>
        <li>{ic("check")}أسلوب تطبيقي يعتمد الحالات والتمارين لا التلقين</li>
      </ul></div>
    <div class="framed">{img(rel, "t-table", "مدرب يحاور مشاركين حول طاولة اجتماعات")}<span class="tag">{ic("star")} تقييم بعد كل برنامج</span></div>
  </div>
  <div class="join"><div><h3>هل أنت مدرب أو خبير في أحد مساراتنا؟</h3><p>نرحّب بانضمام المدربين والمستشارين في الإمارات والمنطقة إلى شبكتنا. أرسل سيرتك الذاتية ومجالات تخصصك.</p></div>
    <div style="display:grid;gap:8px;justify-items:start"><span class="mail">{ic("mail")}<span class="ltr">{EMAILS[0]}</span></span><button class="copy-btn" type="button" data-copy="{EMAILS[0]}" style="color:var(--gold)">{ic("copy")} نسخ البريد</button></div></div>
</div></section>
{cta_band(rel)}'''
    page("team/", "team", "فريق نُهال المعرفة | مدربون وخبراء في دبي والإمارات",
         "تعرّف على فريق نُهال المعرفة في دبي: وحدات الإدارة والتصميم التدريبي والجودة، وشبكة خبراء في القيادة والذكاء الاصطناعي والمالية والأمن السيبراني.",
         body, ld=[crumbs_ld(crumbs)])
    # frow as link styling
def build_experience():
    rel = "../"; crumbs = [("الخبرات", "experience/")]
    maxC = max(by_city.values()); maxT = max(len(v) for v in by_track.values()); maxM = max(by_month.values())
    chc = "".join(f'<div class="bar" style="--tone:{"var(--ink)" if i == 0 else "var(--leaf)"}"><span class="lab">{ic("map-pin")} {esc(c)}</span><span class="trk"><span class="fill" style="display:block;width:{by_city[c] / maxC * 100:.1f}%"></span></span><span class="v">{by_city[c]}</span></div>' for i, c in enumerate(CITIES))
    cht = "".join(f'<div class="bar" style="--tone:{TONE[TRACKS[k]["t"]]}"><a class="lab" href="{rel}programs/{TRACKS[k]["slug"]}/" title="{esc(TRACKS[k]["n"])}">{esc(TRACKS[k]["s"])}</a><span class="trk"><span class="fill" style="display:block;width:{len(by_track[k]) / maxT * 100:.1f}%"></span></span><span class="v">{len(by_track[k])}</span></div>' for k in sorted(range(len(TRACKS)), key=lambda k: -len(by_track[k])))
    chm = "".join(f'<div class="mcol"><b>{by_month[m]}</b><span class="col" style="height:{by_month[m] / maxM * 150:.0f}px"></span></div>' for m in (10, 11, 12))
    intl = "".join(f"<span>{esc(c)} · {by_city[c]}</span>" for c in CITIES if c != "دبي")
    body = f'''
{phero(rel, crumbs, "خبراتنا في التدريب الحكومي والمؤسسي في دبي", "برامج منفّذة لجهات حكومية في دبي، وتقويم يمتد عبر خمس مدن، ومحفظة تخدم الحكومات والشركات والأفراد في الإمارات.", side((len(ITEMS), "برنامجاً مجدولاً"), (len(CITIES), "مدن"), (len(TRACKS), "مسارات")))}
<section class="section" id="case"><div class="wrap">
  {sec_head("من المشاريع المنفّذة", "بلدية دبي: برنامجان لإدارة التسويق المؤسسي")}
  <div class="case">
    <div class="cside"><svg aria-hidden="true" style="position:absolute;left:-30px;bottom:-40px;width:210px;opacity:.1"><use href="#logo-mark"/></svg><span class="leaf lg t-gold">{ic("building-2")}</span><h3>بلدية دبي</h3>
      <p>صمّمنا ونفّذنا برنامجين حضوريين في دبي لفريق إدارة التسويق المؤسسي، باللغة العربية مع المصطلحات الإنجليزية، ضمن مسار التسويق الحكومي والرقمي.</p>
      <div class="kv"><div><b>2</b><span>برنامجان منفّذان</span></div><div><b>31</b><span>ساعة تدريبية</span></div><div><b>7</b><span>أيام تدريب</span></div><div><b>2026</b><span>سنة التنفيذ</span></div></div></div>
    <div class="cmain">
      <div class="prog"><div class="top"><h4>الاحتراف المتقدم والابتكار في التسويق الحكومي</h4><span class="pill st-open">منفّذ</span></div>
        <div class="meta"><span>{ic("calendar-days")} 4 أيام × 4 ساعات</span><span>{ic("map-pin")} حضوري، دبي</span><span>{ic("languages")} عربي مع مصطلحات إنجليزية</span></div>
        <p style="color:var(--muted);font-size:15px">برنامج استراتيجي يربط التسويق الحكومي بأهداف الجهة وتجربة المتعامل، ويقدّم أدوات الابتكار في الحملات والرسائل المؤسسية.</p></div>
      <div class="prog"><div class="top"><h4>تطوير الأداء المتقدم في التسويق الرقمي</h4><span class="pill st-open">منفّذ</span></div>
        <div class="meta"><span>{ic("calendar-days")} 3 أيام × 5 ساعات</span><span>{ic("map-pin")} حضوري، دبي</span><span>{ic("file-text")} مادة عربية بالكامل</span></div>
        <div class="mods"><div><small>اليوم الأول</small>الإعلانات الاجتماعية والقنوات والمحتوى</div><div><small>اليوم الثاني</small>تحسين الظهور في محركات البحث SEO وGEO</div><div><small>اليوم الثالث</small>الذكاء الاصطناعي في التسويق الرقمي</div></div></div>
    </div>
  </div>
</div></section>
<section class="section on-surface" id="footprint"><div class="wrap">
  {sec_head("الانتشار والتوزيع", "أين ومتى تنعقد برامجنا", "أرقام محسوبة من تقويم برامج الربع الرابع 2026.")}
  <div class="charts">
    <div class="chart"><h3>البرامج حسب المدينة</h3><p class="sub">عدد البرامج المجدولة في كل مدينة</p><div class="bars">{chc}</div></div>
    <div class="chart"><h3>البرامج حسب المسار</h3><p class="sub">عدد البرامج في كل مسار تخصصي</p><div class="bars">{cht}</div></div>
    <div class="chart" style="grid-column:1/-1"><h3>الإيقاع الشهري</h3><p class="sub">عدد البرامج التي تبدأ في كل شهر</p><div class="months">{chm}</div><div class="mlabels"><span>أكتوبر</span><span>نوفمبر</span><span>ديسمبر</span></div></div>
  </div>
</div></section>
<section class="section" id="sectors"><div class="wrap">
  {sec_head("القطاعات", "من نخدم في الإمارات")}
  <div class="sectors">
    <div class="sector"><span class="leaf t-ink">{ic("landmark")}</span><h3>الجهات الحكومية</h3><p>قيادة، تحول رقمي، مالية حكومية، تجربة متعامل.</p></div>
    <div class="sector"><span class="leaf t-leaf">{ic("building-2")}</span><h3>الشركات</h3><p>إدارة، مبيعات، خدمة عملاء، مهارات تقنية.</p></div>
    <div class="sector"><span class="leaf t-gold">{ic("briefcase")}</span><h3>المهنيون</h3><p>تطوير وظيفي، لغات، أدوات رقمية.</p></div>
    <div class="sector"><span class="leaf t-ink">{ic("graduation-cap")}</span><h3>الطلاب</h3><p>دعم أكاديمي، تحضير للاختبارات، مهارات الدراسة.</p></div>
    <div class="sector"><span class="leaf t-leaf">{ic("blocks")}</span><h3>الأطفال</h3><p>STEM، التفكير الناقد، الفنون، بناء الثقة.</p></div>
  </div>
  {sec_head("صيغ التنفيذ", "ثلاث طرق لتقديم البرنامج").replace('class="sec-head"', 'class="sec-head" style="margin-top:72px"')}
  <div class="formats">
    <div class="format"><span class="leaf t-leaf">{ic("map-pin")}</span><h3>حضوري في دبي</h3><p>برامج في قاعاتنا المرخّصة في دبي، وهي النسبة الأكبر من تقويم هذا الربع.</p><div class="cities"><span>دبي · {by_city.get("دبي", 0)} برنامجاً</span></div></div>
    <div class="format"><span class="leaf t-gold">{ic("plane")}</span><h3>برامج دولية</h3><p>برامج تجمع التدريب بالاطلاع على تجارب مؤسسية في وجهات خارج الدولة.</p><div class="cities">{intl}</div></div>
    <div class="format"><span class="leaf t-ink">{ic("settings-2")}</span><h3>برامج مخصصة</h3><p>محتوى ومدة وموعد يُصمَّم لجهة واحدة حسب احتياجها وفي المكان الذي تختاره.</p><div class="cities"><span>حسب الطلب</span></div></div>
  </div>
</div></section>
{cta_band(rel, "أضف جهتك إلى سجل خبراتنا", "نصمّم برنامجاً بأهداف واضحة ونقيس أثره بعد التنفيذ.")}'''
    page("experience/", "experience", "خبراتنا التدريبية في دبي والإمارات | نُهال المعرفة",
         "سجل خبرات نُهال المعرفة في التدريب الحكومي والمؤسسي: برامج منفّذة لبلدية دبي، وتقويم 2026 في دبي والقاهرة واسطنبول ومدريد وفرنسا، والقطاعات التي نخدمها.",
         body, ld=[crumbs_ld(crumbs)])

def build_contact():
    rel = "../"; crumbs = [("تواصل معنا", "contact/")]
    opts = "".join(f"<option>{esc(T['n'])}</option>" for T in TRACKS) + "".join(f"<option>{esc(A['n'])}</option>" for A in AREAS)
    faqs = [
        ("كم يستغرق الرد على الطلبات؟", "يتواصل معك فريق علاقات العملاء خلال يوم عمل من استلام طلبك."),
        ("هل تقدّمون عروضاً للجهات الحكومية والشركات؟", "نعم، نرسل عرضاً تدريبياً مفصّلاً يتضمن المحتوى والمدة والموعد والرسوم، بعد فهم احتياج الجهة وعدد المشاركين."),
        ("هل يمكن تنفيذ التدريب خارج دبي؟", "نعم، ننفّذ البرامج في أي إمارة داخل الدولة، وفي وجهات دولية مثل القاهرة واسطنبول ومدريد وفرنسا."),
    ]
    body = f'''
{phero(rel, crumbs, "تواصل مع نُهال المعرفة في دبي", "أخبرنا باحتياج جهتك أو الدورة التي تهمك، وسيتواصل معك فريق علاقات العملاء خلال يوم عمل.")}
<section class="section on-surface contact" id="contact"><div class="wrap">
  <div><span class="kicker">بيانات التواصل</span><h2 class="h2">نحن في دبي، ونخدم الإمارات والمنطقة</h2>
    <div class="cinfo">
      <div class="cline"><span class="leaf sm t-leaf">{ic("mail")}</span><div><small>البريد الإلكتروني</small><div class="two"><b class="ltr">{EMAILS[0]}</b><b class="ltr">{EMAILS[1]}</b></div></div></div>
      <div class="cline"><span class="leaf sm t-gold">{ic("phone")}</span><div><small>الهاتف وواتساب</small><div class="two"><b class="ltr">{PHONES[0]}</b><b class="ltr">{PHONES[1]}</b></div></div></div>
      <div class="cline"><span class="leaf sm t-ink">{ic("map-pin")}</span><div><small>المقر</small><b>دبي، الإمارات العربية المتحدة</b></div></div>
      <div class="cline"><span class="leaf sm t-leaf">{ic("globe")}</span><div><small>الموقع</small><b class="ltr">www.nuhal.ae</b></div></div>
    </div></div>
  <div class="cform" id="cformBox"><h3>طلب برنامج أو دورة تدريبية</h3><p>املأ البيانات وسنجهّز لك طلباً مكتملاً لإرساله إلينا.</p>
    <form class="form" id="cform" novalidate>
      <label>الاسم الكامل <span class="req">*</span><input class="input" id="c-name" required autocomplete="name"></label>
      <label>الجهة / الشركة <span class="req">*</span><input class="input" id="c-org" required autocomplete="organization"></label>
      <label>البريد الإلكتروني <span class="req">*</span><input class="input" id="c-email" type="email" required autocomplete="email" dir="ltr"></label>
      <label>رقم الهاتف <span class="req">*</span><input class="input" id="c-phone" type="tel" required autocomplete="tel" dir="ltr" placeholder="+971"></label>
      <label>المجال المطلوب<select class="select" id="c-track" style="width:100%;flex:none"><option value="">اختر المجال</option>{opts}<option>برنامج مخصص آخر</option></select></label>
      <label>عدد المشاركين المتوقع<input class="input" id="c-count" type="number" min="1" value="10"></label>
      <label class="full">تفاصيل الاحتياج<textarea id="c-msg" placeholder="مثال: برنامج لثلاثة أيام لفريق التحول الرقمي، في دبي، خلال يناير"></textarea></label>
      <div class="full form-actions"><button class="btn btn-primary" type="submit">{ic("send")} تجهيز الطلب</button><span class="form-note">الحقول المعلّمة بـ * مطلوبة</span></div>
    </form></div>
</div></section>
<section class="section"><div class="wrap two-col">
  <div>{sec_head("أسئلة شائعة", "قبل أن تتواصل معنا")}{faq_html(faqs)}</div>
  <div><span class="kicker">روابط سريعة</span><h2 class="h2">ابحث عن البرنامج المناسب</h2>
    <div class="related" style="grid-template-columns:1fr;margin-top:24px">
      <a class="rel" href="{rel}programs/"><span class="leaf sm t-ink">{ic("calendar-range")}</span><span><b>تقويم البرامج الحكومية 2026</b><small>{len(ITEMS)} برنامجاً في {len(TRACKS)} مسارات</small></span>{ic("arrow-left", "go")}</a>
      <a class="rel" href="{rel}courses/"><span class="leaf sm t-leaf">{ic("grid-2x2")}</span><span><b>دورات للأفراد والشركات</b><small>{len(AREAS)} مجالات تدريب في دبي</small></span>{ic("arrow-left", "go")}</a>
      <a class="rel" href="{rel}programs/government-ai/"><span class="leaf sm t-gold">{ic("brain-circuit")}</span><span><b>دورات الذكاء الاصطناعي الحكومي</b><small>{len(by_track[5])} برنامجاً</small></span>{ic("arrow-left", "go")}</a>
    </div></div>
</div></section>'''
    page("contact/", "contact", "تواصل مع نُهال المعرفة | مركز تدريب في دبي",
         f"تواصل مع نُهال المعرفة للتدريب والتطوير في دبي لطلب برنامج تدريبي أو دورة: {EMAILS[0]} · {PHONES[0]}. نرد خلال يوم عمل.",
         body, ld=[crumbs_ld(crumbs), faq_ld(faqs), {"@type": "ContactPage", "name": "تواصل مع نُهال المعرفة", "url": SITE + "contact/", "about": {"@id": ORG_ID}}])

def build_404():
    body = f'''<section class="section err404"><div class="wrap"><b>404</b><h1 style="font-size:30px;margin-top:10px">الصفحة غير موجودة</h1><p class="lead" style="margin-inline:auto">ربما تغيّر الرابط أو حُذفت الصفحة. ابدأ من إحدى الصفحات التالية.</p>
<div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin-top:24px"><a class="btn btn-primary" href="./">الصفحة الرئيسية</a><a class="btn btn-line" href="programs/">البرامج التدريبية</a><a class="btn btn-line" href="courses/">الدورات</a><a class="btn btn-line" href="contact/">تواصل معنا</a></div></div></section>'''
    page("404.html", "", "الصفحة غير موجودة | نُهال المعرفة", "الصفحة المطلوبة غير موجودة على موقع نُهال المعرفة للتدريب والتطوير في دبي.", body)
    # 404 must not be indexed
    p = os.path.join(OUT, "404.html"); s = open(p).read().replace('content="index, follow, max-image-preview:large, max-snippet:-1"', 'content="noindex, follow"')
    open(p, "w").write(s); PAGES.pop()

# ------------------------------------------------------------------ assets & SEO files
def write_assets():
    os.makedirs(os.path.join(OUT, "assets", "css"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "assets", "js"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "assets", "img"), exist_ok=True)
    open(os.path.join(OUT, "assets", "css", "site.css"), "w").write(BASE_CSS.strip() + "\n" + EXTRA_CSS)
    for f in os.listdir(os.path.join(SRC, "img")):
        shutil.copy(os.path.join(SRC, "img", f), os.path.join(OUT, "assets", "img", f))
    here = os.path.dirname(os.path.abspath(__file__))
    shutil.copy(os.path.join(here, "logo.png"), os.path.join(OUT, "assets", "logo.png"))
    shutil.copy(os.path.join(here, "og.jpg"), os.path.join(OUT, "assets", "og.jpg"))
    mark = LOGO_MARK.replace("var(--lt)", "#4A9698").replace("var(--lg)", "#DDAE4A")
    open(os.path.join(OUT, "assets", "favicon.svg"), "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="44 50 280 297">{mark}</svg>\n')
    data = {"items": [{k: it[k] for k in ("t", "tr", "m", "d1", "d2", "c")} for it in ITEMS],
            "tracks": [{"n": T["n"], "s": T["s"], "i": T["i"], "t": T["t"], "slug": T["slug"]} for T in TRACKS],
            "emails": EMAILS, "phones": PHONES}
    js = open(os.path.join(here, "site.js")).read().replace("/*DATA*/null", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    open(os.path.join(OUT, "assets", "js", "site.js"), "w").write(js)

def write_seo_files():
    prio = lambda p: "1.0" if p == "" else ("0.9" if p in ("programs/", "courses/") else ("0.8" if p.count("/") == 2 else "0.7"))
    urls = "".join(f"  <url><loc>{SITE}{p['path']}</loc><lastmod>{BUILD_DATE.isoformat()}</lastmod><priority>{prio(p['path'])}</priority></url>\n" for p in PAGES)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(os.path.join(OUT, "robots.txt"), "w").write(
        "User-agent: *\nAllow: /\n\n# AI search and answer engines are welcome\nUser-agent: GPTBot\nAllow: /\nUser-agent: OAI-SearchBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\n\n"
        f"Sitemap: {SITE}sitemap.xml\n")
    tl = "\n".join(f"- [{T['n']}]({SITE}programs/{T['slug']}/): {len(by_track[k])} برنامجاً في {'، '.join(cities_of(k))}. {T['card']}" for k, T in enumerate(TRACKS))
    al = "\n".join(f"- [{A['n']}]({SITE}courses/{A['slug']}/): {A['card']}" for A in AREAS)
    open(os.path.join(OUT, "llms.txt"), "w").write(f"""# {BRAND_FULL} ({LEGAL_EN})

> مركز تدريب وتطوير في دبي، الإمارات العربية المتحدة، مرخّص من هيئة المعرفة والتنمية البشرية (KHDA). يقدّم برامج تدريبية للجهات الحكومية والشركات والأفراد، ودورات في الإدارة والحاسوب واللغات والمهارات المهنية وبرامج الأطفال.
> A KHDA-licensed training and development center in Dubai, UAE, serving government entities, companies and individuals.

- الموقع: دبي، الإمارات العربية المتحدة
- البريد: {EMAILS[0]}، {EMAILS[1]}
- الهاتف: {PHONES[0]}، {PHONES[1]}
- تقويم الربع الرابع 2026: {len(ITEMS)} برنامجاً في {len(TRACKS)} مسارات، تُعقد في {'، '.join(CITIES)}. مدة كل برنامج 5 أيام (الأحد – الخميس).

## الصفحات الرئيسية
- [الرئيسية]({SITE})
- [عن الشركة]({SITE}about/): الرؤية والرسالة والقيم وقسم جاهزية الذكاء الاصطناعي
- [البرامج التدريبية الحكومية]({SITE}programs/): التقويم الكامل والمسارات
- [الدورات للأفراد والشركات]({SITE}courses/)
- [الاعتمادات]({SITE}accreditations/): ترخيص KHDA ودورة الجودة وقياس الأثر
- [الفريق]({SITE}team/)
- [الخبرات]({SITE}experience/): برامج منفّذة لبلدية دبي والانتشار الجغرافي
- [تواصل معنا]({SITE}contact/)

## مسارات البرامج الحكومية
{tl}

## مجالات الدورات
{al}
""")

def main():
    if os.path.exists(OUT):
        for f in os.listdir(OUT):
            if f in (".git", "README.md", ".gitignore", "CNAME", "_build"): continue
            p = os.path.join(OUT, f); shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    os.makedirs(OUT, exist_ok=True)
    write_assets()
    build_home(); build_about(); build_programs_hub()
    for k in range(len(TRACKS)): build_track(k)
    build_courses_hub()
    for k in range(len(AREAS)): build_area(k)
    build_accreditations(); build_team(); build_experience(); build_contact(); build_404()
    write_seo_files()
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    print(f"built {len(PAGES)} indexable pages into {OUT}")
    for p in PAGES: print(f"{len(p['title']):3d} {len(p['desc']):3d}  /{p['path']:42s} {p['title']}")

if __name__ == "__main__":
    main()
