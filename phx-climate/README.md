# Phoenix Metro climate, 2016-2025

Run order: `fetch_noaa.py` -> `fetch_iem.py` -> `fetch_fcd.py` -> `analyze.py` -> `fcd_analyze.py` -> `build_report.py` -> `build_map.py` -> `build_report.py` (again, to embed the map preview); open `report.html` and `map.html`.
`colors.py` fixes each area's color; `data/cities.geojson` and `data/highways.geojson` come from Maricopa County GIS (gis.maricopa.gov).
Several areas share or average nearby airport stations for temperature (see the notes column in the report); Ahwatukee and San Tan Valley outlines on the map are approximate.
(`fetch_fcd.py` needs `/tmp/fcd/meta/sensors.xlsx` from https://alert.fcd.maricopa.gov/alert/Meta/ALERT_sensors_all_by_name.xlsx and the 2025 zip it downloads itself.)

- **Rain (primary)**: Flood Control District of Maricopa County (FCDMC) automated gauges, the 2-6 nearest each area (`fcd_gauges.py`), calendar years 2016-2025. Water years 2016-2024 come from the per-gauge official precipitation workbooks (rows outside each sheet's water year are discarded because some sheets in that archive are stale copies); 2025 on comes from `pcp_WY_2025/2026.xlsx`.
- **Rain (cross-check)**: NOAA GHCN-Daily co-op + CoCoRaHS volunteer gauges; these read ~6-30% wetter than the county gauges in most areas.
- **Temperature**: NOAA GHCN-Daily stations where a long-record station exists; otherwise daily highs/lows from airport observations via the Iowa Environmental Mesonet (`fetch_iem.py`: Chandler, Williams Gateway, Phoenix Goodyear, Buckeye, Glendale). Checked against official records at Sky Harbor, Deer Valley, Scottsdale and Gateway: highs within ~0.5F on average, 110F+ day counts ~10-15% low. Some areas share or average a nearby station (see the notes column in the report).
- `fetch_openmeteo.py` (modeled grid data) was used only to cross-check; it runs 2-4F cool on highs and is not used in the results.
