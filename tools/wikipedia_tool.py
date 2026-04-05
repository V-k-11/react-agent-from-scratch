import wikipedia

DESCRIPTION = """wikipedia: Fetch concise summaries from Wikipedia.
Input: {"query": "topic"}
Example: {"query": "Quantum entanglement"}, {"query": "Alan Turing"}"""

def wikipedia_search(params: dict) -> str:
    query = params.get("query", "").strip()
    if not query:
        return "Error: No query provided."
    try:
        wikipedia.set_lang("en")
        hits = wikipedia.search(query, results=1)
        if not hits:
            return f"No Wikipedia article found for '{query}'."
        summary = wikipedia.summary(hits[0], sentences=4, auto_suggest=False)
        return f"Wikipedia — {hits[0]}:\n{summary}"
    except wikipedia.exceptions.DisambiguationError as e:
        try:
            summary = wikipedia.summary(e.options[0], sentences=4, auto_suggest=False)
            return f"Wikipedia — {e.options[0]}:\n{summary}"
        except:
            return f"Disambiguation options: {e.options[:3]}"
    except Exception as e:
        return f"Wikipedia Error: {e}"