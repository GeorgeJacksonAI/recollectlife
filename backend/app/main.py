from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.endpoints import chat, messages

app = FastAPI(title="Life Story Game API")

# Configure CORS for Frontend
origins = [
    "http://localhost:5173",  # Local Vite (default)
    "http://localhost:8080",  # Local Vite (Lovable frontend)
    "http://localhost:3000",  # Alternative dev server
    "https://your-vercel-app.vercel.app",  # Vercel Prod
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(messages.router, prefix="/api/messages", tags=["messages"])


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Life Story Game API"}


# Register the Chat Router
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
