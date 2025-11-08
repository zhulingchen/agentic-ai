import json
from pydantic import BaseModel, Field
from typing import Type, List, Optional
from urllib.parse import urlparse

from shared_tools.turso_base_tool import TursoBaseTool

class ResearchSource(BaseModel):
    """A single research source."""
    url: str = Field(..., description="The URL of the source")
    title: Optional[str] = Field(None, description="The title of the source/page")


class ResearchSourcesInput(BaseModel):
    """Input schema for TursoResearchSourcesTool."""
    research_id: int = Field(..., description="The ID of the research record this source belongs to")
    sources: List[ResearchSource] = Field(..., description="List of sources (URLs and titles) to save")


class TursoResearchSourcesTool(TursoBaseTool):
    name: str = "Save research sources to Turso database"
    description: str = (
        "This tool saves research sources (URLs and titles) to the Turso Cloud SQLite database. "
        "Use this to store all the URLs that were consulted during research, linking them to "
        "a specific research record by its ID. Each source should include the URL and optionally "
        "the page title."
    )
    args_schema: Type[BaseModel] = ResearchSourcesInput

    def _extract_domain(self, url: str) -> str:
        """
        Extract the domain from a URL.
        
        Args:
            url: Full URL string
            
        Returns:
            Domain string (e.g., 'github.com')
        """
        try:
            parsed = urlparse(url)
            return parsed.netloc
        except Exception:
            return ""

    def _run(self, research_id: int, sources: List[ResearchSource]) -> str:
        """
        Save research sources to the database.
        
        Args:
            research_id: ID of the research record these sources belong to
            sources: List of source objects with URL and optional title
            
        Returns:
            JSON string with status and saved sources
        """
        conn = self._get_connection()
        try:
            saved_sources = []
            
            with conn:
                for source in sources:
                    domain = self._extract_domain(source.url)
                    
                    cur = conn.execute(
                        """
                        INSERT INTO research_sources (research_id, url, title, domain)
                        VALUES (?, ?, ?, ?)
                        RETURNING id
                        """,
                        [research_id, source.url, source.title, domain],
                    )
                    row = cur.fetchone()
                    source_id = row[0] if row else None
                    
                    saved_sources.append({
                        "id": source_id,
                        "url": source.url,
                        "title": source.title,
                        "domain": domain
                    })

            payload = {
                "status": "saved",
                "research_id": research_id,
                "sources_count": len(saved_sources),
                "sources": saved_sources
            }
            return json.dumps(payload)
        except Exception as e:
            payload = {
                "status": "error",
                "message": str(e),
            }
            return json.dumps(payload)
        finally:
            conn.close()