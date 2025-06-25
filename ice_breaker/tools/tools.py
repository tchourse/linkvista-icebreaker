from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_url_tavily(name: str):
    """Searches for a LinkedIn profile page."""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res
