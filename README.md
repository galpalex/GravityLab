# GravityLab: Multi-Agent Project Planner

GravityLab is a multi-agent AI project planner that turns a raw product idea into grounded research, an implementation roadmap, a product brief, and a launch pitch. It was built for the Kaggle Freestyle Track to demonstrate multi-agent orchestration with Google ADK, real Google Developer Knowledge MCP grounding, security guardrails, and runtime-loaded agent skills. 


## Watch the Demo
[Watch the GravityLab demo on YouTube](https://youtu.be/lLffYP_K6g4)
This 38-second walkthrough shows the end-to-end GravityLab flow: user idea input, security scanning, MCP grounding, research generation, product planning, and launch messaging. 

## Problem

Turning an early-stage product idea into something structured and credible usually requires several manual steps: researching technical options, choosing an architecture, shaping a product brief, and translating it into a presentable concept. That process is slow, repetitive, and easy to derail when ideas are vague or when technical grounding is missing.

## Solution

GravityLab solves that problem by running a sequential AI workflow that transforms one user prompt into multiple decision-ready artifacts. It sanitizes the input, retrieves developer context from Google Developer Knowledge MCP, generates a technical roadmap through a research agent, creates a product brief through a product agent, and finishes with a launch pitch shaped by a reusable writing skill. 

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
The pipeline is intentionally linear so judges can easily follow what each component contributes to the final result. The interface also exposes the execution trace and security alerts to make the orchestration visible during a live demo.
---

## Core Concepts

### 1. ADK (Agent Development Kit)
- **Files**: [agents.py](file:///gravitylab-capstone/app/agents.py)
- **Demonstration**: GravityLab defines specialized agents with the official Google ADK LlmAgent and executes them through the ADK runner when credentials are available, while preserving a strong offline fallback for demo reliability.

### 2. MCP (Model Context Protocol)
- **Files**: [mcp_client.py](file:///gravitylab-capstone/app/mcp_client.py)
- **Demonstration**: The MCP client queries the Google Developer Knowledge MCP endpoint over JSON-RPC and formats returned documentation into grounded context for downstream agent steps, with fallback documents when connectivity or credentials are unavailable. 

### 3. Security
- **Files**: [security.py](file:///gravitylab-capstone/app/security.py)
- **Demonstration**: User prompts are scanned for prompt-injection patterns, email addresses, and possible API keys before entering the multi-agent workflow. The system redacts sensitive content and logs visible safety alerts.

### 4. Agent Skill
- **Files**: [pitch_writer.md](file:///gravitylab-capstone/app/skills/pitch_writer.md) and [agents.py](file:///gravitylab-capstone/app/agents.py#L42-L56)
- **Demonstration**: The LaunchAgent loads an external writing skill at runtime to structure the final pitch using a defined hook, solution, value proposition, and call-to-action format.

### 5. Antigravity Usage
- **Demonstration**: Antigravity was used as the primary build environment to scaffold, iterate, and refine the application, and that development workflow is reflected in the final demo and repository narrative.

---
## Project Structure

- `app/main.py` — FastAPI entrypoint and static file mounting
- `app/orchestrator.py` — sequential multi-agent pipeline orchestration
- `app/agents.py` — ADK agent definitions and fallback execution
- `app/mcp_client.py` — Google Developer Knowledge MCP integration and fallback handling
- `app/security.py` — prompt-injection and sensitive-data scanning
- `app/static/` — frontend dashboard for input, trace logs, alerts, and generated artifacts
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
   Live ADK and MCP are used when credentials are available. If they are missing, GravityLab falls back to local outputs so the demo still runs end to end. 

Usage
Enter a product or app idea in the dashboard input box.

Click Run GravityLab to trigger the pipeline.

Review the execution trace, any security alerts, grounded documentation, the research roadmap, the product brief, platform features, and the final launch pitch. 

Good test prompts include a Firebase-based task manager, an AI customer support workflow, or a Gemini-powered developer assistant, because those ideas visibly exercise both MCP grounding and the multi-agent chain. 

Notes
GravityLab is optimized for demo clarity rather than production deployment. The system is designed to make each stage of the pipeline visible and understandable for judges reviewing the repository, the UI, and the short video walkthrough
