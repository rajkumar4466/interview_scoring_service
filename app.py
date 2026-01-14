"""Main entry point for the Interview Simulator application."""

import streamlit as st
from config import PAGE_TITLE, PAGE_ICON
from state.session_state import initialize_session_state
from ui.setup_ui import render_setup_form
from ui.interview_ui import render_interview_interface
from ui.feedback_ui import render_feedback_button, render_feedback_interface


def main() -> None:
    """Main application entry point."""
    # Page configuration
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)
    st.title("Interview Simulator")
    
    # Initialize session state
    initialize_session_state()
    
    # Setup stage
    if not st.session_state.setup_complete:
        render_setup_form()
    
    # Interview stage (includes feedback button when complete)
    elif (st.session_state.setup_complete 
          and not st.session_state.feedback_shown):
        render_interview_interface()
    
    # Feedback display stage
    elif st.session_state.feedback_shown:
        render_feedback_interface()


if __name__ == "__main__":
    main()
