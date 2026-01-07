from graph.orch import graph
from langgraph.types import Command

thread_id = "demo-1"

config = {"configurable": {"thread_id": thread_id}}

# --- Step 1: Start workflow ---
print("---- START ----")
text=input("How can i help you? ")
initial_input = {"input": text, "messages": []}

result = graph.invoke(initial_input, config=config)
print(result)

# --- Step 2: HITL loop (pause/resume for human input) ---
while "__interrupt__" in result:
    # Ask user for input
    prompt = result["__interrupt__"][0].value
    user_response = input(f"[HITL] {prompt} ")

    # Update the state with HITL response
    result["confirmation"] = user_response  # important!

    # Resume workflow — MemorySaver automatically uses the same thread_id
    result = graph.invoke(result, config=config)

# --- Step 3: Final workflow result ---
print("\nFinal workflow result:")
print(result)
