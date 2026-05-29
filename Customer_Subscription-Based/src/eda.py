"""
Exploratory Data Analysis for customer churn.
Generates plots saved to reports/plots/.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from pathlib import Path

PLOT_DIR = Path(__file__).parent.parent / "reports" / "plots"
PALETTE = {"Churned": "#E74C3C", "Retained": "#2ECC71"}
sns.set_theme(style="whitegrid", palette="muted")


def _save(fig: plt.Figure, name: str):
    PLOT_DIR.mkdir(parents=True, exist_ok=True)
    path = PLOT_DIR / name
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"  Saved -> {path.name}")


def run_eda(df: pd.DataFrame) -> dict:
    """Run full EDA suite and return summary statistics."""
    print("\n[EDA] Running exploratory data analysis...")

    stats = {}

    # 1. Overall churn rate
    churn_rate = df["churned"].mean()
    stats["overall_churn_rate"] = churn_rate
    print(f"  Overall churn rate: {churn_rate:.2%}")

    # 2. Churn distribution pie
    fig, ax = plt.subplots(figsize=(5, 5))
    counts = df["churned"].value_counts()
    ax.pie(
        counts,
        labels=["Retained", "Churned"],
        autopct="%1.1f%%",
        colors=["#2ECC71", "#E74C3C"],
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 2},
    )
    ax.set_title("Overall Churn Distribution", fontsize=14, fontweight="bold")
    _save(fig, "01_churn_distribution.png")

    # 3. Churn by plan
    fig, ax = plt.subplots(figsize=(7, 4))
    plan_churn = df.groupby("plan")["churned"].mean().sort_values(ascending=False)
    bars = ax.bar(plan_churn.index, plan_churn.values * 100, color=["#E74C3C", "#F39C12", "#3498DB"])
    ax.set_ylabel("Churn Rate (%)")
    ax.set_title("Churn Rate by Subscription Plan", fontsize=13, fontweight="bold")
    for bar, val in zip(bars, plan_churn.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f"{val:.1%}", ha="center", va="bottom", fontweight="bold")
    _save(fig, "02_churn_by_plan.png")
    stats["churn_by_plan"] = plan_churn.to_dict()

    # 4. Satisfaction scores vs churn
    sat_cols = ["content_satisfaction", "price_satisfaction", "support_satisfaction"]
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for ax, col in zip(axes, sat_cols):
        sat_churn = df.groupby(col)["churned"].mean() * 100
        ax.bar(sat_churn.index, sat_churn.values, color="#E74C3C", alpha=0.8)
        ax.set_xlabel("Satisfaction Score (1=Low, 5=High)")
        ax.set_ylabel("Churn Rate (%)")
        ax.set_title(col.replace("_", " ").title(), fontsize=11, fontweight="bold")
    fig.suptitle("Churn Rate by Satisfaction Dimension", fontsize=13, fontweight="bold", y=1.02)
    _save(fig, "03_satisfaction_vs_churn.png")

    # 5. Engagement vs churn (boxplots)
    eng_cols = ["avg_watch_hours_per_week", "login_frequency_per_month"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for ax, col in zip(axes, eng_cols):
        df_plot = df.copy()
        df_plot["Churn"] = df_plot["churned"].map({0: "Retained", 1: "Churned"})
        sns.boxplot(data=df_plot, x="Churn", y=col, palette=PALETTE, ax=ax)
        ax.set_title(col.replace("_", " ").title(), fontsize=11, fontweight="bold")
    fig.suptitle("Engagement Metrics: Churned vs Retained", fontsize=13, fontweight="bold")
    _save(fig, "04_engagement_vs_churn.png")

    # 6. Competitive exposure
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, col in zip(axes, ["uses_competitor", "received_competitor_offer"]):
        comp_churn = df.groupby(col)["churned"].mean() * 100
        ax.bar(["No", "Yes"], comp_churn.values, color=["#2ECC71", "#E74C3C"])
        ax.set_ylabel("Churn Rate (%)")
        ax.set_title(col.replace("_", " ").title(), fontsize=11, fontweight="bold")
        for i, v in enumerate(comp_churn.values):
            ax.text(i, v + 0.5, f"{v:.1f}%", ha="center", fontweight="bold")
    fig.suptitle("Competitive Exposure vs Churn", fontsize=13, fontweight="bold")
    _save(fig, "05_competitive_exposure.png")

    # 7. Tenure distribution by churn
    fig, ax = plt.subplots(figsize=(9, 4))
    df_plot = df.copy()
    df_plot["Churn"] = df_plot["churned"].map({0: "Retained", 1: "Churned"})
    sns.histplot(data=df_plot, x="tenure_months", hue="Churn",
                 palette=PALETTE, bins=20, alpha=0.7, ax=ax)
    ax.set_title("Tenure Distribution: Churned vs Retained", fontsize=13, fontweight="bold")
    ax.set_xlabel("Tenure (Months)")
    _save(fig, "06_tenure_distribution.png")

    # 8. Correlation heatmap (numeric features)
    fig, ax = plt.subplots(figsize=(11, 8))
    numeric_df = df.select_dtypes(include="number").drop(columns=["customer_id"], errors="ignore")
    corr = numeric_df.corr()
    import numpy as np
    mask_arr = np.zeros(corr.shape, dtype=bool)
    mask_arr[np.triu_indices_from(mask_arr, k=1)] = True
    mask = pd.DataFrame(mask_arr, index=corr.index, columns=corr.columns)
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdYlGn",
                center=0, linewidths=0.5, ax=ax, annot_kws={"size": 8})
    ax.set_title("Feature Correlation Heatmap", fontsize=13, fontweight="bold")
    _save(fig, "07_correlation_heatmap.png")

    print("[EDA] Complete.\n")
    return stats
