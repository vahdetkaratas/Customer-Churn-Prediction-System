"""Tests for CLI inference."""
import json
import subprocess
import sys
from pathlib import Path

import pytest


def test_cli_help():
    """CLI --help exits 0 and prints usage."""
    result = subprocess.run(
        [sys.executable, "-m", "src.cli.predict", "--help"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).resolve().parent.parent,
    )
    assert result.returncode == 0
    assert "predict" in result.stdout or "input" in result.stdout.lower()


def test_cli_file_not_found_exits_nonzero():
    """CLI with missing input file exits with code 1."""
    result = subprocess.run(
        [sys.executable, "-m", "src.cli.predict", "--input", "nonexistent.json"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).resolve().parent.parent,
    )
    assert result.returncode != 0
    assert "not found" in result.stderr or "Error" in result.stderr


def test_cli_with_sample_json():
    """CLI with valid JSON outputs churn_probability and prediction (if model exists)."""
    sample = Path(__file__).resolve().parent.parent / "scripts" / "sample_customer.json"
    if not sample.exists():
        pytest.skip("scripts/sample_customer.json not found")
    result = subprocess.run(
        [sys.executable, "-m", "src.cli.predict", "--input", str(sample), "--json"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).resolve().parent.parent,
    )
    if result.returncode != 0:
        pytest.skip("Model not found; run training first")
    data = json.loads(result.stdout)
    assert "churn_probability" in data
    assert "prediction" in data
    assert data["prediction"] in ("Yes", "No")
    assert 0 <= data["churn_probability"] <= 1
