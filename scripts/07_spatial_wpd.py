import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ------------------------------------------------------------
# GoG-WaveSpec: Spatial Mean Wave Power Density
# ERA5 Gulf of Guinea, 2014–2025
# ------------------------------------------------------------

# Repository root determined from this script
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# ERA5 dataset stored locally in the repository data directory
DATA_FILE = PROJECT_ROOT / "data" / "gog_2014_2025.nc"

# Repository output directories
TABLE_DIR = PROJECT_ROOT / "outputs" / "tables"
FIGURE_DIR = PROJECT_ROOT / "outputs" / "figures"

TABLE_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# Physical constants
RHO = 1025.0
G = 9.81

# ------------------------------------------------------------
# 1. Open ERA5 dataset
# ------------------------------------------------------------

ds = xr.open_dataset(DATA_FILE)

hs = ds["swh"]
tm = ds["mwp"]

# ------------------------------------------------------------
# 2. Calculate WPD at EACH observation
#
# P = rho * g^2 * Hs^2 * Tm / (64*pi)
#
# IMPORTANT:
# WPD is calculated before temporal averaging.
# Result converted from W/m to kW/m.
# ------------------------------------------------------------

wpd = (
    RHO * G**2 * hs**2 * tm
    / (64.0 * np.pi)
) / 1000.0

# ------------------------------------------------------------
# 3. Calculate long-term mean WPD at every grid cell
# ------------------------------------------------------------

mean_wpd = wpd.mean(
    dim="valid_time",
    skipna=True
)

# ------------------------------------------------------------
# 4. Export spatial WPD grid
# ------------------------------------------------------------

spatial_df = (
    mean_wpd
    .to_dataframe(name="Mean_WPD_kW_per_m")
    .reset_index()
)

spatial_df["Mean_WPD_kW_per_m"] = (
    spatial_df["Mean_WPD_kW_per_m"].round(4)
)

table_file = (
    TABLE_DIR / "spatial_mean_wpd.csv"
)

spatial_df.to_csv(
    table_file,
    index=False
)

# ------------------------------------------------------------
# 5. Report spatial range
# ------------------------------------------------------------

minimum_wpd = float(
    mean_wpd.min(skipna=True).values
)

maximum_wpd = float(
    mean_wpd.max(skipna=True).values
)

# Find grid cells containing min and max
min_index = np.unravel_index(
    np.nanargmin(mean_wpd.values),
    mean_wpd.shape
)

max_index = np.unravel_index(
    np.nanargmax(mean_wpd.values),
    mean_wpd.shape
)

min_lat = float(
    mean_wpd["latitude"].values[min_index[0]]
)

min_lon = float(
    mean_wpd["longitude"].values[min_index[1]]
)

max_lat = float(
    mean_wpd["latitude"].values[max_index[0]]
)

max_lon = float(
    mean_wpd["longitude"].values[max_index[1]]
)

print("\nGoG-WaveSpec — Spatial Mean WPD")
print("--------------------------------")

print(
    f"Minimum grid-cell mean WPD: "
    f"{minimum_wpd:.4f} kW/m"
)

print(
    f"Minimum location: "
    f"{min_lat:.2f}°, {min_lon:.2f}°"
)

print(
    f"\nMaximum grid-cell mean WPD: "
    f"{maximum_wpd:.4f} kW/m"
)

print(
    f"Maximum location: "
    f"{max_lat:.2f}°, {max_lon:.2f}°"
)

# ------------------------------------------------------------
# 6. Generate corrected spatial WPD map
# ------------------------------------------------------------

fig, ax = plt.subplots(
    figsize=(10, 7)
)

mesh = ax.pcolormesh(
    mean_wpd["longitude"],
    mean_wpd["latitude"],
    mean_wpd,
    shading="auto"
)

colorbar = fig.colorbar(
    mesh,
    ax=ax
)

colorbar.set_label(
    "Mean Wave Power Density (kW/m)"
)

ax.set_xlabel("Longitude (°)")
ax.set_ylabel("Latitude (°)")

ax.set_title(
    "Long-Term Mean Wave Power Density\n"
    "Gulf of Guinea Analysis Domain "
    "(ERA5, 2014–2025)"
)

ax.grid(
    True,
    alpha=0.25
)

fig.tight_layout()

figure_file = (
    FIGURE_DIR / "spatial_mean_wpd.png"
)

fig.savefig(
    figure_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)

# ------------------------------------------------------------
# 7. Confirmation
# ------------------------------------------------------------

print(
    f"\nSpatial WPD table saved to:\n{table_file}"
)

print(
    f"\nSpatial WPD figure saved to:\n{figure_file}"
)

ds.close()