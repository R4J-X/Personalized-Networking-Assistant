"""
Unit tests for the fact checker service.

External network calls are mocked with unittest.mock so tests run reliably
without network connectivity, including in CI/CD pipelines. Covers the
happy path, the missing-data path, and the network-error path.
"""

from unittest.mock import MagicMock, patch

import requests

from app.services.fact_checker import FALLBACK_MESSAGE, fact_check


@patch("app.services.fact_checker.requests.get")
def test_fact_check_happy_path(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"extract": "Zero-shot learning is a machine learning problem setup."}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fact_check("Zero-shot learning")

    assert result == "Zero-shot learning is a machine learning problem setup."


@patch("app.services.fact_checker.requests.get")
def test_fact_check_missing_extract_returns_fallback(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fact_check("Some obscure nonexistent topic")

    assert result == FALLBACK_MESSAGE


@patch("app.services.fact_checker.requests.get")
def test_fact_check_network_error_returns_fallback(mock_get):
    mock_get.side_effect = requests.ConnectionError("network unreachable")

    result = fact_check("AI")

    assert result == FALLBACK_MESSAGE


@patch("app.services.fact_checker.requests.get")
def test_fact_check_timeout_returns_fallback(mock_get):
    mock_get.side_effect = requests.Timeout("request timed out")

    result = fact_check("Distributed systems")

    assert result == FALLBACK_MESSAGE
