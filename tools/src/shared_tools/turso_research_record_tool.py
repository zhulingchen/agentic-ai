import json
from pydantic import BaseModel, Field
from typing import Optional, Type

from shared_tools.turso_base_tool import TursoBaseTool


class TursoResearchRecordInput(BaseModel):
    """Input schema for TursoResearchRecordTool."""
    topic: str = Field(..., description="The research topic")
    report_en: str = Field(..., description="The English research report content")
    report_zh: str = Field(..., description="The Chinese research report content")
    word_count_en: Optional[int] = Field(None, description="Word count of English report")
    word_count_zh: Optional[int] = Field(None, description="Word count of Chinese report")


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
        word_count_en: Optional[int] = None,
        word_count_zh: Optional[int] = None,
    ) -> str:
        conn = self._get_connection()
        try:
            # Calculate word counts if not provided
            if word_count_en is None:
                word_count_en = len(report_en.split())
            if word_count_zh is None:
                # For Chinese, count characters instead of words
                word_count_zh = len([c for c in report_zh if c.strip()])

            with conn:
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

            payload = {
                "status": "OK",
                "record_id": record_id,
                "topic": topic,
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
