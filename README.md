# TripMate AI

An AI travel-planning assistant. A LangGraph agent (Groq LLM + Tavily web search + airport/country lookup tools) served by FastAPI, with a React + TypeScript + RTK Query chat frontend.

```
tripmate_AI/
├── backend/    FastAPI + LangGraph agent (Postgres-backed conversation memory)
└── frontend/   React + TypeScript + Vite + Redux Toolkit / RTK Query + ESLint
```

## Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add GROQ_API_KEY, TAVILY_API_KEY, DATABASE_URL
uvicorn app.main:app --reload --port 8000
```

If `DATABASE_URL` is empty, conversations are kept in memory and lost on restart.
API docs: http://localhost:8000/docs

| Method | Path                     | Description                          |
| ------ | ------------------------ | ------------------------------------ |
| GET    | `/api/health`            | Health check                         |
| POST   | `/api/chat`              | `{ message, thread_id? }` → reply    |
| GET    | `/api/chat/{thread_id}`  | Conversation history for a thread    |

## Frontend

```bash
cd frontend
npm install
npm run dev     # http://localhost:5173 (proxies /api to :8000)
npm run lint
npm run build
```
