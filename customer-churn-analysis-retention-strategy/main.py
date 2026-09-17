"""
Main orchestrator for the Customer Churn Analysis & Retention Strategy project.

Run:
    python main.py

Outputs:
    data/customer_churn_data.csv
    reports/plots/*.png
    reports/Customer_Retention_Analysis_Report.pdf
"""

import sys
from pathlib import Path

# Ensure src is importable
sys.path.insert(0, str(Path(__file__).parent))

from src.data_generator import generate_churn_dataset
from src.eda import run_eda
from src.churn_model import train_and_evaluate
from src.retention_strategies import simulate_impact
from src.report_generator import generate_report


def main():
    print("=" * 60)
    print("  Customer Churn Analysis & Retention Strategy Pipeline")
    print("=" * 60)

    # 1. Generate synthetic dataset
    print("\n[1/5] Generating synthetic customer dataset...")
    df = generate_churn_dataset(n_customers=5000)
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    csv_path = data_dir / "customer_churn_data.csv"
    df.to_csv(csv_path, index=False)
    print(f"  Dataset: {df.shape[0]} customers | Churn rate: {df['churned'].mean():.2%}")

    # 2. Exploratory Data Analysis
    print("\n[2/5] Running EDA...")
    eda_stats = run_eda(df)

    # 3. Train churn prediction model
    print("\n[3/5] Training ML models...")
    model_metrics = train_and_evaluate(df)

    # 4. Simulate retention strategies
    print("\n[4/5] Simulating retention strategies...")
    strategy_results = simulate_impact(df, baseline_churn_rate=eda_stats["overall_churn_rate"])

    # 5. Generate PDF report
    print("\n[5/5] Generating PDF report...")
    report_path = generate_report(eda_stats, model_metrics, strategy_results)

    print("\n" + "=" * 60)
    print("  Pipeline complete.")
    print(f"  Report: {report_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
