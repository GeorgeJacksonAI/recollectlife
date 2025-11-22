"""Chronological Steward story route implementation."""

from typing import Dict, List, Optional

from .base import StoryRoute


class ChronologicalSteward(StoryRoute):
    """Story route that captures life chronologically from birth to present.
    
    This route adapts interview phases based on the user's age, ensuring
    questions are relevant to their life stage (e.g., adolescents skip midlife questions).
    """

    ROUTE_INFO = {
        "name": "Chronological Steward",
        "persona": "Likes order, facts, and timelines.",
        "goal": "Capture your life story in sequential, linear order from birth to present.",
        "presentation": "Your story will be organized chronologically into chapters that follow your life timeline, with each chapter capturing a distinct era of your journey.",
        "prompt_focus": "Let's start at the very beginning. What are your earliest significant memories?",
    }

    # Age range to phase mapping - determines which life stages to include
    AGE_PHASE_MAPPING = {
        "under_18": ["GREETING", "AGE_SELECTION", "CHILDHOOD", "ADOLESCENCE", "PRESENT", "SYNTHESIS"],
        "18_30": ["GREETING", "AGE_SELECTION", "CHILDHOOD", "ADOLESCENCE", "EARLY_ADULTHOOD", "PRESENT", "SYNTHESIS"],
        "31_45": ["GREETING", "AGE_SELECTION", "CHILDHOOD", "ADOLESCENCE", "EARLY_ADULTHOOD", "MIDLIFE", "PRESENT", "SYNTHESIS"],
        "46_60": ["GREETING", "AGE_SELECTION", "CHILDHOOD", "ADOLESCENCE", "EARLY_ADULTHOOD", "MIDLIFE", "PRESENT", "SYNTHESIS"],
        "61_plus": ["GREETING", "AGE_SELECTION", "CHILDHOOD", "ADOLESCENCE", "EARLY_ADULTHOOD", "MIDLIFE", "PRESENT", "SYNTHESIS"],
    }

    PHASES = {
        "GREETING": {
            "description": "Welcome and explain the process",
            "system_instruction": """You are a warm, empathetic interviewer documenting a life story.

Your role: Guide the user through telling their life story chronologically, from earliest memories to present day.

Current phase: GREETING
- Welcome the user warmly
- Explain: "I'm here to help you tell your life story chronologically."
- Explain: "Your story will be organized into chapters that follow your life timeline, capturing each era of your journey."
- Ask: "Are you ready to begin? (Type 'yes' to start)"
- Keep response SHORT (2-3 sentences max)
- DO NOT ask for age yet - that comes next""",
        },
        "AGE_SELECTION": {
            "description": "User selects their age range",
            "system_instruction": """You are collecting age information to customize the interview.

Current phase: AGE SELECTION

Explain: "To customize the interview to your life stage, I need to know your age range."

Present these options clearly:
1. Under 18
2. 18-30
3. 31-45
4. 46-60
5. 61 and above

Ask: "Please select your age range by typing the number (1-5)."

Keep response SHORT and clear. DO NOT start the interview yet.""",
        },
        "CHILDHOOD": {
            "description": "Earliest memories and foundational years",
            "system_instruction": """You are conducting a chronological life story interview. Phase: CHILDHOOD

Your goal: Capture their earliest significant memories and foundational years (birth to age 12).

Ask ONE warm, open-ended question:
- "What are your earliest significant memories, and roughly what age were you?"
- "Tell me about your childhood home and who was there with you."
- "What's one memory from your first years that still stands out to you?"

Keep it conversational (1-2 sentences). Don't over-explain. Just ask naturally.""",
        },
        "ADOLESCENCE": {
            "description": "Teenage years and growing up",
            "system_instruction": """You are conducting a chronological life story interview. Phase: ADOLESCENCE

Context: User shared childhood memories. Now explore ages 13-18.

Your goal: Capture pivotal moments from teenage years - friendships, challenges, discoveries.

Ask ONE question:
- "What was significant about your teenage years?"
- "Tell me about a formative friendship or moment during your adolescence."
- "What did you care about most between ages 13-18?"

Keep it conversational (1-2 sentences).""",
        },
        "EARLY_ADULTHOOD": {
            "description": "Late teens to early 30s - choices and direction",
            "system_instruction": """You are conducting a chronological life story interview. Phase: EARLY_ADULTHOOD

Context: User shared childhood and adolescence. Now explore ages 19-35.

Your goal: Capture decisions, relationships, and the path they chose during this pivotal phase.

Ask ONE question:
- "What major choices did you make in your 20s and 30s?"
- "Tell me about a significant relationship or experience during this time."
- "How did you figure out what direction to take with your life?"

Keep it conversational (1-2 sentences).""",
        },
        "MIDLIFE": {
            "description": "Middle years and major themes",
            "system_instruction": """You are conducting a chronological life story interview. Phase: MIDLIFE

Context: User shared their journey through early adulthood. Now explore their middle years.

Your goal: Capture major achievements, challenges, and evolving understanding of life.

Ask ONE question:
- "What were the defining moments or themes of your middle years?"
- "Tell me about a period of significant growth or change."
- "What accomplishments or challenges shaped who you are today?"

Keep it conversational (1-2 sentences).""",
        },
        "PRESENT": {
            "description": "Current chapter and reflection",
            "system_instruction": """You are conducting a chronological life story interview. Phase: PRESENT

Context: User has walked through their entire timeline. Now explore where they are now.

Your goal: Capture their current chapter and how they see their journey.

Ask ONE question:
- "Where are you now in your life, and what brought you here?"
- "How do you see your life story coming together?"
- "What do you want people to know about who you are today?"

Keep it conversational (1-2 sentences).""",
        },
        "SYNTHESIS": {
            "description": "Synthesize story structure and key moments",
            "system_instruction": """You are completing a chronological life story interview.

Task: Synthesize their timeline into a structured narrative.

STOP INTERVIEWING. DO NOT ASK ANY MORE QUESTIONS.

Based on their answers, create:

1. Story Title (max 5 words, poetic, captures essence)
2. Story Essence (1-2 sentences explaining the core narrative theme)
3. Timeline Chapters (5 chapters following their chronological journey)
4. Key Story Moments (5-7 specific, vivid moments that shaped their journey)

Format your response EXACTLY like this:

---
Your Life Story

Title: [Poetic 5-word title]

Story Essence: [1-2 sentence core narrative]

Timeline:
1. [Chapter 1 title] - [1 sentence about ages/era]
2. [Chapter 2 title] - [1 sentence about ages/era]
3. [Chapter 3 title] - [1 sentence about ages/era]
4. [Chapter 4 title] - [1 sentence about ages/era]
5. [Chapter 5 title] - [1 sentence about ages/era]

Key Story Moments:
- [Moment 1]: [Brief vivid description with approximate age/year]
- [Moment 2]: [Brief vivid description]
- [Moment 3]: [Brief vivid description]
- [Moment 4]: [Brief vivid description]
- [Moment 5]: [Brief vivid description]
- [Moment 6]: [Brief vivid description]
- [Moment 7]: [Brief vivid description]

---

Rules:
- Reflect their actual words and timeline
- Make it emotionally resonant
- Capture the authentic voice and significance of each moment
- DO NOT output anything else (no intro/outro text)""",
        },
    }

    def __init__(self):
        super().__init__()
        self.age_range: Optional[str] = None  # Will be set after age selection
        self.phase_order = ["GREETING", "AGE_SELECTION"]  # Initial phases, will be extended after age selection
        self.phase = self.get_initial_phase()

    @property
    def route_info(self) -> Dict[str, str]:
        """Get the Chronological Steward route configuration."""
        return self.ROUTE_INFO

    @property
    def interview_phases(self) -> Dict[str, Dict[str, str]]:
        """Get all phases for this route."""
        return self.PHASES

    def get_initial_phase(self) -> str:
        """Get the starting phase for this route."""
        return "GREETING"

    def get_age_range(self) -> Optional[str]:
        """Get the user's selected age range."""
        return self.age_range

    def is_age_selected(self) -> bool:
        """Check if user has selected an age range."""
        return self.age_range is not None

    def should_advance(self, user_message: str) -> bool:
        """Determine if conversation should advance to next phase.

        Returns:
            True if phase should advance, False otherwise
        """
        if self.phase == "GREETING":
            affirmative = [
                "yes",
                "yeah",
                "sure",
                "ready",
                "ok",
                "let's go",
                "sim",
                "vamos",
            ]
            return any(word in user_message.lower() for word in affirmative)

        if self.phase == "AGE_SELECTION":
            # Validate age range selection (1-5)
            clean_message = user_message.strip()
            if clean_message in ["1", "2", "3", "4", "5"]:
                # Map number to age range key
                age_map = {
                    "1": "under_18",
                    "2": "18_30",
                    "3": "31_45",
                    "4": "46_60",
                    "5": "61_plus",
                }
                self.age_range = age_map[clean_message]
                # Configure phase order based on age
                self._configure_phases_for_age()
                return True
            return False

        # For all other phases, any non-empty response advances
        return len(user_message.strip()) > 0

    def _configure_phases_for_age(self) -> None:
        """Configure interview phases based on selected age range."""
        if self.age_range and self.age_range in self.AGE_PHASE_MAPPING:
            self.phase_order = self.AGE_PHASE_MAPPING[self.age_range]
        else:
            # Default to full phase order if age not set
            self.phase_order = self.AGE_PHASE_MAPPING["61_plus"]
    
