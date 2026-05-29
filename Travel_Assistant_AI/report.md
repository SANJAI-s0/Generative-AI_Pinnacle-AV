# Travel Assistant AI — Report

## Overview

This project implements an intelligent Travel Assistant using **LangChain** and **Google Gemini**. Given a destination, the agent automatically fetches the current weather forecast and searches for top tourist attractions, then synthesizes both into a coherent travel summary.

---

## How the LLM is Used for Reasoning

The LLM (Gemini 2.0 Flash via `langchain-google-genai`) acts as the **reasoning engine** inside a tool-calling agent. Here's how the reasoning step works:

1. **Input parsing** — The user provides a destination. The LLM reads the system prompt and user message to understand the intent.
2. **Tool selection** — The LLM decides which tools to call and in what order. Because the system prompt instructs it to always use *both* tools, it will invoke `get_weather` and `search_attractions` for every query.
3. **Tool call generation** — LangChain's `create_tool_calling_agent` binds the tools to the LLM. The model emits structured tool-call requests (function name + arguments) rather than free text.
4. **Observation integration** — After each tool returns its result, the LLM reads the output (stored in `agent_scratchpad`) and decides whether more tool calls are needed or if it has enough information to answer.
5. **Final synthesis** — Once all tool results are collected, the LLM composes a friendly, structured travel summary covering weather and attractions.

This loop — **Reason → Act (tool call) → Observe → Reason again** — is the core ReAct-style reasoning pattern that LangChain's `AgentExecutor` orchestrates automatically.

---

## Code & Program Flow

```
User Input (destination)
        │
        ▼
  AgentExecutor.invoke()
        │
        ▼
  LLM (Gemini) reasons about the query
        │
        ├──► get_weather(destination)
        │         └── Calls WeatherAPI.com REST endpoint
        │             Returns: current conditions + 3-day forecast
        │
        └──► search_attractions(destination)
                  └── Runs DuckDuckGoSearchRun query
                      Returns: top tourist attractions text
        │
        ▼
  LLM synthesizes both tool outputs
        │
        ▼
  Final travel summary printed to user
```

### Key Components

| Component | Role |
|---|---|
| `ChatGoogleGenerativeAI` | LLM backbone — reasoning and synthesis |
| `@tool get_weather` | Custom tool — fetches weather from WeatherAPI.com |
| `@tool search_attractions` | Custom tool — DuckDuckGo web search for attractions |
| `create_tool_calling_agent` | Binds LLM + tools into a tool-calling agent |
| `AgentExecutor` | Runs the agent loop, manages tool calls and scratchpad |
| `ChatPromptTemplate` | System prompt that guides the LLM's behavior |

### `get_weather` Tool

Uses the [WeatherAPI.com](https://www.weatherapi.com/) free-tier REST API to fetch:
- Current temperature, condition, humidity, wind speed
- 3-day forecast with high/low temps and rain probability

### `search_attractions` Tool

Wraps LangChain's `DuckDuckGoSearchRun` to query:
> *"top tourist attractions and places to visit in {destination}"*

No API key required — DuckDuckGo is free to use.

### Agent Prompt

The system prompt explicitly instructs the LLM to always call both tools before answering, ensuring the response is always grounded in real-time data rather than the model's training knowledge.

---

## Setup & Usage

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and fill in your API keys
cp .env.example .env

# 3. Run the assistant
python travel_assistant.py
```

### Required API Keys (`.env`)

```
GEMINI_API_KEY=...      # https://aistudio.google.com/
TAVILY_API_KEY=...      # optional, not used in default config
WEATHER_API_KEY=...     # https://www.weatherapi.com/ (free tier)
```
