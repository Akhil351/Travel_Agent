import operator
from typing import Annotated, TypedDict, List

from langchain_core.messages import AnyMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from src.tools import flights_finder, hotels_finder
from src.llms import get_openai_model


# ------------------------------------------------------------------
# 🧠 Agent State
# ------------------------------------------------------------------

class AgentState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]


# ------------------------------------------------------------------
# 🧭 System Prompt
# ------------------------------------------------------------------

TRAVEL_AGENT_SYSTEM_PROMPT = """
You are a smart travel assistant that returns structured JSON responses.

You can:
- Search for flights using the flights_finder tool
- Search for hotels using the hotels_finder tool

IMPORTANT Response Format Rules:

1. When user provides ALL required parameters, call the appropriate tool and return the results in JSON format

2. After calling a tool, return ONLY valid JSON (no extra text, no markdown):

For flights (after calling flights_finder):
{
  "response_type": "flights",
  "data": [list of flights from tool]
}

For hotels (after calling hotels_finder):
{
  "response_type": "hotels", 
  "data": [list of hotels from tool]
}

For conversational responses (missing params, greetings, clarifications):
{
  "response_type": "message",
  "message": "your friendly response here"
}

3. If user is missing required parameters, ask for them using the "message" format
4. Tool results are already cleaned - just wrap them in the appropriate response_type structure
5. Always return valid JSON - no markdown, no code blocks, just pure JSON
"""


# ------------------------------------------------------------------
# 🔧 Tools
# ------------------------------------------------------------------

TOOLS = [flights_finder, hotels_finder]


# ------------------------------------------------------------------
# 🤖 LLM (tool-enabled)
# ------------------------------------------------------------------

llm = get_openai_model().bind_tools(TOOLS)


# ------------------------------------------------------------------
# 🧩 Graph Nodes
# ------------------------------------------------------------------

def call_llm(state: AgentState) -> AgentState:
    messages = [SystemMessage(content=TRAVEL_AGENT_SYSTEM_PROMPT)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


def decide_next_node(state: AgentState) -> str:
    last_message = state["messages"][-1]
    tool_calls = getattr(last_message, "tool_calls", None)
    return "tools" if tool_calls else END



# ------------------------------------------------------------------
# 🕸️ LangGraph Builder
# ------------------------------------------------------------------

def build_travel_agent():
    """Build and compile the travel agent graph."""
    graph = StateGraph(AgentState)

    graph.add_node("call_llm", call_llm)
    graph.add_node("tools", ToolNode(TOOLS))

    graph.set_entry_point("call_llm")

    graph.add_conditional_edges(
        "call_llm",
        decide_next_node,
        {
            "tools": "tools",
            END: END,
        },
    )

    graph.add_edge("tools", "call_llm")

    return graph.compile()
