import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Step 1: Define a real Python function - our "tool"
def calculator(operation: str, a: float, b: float) -> float:
    """Performs a basic math operation on two numbers."""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b
    else:
        return "Unknown operation"

# Step 2: Tell Gemini this tool exists, using the function directly
config = types.GenerateContentConfig(
    tools=[calculator],
    system_instruction="You are a helpful, knowledgeable assistant. Answer all general knowledge questions directly and confidently. Only use the calculator tool for math calculations."
)

print("Calculator Agent ready! Ask me a math question. Type 'quit' to exit.\n")

conversation_history = []

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    conversation_history.append({"role": "user", "parts": [{"text": user_input}]})

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation_history,
        config=config
    )

    reply = response.text
    print("Bot:", reply, "\n")
    conversation_history.append({"role": "model", "parts": [{"text": reply}]})