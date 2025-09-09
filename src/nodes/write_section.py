from src.state import SectionWriterState
from langchain_core.runnables import RunnableConfig
from src.configuration import Configuration
from langchain.chat_models import init_chat_model

section_writer_llm = init_chat_model(model="gpt-4",temperature=0)

AGENT_PROMPT = """
# Identity
You are a skilled research writing assistant.  tasked with writing {section_title} section of a research paper.
Your job is to draft **one section** of a research paper in clear, professional, and well-structured academic writing.

# Task
You are provided with:
1. A **section title** (the heading of the section).
2. A **section description** (what must be covered in the section).
3. A **template** (the overall structure and expectations for the paper).

You must write the section content in Markdown format.

# Guidelines
- Always begin with a level-2 Markdown heading (## {section_title}).
- Write in a **scholarly, precise, and explanatory** tone.
- Expand the section into **well-developed paragraphs** that follow the description.
- Where useful, include:
  * Explanations of key concepts
  * Comparative analysis
  * Examples, case studies, or applications
  * Best practices, challenges, or limitations
- Ensure smooth **flow and coherence** across paragraphs.
- Avoid redundancy: each section should focus on its specific role in the paper.
- If the section suggests subpoints (e.g., “evaluation, metrics, error analysis”), create **subheadings (###)** for clarity.
- Do **not** output references directly; instead, use placeholders like [Author, Year].
- Maintain Markdown formatting throughout.

# Section
Title: {section_title}  
Description: {section_description}  

# Template
{template}

# Output
Return only the section content in **Markdown format**.
Do not include extra commentary, explanations, or metadata.
"""



async def write_section(state: SectionWriterState, config: RunnableConfig):
    
    #get the section title and description
    section_title = state['section'].title
    
    section_description = state['section'].description
    
    #Load configuration
    configuration = config.get("configurable", {})
    
    template = configuration.get("template", "")
    
    #system instruction
    system_instruction = AGENT_PROMPT.format(
        section_title=section_title,
        section_description=section_description,
        template=template
    )   
    
    #messages
    messages = [
        {
            "role": "system",
            "content": system_instruction,
        },
        {
            "role": "user",
            "content": "Write the section content in Markdown format",
        }
    ]
    
    response = await section_writer_llm.ainvoke(messages)
    
    return {"completed_sections":[response.content]}