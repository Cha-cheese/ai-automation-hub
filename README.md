# ⚡ AI-Powered Business Automation Hub

> Multi-agent automation system that understands natural language and orchestrates sub-agents to handle emails, calendar scheduling, Slack notifications, and web search — autonomously.

**Live Demo:** https://ai-automation-hub.onrender.com  
**Demo Video:** [Watch 2-min walkthrough](#)

## Architecture

## Key Design Decisions

- **LangGraph over raw LangChain** — Explicit state machine for agent routing; easier to debug, extend, and monitor than callback-based chains.
- **Gemini API as backbone** — Hosted LLM keeps the app inside Render's small-memory free tier; no local `torch`/`transformers` runtime.
- **Upstash Redis (serverless)** — Zero cold-start, pay-per-request, GDPR-compliant EU region.
- **n8n as visual orchestration layer** — Allows non-technical stakeholders to audit and modify workflows without touching code.

## Tech Stack

| Layer | Technology |
|---|---|
| Orchestration | LangGraph 0.1 |
| LLM Backbone | Gemini API (`gemini-2.0-flash` by default) |
| API Framework | FastAPI + Uvicorn |
| Email | Gmail API (Service Account) |
| Calendar | Google Calendar API |
| Notifications | Slack SDK |
| Web Search | Tavily |
| State Store | Upstash Redis |
| Visual Workflows | n8n |
| Container | Docker (python:3.11-slim) |
| Hosting | Render.com (Frankfurt region) |

## Quickstart

```bash
git clone https://github.com/YOUR_USERNAME/ai-automation-hub
cd ai-automation-hub
cp .env.example .env
# Fill in API keys in .env
docker-compose up
```

API: `http://localhost:8000`  
n8n: `http://localhost:5678`

## Deployment

Render is a good portfolio/demo choice, but it is not required. This app is a standard Dockerized FastAPI service, so it can run on Render, Railway, Fly.io, Google Cloud Run, AWS App Runner, Azure Container Apps, or a VPS. For EU-focused demos, choose an EU region and keep API keys in the platform's environment variables.

## API Usage

```bash
curl -X POST https://ai-automation-hub.onrender.com/automate \
  -H "Content-Type: application/json" \
  -d '{"message": "Check my emails and send a summary to Slack"}'
```

## Example Automations

- **Email pipeline**: Fetches unread emails → Gemini summarizes + categorizes → Slack notification with urgency flag
- **Meeting scheduler**: Parses natural language date/time → Creates Google Calendar event automatically  
- **Research agent**: Web search via Tavily → Gemini synthesizes results with citations

## Troubleshooting

If the UI stays on `Agents working...`, check these first:

- `/automate` now has a backend timeout (`REQUEST_TIMEOUT_SECONDS`, default 45s) and the browser aborts after 50s.
- Set `GOOGLE_API_KEY`; without it, the app returns a demo-mode response instead of hanging.
- Set `TAVILY_API_KEY` only when you need live search. Tavily calls time out after `TAVILY_TIMEOUT_SECONDS`.
- Redis is optional for the demo. If `UPSTASH_REDIS_REST_URL` or token is missing, automations still run but `/history/{session_id}` is disabled.

