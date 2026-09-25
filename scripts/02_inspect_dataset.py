import xarray as xr
from pathlib import Path

# ------------------------------------------------------------
# GoG-WaveSpec: ERA5 Dataset Inspection
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "gog_2014_2025.nc"

# ------------------------------------------------------------
# 1. Open dataset
# ------------------------------------------------------------

ds = xr.open_dataset(DATA_FILE)

print("\nGoG-WaveSpec — ERA5 Dataset Inspection")
print("---------------------------------------")

# ------------------------------------------------------------
# 2. Display dataset structure
# ------------------------------------------------------------

print("\nDataset structure:")
print(ds)

# ------------------------------------------------------------
# 3. Report key dimensions
# ------------------------------------------------------------

print("\nKey dimensions:")
print(f"Time steps: {ds.sizes['valid_time']:,}")
print(f"Latitude points: {ds.sizes['latitude']}")
print(f"Longitude points: {ds.sizes['longitude']}")

# ------------------------------------------------------------
# 4. Report temporal coverage
# ------------------------------------------------------------

start_time = ds["valid_time"].values[0]
end_time = ds["valid_time"].values[-1]

print("\nTemporal coverage:")
print(f"Start: {start_time}")
print(f"End:   {end_time}")

# ------------------------------------------------------------
# 5. Report spatial coverage
# ------------------------------------------------------------

latitudes = ds["latitude"].values
longitudes = ds["longitude"].values

print("\nSpatial coverage:")
print(f"Latitude:  {latitudes.min():.2f}° to {latitudes.max():.2f}°")
print(f"Longitude: {longitudes.min():.2f}° to {longitudes.max():.2f}°")

# ------------------------------------------------------------
# 6. Confirm required variables
# ------------------------------------------------------------

required_variables = [
    "swh",
    "mwp",
    "mwd",
]

print("\nRequired variables:")

for variable in required_variables:
    if variable in ds:
        print(f"[OK] {variable}")
    else:
        print(f"[MISSING] {variable}")

ds.close()