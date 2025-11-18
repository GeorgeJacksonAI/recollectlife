from src.conversation import ConversationState


def print_header():
    """Print colorful header"""
    print("\n" + "=" * 70)
    print("         LIFE STORY GAME - AI INTERVIEWER TEST")
    print("=" * 70 + "\n")


def print_phase_info(state: ConversationState):
    """Print current phase information"""
    phase_config = state.get_current_phase()

    if state.phase == "GREETING":
        print(f"\n[PHASE: {state.phase}]")
    elif "QUESTION" in state.phase:
        print(f"\n[PHASE: {state.phase}] - Question {state.question_count} of 5")
        print(f"Focus: {phase_config['description']}")
    elif state.phase == "SYNTHESIS":
        print(f"\n[PHASE: {state.phase}]")
        print("Generating your story structure...")

    print("-" * 70)


def print_ai_message(message: str):
    """Print AI message with formatting"""
    print(f"\nAI: {message}\n")


def get_user_input() -> str:
    """Get user input with prompt"""
    return input("You: ").strip()
