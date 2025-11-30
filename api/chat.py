"""
Serverless chat endpoint for Life Story AI Interviewer - Modular Route System.

Vercel serverless function that handles AI chat requests with stateless
architecture. Uses new modular route system from api/routes/.

Endpoint: POST /api/chat
"""

import json
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Dict, Optional
from urllib.parse import parse_qs

# Add project root to path to import route logic
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from api.ai_fallback import run_gemini_fallback
from api.routes import ChronologicalSteward

# Route registry - maps route identifiers to route classes
ROUTE_REGISTRY = {
    "1": ChronologicalSteward,
    "chronological": ChronologicalSteward,
}

# Theme keyword mappings for detecting addressed themes in AI responses
# Each theme maps to a list of keywords that indicate the theme was discussed
THEME_KEYWORDS: Dict[str, list] = {
    "family": [
        "family",
        "families",
        "parents",
        "siblings",
        "relatives",
        "mother",
        "father",
        "brother",
        "sister",
    ],
    "career": [
        "career",
        "job",
        "work",
        "profession",
        "occupation",
        "employment",
        "workplace",
    ],
    "love": [
        "love",
        "romance",
        "relationship",
        "partner",
        "spouse",
        "dating",
        "marriage",
    ],
    "adventure": [
        "adventure",
        "adventures",
        "exciting",
        "explore",
        "exploration",
        "journey",
    ],
    "challenge": [
        "challenge",
        "challenges",
        "difficult",
        "struggle",
        "overcome",
        "obstacle",
    ],
    "growth": ["growth", "growing", "develop", "progress", "evolve", "mature", "learn"],
    "travel": [
        "travel",
        "traveled",
        "trip",
        "trips",
        "journey",
        "visited",
        "destination",
    ],
    "friendship": ["friendship", "friends", "friend", "companion", "buddy", "pal"],
    "legacy": [
        "legacy",
        "heritage",
        "inheritance",
        "lasting",
        "remember",
        "leave behind",
    ],
    "identity": ["identity", "who you are", "sense of self", "define", "authentic"],
    "father_figure": ["father", "dad", "daddy", "paternal", "fatherly"],
    "mother_figure": ["mother", "mom", "mommy", "maternal", "motherly"],
    "mentor": ["mentor", "mentors", "guide", "teacher", "coach", "advisor"],
    "loss": ["loss", "lost", "grief", "grieving", "mourning", "passed away", "death"],
    "success": [
        "success",
        "successful",
        "achievement",
        "accomplish",
        "triumph",
        "victory",
    ],
    "failure": ["failure", "failed", "setback", "mistake", "defeat"],
    "humor": ["humor", "humour", "funny", "laugh", "comedy", "joke"],
    "courage": ["courage", "courageous", "brave", "bravery", "fearless"],
    "resilience": ["resilience", "resilient", "bounce back", "recover", "persevere"],
}


def validate_payload(data: Dict) -> tuple[bool, str, Dict]:
    """
    Validate incoming request payload.

    Args:
        data: Parsed JSON request body

    Returns:
        Tuple of (is_valid, error_message, validated_data)
    """
    if not data:
        return False, "Empty request body", {}

    # Get messages
    messages = data.get("messages", [])
    if not isinstance(messages, list) or len(messages) == 0:
        return False, "messages must be a non-empty array", {}

    # Validate message structure
    for idx, msg in enumerate(messages):
        if not isinstance(msg, dict):
            return False, f"Message {idx} must be an object", {}

        if "role" not in msg or "content" not in msg:
            return False, f"Message {idx} missing 'role' or 'content'", {}

        if msg["role"] not in ["user", "assistant", "system"]:
            return False, f"Message {idx} has invalid role: {msg['role']}", {}

        if not isinstance(msg["content"], str):
            return False, f"Message {idx} content must be a string", {}

    # Validate total message size (prevent abuse)
    total_chars = sum(len(msg.get("content", "")) for msg in messages)
    if total_chars > 50000:  # 50K char limit
        return False, f"Total message size ({total_chars} chars) exceeds 50K limit", {}

    # Get route (default to chronological)
    route_id = data.get("route", "1")
    if route_id not in ROUTE_REGISTRY:
        return False, f"Invalid route: {route_id}", {}

    # Get phase (optional - route will determine if not provided)
    phase = data.get("phase")

    # Get age range (for age-aware routes)
    age_range = data.get("age_range")

    # Get explicit transition flag (user clicked "Next Phase" button)
    advance_phase = data.get("advance_phase", False)

    # Get age selection input (control code 1-5, not added to message history)
    age_selection_input = data.get("age_selection_input")

    # Get jump_to_phase (user clicked on a phase in timeline to jump to it)
    jump_to_phase = data.get("jump_to_phase")

    # Get selected tags (user's chosen focus areas)
    selected_tags = data.get("selected_tags", [])
    if not isinstance(selected_tags, list):
        return False, "selected_tags must be an array", {}

    # Validate tag content (only strings allowed)
    for tag in selected_tags:
        if not isinstance(tag, str):
            return False, "All tags must be strings", {}

    # Get already addressed themes (tracked by frontend)
    addressed_themes = data.get("addressed_themes", [])
    if not isinstance(addressed_themes, list):
        return False, "addressed_themes must be an array", {}

    return (
        True,
        "",
        {
            "messages": messages,
            "route_id": route_id,
            "phase": phase,
            "age_range": age_range,
            "advance_phase": advance_phase,
            "age_selection_input": age_selection_input,
            "jump_to_phase": jump_to_phase,
            "selected_tags": selected_tags,
            "addressed_themes": addressed_themes,
        },
    )


