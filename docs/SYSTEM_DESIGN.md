# ML System Design

Technical design for the Customer Churn Prediction System. This document defines the end-to-end ML pipeline and removes ambiguities. It assumes a portfolio ML system, not a production enterprise platform.

---

## 1. End-to-End Pipeline Overview

```
Raw CSV (Telco Customer Churn)
        │
        ▼
┌───────────────────┐
│ Load Data         │  (optional: validate columns)
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Feature Engineering│  (num_active_services, tenure_group, TotalCharges fix)
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Train/Test Split  │  (80/20, stratified)
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Preprocessing      │  (imputation, encoding, scaling)
│ + Model Training   │  (LogReg, RF, GB — compare, select best)
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Threshold Analysis │  (evaluate multiple thresholds, select by F1)
│ Error Analysis     │  (segment breakdown)
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Save Artifact      │  (full Pipeline as joblib)
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ FastAPI Inference  │  (load model once, predict on request)
└───────────────────┘
```

**Training:** Local only. Run `python -m src.pipeline.training_pipeline`.

**Inference:** FastAPI loads the saved pipeline once at startup. Each request passes customer data → pipeline predicts → returns probability, prediction, risk band.

---

## 2. Dataset

| Attribute | Value |
|-----------|-------|
| **Name** | Telco Customer Churn Dataset |
| **Source** | Public dataset (e.g. Kaggle, IBM sample data) |
| **Target variable** | `Churn` — binary (`Yes` / `No`), mapped to 1 / 0 |
| **Class imbalance** | Yes. Churn rate typically ~20%. Use `class_weight="balanced"` in models. |

### Important Features

| Column | Type | Notes |
|--------|------|-------|
| customerID | identifier | Dropped before modeling (not a feature) |
| gender | categorical | |
| SeniorCitizen | numeric | 0/1 |
| Partner | categorical | Yes/No |
| Dependents | categorical | Yes/No |
| tenure | numeric | Months with company |
| PhoneService | categorical | Yes/No |
| MultipleLines | categorical | Yes/No/No phone service |
| InternetService | categorical | DSL/Fiber optic/No |
| OnlineSecurity | categorical | Yes/No/No internet service |
| OnlineBackup | categorical | Yes/No/No internet service |
| DeviceProtection | categorical | Yes/No/No internet service |
| TechSupport | categorical | Yes/No/No internet service |
| StreamingTV | categorical | Yes/No/No internet service |
| StreamingMovies | categorical | Yes/No/No internet service |
| Contract | categorical | Month-to-month/One year/Two year |
| PaperlessBilling | categorical | Yes/No |
| PaymentMethod | categorical | Electronic check/Mailed check/Bank transfer/Credit card |
| MonthlyCharges | numeric | |
| TotalCharges | numeric | May arrive as string; convert to numeric, coerce errors |

---

## 3. Data Processing

### Cleaning Steps

1. **Drop `customerID`** — identifier, not a feature.
2. **Convert `TotalCharges`** — `pd.to_numeric(..., errors="coerce")`; handle empty strings.
3. **Target encoding** — `Churn`: `Yes` → 1, `No` → 0.

### Missing Values

| Column type | Strategy |
|-------------|----------|
| Numeric | `SimpleImputer(strategy="median")` |
| Categorical | `SimpleImputer(strategy="most_frequent")` |

### Categorical Encoding

- **Method:** `OneHotEncoder(handle_unknown="ignore")`
- **Reason:** Avoids retraining when new categories appear at inference; unknown categories are ignored.

### Numeric Scaling

- **Method:** `StandardScaler()` (zero mean, unit variance)
- **Reason:** Logistic Regression benefits from scaled features; tree models are robust but scaling keeps behavior consistent.

### Preprocessor Structure

```text
ColumnTransformer
├── num:  [numeric columns]  → SimpleImputer(median) → StandardScaler
└── cat:  [categorical]      → SimpleImputer(most_frequent) → OneHotEncoder(handle_unknown="ignore")
```

---

## 4. Feature Engineering

| Feature | Definition | Why |
|---------|------------|-----|
| **num_active_services** | Count of Yes across PhoneService, MultipleLines, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies (No internet/phone service → 0) | Captures service usage intensity. |
| **tenure_group** | `pd.cut(tenure, bins=[-1, 12, 24, 48, 72], labels=["0-12","13-24","25-48","49-72"])` | Groups tenure into meaningful buckets. |
| **TotalCharges (numeric)** | `pd.to_numeric(TotalCharges, errors="coerce")` | Ensures numeric type for modeling. |

Feature engineering runs **before** train/test split and **before** the sklearn preprocessor. The preprocessor is built on the feature-engineered data.

---

## 5. Train / Validation Split

| Attribute | Value |
|-----------|-------|
| **Strategy** | Single train/test split (no separate validation set) |
| **Split ratio** | 80% train, 20% test |
| **Stratification** | `stratify=y` to preserve churn proportion |
| **Random seed** | `random_state=42` |
| **Leakage check** | Ensure no future/target-derived info leaks into features |

No explicit validation set. Model comparison and threshold selection use the test set. For a portfolio project this is acceptable; in production, a held-out validation set would be used for threshold tuning.

