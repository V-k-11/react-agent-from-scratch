from duckduckgo_search import DDGS

DESCRIPTION = """web_search: Search the web for current information using DuckDuckGo (free, no API key).
Input: {"query": "search terms"}
Example: {"query": "latest AI news 2025"}"""

def web_search(params: dict) -> str:
    query = params.get("query", "").strip()
    if not query:
        return "Error: No query provided."
    try:
        results = DDGS().text(query, max_results=3)
        if not results:
            return "No results found."
        output = f"Search results for '{query}':\n"
        for i, r in enumerate(results, 1):
            output += f"\n[{i}] {r['title']}\n    {r['body']}\n    Source: {r['href']}\n"
        return output
    except Exception as e:
        return f"Search Error: {e}"