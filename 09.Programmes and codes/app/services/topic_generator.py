"""
Topic Generator Service
-------------------------
Handles the creative core of the application: generating natural, engaging
conversation starters using GPT-2. Unlike the classifier, which makes binary
judgment calls, the generator produces original text that must sound
human-like and contextually appropriate.
"""

import re
from typing import List
from transformers import pipeline, set_seed

# Fixing the random seed makes outputs reproducible across runs -- invaluable
# for debugging and testing.
set_seed(42)

_generator = pipeline("text-generation", model="gpt2")

MAX_LENGTH = 80
NUM_SUGGESTIONS = 3


def _build_prompt(themes: List[str], interests: List[str]) -> str:
    """
    Construct a structured, first-person context narrative that guides GPT-2
    toward producing conversation starters rather than arbitrary text.
    """
    theme_str = ", ".join(themes) if themes else "this event"
    interest_str = ", ".join(interests) if interests else "meeting new people"

    return (
        f"I'm attending an event focused on {theme_str}. "
        f"I'm personally interested in {interest_str}. "
        f"Here are three friendly conversation starters I could use to break the ice:\n"
        f"1."
    )


def _clean_line(line: str) -> str:
    """Strip bullet markers, numbering, and surrounding whitespace from a raw generated line."""
    cleaned = re.sub(r"^\s*[\d]+[\.\)]\s*", "", line)
    cleaned = re.sub(r"^\s*[-*•]\s*", "", cleaned)
    return cleaned.strip()


def generate_topics(themes: List[str], interests: List[str]) -> List[str]:
    """
    Generate personalized conversation starters based on extracted event
    themes and the user's stated interests.

    Args:
        themes: Themes extracted by the event analyzer service.
        interests: The user's personal/professional interests.

    Returns:
        A list of up to NUM_SUGGESTIONS cleaned conversation-starter strings.
    """
    prompt = _build_prompt(themes, interests)

    raw_output = _generator(
        prompt,
        max_length=MAX_LENGTH,
        num_return_sequences=1,
        truncation=True,
    )[0]["generated_text"]

    # GPT-2 does not always produce cleanly formatted lists, so the output is
    # split by newline, cleaned of bullet markers, and the first N non-empty
    # lines are extracted as usable suggestions.
    lines = [_clean_line(line) for line in raw_output.split("\n")]
    suggestions = [line for line in lines if line][:NUM_SUGGESTIONS]

    # Fallback in case generation produced fewer than NUM_SUGGESTIONS usable lines.
    while len(suggestions) < NUM_SUGGESTIONS:
        theme = themes[0] if themes else "this event"
        suggestions.append(f"What brings you to this event focused on {theme}?")

    return suggestions
