# Daily rainfall from Flood Control District of Maricopa County (FCDMC) official precipitation records.
# The 2025 workbook for each gauge holds the full daily history by water year (Oct-Sep).
import csv, os, urllib.request, zipfile, io, datetime as dt, openpyxl
from fcd_gauges import pick
ZIP = "/tmp/fcd/zips/Master_Rain_xlsx_2025.zip"
if not os.path.exists(ZIP):
    os.makedirs(os.path.dirname(ZIP), exist_ok=True)
    urllib.request.urlretrieve("https://alert.fcd.maricopa.gov/alert/Rain/FOPR/Master_Rain_xlsx_2025.zip", ZIP)
chosen = {}
for a, g in pick().items():
    for _, gid, name in g: chosen[gid] = name
z = zipfile.ZipFile(ZIP); names = {os.path.basename(n): n for n in z.namelist()}
rows = []
for gid, name in sorted(chosen.items()):
    fn = names.get(f"{gid}_FOPR.xlsx")
    if not fn: print("missing workbook", gid, name); continue
    wb = openpyxl.load_workbook(io.BytesIO(z.read(fn)), read_only=True, data_only=True)
    n = 0
    for wy in range(2016, 2025):   # WY2025+ come from the pcp_WY files below
        if str(wy) not in wb.sheetnames: continue
        lo, hi = dt.datetime(wy-1, 10, 1), dt.datetime(wy, 9, 30)
        for d, v, *_ in wb[str(wy)].iter_rows(values_only=True):
            # some sheets in the District's archive are stale copies of other years; keep only in-water-year dates
            if not isinstance(d, dt.datetime) or not (lo <= d <= hi): continue
            ok = isinstance(v, (int, float))
            rows.append((gid, name, d.date().isoformat(), round(v, 3) if ok else ""))
            n += ok
    print(gid, name, n)
# WY2025 onward: District daily-totals workbooks (one sheet per month, gauge IDs in a header row)
for wy in (2025, 2026):
    p = f"/tmp/fcd/wy/pcp_WY_{wy}.xlsx"
    if not os.path.exists(p):
        os.makedirs("/tmp/fcd/wy", exist_ok=True)
        urllib.request.urlretrieve(f"https://alert.fcd.maricopa.gov/alert/Rain/pcp_WY_{wy}.xlsx", p)
    wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
    for sh in wb.sheetnames:
        if sh == "Annual_Totals": continue
        grid = list(wb[sh].iter_rows(values_only=True))
        ids = {j: int(v) for j, v in enumerate(grid[2]) if isinstance(v, (int, float)) and int(v) in chosen}
        for r in grid[4:]:
            if not isinstance(r[0], dt.datetime): continue
            for j, gid in ids.items():
                v = r[j]; ok = isinstance(v, (int, float))
                rows.append((gid, chosen[gid], r[0].date().isoformat(), round(v, 3) if ok else ""))
    print("loaded", p)
seen = set(); uniq = []
for r in rows:                                   # de-duplicate (gauge, date)
    if (r[0], r[2]) in seen: continue
    seen.add((r[0], r[2])); uniq.append(r)
rows = uniq
with open("data/fcd_daily.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["GAUGE","NAME","DATE","INCHES"]); w.writerows(rows)
print("rows", len(rows))
