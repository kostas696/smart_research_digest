import sqlite_patch
from crewai import Agent, Task, Crew
#from langchain_huggingface import HuggingFaceEndpoint
from langchain_ollama import ChatOllama
from duckduckgo_search import DDGS
from dotenv import load_dotenv
import os

load_dotenv()

# llm = HuggingFaceEndpoint(
#     repo_id="google/gemma-2b",
#     huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
#     temperature=0.3,
#     max_new_tokens=50
# )

llm = ChatOllama(model="phi3")

def get_links(query):
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=2)
            if not results:
                return "No relevant links found."
            return "\n".join([res["body"] for res in results if "body" in res])
    except Exception as e:
        print("DuckDuckGo search error:", e)
        return "Search failed."

def run_crew(topic):
    try:
        context = get_links(topic)[:500]
        print(f"Context gathered:\n{context}") 
        researcher = Agent(
            role="Researcher",
            goal="Quickly collect 2-3 main points on the topic.",
            backstory="An expert in AI trends and sustainability, focused on gathering valuable insights.",
            llm=llm
        )

        analyst = Agent(
            role="Analyst",
            goal="Extract 1-2 core insights from the research.",
            backstory="A strategic thinker who processes research data into actionable insights.",
            llm=llm
        )

        writer = Agent(
            role="Writer",
            goal="Write a very short summary for a newsletter.",
            backstory="A communications specialist skilled in translating insights into engaging summaries.",
            llm=llm
        )

        task1 = Task(
            description=f"Quickly identify 2-3 main points about: {topic}\nContext:\n{context}",
            expected_output="A very brief list of 2-3 key findings.",
            agent=researcher
        )

        task2 = Task(
            description="Analyze the brief research findings and identify 1-2 quick trends.",
            expected_output="A very short summary of 1-2 insights derived from the research.",
            agent=analyst
        )

        task3 = Task(
            description="Write a single, concise sentence for a newsletter digest based on the insights.",
            expected_output="A single, short sentence digest.",
            agent=writer
        )

        crew = Crew(agents=[researcher, analyst, writer], tasks=[task1, task2, task3], verbose=True)
        return crew.kickoff()
    except Exception as e:
        import traceback
        print("Error in run_crew():", e)
        traceback.print_exc()
        return "Internal processing error"