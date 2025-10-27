from crewai.tools import BaseTool
import os
from pydantic import BaseModel, Field
import requests
from typing import Type


class PushoverNotificationInput(BaseModel):
    """Input schema for PushNotificationTool."""
    title: str = Field(..., description="The title of the message")
    message: str = Field(..., description="The message to be sent to the user")


class PushoverNotificationTool(BaseTool):
    name: str = "Send a push notification via Pushover"
    description: str = (
        "This tool is used to send a push notification to the user via Pushover. "
        "Use this when you need to notify the user about important updates or completed tasks."
    )
    args_schema: Type[BaseModel] = PushoverNotificationInput

    def _run(self, title: str, message: str) -> str:
        pushover_user = os.getenv("PUSHOVER_USER")
        pushover_token = os.getenv("PUSHOVER_TOKEN")
        pushover_url = "https://api.pushover.net/1/messages.json"

        if not pushover_user or not pushover_token:
            raise ValueError("PUSHOVER_USER or PUSHOVER_TOKEN not set in environment variables")
        
        payload = {
            "user": pushover_user,
            "token": pushover_token,
            "title": title,
            "message": message,
        }
        
        try:
            response = requests.post(pushover_url, data=payload)
            response.raise_for_status()
            return '{"notification": "ok"}'
        except requests.exceptions.RequestException as e:
            return f"Error sending push notification: {str(e)}"
