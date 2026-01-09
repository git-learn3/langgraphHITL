# from langchain.tools import tool

# @tool
# def validate_product(product_name: str) -> str:
#     """
#     Validate whether the product exists.
#     Returns 'valid' or 'invalid'.
#     """
#     if product_name.lower() in ["iphone", "laptop"]:
#         return "valid"
#     return "invalid"

from langgraph.graph import StateGraph
from state.state import OrderState
from langgraph.types import interrupt

#---------------- Product tool ----------------
"""
product_tool:
Selects a product for ordering.
"""
def product_tool_fn(state: OrderState):
    return {
        "product": state["product"],   # 🔑 WRITE IT BACK
        "messages": [
            f"Tool(product): product selected = {state['product']}"
        ]
    }



b = StateGraph(OrderState)
b.add_node("run", product_tool_fn)
b.set_entry_point("run")
product_tool = b.compile()


# ---------------- Size tool ----------------
"""
size_tool:
Determines size for the product.
"""
def size_tool_fn(state: OrderState):
    return {
        "size": "M",
        "messages": ["Tool(size): M selected"]
    }

b = StateGraph(OrderState)
b.add_node("run", size_tool_fn)
b.set_entry_point("run")
size_tool = b.compile()


# ---------------- Quantity tool ----------------
# """
# quantity_tool:
# Ask quantity for the order.
# """
# # def quantity_tool_fn(state: OrderState):
# #     return {
# #         "quantity": 2,
# #         "messages": ["Tool(quantity): 2 selected"]
# #     }
# def ask_quantity(state: OrderState):
#     if not state.get("quantity"):
#         return interrupt("Enter quantity:")
#     return {"messages": [f"Quantity: {state['quantity']}"]}


# b = StateGraph(OrderState)
# b.add_node("run", ask_quantity)
# b.set_entry_point("run")
# quantity_tool = b.compile()


# ---------------- Payment tool ----------------
"""
payment_tool:
Processes payment for the order.
"""
def payment_tool_fn(state: OrderState):
    return {
        "payment_status": "success",
        "messages": ["Tool(payment): success"]
    }

b = StateGraph(OrderState)
b.add_node("run", payment_tool_fn)
b.set_entry_point("run")
payment_tool = b.compile()


# 🔑 EXPORT REGISTRY
TOOLS = {
    "product": product_tool,
    "size": size_tool,
    # "quantity": quantity_tool,
    "payment": payment_tool,
}
