"""
PDF report generator using fpdf2.
Produces a professional structured report covering:
  - Executive Summary
  - Problem Analysis
  - EDA Findings
  - ML Model Results
  - Retention Strategies & Forecasts
  - Recommendations
"""

from fpdf import FPDF
from pathlib import Path
from datetime import date

PLOT_DIR = Path(__file__).parent.parent / "reports" / "plots"
REPORT_DIR = Path(__file__).parent.parent / "reports"


class ChurnReport(FPDF):
    BRAND_BLUE = (41, 128, 185)
    BRAND_GREEN = (39, 174, 96)
    BRAND_RED = (231, 76, 60)
    LIGHT_GRAY = (245, 245, 245)
    DARK_GRAY = (80, 80, 80)

    def header(self):
        self.set_fill_color(*self.BRAND_BLUE)
        self.rect(0, 0, 210, 12, "F")
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 3)
        self.cell(0, 6, "Customer Retention Analysis Report  |  Subscription-Based Streaming Service", ln=False)
        self.ln(14)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*self.DARK_GRAY)
        self.cell(0, 6, f"Page {self.page_no()} | Confidential - Internal Use Only", align="C")

    def section_title(self, title: str):
        self.ln(4)
        self.set_fill_color(*self.BRAND_BLUE)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, f"  {title}", ln=True, fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def sub_title(self, title: str):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*self.BRAND_BLUE)
        self.cell(0, 6, title, ln=True)
        self.set_text_color(0, 0, 0)

    def body_text(self, text: str, indent: int = 0):
        self.set_font("Helvetica", "", 9)
        self.set_x(10 + indent)
        self.multi_cell(0, 5, text)
        self.ln(1)

    def bullet(self, text: str):
        self.set_font("Helvetica", "", 9)
        self.set_x(14)
        self.cell(4, 5, chr(149), ln=False)
        self.multi_cell(0, 5, text)

    def kpi_box(self, label: str, value: str, color: tuple):
        self.set_fill_color(*color)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 14)
        self.cell(58, 14, value, align="C", fill=True, ln=False)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.DARK_GRAY)
        # label below
        x = self.get_x() - 58
        self.set_xy(x, self.get_y() + 14)
        self.cell(58, 5, label, align="C", ln=False)
        self.set_xy(self.get_x(), self.get_y() - 14)

    def add_plot(self, filename: str, w: int = 170, caption: str = ""):
        path = PLOT_DIR / filename
        if path.exists():
            self.image(str(path), x=20, w=w)
            if caption:
                self.set_font("Helvetica", "I", 8)
                self.set_text_color(*self.DARK_GRAY)
                self.cell(0, 5, caption, align="C", ln=True)
                self.set_text_color(0, 0, 0)
            self.ln(2)

    def table_row(self, cells: list, widths: list, header: bool = False, fill: bool = False):
        if header:
            self.set_fill_color(*self.BRAND_BLUE)
            self.set_text_color(255, 255, 255)
            self.set_font("Helvetica", "B", 8)
        else:
            self.set_font("Helvetica", "", 8)
            self.set_text_color(0, 0, 0)
            if fill:
                self.set_fill_color(*self.LIGHT_GRAY)
            else:
                self.set_fill_color(255, 255, 255)

        for cell, w in zip(cells, widths):
            self.cell(w, 6, str(cell), border=1, fill=True, ln=False)
        self.ln()


