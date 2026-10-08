# Phoenix Metro climate, 2016-2025

Run order: `fetch_noaa.py` -> `fetch_isd.py` -> `fetch_fcd.py` -> `analyze.py` -> `fcd_analyze.py` -> `build_report.py`; open `report.html`.
(`fetch_fcd.py` needs `/tmp/fcd/meta/sensors.xlsx` from https://alert.fcd.maricopa.gov/alert/Meta/ALERT_sensors_all_by_name.xlsx and the 2025 zip it downloads itself.)

- **Rain (primary)**: Flood Control District of Maricopa County (FCDMC) automated gauges, the 2-6 nearest each area (`fcd_gauges.py`), calendar years 2016-2025. Water years 2016-2024 come from the per-gauge official precipitation workbooks (rows outside each sheet's water year are discarded because some sheets in that archive are stale copies); 2025 on comes from `pcp_WY_2025/2026.xlsx`.
- **Rain (cross-check)**: NOAA GHCN-Daily co-op + CoCoRaHS volunteer gauges; these read ~6-30% wetter than the county gauges in most areas.
- **Temperature**: NOAA GHCN-Daily stations; Gilbert (Williams Gateway) and Chandler (Chandler Muni) are derived from hourly airport observations (`fetch_isd.py`), so 110F+ day counts there are biased low (about 1/3 vs. official daily highs in 2025).
- `fetch_openmeteo.py` (modeled grid data) was used only to cross-check; it runs 2-4F cool on highs and is not used in the results.
