# Map of the Valley: each point of land is shaded with the color of the nearest report area (same colors/order as report.html).
import json, math
from shapely.geometry import shape, mapping, Point, box
from shapely.ops import unary_union, voronoi_diagram
from fcd_gauges import CENTERS
D = json.load(open("data/report_data.json"))
PAL = ["#1f77b4","#d62728","#2ca02c","#ff7f0e","#9467bd","#8c564b","#e377c2","#17becf","#7f7f7f","#bcbd22","#393b79","#ad494a","#637939","#00a6a6","#e6ab02","#4d4d4d"]
areas = [r["area"] for r in D["summary"]]; col = {a: PAL[i] for i, a in enumerate(areas)}; stats = {r["area"]: r for r in D["summary"]}
K = math.cos(math.radians(33.5))                       # lon scaling so "nearest" is roughly Euclidean
fwd = lambda x, y: (x * K, y)
from shapely.affinity import scale
BBOX = box(-112.62, 33.12, -111.38, 33.97)
cities = json.load(open("data/cities.geojson"))["features"]
land = unary_union([shape(f["geometry"]).buffer(0) for f in cities]).intersection(BBOX)
pts = {a: Point(lo, la) for a, (la, lo) in CENTERS.items()}
sc = lambda g: scale(g, xfact=K, yfact=1, origin=(0, 0))
unsc = lambda g: scale(g, xfact=1/K, yfact=1, origin=(0, 0))
from shapely.geometry import MultiPoint
# Areas that are a single city (or two) use the real city boundary; everything else is split by nearest area center.
CITY_AREA = {"GILBERT":"Gilbert","CHANDLER":"Chandler","TEMPE":"Tempe","FOUNTAIN HILLS":"Fountain Hills","APACHE JUNCTION":"Apache Junction",
             "CAREFREE":"Carefree/Cave Creek","CAVE CREEK":"Carefree/Cave Creek","GLENDALE":"West Valley (Glendale/Peoria)",
             "PEORIA":"West Valley (Glendale/Peoria)","SURPRISE":"Surprise/Sun City"}
MAXKM = 15                                    # beyond this distance from an area's center, land is left unshaded
own = {}
for f in cities:
    a = CITY_AREA.get(f["properties"]["CityName"].upper())
    if a: own.setdefault(a, []).append(shape(f["geometry"]).buffer(0))
own = {a: unary_union(g).intersection(BBOX) for a, g in own.items()}
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
    if n in ("Phoenix","Scottsdale","Tempe","Mesa","Chandler","Gilbert","Glendale","Peoria","Surprise","Goodyear","Avondale","Buckeye","Queen Creek","Apache Junction","Fountain Hills","Cave Creek","Carefree","Paradise Valley","El Mirage","Litchfield Park","Tolleson","Youngtown","Guadalupe"):
        big = max((gg for gg in (g.geoms if hasattr(g, "geoms") else [g])), key=lambda x: x.area)
        p = big.representative_point(); labels.append(dict(name=n, lat=p.y, lon=p.x))
legend = [dict(area=a, color=col[a], **{k: stats[a][k] for k in ("avg_high","days_110","rain_in")}) for a in areas]
centers = [dict(area=a, lat=CENTERS[a][0], lon=CENTERS[a][1], color=col[a]) for a in areas]
data = dict(regions=dict(type="FeatureCollection", features=features), outlines=dict(type="FeatureCollection", features=outl),
            labels=labels, legend=legend, centers=centers)
html = open("map_template.html").read().replace("/*DATA*/null", json.dumps(data))
open("map.html", "w").write(html); print("regions", len(features), "outlines", len(outl), "bytes", len(html))
