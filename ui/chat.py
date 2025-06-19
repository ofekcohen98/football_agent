"""
Web-based chat interface for interacting with the Football Agent.
"""
import os
import base64
import gradio as gr
from agent.agent import FootballAgent

def get_image_data_url():
    """Get the image as a data URL for CSS background."""
    image_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "utils", 
        "image.jpg"
    )
    
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
            return f"data:image/jpeg;base64,{encoded_image}"
    else:
        print(f"Warning: Image file not found at {image_path}")
        # Return a fallback URL or empty string
        return ""

# Create the CSS with the embedded image
bg_image_url = get_image_data_url()
FOOTBALL_CSS = f"""
.football-chat-container {{
    background-image: url('{bg_image_url}');
    background-size: cover;
    background-position: center;
    border-radius: 10px;
    padding: 20px;
}}

.football-chatbot {{
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 10px;
}}

.football-header {{
    color: #0e5814;
    text-shadow: 1px 1px 2px #ffffff;
    font-weight: bold;
}}

.football-btn {{
    background-color: #0e5814 !important;
    color: white !important;
}}

.football-input {{
    border: 2px solid #0e5814 !important;
    border-radius: 5px !important;
}}
"""

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
        with gr.Blocks(title="Football Agent Chat", theme="soft", css=FOOTBALL_CSS) as interface:
            with gr.Column(elem_classes="football-chat-container"):
                gr.Markdown("# ⚽ Football Expert Chat ⚽", elem_classes="football-header")
                gr.Markdown("Ask questions about football/soccer teams, players, competitions, history, tactics, and statistics.", elem_classes="football-header")
                
                chatbot = gr.Chatbot(
                    height=500,
                    show_copy_button=True,
                    bubble_full_width=False,
                    elem_classes="football-chatbot"
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        scale=4,
                        show_label=False,
                        placeholder="Ask a question about football...",
                        container=False,
                        elem_classes="football-input"
                    )
                    reset_btn = gr.Button("Reset Chat", scale=1, elem_classes="football-btn")
                
                gr.Markdown("*Powered by advanced football knowledge AI*")
            
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

