"""Transform a WordPress REST export into a page manifest for PnP PowerShell + a redirect map.
Real export: GET https://<wp-site>/wp-json/wp/v2/posts?per_page=100&page=N  (and /pages)
Usage: python scripts/transform.py wp-export-sample/wp-json-posts.json
"""
import json, sys, csv, re, html, pathlib
CAT_TO_SITE = {"News": "intranet", "Events": "intranet", "HR": "hr", "Learning": "hr", "IT": "it", "Finance": "finance",
               "Facilities": "facilities", "Health & Safety": "facilities", "Policies": "corporate", "Projects": "corporate"}
CAT_TO_TERM = {"HR": "People & HR", "IT": "IT & Tools", "Finance": "Money", "Facilities": "Facilities", "News": "Announcements",
               "Policies": "Policies", "Projects": "Projects", "Events": "Events", "Learning": "Learning", "Health & Safety": "Health & Safety"}
ALLOWED = re.compile(r"</?(p|h2|h3|h4|ul|ol|li|strong|em|a|table|tr|td|th|br)(\s[^>]*)?>", re.I)
def clean(h):  # keep simple, editor-safe HTML; drop shortcodes and inline styles
    h = re.sub(r"\[/?[a-z_\-]+[^\]]*\]", "", h)
    h = re.sub(r'\sstyle="[^"]*"', "", h)
    return "".join(t if t.startswith("<") is False or ALLOWED.fullmatch(t) else "" for t in re.split(r"(<[^>]+>)", h))
items = json.load(open(sys.argv[1], encoding="utf-8"))
out = pathlib.Path(sys.argv[1]).resolve().parents[1] / "scripts"
with open(out/"page-manifest.csv", "w", newline="", encoding="utf-8") as m, open(out/"redirects.csv", "w", newline="", encoding="utf-8") as r:
    mw, rw = csv.writer(m), csv.writer(r)
    mw.writerow(["site", "pageName", "title", "isNews", "topic", "html", "originalModified"]); rw.writerow(["old_url", "new_url"])
    for it in items:
        cat = it["categories_names"][0]; site = CAT_TO_SITE[cat]; name = it["slug"][:60] + ".aspx"
        mw.writerow([site, name, html.unescape(it["title"]["rendered"]), it["type"] == "post", CAT_TO_TERM[cat], clean(it["content"]["rendered"]), it["modified"]])
        rw.writerow([it["link"], f"https://contoso.sharepoint.com/sites/{site}/SitePages/{name}"])
print(f"Wrote {len(items)} pages to scripts/page-manifest.csv and scripts/redirects.csv")
