from typing import TypedDict
from typing import Annotated
import operator

class Section(TypedDict):
    title: str
    content: str
    
    
class InputState(TypedDict):
    topic: str

class AgentState(TypedDict):
    topic: str
    sections: list[Section]
    completed_sections: Annotated[list[Section], operator.add]
    final_report: str
    
class OutputState(TypedDict):
    final_report: str
  
class SectionWriterState(TypedDict):
    section: Section
    completed_sections: Annotated[list[Section], operator.add]