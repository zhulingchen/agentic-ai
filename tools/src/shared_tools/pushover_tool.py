from crewai.tools import BaseTool
import json
import os
from pydantic import BaseModel, Field
import requests
from typing import Type, Optional


class PushoverNotificationInput(BaseModel):
    """Input schema for PushNotificationTool."""
    title: str = Field(None, description="The title of the message")
    message: str = Field(None, description="The message to be sent to the user")


class PushoverNotificationTool(BaseTool):
    name: str = "Send a push notification via Pushover"
    description: str = (
        "This tool is used to send a push notification to the user via Pushover. "
        "Use this when you send a push notification with the title and the complete report content."
    )
    args_schema: Type[BaseModel] = PushoverNotificationInput

    def _run(self, title: str, message: str) -> str:
        pushover_user = os.getenv("PUSHOVER_USER")
        pushover_token = os.getenv("PUSHOVER_TOKEN")
        pushover_url = "https://api.pushover.net/1/messages.json"

        if not pushover_user or not pushover_token:
            raise ValueError("PUSHOVER_USER or PUSHOVER_TOKEN not set in environment variables")

        # Pushover has a 1024 character limit for messages
        max_message_length = 1024
        
        # Split message into chunks (works for both short and long messages)
        messages = self._split_message(message, max_message_length)
        results = []
        
        for i, msg_part in enumerate(messages):
            part_title = f"{title} (Part {i+1}/{len(messages)})" if len(messages) > 1 else title
            payload = {
                "user": pushover_user,
                "token": pushover_token,
                "title": part_title,
                "message": msg_part,
            }
            
            try:
                response = requests.post(pushover_url, data=payload)
                response.raise_for_status()
                results.append(f"Part {i+1}: OK")
            except requests.exceptions.RequestException as e:
                results.append(f"Part {i+1}: Error - {str(e)}")
        
        payload = {
            "notification": "sent",
            "results": results,
        }
        return json.dumps(payload)
    
    def _split_message(self, message: str, max_length: int) -> list:
        """Split a long message into chunks that fit within the character limit."""
        if len(message) <= max_length:
            return [message]
        
        chunks = []
        current_chunk = ""
        
        # Split by lines first to maintain readability
        lines = message.split('\n')
        
        for line in lines:
            # If adding this line would exceed the limit, start a new chunk
            if len(current_chunk) + len(line) + 1 > max_length:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = line
                else:
                    # Line itself is too long, split it by words
                    words = line.split(' ')
                    for word in words:
                        if len(current_chunk) + len(word) + 1 > max_length:
                            if current_chunk:
                                chunks.append(current_chunk.strip())
                                current_chunk = word
                            else:
                                # Word itself is too long, truncate it
                                chunks.append(word[:max_length])
                                current_chunk = ""
                        else:
                            current_chunk += (" " + word) if current_chunk else word
            else:
                current_chunk += ("\n" + line) if current_chunk else line
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
