"""
Streamlit Frontend
-------------------
Interactive web UI for the Personalized Networking Assistant. Communicates
with the FastAPI backend over HTTP. All data (results, history) is persisted
via st.session_state across reruns within the same browser session.
"""

import sys
from pathlib import Path

# Allows this script (located in frontend/) to import modules from the parent
# project directory (specifically app.services.feedback_logger for the
# feedback history view).
sys.path.append(str(Path(__file__).resolve().parent.parent))

import requests
import streamlit as st

from app.services.feedback_logger import load_feedback
from app.services.history_logger import load_history

# Backend API location -- change this when deploying to a remote/cloud environment.
BASE_URL = "http://127.0.0.1:8000"

# ---------------------------------------------------------------------------
# Page configuration & styling
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Personalized Networking Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS – force ALL main headers (h2) to bright orange
st.markdown(
    """
    <style>
        .main > div {
            padding-top: 2rem;
        }
        .stButton > button {
            width: 100%;
        }
        .block-container {
            padding-bottom: 2rem;
        }
        .sidebar-content {
            padding: 1rem 0;
        }
        .feedback-icon {
            font-size: 1.2rem;
            margin-right: 0.5rem;
        }
        .history-entry {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
            border-left: 4px solid #4CAF50;
        }
        .suggestion-box {
            background-color: #ffffff;
            border-radius: 8px;
            padding: 0.8rem 1rem;
            margin-bottom: 0.8rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        /* ----  REMOVE OLD CONFLICTING RULE  ---- */
        /* .stMarkdown h1, h2, h3 { color: #2c3e50; }   <-- this was the culprit */

        /* ----  NEW RULE: ALL h2 inside the main block become orange  ---- */
        section.main div.block-container h2 {
            color: #FF6600 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------------------------
st.sidebar.title("🤖 Personlized Networking Assistant")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["✨ Generate", "📋 History", "💬 Feedback", "🔍 Fact‑check"],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.caption("v1.0 · Powered by FastAPI & Streamlit")

# ---------------------------------------------------------------------------
# Page: Generate
# ---------------------------------------------------------------------------
def page_generate():
    st.header("1. Tell us about the event")
    event_description = st.text_area(
        "Event description",
        placeholder="e.g. A conference bringing together AI startups and healthcare providers to discuss the future of diagnostics.",
        height=120,
    )

    user_interests = st.text_input(
        "Your interests (comma-separated)",
        placeholder="e.g. AI, blockchain, healthcare",
    )

    col_btn, _ = st.columns([2, 4])
    with col_btn:
        generate_clicked = st.button("✨ Generate conversation starters", type="primary")

    if generate_clicked:
        if not event_description.strip():
            st.warning("Please enter an event description first.")
        else:
            interests = [i.strip() for i in user_interests.split(",") if i.strip()]
            with st.spinner("Analyzing event and generating suggestions..."):
                try:
                    response = requests.post(
                        f"{BASE_URL}/generate-conversation",
                        json={"description": event_description, "interests": interests},
                        timeout=30,
                    )
                    response.raise_for_status()
                    st.session_state["result"] = response.json()
                except requests.RequestException as exc:
                    st.error(f"Could not reach the backend API: {exc}")

    # Display results if available
    if "result" in st.session_state and st.session_state["result"]:
        st.markdown("---")
        st.header("2. Your personalized suggestions")
        result = st.session_state["result"]

        st.subheader("Detected themes")
        st.write(", ".join(result.get("themes", [])) or "No themes detected.")

        st.subheader("Conversation starters")
        for i, suggestion in enumerate(result.get("suggestions", [])):
            with st.container():
                col_text, col_like, col_dislike = st.columns([8, 1, 1])
                with col_text:
                    st.markdown(f"**{i+1}.** {suggestion}")
                with col_like:
                    if st.button("👍", key=f"like_{i}", help="Like this suggestion"):
                        requests.post(f"{BASE_URL}/feedback", json={"suggestion": suggestion, "action": "like"})
                        st.success("Thanks for the feedback!")
                        st.balloons()
                with col_dislike:
                    if st.button("👎", key=f"dislike_{i}", help="Dislike this suggestion"):
                        requests.post(f"{BASE_URL}/feedback", json={"suggestion": suggestion, "action": "dislike"})
                        st.info("Thanks — we'll use this to improve.")
                st.markdown("---")

# ---------------------------------------------------------------------------
# Page: History
# ---------------------------------------------------------------------------
def page_history():
    st.header("📋 Recent conversation history")
    history = load_history()
    if not history:
        st.info("No conversations generated yet.")
    else:
        # Show the 10 most recent entries, newest first.
        for entry in reversed(history[-10:]):
            with st.container():
                st.markdown(f"**Event:** {entry.get('description', '')}")
                st.markdown(f"**Themes:** {', '.join(entry.get('themes', []))}")
                st.markdown(f"**Suggestions:** {', '.join(entry.get('suggestions', []))}")
                st.caption(f"🕒 {entry.get('timestamp', '')}")
                st.markdown("---")

# ---------------------------------------------------------------------------
# Page: Feedback
# ---------------------------------------------------------------------------
def page_feedback():
    st.header("💬 Recent feedback")
    feedback_entries = load_feedback()
    if not feedback_entries:
        st.info("No feedback submitted yet.")
    else:
        for entry in reversed(feedback_entries[-20:]):
            icon = "👍" if entry.get("action") == "like" else "👎"
            st.markdown(f"{icon} {entry.get('suggestion', '')}")
            st.caption(f"🕒 {entry.get('timestamp', '')}")
            st.markdown("---")

# ---------------------------------------------------------------------------
# Page: Fact-check
# ---------------------------------------------------------------------------
def page_factcheck():
    st.header("🔍 Quick fact-check")
    st.write("Verify a topic before you bring it up in conversation.")

    fact_query = st.text_input("Topic to verify", placeholder="e.g. Zero-shot learning")

    if st.button("🔍 Fact-check", type="primary"):
        if not fact_query.strip():
            st.warning("Please enter a topic to verify.")
        else:
            with st.spinner("Checking Wikipedia..."):
                try:
                    response = requests.post(f"{BASE_URL}/fact-check", json={"query": fact_query}, timeout=15)
                    response.raise_for_status()
                    extract = response.json().get("extract", "No information found.")
                    st.success(extract)
                except requests.RequestException as exc:
                    st.error(f"Could not reach the backend API: {exc}")

# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------
if page == "✨ Generate":
    page_generate()
elif page == "📋 History":
    page_history()
elif page == "💬 Feedback":
    page_feedback()
elif page == "🔍 Fact‑check":
    page_factcheck()