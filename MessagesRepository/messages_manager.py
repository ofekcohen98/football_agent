from .message_model import Message
from .repository import RedisRepository
import json


class MessagesManager:
    def __init__(self, conversation_id=None, context_limit=10):
        """
        Initialize the MessagesManager.
        
        Args:
            conversation_id (str, optional): The ID of the conversation.
            context_limit (int, optional): The maximum number of messages to keep in context.
        """
        self.repository = RedisRepository()
        self.conversation_id = conversation_id or "default"
        self.context_limit = context_limit
        
        # Initialize or retrieve the conversation
        self._initialize_conversation()
    
    def _get_conversation_key(self):
        """
        Get the Redis key for the current conversation.
        
        Returns:
            str: The Redis key.
        """
        return f"conversation:{self.conversation_id}"
    
    def _initialize_conversation(self):
        """
        Initialize the conversation in Redis if it doesn't exist.
        Add the system message if this is a new conversation.
        """
        conversation_key = self._get_conversation_key()
        stored_messages = self.repository.get(conversation_key)
        
        if not stored_messages:
            # Create a new conversation with the system message
            system_message = Message(
                role="system",
                content="You are a helpful football agent with expert knowledge of football/soccer. You know about teams, players, competitions, history, tactics, and statistics."
            )
            self.add_message(system_message)
    
    def add_message(self, message):
        """
        Add a message to the conversation.
        
        Args:
            message (Message): The message to add.
            
        Returns:
            Message: The added message.
        """
        conversation_key = self._get_conversation_key()
        stored_messages = self.repository.get(conversation_key)
        
        if stored_messages:
            messages = [Message.from_dict(msg) for msg in json.loads(stored_messages)]
        else:
            messages = []
        
        # Add the new message
        messages.append(message)
        
        # Store all messages
        self.repository.set(
            conversation_key,
            json.dumps([msg.to_dict() for msg in messages])
        )
        
        return message
    
    def get_context_messages(self):
        """
        Get the last N messages to use as context, where N is the context_limit.
        Always include the system message at the beginning.
        
        Returns:
            list: List of messages in OpenAI format.
        """
        conversation_key = self._get_conversation_key()
        stored_messages = self.repository.get(conversation_key)
        
        if not stored_messages:
            return []
        
        messages = [Message.from_dict(msg) for msg in json.loads(stored_messages)]
        
        # Always include the system message (assuming it's the first one)
        system_messages = [msg for msg in messages if msg.role == "system"]
        
        other_messages = [msg for msg in messages if msg.role != "system"]
        
        limited_other_messages = other_messages[-(self.context_limit - len(system_messages)):]
        
        context_messages = system_messages + limited_other_messages

        print(f"Context messages: {[msg.to_openai_format() for msg in context_messages]}")
        
        # Convert to OpenAI format
        return [msg.to_openai_format() for msg in context_messages]
    
    def get_all_messages(self):
        """
        Get all messages in the conversation.
        
        Returns:
            list: List of all Message objects.
        """
        conversation_key = self._get_conversation_key()
        stored_messages = self.repository.get(conversation_key)
        
        if not stored_messages:
            return []
        
        return [Message.from_dict(msg) for msg in json.loads(stored_messages)]
    
    def reset_conversation(self):
        """
        Reset the conversation to only contain the system message.
        """
        conversation_key = self._get_conversation_key()
        self.repository.delete(conversation_key)
        self._initialize_conversation()
        return "Conversation has been reset."
