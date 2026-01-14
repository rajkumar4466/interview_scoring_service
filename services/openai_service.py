"""OpenAI service for handling API interactions."""

from openai import OpenAI
from typing import List, Dict, Iterator
import streamlit as st
from config import INTERVIEWER_SYSTEM_PROMPT_TEMPLATE, FEEDBACK_SYSTEM_PROMPT_TEMPLATE


class OpenAIService:
    """Service class for OpenAI API interactions."""
    
    def __init__(self, api_key: str):
        """Initialize OpenAI client."""
        self.client = OpenAI(api_key=api_key)
    
    def get_system_message(self, name: str, experience: str, skills: str, 
                          level: str, position: str, company: str) -> Dict[str, str]:
        """Generate system message for the interview."""
        return {
            "role": "system",
            "content": INTERVIEWER_SYSTEM_PROMPT_TEMPLATE.format(
                name=name,
                experience=experience,
                skills=skills,
                level=level,
                position=position,
                company=company
            )
        }
    
    def get_feedback_system_message(self, conversation_history: str) -> Dict[str, str]:
        """Generate system message for feedback generation."""
        return {
            "role": "system",
            "content": FEEDBACK_SYSTEM_PROMPT_TEMPLATE.format(
                conversation_history=conversation_history
            )
        }
    
    def create_chat_stream(self, model: str, messages: List[Dict[str, str]]) -> Iterator:
        """Create a streaming chat completion."""
        if not model:
            raise ValueError("Model parameter is required for OpenAI API call")
        return self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
        )
    
    def create_chat_completion(self, model: str, messages: List[Dict[str, str]]) -> str:
        """Create a non-streaming chat completion."""
        if not model:
            raise ValueError("Model parameter is required for OpenAI API call")
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream=False,
        )
        return response.choices[0].message.content


def get_openai_service() -> OpenAIService:
    """Get initialized OpenAI service instance."""
    api_key = st.secrets.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in Streamlit secrets")
    return OpenAIService(api_key=api_key)
