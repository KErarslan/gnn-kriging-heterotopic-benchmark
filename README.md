# When do graph neural networks outperform kriging with auxiliary data?

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23437648.svg)](https://doi.org/10.5281/zenodo.23437648)

Code, fold-level predictions and figures for the manuscript

> Erarslan, K. *When do graph neural networks outperform kriging with auxiliary data? Noise, auxiliary–latent coupling and the role of hybrids.* (submitted)

The study compares graph neural networks (GNN), plain neural networks and hybrid neural–geostatistical models
with kriging-based methods (OK, RK, KED, co-kriging) for **heterotopic** prediction, where the auxiliary variables
are known at the prediction location. The design was neutral by intent: both sides received the same
information, the same inner-fold selection protocol and comparable tuning effort.

## Data

| Data set | Role | n | Source |
|---|---|---|---|
| Jura | real data, confirmatory + H9 | 359 | Goovaerts (1997); R package `gstat`, files as served by `geostats-datasets` v1.0.0 |
| Meuse | real data, pre-declared replication + H9 | 155 | Rikken & Van Rijn (1993); R package `sp` (Pebesma & Bivand 2005) |
| Walker Lake | exhaustive reference, mechanism experiments | 470 / 78 000 | Isaaks & Srivastava (1989); R package `gstat`, via `geostats-datasets` v1.0.0 |

The exact files used are included in `data/` (GPL ≥ 2, see `data/LICENSE-DATA.md`; checksums in `data/SHA256SUMS`).
The Python package `geostats-datasets` can no longer be installed from PyPI, so the notebook does **not** download Jura and
Walker Lake: CELL 1 reads them from `ROOT/data/` and stops if a SHA-256 checksum differs from the files used in the study.
Meuse is downloaded from the `sp` repository at run time (a copy is in `data/meuse/`). Fold definitions are in `folds/`.

**Setup on Colab:** zip the `data/` folder as `datasets_v1.zip` with top-level folder `datasets_v1/` (or copy the folder itself
to `MyDrive/GNN_Jura_Benchmark/data/datasets_v1/`); CELL 1 unpacks and verifies it.

## Repository layout

```
notebooks/   GNN_kriging_benchmark_v17.ipynb  – full pipeline (CELL 1–76), with saved outputs
results/     fold-level predictions (*.csv.gz), selection metadata, summary tables and test results
figures/     Figures 1–8 (PDF + PNG; Figs 1 and 8 also SVG), numbered as in the manuscript, and the data behind Figs 3, 4, 6, 7 (FigN_data.csv)
tables/      real-data MAE table with SDs (Table 2 of the manuscript; file name Table3_real_data_MAE.*)
folds/       outer/inner fold indices (repeated 5 × 5 CV, 4 inner folds)
docs/        H9 pre-registration record (Turkish original + English translation)
scripts/     make_schematics_v5.py – draws Figures 1 and 8 (no data needed);
             review_tables_v1.py – MAE/RMSE and block-bootstrap ratio tables (Supplementary Tables S4f, S6h) from results/
data/        raw data copies (GPL ≥ 2) + SHA256SUMS
manifest.json  SHA-256 of every file + package versions
```

## Reproducing

* **Figures and tables only (minutes, no training):** run notebook CELL 1, then CELL 74–75.
  They read only the saved predictions.
* **Full re-run (≈ 2 days on a Colab CPU runtime):** run all cells. Every run is checkpointed per outer fold,
  so an interrupted session resumes where it stopped. CELL 76 times one outer fold per method
  (computing-time table, Table 3 of the manuscript).

Environment: Python 3.13 (Google Colab); exact package versions in `requirements.txt` and `manifest.json`. Seeds are fixed (`SEED = 42`); neural predictions are
5-seed ensembles. Small numerical differences across hardware are expected for the neural models.

## Naming note

A few keys are kept exactly as stored on disk so that the checkpoints remain valid: the Walker Lake proxy conditions
`yeniden` (reconstructed), `döndürülmüş` (fully rotated), `ayrıntı-döndürülmüş` (detail rotated), `düzey-döndürülmüş` (level rotated),
and the method name `Ort` (simple average of GNN-sel and KED-sel; called **Avg** in the manuscript). Figures and tables use the English labels.

## Transparency

* Stages were added sequentially; what had been seen before each stage, and every withdrawn claim,
  is logged in the manuscript's Supplementary Material (Table S1 and Section S2).
* H9 (equal effort on the neural side) was specified in a dated internal record before any H9 error was inspected
  (`docs/H9_preregistration_TR_v1.md`; English translation in `docs/H9_preregistration_EN_v1.md`). The record was not deposited
  with an external registry. Post-hoc analyses (H9-4) are labelled as such.
* A sign error in the pre-declared M3 hypothesis is disclosed in the notebook (correction note after cell 69).

## Citation

See `CITATION.cff`. Archived release (code, results and the full raw result folders): Zenodo, [doi:10.5281/zenodo.23437648](https://doi.org/10.5281/zenodo.23437648).

## Licence

Code: MIT (see `LICENSE`). Results, figures and tables: CC BY 4.0.
Data in `data/`: GPL ≥ 2, under the terms of their original sources (see `data/LICENSE-DATA.md`).
