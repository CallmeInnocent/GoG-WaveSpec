import xarray as xr
import numpy as np
import pandas as pd
from pathlib import Path

# ------------------------------------------------------------
# GoG-WaveSpec: Regional Wave Resource Statistics
# ERA5 Gulf of Guinea, 2014–2025
# ------------------------------------------------------------

# Repository root determined from this script
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# ERA5 dataset stored locally in the repository data directory
DATA_FILE = PROJECT_ROOT / "data" / "gog_2014_2025.nc"

# Output directory
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "tables"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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
# 2. Calculate wave power density for every valid observation
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
# 3. Regional long-term statistics
# ------------------------------------------------------------

mean_hs = float(hs.mean(skipna=True).values)
mean_tm = float(tm.mean(skipna=True).values)
mean_wpd = float(wpd.mean(skipna=True).values)

# ------------------------------------------------------------
# 4. Display results
# ------------------------------------------------------------

print("\nGoG-WaveSpec — Regional Statistics")
print("----------------------------------")
print(f"Mean Hs  : {mean_hs:.4f} m")
print(f"Mean Tm  : {mean_tm:.4f} s")
print(f"Mean WPD : {mean_wpd:.4f} kW/m")

# ------------------------------------------------------------
# 5. Save results for report/reproducibility
# ------------------------------------------------------------

results = pd.DataFrame(
    {
        "Statistic": [
            "Mean significant wave height",
            "Mean wave period",
            "Mean wave power density",
        ],
        "Symbol": ["Hs", "Tm", "WPD"],
        "Value": [mean_hs, mean_tm, mean_wpd],
        "Unit": ["m", "s", "kW/m"],
    }
)

output_file = OUTPUT_DIR / "regional_statistics.csv"
results.to_csv(output_file, index=False)

print(f"\nResults saved to:\n{output_file}")

ds.close()