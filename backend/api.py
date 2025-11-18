import os

import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# ==============================================================================
# CONFIGURATION
# ==============================================================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-exp")

# System prompt for the chatbot
SYSTEM_PROMPT = """You are a helpful, friendly, and knowledgeable AI assistant. 
Provide clear, accurate, and concise responses. Be conversational but professional.
If you don't know something, admit it rather than making up information."""


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================


def format_messages_for_gemini(messages):
    """Convert message history to Gemini API format"""
    gemini_messages = []

    for msg in messages:
        role = msg.get("role")
        content = msg.get("content", "")

        # Map roles: assistant -> model, user -> user
        if role == "assistant":
            gemini_messages.append({"role": "model", "parts": [{"text": content}]})
        elif role == "user":
            gemini_messages.append({"role": "user", "parts": [{"text": content}]})

    return gemini_messages


def generate_ai_response(messages):
    """Generate response using Google Gemini AI"""
    try:
        # Convert messages to Gemini format
        gemini_messages = format_messages_for_gemini(messages)

        # Start chat with history
        chat = model.start_chat(
            history=gemini_messages[:-1] if len(gemini_messages) > 1 else []
        )

        # Get the last user message
        last_message = messages[-1].get("content", "")

        # Generate response
        response = chat.send_message(last_message)

        return response.text

    except Exception as e:
        print(f"Error generating AI response: {e}")
        import traceback

        traceback.print_exc()
        raise


# ==============================================================================
# API ENDPOINTS
# ==============================================================================


@app.route("/api/chat", methods=["POST"])
def chat():
    """Main chat endpoint for AI conversation"""
    try:
        data = request.json

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Support both 'messages' (full history) and 'message' (legacy single message)
        messages = data.get("messages", [])

        if not messages:
            # Fallback to legacy format
            if "message" in data:
                user_message = data["message"].strip()
                if not user_message:
                    return jsonify({"error": "Empty message"}), 400
                messages = [{"role": "user", "content": user_message}]
            else:
                return jsonify({"error": "No messages provided"}), 400

        # Validate messages
        if not isinstance(messages, list) or len(messages) == 0:
            return jsonify({"error": "Messages must be a non-empty array"}), 400

        # Generate AI response
        response_text = generate_ai_response(messages)

        return jsonify({"response": response_text}), 200

    except Exception as e:
        print(f"Error processing message: {e}")
        import traceback

        traceback.print_exc()
        return jsonify({"error": f"Error processing message: {str(e)}"}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "service": "AI Chatbot"}), 200


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    print("🚀 Flask server running at http://localhost:5000")
    print("📡 Available endpoints:")
    print("   - POST /api/chat   (Chat with AI)")
    print("   - GET  /health     (Health check)")
    app.run(debug=True, port=5000, host="0.0.0.0")
