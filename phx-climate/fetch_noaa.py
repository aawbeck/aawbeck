import csv, io, sys, time, urllib.request
from stations import AREAS
ids = sorted({AREAS[a][0] for a in AREAS} | {s for a in AREAS for s in AREAS[a][1]})
url = ("https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries"
       "&dataTypes=PRCP,TMAX,TMIN&startDate=2016-01-01&endDate=2025-12-31"
       "&format=csv&units=standard&stations=%s")
out = "data/noaa_daily.csv"; rows = []; hdr = None
for i in range(0, len(ids), 6):
    chunk = ids[i:i+6]
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url % ",".join(chunk), timeout=180) as r:
                text = r.read().decode()
            break
        except Exception as e:
            print("retry", chunk, e, file=sys.stderr); time.sleep(3*(attempt+1))
    rd = list(csv.reader(io.StringIO(text)))
    hdr = hdr or rd[0]; rows += rd[1:]
    print(chunk, len(rd)-1, file=sys.stderr)
import os; os.makedirs("data", exist_ok=True)
with open(out, "w", newline="") as f:
    w = csv.writer(f); w.writerow(hdr); w.writerows(rows)
print("wrote", len(rows), "rows")
