"""
Synthetic dataset generator for subscription-based streaming service churn analysis.
Simulates realistic customer behavior patterns aligned with the problem statement.
"""

import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
np.random.seed(SEED)


def generate_churn_dataset(n_customers: int = 5000) -> pd.DataFrame:
    """
    Generate a synthetic customer dataset with realistic churn signals.

    Features reflect the problem statement:
    - Content dissatisfaction
    - Pricing sensitivity
    - Competitive pressure signals
    - Engagement metrics
    """

    # --- Demographics ---
    age = np.random.normal(35, 12, n_customers).clip(18, 70).astype(int)
    tenure_months = np.random.exponential(18, n_customers).clip(1, 60).astype(int)

    # --- Subscription plan ---
    plan = np.random.choice(["basic", "standard", "premium"], n_customers, p=[0.4, 0.35, 0.25])
    plan_price = {"basic": 7.99, "standard": 13.99, "premium": 19.99}
    monthly_charge = np.array([plan_price[p] for p in plan])
    monthly_charge += np.random.normal(0, 0.5, n_customers)  # slight noise

    # --- Engagement metrics ---
    avg_watch_hours_per_week = np.random.gamma(2, 3, n_customers).clip(0, 40)
    login_frequency_per_month = np.random.poisson(12, n_customers).clip(0, 60)
    content_searches_per_month = np.random.poisson(8, n_customers).clip(0, 50)

    # --- Satisfaction signals ---
    # 1-5 scale; lower = more likely to churn
    content_satisfaction = np.random.choice([1, 2, 3, 4, 5], n_customers, p=[0.15, 0.20, 0.25, 0.25, 0.15])
    price_satisfaction = np.random.choice([1, 2, 3, 4, 5], n_customers, p=[0.20, 0.25, 0.25, 0.20, 0.10])
    support_satisfaction = np.random.choice([1, 2, 3, 4, 5], n_customers, p=[0.10, 0.15, 0.30, 0.30, 0.15])

    # --- Competitive exposure ---
    uses_competitor = np.random.choice([0, 1], n_customers, p=[0.55, 0.45])
    received_competitor_offer = np.random.choice([0, 1], n_customers, p=[0.65, 0.35])

    # --- Support interactions ---
    support_tickets_last_3m = np.random.poisson(1.2, n_customers).clip(0, 10)
    payment_failures_last_3m = np.random.poisson(0.3, n_customers).clip(0, 5)

    # --- Promotional history ---
    received_discount = np.random.choice([0, 1], n_customers, p=[0.70, 0.30])
    discount_amount = np.where(received_discount, np.random.uniform(1, 5, n_customers), 0.0)

    # --- Churn probability model (logistic-style) ---
    # Weighted combination of risk factors
    churn_score = (
        -0.05 * tenure_months
        + 0.30 * (6 - content_satisfaction)       # low content satisfaction → higher churn
        + 0.35 * (6 - price_satisfaction)          # price sensitivity is strong driver
        + 0.15 * (6 - support_satisfaction)
        - 0.08 * avg_watch_hours_per_week          # engaged users less likely to churn
        - 0.04 * login_frequency_per_month
        + 0.40 * uses_competitor
        + 0.30 * received_competitor_offer
        + 0.20 * support_tickets_last_3m
        + 0.25 * payment_failures_last_3m
        - 0.15 * received_discount
        + np.random.normal(0, 0.5, n_customers)    # noise
    )

    # Normalize to probability
    churn_prob = 1 / (1 + np.exp(-0.4 * churn_score))
    churned = (np.random.rand(n_customers) < churn_prob).astype(int)

    df = pd.DataFrame({
        "customer_id": [f"CUST_{i:05d}" for i in range(n_customers)],
        "age": age,
        "tenure_months": tenure_months,
        "plan": plan,
        "monthly_charge": monthly_charge.round(2),
        "avg_watch_hours_per_week": avg_watch_hours_per_week.round(2),
        "login_frequency_per_month": login_frequency_per_month,
        "content_searches_per_month": content_searches_per_month,
        "content_satisfaction": content_satisfaction,
        "price_satisfaction": price_satisfaction,
        "support_satisfaction": support_satisfaction,
        "uses_competitor": uses_competitor,
        "received_competitor_offer": received_competitor_offer,
        "support_tickets_last_3m": support_tickets_last_3m,
        "payment_failures_last_3m": payment_failures_last_3m,
        "received_discount": received_discount,
        "discount_amount": discount_amount.round(2),
        "churned": churned,
    })

    return df


if __name__ == "__main__":
    out_dir = Path(__file__).parent.parent / "data"
    out_dir.mkdir(exist_ok=True)
    df = generate_churn_dataset()
    path = out_dir / "customer_churn_data.csv"
    df.to_csv(path, index=False)
    print(f"Dataset saved → {path}  |  Shape: {df.shape}")
    print(f"Churn rate: {df['churned'].mean():.2%}")
