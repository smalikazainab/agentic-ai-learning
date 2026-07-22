import os
import json
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

# --- Setup ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

MEMORY_FILE = "chat_history.json"
MODEL = "gemini-2.5-flash"


# --- Tools ---
def calculator(operation: str, a: float, b: float) -> float:
    """Performs a basic math operation (add, subtract, multiply, divide) on two numbers."""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            return "Cannot divide by zero"
        return a / b
    else:
        return "Unknown operation"


def get_weather(city: str) -> str:
    """Gets the current temperature for a given city name."""
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    geo_response = requests.get(geo_url).json()

    if "results" not in geo_response:
        return f"Could not find location: {city}"

    lat = geo_response["results"][0]["latitude"]
    lon = geo_response["results"][0]["longitude"]

    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    weather_response = requests.get(weather_url).json()

    temp = weather_response["current_weather"]["temperature"]
    return f"The current temperature in {city} is {temp}°C."


# --- Memory (persistent across sessions) ---
def load_history():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []


def save_history(history):
    with open(MEMORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


# --- Agent configuration ---
config = types.GenerateContentConfig(
    tools=[calculator, get_weather],
    system_instruction=(
        "You are a helpful, knowledgeable assistant. Answer all general knowledge "
        "questions directly and confidently, using your own knowledge. "
        "Use the calculator tool only for math calculations that require precision. "
        "Use the get_weather tool only when asked about current weather or temperature "
        "in a specific place."
    ),
)


# --- Main loop ---
def main():
    conversation_history = load_history()

    if conversation_history:
        print(f"Loaded {len(conversation_history)} previous messages. Continuing our chat!\n")
    else:
        print("Starting a brand new conversation.\n")

    print("Agent ready — I can chat, do math, and check the weather. Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print("Goodbye! Your conversation has been saved.")
            break

        conversation_history.append({"role": "user", "parts": [{"text": user_input}]})

        response = client.models.generate_content(
            model=MODEL,
            contents=conversation_history,
            config=config,
        )

        reply = response.text
        print("Bot:", reply, "\n")

        conversation_history.append({"role": "model", "parts": [{"text": reply}]})
        save_history(conversation_history)


if __name__ == "__main__":
    main()