import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# =============================================
# Option B — One figure per metric (means + IQR),
#             sizes encoded as line styles
# =============================================

# ---------- Load data ----------
df = pd.read_excel("results_big.xlsx")

# ---------- Derived metrics ----------
df["float_cut_ratio"] = df["floats"] / df["cuts"].replace(0, 1)
df["interruptions"] = df["cuts"] + df["skeins_used"]

df["width"] = df["size"].str.split("x").str[0].astype(int)
df["height"] = df["size"].str.split("x").str[1].astype(int)
df["stitches"] = df["width"] * df["height"]

df["cuts_per_100"] = df["cuts"] / df["stitches"] * 100
df["floats_per_100"] = df["floats"] / df["stitches"] * 100
df["loose_ends_per_100"] = df["loose_ends"] / df["stitches"] * 100
df["interruptions_per_100"] = df["interruptions"] / df["stitches"] * 100

# ---------- Styling ----------
MODEL_COLORS = {
    "dp": "#1f77b4",
    "f1s": "#d62728",
    "f2s": "#228B22"
}
LINESTYLES = ["-", "--", ":"]

def sizes_sorted(unique_sizes):
    def keyfunc(s):
        w, h = s.split("x")
        return (int(w), int(h))
    return sorted(unique_sizes, key=keyfunc)

def mean_iqr_line(df, y, ylabel, title):
    df2 = df.copy()
    df2["cluster_prob"] = df2["cluster_prob"].astype(float)
    df2["model"] = df2["model"].astype(str).str.strip().str.lower()

    g = (
        df2.groupby(["model", "size", "cluster_prob"])[y]
           .agg(mean="mean",
                q1=lambda s: s.quantile(0.25),
                q3=lambda s: s.quantile(0.75))
           .reset_index()
    )

    sizes = sizes_sorted(df2["size"].unique())
    ls_map = {s: LINESTYLES[i % len(LINESTYLES)] for i, s in enumerate(sizes)}

    fig, ax = plt.subplots(figsize=(8, 5))
    legend_entries = []

    for model, mdf in g.groupby("model"):
        color = MODEL_COLORS.get(model, "gray")
        for size, sdf in mdf.groupby("size"):
            sdf = sdf.sort_values("cluster_prob")
            (line,) = ax.plot(sdf["cluster_prob"], sdf["mean"],
                              linestyle=ls_map[size], color=color,
                              label=f"{model} | {size}")
            ax.fill_between(sdf["cluster_prob"], sdf["q1"], sdf["q3"],
                            alpha=0.15, color=color)
            legend_entries.append((line, f"{model} | {size}"))

    ax.set_title(title)
    ax.set_xlabel("Cluster Probability")
    ax.set_ylabel(ylabel)
    handles, labels = zip(*legend_entries)
    ax.legend(handles, labels, ncol=2, fontsize=9)
    fig.tight_layout()
    plt.show()

# ---------- Generate figures ----------
mean_iqr_line(df, "cost", "Yarn Cost",
              "Yarn Cost vs Cluster Probability (mean ± IQR)")
mean_iqr_line(df, "loose_ends_per_100", "Loose Ends per 100",
              "Loose Ends vs Cluster Probability (mean ± IQR)")
mean_iqr_line(df, "interruptions_per_100", "Interruptions per 100",
              "Interruptions vs Cluster Probability (mean ± IQR)")
mean_iqr_line(df, "float_cut_ratio", "Float / Cut Ratio",
              "Float vs Cutting Strategy Balance (mean ± IQR)")
mean_iqr_line(df, "floats_per_100", "Floats per 100",
              "Float Frequency vs Cluster Probability (mean ± IQR)")

# ---------- Optional summary ----------
summary = df.groupby(["size", "cluster_prob", "model"])[
    ["cost", "loose_ends_per_100", "interruptions_per_100", "float_cut_ratio"]
].mean().reset_index()
summary.to_csv("summary_results_table_option_b.csv", index=False)
print("Saved summary table → summary_results_table_option_b.csv")
