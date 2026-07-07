# GravityLab: Multi-Agent Project Planner

GravityLab turns a raw app idea into a grounded product brief, feature list, and launch pitch using ADK agents and Google Developer Knowledge MCP. It is built for the Kaggle Freestyle Track to clearly demonstrate four course concepts: multi-agent ADK pipelines, real MCP integration, security guardrails, and agent skills.

## Watch the Demo
[Watch the GravityLab demo on YouTube](https://youtu.be/lLffYP_K6g4)

## Architecture & Workflow

```
[ User Input / Idea ]
        |
        v
 [ Security Module ] (Checks injection, redacts API keys/emails)
        |
        v
[ Developer Knowledge MCP Client ] (Retrieves official Google docs context)
        |
        v
  [ ResearchAgent ] (Generates grounded architecture roadmap)
        |
        v
   [ ProductAgent ] (Structures PM brief and feature definitions)
        |
        v
    [ LaunchAgent ] (Uses pitch_writer.md skill to compose marketing copy)
        |
        v
 [ Modern Dashboard UI ] (Presents execution trace and final output)
```

---

## Where the course concepts are demonstrated

### 1. ADK (Agent Development Kit)
- **Files**: [agents.py](file:///gravitylab-capstone/app/agents.py)
- **Demonstration**: I import and instantiate `LlmAgent` and `Runner` directly from the official Google Agent Development Kit (`google-adk`). If a Gemini API key is configured, it runs the pipeline live; if not, it triggers a robust offline fallback to guarantee a clean demo.

### 2. MCP (Model Context Protocol)
- **Files**: [mcp_client.py](file:///gravitylab-capstone/app/mcp_client.py)
- **Demonstration**: The `ResearchAgent` queries the real Google Developer Knowledge MCP server over HTTP JSON-RPC to fetch official reference guidelines for Google Cloud, Firebase, and Gemini. If offline or credentials are missing, it falls back to styled mock developer references.

### 3. Security
- **Files**: [security.py](file:///gravitylab-capstone/app/security.py)
- **Demonstration**: Intercepts user inputs, scans for prompt injection expressions (e.g. "ignore previous instructions"), redacts PII (emails) and API credentials using regex guardrails, and outputs alerts directly to a logger.

### 4. Agent Skill
- **Files**: [pitch_writer.md](file:///gravitylab-capstone/app/skills/pitch_writer.md) and [agents.py](file:///gravitylab-capstone/app/agents.py#L42-L56)
- **Demonstration**: The `LaunchAgent` loads external copywriting guidelines from `app/skills/pitch_writer.md` at run-time, applying specific structures (Hook, Solution, Value Props, Call-to-Action) to write the product pitch.

### 5. Antigravity in video
- **Demonstration**: Antigravity is showcased as the primary pair-programming agent used to scaffold and code this application. The dynamic execution logger in the UI updates sequentially, allowing judges to trace the exact agent actions.

---
## Project Structure


gravitylab-capstone/
├── README.md
├── requirements.txt
├── .env.example
├── app/
│   ├── _pycache_/
│   ├── main.py
│   ├── orchestrator.py
│   ├── agents.py
│   ├── mcp_client.py
│   ├── security.py
│   ├── skills/
│   │   └── pitch_writer.md
│   └── static/
│       ├── index.html
│       ├── app.js
│       └── style.css
└── screenshots/
    └── GravityLab in action.png
    └── security guardrails.png

- `app/main.py` — FastAPI entrypoint and static file mounting
- `app/orchestrator.py` — sequential multi-agent pipeline orchestration
- `app/agents.py` — ADK agent definitions and fallback execution
- `app/mcp_client.py` — Google Developer Knowledge MCP integration
- `app/static/` — dashboard frontend
---

## Setup & Running Locally

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Keys (Optional)**:
   Create a `.env` file in the project root (already loaded via `python-dotenv`):
   ```bash
   GEMINI_API_KEY=your-gemini-key
   DEVELOPER_KNOWLEDGE_API_KEY=your-google-api-key
   ```
   Live ADK and MCP are used when credentials are available; otherwise the app falls back to local outputs so judges can always run the demo.

3. **Start the Application**:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

4. **Access the Dashboard**:
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser.
