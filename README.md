# Life Story Game – AI Interviewer

An AI-powered interviewer that transforms personal life stories into meaningful board game narratives. Built with React, Vite, Tailwind CSS (frontend) and Python serverless functions + Google Gemini (backend).

The AI conducts a compassionate chronological interview adapted to the user's age, exploring life phases from family history through childhood, adolescence, adulthood, and present day, then synthesizes a structured narrative with title, chapters, and key moments.

## 🚀 Tech Stack

- **Frontend**: React 19, Vite 7, Tailwind CSS 4
- **Backend**: Python 3.9+ serverless functions (Vercel)
- **AI Model**: Google Gemini (fallback cascade: 2.5-flash → 2.0-flash → lite variants)
- **Architecture**: Stateless REST API, client-managed conversation state
- **Testing**: Pytest (19 tests), Vitest + React Testing Library (8 tests)
- **Deployment**: Vercel (automatic from git push)

## 📋 Features

- 🎭 **Age-Aware Interview**: Phases adapt based on user's age range (under 18, 18-30, 31-45, 46-65, 65+)
- 📖 **Chronological Journey**: GREETING → AGE_SELECTION → FAMILY_HISTORY → CHILDHOOD → ADOLESCENCE → EARLY_ADULTHOOD → MIDLIFE → PRESENT → SYNTHESIS
- 🏷️ **Theme Tracking**: Select story themes (family, career, love, etc.) and track which have been addressed
- ✨ **AI Fallback Cascade**: Automatic retry across 6 Gemini models on rate limits
- 🔒 **Stateless Architecture**: No server-side sessions, scales horizontally
- 💬 **Context-Aware**: Client sends full conversation history each request
- 🎨 **Modern UI**: Dark mode chat interface with phase timeline and theme tags
- ⚡ **Fast**: Serverless functions with 30s timeout, optimized fallback
- 🛡️ **Production-Ready**: Input validation, error handling, comprehensive tests

## 📁 Project Structure

```
/
├── api/                          # Vercel serverless functions (Python)
│   ├── chat.py                   # POST /api/chat - main AI endpoint
│   ├── ai_fallback.py            # Gemini fallback cascade logic
│   ├── health.py                 # GET /api/health - health check
│   ├── model_status.py           # GET /api/model-status - model info
│   ├── summary.py                # GET /api/summary - story summary
│   └── routes/                   # Modular interview routes
│       ├── base.py               # StoryRoute abstract base class
│       └── chronological_steward.py  # Age-aware chronological route
├── frontend/                     # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx               # Main chat UI (stateless)
│   │   ├── App.css               # Tailwind styles
│   │   └── __tests__/            # Vitest component tests
│   ├── vite.config.js            # Build config
│   └── package.json              # Frontend dependencies
├── tests/
│   └── python/                   # Backend unit tests (19 tests)
│       ├── test_ai_fallback.py   # AI fallback logic tests
│       └── test_age_aware.py     # Age-aware phase tests
├── dev_server.py                 # Local development server
├── vercel.json                   # Vercel deployment config
├── requirements.txt              # Python deps for Vercel runtime
└── .env.example                  # Environment variable template
```

## Prerequisites

- **Node.js** 18+
- **Python** 3.9+
- **Vercel CLI** (optional): `npm install -g vercel`
- **Google AI Studio** account: [Get API key](https://aistudio.google.com/app/apikey)

## 🔧 Setup

### 1. Clone & Configure

```bash
git clone <repo-url>
cd openai_chatbot
```

Create `.env` (NEVER commit):
```bash
GEMINI_API_KEY="your_google_gemini_api_key_here"
```

### 2. Install Dependencies

**Frontend:**
```bash
cd frontend && npm install
```

**Backend (for tests):**
```bash
conda create -y -n chatbot python=3.10
conda activate chatbot
pip install -r requirements.txt
```

## 🧪 Testing

**Backend:** ✅ 19 tests
```bash
conda activate chatbot
pytest tests/python/ -v
```

**Frontend:** ✅ 8 tests
```bash
cd frontend && npm test
```

## 🚀 Running Locally

**Vercel Dev (Recommended):**
```bash
vercel dev
# Frontend + API at http://localhost:3000
```

**Dev Server (Alternative):**
```bash
python dev_server.py
# API at http://localhost:5328
```

## 📡 API Endpoints

### `POST /api/chat`

Main chat endpoint for AI conversation.

**Request:**
```json
{
  "messages": [{"role": "user", "content": "Hello"}],
  "route": "1",
  "phase": "GREETING",
  "age_range": "31_45",
  "advance_phase": false,
  "selected_tags": ["family", "career", "adventure"],
  "addressed_themes": ["family"]
}
```

**Response:**
```json
{
  "response": "AI generated response...",
  "model": "gemini-2.5-flash",
  "attempts": 1,
  "phase": "GREETING",
  "phase_order": ["GREETING", "AGE_SELECTION", "FAMILY_HISTORY", "..."],
  "phase_index": 0,
  "age_range": "31_45",
  "newly_addressed_themes": ["career"]
}
```

### `GET /api/model-status`
Returns fallback cascade info.

### `GET /api/health`
Health check.

### `GET /api/summary`
Generate story summary from conversation.

## 🚢 Vercel Deployment

### 1. Connect Repository
- Visit [vercel.com](https://vercel.com)
- Import GitHub repository

### 2. Configure Project
- **Build Command:** `cd frontend && npm install && npm run build`
- **Output Directory:** `frontend/dist`
- **Root Directory:** `./` (leave empty)

### 3. Environment Variables
Add in Vercel dashboard:
- `GEMINI_API_KEY`: Your Google AI Studio key

### 4. Deploy
```bash
vercel --prod
```

Auto-deploys on git push to `main`.

## 🔒 Security

- ✅ API keys server-side only (Vercel env)
- ✅ Input validation (50K char limit)
- ✅ Theme injection protection (sanitized user input)
- ✅ Never commit `.env`
- ✅ CORS headers in serverless functions

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **401 Auth Error** | Verify `GEMINI_API_KEY` in Vercel env vars |
| **429 Rate Limit** | Normal - fallback retries next model |
| **Empty responses** | Check Vercel function logs |
| **Build fails** | Delete `node_modules`, reinstall |

## 📦 Key Dependencies

**Backend:** `google-generativeai`, `pytest`  
**Frontend:** React 19, Vite 7, Vitest, Tailwind CSS 4

## 🎨 Customization

**Change Models:**
```bash
# In Vercel env vars
GEMINI_MODELS=gemini-2.5-flash,gemini-1.5-pro
```

**Add New Interview Routes:** Create a new class in `api/routes/` extending `StoryRoute` base class

**Modify Phases:** Edit `AGE_PHASE_MAPPING` in `api/routes/chronological_steward.py`

**Adjust Timeout:** Edit `vercel.json` `maxDuration`

## 🤝 Contributing

Focus areas: new interview routes, UI/UX improvements, additional theme keywords, test coverage

## 📝 License

MIT License

## 🔗 Resources

- [Google AI Studio](https://aistudio.google.com/)
- [Vercel Docs](https://vercel.com/docs)
- [Gemini API Docs](https://ai.google.dev/docs)

---

**Built with ❤️ for preserving life stories through AI**
