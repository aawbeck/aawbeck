# Pick FCDMC rain gauges near each area center (precip gauges installed before 2016).
import openpyxl, math
CENTERS = {"Central Phoenix":(33.45,-112.07),"North Phoenix":(33.66,-112.07),"Scottsdale":(33.50,-111.92),
 "North Scottsdale":(33.70,-111.88),"Tempe":(33.41,-111.93),"Mesa (East)":(33.42,-111.70),"Gilbert":(33.35,-111.79),
 "Chandler":(33.30,-111.84),"Fountain Hills":(33.61,-111.72),"Carefree/Cave Creek":(33.82,-111.95),
 "West Valley (Glendale/Peoria)":(33.58,-112.24),"Surprise/Sun City":(33.63,-112.35),
 "Goodyear/Litchfield":(33.45,-112.38),"Apache Junction":(33.41,-111.55)}
def km(a,b):
    return 6371*math.hypot(math.radians(b[0]-a[0]), math.radians(b[1]-a[1])*math.cos(math.radians(a[0])))
def pick(meta="/tmp/fcd/meta/sensors.xlsx", radius_km=8, n=6):
    rows=[r for r in openpyxl.load_workbook(meta,read_only=True).worksheets[0].iter_rows(min_row=2,values_only=True)
          if r[2] and "Precip" in str(r[2]) and r[1] and r[3] and r[3].year<=2015 and r[4]]
    out={}
    for a,c in CENTERS.items():
        d=sorted((km(c,(r[4],r[5])),int(r[1]),r[0]) for r in rows)
        out[a]=[(round(x,1),i,nm) for x,i,nm in d if x<=radius_km][:n] or d[:2]
    return out
if __name__=="__main__":
    for a,g in pick().items(): print(a, g)
