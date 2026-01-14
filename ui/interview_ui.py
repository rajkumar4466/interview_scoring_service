"""UI components for the interview stage."""

import streamlit as st
from typing import Optional
from config import MAX_CHAT_COUNT, MAX_CHAT_INPUT_LENGTH, OPENAI_MODEL
from services.openai_service import get_openai_service
from ui.feedback_ui import render_feedback_button


def initialize_chat_messages() -> None:
    """Initialize chat messages with system prompt if not already done."""
    if not st.session_state.messages:
        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = OPENAI_MODEL
        
        openai_service = get_openai_service()
        system_message = openai_service.get_system_message(
            name=st.session_state["name"],
            experience=st.session_state["experience"],
            skills=st.session_state["skills"],
            level=st.session_state["level"],
            position=st.session_state["position"],
            company=st.session_state["company"]
        )
        st.session_state.messages = [system_message]


def display_chat_messages() -> None:
    """Display all chat messages except system messages."""
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


def handle_user_input() -> Optional[str]:
    """Handle user input and return the prompt if provided."""
    prompt = st.chat_input("Your answer", max_chars=MAX_CHAT_INPUT_LENGTH)
    return prompt


def process_user_message(prompt: str) -> None:
    """Process and display user message."""
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    with st.chat_message("user"):
        st.markdown(prompt)


def get_assistant_response() -> str:
    """Get and display assistant's streaming response."""
    # Ensure model is set
    if "openai_model" not in st.session_state or st.session_state["openai_model"] is None:
        st.session_state["openai_model"] = OPENAI_MODEL
    
    openai_service = get_openai_service()
    stream = openai_service.create_chat_stream(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
    )
    
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    
    return response


def render_interview_interface() -> None:
    """Render the complete interview chat interface."""
    st.info("Start by introducing yourself", icon="👋")
    
    # Initialize chat messages
    initialize_chat_messages()
    
    # Display existing messages
    display_chat_messages()
    
    # Handle user input and responses
    if st.session_state.user_message_count < MAX_CHAT_COUNT:
        prompt = handle_user_input()
        
        if prompt:
            process_user_message(prompt)
            
            # Get assistant response if not at max count
            if st.session_state.user_message_count < MAX_CHAT_COUNT - 1:
                response = get_assistant_response()
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })
            
            st.session_state.user_message_count += 1
    
    # Mark chat as complete when max count reached
    if st.session_state.user_message_count >= MAX_CHAT_COUNT:
        st.session_state.chat_complete = True
    
    # Show feedback button if chat is complete
    if st.session_state.chat_complete:
        st.success("Interview completed! Click 'Get Feedback' to see your results.")
        st.divider()
        render_feedback_button()
