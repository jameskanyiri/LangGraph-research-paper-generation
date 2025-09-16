from langchain_core.runnables import RunnableConfig
from src.state import ResearchAgentState
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

client = TavilyClient(api_key=TAVILY_API_KEY)


def search_web(state: ResearchAgentState, config: RunnableConfig):
    """This node searches the web for the search queries and returns the search results"""

    # Get the search queries
    search_queries = state["search_queries"]

    search_results = []

    for query in search_queries:
        results = client.search(query, max_results=5, topic="general")
        search_results.append(results)

    # Flatten individual result items across all queries
    flattened_results = []
    for per_query_response in search_results:
        if isinstance(per_query_response, dict):
            flattened_results.extend(per_query_response.get("results", []))

    context = "\n\n---\n\n".join(
        f"### {item.get('title', 'Untitled')}\n"
        f"**URL:** [{item.get('url', 'N/A')}]({item.get('url', '#')})\n\n"
        f"{item.get('content', '')}"
        for item in flattened_results
    )
    
    section = state["section"]
    if isinstance(section, BaseModel):
        section_dict = section.model_dump()
    else:
        section_dict = dict(section) 

    section_dict.setdefault("search_queries", [])
    section_dict.setdefault("search_results", [])
    section_dict.setdefault("section_context", "")

    section_dict["search_queries"] = search_queries
    section_dict["search_results"] = flattened_results
    section_dict["section_context"] = context

    return {
        "search_results": flattened_results,
        "section_context": context,
        "section": section_dict,                 
        "researched_sections": [section_dict], 
    }
