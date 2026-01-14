
from openai import OpenAI
import streamlit as st

st.set_page_config(page_title="Streamlit Chat", page_icon="💬 ")
st.title("Chatbot")

max_chat_count = 5

if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False
if "feedback_shown" not in st.session_state:
    st.session_state.feedback_shown = False
if "chat_complete" not in st.session_state:
    st.session_state.chat_complete = False
if "user_message_count" not in st.session_state:
    st.session_state.user_message_count = 0
if "messages" not in st.session_state:
    st.session_state.messages = []

def complete_setup():
    st.session_state.setup_complete = True

def getFeedback():
    st.session_state.feedback_shown = True



if not st.session_state.setup_complete:
    st.subheader('Personal information', divider='rainbow')

    if "name" not in st.session_state:
        st.session_state["name"] = ""
    if "experience" not in st.session_state:
        st.session_state["experience"] = ""
    if "skills" not in st.session_state:
        st.session_state["skills"] = ""

    st.session_state["name"] = st.text_input(label = "Name", max_chars = 40, value = st.session_state["name"], placeholder = "Enter your name")
    st.session_state["experience"] = st.text_area(label = "Expirience", value = st.session_state["experience"], height = None, max_chars = 200, placeholder = "Describe your experience")
    st.session_state["skills"] = st.text_area(label = "Skills", value = st.session_state["skills"], height = None, max_chars = 200, placeholder = "List your skills")


    
    st.write(f"**Your Name**: {st.session_state['name']}")
    st.write(f"**Your Experience**: {st.session_state['experience']}")
    st.write(f"**Your Skills**: {st.session_state['skills']}")

    st.subheader('Company and Position', divider = 'rainbow')

    if "level" not in st.session_state:
        st.session_state["level"] = "Junior"
    if "position" not in st.session_state:
        st.session_state["position"] = "Data Scientist"
    if "company" not in st.session_state:
        st.session_state["company"] = "Amazon"

    st.session_state["level"] = st.radio(label = "Choose level", key = "visibility", options = ["Junior", "Mid-level", "Senior"])
    st.session_state["position"] = st.selectbox(label = "Choose a position", options = ("Data Scientist", "Data engineer", "ML Engineer", "BI Analyst", "Financial Analyst"))
    st.session_state["company"] = st.selectbox(label = "Choose a company", options = ("Amazon", "Meta", "Udemy", "Microsoft", "Nestle", "LinkedIn", "Spotify"))

    st.write(f"**Your information**: {st.session_state['level']} {st.session_state['position']} at {st.session_state['company']}")

    if st.button("Start Interview", on_click=complete_setup):
        st.write("Setup complete. Starting interview...")

if st.session_state.setup_complete and not st.session_state.feedback_shown and not st.session_state.chat_complete:
    st.info("Start by introducing yourself")

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"

    if not st.session_state.messages:
        st.session_state.messages = [{
            "role": "system",
            "content": (f"You are an HR executive that interviews an interviewee called {st.session_state['name']} "
                        f"with experience {st.session_state['experience']} and skills {st.session_state['skills']}. "
                        f"You should interview him for the position {st.session_state['level']} {st.session_state['position']} "
                        f"at the company {st.session_state['company']}")
        }]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


    if st.session_state.user_message_count < max_chat_count:
        if prompt := st.chat_input("Your answer", max_chars = 40):
            st.session_state.messages.append({
                "role": "user",
                "content": prompt
                })
            with st.chat_message("user"):
                st.markdown(prompt)

            if st.session_state.user_message_count < max_chat_count-1:
                with st.chat_message("assistant"):
                    stream = client.chat.completions.create(
                        model = st.session_state["openai_model"],
                        messages = [
                            { "role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        stream= True,
                    )
                    response = st.write_stream(stream)
                
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.session_state.user_message_count += 1

    if st.session_state.user_message_count >= max_chat_count:
        st.session_state.chat_complete = True


if st.session_state.chat_complete and not st.session_state.feedback_shown:
    if st.button("get feedback", on_click= getFeedback):
        st.write("fetching feedback")

if st.session_state.feedback_shown:
    st.subheader("Feedback")

    conversation_history = "\n".join([f"{msg["role"]}: {msg["content"]}"  
        for msg in st.session_state.messages])

    feedbackClient = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    feedbackCompletion = feedbackClient.chat.completions.create(
         model = st.session_state["openai_model"],
         messages = [{
            "role": "system",
            "content": f"""You are a helpful tool that provides feedback for HR interview performance.
                        Before the feedback give a score of 1 to 10.
                        
                        Conversation History:
                        {conversation_history}
                        
                        Follow this format:
                        Overall Score: // Your score
                        Feedback: // your feedback
                       """
        }]
    )

    st.write(feedbackCompletion.choices[0].message.content)