import streamlit as st
import requests
import speech_recognition as sr
import pyttsx3

# Backend API URL
API_URL = "http://localhost:5000/chat"

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

# Streamlit UI Setup
st.set_page_config(page_title="Gemini AI Chatbot", layout="centered")
st.title("🤖 Gemini AI Chatbot")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            st.write(f"🗣 You: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Could not understand audio")
        except sr.RequestError:
            st.error("Speech recognition service unavailable")
    return ""

# User input methods
col1, col2 = st.columns([3, 1])
with col1:
    user_input = st.chat_input("Type your message...")
with col2:
    if st.button("🎤 Speak"):
        user_input = recognize_speech()

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send to Flask backend
    response = requests.post(API_URL, json={"message": user_input})
    bot_response = response.json().get("response", "Error: No response")

    # Display AI response
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)

    # AI speaks response
    engine.say(bot_response)
    engine.runAndWait()
