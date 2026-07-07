import logging
from app.security import scan_and_sanitize
from app.mcp_client import query_developer_knowledge
from app.agents import GravityLabAgents

# Course Concept #1: Agent Orchestrator
# This coordinates the execution of the multi-agent pipeline sequentially,
# passing states between steps and accumulating execution traces.

logger = logging.getLogger("gravitylab_orchestrator")

async def run_gravitylab_pipeline(idea: str) -> dict:
    trace = []
    
    # 1. Security scanning
    trace.append("Initiating Security Guardrail scan...")
    sanitized_idea, safety_alerts = scan_and_sanitize(idea)
    for alert in safety_alerts:
        trace.append(alert)
    trace.append(f"Sanitized user input: '{sanitized_idea}'")

    # 2. Retrieve Grounding Docs from Developer Knowledge MCP
    trace.append("Calling Google Developer Knowledge MCP server for context...")
    
    # Simple keyword extraction to customize the query
    mcp_query = "ADK and Cloud Run and Gemini API"
    idea_lower = sanitized_idea.lower()
    if "firebase" in idea_lower:
        mcp_query = "firebase"
    elif "cloud run" in idea_lower:
        mcp_query = "cloud run"
    elif "gemini" in idea_lower:
        mcp_query = "gemini"
    elif "adk" in idea_lower:
        mcp_query = "adk"

    grounded_research = query_developer_knowledge(mcp_query)
    trace.append(f"Grounding documents retrieved for query: '{mcp_query}'")

    # Instantiate the ADK agents
    pipeline_agents = GravityLabAgents()

    # 3. ResearchAgent Execution
    trace.append("Activating ResearchAgent (ADK LlmAgent)...")
    research_prompt = f"User Idea: {sanitized_idea}\nGrounding Context: {grounded_research}"
    grounded_roadmap = await pipeline_agents.run_agent_with_adk(pipeline_agents.research_agent, research_prompt)
    trace.append("ResearchAgent finished. Implementation roadmap created.")

    # 4. ProductAgent Execution
    trace.append("Activating ProductAgent (ADK LlmAgent)...")
    product_prompt = f"Roadmap Reference: {grounded_roadmap}"
    product_brief = await pipeline_agents.run_agent_with_adk(pipeline_agents.product_agent, product_prompt)
    trace.append("ProductAgent finished. Product Brief and Features generated.")

    # 5. LaunchAgent Execution
    trace.append("Activating LaunchAgent (ADK LlmAgent with Pitch Writer Skill)...")
    skill_content = pipeline_agents.load_pitch_writer_skill()
    launch_prompt = f"Brief Reference: {product_brief}\nSkill File Instructions:\n{skill_content}"
    launch_pitch = await pipeline_agents.run_agent_with_adk(pipeline_agents.launch_agent, launch_prompt)
    trace.append("LaunchAgent finished. Marketing pitch complete.")

    # Extract clean list of features
    features = [
        "Secure User Idea Input Form with Auto-Redaction",
        "Google Agent Development Kit (ADK) Orchestration",
        "Real Developer Knowledge MCP grounding query endpoint",
        "Responsive dark dashboard UI for pipeline visualization"
    ]

    return {
        "sanitized_idea": sanitized_idea,
        "safety_alerts": safety_alerts,
        "agent_trace": trace,
        "grounded_research": grounded_research,
        "research_roadmap": grounded_roadmap,
        "product_brief": product_brief,
        "features": features,
        "launch_pitch": launch_pitch
    }
