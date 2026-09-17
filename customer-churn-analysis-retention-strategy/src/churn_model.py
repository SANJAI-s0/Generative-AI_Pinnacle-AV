"""
Churn prediction model: trains multiple classifiers, selects best,
evaluates performance, and returns feature importances.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    classification_report, roc_auc_score, roc_curve,
    confusion_matrix, ConfusionMatrixDisplay
)
from xgboost import XGBClassifier
import warnings
warnings.filterwarnings("ignore")

PLOT_DIR = Path(__file__).parent.parent / "reports" / "plots"
PLOT_DIR.mkdir(parents=True, exist_ok=True)


def _save(fig: plt.Figure, name: str):
    path = PLOT_DIR / name
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"  Saved -> {path.name}")


def prepare_features(df: pd.DataFrame):
    """Encode categoricals and return X, y."""
    df = df.copy()
    le = LabelEncoder()
    df["plan_encoded"] = le.fit_transform(df["plan"])

    feature_cols = [
        "age", "tenure_months", "plan_encoded", "monthly_charge",
        "avg_watch_hours_per_week", "login_frequency_per_month",
        "content_searches_per_month", "content_satisfaction",
        "price_satisfaction", "support_satisfaction",
        "uses_competitor", "received_competitor_offer",
        "support_tickets_last_3m", "payment_failures_last_3m",
        "received_discount", "discount_amount",
    ]
    X = df[feature_cols]
    y = df["churned"]
    return X, y, feature_cols


def train_and_evaluate(df: pd.DataFrame) -> dict:
    """Train models, evaluate, plot results, return best model metrics."""
    print("[MODEL] Training churn prediction models...")

    X, y, feature_cols = prepare_features(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc = scaler.transform(X_test)

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=200, random_state=42),
        "XGBoost": XGBClassifier(n_estimators=200, random_state=42,
                                  eval_metric="logloss", verbosity=0),
    }

    results = {}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    for name, model in models.items():
        X_tr = X_train_sc if name == "Logistic Regression" else X_train
        X_te = X_test_sc if name == "Logistic Regression" else X_test

        cv_scores = cross_val_score(model, X_tr, y_train, cv=cv, scoring="roc_auc")
        model.fit(X_tr, y_train)
        y_pred = model.predict(X_te)
        y_prob = model.predict_proba(X_te)[:, 1]
        auc = roc_auc_score(y_test, y_prob)
        report = classification_report(y_test, y_pred, output_dict=True)

        results[name] = {
            "model": model,
            "auc": auc,
            "cv_auc_mean": cv_scores.mean(),
            "cv_auc_std": cv_scores.std(),
            "precision": report["1"]["precision"],
            "recall": report["1"]["recall"],
            "f1": report["1"]["f1-score"],
            "y_prob": y_prob,
            "y_pred": y_pred,
        }
        print(f"  {name:25s} | AUC: {auc:.4f} | CV AUC: {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}")

    # --- Plot 1: Model comparison bar chart ---
    fig, ax = plt.subplots(figsize=(9, 4))
    names = list(results.keys())
    aucs = [results[n]["cv_auc_mean"] for n in names]
    stds = [results[n]["cv_auc_std"] for n in names]
    colors = ["#3498DB", "#2ECC71", "#F39C12", "#E74C3C"]
    bars = ax.bar(names, aucs, yerr=stds, capsize=5, color=colors, alpha=0.85)
    ax.set_ylim(0.5, 1.0)
    ax.set_ylabel("CV ROC-AUC Score")
    ax.set_title("Model Comparison (5-Fold CV AUC)", fontsize=13, fontweight="bold")
    for bar, val in zip(bars, aucs):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
                f"{val:.3f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
    _save(fig, "08_model_comparison.png")

    # --- Best model ---
    best_name = max(results, key=lambda n: results[n]["auc"])
    best = results[best_name]
    print(f"\n  Best model: {best_name} (AUC={best['auc']:.4f})")

    # --- Plot 2: ROC curves ---
    fig, ax = plt.subplots(figsize=(7, 6))
    for name, res in results.items():
        fpr, tpr, _ = roc_curve(y_test, res["y_prob"])
        ax.plot(fpr, tpr, label=f"{name} (AUC={res['auc']:.3f})", linewidth=2)
    ax.plot([0, 1], [0, 1], "k--", linewidth=1)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curves - All Models", fontsize=13, fontweight="bold")
    ax.legend(loc="lower right", fontsize=9)
    _save(fig, "09_roc_curves.png")

    # --- Plot 3: Confusion matrix for best model ---
    fig, ax = plt.subplots(figsize=(5, 4))
    cm = confusion_matrix(y_test, best["y_pred"])
    disp = ConfusionMatrixDisplay(cm, display_labels=["Retained", "Churned"])
    disp.plot(ax=ax, colorbar=False, cmap="Blues")
    ax.set_title(f"Confusion Matrix - {best_name}", fontsize=12, fontweight="bold")
    _save(fig, "10_confusion_matrix.png")

    # --- Plot 4: Feature importance ---
    best_model = best["model"]
    if hasattr(best_model, "feature_importances_"):
        importances = best_model.feature_importances_
        fi_df = pd.DataFrame({"feature": feature_cols, "importance": importances})
        fi_df = fi_df.sort_values("importance", ascending=True).tail(12)

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.barh(fi_df["feature"], fi_df["importance"], color="#3498DB", alpha=0.85)
        ax.set_xlabel("Feature Importance")
        ax.set_title(f"Top Feature Importances - {best_name}", fontsize=13, fontweight="bold")
        _save(fig, "11_feature_importance.png")

        top_features = fi_df.sort_values("importance", ascending=False)["feature"].tolist()
    else:
        top_features = feature_cols

    print("[MODEL] Complete.\n")

    return {
        "best_model_name": best_name,
        "best_auc": best["auc"],
        "best_precision": best["precision"],
        "best_recall": best["recall"],
        "best_f1": best["f1"],
        "top_features": top_features[:5],
        "all_results": {n: {k: v for k, v in r.items() if k != "model" and k != "y_prob" and k != "y_pred"}
                        for n, r in results.items()},
    }
