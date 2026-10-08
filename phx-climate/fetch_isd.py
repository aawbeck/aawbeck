# Daily high/low from hourly airport obs (NOAA ISD) for stations with no GHCN-Daily temperature record.
import csv, io, sys, time, urllib.request, collections, datetime as dt
ST = {"72274953128":"CHD_AP", "72278623104":"IWA_AP", "72278803186":"GYR_AP", "72064400226":"BXK_AP"}   # Chandler Muni, Williams Gateway, Phoenix Goodyear, Buckeye Muni
url = "https://www.ncei.noaa.gov/access/services/data/v1?dataset=global-hourly&dataTypes=TMP&format=csv&stations=%s&startDate=%d-01-01T00:00:00&endDate=%d-12-31T23:59:59"
days = collections.defaultdict(list)
for sid in ST:
    for y in range(2016, 2026):
        for k in range(4):
            try: t = urllib.request.urlopen(url % (sid, y, y), timeout=180).read().decode(); break
            except Exception as e: print("retry", sid, y, e, file=sys.stderr); time.sleep(5*(k+1))
        n = 0
        for r in csv.DictReader(io.StringIO(t)):
            v, q = (r["TMP"].split(",") + ["9"])[:2]
            if v.startswith("+9999") or q in ("2","3","6","7") or not v: continue
            utc = dt.datetime.fromisoformat(r["DATE"]) - dt.timedelta(hours=7)   # Arizona = UTC-7 year round
            days[(ST[sid], utc.date())].append(int(v)/10*9/5+32); n += 1
        print(sid, y, n, file=sys.stderr)
with open("data/airport_daily.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["STATION","DATE","TMAX","TMIN","N_OBS"])
    for (s, d), v in sorted(days.items()):
        if len(v) >= (12 if s in ("CHD_AP", "GYR_AP") else 18): w.writerow([s, d, round(max(v),1), round(min(v),1), len(v)])
