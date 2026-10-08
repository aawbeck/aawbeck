# Area -> (temperature station, rain stations). GHCN-Daily IDs.
# Rain uses the nearest long-record gauges (NWS co-op + CoCoRaHS volunteer gauges, averaged).
AREAS = {
 "Central Phoenix":  ("USW00023183", ["USW00023183","US1AZMR0198","US1AZMR0410","US1AZMR0343"]),
 "North Phoenix":    ("USW00003184", ["USW00003184","US1AZMR0220","US1AZMR0443","US1AZMR0078"]),
 "Scottsdale":       ("USW00003192", ["USW00003192","US1AZMR0110","US1AZMR0113","US1AZMR0207"]),
 "North Scottsdale": ("USC00026603", ["USC00026603","US1AZMR0045","US1AZMR0232","US1AZMR0265"]),
 "Tempe":            ("USC00028499", ["USC00028499","US1AZMR0267","US1AZMR0347","US1AZMR0032"]),
 "Mesa (East)":      ("USC00022782", ["USC00022782","US1AZMR0153","US1AZMR0213","US1AZMR0373"]),
 "Gilbert": (["CHD_AP","IWA_AP"], ["US1AZMR0280","US1AZMR0392","US1AZMR0339","US1AZMR0338"]),
 "Chandler": ("CHD_AP", ["US1AZMR0197","US1AZMR0278","US1AZMR0290","US1AZMR0458","US1AZMR0157"]),
 "Fountain Hills":   ("USC00023190", ["USC00023190","US1AZMR0022","US1AZMR0319"]),
 "Carefree/Cave Creek": ("USC00021282", ["USC00021282","US1AZMR0017","US1AZMR0163"]),
 "West Valley (Glendale/Peoria)": ("GEU_AP", ["US1AZMR0046","US1AZMR0226","US1AZMR0379","USC00029634"]),
 "Surprise/Sun City": ("USC00029634", ["US1AZMR0042","US1AZMR0026","US1AZMR0103","US1AZMR0287"]),
 "Ahwatukee":        (["USW00023183","CHD_AP"], ["US1AZMR0382"]),
 "Queen Creek":      ("IWA_AP", []),
 "San Tan Valley":   ("IWA_AP", ["US1AZPN0064","US1AZPN0065"]),
 "Goodyear":         ("GYR_AP", ["US1AZMR0245","US1AZMR0411"]),
 "Avondale/Litchfield Park": ("GYR_AP", ["USC00024977","US1AZMR0035","US1AZMR0412","US1AZMR0402","USC00028598"]),
 "Buckeye":          ("BXK_AP", []),
 "Anthem/New River": ("USW00003184", ["US1AZMR0322","US1AZMR0289"]),
 "Apache Junction":  ("USC00020288", ["USC00020288","US1AZPN0020","US1AZPN0035"]),
}

# Notes shown in outputs where the temperature source is not an in-area, full-record station.
# Airport temperatures are daily highs/lows from the Iowa Mesonet (close to official records; 110F+ day counts run ~10-15% low).
TEMP_PROXY = {
 "Gilbert": "Average of Chandler Municipal and Williams Gateway airports (Gilbert sits between them)",
 "Chandler": "Chandler Municipal Airport",
 "West Valley (Glendale/Peoria)": "Glendale Municipal Airport",
 "Surprise/Sun City": "Youngtown station (Sun City area)",
 "Ahwatukee": "Average of Sky Harbor and Chandler Municipal airports; foothills may run a bit cooler at night",
 "Queen Creek": "Williams Gateway Airport (~4 mi); same source as San Tan Valley",
 "San Tan Valley": "Williams Gateway Airport (~8 mi); same source as Queen Creek",
 "Goodyear": "Phoenix Goodyear Airport; same source as Avondale/Litchfield Park",
 "Avondale/Litchfield Park": "Phoenix Goodyear Airport (~5 mi); same source as Goodyear",
 "Buckeye": "Buckeye Municipal Airport",
 "Anthem/New River": "Deer Valley Airport (~12 mi, similar elevation); same source as North Phoenix",
}
