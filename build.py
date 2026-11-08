#!/usr/bin/env python3
"""Builds the topic pages in pages/*.html into <slug>/index.html, adds FAQ structured data to
every page with a FAQ, and rewrites sitemap.xml. Run after editing any page: python3 build.py

A page file starts with a JSON header between <!--meta and -->, then the body HTML:
  {"slug": "...", "title": "...", "description": "...", "kicker": "...", "h1": "...", "lead": "...",
   "starter": true}
The body may use <details><summary>Q</summary><p>A</p></details> for FAQs."""
import glob, html, json, os, re, datetime

SITE = "https://zclap.com"
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,500;0,8..60,600;1,8..60,500&display=swap" rel="stylesheet">'
GTAG = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-QG1B2QHK2T"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-QG1B2QHK2T');gtag('config','AW-18483009453');</script>"""
ESTIMATOR = "https://zclap.com/estimator/index.html"   # build-production.sh points this at /estimator/

# Every topic page, for the nav strip and footer. Order = how they appear.
TOPICS = [
    ("informatica-mdm-implementation", "Implementation"),
    ("informatica-mdm-saas-migration", "SaaS migration"),
    ("informatica-mdm-cost", "Cost"),
    ("informatica-mdm-replacement", "Replacing another MDM"),
    ("healthcare", "Healthcare"),
]

STARTER = f"""<div class="starter" id="start">
      <div class="step"><span>Free estimate</span><span>Question 1 of about 12</span></div>
      <h2>What kind of MDM project is it?</h2>
      <a class="choice" href="{ESTIMATOR}" data-project="new"><span>New Informatica MDM implementation</span><span class="arrow">→</span></a>
      <a class="choice" href="{ESTIMATOR}" data-project="modernize"><span>Moving an on-prem hub to MDM SaaS</span><span class="arrow">→</span></a>
      <a class="choice" href="#contact" data-project="expand"><span>Adding a domain to a live hub<small>We'll scope this one on a short call</small></span><span class="arrow">→</span></a>
      <a class="choice" href="#contact" data-project="replace"><span>Replacing another MDM<small>We'll scope this one on a short call</small></span><span class="arrow">→</span></a>
      <p class="fine">Takes about five minutes. A person on our team reviews every answer. You're not signing up for anything.</p>
    </div>"""

CONTACT = """<section class="sec tint contact" id="contact">
  <div class="wrap">
    <div>
      <h2>Tell us about your project</h2>
      <p class="big">For domain expansions, replacements and integrations, or anything you'd rather talk through first. An MDM consultant will reply.</p>
      <p>Or use the <a href="#start">5-minute questionnaire</a> for a written estimate.</p>
      <p class="mute">Email us directly at <a href="mailto:info@zclap.com">info@zclap.com</a></p>
    </div>
    <form id="contact-form" action="https://api.web3forms.com/submit" method="POST">
      <div class="ok"><h3>Thanks, it's with our team.</h3><p>An MDM consultant will be in touch shortly.</p></div>
      <div class="fields">
        <input type="hidden" name="access_key" value="fde866e1-2dad-4c62-838c-498b62151c5c">
        <input type="hidden" name="subject" value="New inquiry from zclap.com/{slug}">
        <input type="checkbox" name="botcheck" style="display:none" tabindex="-1" autocomplete="off">
        <div class="pair">
          <div><label for="f-name">Name</label><input id="f-name" name="name" required autocomplete="name"></div>
          <div><label for="f-email">Work email</label><input id="f-email" name="email" type="email" required autocomplete="email"></div>
        </div>
        <label for="f-company">Company</label><input id="f-company" name="company" required autocomplete="organization">
        <label for="f-type">Project</label>
        <select id="f-type" name="project_type">
          <option data-project="new">New Informatica MDM implementation</option>
          <option data-project="modernize">On-prem to SaaS modernization</option>
          <option data-project="expand">Adding a domain</option>
          <option data-project="replace">Replacing another MDM</option>
          <option data-project="integrate">Integration with Salesforce, SAP, Workday or Oracle</option>
          <option data-project="other">Something else</option>
        </select>
        <label for="f-msg">What are you trying to get done?</label><textarea id="f-msg" name="message" required></textarea>
        <button class="btn btn-primary" type="submit" style="width:100%;justify-content:center">Send to an MDM consultant <span class="arrow">→</span></button>
      </div>
    </form>
  </div>
</section>"""

def faq_jsonld(body):
    qs = re.findall(r"<details><summary>(.*?)</summary>(.*?)</details>", body, re.S)
    if not qs: return ""
    strip = lambda s: html.unescape(re.sub(r"<[^>]+>", " ", s)).split()
    items = [{"@type": "Question", "name": " ".join(strip(q)),
              "acceptedAnswer": {"@type": "Answer", "text": " ".join(strip(a))}} for q, a in qs]
    return '<script type="application/ld+json" data-faq>' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}) + "</script>"

