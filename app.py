import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to access backend

# Configure API Key
genai.configure(api_key="AIzaSyBVJFmwmlxucPurVtU6_0OzH3zcgP9wtic")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No input provided"}), 400

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(user_message)

    return jsonify({"response": response.text})

if __name__ == "__main__":
    import os
    os.system("streamlit run chatbot.py")
