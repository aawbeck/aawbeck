# Area -> (temperature station, rain stations). GHCN-Daily IDs.
# Rain uses the nearest long-record gauges (NWS co-op + CoCoRaHS volunteer gauges, averaged).
AREAS = {
 "Central Phoenix":  ("USW00023183", ["USW00023183","US1AZMR0198","US1AZMR0410","US1AZMR0343"]),
 "North Phoenix":    ("USW00003184", ["USW00003184","US1AZMR0220","US1AZMR0443","US1AZMR0078"]),
 "Scottsdale":       ("USW00003192", ["USW00003192","US1AZMR0110","US1AZMR0113","US1AZMR0207"]),
 "North Scottsdale": ("USC00026603", ["USC00026603","US1AZMR0045","US1AZMR0232","US1AZMR0265"]),
 "Tempe":            ("USC00028499", ["USC00028499","US1AZMR0267","US1AZMR0347","US1AZMR0032"]),
 "Mesa (East)":      ("USC00022782", ["USC00022782","US1AZMR0153","US1AZMR0213","US1AZMR0373"]),
 "Gilbert/Chandler": ("USC00022782", ["US1AZMR0280","US1AZMR0392","US1AZMR0197","US1AZMR0278"]),
 "Fountain Hills":   ("USC00023190", ["USC00023190","US1AZMR0022","US1AZMR0319"]),
 "Carefree/Cave Creek": ("USC00021282", ["USC00021282","US1AZMR0017","US1AZMR0163"]),
 "West Valley (Glendale/Peoria)": ("USC00029634", ["US1AZMR0046","US1AZMR0226","US1AZMR0379","USC00029634"]),
 "Surprise/Sun City": ("USC00029634", ["US1AZMR0042","US1AZMR0026","US1AZMR0103","US1AZMR0287"]),
 "Goodyear/Litchfield": ("USC00024977", ["USC00024977","US1AZMR0035","US1AZMR0245","USC00028598"]),
 "Apache Junction":  ("USC00020288", ["USC00020288","US1AZPN0020","US1AZPN0035"]),
}

# Areas whose temperature comes from a nearby (not in-area) station -> shown as "proxy" in outputs.
TEMP_PROXY = {
 "Gilbert/Chandler": "East Mesa station (no long-record Gilbert/Chandler station)",
 "West Valley (Glendale/Peoria)": "Youngtown station (Sun City area)",
 "Goodyear/Litchfield": "Litchfield Park station; record ends 2021",
 "Surprise/Sun City": "Youngtown station",
 "North Phoenix": None, "Mesa (East)": None,
}
