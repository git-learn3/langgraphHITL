"""
track_order:
Tracks an existing order.
Takes order ID and returns current delivery status.
No human interaction required.
"""
from langgraph.graph import StateGraph
from state.state import OrderState
from graph.track_order.tools import fetch_status_tool

def get_order_id(state: OrderState):
    return {
        "order_id": "ORD-1234",
        "messages": ["Order ID received"]}

def fetch_status(state: OrderState):
    return {
        "order_status":"In Transit",
        "messages": ["Order is in transit"]}

def build_track_order_graph(CheckpointSaver=None):
    builder = StateGraph(OrderState)

    builder.add_node("get_order_id", get_order_id)
    builder.add_node("fetch_status", fetch_status_tool)

    builder.set_entry_point("get_order_id")
    builder.add_edge("get_order_id", "fetch_status")

    track_order_graph = builder.compile()
    return track_order_graph