def reconstruct_route_state(
    route_class, messages: list, age_range: Optional[str] = None
):
    """
    Reconstruct route state from message history.

    Since the backend is stateless, we reconstruct the route object's state
    from the client-provided message history.

    Args:
        route_class: The route class to instantiate
        messages: Message history from client
        age_range: User's age range (if already selected)

    Returns:
        Instantiated route object with reconstructed state
    """
    route = route_class()

    # Replay messages to reconstruct state
    for msg in messages:
        route.add_message(msg["role"], msg["content"])

    # Set age range if provided
    if age_range and hasattr(route, "age_range"):
        route.age_range = age_range
        if hasattr(route, "_configure_phases_for_age"):
            route._configure_phases_for_age()

    return route


def detect_addressed_themes(
    text: str, selected_tags: list, already_addressed: list
) -> list:
    """
    Detect which themes are mentioned in the text.

    Args:
        text: The AI response text to scan
        selected_tags: All user-selected themes
        already_addressed: Themes already marked as addressed

    Returns:
        List of newly addressed themes found in this response
    """
    if not text or not selected_tags:
        return []

    text_lower = text.lower()
    newly_addressed = []

    for theme in selected_tags:
        if theme in already_addressed:
            continue

        # Get keywords for this theme, or use the theme itself as fallback
        keywords = THEME_KEYWORDS.get(theme.lower(), [theme.lower()])

        # Check if any keyword appears in the text
        if any(keyword in text_lower for keyword in keywords):
            newly_addressed.append(theme)

    return newly_addressed


def get_current_phase_from_route(route, messages: list) -> str:
    """
    Determine current phase from route state and message history.

    Args:
        route: Route object
        messages: Message history

    Returns:
        Current phase name
    """
    # If phase_order not configured yet, return initial phase
    if not route.phase_order or len(route.phase_order) <= 2:
        return route.get_initial_phase()

    # Count user messages to estimate phase
    user_message_count = sum(1 for msg in messages if msg["role"] == "user")

    # Determine phase index
    # GREETING: 0 user messages or 1 (saying "yes")
    # AGE_SELECTION: 1-2 user messages
    # Subsequent phases: 3+ user messages

    if user_message_count == 0:
        return "GREETING"
    elif user_message_count == 1:
        # Check if they said yes to greeting
        last_user_msg = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"), ""
        )
        affirmative = ["yes", "yeah", "sure", "ready", "ok", "let's go", "sim", "vamos"]
        if any(word in last_user_msg.lower() for word in affirmative):
            return "AGE_SELECTION"
        return "GREETING"
    elif user_message_count == 2:
        # Should be at AGE_SELECTION or just past it
        if not route.is_age_selected():
            return "AGE_SELECTION"
        # Age was selected, move to first interview phase
        return route.phase_order[2] if len(route.phase_order) > 2 else "CHILDHOOD"
    else:
        # Advanced phases - estimate based on message count
        # user_message 3 → phase_order[2] (CHILDHOOD)
        # user_message 4 → phase_order[3] (ADOLESCENCE), etc.
        phase_index = min(user_message_count - 1, len(route.phase_order) - 1)
        return route.phase_order[phase_index]


