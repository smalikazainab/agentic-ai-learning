import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# This list stores the whole conversation so far
conversation_history = []

print("Chatbot ready! Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    # Add the user's message to history
    conversation_history.append({"role": "user", "parts": [{"text": user_input}]})

    # Send the FULL history so far (not just the latest message)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation_history
    )

    reply = response.text
    print("Bot:", reply, "\n")

    # Add the bot's reply to history too, so it remembers what IT said
    conversation_history.append({"role": "model", "parts": [{"text": reply}]})