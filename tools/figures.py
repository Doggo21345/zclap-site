"""Writes the explanatory diagrams to assets/fig-*.svg. Run: python3 tools/figures.py
Plain SVG, site colors, system fonts (an <img> SVG can't load the page's web fonts)."""
INK, NAVY, OR, RULE, MUTE, PAPER = "#14202E", "#17324D", "#E4622A", "#E2DCD1", "#69717C", "#FBF9F5"
SANS = "IBM Plex Sans, -apple-system, Segoe UI, Helvetica, Arial, sans-serif"
SERIF = "Source Serif 4, Georgia, serif"

def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">'
            f'<title>{title}</title><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker><marker id="o" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{OR}"/></marker></defs>{body}</svg>')

def box(x, y, w, h, fill="#fff", stroke=RULE, sw=1.2, r=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def text(x, y, s, size=14, color=INK, weight=400, family=SANS, anchor="start"):
    s = s.replace("&", "&amp;")
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{s}</text>'

def line(x1, y1, x2, y2, color=INK, marker="a", dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="M{x1},{y1} C{(x1+x2)/2},{y1} {(x1+x2)/2},{y2} {x2},{y2}" fill="none" stroke="{color}" stroke-width="1.4"{d} marker-end="url(#{marker})"/>'

def golden(sources, result, title, merged_label="Match and merge"):
    W, H = 860, 330; b = []
    for i, (sys, l1, l2) in enumerate(sources):
        y = 24 + i * 100
        b += [box(10, y, 270, 78), text(28, y + 24, sys.upper(), 11, MUTE, 600), text(28, y + 47, l1, 15, INK, 500), text(28, y + 66, l2, 13, MUTE)]
        b.append(line(282, y + 39, 352, 165))
    b += [box(356, 132, 150, 66, PAPER, INK, 1.2), text(431, 162, merged_label, 14, INK, 600, anchor="middle"), text(431, 182, "rules you control", 12, MUTE, anchor="middle")]
    b.append(line(508, 165, 566, 165, OR, "o"))
    b += [box(570, 74, 280, 182, "#fff", OR, 2, 10), text(590, 104, "GOLDEN RECORD", 11, OR, 700)]
    for i, l in enumerate(result):
        b.append(text(590, 136 + i * 26, l, 16 if i == 0 else 14, INK if i == 0 else "#36404c", 600 if i == 0 else 400, SERIF if i == 0 else SANS))
    return svg(W, H, "".join(b), title)

def architecture():
    W, H = 940, 360; b = []
    srcs = ["Salesforce (CRM)", "SAP / Oracle (ERP)", "Claims, policy, billing", "Spreadsheets and files"]
    cons = ["Sales and service", "Finance and procurement", "Analytics and AI", "Portals and partners"]
    b.append(text(10, 22, "SOURCES", 11, MUTE, 600)); b.append(text(930, 22, "WHERE IT'S USED", 11, MUTE, 600, anchor="end"))
    for i, s in enumerate(srcs):
        y = 40 + i * 76
        b += [box(10, y, 210, 54), text(26, y + 33, s, 14, INK, 500), line(222, y + 27, 318, 180)]
    b += [box(322, 52, 296, 256, PAPER, INK, 1.4, 12), text(470, 90, "Informatica MDM SaaS", 19, INK, 600, SERIF, "middle")]
    for i, c in enumerate(["Match and merge", "Data quality rules", "Hierarchies", "Stewardship and approvals"]):
        y = 112 + i * 46
        b += [box(346, y, 248, 34, "#fff", RULE, 1, 6), text(470, y + 22, c, 13, INK, 500, anchor="middle")]
    for i, c in enumerate(cons):
        y = 40 + i * 76
        b += [line(620, 180, 716, y + 27, OR, "o"), box(720, y, 210, 54, "#fff", OR, 1.4), text(736, y + 33, c, 14, INK, 500)]
    return svg(W, H, "".join(b), "Sources feed Informatica MDM SaaS, which matches and cleans records and sends trusted golden records to the systems people use")

def migration():
    W, H = 940, 330; b = []
    left = ["Base objects and lookups", "Match and trust rules", "User exits, external calls", "ActiveVOS workflows", "SIF, BES, JMS integrations"]
    right = ["Business entities, Reference 360", "Match and survivorship config", "Cloud Data Quality / App Integration", "Out-of-the-box approvals", "REST APIs and business events"]
    b += [text(10, 22, "ON-PREM MDM HUB (10.x)", 11, MUTE, 700), text(930, 22, "INFORMATICA MDM SAAS", 11, OR, 700, anchor="end")]
    for i, (l, r) in enumerate(zip(left, right)):
        y = 38 + i * 56
        name, col = [("Lift-and-shift, refactor", "#7A8794"), ("Refactor, redesign", NAVY), ("Redesign", OR), ("Lift-and-shift, refactor", NAVY), ("Refactor, redesign", NAVY)][i]
        b += [box(10, y, 290, 42), text(26, y + 27, l, 14, INK, 500)]
        b += [f'<line x1="304" y1="{y+21}" x2="632" y2="{y+21}" stroke="{col}" stroke-width="1.6" marker-end="url(#a)"/>',
              box(370, y + 8, 196, 26, PAPER, col, 1, 13), text(468, y + 26, name, 12, col, 600, anchor="middle")]
        b += [box(640, y, 290, 42, "#fff", OR, 1.3), text(656, y + 27, r, 14, INK, 500)]
    b.append(text(470, 322, "Approach per component follows Informatica's Feb 2025 modernization guidance", 11, MUTE, 400, anchor="middle"))
    return svg(W, H, "".join(b), "How on-prem MDM Hub components map to Informatica MDM SaaS, and the approach for each")

figs = {
    "fig-golden-record.svg": golden(
        [("CRM", "Jon Smith", "12 Main St · (555) 010-2000"), ("ERP", "J. Smith", "12 Main Street, Apt 4"), ("Billing", "Jonathan Smith", "jsmith@acme.com")],
        ["Jonathan Smith", "12 Main Street, Apt 4", "(555) 010-2000", "jsmith@acme.com", "Linked to: CRM, ERP, Billing"],
        "Three records for the same customer from CRM, ERP and billing are matched and merged into one golden record"),
    "fig-provider-record.svg": golden(
        [("Credentialing", "Maria Lopez, MD", "NPI on file · Cardiology"), ("Claims", "M. Lopez", "Lopez Heart Clinic"), ("Directory", "Dr. Maria Lopez", "Old address · not accepting")],
        ["Dr. Maria Lopez, MD", "Cardiology · Lopez Heart Clinic", "Current address and phone", "Accepting new patients", "Linked to: credentialing, claims, directory"],
        "Three records for the same provider from credentialing, claims and the directory become one provider record", "Match and merge"),
    "fig-architecture.svg": architecture(),
    "fig-migration.svg": migration(),
}
for name, s in figs.items():
    open("assets/" + name, "w").write(s)
print("wrote", ", ".join(figs))
