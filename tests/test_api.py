"""Tests for API root and health. Full implementation in M8."""
import pytest
from fastapi.testclient import TestClient

from src.api.app import app

client = TestClient(app)


def test_root():
    """Root serves HTML demo."""
    r = client.get("/")
    assert r.status_code == 200
    assert "text/html" in r.headers.get("content-type", "")
    assert "Customer Churn Scoring API" in r.text


def test_meta():
    """Meta returns JSON for automation."""
    r = client.get("/meta")
    assert r.status_code == 200
    assert r.json().get("message")
    assert r.json().get("docs") == "/docs"


def test_health():
    """Health returns ok."""
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
