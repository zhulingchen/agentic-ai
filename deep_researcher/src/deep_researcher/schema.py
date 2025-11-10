from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional


class ResearchDepth(str, Enum):
    SURFACE = "surface"
    MODERATE = "moderate"
    COMPREHENSIVE = "comprehensive"


class ConfidenceLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ResearchSource(BaseModel):
    """A research source found during investigation."""
    url: str = Field(..., description="The URL of the source")
    title: str = Field(..., description="The title or description of the source")
    relevance: str = Field(..., description="Why this source is relevant and what information it provides")
    source_type: Optional[str] = Field(
        None,
        description="Type of source: 'academic', 'news', 'blog', 'documentation', 'forum', etc.",
    )
    publication_date: Optional[str] = Field(
        None,
        description="Publication or last updated date if available",
    )
    key_information: Optional[str] = Field(
        None,
        description="1-2 sentence summary of key information from this source",
    )
    quality_score: Optional[int] = Field(
        None, 
        ge=1, 
        le=10, 
        description="Quality score of the source (1-10)",
    )


class ResearchOutput(BaseModel):
    """Structured output from research task."""
    topic: str = Field(..., description="The research topic")
    used_search_queries: Optional[List[str]] = Field(
        None,
        description="Key search queries that were used",
    )
    sources: List[ResearchSource] = Field(
        ..., 
        description="All sources consulted during research",
        min_length=3,
    )
    summary: str = Field(..., description="Brief summary of research conducted")
    tags: List[str] = Field(
        ..., 
        description="Categorical tags for this research",
        min_length=3,
        max_length=7,
    )
    research_depth: ResearchDepth = Field(
        ...,
        description="Assessment of research depth",
    )
    confidence_level: ConfidenceLevel = Field(
        ...,
        description="Overall confidence in findings",
    )
    limitations: Optional[List[str]] = Field(
        None,
        description="Any limitations or gaps identified during research",
    )
