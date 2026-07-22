# AI Agent — Conversational Assistant with Tools & Memory

A command-line AI agent built with Python and Google's Gemini API. It holds natural conversations, remembers context across sessions, and can autonomously decide when to use tools like performing calculations or checking live weather  instead of just generating text.

## Features

- **Multi-turn conversation**  maintains full context throughout a session
- **Persistent memory** conversation history is saved to disk and restored automatically, even after closing and reopening the program
- **Tool calling** the agent decides on its own when a question needs a real calculation or live weather data, rather than guessing
- **Live weather lookup**  fetches real-time temperature data for any city using the Open-Meteo API
- **Precise calculations**  handles arithmetic through an actual function call, not language-model guessing

## How it works

The agent is built around Gemini's function-calling capability. Two Python functions (`calculator` and `get_weather`) are registered as tools the model can invoke. When a user's message requires one of these tools, the model automatically triggers the function, receives the real result, and incorporates it into its response  without the developer having to manually route the request.

Conversation history is stored as JSON on disk (`chat_history.json`), so context persists across separate runs of the program.

## Tech stack

- Python
- Google Gemini API (`google-genai`)
- Open-Meteo API (free, no key required) for weather data
- `python-dotenv` for environment variable management

## Setup

1. Clone this repository
   ```bash
   git clone https://github.com/smalikazainab/agentic-ai-learning/tree/main
   cd agentic-ai-learning
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root folder with your own Gemini API key:
   ```
   GEMINI_API_KEY=your_key_here
   ```
   Get a free key at [Google AI Studio](https://aistudio.google.com/apikey).

4. Run the agent
   ```bash
   python agent.py
   ```

## Example usage

```
You: what's the weather in Lahore right now?
Bot: The current temperature in Lahore is 34°C.

You: what is 847 multiplied by 392?
Bot: 847 multiplied by 392 is 332,024.

You: who is the president of France?
Bot: Emmanuel Macron is the current President of France.
```

## Future improvements

- Add more tools (e.g., web search, currency conversion)
- Multi-agent orchestration for more complex task delegation
- Web-based interface instead of CLI
