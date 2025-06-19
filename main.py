from ui.chat import start_ui

# Define the message context limitation
CONTEXT_LIMIT = 10

if __name__ == "__main__":
    start_ui(context_limit=CONTEXT_LIMIT)