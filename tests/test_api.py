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


def test_root_sidebar_recruiter_host():
    """Non-labs host keeps recruiter sidebar copy (strip commercial variant)."""
    r = client.get("/", headers={"host": "churn-api.vahdetkaratas.com"})
    assert r.status_code == 200
    body = r.text
    assert 'class="api-host-recruiter"' in body
    assert "For hiring review" in body
    assert "For client evaluation" not in body


def test_root_sidebar_labs_host():
    """*vahdetlabs* API host keeps commercial sidebar (same framing as churn.vahdetlabs.com)."""
    r = client.get("/", headers={"host": "churn-api.vahdetlabs.com"})
    assert r.status_code == 200
    body = r.text
    assert 'class="api-host-labs"' in body
    assert "For client evaluation" in body
    assert "For hiring review" not in body


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
