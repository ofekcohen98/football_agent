import json
import uuid
from datetime import datetime


class Message:
    def __init__(self, role, content, message_id=None, timestamp=None):
        """
        Initialize a Message object.
        
        Args:
            role (str): The role of the message sender (system, user, assistant).
            content (str): The content of the message.
            message_id (str, optional): The unique ID of the message.
            timestamp (str, optional): The timestamp of when the message was created.
        """
        self.role = role
        self.content = content
        self.message_id = message_id or str(uuid.uuid4())
        self.timestamp = timestamp or datetime.now().isoformat()
    
    def to_dict(self):
        """
        Convert the Message object to a dictionary.
        
        Returns:
            dict: Dictionary representation of the Message.
        """
        return {
            "role": self.role,
            "content": self.content,
            "message_id": self.message_id,
            "timestamp": self.timestamp
        }
    
    def to_openai_format(self):
        """
        Convert the Message object to the format expected by OpenAI API.
        
        Returns:
            dict: OpenAI format message with role and content.
        """
        return {
            "role": self.role,
            "content": self.content
        }
    
    @classmethod
    def from_dict(cls, message_dict):
        """
        Create a Message object from a dictionary.
        
        Args:
            message_dict (dict): Dictionary representation of a Message.
            
        Returns:
            Message: A new Message object.
        """
        return cls(
            role=message_dict["role"],
            content=message_dict["content"],
            message_id=message_dict.get("message_id"),
            timestamp=message_dict.get("timestamp")
        )
