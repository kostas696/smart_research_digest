from langchain_huggingface import HuggingFaceEndpoint
import os
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="google/gemma-2b",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    temperature=0.3,
    max_new_tokens=128
)

print(llm.invoke("Summarize the benefits of AI in farming"))