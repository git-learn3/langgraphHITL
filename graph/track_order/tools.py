

from state.state import OrderState

def fetch_status_tool(state: OrderState):
    return {
        "order_status": "In Transit",
        "messages": ["Tool(fetch_status): In Transit"]
    }
