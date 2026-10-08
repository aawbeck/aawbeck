# Phoenix Metro climate, 2016-2025

Run order: `fetch_noaa.py` -> `fetch_isd.py` -> `analyze.py` -> `build_report.py`; open `report.html`.

- **Rain**: average of NWS co-op + CoCoRaHS gauges near each area (NOAA GHCN-Daily), station-years with 330+ reporting days only.
- **Temperature**: NOAA GHCN-Daily stations; Gilbert (Williams Gateway) and Chandler (Chandler Muni) are derived from hourly airport observations (`fetch_isd.py`), so 110F+ day counts there are biased low (about 1/3 vs. official daily highs in 2025).
- `fetch_openmeteo.py` (modeled grid data) was used only to cross-check; it runs 2-4F cool on highs and is not used in the results.
- Not yet included: Maricopa County Flood Control gauges (www.maricopa.gov / alert.fcd.maricopa.gov are blocked in this environment).
