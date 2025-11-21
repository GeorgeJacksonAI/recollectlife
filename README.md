# Life Story Game – AI Interviewer

An AI-powered interviewer that transforms personal life stories into meaningful board game narratives. Built with React, Vite, Tailwind CSS (frontend) and Python serverless functions + Google Gemini (backend).

The AI conducts a compassionate 6-question interview across 7 storytelling routes to extract core motivations, turning points, and emotional themes, then synthesizes a structured narrative with title, chapters, and key moments.

## 🚀 Tech Stack

- **Frontend**: React 19, Vite 7, Tailwind CSS 4
- **Backend**: Python 3.9+ serverless functions (Vercel)
- **AI Model**: Google Gemini (fallback cascade: 2.5-flash → 2.0-flash → lite variants)
- **Architecture**: Stateless REST API, client-managed conversation state
- **Testing**: Pytest (backend), Vitest + React Testing Library (frontend)
- **Deployment**: Vercel (automatic from git push)

## 📋 Features

- 🎭 **7 Storytelling Routes**: Chronological, Thematic, Anecdotal, Interview, Reflective, Legacy, Custom
- 📖 **6-Phase Interview**: GREETING → ROUTE_SELECTION → 5 QUESTIONS → SYNTHESIS
- ✨ **AI Fallback Cascade**: Automatic retry across 6 Gemini models on rate limits
- 🔒 **Stateless Architecture**: No server-side sessions, scales horizontally
- 💬 **Context-Aware**: Client sends full conversation history each request
- 🎨 **Modern UI**: Dark mode chat interface with phase indicators
- ⚡ **Fast**: Serverless functions with 30s timeout, optimized fallback
- 🛡️ **Production-Ready**: Input validation, error handling, comprehensive tests

## 📁 Project Structure

```
/
├── api/                      # Vercel serverless functions (Python)
│   ├── chat.py              # POST /api/chat - main AI endpoint
│   ├── model_status.py      # GET /api/model-status - model info
│   ├── health.py            # GET /api/health - health check
│   └── ai_fallback.py       # Pure fallback logic (tested)
├── frontend/                 # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx          # Main chat UI (stateless)
│   │   ├── __tests__/       # Vitest component tests
│   │   └── test/setup.js    # Test configuration
│   ├── vite.config.js       # Build config (no proxy needed)
│   └── package.json         # Frontend dependencies + test scripts
├── src/                      # Shared Python logic
│   ├── conversation.py      # ConversationState, phase definitions
│   └── ...
├── tests/
│   └── python/              # Backend unit tests (37 passing)
├── vercel.json              # Vercel deployment config
├── requirements.txt         # Python deps for Vercel runtime
└── .env.example             # Environment variable template
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

**Backend (tests):**
```bash
conda create -y -n chatbot python=3.10
conda activate chatbot
pip install -r backend/requirements.txt
```

## 🧪 Testing

**Backend:** ✅ 37/37 passing
```bash
conda activate chatbot
pytest tests/python/ -v
```

**Frontend:**
```bash
cd frontend && npm test
```

## 🚀 Running Locally

**Vercel Dev (Recommended):**
```bash
vercel dev
# Frontend + API at http://localhost:3000
```

**Separate Servers (Legacy):**
```bash
# Terminal 1
cd frontend && npm run dev

# Terminal 2 (deprecated Flask)
conda activate chatbot
python backend/api.py
```

## 📡 API Endpoints

### `POST /api/chat`
```json
{
  "messages": [{"role": "user", "content": "Hello"}],
  "phase": "GREETING",
  "selected_route": "1"
}
```

### `GET /api/model-status`
Returns fallback cascade info.

### `GET /api/health`
Health check.

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

**Edit Questions:** Modify `src/conversation.py` `INTERVIEW_PHASES`

**Adjust Timeout:** Edit `vercel.json` `maxDuration`

## 🤝 Contributing

Focus areas: frontend tests, interview optimization, UI/UX, performance

## 📝 License

MIT License

## 🔗 Resources

- [Google AI Studio](https://aistudio.google.com/)
- [Vercel Docs](https://vercel.com/docs)
- [Gemini API Docs](https://ai.google.dev/docs)

---

**Built with ❤️ for preserving life stories through AI**

