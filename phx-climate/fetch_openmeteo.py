# Gridded (reanalysis-based) daily temps for places with no long-record station. Includes Sky Harbor as a bias check.
import json, time, urllib.request, csv
PTS = {"Gilbert":(33.35,-111.79), "Chandler":(33.30,-111.84), "SkyHarbor_check":(33.4278,-112.0036)}
rows=[]
for n,(la,lo) in PTS.items():
    u=("https://archive-api.open-meteo.com/v1/archive?latitude=%s&longitude=%s&start_date=2016-01-01&end_date=2025-12-31"
       "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&temperature_unit=fahrenheit&precipitation_unit=inch&timezone=America%%2FPhoenix"%(la,lo))
    for k in range(4):
        try: j=json.load(urllib.request.urlopen(u,timeout=120)); break
        except Exception as e: print("retry",n,e); time.sleep(10*(k+1))
    d=j["daily"]; print(n, j.get("elevation"), len(d["time"]))
    rows+=[(n,t,a,b,c) for t,a,b,c in zip(d["time"],d["temperature_2m_max"],d["temperature_2m_min"],d["precipitation_sum"])]
    time.sleep(5)
with open("data/openmeteo_daily.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["POINT","DATE","TMAX","TMIN","PRCP"]); w.writerows(rows)
