from pydantic import BaseModel, Field, validator, root_validator
from typing import Annotated, Literal, Optional, Dict


ResearchPaperType = Literal[
    "Analytical Paper",
    "Argumentative/Persuasive Paper",
    "Case Study",
    "Cause and Effect Paper",
    "Compare and Contrast Paper",
    "Descriptive Paper",
    "Experimental Research Paper",
    "Interpretive Paper",
    "Survey Research Paper",
    "Review Paper",
]

ModelName = Literal[
    # --- OpenAI GPT-4 family ---
    "openai:gpt-4o",
    "openai:gpt-4o-mini",

    # --- OpenAI GPT-5 family ---
    "openai:gpt-5",
    "openai:gpt-5-mini",
    "openai:gpt-5-large",

    # --- Anthropic Claude family ---
    "anthropic:claude-3-haiku",
    "anthropic:claude-3-sonnet",
    "anthropic:claude-3-opus",
    "anthropic:claude-3-5-sonnet",
    "anthropic:claude-3-5-opus",

    # --- Google Gemini family ---
    "google:gemini-1.5-flash",
    "google:gemini-1.5-pro",
    "google:gemini-1.5-ultra",
    "google:gemini-2.0-flash",
    "google:gemini-2.0-pro",
]
class Configuration(BaseModel):

    research_paper_type: Annotated[
        Optional[ResearchPaperType],
        {"__template_metadata__": {"kind": "research_paper_type"}},
    ] = Field(
        default="Analytical Paper",
        description="The type of research paper to draft.",
    )

    # Models
    query_model: Annotated[ModelName, {"__template_metadata__": {"kind": "llm"}}] = Field(
        default="openai:gpt-4o-mini", description="Model for retrieval/planning queries."
    )
    planner_model: Annotated[ModelName, {"__template_metadata__": {"kind": "llm"}}] = Field(
        default="openai:gpt-4o-mini", description="Model for section planning/outline."
    )
    drafting_model: Annotated[ModelName, {"__template_metadata__": {"kind": "llm"}}] = Field(
        default="openai:gpt-4o", description="Model for prose drafting."
    )

    # Templates
    document_template: str = Field(
        default="""
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
            """,
        description="Template to use when drafting the research paper.",
    )


   
