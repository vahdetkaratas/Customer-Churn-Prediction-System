"""
CLI inference: predict churn for one customer from JSON file or stdin.
Run from project root: python -m src.cli.predict --input customer.json
Or: echo '{"tenure": 12, ...}' | python -m src.cli.predict
"""
import argparse
import json
import sys
from pathlib import Path

# Ensure project root is on path when run as __main__
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.api.service import predict_single_customer

# Default customer (ChurnRequest schema) for reference / missing keys
DEFAULT_CUSTOMER = {
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 12,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 79.85,
    "TotalCharges": 965.4,
}


def load_payload(stream_or_path):
    """Load one customer JSON from file path or stream (stdin)."""
    if stream_or_path is None or stream_or_path == "-":
        data = json.load(sys.stdin)
    else:
        path = Path(stream_or_path)
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {path}")
        with open(path) as f:
            data = json.load(f)
    # Merge with defaults so missing keys get sensible values
    payload = {**DEFAULT_CUSTOMER, **{k: v for k, v in data.items() if k in DEFAULT_CUSTOMER}}
    return payload


def main():
    parser = argparse.ArgumentParser(
        description="Predict churn for one customer (JSON input). Same schema as POST /predict."
    )
    parser.add_argument(
        "--input", "-i",
        default="-",
        help="Path to JSON file with one customer, or '-' for stdin (default: stdin)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output only JSON (churn_probability, prediction, risk_band, threshold_used)",
    )
    args = parser.parse_args()

    try:
        payload = load_payload(args.input)
        prob, pred, band, thresh = predict_single_customer(payload)
        out = {
            "churn_probability": prob,
            "prediction": pred,
            "risk_band": band,
            "threshold_used": thresh,
        }
        if args.json:
            print(json.dumps(out, indent=2))
        else:
            print(f"Churn probability: {prob:.4f}")
            print(f"Prediction:        {pred}")
            print(f"Risk band:        {band}")
            print(f"Threshold used:   {thresh}")
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
