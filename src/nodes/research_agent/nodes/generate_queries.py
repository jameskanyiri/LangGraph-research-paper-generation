from src.state import ResearchAgentState
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model


class SearchQueries(BaseModel):
    queries: list[str] = Field(
        description="The search queries to find relevant information."
    )


structured_llm = init_chat_model(
    model="gpt-4.1-nano", model_provider="openai"
).with_structured_output(SearchQueries)


GENERATE_QUERIES_PROMPT = """

You are a helpful assistant that generates search queries for the {section_title} section of a research paper.

# Task
You are provided with:
1. A **section title** (the heading of the section).
2. A **section description** (what must be covered in the section).

Your goal is to produce a **list of search queries** to find relevant information that will be used to write the section.

# Guidelines
- Make sure the generated search queries are specific to the section and its description.
- Make sure the generated search queries are not too broad or too narrow.
- Make sure the search queries are suitable for the web search engine.

# SECTION TITLE
<section_title>
{section_title}
</section_title>

# SECTION DESCRIPTION
<section_description>
{section_description}
</section_description>
"""


def generate_queries(state: ResearchAgentState, config: RunnableConfig):
    """
    This node takes what the section is about and generates search queries to find relevant information.
    """

    # Get the section title
    section_title = state["section"].title

    # Get the section description
    section_description = state["section"].description

    system_instruction = GENERATE_QUERIES_PROMPT.format(
        section_title=section_title,
        section_description=section_description,
    )

    # Generate search queries
    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": "Generate search queries for the given section."},
    ]

    response = structured_llm.invoke(messages)

    return {"search_queries": response.queries}
