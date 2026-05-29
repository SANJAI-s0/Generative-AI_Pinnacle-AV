import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

# ── LLM ──────────────────────────────────────────────────────────────────────

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3,
)

# ── Tools ─────────────────────────────────────────────────────────────────────

_ddg = DuckDuckGoSearchRun()


@tool
def search_competitors(location: str) -> str:
    """Search for nearby clothing store competitors in a given location.

    Args:
        location: The area or city to search for clothing store competitors.

    Returns:
        A string with information about nearby clothing stores.
    """
    query = f"clothing stores near {location} competitors list popular"
    try:
        return _ddg.run(query)
    except Exception as e:
        return f"Could not search competitors for '{location}': {e}"


@tool
def search_footfall_and_busy_hours(store_or_location: str) -> str:
    """Search for footfall trends and busiest hours for clothing stores in a location.

    Args:
        store_or_location: The store name or location to search footfall data for.

    Returns:
        A string with footfall trends and peak hours information.
    """
    query = f"clothing stores {store_or_location} busiest hours peak footfall customer traffic times"
    try:
        return _ddg.run(query)
    except Exception as e:
        return f"Could not search footfall data for '{store_or_location}': {e}"


# ── Agent Setup ───────────────────────────────────────────────────────────────

tools = [search_competitors, search_footfall_and_busy_hours]

system_prompt = """You are a Competitive Intelligence AI assistant specializing in retail market analysis for clothing stores.

Your role is to help business owners understand their local competition by:
1. Identifying nearby clothing store competitors in a given location
2. Analyzing footfall trends and peak customer hours for those competitors
3. Providing actionable business insights based on the data

When a user provides a location or asks about competitors:
- Use the search_competitors tool to find nearby clothing stores
- Use the search_footfall_and_busy_hours tool to gather peak hours and traffic data
- Synthesize the findings into clear, actionable insights

When the user asks to generate a report, compile all gathered information into a structured markdown report covering:
- Executive Summary
- Competitor Overview (names, locations, key details)
- Footfall & Peak Hours Analysis
- Strategic Recommendations

Always be professional, data-driven, and focused on helping the business owner make informed decisions.
Maintain context across the conversation — remember what has been discussed previously."""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)


# ── Report Generator ──────────────────────────────────────────────────────────

def save_report(content: str, location: str) -> str:
    """Save the generated report to a markdown file."""
    os.makedirs("reports", exist_ok=True)
    safe_location = location.replace(" ", "_").replace(",", "").lower()
    filename = f"reports/competitor_report_{safe_location}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename


# ── Main Conversational Loop ──────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("   Competitive Intelligence AI — Clothing Store Analyzer")
    print("=" * 60)
    print("Ask me about clothing store competitors in any location.")
    print("Type 'report' to generate and save a full competitor report.")
    print("Type 'quit' or 'exit' to stop.\n")

    chat_history = []
    current_location = None

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            print("Goodbye! Good luck with your business strategy.")
            break

        # Detect if user wants a report saved
        save_to_file = "report" in user_input.lower()

        try:
            result = agent_executor.invoke({
                "input": user_input,
                "chat_history": chat_history,
            })

            output = result["output"]
            # Handle list-type output from Gemini
            if isinstance(output, list):
                output = "".join(
                    block.get("text", "") if isinstance(block, dict) else str(block)
                    for block in output
                )

            print(f"\nAssistant: {output}\n")

            # Update chat history for multi-turn context
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=output))

            # Auto-detect location from conversation for report naming
            if not current_location:
                for keyword in ["in ", "near ", "around ", "at "]:
                    if keyword in user_input.lower():
                        idx = user_input.lower().index(keyword) + len(keyword)
                        current_location = user_input[idx:].strip().rstrip("?.")
                        break

            # Save report to file if requested
            if save_to_file and len(output) > 200:
                loc_label = current_location or "location"
                filepath = save_report(output, loc_label)
                print(f"[Report saved to '{filepath}']\n")

        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
