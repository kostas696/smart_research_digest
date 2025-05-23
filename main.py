import sqlite_patch
from fastapi import FastAPI, Request
from pydantic import BaseModel
from crew_agents import run_crew

app = FastAPI()

class TopicRequest(BaseModel):
    topic: str

@app.post("/digest")
async def generate_digest(request: TopicRequest):
    result = run_crew(request.topic)
    return {"topic": request.topic, "digest": result}
