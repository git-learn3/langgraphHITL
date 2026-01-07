"""
place_order:
Creates a new order.
Steps include selecting product, size, quantity,
asking user confirmation, and completing payment.
Requires human confirmation before payment.
"""

from langgraph.graph import StateGraph
from state.state import OrderState
from langgraph.types import interrupt

def select_product(state: OrderState):
    return {"messages": ["Product selected"]}

def select_size(state: OrderState):
    return {"messages": ["Size selected"]}

def select_quantity(state: OrderState):
    return {"messages": ["Quantity selected"]}

def place_order(state:OrderState):
    if not state.get("confirmation"):
        return interrupt("Confirm order? (yes/no)")
    
    if state.get("confirmation").lower() == "no":
        return {
            "messages": [
                "Order was not placed."
            ]
        }

    return {
        "messages": [
            "Order confirmed",
        ]
    }

def payment(state: OrderState):
    return {"messages": ["Payment completed"]}

builder = StateGraph(OrderState)

builder.add_node("select_product", select_product)
builder.add_node("select_size", select_size)
builder.add_node("select_quantity", select_quantity)
builder.add_node("confirm_order", place_order)
builder.add_node("payment", payment)

builder.set_entry_point("select_product")
builder.add_edge("select_product", "select_size")
builder.add_edge("select_size", "select_quantity")
builder.add_edge("select_quantity", "confirm_order")
builder.add_edge("confirm_order", "payment")

place_order_graph = builder.compile()

