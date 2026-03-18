# Overview

**Source code:** [Customer-Churn-Prediction-System](https://github.com/vahdetkaratas/Customer-Churn-Prediction-System) on GitHub.

## Problem

Subscription businesses lose revenue when customers churn. Retention budgets are limited, so teams need **ranked churn risk** to focus outreach on high-probability leavers.

## What this repository provides

| Layer | Description |
|-------|-------------|
| **Training** | Single command: load Telco data → feature engineering → compare Logistic Regression, Random Forest, Gradient Boosting → select best by ROC-AUC → F1-optimal classification threshold → error analysis by contract and tenure. |
| **Artifact** | One `joblib` file: sklearn `ColumnTransformer` + classifier (same transforms at inference). |
| **Inference** | FastAPI (`POST /predict`) and optional CLI; probability, binary label, and risk band. |
| **Quality** | pytest suite, reproducible config via `config/config.yaml`. |

## Dataset

IBM Telco Customer Churn ([Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)) — tabular, binary churn label.

## In scope

- EDA notebooks, modular `src/` pipeline, model comparison, threshold sweep, segment-level error exports under `reports/metrics/`.

## Out of scope

- Automated retraining, drift detection, production monitoring, cost-optimized campaign budgeting (threshold is metric-driven, not business-cost-driven).

## Live demo (optional)

The `vercel_demo/` directory is a minimal inference + UI bundle for deployment to Vercel; train locally, copy the model into `vercel_demo/model/`. See `vercel_demo/README.md`.
