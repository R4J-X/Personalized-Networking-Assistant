"""
Pydantic data contracts shared between the frontend and backend.

Each class inherits from BaseModel, which gives automatic type validation,
serialization, and interactive documentation via FastAPI's built-in Swagger UI.
If a required field is missing or has the wrong type, FastAPI automatically
returns a 422 Unprocessable Entity error with a clear description of what
went wrong -- no additional error-handling code required.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class EventAnalysisRequest(BaseModel):
    description: str = Field(..., min_length=1, description="Free-text description of the networking event.")
    candidate_labels: Optional[List[str]] = Field(
        default=None,
        description="Optional custom list of candidate themes. Defaults to a broad set of professional networking themes.",
    )


class EventAnalysisResponse(BaseModel):
    themes: List[str]


class ConversationRequest(BaseModel):
    description: str = Field(..., min_length=1, description="Free-text description of the networking event.")
    interests: List[str] = Field(default_factory=list, description="List of the user's personal/professional interests.")


class ConversationResponse(BaseModel):
    themes: List[str]
    suggestions: List[str]


class FactCheckRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Topic or phrase to verify against Wikipedia.")


class FactCheckResponse(BaseModel):
    query: str
    extract: str


class FeedbackRequest(BaseModel):
    suggestion: str = Field(..., min_length=1, description="The exact suggestion text being rated.")
    action: str = Field(..., pattern="^(like|dislike)$", description="Either 'like' or 'dislike'.")
