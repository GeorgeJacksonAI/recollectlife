"""
Snippet endpoints for story game cards.

GET /api/snippets/{story_id} - Get existing snippets for a story (cached)
POST /api/snippets/{story_id} - Generate/regenerate snippets for a story
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.core.auth import get_current_active_user
from backend.app.db.session import get_db
from backend.app.models.snippets import Snippet
from backend.app.models.story import Story
from backend.app.models.user import User
from backend.app.services.snippets import SnippetService

router = APIRouter()


# --- Pydantic Models ---


class SnippetItem(BaseModel):
    """Individual snippet for a game card."""

    id: Optional[int] = None
    title: str
    content: str
    phase: Optional[str] = None
    theme: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SnippetsResponse(BaseModel):
    """Response from snippet operations."""

    success: bool
    snippets: List[SnippetItem]
    count: int
    cached: Optional[bool] = None  # True if from database, False if freshly generated
    model: Optional[str] = None
    error: Optional[str] = None


class SnippetUpdate(BaseModel):
    """Request body for updating a snippet."""

    title: Optional[str] = None
    content: Optional[str] = None
    theme: Optional[str] = None
    phase: Optional[str] = None


# --- Endpoints ---


@router.get("/{story_id}", response_model=SnippetsResponse)
def get_snippets(
    story_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get existing snippets for a story from the database.

    Use this endpoint to check if snippets already exist before regenerating.
    If snippets exist, they will be returned with cached=True.
    If no snippets exist, returns empty array with cached=False.

    Requires authentication. User must own the story.

    Args:
        story_id: ID of the story
        current_user: Authenticated user (injected)
        db: Database session (injected)

    Returns:
        SnippetsResponse with cached snippets
    """
    # Verify story exists
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Story not found",
        )

    # Verify user owns the story
    if story.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this story",
        )

    # Get existing snippets
    service = SnippetService(db)
    result = service.get_existing_snippets(story_id)

    return SnippetsResponse(
        success=True,
        snippets=[SnippetItem(**s) for s in result["snippets"]],
        count=result["count"],
        cached=result["cached"],
        error=None,
    )


@router.post("/{story_id}", response_model=SnippetsResponse)
def generate_snippets(
    story_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Generate/regenerate story snippets (game cards) for a specific story.

    This endpoint:
    1. Deletes any existing snippets for the story
    2. Fetches all messages from the story
    3. Sends them to Gemini for analysis
    4. Saves and returns 3-8 snippets (max 300 chars each)

    Use GET /api/snippets/{story_id} to check for existing snippets first.

    Requires authentication. User must own the story.

    Args:
        story_id: ID of the story to generate snippets for
        current_user: Authenticated user (injected)
        db: Database session (injected)

    Returns:
        SnippetsResponse with generated snippets
    """
    # Verify story exists
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Story not found",
        )

    # Verify user owns the story
    if story.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this story",
        )

    # Generate snippets
    print(
        f"[API] POST /api/snippets/{story_id} - Generating snippets for story {story_id}"
    )
    service = SnippetService(db)

    try:
        result = service.generate_snippets(story_id)
        print(
            f"[API] Service returned: success={result.get('success')}, model={result.get('model')}"
        )

        if not result["success"]:
            # Return the error in the response body, not as HTTP error
            # This allows frontend to show a friendly message
            print(f"[API] Generation failed: {result.get('error')}")
            return SnippetsResponse(
                success=False,
                snippets=[],
                count=0,
                cached=False,
                model=result.get("model"),
                error=result.get("error", "Failed to generate snippets"),
            )

        print(f"[API] ✅ Success! Generated {result['count']} snippets")
        return SnippetsResponse(
            success=True,
            snippets=[SnippetItem(**snippet) for snippet in result["snippets"]],
            count=result["count"],
            cached=False,  # Freshly generated
            model=result.get("model"),
            error=None,
        )

    except Exception as e:
        print(f"[API] ❌ Unexpected error: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during snippet generation",
        )


@router.put("/{snippet_id}", response_model=SnippetItem)
def update_snippet(
    snippet_id: int,
    snippet_data: SnippetUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Update an individual snippet's title, content, theme, or phase.

    This endpoint allows users to edit their snippet cards after generation.
    Only the owner of the snippet (via story ownership) can update it.

    Args:
        snippet_id: ID of the snippet to update
        snippet_data: Fields to update (all optional)
        current_user: Authenticated user (injected)
        db: Database session (injected)

    Returns:
        Updated SnippetItem

    Raises:
        HTTPException 404: Snippet not found
        HTTPException 403: Not authorized (not owner)
    """
    # Find the snippet
    snippet = db.query(Snippet).filter(Snippet.id == snippet_id).first()
    if not snippet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Snippet not found",
        )

    # Verify user owns the snippet (via story ownership)
    story = db.query(Story).filter(Story.id == snippet.story_id).first()
    if not story or story.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this snippet",
        )

    # Update fields if provided
    if snippet_data.title is not None:
        snippet.title = snippet_data.title[:200]  # Enforce max length
    if snippet_data.content is not None:
        snippet.content = snippet_data.content[:300]  # Enforce 300 char limit
    if snippet_data.theme is not None:
        snippet.theme = snippet_data.theme
    if snippet_data.phase is not None:
        snippet.phase = snippet_data.phase

    db.commit()
    db.refresh(snippet)

    print(f"[API] ✅ Updated snippet {snippet_id}: title='{snippet.title[:30]}...'")

    return SnippetItem(
        id=snippet.id,
        title=snippet.title,
        content=snippet.content,
        phase=snippet.phase,
        theme=snippet.theme,
        created_at=snippet.created_at,
    )
