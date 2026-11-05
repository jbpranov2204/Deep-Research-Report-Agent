import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in environment variables. Please check your .env file.")

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


def web_search(query: str, max_results: int = 5, search_depth: str = "advanced", include_answer: bool = False):
    """
    Execute a web search using Tavily API for a given search query.

    Args:
        query (str): The search query to look up.
        max_results (int): Maximum number of search results to retrieve.
        search_depth (str): "basic" or "advanced".
        include_answer (bool): Whether to include an AI-generated answer.

    Returns:
        dict: Raw response dictionary from Tavily containing 'results', 'answer', etc.
    """
    try:
        response = tavily_client.search(
            query=query,
            max_results=max_results,
            search_depth=search_depth,
            include_answer=include_answer,
        )
        return response
    except Exception as e:
        print(f"Error during search for query '{query}': {e}")
        return {"query": query, "results": []}


def search_multiple_queries(queries: list[str], max_results_per_query: int = 3, deduplicate: bool = True) -> list[dict]:
    """
    Run searches for a list of queries (e.g., from research planner) and aggregate results.

    Args:
        queries (list[str]): List of query strings.
        max_results_per_query (int): Max results per individual query.
        deduplicate (bool): Whether to remove duplicate results based on URL.

    Returns:
        list[dict]: Flattened list of result dictionaries with title, url, content, and source query.
    """
    aggregated_results = []
    seen_urls = set()

    for query in queries:
        cleaned_query = query.strip()
        if not cleaned_query:
            continue

        search_data = web_search(cleaned_query, max_results=max_results_per_query)
        results = search_data.get("results", [])

        for item in results:
            url = item.get("url", "")
            if deduplicate and url in seen_urls:
                continue

            seen_urls.add(url)
            aggregated_results.append({
                "query": cleaned_query,
                "title": item.get("title", "No Title"),
                "url": url,
                "content": item.get("content", ""),
                "score": item.get("score", 0.0),
            })

    return aggregated_results


if __name__ == "__main__":
    search_input = input("Enter search query (press Enter for default 'Who is CR7?'): ").strip()
    query = search_input if input(search_input) else "Who is CR7?"

    print(f"\nSearching for: '{query}'...\n")
    search_response = web_search(query, max_results=3, search_depth="basic")

    results = search_response.get("results", [])
    print(f"Retrieved {len(results)} results:\n")

    for idx, item in enumerate(results, 1):
        print(f"--- Result {idx} ---")
        print(f"Title: {item.get('title')}")
        print(f"URL:   {item.get('url')}")
        print(f"Snippet:\n{item.get('content')}\n")
