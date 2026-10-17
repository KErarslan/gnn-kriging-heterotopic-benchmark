# Pre-registration — H9: equal effort on the neural side

> English translation of `H9_preregistration_TR_v1.md`. The Turkish file is the original, timestamped record; if the two differ, the Turkish text prevails.

**Study:** Comparison of GNN and kriging-based methods in a heterotopic setting
**Author:** Kaan Erarslan (Kütahya Dumlupınar University)
**Registration date:** 13 October 2026 (the upload timestamp is authoritative)
**Code:** `GNN_Jura_Asama0-5_H4_v9.ipynb`, cells 70–72 (CELL 70–72 in `GNN_kriging_benchmark_v12.ipynb`)

## 1. Rationale

In earlier stages, whenever GNN-K won, new competitors were added on the classical side (KED-lin, KED-spline, KED-log, KED-sel). On the neural side GNN-K did not change: hidden size fixed at 64, a narrow tuning grid. H9 closes this asymmetry of effort. Six new candidates are added on the neural side, and `GNN-sel`, selected on inner folds, competes with `KED-sel`, also selected on inner folds.

## 2. What had been seen before this registration

- No error (MAE) result of any H9 candidate had been seen.
- To check that the code runs, the six candidates were run on Meuse, Zn, first two outer folds. Only the selected hyperparameters and run times were inspected; prediction errors were not. These smoke tests are not part of the main run (written to a separate folder).
- Existing results were known: GNN-K, KED-lin, KED-sel and RK on Jura and Meuse (Stages 4g, 4h, 4j).

## 3. Data and protocol

- **Data:** Jura (359 points; targets Zn, Cd, Cu, Pb; auxiliaries the other six metals) and Meuse (155 points; targets Zn, Cd, Cu, Pb; auxiliaries dist, ffreq, soil).
- **Validation:** repeated cross-validation, 5 repeats × 5 folds, 4 inner folds within every outer training set. Fold files identical to earlier stages. The Jura canonical split is not run at this stage.
- **Metric:** MAE (original scale).

## 4. Candidates (neural side)

All use the same information: coordinates, the auxiliaries known at the target, and the target values at training points. No candidate uses information that KED does not see.

| # | Name | Definition |
|---|---|---|
| 1 | GNN-K | Existing. Neighbour targets, geometry and softmax attention (KCN family). |
| 2 | GNN-GAT | Standard two-layer graph attention network. Does not see neighbour targets. |
| 3 | GNN-K-PE | GNN-K plus multi-scale sinusoidal positional encoding (16 dimensions). |
| 4 | GNN-K-L | Hidden size 128, k ∈ {16, 32}, 20 % neighbour dropout during training, 10-seed ensemble. |
| 5 | GNN-K-cov | ρ(d) from a variogram fitted on the training data and the OK weight within the neighbour set are added to the edge features. |
| 6 | GNN-KED | Drift [1, auxiliaries] by GLS (as in KED); residual learned by GNN-K. |
| 7 | NN-GLS | MLP mean from the auxiliaries only, trained with a GLS (whitened) loss; then OK of the residual. |

## 5. Equality rules

- Every candidate's grid has 8 configurations (dropout {0.1; 0.3} × transform {raw, log} × a third dimension: k, or the hidden size for NN-GLS) and the same epoch grid (20, 40, …, 200).
- Configuration and epoch are selected on inner folds only, by inner-fold MAE.
- Outer prediction: 5-seed ensemble (GNN-K-L: 10).
- **GNN-sel:** in every outer fold, the candidate with the lowest inner-fold MAE among the seven.
- **KED-sel:** as defined in the earlier stage (KED-lin/KED-spline × raw/log, selected on inner folds).

## 6. Analyses

**H9-1 (primary).** GNN-sel vs KED-sel; 8 target–data combinations (Jura 4 + Meuse 4); pointwise paired Wilcoxon test (two-sided); Holm correction. No directional prediction. Decision rule:

- (a) GNN-sel MAE ≤ KED-sel in at least 6/8 **and** no target on which KED-sel is significantly better → "the neural side is at least equal on real data".
- (b) KED-sel significantly better in at least 2/8 **and** GNN-sel significantly better in none → "the classical side is better".
- (c) Otherwise → "mixed / target-dependent".

**H9-2 (exploratory).** Every candidate against KED-sel (7 × 8 = 56 tests, Holm). The pre-specified single variants (GNN-K, KED-lin) are always reported separately, against selection bias.

**H9-3 (exploratory).** Ort = (GNN-sel + KED-sel) / 2 with fixed equal weights; against KED-sel.

**Additional reports.** How many outer folds each candidate was selected in; the MAE table of every candidate.

## 7. Reporting commitment

The result will be published whatever its direction. Every change made after this registration (including bug fixes) will be stated separately with its date.
