# 🧠 AI Automation Hub

A web-based automation system built with FastAPI that routes user commands to different workflow modules such as Gmail, Slack, and Google Calendar.

The project demonstrates API integration, workflow routing, and cloud deployment using a simple multi-module architecture.

## Live Demo

https://ai-automation-hub-42r9.onrender.com

---

# Features

### Gmail Integration

* Read recent emails using Gmail API
* Display email subjects/content previews
* Tested successfully on local environment with Google OAuth

### Calendar Integration

* Create calendar events through Google Calendar API
* Return event creation status
* Generate event links when Google Calendar API is configured

### Slack Integration

* Send notifications through Slack Webhooks
* Modular Slack agent architecture

### Workflow Routing

The system analyzes user commands and routes them to the appropriate module.

Examples:

* read email
* notify slack
* schedule meeting
* read email and notify slack
* read email and schedule meeting

---

# Architecture

User
↓
Web UI (HTML + JavaScript)
↓
FastAPI Backend
↓
Command Router
↓
+-------------+
| Gmail Agent |
+-------------+

+-------------+
| Slack Agent |
+-------------+

+----------------+
| Calendar Agent |
+----------------+

↓

Response Formatter
↓

Web UI

---

# Tech Stack

| Layer           | Technology          |
| --------------- | ------------------- |
| Backend         | FastAPI             |
| Language        | Python 3.11         |
| Frontend        | HTML + JavaScript   |
| API Server      | Uvicorn             |
| Email           | Gmail API           |
| Calendar        | Google Calendar API |
| Notifications   | Slack Webhooks      |
| Deployment      | Render              |
| Version Control | Git + GitHub        |

---

# Project Structure

app/

├── agents/

│ ├── gmail_agent.py

│ ├── slack_agent.py

│ ├── calendar_agent.py

│ └── graph.py

├── api/

│ └── routes.py

├── core/

├── frontend/

│ └── index.html

└── main.py

---

# API Example

POST /automate

Request

{
"message": "read email and schedule meeting"
}

Response

{
"status": "success",
"result": {
"intent": "multi_agent_task",
"gmail": "...",
"calendar": "created"
}
}

---

# Example Commands

read email

read email and notify slack

schedule meeting

read email and schedule meeting

notify slack

---

# Current Status

Implemented

✅ Web UI

✅ FastAPI Backend

✅ Command Routing

✅ Gmail Module

✅ Slack Module

✅ Calendar Module

✅ Render Deployment

In Progress

⚠ Production Gmail OAuth on Render

⚠ Production Slack Configuration

⚠ Production Calendar Workflow

⚠ Advanced AI Agent Orchestration

---

# Learning Goals

This project was built to explore:

* Workflow automation
* API integrations
* FastAPI development
* Cloud deployment
* Modular agent architecture
* Google Workspace integrations

---

# Author

Natcha Aimthap

Computer Engineering Graduate

Thailand