---

## 6. Modeling Strategy

### Models to Train

| Model | Role | Config |
|-------|------|--------|
| Logistic Regression | Baseline | `max_iter=1000`, `class_weight="balanced"`, `random_state=42` |
| Random Forest | Tree baseline | `n_estimators=200`, `class_weight="balanced"`, `random_state=42` |
| Gradient Boosting | Stronger model | `random_state=42` (default params) |

### Baseline Model

Logistic Regression is the baseline. It is interpretable, fast, and suitable for deployment (small artifact).

### Comparison Strategy

1. Train all three with the same preprocessor.
2. Evaluate on the test set.
3. Use **ROC-AUC** as the primary metric for selection.
4. Save the best model (by ROC-AUC) as the deployment artifact.

---

## 7. Evaluation Metrics

| Metric | Role | Why |
|--------|------|-----|
| **ROC-AUC** | Primary (model selection) | Threshold-independent; good for imbalanced data. |
| **Precision** | Secondary | Cost of false positives (unnecessary retention spend). |
| **Recall** | Secondary | Cost of false negatives (missed churners). |
| **F1** | Secondary | Balance of precision and recall. |
| **Accuracy** | Secondary | Less informative with imbalance. |
| **Confusion matrix** | Diagnostic | Shows error distribution. |

Churn is imbalanced; ROC-AUC and precision/recall are more informative than accuracy.

---

## 8. Threshold Selection

### How Threshold Is Chosen

1. Evaluate thresholds from 0.10 to 0.90 in steps of 0.05.
2. For each threshold, compute precision, recall, F1, and number of predicted positives.
3. Select the threshold that maximizes **F1** on the test set.
4. Default inference threshold: **0.55** (can be overridden by threshold analysis output).

### Trade-off Analysis

- **Higher threshold** → fewer customers flagged, higher precision, lower recall.
- **Lower threshold** → more customers flagged, higher recall, lower precision.
- **F1** balances both; suitable when no explicit cost model exists.
- Future: budget-constrained threshold (e.g. top 20% of customers) can replace F1-based selection.

### Risk Bands (Inference Only)

| Probability | Risk band |
|-------------|-----------|
| ≥ 0.75 | high |
| 0.45–0.75 | medium |
| < 0.45 | low |

---

## 9. Model Artifact

### Pipeline Structure

```text
sklearn.pipeline.Pipeline
├── step "preprocessor": ColumnTransformer (imputation + encoding + scaling)
└── step "model": Classifier (LogReg / RF / GB)
```

### What Is Saved

- **Single file:** `artifacts/models/churn_model.joblib`
- **Content:** Full pipeline (preprocessor + model)
- **Reason:** Inference uses the same transformations as training; no separate preprocessing code.

### Serialization

- **Method:** `joblib.dump(pipeline, path)`
- **Load:** `joblib.load(path)`

---

## 10. Inference Flow

### How the API Loads the Model

1. On first request (or at startup), load `churn_model.joblib` from disk.
2. Cache in memory (e.g. module-level variable) to avoid reloading per request.
3. If the file is missing, raise a clear error.

### How Requests Are Processed

1. Receive JSON body with customer fields (Pydantic `ChurnRequest`).
2. Convert to a single-row DataFrame.
3. **Apply feature engineering** (`build_features`): add `num_active_services`, `tenure_group`, fix `TotalCharges`. The pipeline expects the same columns as at training time; these features are computed outside the pipeline.
4. Pass the DataFrame to `pipeline.predict_proba()` — the pipeline applies imputation, encoding, and scaling internally.
5. Extract `P(churn=1)` from the probability array.

### How Predictions Are Returned

1. **churn_probability:** `float`, rounded to 4 decimals.
2. **prediction:** `"Yes"` if probability ≥ threshold, else `"No"`.
3. **risk_band:** `"high"` (≥0.75), `"medium"` (0.45–0.75), `"low"` (<0.45).
4. **threshold_used:** The threshold used for the binary prediction (e.g. 0.55).

**Note:** The pipeline handles imputation, encoding, and scaling. Feature engineering (`build_features`) must run in the API before passing data to the pipeline, since those features are computed outside the sklearn pipeline.

---

## 11. Potential Technical Risks

| Risk | Mitigation |
|------|------------|
| **Data leakage** | Drop `customerID`; avoid using future information; ensure features are available at prediction time. |
| **Overfitting** | Use a single train/test split; avoid heavy hyperparameter tuning; prefer simpler models if metrics are similar. |
| **Class imbalance** | Use `class_weight="balanced"`; evaluate with ROC-AUC and precision/recall, not only accuracy. |
| **Dataset limitations** | Static dataset; no drift handling. Acceptable for a portfolio project. Document in README. |
| **TotalCharges edge cases** | Empty string or invalid values → coerce to NaN, then impute. |
| **Categorical unknowns at inference** | `OneHotEncoder(handle_unknown="ignore")` handles new categories. |
| **Model size for deployment** | If Gradient Boosting artifact is too large for Vercel (500 MB limit), fall back to Logistic Regression or a smaller tree model. |

---

*Implementation guidance for this repository; not an enterprise production specification.*
