"""UI components for the feedback stage."""

import streamlit as st
from config import OPENAI_MODEL
from services.openai_service import get_openai_service
from state.session_state import show_feedback, reset_interview


def format_conversation_history() -> str:
    """Format conversation history as a string."""
    return "\n".join([
        f"{msg['role']}: {msg['content']}"
        for msg in st.session_state.messages
    ])


def generate_feedback() -> str:
    """Generate feedback based on conversation history."""
    conversation_history = format_conversation_history()
    
    openai_service = get_openai_service()
    system_message = openai_service.get_feedback_system_message(conversation_history)
    
    feedback = openai_service.create_chat_completion(
        model=st.session_state.get("openai_model", OPENAI_MODEL),
        messages=[system_message]
    )
    
    return feedback


def render_feedback_button() -> None:
    """Render the button to get feedback."""
    if st.button("Get Feedback", on_click=show_feedback, type="primary"):
        st.info("Fetching feedback...")


def render_feedback_display() -> None:
    """Render the feedback display."""
    st.subheader("Feedback", divider="rainbow")
    
    try:
        feedback = generate_feedback()
        st.markdown(feedback)
    except Exception as e:
        st.error(f"Error generating feedback: {str(e)}")
        st.info("Please try again later.")


def render_restart_button() -> None:
    """Render the restart interview button."""
    if st.button("Restart Interview", type="primary"):
        reset_interview()
        st.rerun()


def render_feedback_interface() -> None:
    """Render the complete feedback interface."""
    render_feedback_display()
    st.divider()
    render_restart_button()
