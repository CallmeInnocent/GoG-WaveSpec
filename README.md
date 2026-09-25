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

The extracted dataset contains a **31 × 31 spatial grid** at approximately 0.5° spacing.

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

### Temporal coverage

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

$begin:math:display$
P \= \\frac\{\\rho g\^2 H\_s\^2 T\_m\}\{64\\pi\}
$end:math:display$

where:

- $begin:math:text$P$end:math:text$ = wave power density
- $begin:math:text$\\rho \= 1025\\ \\mathrm\{kg\/m\^3\}$end:math:text$ = seawater density
- $begin:math:text$g \= 9\.81\\ \\mathrm\{m\/s\^2\}$end:math:text$ = gravitational acceleration
- $begin:math:text$H\_s$end:math:text$ = significant wave height
- $begin:math:text$T\_m$end:math:text$ = mean wave period

Wave power density is reported in **kW/m**.

### Important averaging procedure

Wave power density is calculated independently at each valid observation **before temporal averaging**:

$begin:math:display$
\\overline\{P\} \= \\operatorname\{mean\}\[P\(t\)\]
$end:math:display$

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

### 01 — ERA5 acquisition

Downloads the required ERA5 wave variables for the analysis domain and study period using the Copernicus Climate Data Store API.

### 02 — Dataset inspection

Checks the downloaded NetCDF dataset, including dimensions, temporal coverage, spatial coverage, and the presence of the required variables.

### 03 — Regional statistics

Calculates domain-wide long-term mean:

- significant wave height
- mean wave period
- wave power density

### 04 — Monthly climatology

Calculates monthly climatological means for Hs, Tm, and wave power density.

### 05 — Seasonal climatology

Calculates climatological statistics for:

- DJF — December, January, February
- MAM — March, April, May
- JJA — June, July, August
- SON — September, October, November

### 06 — Hs–Tm occurrence analysis

Constructs a two-dimensional occurrence distribution using:

- Hs bins: **0–3 m**, at **0.25 m** intervals
- Tm bins: **4–13 s**, at **0.5 s** intervals

The selected plotting range contains approximately **99.29%** of valid paired Hs–Tm observations.

### 07 — Spatial wave power density

Calculates long-term mean wave power density independently at each ERA5 grid cell across the analysis domain.

### 08 — Representative offshore case studies

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

---

## Representative Offshore Case Studies

The three case-study locations produce the following long-term statistics:

| Location | ERA5 grid location | Mean Hs (m) | Mean Tm (s) | Mean WPD (kW/m) |
|---|---|---:|---:|---:|
| Côte d'Ivoire offshore | 4.5°N, 4.0°W | 1.3746 | 8.7484 | 8.8338 |
| Ghana offshore | 4.5°N, 1.0°W | 1.3264 | 8.7359 | 8.1999 |
| Lagos offshore | 5.0°N, 3.5°E | 1.3742 | 8.8960 | 9.0541 |

The nominal Lagos case-study longitude is **3.4°E**. Because the ERA5 dataset uses a 0.5° grid, nearest-neighbour extraction selects the **3.5°E** ERA5 grid cell.

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
├── requirements.txt
└── README.md
```

---

## Reproducing the Analysis

### 1. Clone the repository

```bash
git clone <repository-url>
cd GoG-WaveSpec
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Copernicus CDS access

A valid Copernicus Climate Data Store account and CDS API configuration are required to retrieve ERA5 data.

### 4. Download the ERA5 dataset

```bash
python scripts/01_download_era5.py
```

The resulting file should be stored as:

```text
data/gog_2014_2025.nc
```

### 5. Inspect the dataset

```bash
python scripts/02_inspect_dataset.py
```

### 6. Run the analyses

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

This separation prevents resource characterization from being conflated with WEC performance.

---

## Data Availability

ERA5 data are available through the **Copernicus Climate Data Store**.

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

License information will be added to the repository before public release.