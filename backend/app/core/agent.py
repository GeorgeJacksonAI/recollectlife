import os
from typing import Annotated, List, TypedDict, Union

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, StateGraph

load_dotenv()


# 1. Define State
# This tracks the conversation history passing through the graph
class AgentState(TypedDict):
    messages: List[BaseMessage]
    phase_instruction: str


# 2. Initialize Model (Gemini)
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY is not set in .env")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",  # Fallback to gemini-1.5-flash if needed
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True,  # Helper for Gemini's specific role requirements
)


# 3. Define Nodes
def chatbot_node(state: AgentState):
    """The core node that talks to the AI"""
    messages = state["messages"]
    phase_instruction = state["phase_instruction"]

    # Prepend the system instruction (Phase/Persona)
    # We do this dynamically so we can change instructions based on the Story Phase
    system_msg = SystemMessage(content=phase_instruction)

    # Call Gemini
    # We invoke the model with [SystemMessage, ...History]
    response = llm.invoke([system_msg] + messages)

    # Return the *new* message to append to state
    return {"messages": [response]}


# 4. Build Graph
workflow = StateGraph(AgentState)

# Add the node
workflow.add_node("chatbot", chatbot_node)

# Define flow (Start -> Chatbot -> End)
workflow.set_entry_point("chatbot")
workflow.add_edge("chatbot", END)

# 5. Compile the app
agent_app = workflow.compile()
