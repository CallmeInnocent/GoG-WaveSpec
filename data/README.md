# Data

This directory is used for the ERA5 wave reanalysis dataset analysed in the GoG-WaveSpec study.

## Dataset

The analysis uses ERA5 single-level reanalysis data obtained from the Copernicus Climate Data Store (CDS).

The following wave variables are requested:

- Significant height of combined wind waves and swell (`swh`)
- Mean wave period (`mwp`)
- Mean wave direction (`mwd`)

## Temporal coverage

The dataset covers:

- 1 January 2014 to 31 December 2025
- Daily observations
- 12:00 UTC

This corresponds to 12 complete calendar years of ERA5 data.

## Analysis domain

The rectangular analysis domain is bounded by:

- North: 10°N
- South: 5°S
- West: 5°W
- East: 10°E

This domain is used as the Gulf of Guinea analysis region for the study and should not be interpreted as a formal geographic definition of the entire Gulf of Guinea.

## Data acquisition

The dataset can be reproduced using:

`../scripts/01_download_era5.py`

The script requires access to the Copernicus Climate Data Store API and the Python `cdsapi` package.

After successful acquisition, the expected local file is:

`gog_2014_2025.nc`

The analysis scripts in the repository expect this file to be located inside this `data` directory.

## Raw-data availability

The raw NetCDF dataset is intentionally not version-controlled in this repository.

Instead, the acquisition script provides the configuration required to retrieve the source data from the Copernicus Climate Data Store.

Users must comply with the applicable Copernicus/ECMWF data-access terms when retrieving and using ERA5 data.

## Important methodological note

Wave power density is not supplied directly by the dataset.

For the GoG-WaveSpec analysis, wave power density is calculated for each valid observation using significant wave height and mean wave period before any temporal averaging is performed.

The calculation methodology is documented in the analysis scripts and accompanying technical report.