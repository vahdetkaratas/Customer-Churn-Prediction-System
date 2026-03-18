"""Tests for API root and health. Full implementation in M8."""
import pytest
from fastapi.testclient import TestClient

from src.api.app import app

client = TestClient(app)


def test_root():
    """Root returns message."""
    r = client.get("/")
    assert r.status_code == 200
    assert "message" in r.json()


def test_health():
    """Health returns ok."""
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
