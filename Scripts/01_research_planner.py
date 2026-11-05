
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
import re

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "qwen/qwen3.8-27b"

model = ChatGroq(
    model=GROQ_MODEL,
    groq_api_key=GROQ_API_KEY
)


def research_planner(user_query):

    prompt = f"""
    You are an autonomous research planning assistant.

    Analyze the user's research request.

    1. Break it into smaller research questions.
    2. Generate specific web search queries.
    3. Group the queries according to research dimensions.

    Return a structured research plan with these headings:

    1. Decomposed Research Questions
    2. Specific Web Search Queries
    3. Recommended Source Types
    4. Suggested Research Workflow

    User request: {user_query}
    """

    response = model.invoke(prompt)

    return response.content

def extract_search_queries(planner_output):

    queries = []
    capture = False

    for line in planner_output.splitlines():

        line = line.strip()

        # Start capturing at Section 2
        if re.search(r"Specific Web Search Queries", line, re.I):
            capture = True
            continue

        # Stop at Section 3
        if capture and re.match(
            r"^#{1,6}\s*3\.", line
        ):
            break

        if not capture:
            continue

        # Match -, *, or numbered list items
        match = re.match(
            r"^(?:[-*]\s+|\d+[.)]\s+)(.+)$",
            line
        )

        if match:

            query = match.group(1).strip()

            # Remove Markdown emphasis and code formatting
            query = query.strip("*`\" ")

            if query:
                queries.append(query)

    return queries


if __name__ == "__main__":

    user_query = input("Enter research topic: ")

    planner_output = research_planner(user_query)

    print("\nRESEARCH PLAN:\n")
    print(planner_output)

    queries = extract_search_queries(planner_output)

    print("\nEXTRACTED SEARCH QUERIES:\n")

    for index, query in enumerate(queries, 1):
        print(f"{index}. {query}")

    print(f"\nTotal queries: {len(queries)}")
