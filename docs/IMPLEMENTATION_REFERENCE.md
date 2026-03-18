# Implementation reference

Concrete values, schemas, and layout for this repo. **Doc index:** root [README.md](../README.md). **Canonical repo:** [github.com/vahdetkaratas/Customer-Churn-Prediction-System](https://github.com/vahdetkaratas/Customer-Churn-Prediction-System).

## 1. Repository layout

```
customer-churn-prediction-system/
├── README.md
├── requirements.txt
├── Makefile
├── config/config.yaml
├── data/raw/.gitkeep                    # add telco_customer_churn.csv locally (gitignored)
├── notebooks/01_eda.ipynb … 04_error_analysis.ipynb
├── src/
│   ├── config_loader.py
│   ├── data/load_data.py, preprocess.py
│   ├── features/build_features.py
│   ├── models/*.py
│   ├── pipeline/training_pipeline.py
│   ├── api/app.py, schemas.py, service.py
│   └── cli/predict.py
├── scripts/generate_figures.py, sample_customer.json
├── vercel_demo/
├── artifacts/models/                    # churn_model.joblib after train (gitignored)
├── reports/
│   ├── metrics/*.json, *.csv             # training outputs
│   └── figures/*.png                     # from generate_figures (gitignored)
└── tests/
```

**Figures:** `python scripts/generate_figures.py`  
**CLI:** `python -m src.cli.predict --input scripts/sample_customer.json` (or `-i`)

## 1b. Dataset

| | |
|--|--|
| Source | [Kaggle Telco Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) |
| Save as | `data/raw/telco_customer_churn.csv` |

## 2. Config (`config/config.yaml`)

Keys under `paths` (all overridable):

- `raw_data`, `model_output`, `metrics_output`, `threshold_table`, `threshold_summary`, `model_comparison`, `error_analysis_detailed`

`data.target_column`, `data.test_size`, `random_state`, `model.default_threshold`.

## 3. Dependencies

See `requirements.txt`. Vercel demo subset: fastapi, uvicorn, pydantic, pandas, numpy, scikit-learn, joblib.

## 3b. Two-repo option (Vercel)

| | |
|--|--|
| Dev repo | Full project |
| Demo repo | Copy `vercel_demo/` + `model/churn_model.joblib` (+ optional `threshold_summary.json`) |

## 4. API schemas

**POST /predict** body = fields in `ChurnRequest` (gender, SeniorCitizen, Partner, … MonthlyCharges, TotalCharges).  
**Response:** `churn_probability`, `prediction` (`Yes`/`No`), `risk_band` (`high`/`medium`/`low`), `threshold_used`.

Risk bands: ≥0.75 high; ≥0.45 medium; else low.

## 5. Models

| Model | Settings |
|-------|----------|
| LogisticRegression | max_iter=1000, class_weight=balanced, random_state=42 |
| RandomForestClassifier | n_estimators=200, class_weight=balanced, random_state=42 |
| GradientBoostingClassifier | random_state=42 |

Best model by **ROC-AUC** on hold-out test set.

## 6. Threshold sweep

Thresholds 0.10–0.90 step 0.05; pick best **F1** → `reports/metrics/threshold_summary.json`.

## 7. Feature engineering

`TotalCharges` numeric; `num_active_services` (count of Yes in eight service columns); `tenure_group` from `pd.cut` on tenure.

## 8. Inference rule

Always run **`build_features`** on the request row before `pipeline.predict_proba` (same as training).

## 9. Makefile targets

`train`, `run-api`, `test`, `predict` (CLI sample).

---

*Paths default to `reports/metrics/` for all training tables/JSON; model artifact under `artifacts/models/`.*
