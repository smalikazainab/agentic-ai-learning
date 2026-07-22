import os
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Tool 1: Calculator (same as before)
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

# Tool 2: Real weather lookup (new!)
def get_weather(city: str) -> str:
    """Gets the current weather for a given city name."""
    # Step A: convert city name to latitude/longitude
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    geo_response = requests.get(geo_url).json()

    if "results" not in geo_response:
        return f"Could not find location: {city}"

    lat = geo_response["results"][0]["latitude"]
    lon = geo_response["results"][0]["longitude"]

    # Step B: get current weather for those coordinates
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    weather_response = requests.get(weather_url).json()

    temp = weather_response["current_weather"]["temperature"]
    return f"The current temperature in {city} is {temp}°C."

# Register BOTH tools
config = types.GenerateContentConfig(
    tools=[calculator, get_weather],
    system_instruction="You are a helpful, knowledgeable assistant. Answer all general knowledge questions directly and confidently. Use the calculator tool for math, and the get_weather tool when asked about weather or temperature in a specific place."
)

print("Multi-tool Agent ready! Ask me anything. Type 'quit' to exit.\n")

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