import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ------------------------------------------------------------
# GoG-WaveSpec: Seasonal Wave Resource Climatology
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
# 1. Open dataset
# ------------------------------------------------------------

ds = xr.open_dataset(DATA_FILE)

hs = ds["swh"]
tm = ds["mwp"]

# ------------------------------------------------------------
# 2. Calculate WPD for each observation BEFORE averaging
#
# P = rho * g^2 * Hs^2 * Tm / (64*pi)
#
# Result converted from W/m to kW/m.
# ------------------------------------------------------------

wpd = (
    RHO * G**2 * hs**2 * tm
    / (64.0 * np.pi)
) / 1000.0

# ------------------------------------------------------------
# 3. Define climatological seasons
# ------------------------------------------------------------

seasons = {
    "DJF": [12, 1, 2],
    "MAM": [3, 4, 5],
    "JJA": [6, 7, 8],
    "SON": [9, 10, 11],
}

rows = []

for season, months in seasons.items():

    mask = ds["valid_time"].dt.month.isin(months)

    season_hs = hs.where(mask, drop=True)
    season_tm = tm.where(mask, drop=True)
    season_wpd = wpd.where(mask, drop=True)

    rows.append(
        {
            "Season": season,
            "Mean_Hs_m": float(
                season_hs.mean(skipna=True).values
            ),
            "Mean_Tm_s": float(
                season_tm.mean(skipna=True).values
            ),
            "Mean_WPD_kW_per_m": float(
                season_wpd.mean(skipna=True).values
            ),
        }
    )

results = pd.DataFrame(rows)

# ------------------------------------------------------------
# 4. Round exported/displayed values
#
# Calculations above retain full precision.
# ------------------------------------------------------------

results_rounded = results.copy()

results_rounded["Mean_Hs_m"] = (
    results_rounded["Mean_Hs_m"].round(4)
)

results_rounded["Mean_Tm_s"] = (
    results_rounded["Mean_Tm_s"].round(4)
)

results_rounded["Mean_WPD_kW_per_m"] = (
    results_rounded["Mean_WPD_kW_per_m"].round(4)
)

# ------------------------------------------------------------
# 5. Print results
# ------------------------------------------------------------

print("\nGoG-WaveSpec — Seasonal Climatology")
print("-----------------------------------")
print(results_rounded.to_string(index=False))

# ------------------------------------------------------------
# 6. Save numerical results
# ------------------------------------------------------------

table_file = TABLE_DIR / "seasonal_climatology.csv"

results_rounded.to_csv(
    table_file,
    index=False
)

# ------------------------------------------------------------
# 7. Generate seasonal figure
# ------------------------------------------------------------

x = np.arange(len(results))

fig, axes = plt.subplots(
    3,
    1,
    figsize=(8, 10),
    sharex=True
)

# Significant wave height
axes[0].plot(
    x,
    results["Mean_Hs_m"],
    marker="o",
    linewidth=1.8
)

axes[0].set_ylabel("Hs (m)")
axes[0].set_title(
    "(a) Seasonal Mean Significant Wave Height"
)
axes[0].grid(True, alpha=0.3)

# Mean wave period
axes[1].plot(
    x,
    results["Mean_Tm_s"],
    marker="o",
    linewidth=1.8
)

axes[1].set_ylabel("Tm (s)")
axes[1].set_title(
    "(b) Seasonal Mean Wave Period"
)
axes[1].grid(True, alpha=0.3)

# Wave power density
axes[2].plot(
    x,
    results["Mean_WPD_kW_per_m"],
    marker="o",
    linewidth=1.8
)

axes[2].set_ylabel("WPD (kW/m)")
axes[2].set_xlabel("Season")
axes[2].set_title(
    "(c) Seasonal Mean Wave Power Density"
)
axes[2].grid(True, alpha=0.3)

axes[2].set_xticks(x)
axes[2].set_xticklabels(results["Season"])

fig.suptitle(
    "Seasonal Climatology of the Gulf of Guinea Wave Resource\n"
    "(ERA5, 2014–2025)",
    fontsize=13
)

fig.tight_layout(
    rect=[0, 0, 1, 0.96]
)

figure_file = (
    FIGURE_DIR / "seasonal_climatology.png"
)

fig.savefig(
    figure_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)

# ------------------------------------------------------------
# 8. Confirmation
# ------------------------------------------------------------

print(
    f"\nSeasonal table saved to:\n{table_file}"
)

print(
    f"\nSeasonal figure saved to:\n{figure_file}"
)

ds.close()