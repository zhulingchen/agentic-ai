from pydantic import BaseModel, Field
from typing import List, Optional


class ResearchSource(BaseModel):
    """A research source found during investigation."""
    url: str = Field(..., description="The URL of the source")
    title: str = Field(..., description="The title or description of the source")
    relevance: Optional[str] = Field(None, description="Why this source is relevant")


class ResearchOutput(BaseModel):
    """Structured output from research task."""
    topic: str = Field(..., description="The research topic")
    tags: List[str] = Field(..., description="Main findings from research")
    sources: List[ResearchSource] = Field(..., description="All sources consulted")
    summary: str = Field(..., description="Brief summary of research conducted")
