from typing import TypedDict
from typing import Annotated
import operator

from src.schema import Section, SearchResult


# Main Agent Input State
class InputState(TypedDict):
    topic: str


# Main Agent State
class AgentState(TypedDict):
    topic: str
    sections: list[Section]
    researched_sections: Annotated[list[Section], operator.add]
    final_report: str


# Main Agent Output State
class OutputState(TypedDict):
    final_report: str


class ResearchAgentState(TypedDict):
    section: Section
    search_queries: list[str]
    search_results: list[SearchResult]
    section_context: str
    researched_sections: Annotated[list[Section], operator.add]
