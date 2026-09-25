import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ------------------------------------------------------------
# GoG-WaveSpec: Representative Offshore Case-Study Locations
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
# 1. Representative offshore locations
#
# These are case-study locations, NOT optimized deployment
# sites.
# ------------------------------------------------------------

locations = {
    "Cote d'Ivoire offshore": {
        "latitude": 4.5,
        "longitude": -4.0,
    },
    "Ghana offshore": {
        "latitude": 4.5,
        "longitude": -1.0,
    },
    "Lagos offshore": {
        "latitude": 5.0,
        "longitude": 3.4,
    },
}

# ------------------------------------------------------------
# 2. Open ERA5 dataset
# ------------------------------------------------------------

ds = xr.open_dataset(DATA_FILE)

rows = []

# ------------------------------------------------------------
# 3. Extract nearest ERA5 grid cell for each location
# ------------------------------------------------------------

for name, coordinates in locations.items():

    point = ds.sel(
        latitude=coordinates["latitude"],
        longitude=coordinates["longitude"],
        method="nearest",
    )

    hs = point["swh"]
    tm = point["mwp"]

    # --------------------------------------------------------
    # Calculate WPD for every observation BEFORE averaging
    #
    # P = rho * g^2 * Hs^2 * Tm / (64*pi)
    #
    # Result converted from W/m to kW/m.
    # --------------------------------------------------------

    wpd = (
        RHO * G**2 * hs**2 * tm
        / (64.0 * np.pi)
    ) / 1000.0

    actual_lat = float(
        point["latitude"].values
    )

    actual_lon = float(
        point["longitude"].values
    )

    mean_hs = float(
        hs.mean(skipna=True).values
    )

    mean_tm = float(
        tm.mean(skipna=True).values
    )

    mean_wpd = float(
        wpd.mean(skipna=True).values
    )

    rows.append(
        {
            "Location": name,
            "Nominal_Latitude": coordinates["latitude"],
            "Nominal_Longitude": coordinates["longitude"],
            "ERA5_Latitude": actual_lat,
            "ERA5_Longitude": actual_lon,
            "Mean_Hs_m": mean_hs,
            "Mean_Tm_s": mean_tm,
            "Mean_WPD_kW_per_m": mean_wpd,
        }
    )

# ------------------------------------------------------------
# 4. Create results table
# ------------------------------------------------------------

results = pd.DataFrame(rows)

results_rounded = results.copy()

numeric_columns = [
    "Nominal_Latitude",
    "Nominal_Longitude",
    "ERA5_Latitude",
    "ERA5_Longitude",
    "Mean_Hs_m",
    "Mean_Tm_s",
    "Mean_WPD_kW_per_m",
]

for column in numeric_columns:
    results_rounded[column] = (
        results_rounded[column].round(4)
    )

# ------------------------------------------------------------
# 5. Print results
# ------------------------------------------------------------

print(
    "\nGoG-WaveSpec — Representative Offshore Locations"
)

print(
    "------------------------------------------------"
)

print(
    results_rounded.to_string(index=False)
)

# ------------------------------------------------------------
# 6. Save numerical table
# ------------------------------------------------------------

table_file = (
    TABLE_DIR / "case_study_statistics.csv"
)

results_rounded.to_csv(
    table_file,
    index=False
)

# ------------------------------------------------------------
# 7. Generate representative-location map
# ------------------------------------------------------------

# Calculate spatial mean WPD for the background map.
# WPD is calculated at each observation before averaging.

hs_domain = ds["swh"]
tm_domain = ds["mwp"]

wpd_domain = (
    RHO * G**2 * hs_domain**2 * tm_domain
    / (64.0 * np.pi)
) / 1000.0

mean_wpd_domain = wpd_domain.mean(
    dim="valid_time",
    skipna=True
)

fig, ax = plt.subplots(
    figsize=(10, 7)
)

mesh = ax.pcolormesh(
    mean_wpd_domain["longitude"],
    mean_wpd_domain["latitude"],
    mean_wpd_domain,
    shading="auto",
)

colorbar = fig.colorbar(
    mesh,
    ax=ax,
)

colorbar.set_label(
    "Mean Wave Power Density (kW/m)"
)

# ------------------------------------------------------------
# Plot and label the three selected ERA5 grid cells
# ------------------------------------------------------------

for _, row in results.iterrows():

    ax.scatter(
        row["ERA5_Longitude"],
        row["ERA5_Latitude"],
        marker="o",
        s=65,
        edgecolors="black",
        linewidths=0.8,
    )

    label = (
        f'{row["Location"]}\n'
        f'{row["Mean_WPD_kW_per_m"]:.2f} kW/m'
    )

    ax.annotate(
        label,
        (
            row["ERA5_Longitude"],
            row["ERA5_Latitude"],
        ),
        xytext=(7, 7),
        textcoords="offset points",
        fontsize=8,
    )

ax.set_xlabel("Longitude (°)")
ax.set_ylabel("Latitude (°)")

ax.set_title(
    "Representative Offshore Case-Study Locations\n"
    "Gulf of Guinea Analysis Domain (ERA5, 2014–2025)"
)

ax.grid(
    True,
    alpha=0.25,
)

fig.tight_layout()

figure_file = (
    FIGURE_DIR / "case_study_locations.png"
)

fig.savefig(
    figure_file,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)

# ------------------------------------------------------------
# 8. Confirmation
# ------------------------------------------------------------

print(
    f"\nCase-study table saved to:\n{table_file}"
)

print(
    f"\nCase-study figure saved to:\n{figure_file}"
)

ds.close()