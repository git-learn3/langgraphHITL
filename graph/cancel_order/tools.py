

from state.state import OrderState

def get_order_id_tool(state: OrderState):
    return {
        "order_id": "ORD-1234",
        "messages": ["Order ID verified"]}