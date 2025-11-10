import json
from pydantic import BaseModel, Field
from typing import Optional, List, Type

from shared_tools.turso_base_tool import TursoBaseTool


class TursoResearchRecordInput(BaseModel):
    """Input schema for TursoResearchRecordTool."""
    topic: str = Field(..., description="The research topic")
    report_en: str = Field(..., description="The English research report content")
    report_zh: str = Field(..., description="The Chinese research report content")
    tags: Optional[List[str]] = Field(None, description="Categorical tags for this research")


class TursoResearchRecordTool(TursoBaseTool):
    name: str = "Save research record to Turso database"
    description: str = (
        "This tool saves a deep research record to the Turso Cloud SQLite database. "
        "Use this to store research history with the topic, English report, and Chinese report. "
    )
    args_schema: Type[BaseModel] = TursoResearchRecordInput

    def _run(
        self,
        topic: str,
        report_en: str,
        report_zh: str,
        tags: Optional[List[str]] = None,
    ) -> str:
        conn = self._get_connection()
        try:
            # Calculate word counts
            word_count_en = len(report_en.split())

            # For Chinese, count characters instead of words
            word_count_zh = len([c for c in report_zh if c.strip()])

            with conn:
                # Insert the research record (without tags column)
                cur = conn.execute(
                    """
                    INSERT INTO research_records (topic, report_en, report_zh, word_count_en, word_count_zh)
                    VALUES (?, ?, ?, ?, ?)
                    RETURNING id, created_timestamp
                    """,
                    [topic, report_en, report_zh, word_count_en, word_count_zh],
                )
                row = cur.fetchone()
                record_id, created_timestamp = row if row else (None, None)

                # Insert tags into research_tags table if provided
                saved_tags = []
                if tags and record_id:
                    for tag in tags:
                        try:
                            cur = conn.execute(
                                """
                                INSERT INTO research_tags (research_id, tag)
                                VALUES (?, ?)
                                RETURNING id
                                """,
                                [record_id, tag],
                            )
                            tag_row = cur.fetchone()
                            tag_id = tag_row[0] if tag_row else None
                            saved_tags.append({"id": tag_id, "tag": tag})
                        except Exception:
                            # Ignore duplicate tags (UNIQUE constraint)
                            pass

            payload = {
                "status": "OK",
                "record_id": record_id,
                "topic": topic,
                "tags": saved_tags,
                "word_count_en": word_count_en,
                "word_count_zh": word_count_zh,
                "created_timestamp": created_timestamp,
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
