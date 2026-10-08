# Map of the Valley: each point of land is shaded with the color of the nearest report area (same colors/order as report.html).
import json, math
from shapely.geometry import shape, mapping, Point, box
from shapely.ops import unary_union, voronoi_diagram
from fcd_gauges import CENTERS
D = json.load(open("data/report_data.json"))
_OLD = ["#1f77b4","#d62728","#2ca02c","#ff7f0e","#9467bd","#8c564b","#e377c2","#17becf","#7f7f7f","#bcbd22","#393b79","#ad494a","#637939","#00a6a6","#e6ab02","#4d4d4d","#ff9896","#98df8a","#c5b0d5","#dbdb8d"]
areas = [r["area"] for r in D["summary"]]; from colors import COLORS
col = {a: COLORS[a] for a in areas}; stats = {r["area"]: r for r in D["summary"]}
K = math.cos(math.radians(33.5))                       # lon scaling so "nearest" is roughly Euclidean
fwd = lambda x, y: (x * K, y)
from shapely.affinity import scale
BBOX = box(-112.75, 33.02, -111.35, 33.98)
cities = json.load(open("data/cities.geojson"))["features"]
land = unary_union([shape(f["geometry"]).buffer(0) for f in cities]).intersection(BBOX)
pts = {a: Point(lo, la) for a, (la, lo) in CENTERS.items()}
sc = lambda g: scale(g, xfact=K, yfact=1, origin=(0, 0))
unsc = lambda g: scale(g, xfact=1/K, yfact=1, origin=(0, 0))
from shapely.geometry import MultiPoint
# Areas that are a single city (or two) use the real city boundary; everything else is split by nearest area center.
CITY_AREA = {"GILBERT":"Gilbert","CHANDLER":"Chandler","TEMPE":"Tempe","FOUNTAIN HILLS":"Fountain Hills","APACHE JUNCTION":"Apache Junction",
             "CAREFREE":"Carefree/Cave Creek","CAVE CREEK":"Carefree/Cave Creek","GLENDALE":"West Valley (Glendale/Peoria)",
             "PEORIA":"West Valley (Glendale/Peoria)","SURPRISE":"Surprise/Sun City",
             "QUEEN CREEK":"Queen Creek","GOODYEAR":"Goodyear","BUCKEYE":"Buckeye","AVONDALE":"Avondale/Litchfield Park",
             "LITCHFIELD PARK":"Avondale/Litchfield Park","TOLLESON":"Avondale/Litchfield Park"}
MAXKM = 15                                    # beyond this distance from an area's center, land is left unshaded
own = {}
for f in cities:
    a = CITY_AREA.get(f["properties"]["CityName"].upper())
    if a: own.setdefault(a, []).append(shape(f["geometry"]).buffer(0))
own = {a: unary_union(g).intersection(BBOX) for a, g in own.items()}
phx = unary_union([shape(f["geometry"]).buffer(0) for f in cities if f["properties"]["CityName"].upper() == "PHOENIX"])
own["Ahwatukee"] = phx.intersection(box(-112.055, 33.285, -111.955, 33.350))   # approximate Ahwatukee Foothills footprint
own = {a: g for a, g in own.items() if not g.is_empty}
own["San Tan Valley"] = box(-111.605, 33.12, -111.43, 33.245)     # approximate; Pinal County is outside the county GIS layer
claimed = unary_union(list(own.values()))
vor = voronoi_diagram(MultiPoint([sc(p) for p in pts.values()]), envelope=sc(box(-114, 32, -110, 35)))
regions = {}
for cell in vor.geoms:
    a = next(k for k, p in pts.items() if cell.contains(sc(p)))
    cap = unsc(sc(pts[a]).buffer(MAXKM / 111.0))            # ~111 km per degree of latitude
    r = unsc(cell).intersection(land).intersection(cap).difference(claimed)
    regions[a] = r
for a, g in own.items(): regions[a] = regions[a].union(g) if a in regions else g
features = []
for a, region in regions.items():
    if region.is_empty: continue
    s = stats[a]
    features.append(dict(type="Feature", geometry=mapping(region.simplify(0.0004)),
        properties=dict(area=a, color=col[a], avg_high=s["avg_high"], avg_low=s["avg_low"], days_110=s["days_110"], days_100=s["days_100"],
                        rain=s["rain_in"], monsoon=s["monsoon_in"], note=s.get("temp_note",""))))
# incorporated city outlines + labels
by = {}
for f in cities:
    n = f["properties"]["CityName"].title()
    if "Unincorporated" in n: continue
    by.setdefault(n, []).append(shape(f["geometry"]).buffer(0))
outl, labels = [], []
for n, gs in by.items():
    g = unary_union(gs).intersection(BBOX)
    if g.is_empty: continue
    outl.append(dict(type="Feature", properties=dict(name=n), geometry=mapping(g.simplify(0.0004))))
    if n in ("Phoenix","Scottsdale","Tempe","Mesa","Chandler","Gilbert","Glendale","Peoria","Surprise","Goodyear","Avondale","Buckeye","Queen Creek","Apache Junction","Fountain Hills","Cave Creek","Carefree","Paradise Valley","El Mirage","Litchfield Park","Tolleson","Youngtown","Guadalupe","Tolleson"):
        big = max((gg for gg in (g.geoms if hasattr(g, "geoms") else [g])), key=lambda x: x.area)
        p = big.representative_point(); labels.append(dict(name=n, lat=p.y, lon=p.x))
