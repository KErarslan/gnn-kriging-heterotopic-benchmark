"""Figure 1 (study design) and Figure 8 (decision chart) — schematic figures, no data. v4: terminology (MAE, computing time); computing times from notebook v17, Cell 76.
Output: PDF (vector), SVG (editable) and PNG (600 dpi). Springer double-column width 174 mm."""
import os, sys
import matplotlib as mpl, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch

OUT = sys.argv[1] if len(sys.argv) > 1 else "figures"
os.makedirs(OUT, exist_ok=True)
MM = 1 / 25.4; W2 = 174 * MM
mpl.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7, "pdf.fonttype": 42, "svg.fonttype": "none", "savefig.dpi": 600})
INK, MUTED, LINE = "#222222", "#6b6b6b", "#9a9a9a"
BLUE, GREEN, VERM, GREY = "#0072B2", "#009E73", "#D55E00", "#7a7a7a"     # same colours as Figs 3–7 (KED-sel, NN-GLS, GNN-K, RK)
def tint(hex_, a):                                                       # light fill from a colour
    r, g, b = (int(hex_[i:i + 2], 16) / 255 for i in (1, 3, 5)); return (1 - a + a * r, 1 - a + a * g, 1 - a + a * b)

def box(ax, x, y, w, h, title, body, edge=LINE, fill="#ffffff", tsize=7.2, bsize=6.3, lw=0.8, title_color=INK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2", fc=fill, ec=edge, lw=lw))
    ax.text(x + 1.6, y + h - 1.6, title, ha="left", va="top", fontsize=tsize, fontweight="bold", color=title_color)
    if body: ax.text(x + 1.6, y + h - 5.2, body, ha="left", va="top", fontsize=bsize, color=INK, linespacing=1.35)

def arrow(ax, p, q, color=LINE, lw=0.9, style="-|>", rad=0.0, ms=7):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms, color=color, lw=lw, shrinkA=0, shrinkB=0,
                                 connectionstyle=f"arc3,rad={rad}"))

def save(fig, name):
    for ext in ("pdf", "svg", "png"): fig.savefig(os.path.join(OUT, f"{name}.{ext}"), bbox_inches="tight")
    plt.close(fig); print("saved", name)

