# VinDatathon 2026: BI-Driven Forecasting & Analytics

This repository contains the end-to-end data pipeline for **Task 2 (Dashboarding)** and **Task 3 (Forecasting)**. The solution strictly adheres to all constraints (no external data, no look-ahead bias, absolute reproducibility) and prioritizes "Business Truth"—identifying and exploiting structural anomalies in the data rather than blindly tuning black-box models.

---

## 📁 Repository Architecture

```text
VinDatathon/
├── data/
│   ├── raw/                              # Original Kaggle datasets
│   └── tableu/                           # Master dataset output (from Task 2)
├── outputs/
│   ├── dashboard/
│   │   └── output-*.pdf                  # Individual chart exports for LaTeX report
│   └── submissions/
│       ├── submission.csv                # ✅ WINNING SUBMISSION (v57 MP Blend — submit this)
│       ├── submission_lgb.csv            # Ablation: LightGBM standalone
│       ├── submission_xgb.csv            # Ablation: XGBoost standalone
│       ├── submission_hw.csv             # Ablation: Holt-Winters standalone
│       ├── submission_nnls_no_regime.csv # Ablation: NNLS blend (no biennial regime flag)
│       ├── shap_revenue_summary.png      # SHAP explainability — Revenue
│       ├── shap_cogs_summary.png         # SHAP explainability — COGS
│       ├── feature_importance.png        # LightGBM feature importance
│       └── baseline_vs_upgraded.png      # Visual comparison chart
├── 01_Task2_Visualizations_and _Analysis.ipynb # Task 2: Data prep & analysis pipeline
├── 02_Task3_Sales_Forecasting.ipynb            # ✅ Task 3: Production pipeline (use this)
├── baseline.ipynb                         # Organizing committee baseline
├── datathon_report.tex                    # NeurIPS-format academic report (LaTeX)
├── datathon_report.pdf                    # Compiled report (7 pages)
└── purpose.md                             # Competition constraints
```

---

## 🚀 How to Run

### Step 1 — Task 2: Data Preparation & Dashboarding

Run **`01_Task2_Visualizations_and _Analysis.ipynb`**.

- **What it does:** Ingests the 5 raw tables (`sales`, `items`, `returns`, `promos`, `web_traffic`). Merges them relationally. Calculates Delivery SLAs, RFM Customer Segmentation, and granular financial margins.
- **Output:** Writes `data/tableu/tableau_master_dataset.csv`.
- **Next Step:** Open Power BI / Tableau, connect to the CSV to build the visualizations.

### Step 2 — Task 3: Winning Forecast

Run **`02_Task3_Sales_Forecasting.ipynb`** ← **this is the canonical submission notebook**.

- **What it does:** Executes the full production ML pipeline deterministically.
- **Self-validates:** Automatically checks row count, column names, and date order against `sample_submission.csv` before saving.
- **Output:** Writes `outputs/submissions/submission.csv` (the v57 MP Blend forecast) and regenerates all SHAP / feature importance plots.

---

## 🧠 Task 3: Machine Learning Architecture

The forecasting pipeline is a **3-Tier Prescriptively-Calibrated Ensemble** — not a single black-box model.

### Tier 1 — Base Models

| Model | Role | Key Parameters |
|---|---|---|
| **LightGBM (Global)** | Non-linear local interactions | 63 leaves, MAE objective |
| **LightGBM (Q-Specialists × 4)** | Quarter-specific experts | 2× sample weight boost per quarter |
| **XGBoost** | Structural tree diversity | Depth 6, colsample 0.85 |
| **Ridge Regression** | Global linear trend anchor | α tuned on 2022 holdout |
| **Holt-Winters (Fallback)** | Deterministic seasonality fallback | Trained on 2018-2022 regime |

### Tier 2 — Ensemble Blending

- **Hand-tuned Blend:** `0.10 × Holt-Winters + 0.10 × HW-fallback + 0.80 × LGB blend` (primary)
- **NNLS Upgrade (optional):** Mathematically optimal Non-Negative Least Squares weights computed on 2022-H2 validation holdout. Available as `submission_upgraded.csv`.

### Tier 3 — Prescriptive Calibration (v57 MP Blend)

A deterministic post-processing override that anchors COGS predictions to historical quarterly margin ratios (`BETA = 0.30`), correcting ML hallucinations in Q3. This is the key differentiator of the **winning v57 submission** over the plain NNLS blend.

### Feature Engineering

