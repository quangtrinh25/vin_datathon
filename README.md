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
│   │   ├── business_insights_report.md   # Task 2 executive pitch scripts
│   │   └── output-*.pdf                  # Individual chart exports for LaTeX report
│   └── submissions/
│       ├── submission.csv                # ✅ WINNING SUBMISSION (v57 MP Blend)
│       ├── submission_v57_mp_blend30.csv # Identical to submission.csv
│       ├── submission_upgraded.csv       # Experimental NNLS blend
│       ├── submission_nnls.csv           # Pure NNLS baseline reference
│       ├── shap_revenue_summary.png      # SHAP explainability — Revenue
│       ├── shap_cogs_summary.png         # SHAP explainability — COGS
│       ├── feature_importance.png        # LightGBM feature importance
│       └── baseline_vs_upgraded.png      # Visual comparison chart
├── 01_Task2_Prepare_Dashboard_Data.ipynb # Task 2: Data prep pipeline
├── 02_Task3_Final_Forecasting.ipynb      # Task 3: Full development history
├── 03_Task3_Winning_Model.ipynb          # ✅ Task 3: Production pipeline (use this)
├── baseline.ipynb                         # Organizing committee baseline
├── datathon_report.tex                    # NeurIPS-format academic report (LaTeX)
├── datathon_report.pdf                    # Compiled report (7 pages)
└── purpose.md                             # Competition constraints
```

---

## 🚀 How to Run

### Step 1 — Task 2: Data Preparation & Dashboarding

Run **`01_Task2_Prepare_Dashboard_Data.ipynb`**.

- **What it does:** Ingests the 5 raw tables (`sales`, `items`, `returns`, `promos`, `web_traffic`). Merges them relationally. Calculates Delivery SLAs, RFM Customer Segmentation, and granular financial margins.
- **Output:** Writes `data/tableu/tableau_master_dataset.csv`.
- **Next Step:** Open Power BI / Tableau, connect to the CSV, and follow `outputs/dashboard/business_insights_report.md` to build the visualizations.

### Step 2 — Task 3: Winning Forecast

Run **`03_Task3_Winning_Model.ipynb`** ← **this is the canonical submission notebook**.

- **What it does:** Executes the full production ML pipeline deterministically.
- **Self-validates:** Automatically checks row count, column names, and date order against `sample_submission.csv` before saving.
- **Output:** Writes `outputs/submissions/submission.csv` (the v57 MP Blend forecast) and regenerates all SHAP / feature importance plots.

> `02_Task3_Final_Forecasting.ipynb` is kept for full development history and intermediate experiment reference only.

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

### Reproducibility Guarantee

The `prophet` package relies on L-BFGS optimization that can vary across OS/library versions. We intentionally disabled it (`HAS_PROPHET = False`) in the final pipeline. The notebook falls back deterministically to **Holt-Winters**, ensuring identical output across all environments.

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

| Model | Evaluate Score | Forecasted Revenue | Forecasted COGS |
|---|---|---|---|
| Organizing Committee Baseline | [TBD] | $3,249,795 /day | $2,783,810 /day |
| Holt-Winters Standalone | [TBD] | $3,058,695 /day | $2,770,203 /day |
| XGBoost Standalone | [TBD] | $3,176,207 /day | $2,767,520 /day |
| LightGBM Standalone | [TBD] | $3,266,419 /day | $2,842,544 /day |
| NNLS Upgraded Ensemble | [TBD] | $4,156,264 /day | $3,900,822 /day |
| **v57 MP Blend (Final)** ✅ | **[TBD]** | **$4,182,326 /day** | **$3,909,500 /day** |

> **[TBD]** fields will be updated with official Kaggle leaderboard scores after final submission.

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
