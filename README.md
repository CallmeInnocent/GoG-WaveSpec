# GoG-WaveSpec

## Gulf of Guinea Wave-Energy Resource Characterization Using ERA5 (2014–2025)

GoG-WaveSpec is a reproducible Python workflow for characterizing the wave-energy resource within a Gulf of Guinea analysis domain using ERA5 reanalysis data from the Copernicus Climate Data Store.

The study examines the spatial, seasonal, and occurrence characteristics of the regional wave climate and translates them into engineering-relevant resource information that can support subsequent wave energy converter (WEC) assessment.

The analysis covers the period **2014–2025** and uses significant wave height, mean wave period, and mean wave direction obtained from ERA5.

---

## Research Question

The study addresses the following question:

> **What are the spatial and seasonal characteristics of the Gulf of Guinea wave-energy resource, and what do they imply for representative operating conditions relevant to subsequent WEC assessment?**

The purpose of the repository is therefore **resource characterization**, rather than device-performance or commercial-feasibility assessment.

---

## Analysis Domain

The ERA5 analysis domain is bounded by:

- **North:** 10°N
- **South:** 5°S
- **West:** 5°W
- **East:** 10°E

The extracted dataset contains a **31 × 31 spatial grid** at 0.5° spacing.

The rectangular domain is used as the analysis region for this study and should not be interpreted as a formal geographic definition of the entire Gulf of Guinea.

---

## ERA5 Dataset

The analysis uses the Copernicus Climate Data Store dataset:

**ERA5 hourly data on single levels**

Three wave variables were retrieved:

| Variable | ERA5 field | Symbol used |
|---|---|---|
| Significant height of combined wind waves and swell | `swh` | Hs |
| Mean wave period | `mwp` | Tm |
| Mean wave direction | `mwd` | — |

### Temporal Coverage

- **Start:** 1 January 2014
- **End:** 31 December 2025
- **Sampling:** one observation per day
- **Time:** 12:00 UTC
- **Time steps:** 4,383

This provides **12 complete calendar years** of ERA5 observations.

The raw NetCDF dataset is not included in the repository. It can be retrieved using the provided CDS acquisition script.

---

## Wave Power Density

Wave power density is calculated using:

**P = (ρg²Hs²Tm) / (64π)**

where:

- **P** = wave power density
- **ρ = 1025 kg/m³** = seawater density
- **g = 9.81 m/s²** = gravitational acceleration
- **Hs** = significant wave height
- **Tm** = mean wave period

Wave power density is reported in **kW/m**.

### Important Averaging Procedure

Wave power density is calculated independently at each valid observation before temporal averaging:

**Mean WPD = mean[P(t)]**

The workflow therefore does **not** estimate long-term wave power by substituting mean wave height and mean period into the nonlinear power equation.

---

## Analysis Workflow

The repository contains the following reproducible workflow:

```text
01_download_era5.py
        ↓
02_inspect_dataset.py
        ↓
03_regional_statistics.py
        ↓
04_monthly_climatology.py
        ↓
05_seasonal_climatology.py
        ↓
06_wave_scatter.py
        ↓
07_spatial_wpd.py
        ↓
08_case_study_locations.py
```

### 01 — ERA5 Acquisition

Downloads the required ERA5 wave variables for the analysis domain and study period using the Copernicus Climate Data Store API.

### 02 — Dataset Inspection

Checks the downloaded NetCDF dataset, including dimensions, temporal coverage, spatial coverage, and the presence of the required variables.

### 03 — Regional Statistics

Calculates domain-wide long-term mean:

- significant wave height
- mean wave period
- wave power density

### 04 — Monthly Climatology

Calculates monthly climatological means for Hs, Tm, and wave power density.

### 05 — Seasonal Climatology

Calculates climatological statistics for:

- DJF — December, January, February
- MAM — March, April, May
- JJA — June, July, August
- SON — September, October, November

### 06 — Hs–Tm Occurrence Analysis

Constructs a two-dimensional occurrence distribution using:

- Hs bins: **0–3 m**, at **0.25 m** intervals
- Tm bins: **4–13 s**, at **0.5 s** intervals

The selected plotting range contains approximately **99.29%** of valid paired Hs–Tm observations.

### 07 — Spatial Wave Power Density

Calculates long-term mean wave power density independently at each ERA5 grid cell across the analysis domain.

### 08 — Representative Offshore Case Studies

Extracts ERA5 conditions at three representative offshore locations:

- Côte d'Ivoire offshore
- Ghana offshore
- Lagos offshore

These locations are used as engineering case studies and are **not claimed to represent optimized WEC deployment sites**.

---

## Selected Results

The domain-wide long-term means obtained from the ERA5 dataset are:

| Metric | Mean |
|---|---:|
| Significant wave height | 1.4133 m |
| Mean wave period | 8.8299 s |
| Wave power density | 9.6718 kW/m |

Seasonal mean wave power density is:

| Season | Mean WPD (kW/m) |
|---|---:|
| DJF | 6.1838 |
| MAM | 9.3512 |
| JJA | 13.5932 |
| SON | 9.4907 |

The results show a clear seasonal cycle, with the strongest mean resource during **JJA** and the weakest during **DJF**.

The most populated Hs–Tm occurrence bin is:

- **Hs:** 1.25–1.50 m
- **Tm:** 8.5–9.0 s
- **Occurrence count:** 146,444 observations

The occurrence diagram contains **2,780,846** observations within the selected Hs–Tm plotting range, representing **99.29%** of the **2,800,737** valid paired observations.

---

## Spatial Wave Power Distribution

Long-term mean wave power density varies substantially across the rectangular analysis domain.

