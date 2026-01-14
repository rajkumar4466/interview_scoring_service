"""Session state management for the Interview Simulator."""

import streamlit as st
from typing import Dict, Any


def initialize_session_state() -> None:
    """Initialize all session state variables with default values."""
    defaults: Dict[str, Any] = {
        "setup_complete": False,
        "feedback_shown": False,
        "chat_complete": False,
        "user_message_count": 0,
        "messages": [],
        "name": "",
        "experience": "",
        "skills": "",
        "level": None,
        "position": None,
        "company": None,
        "openai_model": None,
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def complete_setup() -> None:
    """Mark setup as complete."""
    st.session_state.setup_complete = True


def show_feedback() -> None:
    """Mark feedback as shown."""
    st.session_state.feedback_shown = True


def reset_interview() -> None:
    """Reset interview state for a new interview."""
    st.session_state.setup_complete = False
    st.session_state.feedback_shown = False
    st.session_state.chat_complete = False
    st.session_state.user_message_count = 0
    st.session_state.messages = []
