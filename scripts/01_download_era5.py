import cdsapi
from pathlib import Path

# ------------------------------------------------------------
# GoG-WaveSpec: ERA5 Data Acquisition
# Gulf of Guinea analysis domain, 2014–2025
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

DATA_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = DATA_DIR / "gog_2014_2025.nc"

# ------------------------------------------------------------
# ERA5 request configuration
#
# Analysis domain:
# North: 10°N
# West : 5°W
# South: 5°S
# East : 10°E
#
# One observation per day at 12:00 UTC.
# ------------------------------------------------------------

dataset = "reanalysis-era5-single-levels"

request = {
    "product_type": ["reanalysis"],
    "variable": [
        "significant_height_of_combined_wind_waves_and_swell",
        "mean_wave_period",
        "mean_wave_direction",
    ],
    "year": [
        str(year)
        for year in range(2014, 2026)
    ],
    "month": [
        f"{month:02d}"
        for month in range(1, 13)
    ],
    "day": [
        f"{day:02d}"
        for day in range(1, 32)
    ],
    "time": ["12:00"],
    "data_format": "netcdf",
    "download_format": "unarchived",
    "area": [
        10,     # North
        -5,     # West
        -5,     # South
        10,     # East
    ],
}

# ------------------------------------------------------------
# Download dataset
# ------------------------------------------------------------

print("GoG-WaveSpec — ERA5 Data Acquisition")
print("------------------------------------")
print("Dataset: ERA5 single levels")
print("Period: 2014–2025")
print("Time: 12:00 UTC daily")
print("Domain: 10°N–5°S, 5°W–10°E")
print(f"\nOutput file:\n{OUTPUT_FILE}")
print("\nSubmitting request to Copernicus CDS...")

client = cdsapi.Client()

client.retrieve(
    dataset,
    request,
    str(OUTPUT_FILE),
)

print("\nDownload complete.")