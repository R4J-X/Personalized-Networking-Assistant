"""
Unit tests for the event analyzer service.

These tests validate the function's contract without asserting specific
themes (which would be brittle since output depends on model weights).
Instead they test structural properties: list output, at most 3 items,
items drawn from the candidate set, and at least one result returned.
"""

from app.services.event_analyzer import DEFAULT_CANDIDATE_LABELS, TOP_K, extract_event_themes


def test_returns_a_list():
    themes = extract_event_themes("A conference about artificial intelligence in healthcare.")
    assert isinstance(themes, list)


def test_returns_at_most_top_k_items():
    themes = extract_event_themes("A large multi-track technology and business summit.")
    assert len(themes) <= TOP_K


def test_returns_at_least_one_result():
    themes = extract_event_themes("A meetup for people who love building startups.")
    assert len(themes) >= 1


def test_themes_are_drawn_from_default_candidate_labels():
    themes = extract_event_themes("A hackathon focused on fintech and blockchain innovation.")
    for theme in themes:
        assert theme in DEFAULT_CANDIDATE_LABELS


def test_accepts_custom_candidate_labels():
    custom_labels = ["cooking", "travel", "gardening"]
    themes = extract_event_themes("A community potluck and recipe swap.", candidate_labels=custom_labels)
    assert all(theme in custom_labels for theme in themes)
