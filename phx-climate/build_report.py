import pandas as pd, json
s=pd.read_csv("data/summary_10yr.csv").fillna("")
a=pd.read_csv("data/annual_by_area.csv"); m=pd.read_csv("data/monthly_climatology.csv")
data=dict(summary=s.to_dict("records"), annual=a.where(a.notna(),None).to_dict("records"), monthly=m.where(m.notna(),None).to_dict("records"))
html=open("report_template.html").read().replace("/*DATA*/null", json.dumps(data))
open("report.html","w").write(html)