class handler(BaseHTTPRequestHandler):
    """
    Vercel serverless function handler for chat endpoint.

    Expected request body:
    {
        "messages": [{"role": "user|assistant", "content": "..."}],
        "route": "1|chronological" (optional, default: "1"),
        "phase": "GREETING|AGE_SELECTION|..." (optional),
        "age_range": "under_18|18_30|..." (optional, for age-aware routes)
    }

    Returns:
    {
        "response": "AI generated response",
        "model": "model_name_used",
        "attempts": 2,
        "phase": "current_phase",
        "age_range": "under_18|..." (if applicable)
    }
    """

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        """Handle POST requests for chat."""
        try:
            payload = self._parse_request_body()
            if payload is None:
                return  # Error response already sent

            is_valid, error_msg, validated = validate_payload(payload)
            if not is_valid:
                return self._send_error(400, error_msg)

            route, messages, context = self._initialize_route_context(validated)

            # Handle age selection (silent operation - no AI response)
            if context["age_selection_input"]:
                response = self._handle_age_selection(
                    route, context["age_selection_input"]
                )
                if response:
                    return self._send_json_response(200, response)

            # Determine current phase with jump/advance handling
            current_phase, messages = self._resolve_current_phase(
                route, messages, context
            )
            if current_phase is None:
                return  # Error response already sent

            # Build system instruction with theme context
            system_instruction = self._build_system_instruction(
                route, current_phase, context
            )
            if system_instruction is None:
                return  # Error response already sent

            # Generate AI response
            result = run_gemini_fallback(
                messages=messages, system_instruction=system_instruction
            )
            if not result["success"]:
                return self._send_error(
                    500,
                    result["error"] or "Failed to generate AI response",
                    {"attempts": result["attempts"]},
                )

            # Build and send response
            response = self._build_chat_response(route, current_phase, result, context)
            self._send_json_response(200, response)

        except json.JSONDecodeError as e:
            self._send_error(400, f"Invalid JSON: {str(e)}")
        except Exception as e:
            print(f"[ERROR] Unhandled exception in chat handler: {e}")
            import traceback

            traceback.print_exc()
            self._send_error(500, f"Internal server error: {str(e)}")

    def _parse_request_body(self) -> Optional[Dict]:
        """Parse and return JSON request body, or None on error."""
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        try:
            return json.loads(body) if body else {}
        except json.JSONDecodeError as e:
            self._send_error(400, f"Invalid JSON: {str(e)}")
            return None

    def _initialize_route_context(self, validated: Dict) -> tuple:
        """Initialize route object and extract context from validated payload."""
        route_class = ROUTE_REGISTRY[validated["route_id"]]
        route = reconstruct_route_state(
            route_class, validated["messages"], validated["age_range"]
        )

        context = {
            "provided_phase": validated["phase"],
            "advance_phase": validated["advance_phase"],
            "age_selection_input": validated.get("age_selection_input"),
            "jump_to_phase": validated.get("jump_to_phase"),
            "selected_tags": validated.get("selected_tags", []),
            "addressed_themes": validated.get("addressed_themes", []),
            "route_id": validated["route_id"],
        }

        return route, validated["messages"], context

    def _handle_age_selection(self, route, age_selection_input: str) -> Optional[Dict]:
        """Handle age selection input, return response dict or None."""
        route.phase = "AGE_SELECTION"

        if not route.should_advance(age_selection_input, explicit_transition=False):
            return None

        current_phase = route.advance_phase()
        print(f"[AGE] Selected: {age_selection_input} -> {route.age_range}")
        print(f"[PHASE] Advanced to: {current_phase}")

        return self._build_response_data(
            route=route,
            current_phase=current_phase,
            content="",
            model="none",
            attempts=0,
        )

    def _resolve_current_phase(
        self, route, messages: list, context: Dict
    ) -> tuple[Optional[str], list]:
        """Determine current phase, handling jumps and advances. Returns (phase, messages)."""
        jump_to_phase = context["jump_to_phase"]
        provided_phase = context["provided_phase"]
        advance_phase = context["advance_phase"]

        # Handle phase jump
        if jump_to_phase:
            if not (
                hasattr(route, "phase_order") and jump_to_phase in route.phase_order
            ):
                self._send_error(400, f"Invalid phase: {jump_to_phase}")
                return None, messages

            old_phase = provided_phase or "UNKNOWN"
            route.phase = jump_to_phase
            print(f"[PHASE] Jumped from {old_phase} to: {jump_to_phase}")
            messages = messages + [
                {"role": "user", "content": f"[Jumping to chapter: {jump_to_phase}]"}
            ]
            return jump_to_phase, messages

        # Determine phase normally
        current_phase = provided_phase or get_current_phase_from_route(route, messages)

        # Handle explicit phase advancement
        if advance_phase:
            route.phase = current_phase
            last_user_msg = next(
                (m["content"] for m in reversed(messages) if m["role"] == "user"), ""
            )
            if route.should_advance(last_user_msg, explicit_transition=True):
                old_phase = current_phase
                current_phase = route.advance_phase()
                print(f"[PHASE] Advanced from {old_phase} to: {current_phase}")
                messages = messages + [
                    {
                        "role": "user",
                        "content": f"[Moving to next phase: {current_phase}]",
                    }
                ]

        return current_phase, messages

    def _build_system_instruction(
        self, route, current_phase: str, context: Dict
    ) -> Optional[str]:
        """Build system instruction with optional theme context. Returns None on error."""
        try:
            route.phase = current_phase
            phase_config = route.get_current_phase()
            system_instruction = phase_config["system_instruction"]
        except (ValueError, KeyError) as e:
            self._send_error(
                400,
                f"Invalid phase '{current_phase}' for route '{context['route_id']}': {str(e)}",
            )
            return None

        # Inject theme context if themes are selected
        selected_tags = context["selected_tags"]
        if not selected_tags:
            return system_instruction

        addressed_themes = context["addressed_themes"]
        sanitized_tags = [
            tag.replace('"', "").replace("'", "")[:30] for tag in selected_tags
        ]

        pending = [t for t in sanitized_tags if t not in addressed_themes]
        addressed = [t for t in sanitized_tags if t in addressed_themes]

        pending_str = ", ".join(f'"{t}"' for t in pending) if pending else "none"
        addressed_str = ", ".join(f'"{t}"' for t in addressed) if addressed else "none"

        theme_context = f"""

STORY THEMES TO ADDRESS:

Pending themes (prioritize these): {pending_str}
Already addressed themes: {addressed_str}

For the pending themes, find natural opportunities to ask about or explore these topics in the conversation. Each theme should be addressed at least once before the story is complete. Weave them naturally into questions when relevant - don't force them."""

        print(f"[TAGS] Pending: {pending_str} | Addressed: {addressed_str}")
        return system_instruction + theme_context

    def _build_chat_response(
        self, route, current_phase: str, ai_result: Dict, context: Dict
    ) -> Dict:
        """Build the final chat response with theme detection."""
        selected_tags = context["selected_tags"]
        addressed_themes = context["addressed_themes"]

        newly_addressed = []
        if selected_tags:
            newly_addressed = detect_addressed_themes(
                ai_result["content"], selected_tags, addressed_themes
            )
            if newly_addressed:
                print(f"[TAGS] Newly addressed: {newly_addressed}")

        response = self._build_response_data(
            route=route,
            current_phase=current_phase,
            content=ai_result["content"],
            model=ai_result["model"],
            attempts=ai_result["attempts"],
            newly_addressed_themes=newly_addressed,
        )
        return response

    def _build_response_data(
        self,
        route,
        current_phase: str,
        content: str,
        model: str,
        attempts: int,
        newly_addressed_themes: Optional[list] = None,
    ) -> Dict:
        """Build standardized response data dictionary."""
        response = {
            "response": content,
            "model": model,
            "attempts": attempts,
            "phase": current_phase,
        }

        if newly_addressed_themes is not None:
            response["newly_addressed_themes"] = newly_addressed_themes

        if hasattr(route, "get_age_range") and route.get_age_range():
            response["age_range"] = route.get_age_range()

        if hasattr(route, "phase_order"):
            response["phase_order"] = route.phase_order
            try:
                response["phase_index"] = route.phase_order.index(current_phase)
            except ValueError:
                response["phase_index"] = -1

        return response

    def _send_error(self, status_code: int, message: str, extra: Optional[Dict] = None):
        """Send error response with optional extra fields."""
        data = {"error": message}
        if extra:
            data.update(extra)
        self._send_json_response(status_code, data)

    def _send_json_response(self, status_code: int, data: dict):
        """Send JSON response with CORS headers."""
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))
