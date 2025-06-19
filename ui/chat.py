"""
Web-based chat interface for interacting with the Football Agent.
"""
import gradio as gr
from agent.agent import FootballAgent

class FootballAgentUI:
    def __init__(self, context_limit=10):
        """
        Initialize the Football Agent UI.
        
        Args:
            context_limit (int, optional): Maximum number of messages in context. Defaults to 10.
        """
        self.agent = FootballAgent(context_limit=context_limit)
        
    def chat(self, message, history):
        """
        Process a message from the user and return the agent's response.
        
        Args:
            message: The user's message
            history: The conversation history
            
        Returns:
            The agent's response
        """
        response = self.agent.ask_question(message)
        return response
    
    def reset_chat(self):
        """Reset the conversation history in the agent."""
        self.agent.reset_conversation()
        return "Conversation has been reset."

    def launch(self):
        """Launch the web interface."""
        with gr.Blocks(title="Football Agent Chat", theme="soft") as interface:
            gr.Markdown("# Football Agent Chat")
            gr.Markdown("Ask questions about football/soccer teams, players, competitions, history, tactics, and statistics.")
            
            chatbot = gr.Chatbot(
                height=500,
                show_copy_button=True,
                bubble_full_width=False,
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    scale=4,
                    show_label=False,
                    placeholder="Ask a question about football...",
                    container=False,
                )
                reset_btn = gr.Button("Reset Chat", scale=1)
            
            def respond(message, chat_history):
                response = self.chat(message, chat_history)
                chat_history.append((message, response))
                return "", chat_history
            
            def reset_chat_ui():
                self.reset_chat()
                return [], ""
            
            msg.submit(respond, [msg, chatbot], [msg, chatbot])
            reset_btn.click(reset_chat_ui, [], [chatbot, msg])
            
        return interface.launch(share=True, inbrowser=True)


def start_ui(context_limit=10):
    """
    Start the Football Agent UI.
    
    Args:
        context_limit (int, optional): Maximum number of messages in context. Defaults to 10.
    """
    ui = FootballAgentUI(context_limit=context_limit)
    ui.launch()

