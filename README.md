# Football Agent

An OpenAI-powered football (soccer) agent that answers questions about teams, players, competitions, history, tactics, and statistics.

## Features

- Uses OpenAI GPT models to provide expert football knowledge
- Web-based chat interface using Gradio
- Message context management with a configurable limit (default: 10 messages)
- Persistent message storage using Redis

## Message Model System

The Football Agent uses a sophisticated message modeling system:

1. **Message Structure**:
   - Each message has a role (system, user, assistant)
   - Content (the actual message text)
   - Unique ID for tracking
   - Timestamp for chronological ordering

2. **Context Limitation**:
   - Only keeps the most recent N messages in context (default: 10)
   - Always includes the system message in the context
   - Ensures efficient API usage while maintaining conversation coherence

3. **Persistence**:
   - All messages are stored in Redis for historical purposes
   - Allows for conversation history analysis and retrieval

## Setup and Running

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up environment variables in a `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key
   REDIS_HOST= your_def
   REDIS_PORT= your_def
   REDIS_DB= your_def
   ```

3. Run the application:
   ```
   Make sure redis is running and properly configurated
   python main.py
   Find the ui at: http://127.0.0.1:7860/
   ```

## Adjusting Context Limit

You can adjust the message context limit in `main.py` by changing the `CONTEXT_LIMIT` variable.
