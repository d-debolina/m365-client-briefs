"""Generate a fictional inventory (Contoso Landscaping) with planted sync duplicates and empty folders."""
import csv, random, hashlib, datetime as dt
random.seed(29)
rows, n = [], 0
def nid():
    global n; n += 1; return f"01SWEEP{n:05d}"
def h(s): return hashlib.sha1(s.encode()).hexdigest()[:27] + "="
folders = ["/Projects/2024/Harbour Park", "/Projects/2025/Riverside Gardens", "/Projects/2025/Oak Lane",
           "/Admin/Invoices", "/Admin/HR", "/Photos/Site visits", "/Marketing/Brochures",
           "/Projects/2025/Oak Lane - Copy", "/Old/Desktop backup", "/Old/Empty sync folder", "/Old/Empty sync folder/Sub"]
for f in folders:
    rows.append([nid(), f, f.rsplit("/",1)[-1], "folder", 0, "2025-06-01T09:00:00Z", "", ""])
names = ["Site plan.pdf", "Quote.xlsx", "Planting schedule.docx", "Photo_{i}.jpg", "Invoice_{i}.pdf", "Brochure.pptx"]
base = dt.datetime(2025, 1, 6)
for f in folders[:7]:
    for i in range(1, 9):
        name = random.choice(names).format(i=i)
        size = random.randint(40_000, 25_000_000)
        mod = (base + dt.timedelta(days=random.randint(0, 600))).strftime("%Y-%m-%dT%H:%M:%SZ")
        rows.append([nid(), f"{f}/{name}", name, "file", size, mod, h(f+name), ""])
src = [r for r in rows if r[3] == "file"]
# exact duplicates: whole-folder copy and desktop backup
for r in src:
    if r[1].startswith("/Projects/2025/Oak Lane/"):
        rows.append([nid(), r[1].replace("Oak Lane/", "Oak Lane - Copy/"), r[2], "file", r[4], "2025-11-02T08:15:00Z", r[6], ""])
for r in random.sample(src, 12):
    rows.append([nid(), "/Old/Desktop backup/" + r[2], r[2], "file", r[4], "2024-12-20T17:00:00Z", r[6], ""])
# device-suffixed copies: identical (safe) and different (needs review)
for r in random.sample(src, 6):
    stem, ext = r[2].rsplit(".", 1)
    rows.append([nid(), r[1].rsplit("/",1)[0] + f"/{stem}-OFFICE-PC7.{ext}", f"{stem}-OFFICE-PC7.{ext}", "file", r[4], r[5], r[6], ""])
for r in random.sample(src, 4):
    stem, ext = r[2].rsplit(".", 1)
    rows.append([nid(), r[1].rsplit("/",1)[0] + f"/{stem}-JAMIE-LAPTOP.{ext}", f"{stem}-JAMIE-LAPTOP.{ext}", "file", r[4] + 1234, "2026-02-14T10:30:00Z", h("edit"+r[1]), ""])
with open("data/sample-inventory.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(["id","path","name","type","size","modified","quickXorHash","child_count"]); w.writerows(rows)
print(len(rows), "rows")
