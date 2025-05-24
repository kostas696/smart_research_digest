import sqlite_patch
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="ollama/gemma:2b",  # or "llama3"
    stream=True
)

researcher = Agent(
    role="Researcher",
    goal="Summarize the main benefits of AI in sustainable farming.",
    backstory="Expert in agricultural innovation and AI tools for farmers.",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

task = Task(
    description="List 2 key benefits of AI in sustainable farming.",
    expected_output="Two concise bullet points.",
    agent=researcher
)

crew = Crew(
    agents=[researcher],
    tasks=[task],
    verbose=True,
    process=Process.sequential
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\nFinal Output:\n", result)