def page(meta, body):
    slug = meta["slug"]; url = f"{SITE}/{slug}/"
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "ZCLAP", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": meta["crumb"], "item": url}]}
    service = {"@context": "https://schema.org", "@type": "Service", "name": meta["crumb"], "serviceType": "Informatica MDM consulting",
               "provider": {"@type": "ProfessionalService", "name": "ZCLAP", "url": SITE + "/"}, "areaServed": "US", "url": url,
               "description": meta["description"]}
    topics = " ".join(f'<a href="../{s}/"{" aria-current=page" if s == slug else ""}>{n}</a>' for s, n in TOPICS)
    hero = f"""<section class="hero">
  <div class="wrap">
    <div>
      <nav class="crumbs" aria-label="Breadcrumb"><a href="../">ZCLAP</a> / <span>{meta["crumb"]}</span></nav>
      <span class="kicker">{meta["kicker"]}</span>
      <h1>{meta["h1"]}</h1>
      <p class="big">{meta["lead"]}</p>
      <div class="hero-proof">
        <div><b>150+</b>MDM projects delivered across our team</div>
        <div><b>85%</b>of our consultants hold an Informatica certification</div>
        <div><b>72 hrs</b>from your answers to a written estimate</div>
      </div>
    </div>
    {STARTER}
  </div>
</section>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{meta["title"]}</title>
<meta name="description" content="{html.escape(meta["description"])}">
<meta name="robots" content="noindex"><!-- preview only: remove when this goes live on zclap.com -->
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="../assets/favicon.png">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{html.escape(meta["title"])}">
<meta property="og:description" content="{html.escape(meta["description"])}">
<meta property="og:image" content="{SITE}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
{FONTS}
<link rel="stylesheet" href="../styles.css">
<script type="application/ld+json">{json.dumps(service)}</script>
<script type="application/ld+json">{json.dumps(crumbs)}</script>
{faq_jsonld(body)}
{GTAG}
</head>
<body>
<!-- Built by build.py from pages/{slug}.html. Edit that file, not this one. -->
<header class="top">
  <div class="wrap">
    <a href="../" aria-label="ZCLAP home"><img src="../assets/logo-dark.png" alt="ZCLAP" width="142" height="32"></a>
    <button class="menu" aria-label="Menu" aria-expanded="false" aria-controls="menu">☰</button>
    <nav id="menu">
      <a href="../#services">Services</a>
      <a href="../#work">Work</a>
      <a href="#faq">FAQ</a>
      <a href="../">Home</a>
      <a class="btn btn-primary" href="#start" data-track="nav_estimate">Get an estimate</a>
    </nav>
  </div>
</header>
<main>
{hero}
<div class="topics"><div class="wrap"><span>Informatica MDM guides:</span> {topics}</div></div>
{body}
{CONTACT.replace("{slug}", slug)}
</main>
{footer("../")}
<div class="mbar"><a class="btn btn-primary" href="#start" data-track="mobile_bar">Get a free MDM estimate <span class="arrow">→</span></a></div>
<script src="../site.js" defer></script>
</body>
</html>
"""

def footer(root):
    links = "".join(f'<a href="{root}{s}/">{n}</a>' for s, n in TOPICS)
    return f"""<footer>
  <div class="wrap">
    <img src="{root}assets/logo-dark.png" alt="ZCLAP" width="107" height="24">
    <span>© 2026 ZCLAP</span>
    <span class="flinks">{links}<a href="https://zclap.com/estimator/">MDM estimator</a><a href="mailto:info@zclap.com">info@zclap.com</a><a href="https://www.linkedin.com/company/zclap-inc/" rel="noopener">LinkedIn</a></span>
  </div>
</footer>"""

def add_faq_to(path):
    s = open(path).read()
    s = re.sub(r'<script type="application/ld\+json" data-faq>.*?</script>\n?', "", s, flags=re.S)
    tag = faq_jsonld(s)
    if tag: s = s.replace("</head>", tag + "\n</head>", 1)
    open(path, "w").write(s)

def main():
    root = os.path.dirname(os.path.abspath(__file__)); os.chdir(root)
    built = []
    for f in sorted(glob.glob("pages/*.html")):
        src = open(f).read()
        m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->\s*(.*)", src, re.S)
        meta, body = json.loads(m.group(1)), m.group(2)
        os.makedirs(meta["slug"], exist_ok=True)
        open(f'{meta["slug"]}/index.html', "w").write(page(meta, body))
        built.append(meta["slug"])
    for p in ["index.html", "healthcare/index.html"]: add_faq_to(p)
    today = datetime.date.today().isoformat()
    urls = ["", "healthcare/"] + [s + "/" for s in built] + ["estimator/"]
    open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{SITE}/{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    print("built:", ", ".join(built) or "(none)", "| sitemap:", len(urls), "urls")

if __name__ == "__main__": main()
