"""Builds downloads/mdm-hub-to-saas-worksheet.xlsx, the playbook's companion worksheet.
Run: python3 tools/make_worksheet.py (needs openpyxl).
The component-to-SaaS mapping and approaches follow Informatica Global Customer Support's
"MDM Modernization: Transitioning from On-Premises to SaaS" (Tech Tuesdays, 18 Feb 2025)."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

NAVY, ORANGE, PAPER = "17324D", "E4622A", "FBF9F5"
head = Font(bold=True, color="FFFFFF"); fill = PatternFill("solid", fgColor=NAVY)
wrap = Alignment(wrap_text=True, vertical="top"); thin = Side(style="thin", color="E2DCD1")
box = Border(bottom=thin)

def sheet(wb, title, intro, headers, rows, widths, inputs=()):
    ws = wb.create_sheet(title)
    ws["A1"] = title; ws["A1"].font = Font(bold=True, size=14, color=NAVY)
    ws["A2"] = intro; ws["A2"].alignment = wrap; ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(headers))
    ws.row_dimensions[2].height = 48
    for j, h in enumerate(headers, 1):
        c = ws.cell(4, j, h); c.font = head; c.fill = fill; c.alignment = wrap
    for i, r in enumerate(rows, 5):
        for j, v in enumerate(r, 1):
            c = ws.cell(i, j, v); c.alignment = wrap; c.border = box
            if headers[j - 1] in inputs: c.fill = PatternFill("solid", fgColor="FFF2EC")
    for j, w in enumerate(widths, 1): ws.column_dimensions[chr(64 + j)].width = w
    ws.freeze_panes = "A5"
    return ws

wb = Workbook(); wb.remove(wb.active)

ws = wb.create_sheet("Start here")
lines = [("Informatica MDM Hub to MDM SaaS: migration worksheet", Font(bold=True, size=16, color=NAVY)),
         ("A companion to ZCLAP's migration playbook (zclap.com/mdm-saas-migration-playbook/).", None),
         ("", None),
         ("How to use it", Font(bold=True, size=12, color=NAVY)),
         ("1. Hub inventory: count what your hub has. Orange cells are for you to fill in. The counts drive most of the effort.", None),
         ("2. Data checks: run the consistency checks before any data moves. Table names are examples; use your own base objects.", None),
         ("3. Parity tests: agree what 'the same result' means, then measure it before cutover.", None),
         ("4. Cutover: the go-live checklist.", None),
         ("", None),
         ("Approaches (Informatica's terms)", Font(bold=True, size=12, color=NAVY)),
         ("Lift-and-shift: mapped one-to-one to MDM SaaS.", None),
         ("Refactor: same business behavior, rebuilt with SaaS features and best practices.", None),
         ("Redesign: rebuilt from scratch for SaaS. Most projects mix all three.", None),
         ("", None),
         ("Want a fixed-price estimate? Send this worksheet with your answers to info@zclap.com, or take the 5-minute questionnaire at zclap.com/estimator/.", Font(bold=True, color=ORANGE)),
         ("Source for the component mapping: Informatica GCS, 'MDM Modernization: Transitioning from On-Premises to SaaS', Tech Tuesdays webinar, 18 Feb 2025. Informatica's capabilities change; confirm details with Informatica for your version.", Font(italic=True, color="69717C"))]
for i, (t, f) in enumerate(lines, 1):
    c = ws.cell(i, 1, t); c.alignment = Alignment(wrap_text=True)
    if f: c.font = f
ws.column_dimensions["A"].width = 120

inv = [
 ("Data model", "Base objects (business entities)", "Hub Console > Schema; Provisioning tool", "Business entities in the Business 360 application", "Lift-and-shift, refactor"),
 ("Data model", "Lookup / reference tables", "Schema: lookup base objects", "Reference 360: reference data sets and code lists", "Lift-and-shift, refactor"),
 ("Data model", "Hierarchies", "Hierarchy Manager; Provisioning tool", "Hierarchy models in Business 360", "Lift-and-shift, refactor"),
 ("Data model", "Relationships", "Hierarchy Manager relationship types", "Relationship models in Business 360", "Lift-and-shift, refactor"),
 ("Matching", "Match rules (match paths, columns, rule sets)", "Hub Console > Match/Merge Setup", "Match configuration on the business entity", "Refactor, redesign"),
 ("Matching", "Trust and survivorship settings", "Hub Console > Systems and Trust", "Survivorship on the business entity", "Refactor, redesign"),
 ("Data quality", "Validation rules", "Hub Console > validation rules", "Basic DQ rules on the business entity; advanced rules in Cloud Data Quality", "Refactor, redesign"),
 ("Data quality", "IDQ rules / mapplets", "Informatica Developer (IDQ)", "Basic and advanced DQ rules (Cloud Data Quality)", "Redesign"),
 ("Data quality", "Cleanse functions (Siperian)", "Hub Console > Cleanse Functions", "Basic and advanced DQ rules (Cloud Data Quality)", "Redesign"),
 ("Data quality", "Address Doctor (batch)", "Cleanse functions / IDQ", "DaaS Address Verifier (batch)", "Lift-and-shift, refactor"),
 ("Data quality", "Real-time address, email, phone validation", "DaaS cleanse functions", "DaaS for address, email and phone validation", "Lift-and-shift, refactor"),
 ("Data quality", "Other DaaS enrichment providers", "Cleanse functions / external calls", "Cloud Application Integration", "Redesign"),
 ("Custom code", "Hub user exits", "Custom Java in the hub", "Cloud Data Quality, Cloud Application Integration, Cloud Data Integration", "Redesign"),
 ("Custom code", "IDD user exits", "Data Director customizations", "Cloud Application Integration, Cloud Data Integration", "Redesign"),
 ("Custom code", "External calls", "Hub external call configuration", "Cloud Data Quality, Application Integration, Data Integration", "Redesign"),
 ("Workflow", "Siperian workflows", "Hub workflow configuration", "Out-of-the-box one- and two-step approvals (Application Integration)", "Lift-and-shift, refactor"),
 ("Workflow", "ActiveVOS workflows", "ActiveVOS / BPM", "Out-of-the-box one- and two-step approvals (Application Integration)", "Lift-and-shift, refactor"),
 ("Workflow", "Custom workflows", "ActiveVOS custom processes", "Cloud Application Integration with human tasks", "Redesign"),
 ("Integration", "SIF API consumers", "Applications calling SIF", "Business Entity Services REST APIs", "Refactor, redesign"),
 ("Integration", "Business Entity Services consumers", "Applications calling BES", "Business Entity Services REST APIs", "Lift-and-shift, refactor"),
 ("Integration", "Outbound JMS message queues", "Message queue configuration", "Published business events (batch and real time); streaming ingestion in Cloud Data Integration", "Refactor, redesign"),
 ("Batch", "Stage and load jobs", "Batch Viewer / batch groups", "Ingress jobs with Cloud Data Integration taskflows", "Refactor, redesign"),
 ("Batch", "Match, merge, tokenize and index jobs", "Batch Viewer", "Business 360 Console job definitions", "Refactor"),
 ("Batch", "Batch groups / command-line orchestration", "Batch groups, scripts, schedulers", "REST APIs through Cloud Application Integration", "Refactor, redesign"),
 ("Users", "Users, roles and SSO", "Hub security access manager", "IDMC Administrator services", "Lift-and-shift, refactor"),
 ("UI", "Data Director applications and layouts", "IDD / Provisioning tool layouts", "Business 360 pages, layouts and search", "Refactor"),
]
rows = [(a, b, c, "", "", d, e, "") for a, b, c, d, e in inv]
ws = sheet(wb, "Hub inventory", "One row per kind of component. Fill in the count and whether it's customized. Custom code and heavily tuned matching drive more effort than record volume.",
           ["Area", "Component", "Where to find it on-prem", "Count in your hub", "Customized? (Y/N)", "MDM SaaS equivalent", "Typical approach", "Your notes"],
           rows, [13, 34, 30, 12, 12, 44, 20, 30], inputs=("Count in your hub", "Customized? (Y/N)", "Your notes"))
dv = DataValidation(type="list", formula1='"Y,N"', allow_blank=True); ws.add_data_validation(dv); dv.add(f"E5:E{4 + len(rows)}")
n = 5 + len(rows) + 1
ws.cell(n, 1, "Also note:").font = Font(bold=True, color=NAVY)
for i, t in enumerate(["Number of source systems feeding the hub", "Number of systems consuming the hub (and which are real time)", "Record volumes per base object", "Hub version and patch level", "Target date (renewal, support end, budget cycle)"], 1):
    ws.cell(n + i, 2, t); ws.cell(n + i, 4).fill = PatternFill("solid", fgColor="FFF2EC")

checks = [
 ("Base object records with no cross-reference", "Records in the base object (C_PARTY) whose ROWID_OBJECT has no row in its XREF table. Fix or explain before migrating.",
  "SELECT b.ROWID_OBJECT FROM C_PARTY b LEFT JOIN C_PARTY_XREF x ON x.ROWID_OBJECT = b.ROWID_OBJECT WHERE x.ROWID_OBJECT IS NULL;"),
 ("Orphan child records", "Child rows whose parent no longer exists (example: addresses without a party).",
  "SELECT c.ROWID_OBJECT FROM C_ADDRESS c LEFT JOIN C_PARTY p ON p.ROWID_OBJECT = c.PARTY_ID WHERE p.ROWID_OBJECT IS NULL;"),
 ("Business entity model complete in MDM SaaS", "The SaaS business entity model, including logical attributes for every field you'll load, must be finished before data loads.", ""),
 ("Business ID plan", "In MDM SaaS, an incoming record with an existing Business ID merges into it and skips matching; a new Business ID is a new record. Decide how IDs are generated and what downstream systems consume.", ""),
 ("History tables", "Informatica (Feb 2025) said history data can't currently be migrated and recommended keeping it in a data lake. Decide where history lives and who needs it.", ""),
 ("Lookup values", "Load code lists into Reference 360 first (file import through the UI or API, or ingress).", ""),
 ("Load order", "Extract from the on-prem XREF and load root entities first, then children, then grandchildren.", ""),
 ("Winning records first", "Per source system: first the XREF rows where ROWID_OBJECT = ORIG_ROWID_OBJECT, then the remaining active rows (ROWID_OBJECT != ORIG_ROWID_OBJECT and HUB_STATE_IND = 1).",
  "SELECT * FROM C_PARTY_XREF WHERE ROWID_SYSTEM = :system AND ROWID_OBJECT = ORIG_ROWID_OBJECT;"),
 ("Enrichment on or off during load", "Decide whether DaaS phone, address and email enrichment runs during the migration load. On means data changes as it loads; off means a straight copy.", ""),
]
ws = sheet(wb, "Data checks", "Run these before moving any data. The SQL is illustrative: replace C_PARTY, C_ADDRESS and column names with your own base objects. Approach follows Informatica's Feb 2025 modernization guidance.",
           ["Check", "What it means", "Example SQL (adapt to your schema)", "Result / count", "Owner", "Done?"],
           [(a, b, c, "", "", "") for a, b, c in checks], [34, 60, 70, 16, 14, 8], inputs=("Result / count", "Owner", "Done?"))

parity = [
 ("Golden record count per entity", "Count of golden records in the hub vs MDM SaaS, per entity and record type", "Exact match, or every difference explained"),
 ("Cross-reference count per source", "Source records per source system in each platform", "Exact match"),
 ("Match outcomes on a known sample", "A sample of known duplicates and known non-duplicates, run through both", "Same merges; any change agreed with data owners"),
 ("Survivorship on key attributes", "For a sample of golden records, compare the winning value of each key attribute", "Same winner, or an agreed improvement"),
 ("Hierarchy and relationship counts", "Parents, children and relationship types", "Exact match"),
 ("Downstream outputs", "What each consuming system receives (files, events, API responses) for the same inputs", "Consumers sign off"),
 ("Performance", "Batch run times and real-time API latency against today's", "Within agreed limits"),
]
sheet(wb, "Parity tests", "Agree these with the business before the build starts, then measure them. Parity you can show beats parity you assume.",
      ["Test", "What to compare", "Pass when", "Result", "Signed off by"],
      [(a, b, c, "", "") for a, b, c in parity], [34, 60, 40, 20, 18], inputs=("Result", "Signed off by"))

cut = ["Freeze configuration changes on the on-prem hub", "Final delta load from the on-prem XREF", "Parity tests rerun on the final load",
       "Switch each consuming system (list them on the inventory sheet)", "Switch source systems to load MDM SaaS", "Rollback plan written and tested",
       "Stewards trained on Business 360 pages and tasks", "On-prem hub kept read-only for an agreed period, then retired", "History data archived (data lake or warehouse)"]
sheet(wb, "Cutover", "The go-live checklist.", ["Step", "Owner", "Date", "Done?"], [(t, "", "", "") for t in cut], [70, 18, 14, 8], inputs=("Owner", "Date", "Done?"))

wb.save("downloads/mdm-hub-to-saas-worksheet.xlsx")
print("downloads/mdm-hub-to-saas-worksheet.xlsx:", len(inv), "inventory rows,", len(checks), "checks,", len(parity), "parity tests")
