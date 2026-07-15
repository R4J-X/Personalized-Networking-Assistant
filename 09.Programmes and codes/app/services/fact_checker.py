"""
Fact Checker Service
----------------------
Provides quick fact-verification by querying the Wikipedia REST API.
Wikipedia is a well-maintained, publicly accessible knowledge base that
returns structured JSON data, making it ideal for this use case without
requiring API keys or authentication.
"""

import requests

WIKIPEDIA_SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"
REQUEST_TIMEOUT_SECONDS = 5
FALLBACK_MESSAGE = "Sorry, I couldn't find or verify that information right now. Please try a different search term."


def fact_check(query: str) -> str:
    try:
        url = WIKIPEDIA_SUMMARY_URL.format(
            query.strip().replace(" ", "_")
        )

        headers = {
            "User-Agent": "PersonalizedNetworkingAssistant/1.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )

        response.raise_for_status()

        data = response.json()
        extract = data.get("extract")

        if not extract:
            return FALLBACK_MESSAGE

        return extract

    except (requests.RequestException, ValueError):
        return FALLBACK_MESSAGE