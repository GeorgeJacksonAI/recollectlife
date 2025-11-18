# Life Story Game – AI Interviewer

An AI-powered interviewer that transforms personal life stories into meaningful board game narratives. Built with React, Vite, Tailwind CSS (frontend) and Flask + Google Gemini (backend).

The AI conducts a compassionate 5-7 question interview to extract core motivations, turning points, and emotional themes from your life story, then synthesizes this into a structured narrative with a poetic title, reason statement, and chapter titles.

## 🚀 Tech Stack

- **Frontend**: React 19, Vite 7, Tailwind CSS 4
- **Backend**: Flask 3.0, Python 3.10
- **AI Model**: Google Gemini (gemini-2.0-flash-exp)
- **Architecture**: REST API with CORS-enabled Flask backend

## 📋 Features

- 🎭 **Compassionate AI Interviewer**: Documentary-style questioning that builds on previous answers
- 📖 **Life Story Extraction**: 5-7 open-ended questions uncovering motivations, turning points, themes
- ✨ **Story Synthesis**: Generates poetic title (max 5 words), reason statement, and 3-5 chapter titles
- 🔒 **Secure API Handling**: API key stored server-side, never exposed to browser
- 💬 **Context-Aware Conversation**: AI remembers prior answers and builds deeper questions
- 🎨 **Modern, Responsive UI**: Clean chat interface with Portuguese localization
- ⚡ **Fast Development**: Vite dev server with hot reload
- 🛡️ **Error Handling**: Comprehensive validation and user-friendly error messages

## 📁 Project Structure

```
/
├── backend/
│   ├── api.py              # Flask REST API with /api/chat endpoint
│   └── requirements.txt    # Python dependencies (Flask, Gemini, CORS)
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # React chat interface with interview flow
│   │   ├── main.jsx        # React entry point
│   │   └── index.css       # Tailwind CSS imports
│   ├── vite.config.js      # Dev server config + proxy to Flask backend
│   ├── eslint.config.js    # Flat ESLint configuration
│   └── package.json        # Frontend dependencies
├── docs/
│   └── whatthisprojectis.md  # Product specification & AI interview flow
├── script_chatbot.py       # Standalone Gemini test script
├── .env                    # Google API key (NEVER COMMIT)
├── .gitignore              # Protects secrets and build artifacts
└── README.md
```

## 🎯 How It Works

1. **Interview Phase**: AI asks 5-7 compassionate, open-ended questions:
   - Core motivation: "What do you want your loved ones to truly understand about you?"
   - Target audience: "Who is this for?"
   - Turning points: "What moment changed everything?"
   - Vulnerable moments: "When did you feel most exposed or transformed?"
   - Themes & emotions: "What recurring patterns do you notice?"

2. **Context Building**: AI references previous answers to create deeper follow-up questions

3. **Story Synthesis**: After interview, AI generates:
   - **Story Title**: Poetic, max 5 words capturing essence
   - **Reason**: One sentence explaining why this story matters
   - **Chapter Titles**: 3-5 titles forming narrative arc of life story

## Prerequisites

- Python 3.10+ (Conda recommended)
- Node.js 18+
- Google AI Studio account for Gemini API key

## 🔧 Setup

### 1. Clone & Configure Environment

```bash
git clone <your-repo-url>
cd openai_chatbot
```

Create `.env` in project root (NEVER commit this file):

```env
GOOGLE_API_KEY="YOUR_GEMINI_API_KEY_HERE"
```

Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2. Backend Setup

**Recommended: Use Conda environment**

```bash
conda create -y -n chatbot python=3.10
conda activate chatbot
pip install -r backend/requirements.txt
```

**Alternative: Use system Python with venv**

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
cd ..
```

## 🚀 Running Locally

### Terminal 1: Start Backend (Flask)

```bash
conda activate chatbot  # Or: source .venv/bin/activate
python backend/api.py
```

Backend runs at: `http://localhost:5000`

### Terminal 2: Start Frontend (Vite)

```bash
cd frontend
npm run dev
```

Frontend runs at: `http://localhost:5173`  
API calls to `/api/*` are automatically proxied to Flask backend.

### Health Check

```bash
curl http://localhost:5000/health
# Should return: {"status": "ok", "service": "AI Chatbot"}
```

## 📡 API Endpoints

### `POST /api/chat`

Processes conversation messages and returns AI interviewer response.

**Request Body:**

