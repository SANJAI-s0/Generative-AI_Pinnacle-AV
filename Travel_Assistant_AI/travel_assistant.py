import os
import requests
from dotenv import load_dotenv

from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# ── LLM ──────────────────────────────────────────────────────────────────────

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3,
)

# ── Custom Weather Tool ───────────────────────────────────────────────────────

@tool
def get_weather(destination: str) -> str:
    """Fetch the current weather forecast for a travel destination.

    Args:
        destination: The city or location name to get weather for.

    Returns:
        A human-readable weather summary string.
    """
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "Weather API key not configured. Please set WEATHER_API_KEY in your .env file."

    url = "http://api.weatherapi.com/v1/forecast.json"
    params = {"key": api_key, "q": destination, "days": 3, "aqi": "no", "alerts": "no"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        location = data["location"]
        current = data["current"]
        forecast_days = data["forecast"]["forecastday"]

        summary = (
            f"Weather in {location['name']}, {location['country']}:\n"
            f"  Current: {current['temp_c']}°C ({current['temp_f']}°F), "
            f"{current['condition']['text']}, "
            f"Humidity: {current['humidity']}%, "
            f"Wind: {current['wind_kph']} kph\n\n"
            f"3-Day Forecast:\n"
        )
        for day in forecast_days:
            d = day["day"]
            summary += (
                f"  {day['date']}: High {d['maxtemp_c']}°C / Low {d['mintemp_c']}°C, "
                f"{d['condition']['text']}, "
                f"Rain chance: {d['daily_chance_of_rain']}%\n"
            )
        return summary

    except requests.exceptions.HTTPError as e:
        return f"Could not fetch weather for '{destination}': {e}"
    except Exception as e:
        return f"Unexpected error fetching weather: {e}"


# ── Search Tool (DuckDuckGo) ──────────────────────────────────────────────────

_ddg = DuckDuckGoSearchRun()

@tool
def search_attractions(destination: str) -> str:
    """Search for top tourist attractions and interesting places to visit in a destination.

    Args:
        destination: The city or location name to search attractions for.

    Returns:
        A string with top tourist attractions and points of interest.
    """
    query = f"top tourist attractions and places to visit in {destination}"
    try:
        return _ddg.run(query)
    except Exception as e:
        return f"Could not search attractions for '{destination}': {e}"


# ── Agent Setup ───────────────────────────────────────────────────────────────

tools = [get_weather, search_attractions]

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful Travel Assistant AI. When a user mentions any destination "
        "(country, city, or region), you MUST immediately call both the get_weather tool "
        "AND the search_attractions tool without asking any clarifying questions. "
        "Use the destination exactly as provided by the user. "
        "After both tools return results, provide a well-structured travel summary covering:\n"
        "1. Current weather and 3-day forecast\n"
        "2. Top attractions and places to visit\n"
        "Always be friendly, concise, and helpful.",
    ),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("       Welcome to the Travel Assistant AI")
    print("=" * 55)
    print("Type 'quit' or 'exit' to stop.\n")

    while True:
        destination = input("Enter your travel destination: ").strip()
        if destination.lower() in ("quit", "exit"):
            print("Safe travels! Goodbye.")
            break
        if not destination:
            print("Please enter a valid destination.\n")
            continue

        print(f"\nFetching travel info for '{destination}'...\n")
        try:
            result = agent_executor.invoke({
                "input": f"I'm planning to travel to {destination}. "
                         "Please give me the current weather forecast and the top attractions to visit there."
            })
            output = result["output"]
            # Gemini sometimes returns a list of content blocks instead of a plain string
            if isinstance(output, list):
                output = "".join(
                    block.get("text", "") if isinstance(block, dict) else str(block)
                    for block in output
                )
            print("\n" + "=" * 55)
            print(output)
            print("=" * 55 + "\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
