"""
Model status endpoint for Life Story Game AI Interviewer.

Returns information about available Gemini models and fallback configuration.

Endpoint: GET /api/model-status
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from api.ai_fallback import get_model_cascade


class handler(BaseHTTPRequestHandler):
    """
    Vercel serverless function handler for model status endpoint.

    Returns:
    {
        "available_models": ["gemini-2.5-flash", ...],
        "total_models": 6,
        "fallback_enabled": true,
        "source": "environment|default"
    }
    """

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        """Handle GET requests for model status."""
        try:
            # Get model cascade from environment or defaults
            models = get_model_cascade()
            env_models = os.getenv("GEMINI_MODELS")

            response = {
                "available_models": models,
                "total_models": len(models),
                "fallback_enabled": True,
                "source": "environment" if env_models else "default",
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))

        except Exception as e:
            print(f"[ERROR] Error in model_status handler: {e}")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            error_response = {"error": f"Internal server error: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode("utf-8"))