"""
Health check endpoint for Life Story Game AI Interviewer.

Simple health check to verify serverless functions are operational.

Endpoint: GET /api/health
"""

import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    """
    Vercel serverless function handler for health check endpoint.

    Returns:
    {
        "status": "ok",
        "service": "Life Story Game AI Interviewer",
        "timestamp": "2025-11-21T12:00:00Z"
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
        """Handle GET requests for health check."""
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        response = {
            "status": "ok",
            "service": "Life Story Game AI Interviewer",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        self.wfile.write(json.dumps(response).encode("utf-8"))