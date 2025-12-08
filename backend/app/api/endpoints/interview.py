from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.services.interview import InterviewService

router = APIRouter()


# --- Pydantic Models ---
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    id: int
    role: str
    content: str
    phase: str


# --- Endpoints ---


@router.post("/{story_id}", response_model=ChatResponse)
def chat_with_agent(story_id: int, request: ChatRequest, db: Session = Depends(get_db)):
    """
    Send a message to the AI interviewer for a specific story.
    """
    service = InterviewService(db)
    try:
        # Process the chat (Save User -> Think -> Save AI)
        ai_message = service.process_chat(story_id, request.message)

        return {
            "id": ai_message.id,
            "role": ai_message.role,
            "content": ai_message.content,
            "phase": ai_message.phase_context or "UNKNOWN",
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Error processing chat: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