# ======================================================================================= Figure 1
def fig1():
    fig = plt.figure(figsize=(W2, W2 * 0.62)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 174); ax.set_ylim(0, 108); ax.axis("off")
    # ---- row A: three data settings
    ax.text(2, 106, "A  Data settings and their role", fontsize=7.6, fontweight="bold", va="top")
    bw, bh, by = 55.3, 29, 74
    box(ax, 2, by, bw, bh, "Synthetic fields  (H5, H6)",
        "64 × 64 grid, n = 250 training points\n"
        "form: additive vs multiplicative\n"
        "noise σ$_n$ ∈ {0.01, 0.03, 0.1, 0.3}\n"
        "2 × 4 × 5 = 40 paired runs\n\n"
        "Role: noise dose–response under\na correctly specified drift", edge=GREY)
    box(ax, 59.3, by, bw, bh, "Walker Lake  (H4–H8)",
        "exhaustive truth, 78 000 nodes\n"
        "V = x̄ · ln(U + 1) / 10, noise-free\n"
        "1 clustered + 5 random samples (n = 470)\n"
        "proxy fields: x̄ rotated 180° (all,\nlevel only, detail only)\n"
        "Role: mechanism — auxiliary–latent coupling", edge=GREY)
    box(ax, 116.6, by, bw + 0.4, bh, "Real field data  (Jura, Meuse)",
        "Jura: n = 359, 4 targets, 6 metals as\nauxiliaries\n"
        "Meuse: n = 155, 4 targets, dist,\nflood frequency, soil\n"
        "repeated CV 5 × 5, 4 inner folds\n"
        "Role: practical relevance", edge=GREY)
    # ---- row B: two sides + shared protocol
    ax.text(2, 70.5, "B  Two method families with the same information and the same selection protocol", fontsize=7.6, fontweight="bold", va="top")
    by2, bh2 = 39, 28
    box(ax, 2, by2, 52, bh2, "Kriging-based",
        "OK, RK (OLS trend + residual OK)\n"
        "KED-lin, KED-spline, KED-log\n"
        "  → KED-sel (inner-fold selection)\n"
        "collocated / LMC co-kriging,\nmulti-Gaussian CCoK\n"
        "Ratio-K (oracle form, WL only)", edge=BLUE, fill=tint(BLUE, 0.07), title_color=BLUE)
    box(ax, 120, by2, 52, bh2, "Neural",
        "MLP, GNN-SAGE, GNN-K (learned kriging)\n"
        "H9, equal effort: GNN-GAT, GNN-K-PE,\n"
        "GNN-K-L, GNN-K-cov, GNN-KED,\nNN-GLS (hybrid)\n"
        "  → GNN-sel (inner-fold selection)\n"
        "RK-MLP (two-stage hybrid)", edge=VERM, fill=tint(VERM, 0.07), title_color=VERM)
    box(ax, 57, by2, 60, bh2, "Shared protocol",
        "inputs: coordinates, auxiliaries at the target,\n"
        "targets at training points only\n"
        "all tuning on inner folds (transform, drift,\n"
        "hyperparameters, epochs); MAE\n"
        "pointwise paired Wilcoxon + Holm;\n"
        "spatial block bootstrap", edge=INK, fill="#f4f4f4")
    arrow(ax, (57, by2 + bh2 / 2), (54.4, by2 + bh2 / 2), color=INK); arrow(ax, (117, by2 + bh2 / 2), (119.6, by2 + bh2 / 2), color=INK)
    # ---- row C: stages and evidence layers
    ax.text(2, 35, "C  Staged design and evidence layers (every number in the paper carries one label)", fontsize=7.6, fontweight="bold", va="top")
    stages = [("Stages 0–2", "Jura\nconfirmatory test"), ("Stage 3", "Walker Lake\nvs truth"), ("Stage 4", "mechanism:\nH4–H8, KED"),
              ("Stage 4j", "Meuse\nreplication"), ("Stage 5", "H9: equal\nneural effort"), ("Stage 6", "figures, export\n(no new runs)")]
    sx, sw, sy, sh = 2, 26.3, 20.5, 10.5
    for i, (a, b) in enumerate(stages):
        x = sx + i * (sw + 2.4)
        ax.add_patch(FancyBboxPatch((x, sy), sw, sh, boxstyle="round,pad=0,rounding_size=1", fc="#ffffff", ec=LINE, lw=0.7))
        ax.text(x + sw / 2, sy + sh - 1.4, a, ha="center", va="top", fontsize=6.4, fontweight="bold")
        ax.text(x + sw / 2, sy + 1.4, b, ha="center", va="bottom", fontsize=5.9, color=INK, linespacing=1.2)
        if i: arrow(ax, (x - 2.3, sy + sh / 2), (x - 0.1, sy + sh / 2), color=LINE, ms=6)
    layers = [("1  Confirmatory", "Jura: GNN-K vs RK", INK), ("2a  Pre-registered", "H9-1: GNN-sel vs\nKED-sel", INK),
              ("2b  Rule fixed before run", "H4–H8, J-KED, Meuse\nM1–M2, H9-2/3", MUTED),
              ("3  Exploratory", "error decomposition,\nselection, computing time", MUTED), ("4  Post hoc, labelled", "H9-4, M3 correction", MUTED)]
    lx, lw_, ly, lh = 2, 32.4, 1, 13
    shades = [0.55, 0.42, 0.30, 0.18, 0.10]
    for i, ((a, b, c), sh_) in enumerate(zip(layers, shades)):
        x = lx + i * (lw_ + 2)
        ax.add_patch(FancyBboxPatch((x, ly), lw_, lh, boxstyle="round,pad=0,rounding_size=1", fc=tint("#444444", sh_), ec="none"))
        tc = "white" if sh_ > 0.35 else INK
        ax.text(x + 1.5, ly + lh - 1.5, a, ha="left", va="top", fontsize=6.4, fontweight="bold", color=tc)
        ax.text(x + 1.5, ly + 1.4, b, ha="left", va="bottom", fontsize=5.8, color=tc, linespacing=1.2)
    ax.annotate("", xy=(2, 16.6), xytext=(60, 16.6), arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.6))
    ax.text(62, 16.6, "stronger inference", ha="left", va="center", fontsize=5.8, color=MUTED)
    save(fig, "Fig1_study_design")

# ======================================================================================= Figure 8
def diamond(ax, cx, cy, w, h, text, size=6.4):
    ax.add_patch(Polygon([(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)], closed=True, fc="#f4f4f4", ec=INK, lw=0.8))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=size, linespacing=1.25)

def rec(ax, x, y, w, h, title, body, color):
    box(ax, x, y, w, h, title, body, edge=color, fill=tint(color, 0.09), title_color=color, tsize=7, bsize=6.1, lw=1.0)

def lab(ax, x, y, t, ha="center"):
    ax.text(x, y, t, ha=ha, va="center", fontsize=6.2, color=INK, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))

