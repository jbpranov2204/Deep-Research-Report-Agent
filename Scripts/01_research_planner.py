from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "qwen/qwen3.8-27b"

model = ChatGroq(
    model= GROQ_MODEL,
    groq_api_key=GROQ_API_KEY
)


def research_planner(user_query):
    
    prompt = f"""
    You are a research planning assistant.

    Analyze the user's research request.

    Break it into smaller research questions.
    Generate specific web search queries.

    User request: {user_query}
    """

    response = model.invoke(prompt)

    return response.content

result = research_planner(
    "Research the impact of Agentic AI on enterprise automation"
)

print(result)