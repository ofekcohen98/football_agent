from openai import OpenAI
from dotenv import load_dotenv
import os
from MessagesRepository.message_model import Message
from MessagesRepository.messages_manager import MessagesManager


class FootballAgent:
    def __init__(self, model="gpt-4o-mini", conversation_id=None, context_limit=10):
        """
        Initialize the FootballAgent with OpenAI client.
        
        Args:
            model (str): The OpenAI model to use. Defaults to "gpt-4o-mini".
            conversation_id (str, optional): The ID of the conversation.
            context_limit (int, optional): The maximum number of messages to keep in context.
        """
        # Load environment variables from .env file
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)
        self.model = model
          # Initialize messages manager
        self.messages_manager = MessagesManager(conversation_id, context_limit)
    
    def ask_question(self, question):
        """
        Ask a question to the football agent and return the response.
        The conversation history is maintained between questions.
        
        Args:
            question (str): The question to ask the agent.
            
        Returns:
            str: The agent's response.
        """
        # Add the user's question to the conversation history
        user_message = Message(role="user", content=question)
        self.messages_manager.add_message(user_message)
        
        # Get context messages (limited to context_limit)
        context_messages = self.messages_manager.get_context_messages()
        
        # Get completion using the context messages
        completion = self.client.chat.completions.create(
            model=self.model,
            store=True,
            messages=context_messages
        )
        
        # Extract the assistant's response
        response = completion.choices[0].message.content
          # Add the assistant's response to the conversation history
        assistant_message = Message(role="assistant", content=response)
        self.messages_manager.add_message(assistant_message)
        
        return response
    
    def reset_conversation(self):
        """
        Reset the conversation history, starting a new chat.
        """
        return self.messages_manager.reset_conversation()