def fig8():
    fig = plt.figure(figsize=(W2, W2 * 0.73)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 174); ax.set_ylim(0, 127); ax.axis("off")
    # start
    ax.add_patch(FancyBboxPatch((29, 115), 116, 10, boxstyle="round,pad=0,rounding_size=4", fc=INK, ec="none"))
    ax.text(87, 120, "Heterotopic prediction: auxiliaries known at every prediction location\n"
                     "Step 0 — always fit KED (linear and spline drift, selected on inner folds): seconds per fold",
            ha="center", va="center", fontsize=6.4, color="white", linespacing=1.3)
    # Q1 noise
    diamond(ax, 87, 101, 76, 19, "Q1  Is the target nearly noise-free\nafter the drift? (small relative\nnugget; e.g. exhaustive fields)", size=6.2)
    arrow(ax, (87, 115), (87, 110.6), color=INK)
    # NO branch (noisy, real field data) -> left
    lab(ax, 33, 104.5, "no — typical field data")
    arrow(ax, (49, 101), (29, 101), color=INK); arrow(ax, (29, 101), (29, 45.6), color=INK)
    by_, bh_ = 13, 32
    rec(ax, 2, by_, 54, bh_, "Keep the kriging framework",
        "KED is the reference. Pure GNNs gain little\n"
        "and not reliably: Jura ≈ KED; on Meuse\n"
        "(n = 155) most variants had significantly\n"
        "higher MAE on Zn and Pb. If a neural model\n"
        "is wanted, use a hybrid that keeps kriging:\n"
        "NN-GLS (NN drift under GLS + OK of residual).\n"
        "Never significantly less accurate than KED-lin;\n"
        "MAE: Jura −4 to −10 %, Meuse ≈ equal.", GREEN)
    lab(ax, 87, 84.5, "yes")
    arrow(ax, (87, 91.5), (87, 77.6), color=INK)
    diamond(ax, 87, 66, 80, 22, "Q2  Is the auxiliary coupled to the\nLEVEL of a latent factor that\ndrives the target?", size=6.2)
    ax.add_patch(FancyBboxPatch((122, 78), 50, 21, boxstyle="round,pad=0,rounding_size=1.2", fc="white", ec=LINE, lw=0.6, ls=(0, (2, 1.5))))
    ax.text(124, 97.2, "Examples for Q2", ha="left", va="top", fontsize=6.1, fontweight="bold", color=INK)
    ax.text(124, 93.2, "Walker Lake: U = roughness of the surface\nwhose elevation scales V.\n"
                       "Mining: a lithology or alteration proxy that\nis high where the background grade of the\nore domain is high.",
            ha="left", va="top", fontsize=5.8, color=INK, linespacing=1.3)
    ax.plot([122, 117], [82, 72.5], color=LINE, lw=0.6, ls=(0, (2, 1.5)))
    lab(ax, 137, 69.5, "yes")
    arrow(ax, (127, 66), (145, 66), color=INK); arrow(ax, (145, 66), (145, 45.6), color=INK)
    rec(ax, 118, by_, 54, bh_, "Learned kriging can outperform KED",
        "GNN-K: 30 % lower MAE than KED-sel on\n"
        "Walker Lake (ratio 0.70, 5 random samples).\n"
        "Gain sits where the latent factor is high\n"
        "(Q4 ratio ≈ 0.6); elsewhere no consistent\n"
        "advantage. Smaller under clustered\n"
        "sampling (0.82). Breaking the level coupling\n"
        "removes ≈ 2/3 of the gain. Still validate\n"
        "against KED on inner folds.", VERM)
    arrow(ax, (87, 55), (87, 45.6), color=INK)
    lab(ax, 87, 50.3, "no / unknown")
    rec(ax, 60, by_, 54, bh_, "KED is enough",
        "With a correctly specified drift and no\n"
        "coupling, KED-sel had the lower MAE in\n"
        "40/40 synthetic runs; with the coupling\n"
        "broken on Walker Lake (fully rotated),\n"
        "GNN-K / KED-sel MAE ratio = 1.14.\n\n"
        "Noise changes the size of the difference,\n"
        "not its direction.", BLUE)
    # computing-time strip
    ax.add_patch(FancyBboxPatch((2, 0.5), 170, 11, boxstyle="round,pad=0,rounding_size=1.2", fc="#f4f4f4", ec="none"))
    ax.text(4, 6, "Computing time per outer fold, nested selection included (one CPU core): kriging 0.2–3.5 s · KED-sel 1–7 s · NN-GLS 27–43 s ·\n"
                     "GNN-K 53–97 s · GNN-K-L 187–418 s. "
                     "Full design with all 7 neural candidates (GNN-sel): ≈ 13 h (Meuse), ≈ 26 h (Jura); KED-sel: minutes.\n"
                     "Evidence base: synthetic fields, Walker Lake, Jura, Meuse. The questions are qualitative; no thresholds are calibrated.",
            ha="left", va="center", fontsize=6.1, color=INK, linespacing=1.35)
    save(fig, "Fig8_decision_chart")

if __name__ == "__main__":
    fig1(); fig8()