The calculated grid-cell range is:

- **Minimum mean WPD:** 0.4567 kW/m at 0.50°S, 9.50°E
- **Maximum mean WPD:** 12.7809 kW/m at 5.00°S, 5.00°W

These values represent the minimum and maximum ERA5 grid-cell means within the defined analysis domain.

They should **not** be interpreted as identifying the worst or best deployment locations. In particular, boundary, coastal, and land-adjacent grid cells require careful interpretation, and no siting optimization is performed in this study.

---

## Representative Offshore Case Studies

The three case-study locations produce the following long-term statistics:

| Location | ERA5 grid location | Mean Hs (m) | Mean Tm (s) | Mean WPD (kW/m) |
|---|---|---:|---:|---:|
| Côte d'Ivoire offshore | 4.5°N, 4.0°W | 1.3746 | 8.7484 | 8.8338 |
| Ghana offshore | 4.5°N, 1.0°W | 1.3264 | 8.7359 | 8.1999 |
| Lagos offshore | 5.0°N, 3.5°E | 1.3742 | 8.8960 | 9.0541 |

The nominal Lagos case-study longitude is **3.4°E**. Because the ERA5 dataset uses a 0.5° grid, nearest-neighbour extraction selects the **3.5°E** ERA5 grid cell.

The locations are intended to provide representative offshore cases for engineering interpretation and subsequent WEC assessment. They are not proposed as optimal or deployment-ready sites.

---

## Repository Structure

```text
GoG-WaveSpec/
│
├── data/
│   ├── README.md
│   └── gog_2014_2025.nc        # local only; excluded from Git
│
├── scripts/
│   ├── 01_download_era5.py
│   ├── 02_inspect_dataset.py
│   ├── 03_regional_statistics.py
│   ├── 04_monthly_climatology.py
│   ├── 05_seasonal_climatology.py
│   ├── 06_wave_scatter.py
│   ├── 07_spatial_wpd.py
│   └── 08_case_study_locations.py
│
├── outputs/
│   ├── figures/
│   │   ├── monthly_climatology.png
│   │   ├── seasonal_climatology.png
│   │   ├── hs_tm_occurrence.png
│   │   ├── spatial_mean_wpd.png
│   │   └── case_study_locations.png
│   │
│   └── tables/
│       ├── regional_statistics.csv
│       ├── monthly_climatology.csv
│       ├── seasonal_climatology.csv
│       ├── hs_tm_occurrence_counts.csv
│       ├── spatial_mean_wpd.csv
│       └── case_study_statistics.csv
│
├── .gitignore
├── LICENSE
├── requirements.txt
└── README.md
```

---

## Reproducing the Analysis

### 1. Clone the Repository

```bash
git clone https://github.com/CallmeInnocent/GoG-WaveSpec.git
cd GoG-WaveSpec
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Copernicus CDS Access

A valid Copernicus Climate Data Store account and CDS API configuration are required to retrieve ERA5 data.

### 4. Download the ERA5 Dataset

```bash
python scripts/01_download_era5.py
```

The resulting file should be stored as:

```text
data/gog_2014_2025.nc
```

### 5. Inspect the Dataset

```bash
python scripts/02_inspect_dataset.py
```

The verified dataset used in this study contains:

- **4,383** time steps
- **31** latitude points
- **31** longitude points
- `swh`, `mwp`, and `mwd` variables

### 6. Run the Analyses

```bash
python scripts/03_regional_statistics.py
python scripts/04_monthly_climatology.py
python scripts/05_seasonal_climatology.py
python scripts/06_wave_scatter.py
python scripts/07_spatial_wpd.py
python scripts/08_case_study_locations.py
```

Generated tables and figures are written automatically to the `outputs` directory.

---

## Scope and Limitations

This repository characterizes the **wave-energy resource** rather than the performance of a particular wave energy converter.

The wave power density formulation represents an engineering approximation based on significant wave height and mean wave period. The analysis does not explicitly model:

- WEC capture efficiency
- PTO or generator conversion efficiency
- device-specific hydrodynamics
- detailed directional spreading
- wave breaking
- detailed bathymetric or nearshore transformation
- seabed suitability
- electrical grid connection
- port or infrastructure constraints
- environmental constraints
- economic feasibility or LCOE

The spatial results should therefore be interpreted as **regional resource characteristics**, not as a deployment-suitability or site-optimization assessment.

Likewise, the three offshore locations are representative case studies rather than recommended deployment sites.

---

## Relationship to Subsequent WEC Assessment

GoG-WaveSpec establishes the resource-characterization stage of a broader wave-energy investigation.

The wave-climate characteristics identified here can inform subsequent WEC simulations and control studies. Device-specific modelling, period definitions, hydrodynamic assumptions, PTO control, and performance assessment are intentionally treated as separate downstream research questions.

Accordingly, this repository does not claim that a particular set of WEC operating conditions or controller parameters is formally derived from the resource characterization presented here.

This separation prevents resource characterization from being conflated with WEC performance.

---

## Data Availability

ERA5 data are available through the Copernicus Climate Data Store.

The raw NetCDF dataset used locally is intentionally excluded from version control. The repository provides an acquisition script so that the source dataset can be retrieved independently.

See `data/README.md` for additional information.

---

## Code Availability

All Python scripts required to reproduce the resource characterization, derived tables, and figures are provided in the `scripts` directory.

The numerical outputs used in the study are provided in `outputs/tables`, while generated figures are provided in `outputs/figures`.

---

## Citation

A formal citation for GoG-WaveSpec will be added following completion of the associated technical report/preprint.

---

## License

This project is released under the **MIT License**.

See the `LICENSE` file for the full license text.
