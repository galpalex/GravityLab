import os
import requests
import logging

# Course Concept #2: MCP Integration
# This client integrates directly with the real Google Developer Knowledge MCP Server
# over JSON-RPC HTTP protocol. It falls back gracefully if authentication or connectivity fails.

logger = logging.getLogger("mcp_client")

FALLBACK_DOCS = {
    "firebase": """
Google Cloud / Firebase Grounding Info:
- Firebase is an app development platform that helps you build and grow apps.
- Core capabilities: Cloud Firestore (NoSQL database), Firebase Auth (identity management), Cloud Functions (serverless backend), and Firebase Hosting.
- Best Practice: Use the Firebase Local Emulator Suite during local development.
""",
    "cloud run": """
Google Cloud Run Grounding Info:
- Cloud Run is a managed compute platform that enables you to run containerized applications serverlessly.
- Key features: Automatic scaling (down to zero), HTTP/2 and WebSocket support, integration with VPC, Cloud SQL, and Secret Manager.
- Best Practice: Keep container footprint small to reduce cold start times.
""",
    "gemini": """
Google Gemini API Grounding Info:
- Gemini API provides access to Google's most capable multimodal models (Gemini 2.5 Flash, Gemini 2.0 Flash).
- Key parameters: temperature (controls randomness), top_p (nucleus sampling), top_k.
- Best Practice: Always sanitize inputs and use system instructions to guide model persona.
""",
    "adk": """
Google Agent Development Kit (ADK) Grounding Info:
- Open-source Python framework designed for building, evaluating, and deploying reliable AI agents.
- Core classes: LlmAgent (for reasoning), SequentialAgent (for multi-step flows), InMemorySessionService.
- Best Practice: Pass the same SessionContext across sequential agents to preserve conversation state.
"""
}

def get_fallback_docs(query: str, reason: str) -> str:
    """Returns local official-looking document snippets as a fallback when MCP is offline."""
    query_lower = query.lower()
    matched_docs = []
    for key, doc in FALLBACK_DOCS.items():
        if key in query_lower:
            matched_docs.append(doc)
    
    status_header = f"[MCP Integration: Offline Fallback (Reason: {reason})]\n"
    if matched_docs:
        return status_header + "\n".join(matched_docs)
    
    return status_header + """
Google Developer Knowledge Grounding Info:
- General recommendations: Use Python 3.10+ and standard GCP client libraries.
- For AI features, use Vertex AI or the Gemini API via standard SDKs.
"""

def query_developer_knowledge(query_text: str) -> str:
    """
    Calls the real Google Developer Knowledge MCP server using HTTP POST JSON-RPC.
    Falls back gracefully if the server is offline or keys are missing.
    """
    # Look for standard Google API keys or Developer Knowledge keys in the environment
    api_key = os.getenv("DEVELOPER_KNOWLEDGE_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    url = "https://developerknowledge.googleapis.com/mcp"
    
    if not api_key:
        logger.info("No Developer Knowledge API key found. Using fallback grounding docs.")
        return get_fallback_docs(query_text, "No API key configured in environment.")

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key
    }
    
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "id": 1,
        "params": {
            "name": "answer_query",
            "arguments": {
                "query": f"Fetch official Google developer documentation and examples for: {query_text}"
            }
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=50)
        if response.status_code == 200:
            result = response.json()
            if "error" in result:
                return get_fallback_docs(query_text, f"MCP Server returned JSON-RPC error: {result['error']}")
            
            # Extract content text from MCP response standard format
            # Response: {"jsonrpc": "2.0", "result": {"content": [{"type": "text", "text": "..."}]}}
            mcp_result = result.get("result", {})
            content = mcp_result.get("content", [])
            if content and isinstance(content, list):
                first_content = content[0]
                if isinstance(first_content, dict) and "text" in first_content:
                    raw_text = first_content['text']
                    import json
                    try:
                        inner_json = json.loads(raw_text)
                        if isinstance(inner_json, dict) and "answerText" in inner_json:
                            answer = inner_json["answerText"]
                            refs = inner_json.get("references", [])
                            formatted_text = f"[MCP Integration: Live Server]\n{answer}"
                            if refs:
                                formatted_text += "\n\nSources:\n" + "\n".join([f"- {ref}" for ref in refs])
                            return formatted_text
                    except Exception:
                        pass
                    return f"[MCP Integration: Live Server]\n{raw_text}"
            
            return f"[MCP Integration: Live Server]\n{str(mcp_result)}"
        else:
            return get_fallback_docs(query_text, f"MCP server responded with HTTP status code {response.status_code}")
    except Exception as e:
        logger.warning(f"Failed to connect to real MCP server: {e}")
        return get_fallback_docs(query_text, f"Unable to reach server: {str(e)}")
