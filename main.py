import sqlite_patch
from fastapi import FastAPI
from pydantic import BaseModel
from crew_agents import run_crew

app = FastAPI()

class TopicInput(BaseModel):
    topic: str

@app.post("/digest")
def generate_digest(payload: TopicInput):
    result = run_crew(payload.topic)
    return {"topic": payload.topic, "digest": result}
