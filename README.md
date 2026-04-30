# Structural Anomaly-Driven Retail Revenue Forecasting: A Biennial Supply Chain Smoothing Approach

This repository contains the end-to-end Exploratory Data Analysis (EDA) and forecasting pipeline for a Vietnamese fashion retailer, predicting daily Revenue and COGS over a 548-day horizon. By surfacing two structural anomalies—a biennial COGS spike driven by procurement rigidity and $1.5B in checkout abandonment—we engineer domain-specific features that a leakage-free ensemble model exploits directly.

The result is a Kaggle public-leaderboard Score of 669,024, a 45.4% improvement over the organiser baseline. SHAP attribution confirms that the gain originates from the engineered domain features rather than raw model capacity.

---

## Repository Architecture

```text
VinDatathon/
├── data/
│   ├── raw/                              # Original Kaggle datasets
│   └── tableu/                           # Master dataset output (from Task 2)
├── outputs/
│   ├── dashboard/
│   │   └── output-*.pdf                  # Individual chart exports for LaTeX report
│   └── submissions/
│       ├── submission.csv                # FINAL SUBMISSION (v57 MP Blend)
│       ├── submission_lgb.csv            # Ablation: LightGBM standalone
│       ├── submission_xgb.csv            # Ablation: XGBoost standalone
│       ├── submission_hw.csv             # Ablation: Holt-Winters standalone
│       ├── submission_nnls_no_regime.csv # Ablation: NNLS blend (no biennial regime flag)
│       ├── shap_revenue_summary.png      # SHAP explainability — Revenue
│       ├── shap_cogs_summary.png         # SHAP explainability — COGS
│       ├── feature_importance.png        # LightGBM feature importance
│       └── baseline_vs_upgraded.png      # Visual comparison chart
├── 01_Task2_Visualizations_and_Analysis.ipynb # Task 2: Data prep & analysis pipeline
├── 02_Task3_Sales_Forecasting.ipynb            # Task 3: Production pipeline
├── baseline.ipynb                         # Organizing committee baseline
├── datathon_report.tex                    # NeurIPS-format academic report (LaTeX)
├── datathon_report.pdf                    # Compiled report
└── purpose.md                             # Competition constraints
```

---

## How to Run

### Step 1 — Task 2: Data Preparation & Dashboarding

Run **01_Task2_Visualizations_and_Analysis.ipynb**.

- **Function:** Ingests raw tables (sales, items, returns, promos, web_traffic), performs relational merges, and calculates Delivery SLAs, **RFM Customer Segmentation** (Recency, Frequency, Monetary), and granular financial margins.
- **Output:** Writes data/tableu/tableau_master_dataset.csv for use in BI tools.

### Step 2 — Task 3: Forecasting Pipeline

Run **02_Task3_Sales_Forecasting.ipynb**.

- **Function:** Executes the full production ML pipeline deterministically.
- **Validation:** Automatically checks row count, column names, and date order against sample_submission.csv.
- **Output:** Writes outputs/submissions/submission.csv (the v57 MP Blend forecast) and regenerates all SHAP / feature importance plots.

---

## Machine Learning Architecture

The forecasting pipeline is a 3-Tier Prescriptively-Calibrated Ensemble designed to exploit structural signals identified during EDA.

### Tier 1 — Statistical Anchor
Holt-Winters triple exponential smoothing with additive trend and additive seasonality (period = 365 days). This serves as a structural prior that regularises the gradient-boosted components against out-of-distribution extrapolation.

### Tier 2 — Quarterly LightGBM Specialists
Four LightGBM models trained on the full history, each with double sample weight on its target quarter to capture within-quarter heterogeneity.

### Tier 3 — Blending and Calibration
XGBoost and LightGBM predictions are combined via **Non-Negative Least Squares (NNLS)**, a form of **stacked generalization** [Wolpert, 1992]. A prescriptive Q3 override anchors odd-year August COGS to historical regime values, correcting the systematic upward bias during biennial liquidation periods.

### Feature Engineering (Zero Leakage)
- **Calendar:** Day, day-of-week, month, quarter, year.
- **Fourier Terms:** Cyclic encoding for annual (k=4) and weekly (k=2) patterns to learn asymmetric demand gradients.
- **Holiday Proximity:** Days-to/from Liberation Day and major holidays.
- **Biennial Regime:** A binary indicator for August of odd-numbered years, directly operationalising the Dashboard 4 anomaly.
- **Zero Future Leakage:** All rolling features use `shift(1)` to ensure no test-set data contaminates the training window.

---

## Results and Insights

### Business Intelligence Findings

Our EDA revealed critical structural inefficiencies quantified as follows:

| Focus Area | Key Finding | Quantified Impact |
|---|---|---|
| **Revenue & Profit** | Streetwear (80% vol) has 11.4% margin vs Gen-Z (20.2%). | $296M annual margin upside via mix shift. |
| **Customer Lifecycle** | Champions (<8% base) drive 63.8% of total revenue. | $432.5M top-line uplift from retention recovery. |
| **Geography** | West Coast inverts national trend (Outdoor ≈ Streetwear). | $18–30M annual savings via regional forecasting. |
| **Biennial Anomaly** | COGS = 1.4x Revenue every August of odd years. | $350–400M margin erosion per cycle. |
| **Returns** | Gen-Z Activewear return rate peaks at 5.72%. | $12M annual recovery via fit-matching tools. |
| **Logistics** | 9.19% checkout cancellation rate. | $1.515B in unrealised revenue over 10 years. |

### Forecasting Performance

The final ensemble achieves a Kaggle score of 669,024, a 45.4% reduction from the organiser baseline.

| Strategy | Kaggle MAE | Avg. Daily Rev. | Avg. Daily COGS |
|---|---|---|---|
| Organiser Baseline | 1,225,931 | $3,249,795 | $2,783,810 |
| Holt-Winters only | 1,766,236 | $3,058,695 | $2,770,203 |
| LightGBM only | 1,146,664 | $3,370,260 | $2,890,597 |
| NNLS (no regime flag) | 1,201,739 | $3,296,966 | $2,854,821 |
| **Final v57 Ensemble** | **669,024** | **$4,182,326** | **$3,909,500** |

**Ablation Note:** Removing the biennial regime flag raises MAE by 532,715 points (+79.5%), isolating it as the single largest incremental contributor.

---

## Academic Report

The full methodology is documented in **datathon_report.pdf**, a NeurIPS-format paper grounded in academic frameworks:
- **RFM Customer Lifecycle Analytics** [Hughes, 1994].
- **3-Tier Stacked Generalization Ensemble** [Wolpert, 1992].
- **Industry-Standard Checkout Abandonment Analysis** [Kukar-Kinney, 2010].
- **SHAP-based Model Explainability** [Lundberg, 2017].

---

## Requirements

```bash
pip install lightgbm xgboost statsmodels shap scipy pandas numpy matplotlib
```

Source code and results available at: [https://github.com/quangtrinh25/vin_datathon](https://github.com/quangtrinh25/vin_datathon)
