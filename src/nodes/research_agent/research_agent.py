from langchain_core.runnables import RunnableConfig
from src.configuration import Configuration
from langchain.chat_models import init_chat_model
from src.state import ResearchAgentState
from langgraph.graph import StateGraph, START, END

from src.nodes.research_agent.nodes.generate_queries import generate_queries
from src.nodes.research_agent.nodes.web_research import search_web



research_agent = StateGraph(ResearchAgentState)

research_agent.add_node("generate_queries", generate_queries)
research_agent.add_node("search_web", search_web)

research_agent.add_edge(START, "generate_queries")
research_agent.add_edge("generate_queries", "search_web")
research_agent.add_edge("search_web", END)

research_agent = research_agent.compile()