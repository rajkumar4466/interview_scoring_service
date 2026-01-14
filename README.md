# Interview Simulator

An interview simulation application built with Streamlit and OpenAI. This application allows users to practice job interviews with an AI-powered HR executive.

## Features

- **User Setup**: Collect personal information, experience, skills, and job preferences
- **AI-Powered Interview**: Conduct realistic interviews with configurable message limits
- **Performance Feedback**: Receive detailed feedback and scoring after the interview
- **Session Management**: Persistent state management across app reruns

## Project Structure

```
interview_simulator/
├── app.py                 # Main application entry point
├── config.py              # Configuration constants and settings
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── state/
│   ├── __init__.py
│   └── session_state.py  # Session state management
├── services/
│   ├── __init__.py
│   └── openai_service.py # OpenAI API service layer
├── ui/
│   ├── __init__.py
│   ├── setup_ui.py       # Setup form UI components
│   ├── interview_ui.py   # Interview chat UI components
│   └── feedback_ui.py    # Feedback display UI components
└── utils/
    └── __init__.py        # Utility functions
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Streamlit secrets:
   Create a `.streamlit/secrets.toml` file with your OpenAI API key:
   ```toml
   OPENAI_API_KEY = "your-api-key-here"
   ```

## Usage

Run the application:
```bash
streamlit run app.py
```

## Configuration

Edit `config.py` to customize:
- Maximum chat count
- OpenAI model selection
- Input field constraints
- Available positions and companies
- System prompts

## Architecture

- **Separation of Concerns**: UI, business logic, and services are separated
- **Service Layer**: OpenAI interactions abstracted into a service class
- **State Management**: Centralized session state initialization and management
- **Modular Design**: Each UI component is in its own module
- **Type Hints**: Code includes type annotations for better maintainability

## License

MIT
