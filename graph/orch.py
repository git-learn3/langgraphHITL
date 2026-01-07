from langgraph.graph import StateGraph
from langgraph.types import interrupt
from langgraph.checkpoint.memory import MemorySaver
from state.state import OrderState
from graph.tools.place_order import place_order_graph
from graph.tools.track_order import track_order_graph
from graph.tools.cancel_order import cancel_order_graph
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="/home/sigmoid/HITL/.env")

from langchain_groq import ChatGroq

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
llm=ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0
    )

# Tools are defined here
TOOLS = {
    "place_order": place_order_graph.__doc__,
    "track_order": track_order_graph.__doc__,
    "cancel_order": cancel_order_graph.__doc__,
}

# Router decides which tool to run based on input
def tool_select(state: OrderState):
    prompt = f"""
You are an intent router.

User request:
{state["input"]}

Available tools and their descriptions:
{TOOLS}

Return ONLY the tool name.
"""
    tool = llm.invoke(prompt).content.strip()
    return {"selected_tool": tool}

# Build the graph
builder = StateGraph(OrderState)

builder.add_node("start", tool_select)
builder.add_node("place_order", place_order_graph)
builder.add_node("track_order", track_order_graph)
builder.add_node("cancel_order", cancel_order_graph)

# Conditional edges from router → tool nodes
builder.add_conditional_edges(
    "start",
    lambda s: s["selected_tool"],
    {
        "place_order": "place_order",
        "track_order": "track_order",
        "cancel_order": "cancel_order",
    }
)

builder.set_entry_point("start")

# Compile the graph
graph = builder.compile(checkpointer=MemorySaver())
