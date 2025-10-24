import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
from datetime import datetime

def generate_chart(rows, cols, colors=2, cluster_prob=0.8):
    chart = np.zeros((rows, cols), dtype=int)
    chart[0, 0] = np.random.randint(colors)
    for r in range(rows):
        for c in range(cols):
            if (r, c) != (0, 0):
                neighbors = []
                if r > 0:
                    neighbors.append(chart[r-1, c])
                if c > 0:
                    neighbors.append(chart[r, c-1])
                chart[r, c] = np.random.choice(neighbors) if np.random.rand() < cluster_prob else np.random.randint(colors)
    return chart


def visualize_chart(chart, title, save_base=None, bold_grid=True, major_every=5):
    rows, cols = chart.shape
    cmap = mcolors.ListedColormap(["#800020", "#fdf6e3"])  # Burgundy & Cream

    fig, ax = plt.subplots(figsize=(5, 5), facecolor="#e6e6e6")
    ax.set_aspect('equal', adjustable='box')

    # Draw crisp squares with grid lines
    ax.pcolormesh(
        np.arange(cols + 1), np.arange(rows + 1), chart,
        cmap=cmap, edgecolors='black', linewidth=0.6,
        shading='flat', antialiased=False
    )

    # Top-left origin like knitting charts
    ax.set_xlim(0, cols)
    ax.set_ylim(rows, 0)

    # Optional bold gridlines every n stitches
    if bold_grid and major_every:
        for x in range(0, cols + 1, major_every):
            ax.plot([x, x], [0, rows], color='black', linewidth=1.2)
        for y in range(0, rows + 1, major_every):
            ax.plot([0, cols], [y, y], color='black', linewidth=1.2)

    ax.axis('off')
    fig.suptitle(title, fontsize=14)

    # Save all outputs if save_base provided
    if save_base:
        base_name = f"{save_base}"

        np.save(f"{base_name}.npy", chart)
        pd.DataFrame(chart).to_csv(f"{base_name}.csv", index=False, header=False)
        plt.savefig(f"{base_name}.png", dpi=300, bbox_inches='tight', pad_inches=0.1, facecolor=fig.get_facecolor())
    #plt.show()


if __name__ == "__main__":
    #visualize_chart(chart, title = name, save_base = name, bold_grid=True)
    
    for i in range(1, 2): 
        chart = generate_chart(10, 20, 2, 0.95)
        #name = f"100x100_0.995_#{i}"
        name = "test"
        visualize_chart(chart, title = name, save_base = name, bold_grid = True)
