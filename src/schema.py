from pydantic import BaseModel, Field
from pydantic import ConfigDict


# Search result item schema (for Tavily results)
class SearchResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, description="Result title")
    url: str | None = Field(default=None, description="Result URL")
    content: str | None = Field(default=None, description="Snippet or content extract")
    score: float | None = Field(default=None, description="Relevance score if provided")


# Section Schema
class Section(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(description="The title of the section")
    description: str = Field(
        description="A comprehensive, well-detailed description of what should be included in the section, incorporating current research findings, specific content areas, key concepts, methodologies, and practical guidance"
    )
    require_research: bool = Field(
        description="Whether the section requires research to be written or it can be written based on other section contents"
    )
    search_queries: list[str] = Field(
        description="Make sure this field is always empty"
    )
    search_results: list[SearchResult] = Field(
        description="Make sure this field is always empty"
    )
    section_context: str = Field(description="Make sure this field is always empty")
