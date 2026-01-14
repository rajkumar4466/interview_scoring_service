"""Configuration settings for the Interview Simulator application."""

# Page Configuration
PAGE_TITLE = "Interview Simulator"
PAGE_ICON = "💬"

# Application Settings
MAX_CHAT_COUNT = 5
OPENAI_MODEL = "gpt-4o-mini"

# Input Constraints
MAX_NAME_LENGTH = 40
MAX_EXPERIENCE_LENGTH = 200
MAX_SKILLS_LENGTH = 200
MAX_CHAT_INPUT_LENGTH = 100

# Default Values
DEFAULT_LEVEL = "Junior"
DEFAULT_POSITION = "Data Scientist"
DEFAULT_COMPANY = "Amazon"

# Available Options
LEVEL_OPTIONS = ["Junior", "Mid-level", "Senior"]

POSITION_OPTIONS = [
    "Data Scientist",
    "Data engineer",
    "ML Engineer",
    "BI Analyst",
    "Financial Analyst"
]

COMPANY_OPTIONS = [
    "Amazon",
    "Meta",
    "Udemy",
    "Microsoft",
    "Nestle",
    "LinkedIn",
    "Spotify"
]

# System Prompts
INTERVIEWER_SYSTEM_PROMPT_TEMPLATE = (
    "You are an HR executive that interviews an interviewee called {name} "
    "with experience {experience} and skills {skills}. "
    "You should interview him for the position {level} {position} "
    "at the company {company}."
)

FEEDBACK_SYSTEM_PROMPT_TEMPLATE = """You are a helpful tool that provides feedback for HR interview performance.
Before the feedback give a score of 1 to 10.

Conversation History:
{conversation_history}

Follow this format:
Overall Score: // Your score
Feedback: // your feedback
"""
