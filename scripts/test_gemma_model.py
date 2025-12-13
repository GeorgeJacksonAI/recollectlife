"""
Test script to verify gemma-3-12b model works with LangChain + Google Generative AI.
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr


def test_model(model_name: str):
    """Test a specific model."""
    print(f"\n{'='*50}")
    print(f"Testing model: {model_name}")
    print("=" * 50)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set")
        return False

    try:
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            api_key=SecretStr(api_key),
            temperature=0.7,
        )

        response = llm.invoke(
            [HumanMessage(content="Say 'Hello, I am working!' in exactly 5 words.")]
        )
        print(f"✓ SUCCESS! Response: {response.content}")
        return True

    except Exception as e:
        print(f"✗ FAILED: {type(e).__name__}: {e}")
        return False


def main():
    # Models to test
    models_to_test = [
        "gemma-3-12b",
        "models/gemma-3-12b",
        "gemma-3-12b-it",
        "models/gemma-3-12b-it",
        "gemma-2-9b",
        "gemma-2-9b-it",
        "gemini-2.0-flash-exp",
    ]

    print("Testing Google AI models...")
    print(f"API Key present: {'Yes' if os.getenv('GEMINI_API_KEY') else 'No'}")

    results = {}
    for model in models_to_test:
        results[model] = test_model(model)

    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    for model, success in results.items():
        status = "✓ WORKS" if success else "✗ FAILED"
        print(f"  {status}: {model}")


if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
