# Daily high/low per airport from the Iowa Environmental Mesonet (computed from the full ASOS/AWOS observation stream).
import csv, io, sys, time, urllib.request
ST = {"PHX":"USW00023183","DVT":"USW00003184","SDL":"USW00003192","CHD":"CHD_AP","IWA":"IWA_AP","GYR":"GYR_AP","BXK":"BXK_AP","GEU":"GEU_AP","FFZ":"FFZ_AP","LUF":"LUF_AP"}
url = "https://mesonet.agron.iastate.edu/cgi-bin/request/daily.py?network=AZ_ASOS&stations=%s&year1=2016&month1=1&day1=1&year2=2025&month2=12&day2=31&format=csv"
rows = []
for s in ST:
    for k in range(4):
        try: t = urllib.request.urlopen(url % s, timeout=180).read().decode(); break
        except Exception as e: print("retry", s, e, file=sys.stderr); time.sleep(5*(k+1))
    n = 0
    for r in csv.DictReader(io.StringIO(t)):
        try: hi, lo = float(r["max_temp_f"]), float(r["min_temp_f"])
        except (TypeError, ValueError): continue
        rows.append((s, r["day"], hi, lo)); n += 1
    print(s, n, file=sys.stderr)
with open("data/iem_daily.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["IEM","DATE","TMAX","TMIN"]); w.writerows(rows)
