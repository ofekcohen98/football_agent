from openai import OpenAI
from dotenv import load_dotenv
import os


class FootballAgent:
    def __init__(self, model="gpt-4o-mini"):
        """
        Initialize the FootballAgent with OpenAI client.
        
        Args:
            model (str): The OpenAI model to use. Defaults to "gpt-4o-mini".
        """
        # Load environment variables from .env file
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)
        self.model = model
        
        # Initialize conversation history
        self.messages = [
            {"role": "system", "content": "You are a helpful football agent with expert knowledge of football/soccer. You know about teams, players, competitions, history, tactics, and statistics."}
        ]
    
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
        self.messages.append({"role": "user", "content": question})
        
        # Get completion using the entire conversation history
        completion = self.client.chat.completions.create(
            model=self.model,
            store=True,
            messages=self.messages
        )
        
        # Extract the assistant's response
        response = completion.choices[0].message.content
        
        # Add the assistant's response to the conversation history
        self.messages.append({"role": "assistant", "content": response})
        
        return response
    
    def reset_conversation(self):
        """
        Reset the conversation history, starting a new chat.
        """
        self.messages = [
            {"role": "system", "content": "You are a helpful football agent with expert knowledge of football/soccer. You know about teams, players, competitions, history, tactics, and statistics."}
        ]
        return "Conversation has been reset."

