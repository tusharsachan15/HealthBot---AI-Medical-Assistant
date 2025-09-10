import requests
from config.config import Config

def web_search(query):
    """
    Perform real-time web search using SERPER API.
    Returns list of results (title + link)
    """
    if not Config.SERPER_API_KEY:
        return ["Web search not available. Missing SERPER_API_KEY."]

    url = "https://google.serper.dev/search"
    payload = {"q": query, "num": Config.SEARCH_RESULTS_LIMIT}
    headers = {
        "X-API-KEY": Config.SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        resp = requests.post(url, headers=headers, json=payload).json()
        results = []
        for item in resp.get("organic", []):
            title = item.get("title", "").strip()
            link = item.get("link", "").strip()
            if title and link:
                results.append(f"{title} - {link}")
        return results if results else ["No search results found."]
    except Exception as e:
        return [f"Error in web search: {str(e)}"]
