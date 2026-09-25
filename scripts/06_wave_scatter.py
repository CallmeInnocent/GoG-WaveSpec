import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ------------------------------------------------------------
# GoG-WaveSpec: Hs-Tm Occurrence Analysis
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

# ------------------------------------------------------------
# 1. Open ERA5 dataset
# ------------------------------------------------------------

ds = xr.open_dataset(DATA_FILE)

hs = ds["swh"].values.flatten()
tm = ds["mwp"].values.flatten()

# ------------------------------------------------------------
# 2. Retain only paired valid Hs-Tm observations
# ------------------------------------------------------------

valid = np.isfinite(hs) & np.isfinite(tm)

hs = hs[valid]
tm = tm[valid]

print("\nGoG-WaveSpec — Hs-Tm Occurrence Analysis")
print("----------------------------------------")
print(f"Total valid paired observations: {len(hs):,}")

# ------------------------------------------------------------
# 3. Define occurrence bins
#
# Hs: 0–3 m in 0.25 m intervals
# Tm: 4–13 s in 0.5 s intervals
# ------------------------------------------------------------

hs_edges = np.arange(
    0.0,
    3.0 + 0.25,
    0.25
)

tm_edges = np.arange(
    4.0,
    13.0 + 0.5,
    0.5
)

# histogram2d expects x then y.
# Here:
# x = Hs
# y = Tm
#
# H[i,j] = number of observations in Hs bin i
# and Tm bin j.
# ------------------------------------------------------------

H, hs_edges, tm_edges = np.histogram2d(
    hs,
    tm,
    bins=[hs_edges, tm_edges]
)

# ------------------------------------------------------------
# 4. Export occurrence matrix
# ------------------------------------------------------------

hs_labels = [
    f"{hs_edges[i]:.2f}-{hs_edges[i+1]:.2f}"
    for i in range(len(hs_edges) - 1)
]

tm_labels = [
    f"{tm_edges[i]:.1f}-{tm_edges[i+1]:.1f}"
    for i in range(len(tm_edges) - 1)
]

occurrence_table = pd.DataFrame(
    H,
    index=hs_labels,
    columns=tm_labels
)

occurrence_table.index.name = "Hs_bin_m"

table_file = (
    TABLE_DIR / "hs_tm_occurrence_counts.csv"
)

occurrence_table.to_csv(table_file)

# ------------------------------------------------------------
# 5. Identify most populated bin
# ------------------------------------------------------------

max_index = np.unravel_index(
    np.argmax(H),
    H.shape
)

hs_i, tm_i = max_index

peak_count = int(H[hs_i, tm_i])

peak_hs_range = (
    hs_edges[hs_i],
    hs_edges[hs_i + 1]
)

peak_tm_range = (
    tm_edges[tm_i],
    tm_edges[tm_i + 1]
)

print(
    "\nMost populated occurrence bin:"
)

print(
    f"Hs = {peak_hs_range[0]:.2f}"
    f"–{peak_hs_range[1]:.2f} m"
)

print(
    f"Tm = {peak_tm_range[0]:.1f}"
    f"–{peak_tm_range[1]:.1f} s"
)

print(
    f"Occurrence count = {peak_count:,}"
)

# ------------------------------------------------------------
# 6. Calculate percentage captured by plotted range
# ------------------------------------------------------------

captured = int(H.sum())

capture_percentage = (
    captured / len(hs) * 100.0
)

print(
    f"\nObservations inside plotted range: "
    f"{captured:,}"
)

print(
    f"Coverage of valid observations: "
    f"{capture_percentage:.2f}%"
)

# ------------------------------------------------------------
# 7. Generate occurrence diagram
# ------------------------------------------------------------

fig, ax = plt.subplots(
    figsize=(10, 7)
)

mesh = ax.pcolormesh(
    tm_edges,
    hs_edges,
    H,
    shading="auto"
)

colorbar = fig.colorbar(
    mesh,
    ax=ax
)

colorbar.set_label(
    "Occurrence Count"
)

ax.set_xlabel(
    "Mean Wave Period, Tm (s)"
)

ax.set_ylabel(
    "Significant Wave Height, Hs (m)"
)

ax.set_title(
    "Gulf of Guinea Hs–Tm Occurrence Diagram\n"
    "(ERA5, 2014–2025)"
)

fig.tight_layout()

figure_file = (
    FIGURE_DIR / "hs_tm_occurrence.png"
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
    f"\nOccurrence table saved to:\n{table_file}"
)

print(
    f"\nOccurrence figure saved to:\n{figure_file}"
)

ds.close()