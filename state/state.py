from typing import TypedDict, Annotated
from langgraph.graph import add_messages

class OrderState(TypedDict):
    input: str
    selected_tool: str | None
    confirmation: str | None
    order_id: str | None
    messages: Annotated[list[str], add_messages]  # Reducer function