for nm, a in (("Ahwatukee","Ahwatukee"),("San Tan Valley","San Tan Valley"),("Anthem","Anthem/New River")):
    labels.append(dict(name=nm, lat=CENTERS[a][0]-0.012, lon=CENTERS[a][1]))
legend = [dict(area=a, color=col[a], **{k: stats[a][k] for k in ("avg_high","days_110","rain_in")}) for a in areas]
centers = [dict(area=a, lat=CENTERS[a][0], lon=CENTERS[a][1], color=col[a]) for a in areas]
data = dict(regions=dict(type="FeatureCollection", features=features), outlines=dict(type="FeatureCollection", features=outl),
            labels=labels, legend=legend, centers=centers)

# ---- freeways (Maricopa County GIS Highway layer; ramps and interchange pieces left out)
from shapely.ops import linemerge
ROUTES = {  # (HighwayName) -> (label, class)
 "I 10":("I-10","major"),"I 17":("I-17","major"),"SR 101":("Loop 101","major"),"SR 202":("Loop 202","major"),"SR 303":("Loop 303","major"),
 "SR 51":("SR 51","major"),"US 60":("US 60","major"),"SR 143":("SR 143","major"),"SR 87":("SR 87","major"),
 "SR 85":("SR 85","minor"),"SR 74":("SR 74","minor")}
hw = json.load(open("data/highways.geojson"))["features"]
lines = {}
for f in hw:
    p = f["properties"]; r = ROUTES.get(p["HighwayName"])
    if not r or p["HighwayType"] in ("Ramp", "Interchange"): continue
    lines.setdefault(r, []).append(shape(f["geometry"]))
VIEW = box(-112.78, 33.00, -111.30, 34.00)
roads, shields = [], []
for (label, cls), gs in lines.items():
    g = unary_union(gs).intersection(VIEW)
    if g.is_empty: continue
    g = linemerge(g) if g.geom_type == "MultiLineString" else g
    roads.append(dict(type="Feature", properties=dict(route=label, cls=cls), geometry=mapping(g.simplify(0.0003))))
    parts = sorted((g.geoms if hasattr(g, "geoms") else [g]), key=lambda x: -x.length)[:2]
    for part in parts:
        for frac in ((0.3, 0.75) if part is parts[0] else (0.5,)):
            pt = part.interpolate(frac, normalized=True); 
            if -112.68 < pt.x < -111.40 and 33.07 < pt.y < 33.93: shields.append(dict(label=label, cls=cls, lat=pt.y, lon=pt.x))
data["roads"] = dict(type="FeatureCollection", features=roads); data["shields"] = shields
html = open("map_template.html").read().replace("/*DATA*/null", json.dumps(data))
open("map.html", "w").write(html); print("regions", len(features), "outlines", len(outl), "bytes", len(html))

import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
P = lambda g: [p for p in (g.geoms if hasattr(g, "geoms") else [g]) if p.geom_type == "Polygon"]
Ls = lambda g: [p for p in (g.geoms if hasattr(g, "geoms") else [g]) if p.geom_type == "LineString"]
fig, ax = plt.subplots(figsize=(12.5, 8.4))
for f in data["regions"]["features"]:
    for p in P(shape(f["geometry"])): x, y = p.exterior.xy; ax.fill(x, y, color=f["properties"]["color"], alpha=.6, lw=0)
for f in data["outlines"]["features"]:
    for p in P(shape(f["geometry"])): x, y = p.exterior.xy; ax.plot(x, y, color="#333", lw=.4, alpha=.4)
for f in data["roads"]["features"]:
    for l in Ls(shape(f["geometry"])):
        x, y = l.xy; ax.plot(x, y, color="#fff", lw=4.5); ax.plot(x, y, color="#2b2f3a" if f["properties"]["cls"] == "major" else "#5b6170", lw=2)
for s_ in data["shields"]: ax.text(s_["lon"], s_["lat"], s_["label"], fontsize=6.5, color="w", ha="center", va="center", bbox=dict(boxstyle="round,pad=.2", fc="#2b2f3a", ec="w"))
for l in data["labels"]: ax.text(l["lon"], l["lat"] + .012, l["name"], fontsize=6.5, ha="center", color="#333")
for c in data["centers"]: ax.plot(c["lon"], c["lat"], "o", mfc=c["color"], mec="w", ms=7)
ax.set_aspect(1/0.835); ax.set_xlim(-112.7, -111.4); ax.set_ylim(33.05, 33.95); ax.axis("off")
ax.legend(handles=[plt.Line2D([0],[0],marker="s",ls="",color=x["color"],label=x["area"],ms=9) for x in data["legend"]],
          loc="center left", bbox_to_anchor=(1.0, .5), fontsize=8, frameon=False, title="Report areas")
plt.tight_layout(); plt.savefig("map_preview.png", dpi=100, bbox_inches="tight")