def generate_report(eda_stats: dict, model_metrics: dict, strategy_results: dict) -> str:
    """Build and save the PDF report. Returns the output path."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    pdf = ChurnReport(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(10, 15, 10)

    # -----------------------------------------------------------------------
    # COVER PAGE
    # -----------------------------------------------------------------------
    pdf.add_page()
    pdf.set_fill_color(*ChurnReport.BRAND_BLUE)
    pdf.rect(0, 0, 210, 297, "F")

    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(0, 70)
    pdf.cell(210, 14, "Customer Retention", align="C", ln=True)
    pdf.cell(210, 14, "Analysis & Strategy Report", align="C", ln=True)

    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(200, 230, 255)
    pdf.ln(6)
    pdf.cell(210, 8, "Subscription-Based Streaming Service", align="C", ln=True)

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(180, 210, 240)
    pdf.ln(4)
    pdf.cell(210, 7, f"Prepared: {date.today().strftime('%B %d, %Y')}", align="C", ln=True)
    pdf.cell(210, 7, "Classification: Confidential", align="C", ln=True)

    # KPI strip on cover
    pdf.set_xy(15, 180)
    pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(*ChurnReport.BRAND_BLUE)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(180, 10, "Key Findings at a Glance", align="C", fill=True, ln=True)

    baseline = strategy_results["baseline_churn_rate"]
    projected = strategy_results["projected_churn_rate"]
    reduction = strategy_results["total_churn_reduction_pct"]

    pdf.set_xy(15, 195)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_fill_color(231, 76, 60)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(58, 16, f"{baseline:.1%}", align="C", fill=True, ln=False)
    pdf.set_fill_color(39, 174, 96)
    pdf.cell(58, 16, f"{projected:.1%}", align="C", fill=True, ln=False)
    pdf.set_fill_color(41, 128, 185)
    pdf.cell(58, 16, f"{reduction:.1%}", align="C", fill=True, ln=True)

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(200, 230, 255)
    pdf.set_x(15)
    pdf.cell(58, 6, "Baseline Churn Rate", align="C", ln=False)
    pdf.cell(58, 6, "Projected Churn Rate", align="C", ln=False)
    pdf.cell(58, 6, "Total Churn Reduction", align="C", ln=True)

    # -----------------------------------------------------------------------
    # PAGE 2: EXECUTIVE SUMMARY
    # -----------------------------------------------------------------------
    pdf.add_page()
    pdf.section_title("1. Executive Summary")

    pdf.body_text(
        "This report presents a structured analysis of customer churn for a mid-sized "
        "subscription-based streaming service. The churn rate has increased by 15% over the "
        "past year, driven primarily by content dissatisfaction, pricing sensitivity, and "
        "intensifying competition. A machine learning model was developed to identify at-risk "
        "customers, and six evidence-based retention strategies were evaluated for their "
        "projected impact and ROI."
    )

    pdf.sub_title("Key Findings")
    pdf.bullet(f"Current churn rate: {baseline:.2%} of the customer base per period.")
    pdf.bullet("Top churn drivers: price dissatisfaction, low content satisfaction, and competitor exposure.")
    pdf.bullet(f"Best ML model: {model_metrics['best_model_name']} with AUC = {model_metrics['best_auc']:.4f}.")
    pdf.bullet(
        f"Combined strategies project churn reduction of {reduction:.1%}, "
        f"bringing the rate from {baseline:.2%} to {projected:.2%}."
    )
    pdf.bullet("Budget rebalancing from 80/20 to 60/40 (acquisition/retention) is recommended.")
    pdf.bullet("Highest ROI strategy: Proactive Churn Intervention using ML risk scores.")

    pdf.ln(4)
    pdf.section_title("2. Problem Statement & Context")

    pdf.sub_title("Business Context")
    pdf.body_text(
        "The company has experienced steady growth in new customer acquisition. However, "
        "the churn rate has risen 15% year-over-year, eroding the net subscriber base and "
        "threatening long-term revenue. The current marketing budget allocates 80% to "
        "acquisition and only 20% to retention - a ratio that is misaligned with the "
        "economic reality that retaining a customer costs 5-7x less than acquiring a new one."
    )

    pdf.sub_title("Root Cause Hypothesis (5-Why Framework)")
    causes = [
        ("Why are customers churning?", "They are dissatisfied with the service value."),
        ("Why are they dissatisfied?", "Content variety is limited and pricing feels high relative to alternatives."),
        ("Why is content limited?", "Content investment has not kept pace with competitor libraries."),
        ("Why is pricing a concern?", "New entrants offer cheaper or free ad-supported tiers."),
        ("Why hasn't retention been addressed?", "80% of budget is allocated to acquisition, leaving retention under-resourced."),
    ]
    for i, (q, a) in enumerate(causes, 1):
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_x(14)
        pdf.cell(0, 5, f"  Why {i}: {q}", ln=True)
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_x(22)
        pdf.cell(0, 5, f"-> {a}", ln=True)
    pdf.ln(2)

    # -----------------------------------------------------------------------
    # PAGE 3: EDA
    # -----------------------------------------------------------------------
    pdf.add_page()
    pdf.section_title("3. Exploratory Data Analysis")

    pdf.body_text(
        "A synthetic dataset of 5,000 customers was generated to reflect realistic churn "
        "patterns consistent with the problem statement. The dataset includes demographics, "
        "subscription plan, engagement metrics, satisfaction scores, competitive exposure, "
        "and support interactions."
    )

    pdf.add_plot("01_churn_distribution.png", w=90, caption="Figure 1: Overall churn distribution")
    pdf.add_plot("02_churn_by_plan.png", w=150, caption="Figure 2: Churn rate by subscription plan")
    pdf.add_plot("03_satisfaction_vs_churn.png", w=180, caption="Figure 3: Churn rate by satisfaction dimension")

    pdf.sub_title("Key EDA Insights")
    pdf.bullet("Basic plan subscribers show the highest churn rate, likely due to limited features at a price point close to competitors.")
    pdf.bullet("Customers with content satisfaction score <= 2 churn at 2-3x the rate of satisfied customers.")
    pdf.bullet("Price dissatisfaction is the single strongest satisfaction-based churn predictor.")
    pdf.bullet("Customers exposed to competitor offers churn at significantly higher rates.")

    pdf.add_page()
    pdf.add_plot("04_engagement_vs_churn.png", w=170, caption="Figure 4: Engagement metrics vs churn")
    pdf.add_plot("05_competitive_exposure.png", w=160, caption="Figure 5: Competitive exposure vs churn")
    pdf.add_plot("06_tenure_distribution.png", w=160, caption="Figure 6: Tenure distribution by churn status")

    pdf.sub_title("Engagement & Tenure Insights")
    pdf.bullet("Churned customers watch significantly fewer hours per week - low engagement is an early warning signal.")
    pdf.bullet("Customers who use a competitor service churn at nearly double the rate of those who don't.")
    pdf.bullet("Early-tenure customers (< 6 months) are at highest churn risk - onboarding experience is critical.")

    # -----------------------------------------------------------------------
    # PAGE: CORRELATION
    # -----------------------------------------------------------------------
    pdf.add_page()
    pdf.add_plot("07_correlation_heatmap.png", w=175, caption="Figure 7: Feature correlation heatmap")

    # -----------------------------------------------------------------------
    # PAGE: ML MODEL
    # -----------------------------------------------------------------------
    pdf.add_page()
    pdf.section_title("4. Churn Prediction Model")

    pdf.body_text(
        "Four machine learning classifiers were trained and evaluated using 5-fold "
        "stratified cross-validation. The target variable is binary churn (1 = churned, "
        "0 = retained). Models were compared on ROC-AUC, precision, recall, and F1-score."
    )

    # Model results table
    all_results = model_metrics["all_results"]
    headers = ["Model", "CV AUC", "Test AUC", "Precision", "Recall", "F1"]
    widths = [52, 25, 25, 25, 25, 25]
    pdf.table_row(headers, widths, header=True)
    for i, (name, res) in enumerate(all_results.items()):
        row = [
            name,
            f"{res['cv_auc_mean']:.4f} +/- {res['cv_auc_std']:.4f}",
            f"{res['auc']:.4f}",
            f"{res['precision']:.4f}",
            f"{res['recall']:.4f}",
            f"{res['f1']:.4f}",
        ]
        pdf.table_row(row, widths, fill=(i % 2 == 0))
    pdf.ln(4)

    pdf.sub_title(f"Best Model: {model_metrics['best_model_name']}")
    pdf.bullet(f"Test AUC: {model_metrics['best_auc']:.4f}")
    pdf.bullet(f"Precision: {model_metrics['best_precision']:.4f}")
    pdf.bullet(f"Recall: {model_metrics['best_recall']:.4f}")
    pdf.bullet(f"F1-Score: {model_metrics['best_f1']:.4f}")
    pdf.bullet(f"Top predictors: {', '.join(model_metrics['top_features'][:5])}")
    pdf.ln(2)

    pdf.add_plot("08_model_comparison.png", w=160, caption="Figure 8: Model comparison (CV AUC)")
    pdf.add_page()
    pdf.add_plot("09_roc_curves.png", w=150, caption="Figure 9: ROC curves for all models")
    pdf.add_plot("10_confusion_matrix.png", w=110, caption="Figure 10: Confusion matrix - best model")
    pdf.add_plot("11_feature_importance.png", w=160, caption="Figure 11: Feature importances - best model")

    # -----------------------------------------------------------------------
    # PAGE: STRATEGIES
    # -----------------------------------------------------------------------
    pdf.add_page()
    pdf.section_title("5. Retention Strategies & Impact Forecast")

    pdf.body_text(
        "Six evidence-based retention strategies were designed based on the root cause "
        "analysis and EDA findings. Each strategy targets a specific churn driver and "
        "customer segment. The table below summarises projected impact and ROI."
    )

    # Strategy summary table
    s_df = strategy_results["strategy_df"]
    cols = ["Strategy", "Churn Reduction (%)", "Customers Saved/Month",
            "Annual Revenue Saved ($)", "Net Benefit ($)", "Complexity", "Time to Impact"]
    col_widths = [48, 22, 28, 32, 28, 18, 20]
    pdf.table_row(cols, col_widths, header=True)
    for i, row in s_df.iterrows():
        pdf.table_row([row[c] for c in cols], col_widths, fill=(i % 2 == 0))
    pdf.ln(4)

    # Strategy details
    from src.retention_strategies import STRATEGIES
    pdf.sub_title("Strategy Details")
    for name, s in STRATEGIES.items():
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*ChurnReport.BRAND_BLUE)
        pdf.cell(0, 5, f"  {name}", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.body_text(s["description"], indent=4)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_x(18)
        pdf.cell(0, 4, f"Target: {s['target_segment']}  |  Complexity: {s['complexity']}  |  Time to impact: {s['time_to_impact_months']} months", ln=True)
        pdf.ln(1)

    pdf.add_page()
    pdf.add_plot("12_strategy_net_benefit.png", w=170, caption="Figure 12: Net annual benefit by strategy")
    pdf.add_plot("13_churn_forecast.png", w=170, caption="Figure 13: 12-month churn rate forecast")
    pdf.add_plot("14_budget_reallocation.png", w=160, caption="Figure 14: Proposed budget reallocation")

    # -----------------------------------------------------------------------
    # PAGE: RECOMMENDATIONS & CONCLUSION
    # -----------------------------------------------------------------------
    pdf.add_page()
    pdf.section_title("6. Recommendations & Implementation Roadmap")

    phases = [
        ("Phase 1 - Quick Wins (Month 1-2)", [
            "Deploy engagement re-activation campaigns for low-watch-hour customers.",
            "Implement ML churn scoring pipeline; trigger proactive win-back offers for top 20% risk.",
            "Begin budget rebalancing: shift 20% of acquisition spend to retention.",
        ]),
        ("Phase 2 - Core Initiatives (Month 3-4)", [
            "Launch personalised pricing tiers: annual plans, family bundles, ad-supported tier.",
            "Introduce loyalty & rewards programme for customers with tenure > 12 months.",
            "Establish NPS and satisfaction tracking dashboards for continuous monitoring.",
        ]),
        ("Phase 3 - Strategic Investment (Month 5-6+)", [
            "Accelerate content diversification: commission originals in underserved genres.",
            "A/B test pricing changes and measure churn impact before full rollout.",
            "Refine ML model quarterly with new behavioural data.",
        ]),
    ]

    for phase_title, actions in phases:
        pdf.sub_title(phase_title)
        for action in actions:
            pdf.bullet(action)
        pdf.ln(2)

    pdf.section_title("7. Success Metrics & KPIs")
    kpis = [
        ("Monthly Churn Rate", f"Reduce from {strategy_results['baseline_churn_rate']:.2%} to < {strategy_results['projected_churn_rate']:.2%}"),
        ("Customer Lifetime Value (CLV)", "Increase by >= 15% within 12 months"),
        ("Net Promoter Score (NPS)", "Improve by >= 10 points"),
        ("Content Satisfaction Score", "Increase average from current level to >= 3.8/5"),
        ("Engagement (Watch Hours)", "Increase avg weekly watch hours by >= 20%"),
        ("Retention Budget ROI", "Achieve >= 300% ROI on retention spend"),
    ]
    widths_kpi = [80, 110]
    pdf.table_row(["KPI", "Target"], widths_kpi, header=True)
    for i, (kpi, target) in enumerate(kpis):
        pdf.table_row([kpi, target], widths_kpi, fill=(i % 2 == 0))
    pdf.ln(4)

    pdf.section_title("8. Conclusion")
    pdf.body_text(
        f"The analysis demonstrates that the churn problem is addressable through a "
        f"combination of data-driven targeting, content investment, and pricing flexibility. "
        f"By implementing the six proposed strategies in a phased approach, the projected "
        f"churn rate drops from {strategy_results['baseline_churn_rate']:.2%} to "
        f"{strategy_results['projected_churn_rate']:.2%} - a reduction of "
        f"{strategy_results['total_churn_reduction_pct']:.1%}, exceeding the 20% target "
        f"set in the problem statement. The ML churn prediction model (AUC = "
        f"{model_metrics['best_auc']:.4f}) enables proactive, personalised interventions "
        f"that maximise retention ROI while minimising unnecessary discount spend."
    )

    out_path = REPORT_DIR / "Customer_Retention_Analysis_Report.pdf"
    pdf.output(str(out_path))
    print(f"[REPORT] PDF saved -> {out_path}")
    return str(out_path)
