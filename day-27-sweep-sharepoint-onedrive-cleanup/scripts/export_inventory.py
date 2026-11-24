"""SWEEP step 1: export a drive (SharePoint library or OneDrive) to inventory.csv with Microsoft Graph delta.

Read-only. Needs a delegated access token with Files.Read.All (or Sites.Read.All) in GRAPH_TOKEN,
e.g. from Graph Explorer or `az account get-access-token --resource-type ms-graph` in a test tenant.

    GRAPH_TOKEN=... python scripts/export_inventory.py <drive-id> data/inventory.csv

Delta does not return parentReference.path, so paths are rebuilt from parent ids.
"""
import csv, os, sys, time
import urllib.request, json

GRAPH = "https://graph.microsoft.com/v1.0"

def get(url, token):
    for attempt in range(5):
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        try:
            with urllib.request.urlopen(req) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):                      # throttled: honour Retry-After
                time.sleep(int(e.headers.get("Retry-After", 10)))
                continue
            raise
    raise RuntimeError("Too many throttling retries")

def main(drive_id, out):
    token = os.environ["GRAPH_TOKEN"]
    url = f"{GRAPH}/drives/{drive_id}/root/delta?$select=id,name,size,lastModifiedDateTime,parentReference,file,folder,deleted,root"
    items = {}
    while url:
        page = get(url, token)
        for it in page["value"]:
            if "deleted" in it:
                items.pop(it["id"], None)
            else:
                items[it["id"]] = it                       # last occurrence wins
        url = page.get("@odata.nextLink")
    def path(i):
        parts, cur = [], items.get(i)
        while cur and "root" not in cur:
            parts.append(cur["name"])
            cur = items.get(cur.get("parentReference", {}).get("id"))
        return "/" + "/".join(reversed(parts))
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "path", "name", "type", "size", "modified", "quickXorHash", "child_count"])
        for i, it in items.items():
            if "root" in it:
                continue
            is_folder = "folder" in it
            w.writerow([i, path(i), it["name"], "folder" if is_folder else "file", it.get("size", 0),
                        it.get("lastModifiedDateTime", ""),
                        "" if is_folder else it.get("file", {}).get("hashes", {}).get("quickXorHash", ""),
                        it["folder"].get("childCount", 0) if is_folder else ""])
    print(f"{len(items)} items written to {out}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "data/inventory.csv")
