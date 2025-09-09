from langgraph.graph import StateGraph, START, END

from src.state import AgentState
from src.nodes.generate_sections import generate_sections
from src.configuration import Configuration
from src.nodes.write_section import write_section
from src.nodes.synthesizer import synthesizer
from langgraph.types import Send


def assign_to_section_writer(state: AgentState):
    return [Send("write_section", {"section":s}) for s in state['sections']]
    
    

graph_builder = StateGraph(AgentState, config_schema=Configuration)


graph_builder.add_node("generate_sections", generate_sections)
graph_builder.add_node("write_section", write_section)
graph_builder.add_node("synthesize_sections", synthesizer)

graph_builder.add_edge(START, "generate_sections")
graph_builder.add_conditional_edges(
    "generate_sections", assign_to_section_writer, ["write_section"]
)

graph_builder.add_edge("write_section", "synthesize_sections")
graph_builder.add_edge("synthesize_sections", END)



graph = graph_builder.compile()
