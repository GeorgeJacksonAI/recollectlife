import os
from typing import Dict, List

import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

genai.configure(api_key=GOOGLE_API_KEY)
# Use stable Gemini 2.0 model
model = genai.GenerativeModel("gemini-2.0-flash")


def format_messages_for_gemini(messages: List[Dict[str, str]]) -> List[Dict]:
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


def get_completion(
    system_instruction: str,
    conversation_history: List[Dict[str, str]],
    user_message: str,
) -> str:
    """Generate response using Google Gemini with system instruction"""
    try:
        # Build complete message list with system instruction at the start
        all_messages = [{"role": "user", "content": system_instruction}]
        all_messages.extend(conversation_history)
        all_messages.append({"role": "user", "content": user_message})

        # Convert to Gemini format
        gemini_messages = format_messages_for_gemini(all_messages)

        # Start chat with history (excluding last message)
        chat = model.start_chat(
            history=gemini_messages[:-1] if len(gemini_messages) > 1 else []
        )

        # Send last message
        response = chat.send_message(user_message)

        return response.text

    except Exception as e:
        print(f"\nError generating AI response: {e}")
        raise
