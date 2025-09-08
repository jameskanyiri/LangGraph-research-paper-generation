from src.state import AgentState
from langchain_core.runnables import RunnableConfig


async def synthesizer(state: AgentState, config: RunnableConfig):
    
    #get the completed sections
    completed_sections = state['completed_sections']
    
    completed_sections_str = "\n".join(completed_sections)
    
    return {"final_report": completed_sections_str}