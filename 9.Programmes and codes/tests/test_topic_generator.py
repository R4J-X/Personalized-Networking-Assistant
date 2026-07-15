"""
Unit tests for the topic generator service.

Validate structure rather than specific content, since GPT-2's exact output
is non-deterministic in wording (even with a fixed seed across environments).
"""

from app.services.topic_generator import NUM_SUGGESTIONS, generate_topics


def test_generate_returns_list_of_strings():
    suggestions = generate_topics(["AI", "healthcare"], ["machine learning"])
    assert isinstance(suggestions, list)
    assert all(isinstance(s, str) for s in suggestions)


def test_generate_returns_expected_count():
    suggestions = generate_topics(["blockchain"], ["fintech"])
    assert len(suggestions) == NUM_SUGGESTIONS


def test_generate_non_empty_strings():
    """
    Verifies that bullet-marker/whitespace cleanup does not produce empty
    strings, which would render as blank bullet points in the UI.
    """
    suggestions = generate_topics(["sustainability"], ["renewable energy"])
    for suggestion in suggestions:
        assert suggestion.strip() != ""


def test_generate_handles_empty_themes_and_interests():
    suggestions = generate_topics([], [])
    assert len(suggestions) == NUM_SUGGESTIONS
    assert all(s.strip() for s in suggestions)