- **Cyclicality:** Fourier terms (day-of-year, day-of-week, day-of-month)
- **Holidays:** Custom Lunar New Year (Tet) proximity mapping (−45 to +45 days)
- **Anomaly Anchors:** `liberation_decay` feature scales the post-Liberation Day consumer fatigue trend
- **Rolling Statistics:** 7-day to 90-day momentum lags (shift-windowed to prevent leakage)
- **Boolean Flags:** Major promotional events, odd/even year parity for biennial margin rule

### Reproducibility & Data Leakage Guarantee

The pipeline operates under a strict **Zero Future Leakage** guarantee:
- **Calendar & Promos:** All Fourier terms, holidays, and regime flags are inherently known in advance.
- **Rolling Statistics:** All momentum features (7-day to 90-day lags) are computed within a strict `shift(1)` window. This guarantees that historical target values are never contaminated by future observations during training.
- **Reproducibility:** The `prophet` package relies on L-BFGS optimization that can vary across OS/library versions. We intentionally disabled it (`HAS_PROPHET = False`) in the final pipeline. The notebook falls back deterministically to **Holt-Winters**, ensuring identical output across all environments.

### Cross-Validation Metrics

To validate performance without overfitting to the Kaggle Public Leaderboard, we implemented a robust **4-fold Walk-Forward Time-Series Split** on the training data (2014–2021). By progressively expanding the training window by one year per fold, we strictly simulated real-world deployment conditions. 

On the core LightGBM tier, this yielded:
- **Revenue MAE:** \$313,285 (Mean R² = 0.949)
- **COGS MAE:** \$302,330 (Mean R² = 0.929)

These scores confirm strong generalisation before the NNLS ensemble and $\beta$-calibration are even applied.

---

## 📊 Results

### Task 2 — Dashboarding Insights

Our EDA revealed 4 structural business anomalies across 6 dashboards:

| Dashboard | Key Finding | Prescriptive Action |
|---|---|---|
| **D1: Revenue & Profitability** | Streetwear = 80% volume but only 11.4% margin | Shift 15% procurement to GenZ (20.2% margin) |
| **D2: Customer Lifecycle** | 10,221 "At-Risk" Champions threatening $432.5M LTV | Deploy CRM win-back flows immediately |
| **D3: Marketing & Geography** | West Coast breaks national trend — Outdoor ≈ Streetwear | Geo-targeted Outdoor campaigns in West |
| **D4: Anomaly Detection** | Odd-year August: COGS = 1.4× Revenue → −40% margin | Order leaner in even years; OMS circuit-breaker |
| **D5: Product Analysis** | SaigonFlex UM-92 = $398.2M alone; GenZ return rate 5.72% | Auto-reorder heroes; quality-control alert at 15% return |
| **D6: Operations & Logistics** | 9.19% checkout cancellation = $1.515B lost revenue | 4-day SLA with 3PL; UX audit of checkout flow |

### Task 3 — Forecasting Performance

| Model | Kaggle Score | Avg Daily Revenue | Avg Daily COGS |
|---|---|---|---|
| Organizing Committee Baseline | 1,225,931 | $3,249,795 | $2,783,810 |
| Holt-Winters (standalone) | N/A | $3,058,695 | $2,770,203 |
| XGBoost (standalone) | N/A | $3,176,207 | $2,767,520 |
| LightGBM (standalone) | N/A | $3,370,260 | $2,890,597 |
| NNLS Ensemble (no regime flag) | N/A | $3,296,966 | $2,854,821 |
| **v57 Final Ensemble (Ours)** ✅ | **669,024** | **$4,182,326** | **$3,909,500** |

> **Note:** Ablation CSV files are in `outputs/submissions/`. Submit each file to Kaggle to obtain its public leaderboard score.
> To reproduce exact forecasts, run **`02_Task3_Sales_Forecasting.ipynb`**.

**SHAP Explainability:** `day_of_year` and `month` are the dominant features, with Liberation Day holiday flags producing the largest positive SHAP impulses. The COGS SHAP summary mirrors Revenue, confirming our pipeline correctly learned the locked cost-volume relationship.

---

## 📄 Academic Report

The full methodology is documented in **`datathon_report.pdf`** — a 7-page NeurIPS-format paper covering:
- EDA across all 6 dashboards with prescriptive insights
- 3-Tier ensemble architecture
- SHAP-based model explainability
- Results comparison table (Section 4)
- Full model ablation study (Appendix B)

To recompile: `pdflatex datathon_report.tex && pdflatex datathon_report.tex`

---

## 🔧 Requirements

```bash
pip install -r requirements.txt
```

Key dependencies: `lightgbm`, `xgboost`, `statsmodels` (Holt-Winters), `shap`, `scipy` (NNLS), `pandas`, `numpy`, `matplotlib`.
