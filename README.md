# ⚡ AI-Powered Business Automation Hub

> Multi-agent automation system that understands natural language and orchestrates sub-agents to handle emails, calendar scheduling, Slack notifications, and web search — autonomously.

**Live Demo:** https://ai-automation-hub.onrender.com  
**Demo Video:** [Watch 2-min walkthrough](#)

## Architecture

## Key Design Decisions

- **LangGraph over raw LangChain** — Explicit state machine for agent routing; easier to debug, extend, and monitor than callback-based chains.
- **Claude claude-sonnet-4 as backbone** — Superior instruction-following for structured output extraction; no local model = stays within 512MB RAM on free hosting.
- **Upstash Redis (serverless)** — Zero cold-start, pay-per-request, GDPR-compliant EU region.
- **n8n as visual orchestration layer** — Allows non-technical stakeholders to audit and modify workflows without touching code.

## Tech Stack

| Layer | Technology |
|---|---|
| Orchestration | LangGraph 0.1 |
| LLM Backbone | Anthropic Claude claude-sonnet-4 |
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

## API Usage

```bash
curl -X POST https://ai-automation-hub.onrender.com/automate \
  -H "Content-Type: application/json" \
  -d '{"message": "Check my emails and send a summary to Slack"}'
```

## Example Automations

- **Email pipeline**: Fetches unread emails → Claude summarizes + categorizes → Slack notification with urgency flag
- **Meeting scheduler**: Parses natural language date/time → Creates Google Calendar event automatically  
- **Research agent**: Web search via Tavily → Claude synthesizes results with citations

