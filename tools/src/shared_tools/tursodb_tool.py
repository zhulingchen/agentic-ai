from crewai.tools import BaseTool
import json
import libsql
import os
from pydantic import BaseModel, Field
from typing import Type


class TursoDatabaseInput(BaseModel):
    """Input schema for TursoDatabaseTool."""
    topic: str = Field(..., description="The research topic")
    report_en: str = Field(..., description="The English research report content")
    report_zh: str = Field(..., description="The Chinese research report content")


class TursoDatabaseTool(BaseTool):
    name: str = "Save research record to Turso database"
    description: str = (
        "This tool saves a deep research record to the Turso Cloud SQLite database. "
        "Use this to store research history with the topic, English report, and Chinese report. "
    )
    args_schema: Type[BaseModel] = TursoDatabaseInput

    def _get_connection(self):
        database_url = os.getenv("TURSO_DATABASE_URL")
        auth_token = os.getenv("TURSO_AUTH_TOKEN")
        
        if not database_url or not auth_token:
            raise ValueError(
                "TURSO_DATABASE_URL and TURSO_AUTH_TOKEN must be set in environment variables"
            )
        
        conn = libsql.connect(
            database=database_url,
            auth_token=auth_token,
        )
        return conn

    def _run(self, topic: str, report_en: str, report_zh: str) -> str:
        conn = self._get_connection()
        try:
            with conn:
                cur = conn.execute(
                    """
                    INSERT INTO research_records (topic, report_en, report_zh)
                    VALUES (?, ?, ?)
                    RETURNING id, created_timestamp
                    """,
                    [topic, report_en, report_zh],
                )
                row = cur.fetchone()
                record_id, created_timestamp = row if row else (None, None)

            payload = {
                "status": "saved",
                "id": record_id,
                "topic": topic,
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
