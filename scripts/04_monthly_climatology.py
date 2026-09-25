import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ------------------------------------------------------------
# GoG-WaveSpec: Monthly Wave Resource Climatology
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
RHO = 1025.0       # seawater density, kg/m^3
G = 9.81           # gravitational acceleration, m/s^2

# ------------------------------------------------------------
# 1. Open ERA5 dataset
# ------------------------------------------------------------

ds = xr.open_dataset(DATA_FILE)

hs = ds["swh"]     # significant wave height, m
tm = ds["mwp"]     # mean wave period, s

# ------------------------------------------------------------
# 2. Calculate WPD for each observation BEFORE averaging
#
# P = rho * g^2 * Hs^2 * Tm / (64*pi)
#
# Convert W/m to kW/m.
# ------------------------------------------------------------

wpd = (
    RHO * G**2 * hs**2 * tm
    / (64.0 * np.pi)
) / 1000.0

# ------------------------------------------------------------
# 3. Calculate monthly climatology
#
# All January observations from 2014–2025 are grouped
# together, then February, March, etc.
# ------------------------------------------------------------

monthly_hs = hs.groupby("valid_time.month").mean(
    dim=["valid_time", "latitude", "longitude"],
    skipna=True
)

monthly_tm = tm.groupby("valid_time.month").mean(
    dim=["valid_time", "latitude", "longitude"],
    skipna=True
)

monthly_wpd = wpd.groupby("valid_time.month").mean(
    dim=["valid_time", "latitude", "longitude"],
    skipna=True
)

# ------------------------------------------------------------
# 4. Create numerical monthly table
# ------------------------------------------------------------

month_names = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

results = pd.DataFrame(
    {
        "Month": month_names,
        "Mean_Hs_m": monthly_hs.values,
        "Mean_Tm_s": monthly_tm.values,
        "Mean_WPD_kW_per_m": monthly_wpd.values,
    }
)

# Round only the exported/displayed values.
# Calculations above retain full precision.
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

print("\nGoG-WaveSpec — Monthly Climatology")
print("----------------------------------")
print(results_rounded.to_string(index=False))

# ------------------------------------------------------------
# 6. Save numerical results
# ------------------------------------------------------------

table_file = TABLE_DIR / "monthly_climatology.csv"

results_rounded.to_csv(
    table_file,
    index=False
)

# ------------------------------------------------------------
# 7. Generate monthly climatology figure
# ------------------------------------------------------------

month_abbreviations = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

x = np.arange(1, 13)

fig, axes = plt.subplots(
    3,
    1,
    figsize=(9, 10),
    sharex=True
)

# Significant wave height
axes[0].plot(
    x,
    monthly_hs.values,
    marker="o",
    linewidth=1.8
)

axes[0].set_ylabel("Hs (m)")
axes[0].set_title(
    "(a) Monthly Mean Significant Wave Height"
)
axes[0].grid(True, alpha=0.3)

# Mean wave period
axes[1].plot(
    x,
    monthly_tm.values,
    marker="o",
    linewidth=1.8
)

axes[1].set_ylabel("Tm (s)")
axes[1].set_title(
    "(b) Monthly Mean Wave Period"
)
axes[1].grid(True, alpha=0.3)

# Wave power density
axes[2].plot(
    x,
    monthly_wpd.values,
    marker="o",
    linewidth=1.8
)

axes[2].set_ylabel("WPD (kW/m)")
axes[2].set_title(
    "(c) Monthly Mean Wave Power Density"
)
axes[2].set_xlabel("Month")
axes[2].grid(True, alpha=0.3)

axes[2].set_xticks(x)
axes[2].set_xticklabels(month_abbreviations)

fig.suptitle(
    "Monthly Climatology of the Gulf of Guinea Wave Resource\n"
    "(ERA5, 2014–2025)",
    fontsize=13
)

fig.tight_layout(
    rect=[0, 0, 1, 0.96]
)

figure_file = (
    FIGURE_DIR / "monthly_climatology.png"
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
    f"\nMonthly table saved to:\n{table_file}"
)

print(
    f"\nMonthly figure saved to:\n{figure_file}"
)

ds.close()