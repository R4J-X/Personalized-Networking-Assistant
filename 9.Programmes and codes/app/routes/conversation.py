"""
Conversation Routes
----------------------
Wires the service modules together via FastAPI's APIRouter. This routing
layer is the integration point between the HTTP interface and the business
logic layers, handling request deserialization, service orchestration, and
response serialization.
"""

from fastapi import APIRouter

from app.models.schemas import (
    ConversationRequest,
    ConversationResponse,
    EventAnalysisRequest,
    EventAnalysisResponse,
    FactCheckRequest,
    FactCheckResponse,
    FeedbackRequest,
)
from app.services import event_analyzer, fact_checker, feedback_logger, history_logger, topic_generator

router = APIRouter()


@router.post("/analyze-event", response_model=EventAnalysisResponse)
def analyze_event(request: EventAnalysisRequest) -> EventAnalysisResponse:
    """Standalone theme extraction -- useful for debugging or custom integrations."""
    themes = event_analyzer.extract_event_themes(request.description, request.candidate_labels)
    return EventAnalysisResponse(themes=themes)


@router.post("/fact-check", response_model=FactCheckResponse)
def check_fact(request: FactCheckRequest) -> FactCheckResponse:
    """Wraps the Wikipedia fact-checking service in a type-safe API contract."""
    extract = fact_checker.fact_check(request.query)
    return FactCheckResponse(query=request.query, extract=extract)


@router.post("/generate-conversation", response_model=ConversationResponse)
def generate_conversation(request: ConversationRequest) -> ConversationResponse:
    """
    The primary application endpoint. Orchestrates the full pipeline:
    extracts themes, generates conversation starters, and automatically
    persists the interaction to history as a side effect -- the frontend
    does not need to know about history logging.
    """
    themes = event_analyzer.extract_event_themes(request.description)
    suggestions = topic_generator.generate_topics(themes, request.interests)

    history_logger.log_conversation(
        {
            "description": request.description,
            "interests": request.interests,
            "themes": themes,
            "suggestions": suggestions,
        }
    )

    return ConversationResponse(themes=themes, suggestions=suggestions)


@router.post("/feedback")
def submit_feedback(request: FeedbackRequest) -> dict:
    """Persists a like/dislike rating for a specific generated suggestion."""
    feedback_logger.log_feedback(request.suggestion, request.action)
    return {"status": "recorded"}
