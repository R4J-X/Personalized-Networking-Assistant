"""
Event Analyzer Service
-----------------------
Responsible for the intelligent theme-extraction capability of the application.
Uses the Hugging Face Transformers pipeline abstraction to load and run a
DistilBERT model configured for zero-shot classification.

The pipeline is instantiated once at module import time (rather than on every
request) so that the expensive model-loading step only happens once during the
application lifecycle -- subsequent requests are processed much faster.
"""

from typing import List, Optional
from transformers import pipeline

# Loaded once at startup. bart-large-mnli / distilbert variants both support
# the `zero-shot-classification` task; a DistilBERT-based checkpoint is used
# here to keep inference fast and the memory footprint small.
_classifier = pipeline(
    "zero-shot-classification",
    model="typeform/distilbert-base-uncased-mnli",
)

DEFAULT_CANDIDATE_LABELS = [
    "artificial intelligence",
    "healthcare",
    "blockchain",
    "education",
    "sustainability",
    "finance",
    "startups",
    "product design",
    "marketing",
    "cybersecurity",
]

TOP_K = 3


def extract_event_themes(description: str, candidate_labels: Optional[List[str]] = None) -> List[str]:
    """
    Classify an event description against a set of candidate themes and
    return the top-scoring themes.

    Args:
        description: Free-text description of the networking event.
        candidate_labels: Optional custom label set. Falls back to
            DEFAULT_CANDIDATE_LABELS when not provided.

    Returns:
        A list of up to TOP_K theme strings, ordered by descending relevance.
    """
    labels = candidate_labels if candidate_labels else DEFAULT_CANDIDATE_LABELS

    result = _classifier(description, candidate_labels=labels, multi_label=True)

    # `result["labels"]` is already sorted by descending score by the pipeline.
    top_themes = result["labels"][:TOP_K]
    return top_themes
