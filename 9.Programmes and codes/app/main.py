"""
Application Entry Point
--------------------------
Intentionally minimal, following the principle of doing one thing well.
Creates the FastAPI application instance, registers the conversation router,
and defines a health-check endpoint used by load balancers, monitoring
systems, and developers to verify the API is running and reachable.
"""

from fastapi import FastAPI

from app.routes.conversation import router as conversation_router

app = FastAPI(
    title="Personalized Networking Assistant API",
    description="AI-powered event theme analysis, conversation-starter generation, and Wikipedia fact-checking.",
    version="1.0.0",
)

app.include_router(conversation_router)


@app.get("/")
def health_check() -> dict:
    """Simple health-check endpoint."""
    return {"status": "ok", "service": "Personalized Networking Assistant API"}
