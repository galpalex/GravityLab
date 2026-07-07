from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from app.orchestrator import run_gravitylab_pipeline
import uvicorn
import os

app = FastAPI(title="GravityLab Multi-Agent Dashboard")

# Define request schema
class IdeaRequest(BaseModel):
    idea: str

# POST endpoint for running the multi-agent orchestration pipeline
@app.post("/run")
async def run_pipeline(request: IdeaRequest):
    if not request.idea.strip():
        raise HTTPException(status_code=400, detail="Idea input cannot be empty.")
    try:
        response = await run_gravitylab_pipeline(request.idea)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")

# Mount static files for frontend UI
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    # Redirect root to static index page
    return RedirectResponse(url="/static/index.html")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
