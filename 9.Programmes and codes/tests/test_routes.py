"""
Integration tests for the API routes using httpx's TestClient.

TestClient wraps the FastAPI application and allows tests to make HTTP
requests directly to the application without a running server or network
overhead. Service-layer functions are mocked so these tests don't depend on
loading the real DistilBERT/GPT-2 models, keeping the suite fast.
"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@patch("app.routes.conversation.event_analyzer.extract_event_themes")
def test_analyze_event_returns_themes(mock_extract):
    mock_extract.return_value = ["AI", "healthcare"]

    response = client.post("/analyze-event", json={"description": "An AI in healthcare summit"})

    assert response.status_code == 200
    assert response.json() == {"themes": ["AI", "healthcare"]}


@patch("app.routes.conversation.fact_checker.fact_check")
def test_fact_check_endpoint(mock_fact_check):
    mock_fact_check.return_value = "A well-known machine learning concept."

    response = client.post("/fact-check", json={"query": "Zero-shot learning"})

    assert response.status_code == 200
    body = response.json()
    assert body["query"] == "Zero-shot learning"
    assert body["extract"] == "A well-known machine learning concept."


@patch("app.routes.conversation.history_logger.log_conversation")
@patch("app.routes.conversation.topic_generator.generate_topics")
@patch("app.routes.conversation.event_analyzer.extract_event_themes")
def test_generate_conversation_orchestrates_pipeline(mock_themes, mock_topics, mock_log):
    mock_themes.return_value = ["fintech", "blockchain"]
    mock_topics.return_value = ["Starter one", "Starter two", "Starter three"]

    response = client.post(
        "/generate-conversation",
        json={"description": "A fintech networking mixer", "interests": ["blockchain"]},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["themes"] == ["fintech", "blockchain"]
    assert body["suggestions"] == ["Starter one", "Starter two", "Starter three"]

    # Verifies the automatic side-effect logging described in the design.
    mock_log.assert_called_once()


@patch("app.routes.conversation.feedback_logger.log_feedback")
def test_feedback_endpoint(mock_log_feedback):
    response = client.post("/feedback", json={"suggestion": "What brings you here?", "action": "like"})

    assert response.status_code == 200
    assert response.json() == {"status": "recorded"}
    mock_log_feedback.assert_called_once_with("What brings you here?", "like")


def test_invalid_request_returns_422():
    """
    Sending an empty payload to an endpoint that requires a 'description'
    field should trigger FastAPI's automatic Pydantic validation, returning
    422 Unprocessable Entity without any custom validation code.
    """
    response = client.post("/analyze-event", json={})
    assert response.status_code == 422


def test_invalid_feedback_action_returns_422():
    response = client.post("/feedback", json={"suggestion": "Test suggestion", "action": "meh"})
    assert response.status_code == 422
