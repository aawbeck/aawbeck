import pandas as pd, numpy as np
from fcd_gauges import pick
from stations import AREAS
f = pd.read_csv("data/fcd_daily.csv", parse_dates=["DATE"]).dropna(subset=["INCHES"])
f = f[(f.DATE >= "2016-01-01") & (f.DATE <= "2025-12-31")]
f["WY"] = f.DATE.dt.year; f["M"] = f.DATE.dt.month   # calendar years, to match the temperature window
rows = []
for a, g in pick().items():
    ids = [i for _, i, _ in g]
    x = f[f.GAUGE.isin(ids)]
    for wy, xy in x.groupby("WY"):
        n = xy.groupby("GAUGE").size(); ok = n[n >= 350].index          # gauge-year needs 350+ days
        xy = xy[xy.GAUGE.isin(ok)]
        if xy.empty: continue
        p = xy.groupby("GAUGE").apply(lambda t: pd.Series(dict(total=t.INCHES.sum(),
              monsoon=t[t.M.between(6,9)].INCHES.sum(), days=(t.INCHES >= 0.03).sum())), include_groups=False)
        rows.append(dict(area=a, year=wy, fcd_gauges=len(p), fcd_rain_in=p.total.mean(), fcd_monsoon_in=p.monsoon.mean(),
                         fcd_winter_in=p.total.mean()-p.monsoon.mean(), fcd_rain_days=p.days.mean(), fcd_wettest_gauge=p.total.max(), fcd_driest_gauge=p.total.min()))
fa = pd.DataFrame(rows); fa.round(2).to_csv("data/fcd_annual_by_area.csv", index=False)
s = fa.groupby("area").agg(fcd_gauges=("fcd_gauges","max"), fcd_years=("year","count"), fcd_rain_in=("fcd_rain_in","mean"),
        fcd_monsoon_in=("fcd_monsoon_in","mean"), fcd_winter_in=("fcd_winter_in","mean"), fcd_rain_days=("fcd_rain_days","mean"),
        fcd_driest_year=("fcd_rain_in","min"), fcd_wettest_year=("fcd_rain_in","max"))
# NOAA volunteer-gauge calendar-year totals for comparison
n = pd.read_csv("data/noaa_daily.csv", parse_dates=["DATE"]).dropna(subset=["PRCP"])
n["WY"] = n.DATE.dt.year
c = {}
for a, (_, gauges) in AREAS.items():
    g = n[n.STATION.isin(gauges) & (n.DATE >= "2016-01-01") & (n.DATE <= "2025-12-31")]
    cnt = g.groupby(["STATION","WY"]).size().rename("n").reset_index(); good = cnt[cnt.n >= 330]
    g = g.merge(good[["STATION","WY"]]); t = g.groupby(["STATION","WY"]).PRCP.sum().reset_index()
    c[a] = t.groupby("WY").PRCP.mean().mean() if len(t) else np.nan
s["noaa_rain_in"] = pd.Series(c)
s["diff_pct"] = (s.noaa_rain_in / s.fcd_rain_in - 1) * 100
s.round(2).to_csv("data/fcd_summary.csv")
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 20)
print(s.round(1).to_string())
print(); print(fa[fa.area.isin(["Gilbert","Chandler"])].pivot(index="year", columns="area", values="fcd_rain_in").round(1).T.to_string())

# monthly climatology (10-yr mean monthly total, averaged over qualifying gauges) for the month chart
mm = []
for a, g in pick().items():
    x = f[f.GAUGE.isin([i for _, i, _ in g])]
    t = x.groupby(["GAUGE","WY","M"]).INCHES.sum().reset_index()
    for mo, tm in t.groupby("M"):
        mm.append(dict(area=a, month=mo, fcd_rain_in=tm.groupby("GAUGE").INCHES.sum().mean() / 10))
pd.DataFrame(mm).round(3).to_csv("data/fcd_monthly.csv", index=False)
