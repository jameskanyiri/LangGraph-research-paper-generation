from langgraph.graph import StateGraph, START, END

from src.state import AgentState, InputState, OutputState
from src.nodes.generate_sections import generate_sections
from src.configuration import Configuration
from src.nodes.generate_report import generate_report

from langgraph.types import Send
from src.nodes.research_agent.research_agent import research_agent


def assign_to_section_writer(state: AgentState):
    research_sections = [
        s for s in state["sections"] if getattr(s, "require_research", True)
    ]

    # Send research sections to research agents
    return [Send("research_agent", {"section": s}) for s in research_sections]


graph_builder = StateGraph(
    AgentState,
    input_schema=InputState,
    output_schema=OutputState,
    config_schema=Configuration,
)


graph_builder.add_node("generate_sections", generate_sections)
graph_builder.add_node("research_agent", research_agent)
graph_builder.add_node("generate_report", generate_report)

graph_builder.add_edge(START, "generate_sections")
graph_builder.add_conditional_edges(
    "generate_sections", assign_to_section_writer, ["research_agent"]
)

graph_builder.add_edge("research_agent", "generate_report")
graph_builder.add_edge("generate_report", END)


graph = graph_builder.compile()

# graph_builder.add_node("generate_sections", generate_sections)
# graph_builder.add_node("write_section", write_section)
# graph_builder.add_node("generate_report", generate_report)

# graph_builder.add_edge(START, "generate_sections")
# graph_builder.add_conditional_edges(
#     "generate_sections", assign_to_section_writer, ["write_section"]
# )

# graph_builder.add_edge("write_section", "generate_report")
# graph_builder.add_edge("generate_report", END)


# graph = graph_builder.compile()
