import pandas as pd, json
s=pd.read_csv("data/summary_10yr.csv"); a=pd.read_csv("data/annual_by_area.csv"); m=pd.read_csv("data/monthly_climatology.csv")
fs=pd.read_csv("data/fcd_summary.csv"); fa=pd.read_csv("data/fcd_annual_by_area.csv"); fm=pd.read_csv("data/fcd_monthly.csv")
# County (FCDMC) automated gauges are the primary rain source; NOAA volunteer/co-op gauges kept as a cross-check column.
s=s.drop(columns=["rain_years","rain_in","monsoon_in","winter_in","rain_days"]).merge(
  fs.rename(columns={"fcd_rain_in":"rain_in","fcd_monsoon_in":"monsoon_in","fcd_winter_in":"winter_in","fcd_rain_days":"rain_days","noaa_rain_in":"volunteer_rain_in","fcd_gauges":"rain_gauges"})
    [["area","rain_in","monsoon_in","winter_in","rain_days","volunteer_rain_in","rain_gauges"]],on="area",how="left")
a=a.drop(columns=["gauges","rain_in","monsoon_in","winter_in","rain_days"],errors="ignore").merge(
  fa.rename(columns={"fcd_rain_in":"rain_in","fcd_monsoon_in":"monsoon_in","fcd_winter_in":"winter_in","fcd_rain_days":"rain_days"})
    [["area","year","rain_in","monsoon_in","winter_in","rain_days"]],on=["area","year"],how="outer")
m=m.drop(columns=["rain_in"]).merge(fm.rename(columns={"fcd_rain_in":"rain_in"}),on=["area","month"],how="outer")
s=s.fillna(""); 
data=dict(summary=s.to_dict("records"),annual=a.astype(object).where(a.notna(),None).to_dict("records"),monthly=m.astype(object).where(m.notna(),None).to_dict("records"))
open("report.html","w").write(open("report_template.html").read().replace("/*DATA*/null",json.dumps(data)))
