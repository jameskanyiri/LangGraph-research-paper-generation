from langchain.chat_models import init_chat_model
from src.state import AgentState
from pydantic import BaseModel, Field
from pydantic import ConfigDict
from langchain_core.runnables import RunnableConfig
from src.schema import Section


class Sections(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sections: list[Section] = Field(description="The sections of the topic")


structured_llm = init_chat_model(
    model="gpt-4.1-nano", model_provider="openai"
).with_structured_output(Sections)

AGENT_PROMPT = """
# Identity
You are a helpful assistant that generates a list of sections for a given topic.

# Task
You are provided with:
1. A **topic** that defines the subject.
2. A **template** that specifies the section titles to generate.

Your goal is to produce a **list of sections**, one for each item in the template.

# Guidelines
- Always generate **all sections listed in the template**, in the same order.
- Return a **list of sections** where each section has exactly:
  * `title`: A concise title (use the template wording as-is, or clarify if needed).
  * `description`: A topic-specific coverage plan for what to include in that section.
  * `require_research`: A boolean indicating whether this section needs external research (true) or can be written from other sections' content (false).
  * `search_queries`: Default empty list.
  * `search_results`: Default empty list.
  * `section_context`: Default empty string.
  
  
- Each description must:
  - Be grounded in the provided topic (avoid generic phrasing like "This section should...").
  - State **what content should be covered**, not just what the section “is about.”
  - Include:
    * **Purpose** of the section.
    * **Scope**: what belongs, what is out-of-scope.
    * **Key points, elements, or subtopics** tied to the topic.
    * **Methods, datasets, or evidence** if applicable.
    * **Examples, pitfalls, or best practices** if relevant.
    * **Deliverables** such as figures, tables, or diagrams if useful.
- The descriptions must be **actionable and specific**, so they can guide someone writing the section.
- Do not restate the section title in the description.
- Do not omit any section from the template.
- For `require_research`: Set to `true` for sections that need external data, studies, or current information (e.g., "Related Work", "Results", "Analysis"). Set to `false` for sections that can be written from other sections' content (e.g., "Introduction", "Conclusion", "Organization of the paper").

# Context

<Topic>
{topic}
</Topic>

<Template>
{template}
</Template>
"""


default_template = """
            # Research Paper — Analytical Paper

            ## Title Page
            - **Title**
            - **Authors & Affiliations**
            - **Correspondence**

            ## Abstract (150–250 words)
            - Concise summary of the research question, sources analyzed, methods of analysis, and main insights.
            - Should emphasize interpretation rather than taking a definitive stance.
            - No citations here.

            ## Introduction
            - Background and motivation
            - Research question(s) or guiding problem
            - Scope and boundaries of the analysis
            - Contributions (bulleted list of what the paper adds)
            - Organization of the paper

            ## Related Work / Literature Context
            - Synthesize prior literature and perspectives
            - Highlight debates, patterns, or trends relevant to the analysis
            - Identify gaps that your analysis addresses

            ## Analytical Framework / Method
            - Explain the framework, models, or methods used for analysis
            - Data, texts, or materials examined
            - Criteria for inclusion/exclusion
            - Assumptions and rationale

            ## Analysis
            - Systematic breakdown of the evidence (thematic, chronological, comparative, etc.)
            - Tables, figures, or diagrams to support interpretation
            - Multiple subsections allowed (###) to handle dimensions of analysis

            ## Discussion
            - Interpret the findings: what do they mean?
            - Connections back to literature
            - Strengths and limitations of your analysis
            - Broader implications

            ## Conclusion
            - Recap of key insights
            - What new understanding the analysis provides
            - Implications for theory, practice, or future research

            ## Future Work
            - Open questions raised by the analysis
            - Possible extensions of the framework or data
            - Recommendations for deeper or comparative studies

            ## References
            - Full bibliography in the required style (APA, IEEE, etc.)

            ## Appendices (optional)
            - Extended tables, coding schemes, or supplementary analysis
            """


def generate_sections(state: AgentState, config: RunnableConfig):

    # Get topic to generate sections for
    topic = state["topic"]

    # Load configuration
    configurable = config.get("configurable", {})

    template = configurable.get("document_template", default_template)

    system_instruction = AGENT_PROMPT.format(
        topic=topic,
        template=template,
    )

    messages = [
        {
            "role": "system",
            "content": system_instruction,
        },
        {
            "role": "user",
            "content": "Generate sections for the given topic",
        },
    ]

    response = structured_llm.invoke(messages)

    return {"sections": response.sections}
