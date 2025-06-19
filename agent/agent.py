from agents import Agent, WebSearchTool, Runner
from dotenv import load_dotenv
import os
import asyncio
from MessagesRepository.message_model import Message
from MessagesRepository.messages_manager import MessagesManager


class FootballAgent:
    def __init__(self, model="gpt-4o-mini", conversation_id=None, context_limit=10):
        """
        Initialize the FootballAgent with OpenAI Agent from openai-agents SDK, including the WebSearchTool.
        
        Args:
            model (str): The OpenAI model to use. Defaults to "gpt-4o-mini".
            conversation_id (str, optional): The ID of the conversation.
            context_limit (int, optional): The maximum number of messages to keep in context.
        """
        # Load environment variables from .env file
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        self.model = model
        self.agent = Agent(name="Asistant",instructions="You are a helpful football agent with expert knowledge of football/soccer. You know about teams, players, competitions, history, tactics, and statistics.", tools=[WebSearchTool()])
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
        
        # Create a new event loop for this call
        try:
            # Try to get the current event loop
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Create a new loop if the current one is already running
                new_loop = asyncio.new_event_loop()
                response = new_loop.run_until_complete(Runner.run(self.agent, input=question))
                new_loop.close()
            else:
                # Use the existing loop
                response = loop.run_until_complete(Runner.run(self.agent, input=question, context=context_messages))
        except RuntimeError:
            # No event loop, create one
            response = asyncio.run(Runner.run(self.agent, input=question, context=context_messages))
        
        # Convert response to string if it's not already
        if not isinstance(response, str):
            response = str(response)
        
        # Add the assistant's response to the conversation history
        assistant_message = Message(role="assistant", content=response)
        self.messages_manager.add_message(assistant_message)
        
        return response
    
    def reset_conversation(self):
        """
        Reset the conversation history, starting a new chat.
        """
        return self.messages_manager.reset_conversation()

