#!/bin/sh
# Public WMAP 9-yr products from NASA LAMBDA (used by doc 71, ring test).
cd "$(dirname "$0")"
curl -fLO https://lambda.gsfc.nasa.gov/data/map/dr5/dfp/ilc/wmap_ilc_9yr_v5.fits
curl -fLO https://lambda.gsfc.nasa.gov/data/map/dr5/ancillary/masks/wmap_temperature_kq85_analysis_mask_r9_9yr_v5.fits
sha256sum -c SHA256SUMS
