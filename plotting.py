import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

# ----------------------------------------------------
# Load data
# ----------------------------------------------------
df = pd.read_excel("results_big.xlsx")

# ----------------------------------------------------
# Compute derived metrics
# ----------------------------------------------------

# Avoid division by zero when computing ratios
df["float_cut_ratio"] = df["floats"] / df["cuts"].replace(0, 1)

# Add interruptions metric (cut or attach a new skein stops work flow)
df["interruptions"] = df["cuts"] + df["skeins_used"]

# We normalize counts by total stitches to compare across sizes
df["width"] = df["size"].str.split("x").str[0].astype(int)
df["height"] = df["size"].str.split("x").str[1].astype(int)
df["stitches"] = df["width"] * df["height"]

df["cuts_per_100"] = df["cuts"] / df["stitches"] * 100
df["floats_per_100"] = df["floats"] / df["stitches"] * 100
df["loose_ends_per_100"] = df["loose_ends"] / df["stitches"] * 100
df["interruptions_per_100"] = df["interruptions"] / df["stitches"] * 100

# ----------------------------------------------------
# Plotting helper
# ----------------------------------------------------

MODEL_COLORS = {
    "dp": "#1f77b4",  
    "f1s": "#d62728",  
    "f2s": "#228B22"   
}

def boxplot_by_cluster(df, y, ylabel, title):
    for size in sorted(df["size"].unique()):
        sub = df[df["size"] == size].copy()

        sub["model"] = sub["model"].astype(str).str.strip().str.lower()
        cluster_probs = sorted(map(float, sub["cluster_prob"].unique()))
        models = sorted(sub["model"].unique())

        fig, ax = plt.subplots(figsize=(8, 4))
        group_positions = np.arange(len(cluster_probs), dtype=float)

        total_width = 0.8
        width = total_width / max(len(models), 1)
        offsets = (np.arange(len(models)) - (len(models) - 1) / 2.0) * width

        for i, model in enumerate(models):
            data = [
                sub[(sub["model"] == model) & (sub["cluster_prob"] == cp)][y].dropna().values
                for cp in cluster_probs
            ]
            positions = group_positions + offsets[i]

            bp = ax.boxplot(
                data,
                positions=positions,
                widths=width * 0.9,
                showfliers=False,
                patch_artist=True,
                medianprops=dict(color="black", linewidth=1.5),
                whiskerprops=dict(color="black"),
                capprops=dict(color="black"),
                boxprops=dict(edgecolor="black"),
            )

            face = MODEL_COLORS.get(model, "gray")
            for box in bp["boxes"]:
                box.set(facecolor=face, edgecolor="black", alpha=0.75)

        ax.set_title(f"{title} (size {size})")
        ax.set_xlabel("Cluster Probability")
        ax.set_ylabel(ylabel)
        ax.set_xticks(group_positions)
        ax.set_xticklabels([f"{cp:g}" for cp in cluster_probs])
        ax.set_xlim(group_positions[0] - 0.6, group_positions[-1] + 0.6)

        handles = [
            Patch(facecolor=MODEL_COLORS.get(m, "gray"), edgecolor="black", label=m, alpha=0.75)
            for m in models
        ]
        ax.legend(handles=handles, title="Model")

        fig.tight_layout()
        plt.show()

# ----------------------------------------------------
# PLOTS
# ----------------------------------------------------

boxplot_by_cluster(df, "cost", "Yarn Cost",
                   "Yarn Cost Across Cluster Probabilities and Models")
boxplot_by_cluster(df, "loose_ends_per_100", "Loose Ends per 100 Stitches",
                   "Loose Ends Across Cluster Probabilities and Models")
boxplot_by_cluster(df, "interruptions_per_100", "Interruptions per 100 Stitches",
                   "Crochet Flow Interruptions Across Models")
boxplot_by_cluster(df, "float_cut_ratio", "Float / Cut Ratio",
                   "Float vs Cutting Strategy Balance Across Models")
boxplot_by_cluster(df, "floats_per_100", "Floats per 100 Stitches",
                   "Float Frequency Across Models")



# ----------------------------------------------------
# Optional: export summary table (very useful in results text)
# ----------------------------------------------------
summary = df.groupby(["size", "cluster_prob", "model"])[
    ["cost", "loose_ends_per_100", "interruptions_per_100", "float_cut_ratio"]
].mean().reset_index()

summary.to_csv("summary_results_table.csv", index=False)
print("Saved summary table → summary_results_table.csv")
