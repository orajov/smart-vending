from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_product_revenue_chart(report: pd.DataFrame, output: Path) -> None:  # STUDYME okruh 18
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(report["product_name"], report["revenue"])
    ax.set_title("Tržby podle produktu")
    ax.set_ylabel("Kč")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(output, dpi=150)
    plt.close(fig)