```json
{
  "messages": [
    {"role": "system", "content": "You are a compassionate life story coach..."},
    {"role": "user", "content": "I want to create a game about my journey as an immigrant."}
  ]
}
```

**Legacy Format (also supported):**

```json
{
  "message": "Tell me about your life story"
}
```

**Success Response (200):**

```json
{
  "response": "That's a powerful theme. What moment made you realize this journey was transforming you?"
}
```

**Error Response (4xx/5xx):**

```json
{
  "error": "Detailed error message"
}
```

### `GET /health`

Health check endpoint.

**Response (200):**

```json
{
  "status": "ok",
  "service": "AI Chatbot"
}
```

## 🔒 Security Notes

⚠️ **CRITICAL**: The API key `AIzaSyD3z0-IObrFT00in0qWCpKFME6bqD5EBa0` was accidentally committed to git history.

**Immediate Actions Required:**
1. Rotate the key in [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Update `.env` with new key
3. Verify `.env` is in `.gitignore` (already added)
4. Never commit `.env` or log `GOOGLE_API_KEY`

**Best Practices:**
- API key stays server-side only (Flask backend)
- Frontend never accesses `GOOGLE_API_KEY` directly
- All AI requests proxied through `/api/chat` endpoint
- Validate/sanitize all user inputs before sending to Gemini

## 🎨 Customization

### Change AI Model

Edit `backend/api.py`:

```python
model = genai.GenerativeModel("gemini-2.0-flash-exp")
# Options: gemini-2.0-flash-exp, gemini-1.5-pro, gemini-1.5-flash
```

### Customize Interview Questions

Modify the `SYSTEM_PROMPT` in `backend/api.py` to adjust:
- Interview persona (compassionate, documentary-style)
- Question focus areas (motivations, turning points, themes)
- Response length (currently 1-2 sentences)
- Synthesis output format (title + reason + chapters)

### Adjust UI Language

Frontend uses Portuguese by default. Edit `frontend/src/App.jsx`:

```javascript
// Initial system message
const [messages, setMessages] = useState([
  { role: "system", content: "You are a compassionate life story coach..." },
  { role: "assistant", content: "Olá! ..." },  // Change this
]);

// Placeholder text
placeholder="Digite sua mensagem..."  // Change this
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **401 / Authentication Error** | Rotate API key in Google AI Studio, ensure `.env` is loaded before starting Flask |
| **CORS Issues** | Verify `CORS(app)` is present in `backend/api.py` |
| **Frontend Cannot Reach API** | Ensure Flask runs on port 5000, check proxy config in `frontend/vite.config.js` |
| **Empty/No Responses** | Check request body format: `{ "messages": [...] }` or legacy `{ "message": "..." }` |
| **Flask Won't Start** | Activate conda environment: `conda activate chatbot`, verify dependencies installed |
| **"Module not found" Errors** | Run `pip install -r backend/requirements.txt` in activated environment |
| **Vite Build Errors** | Delete `node_modules` and reinstall: `cd frontend && rm -rf node_modules && npm install` |
| **API Key Not Loading** | Ensure `.env` is in project root (not `backend/` or `frontend/`), check file permissions |

## 📦 Dependencies

### Backend (Python)

- `flask==3.0.0` - Web framework
- `flask-cors==4.0.0` - CORS handling
- `google-generativeai==0.3.2` - Gemini API client
- `python-dotenv==1.0.0` - Environment variable management

### Frontend (Node.js)

- `react==19.2.0` - UI framework
- `vite==7.2.2` - Build tool and dev server
- `tailwindcss==4.1.17` - Utility-first CSS
- `eslint==9.39.1` - Code linting

## 🚀 Next Steps

**Current Implementation**: Generic AI chatbot with Gemini integration

**To Implement Life Story Interviewer**:
1. Update `SYSTEM_PROMPT` in `backend/api.py` with compassionate interviewer persona
2. Implement question sequencing (5-7 questions covering motivations, turning points, themes)
3. Add context-aware questioning logic (reference previous answers)
4. Implement story synthesis after interview completion (title + reason + chapters)
5. Update frontend to show interview progress and final synthesis output

See `docs/whatthisprojectis.md` for complete product specification.

## 📝 License

MIT License - Open source and available for modification.

## 🤝 Contributing

Contributions welcome! Focus areas:
- Interview question flow implementation
- Story synthesis algorithm
- Context-aware follow-up questions
- UI/UX improvements for interview experience
- Accessibility enhancements

