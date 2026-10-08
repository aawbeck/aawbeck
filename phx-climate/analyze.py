import pandas as pd, numpy as np
from stations import AREAS, TEMP_PROXY
d = pd.read_csv("data/noaa_daily.csv", parse_dates=["DATE"])
d["Y"], d["M"] = d.DATE.dt.year, d.DATE.dt.month
MIN_DAYS = 330  # station-year needs this many observed days to count

# ---- rain: average of qualifying gauges per area (station-year coverage filter)
pr = d.dropna(subset=["PRCP"])
cov = pr.groupby(["STATION","Y"]).size().rename("n").reset_index()
good = set(map(tuple, cov[cov.n >= MIN_DAYS][["STATION","Y"]].values))
rain_rows = []
for a,(_, gauges) in AREAS.items():
    g = pr[pr.STATION.isin(gauges)]
    g = g[[ (s,y) in good for s,y in zip(g.STATION, g.Y)]]
    for y, gy in g.groupby("Y"):
        per = gy.groupby("STATION").agg(total=("PRCP","sum"), days=("PRCP", lambda x:(x>=0.01).sum()),
              monsoon=("PRCP", lambda x: x[gy.loc[x.index,"M"].between(6,9)].sum()))
        rain_rows.append(dict(area=a, year=y, gauges=len(per), rain_in=per.total.mean(),
              monsoon_in=per.monsoon.mean(), winter_in=per.total.mean()-per.monsoon.mean(), rain_days=per.days.mean()))
rain = pd.DataFrame(rain_rows)

# ---- temperature
t = d.dropna(subset=["TMAX","TMIN"])
temp_rows = []
for a,(ts,_) in AREAS.items():
    g = t[t.STATION == ts]
    for y, gy in g.groupby("Y"):
        n = len(gy)
        if n < 280: continue  # temp: >=~77% of days observed
        sc = 365/n   # scale threshold-day counts for missing days
        temp_rows.append(dict(area=a, year=y, obs_days=n, avg_high=gy.TMAX.mean(), avg_low=gy.TMIN.mean(),
            avg_temp=(gy.TMAX.mean()+gy.TMIN.mean())/2, max_temp=gy.TMAX.max(),
            days_100=(gy.TMAX>=100).sum()*sc, days_105=(gy.TMAX>=105).sum()*sc,
            days_110=(gy.TMAX>=110).sum()*sc, days_115=(gy.TMAX>=115).sum()*sc,
            nights_90=(gy.TMIN>=90).sum()*sc, freeze_days=(gy.TMIN<=32).sum()*sc))
temp = pd.DataFrame(temp_rows)
annual = temp.merge(rain, on=["area","year"], how="outer").sort_values(["area","year"])
annual.round(2).to_csv("data/annual_by_area.csv", index=False)

# monthly climatology (2016-2025 means)
m = []
for a,(ts,gauges) in AREAS.items():
    g = t[t.STATION==ts]
    for mo, gm in g.groupby("M"):
        m.append(dict(area=a, month=mo, avg_high=gm.TMAX.mean(), avg_low=gm.TMIN.mean()))
mt = pd.DataFrame(m)
pm = pr[[ (s,y) in good for s,y in zip(pr.STATION, pr.Y)]]
mr = []
for a,(_, gauges) in AREAS.items():
    g = pm[pm.STATION.isin(gauges)]
    tot = g.groupby(["STATION","Y","M"]).PRCP.sum().reset_index()
    ym = tot.groupby(["Y","M"]).PRCP.mean().reset_index()
    for mo, gm in ym.groupby("M"):
        mr.append(dict(area=a, month=mo, rain_in=gm.PRCP.sum()/ rain[rain.area==a].year.nunique()))
monthly = mt.merge(pd.DataFrame(mr), on=["area","month"], how="outer").sort_values(["area","month"])
monthly.round(2).to_csv("data/monthly_climatology.csv", index=False)

# 10-year summary
sm = annual.groupby("area").agg(temp_years=("avg_high","count"), avg_high=("avg_high","mean"), avg_low=("avg_low","mean"),
    days_100=("days_100","mean"), days_110=("days_110","mean"), nights_90=("nights_90","mean"), freeze_days=("freeze_days","mean"),
    rain_years=("rain_in","count"), rain_in=("rain_in","mean"), monsoon_in=("monsoon_in","mean"), winter_in=("winter_in","mean"), rain_days=("rain_days","mean"))
sm["temp_note"] = [TEMP_PROXY.get(a) or "" for a in sm.index]
sm.round(1).to_csv("data/summary_10yr.csv")
pd.set_option("display.width",250); pd.set_option("display.max_columns",30)
print(sm.drop(columns="temp_note").round(1))
print(); print(annual[annual.area=="Central Phoenix"][["year","avg_high","avg_low","days_110","days_115","nights_90","rain_in","monsoon_in"]].round(1).to_string(index=False))
