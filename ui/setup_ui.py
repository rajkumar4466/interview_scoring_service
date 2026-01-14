"""UI components for the setup stage."""

import streamlit as st
from config import (
    DEFAULT_LEVEL,
    DEFAULT_POSITION,
    DEFAULT_COMPANY,
    LEVEL_OPTIONS,
    POSITION_OPTIONS,
    COMPANY_OPTIONS,
    MAX_NAME_LENGTH,
    MAX_EXPERIENCE_LENGTH,
    MAX_SKILLS_LENGTH,
)
from state.session_state import complete_setup


def render_personal_information_section() -> None:
    """Render the personal information input section."""
    st.subheader('Personal information', divider='rainbow')
    
    # Initialize defaults if not set
    if "name" not in st.session_state:
        st.session_state["name"] = ""
    if "experience" not in st.session_state:
        st.session_state["experience"] = ""
    if "skills" not in st.session_state:
        st.session_state["skills"] = ""
    
    # Input fields
    st.session_state["name"] = st.text_input(
        label="Name",
        max_chars=MAX_NAME_LENGTH,
        value=st.session_state["name"],
        placeholder="Enter your name"
    )
    
    st.session_state["experience"] = st.text_area(
        label="Experience",
        value=st.session_state["experience"],
        height=None,
        max_chars=MAX_EXPERIENCE_LENGTH,
        placeholder="Describe your experience"
    )
    
    st.session_state["skills"] = st.text_area(
        label="Skills",
        value=st.session_state["skills"],
        height=None,
        max_chars=MAX_SKILLS_LENGTH,
        placeholder="List your skills"
    )
    
    # Display entered information
    st.write(f"**Your Name**: {st.session_state['name']}")
    st.write(f"**Your Experience**: {st.session_state['experience']}")
    st.write(f"**Your Skills**: {st.session_state['skills']}")


def render_company_position_section() -> None:
    """Render the company and position selection section."""
    st.subheader('Company and Position', divider='rainbow')
    
    # Initialize defaults if not set
    if "level" not in st.session_state:
        st.session_state["level"] = DEFAULT_LEVEL
    if "position" not in st.session_state:
        st.session_state["position"] = DEFAULT_POSITION
    if "company" not in st.session_state:
        st.session_state["company"] = DEFAULT_COMPANY
    
    # Selection inputs
    st.session_state["level"] = st.radio(
        label="Choose level",
        key="visibility",
        options=LEVEL_OPTIONS
    )
    
    st.session_state["position"] = st.selectbox(
        label="Choose a position",
        options=POSITION_OPTIONS
    )
    
    st.session_state["company"] = st.selectbox(
        label="Choose a company",
        options=COMPANY_OPTIONS
    )
    
    # Display selected information
    st.write(
        f"**Your information**: {st.session_state['level']} "
        f"{st.session_state['position']} at {st.session_state['company']}"
    )


def render_setup_form() -> None:
    """Render the complete setup form."""
    render_personal_information_section()
    render_company_position_section()
    
    # Start interview button
    if st.button("Start Interview", on_click=complete_setup, type="primary"):
        st.success("Setup complete. Starting interview...")
