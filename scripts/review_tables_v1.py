"""MAE/RMSE table (Supplementary Table S4f) and block-bootstrap ratio intervals (Table S6h) from the fold-level
predictions in results/. Run from the repository root: python scripts/review_tables_v1.py"""
import numpy as np, pandas as pd
J = pd.concat([pd.read_csv("data/jura/prediction.csv"), pd.read_csv("data/jura/validation.csv")], ignore_index=True)
J["id"] = np.arange(len(J))
m = pd.read_csv("data/meuse/meuse.csv"); M = pd.DataFrame({"X": m.x / 1000, "Y": m.y / 1000, "id": np.arange(len(m))})
XY = {"Jura": J.set_index("id")[["X", "Y"]], "Meuse": M.set_index("id")[["X", "Y"]]}; BLK = {"Jura": 1.0, "Meuse": 0.5}
D = {"Jura": pd.read_csv("results/jura_fold_predictions.csv.gz"), "Meuse": pd.read_csv("results/meuse_fold_predictions.csv.gz")}
T4 = ["Zn", "Cd", "Cu", "Pb"]
def sel(d, meth, t): return d[(d.method == meth) & (d.target == t) & (d.scheme == "repcv") & (d.variant == "sel")]
rows = []
for ds, d in D.items():
    for meth in ["OK", "RK", "KED-lin", "KED-spline", "KED-sel", "MLP", "RK-MLP-v3", "GNN-K", "GNN-sel", "NN-GLS", "Ort"]:
        r = {"data": ds, "method": meth}
        for t in T4:
            x = sel(d, meth, t).assign(rep=lambda h: h.fold // 5)
            r["MAE_" + t] = x.groupby("rep").apply(lambda h: np.mean(np.abs(h.pred - h.y))).mean()
            r["RMSE_" + t] = x.groupby("rep").apply(lambda h: np.sqrt(np.mean((h.pred - h.y) ** 2))).mean()
        rows.append(r)
pd.DataFrame(rows).to_csv("tables/TableS4f_MAE_RMSE.csv", index=False)
def pae(d, meth, t):
    x = sel(d, meth, t); return x.assign(ae=(x.pred - x.y).abs()).groupby("id").ae.mean()
out = []
for ds in D:
    for a, b in [("NN-GLS", "KED-lin"), ("GNN-sel", "KED-sel"), ("GNN-K", "KED-lin"), ("GNN-K", "KED-sel"),
                 ("GNN-sel", "KED-lin"), ("Ort", "KED-sel"), ("GNN-K", "RK")]:
        for t in T4:
            ea, eb = pae(D[ds], a, t), pae(D[ds], b, t); eb = eb.loc[ea.index]; xy = XY[ds].loc[ea.index].values
            blk = pd.factorize(pd.Series(list(zip((xy[:, 0] // BLK[ds]).astype(int), (xy[:, 1] // BLK[ds]).astype(int)))))[0]
            nb = blk.max() + 1; sa, sb = np.bincount(blk, ea.values, nb), np.bincount(blk, eb.values, nb)
            pick = np.random.default_rng(42).integers(0, nb, (2000, nb)); r = sa[pick].sum(1) / sb[pick].sum(1)
            lo, hi = np.quantile(r, [0.025, 0.975])
            out.append({"data": ds, "target": t, "A": a, "B": b, "ratio": ea.sum() / eb.sum(), "lo": lo, "hi": hi, "blocks": nb})
pd.DataFrame(out).to_csv("tables/TableS6h_bootstrap_ratio_CI.csv", index=False)
print("written tables/TableS4f_MAE_RMSE.csv and tables/TableS6h_bootstrap_ratio_CI.csv")
