"""
Retention strategy simulation and impact forecasting.
Models the effect of proposed interventions on churn rate and revenue.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

PLOT_DIR = Path(__file__).parent.parent / "reports" / "plots"
PLOT_DIR.mkdir(parents=True, exist_ok=True)


def _save(fig: plt.Figure, name: str):
    path = PLOT_DIR / name
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"  Saved -> {path.name}")


# ---------------------------------------------------------------------------
# Strategy definitions
# Each strategy has:
#   - description
#   - estimated churn reduction (relative %)
#   - estimated cost per customer per month ($)
#   - implementation complexity (Low / Medium / High)
#   - time to impact (months)
# ---------------------------------------------------------------------------
STRATEGIES = {
    "Content Diversification": {
        "description": "Expand content library with exclusive originals and licensed titles "
                       "targeting underserved genres identified via feedback analysis.",
        "churn_reduction_pct": 0.08,
        "cost_per_customer": 1.20,
        "complexity": "High",
        "time_to_impact_months": 6,
        "target_segment": "Low content satisfaction (score <= 2)",
    },
    "Personalised Pricing Tiers": {
        "description": "Introduce flexible pricing: annual discount plans, family bundles, "
                       "and a lower-cost ad-supported tier to compete with free alternatives.",
        "churn_reduction_pct": 0.07,
        "cost_per_customer": 0.80,
        "complexity": "Medium",
        "time_to_impact_months": 3,
        "target_segment": "Low price satisfaction (score <= 2)",
    },
    "Proactive Churn Intervention": {
        "description": "Use ML churn scores to trigger personalised win-back offers "
                       "(discounts, free months) for high-risk customers before they cancel.",
        "churn_reduction_pct": 0.06,
        "cost_per_customer": 0.60,
        "complexity": "Medium",
        "time_to_impact_months": 2,
        "target_segment": "High churn probability (top 20% risk score)",
    },
    "Engagement Re-activation": {
        "description": "Automated email/push campaigns for low-engagement users with "
                       "curated recommendations and 'continue watching' nudges.",
        "churn_reduction_pct": 0.04,
        "cost_per_customer": 0.25,
        "complexity": "Low",
        "time_to_impact_months": 1,
        "target_segment": "Low watch hours (< 2 hrs/week)",
    },
    "Loyalty & Rewards Programme": {
        "description": "Reward long-tenure customers with exclusive perks, early access, "
                       "and milestone discounts to increase switching costs.",
        "churn_reduction_pct": 0.03,
        "cost_per_customer": 0.40,
        "complexity": "Low",
        "time_to_impact_months": 3,
        "target_segment": "Tenure > 12 months",
    },
    "Budget Rebalancing (60/40)": {
        "description": "Shift marketing budget from 80/20 acquisition/retention split "
                       "to 60/40, redirecting funds to retention programmes.",
        "churn_reduction_pct": 0.05,
        "cost_per_customer": 0.50,
        "complexity": "Low",
        "time_to_impact_months": 2,
        "target_segment": "All customers",
    },
}


def simulate_impact(df: pd.DataFrame, baseline_churn_rate: float) -> dict:
    """
    Simulate the combined and individual impact of retention strategies.
    Returns a dict of forecasted metrics.
    """
    print("[STRATEGY] Simulating retention strategy impact...")

    n_customers = len(df)
    avg_monthly_revenue = df["monthly_charge"].mean()
    baseline_churners = int(n_customers * baseline_churn_rate)
    baseline_monthly_revenue = n_customers * avg_monthly_revenue

    # --- Individual strategy impact ---
    strategy_results = []
    for name, s in STRATEGIES.items():
        churners_saved = int(baseline_churners * s["churn_reduction_pct"])
        new_churn_rate = baseline_churn_rate * (1 - s["churn_reduction_pct"])
        monthly_revenue_saved = churners_saved * avg_monthly_revenue
        annual_revenue_saved = monthly_revenue_saved * 12
        annual_cost = n_customers * s["cost_per_customer"] * 12
        net_benefit = annual_revenue_saved - annual_cost
        roi = (net_benefit / annual_cost) * 100 if annual_cost > 0 else 0

        strategy_results.append({
            "Strategy": name,
            "Churn Reduction (%)": f"{s['churn_reduction_pct']:.0%}",
            "Customers Saved/Month": churners_saved,
            "Annual Revenue Saved ($)": f"${annual_revenue_saved:,.0f}",
            "Annual Cost ($)": f"${annual_cost:,.0f}",
            "Net Benefit ($)": f"${net_benefit:,.0f}",
            "ROI (%)": f"{roi:.0f}%",
            "Complexity": s["complexity"],
            "Time to Impact": f"{s['time_to_impact_months']} months",
            "Target Segment": s["target_segment"],
        })

    strategy_df = pd.DataFrame(strategy_results)

    # --- Combined strategy impact (diminishing returns) ---
    # Strategies are partially overlapping; use multiplicative reduction
    combined_reduction = 1.0
    for s in STRATEGIES.values():
        combined_reduction *= (1 - s["churn_reduction_pct"])
    combined_new_churn_rate = baseline_churn_rate * combined_reduction
    total_churn_reduction_pct = (baseline_churn_rate - combined_new_churn_rate) / baseline_churn_rate

    print(f"  Baseline churn rate:  {baseline_churn_rate:.2%}")
    print(f"  Projected churn rate: {combined_new_churn_rate:.2%}")
    print(f"  Total churn reduction: {total_churn_reduction_pct:.2%}")

    # --- 12-month forecast ---
    months = list(range(1, 13))
    monthly_churn_rates = []
    current_rate = baseline_churn_rate

    # Strategies kick in at different months
    strategy_timeline = sorted(STRATEGIES.items(), key=lambda x: x[1]["time_to_impact_months"])
    active_reductions = []

    for m in months:
        for name, s in strategy_timeline:
            if m == s["time_to_impact_months"] and name not in [r[0] for r in active_reductions]:
                active_reductions.append((name, s["churn_reduction_pct"]))

        rate = baseline_churn_rate
        for _, red in active_reductions:
            rate *= (1 - red)
        monthly_churn_rates.append(rate)

    # --- Plot 1: Strategy ROI comparison ---
    fig, ax = plt.subplots(figsize=(10, 5))
    roi_vals = []
    for s_name, s in STRATEGIES.items():
        churners_saved = int(baseline_churners * s["churn_reduction_pct"])
        annual_revenue_saved = churners_saved * avg_monthly_revenue * 12
        annual_cost = n_customers * s["cost_per_customer"] * 12
        net = annual_revenue_saved - annual_cost
        roi_vals.append(net / 1000)  # in $K

    colors = ["#2ECC71" if v > 0 else "#E74C3C" for v in roi_vals]
    bars = ax.bar(list(STRATEGIES.keys()), roi_vals, color=colors, alpha=0.85)
    ax.set_ylabel("Net Annual Benefit ($K)")
    ax.set_title("Net Annual Benefit by Retention Strategy", fontsize=13, fontweight="bold")
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
    plt.xticks(rotation=20, ha="right", fontsize=9)
    for bar, val in zip(bars, roi_vals):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + (0.5 if val >= 0 else -2),
                f"${val:.0f}K", ha="center", va="bottom", fontsize=8, fontweight="bold")
    _save(fig, "12_strategy_net_benefit.png")

    # --- Plot 2: 12-month churn forecast ---
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(months, [baseline_churn_rate * 100] * 12, "r--",
            linewidth=2, label=f"Baseline ({baseline_churn_rate:.1%})")
    ax.plot(months, [r * 100 for r in monthly_churn_rates], "g-o",
            linewidth=2.5, markersize=6, label="Projected (with strategies)")
    ax.fill_between(months, [baseline_churn_rate * 100] * 12,
                    [r * 100 for r in monthly_churn_rates], alpha=0.15, color="green")
    ax.set_xlabel("Month")
    ax.set_ylabel("Monthly Churn Rate (%)")
    ax.set_title("12-Month Churn Rate Forecast", fontsize=13, fontweight="bold")
    ax.legend(fontsize=10)
    ax.set_xticks(months)

    # Annotate strategy activation points
    for name, s in STRATEGIES.items():
        m = s["time_to_impact_months"]
        if m <= 12:
            ax.axvline(m, color="gray", linestyle=":", alpha=0.5)
    _save(fig, "13_churn_forecast.png")

    # --- Plot 3: Budget reallocation impact ---
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    labels = ["Acquisition", "Retention"]
    current_budget = [80, 20]
    proposed_budget = [60, 40]
    colors_b = ["#3498DB", "#2ECC71"]
    for ax, data, title in zip(axes, [current_budget, proposed_budget],
                                ["Current Budget Split", "Proposed Budget Split"]):
        ax.pie(data, labels=labels, autopct="%1.0f%%", colors=colors_b,
               startangle=90, wedgeprops={"edgecolor": "white", "linewidth": 2})
        ax.set_title(title, fontsize=12, fontweight="bold")
    _save(fig, "14_budget_reallocation.png")

    print("[STRATEGY] Complete.\n")

    return {
        "baseline_churn_rate": baseline_churn_rate,
        "projected_churn_rate": combined_new_churn_rate,
        "total_churn_reduction_pct": total_churn_reduction_pct,
        "monthly_forecast": monthly_churn_rates,
        "strategy_df": strategy_df,
        "avg_monthly_revenue": avg_monthly_revenue,
        "n_customers": n_customers,
    }
