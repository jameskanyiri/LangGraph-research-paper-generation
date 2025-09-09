from langchain.chat_models import init_chat_model
from src.state import AgentState
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableConfig


class Section(BaseModel):
    title: str = Field(description="The title of the section")
    description: str = Field(
        description="A well detailed description of what should be included in the section"
    )


class Sections(BaseModel):
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
  * `title`: A concise title (use the template wording as-is, or make it clearer if necessary).
  * `description`: A well-detailed explanation of what should be included in that section.
- Each description must include:
  - The **purpose** of the section.
  - The **scope**: what content belongs (and what does not).
  - The **key points, elements, or subtopics** to cover.
  - Where useful, provide **examples**, **common pitfalls**, or **best practices**.
- Ensure that the sections are **specific, actionable, and informative**, not generic.
- Do not omit any template section, even if it feels redundant.
- The final output must be a **list of sections**, not a single object.

# Examples

<example id="1">
<Topic>
Evaluating LLM-based Coding Agents
</Topic>
<Template>
Introduction; Problem Definition; Methodology; Experiments; Results; Limitations; Future Work
</Template>
<assistant_response_note>
Expected: A list of 7 sections, each with a `title` from the template and a detailed `description`.
For example, "Methodology" should mention data sources, evaluation metrics, and testing pipeline,
while "Limitations" should cover model bias, reproducibility issues, or incomplete coverage.
</assistant_response_note>
</example>

<example id="2">
<Topic>
Building a Multi-Agent LangGraph Workflow
</Topic>
<Template>
Overview; Architecture; Setup; Implementation Steps; Testing & Evaluation; Deployment; Best Practices
</Template>
<assistant_response_note>
Expected: A list of 7 sections with structured `title` and `description`.
"Architecture" should explain agent roles, communication, and state flow,
while "Testing & Evaluation" should describe sandbox execution, metrics, and iteration.
</assistant_response_note>
</example>

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
