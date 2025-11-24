"""Base class for all story routes."""

from abc import ABC, abstractmethod
from typing import Dict, List


class StoryRoute(ABC):
    """Abstract base class for story collection routes.

    Routes can optionally support age-based customization by implementing
    age range tracking and phase filtering logic.
    """

    def __init__(self):
        self.phase = None
        self.messages: List[Dict[str, str]] = []
        self.phase_order: List[str] = []
        self.metadata: Dict[str, str] = (
            {}
        )  # For storing route-specific metadata (age, preferences, etc.)

    @property
    @abstractmethod
    def route_info(self) -> Dict[str, str]:
        """Return route metadata (name, persona, goal, etc)."""
        pass

    @property
    @abstractmethod
    def interview_phases(self) -> Dict[str, Dict[str, str]]:
        """Return all phases for this route with their instructions."""
        pass

    @abstractmethod
    def get_initial_phase(self) -> str:
        """Return the starting phase for this route."""
        pass

    def get_current_phase(self) -> Dict[str, str]:
        """Returns the current phase configuration."""
        if self.phase is None:
            raise ValueError("Phase not initialized")
        return self.interview_phases[self.phase]

    def should_advance(
        self, user_message: str, explicit_transition: bool = False
    ) -> bool:
        """Determine if conversation should advance to next phase.

        Args:
            user_message: The user's message content
            explicit_transition: If True, user explicitly requested phase transition (via button)

        Returns:
            True if phase should advance, False to stay in current phase
        """
        # Default: only advance on explicit transition request
        return explicit_transition

    def advance_phase(self) -> str:
        """Move to next phase and return it."""
        if self.phase not in self.phase_order:
            raise ValueError(f"Unknown phase: {self.phase}")

        current_index = self.phase_order.index(self.phase)
        if current_index < len(self.phase_order) - 1:
            self.phase = self.phase_order[current_index + 1]
        return self.phase

    def add_message(self, role: str, content: str) -> None:
        """Add a message to conversation history."""
        self.messages.append({"role": role, "content": content})

    def get_messages(self) -> List[Dict[str, str]]:
        """Get conversation history."""
        return self.messages

    def is_complete(self) -> bool:
        """Check if route is complete (reached final phase)."""
        return self.phase == self.phase_order[-1]

    def reset(self) -> None:
        """Reset conversation state."""
        self.phase = self.get_initial_phase()
        self.messages = []
        self.metadata = {}

    def get_metadata(self, key: str) -> str:
        """Get metadata value by key."""
        return self.metadata.get(key, "")

    def set_metadata(self, key: str, value: str) -> None:
        """Set metadata value."""
        self.metadata[key] = value
