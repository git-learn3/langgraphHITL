# app/main2.py
from graph.orch import graph
from langgraph.types import Command
import logging
from typing import Dict, Any

# Setup logging for better debugging
import logging

# Silence noisy libraries
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# OPTIMIZED OUTPUT FORMATTING
def pretty_print_result(state: dict):
    """Format and display workflow results with better structure"""
    tool = state.get("selected_tool")
    
    print("\n" + "="*50)
    print("📊 WORKFLOW RESULT")
    print("="*50)
    
    # Place Order Result
    if tool == "place_order":
        if state.get("confirmation") != "yes":
            print("❌ Order was not placed.")
            return
        
        print("✅ 🛒 ORDER PLACED SUCCESSFULLY")
        print(f"   📦 Product   : {state.get('product')}")
        print(f"   📐 Size      : {state.get('size')}")
        print(f"   🔢 Quantity  : {state.get('quantity')}")
        print(f"   💳 Payment   : Success")
    
    # Track Order Result
    elif tool == "track_order":
        print("✅ 📍 TRACKING INFORMATION")
        print(f"   🆔 Order ID  : {state.get('order_id')}")
        print(f"   📦 Status    : {state.get('order_status')}")
    
    # Cancel Order Result
    elif tool == "cancel_order":
        if state.get("confirmation") != "yes":
            print("❌ Order cancellation aborted.")
            return
        
        print("✅ 🚫 ORDER CANCELLED")
        print(f"   🆔 Order ID  : {state.get('order_id')}")
    
    # Unknown workflow
    else:
        print("⚠️ Unknown workflow executed.")
    
    print("="*50 + "\n")


def validate_input(user_input: str) -> bool:
    """Validate user input before processing"""
    if not user_input or not user_input.strip():
        print("⚠️ Input cannot be empty. Please try again.")
        return False
    if len(user_input) > 500:
        print("⚠️ Input too long (max 500 characters).")
        return False
    return True


def get_user_input(prompt: str, input_type: str = "text") -> Any:
    """Get and validate user input based on type"""
    while True:
        try:
            user_input = input(f"[HITL] {prompt} ").strip()
            
            if input_type == "quantity":
                quantity = int(user_input)
                if quantity <= 0:
                    print("⚠️ Quantity must be greater than 0.")
                    continue
                return quantity
            elif input_type == "confirmation":
                if user_input.lower() in ["yes", "no"]:
                    return user_input.lower()
                print("⚠️ Please enter 'yes' or 'no'.")
                continue
            else:  # text
                if validate_input(user_input):
                    return user_input
        
        except ValueError:
            print(f"⚠️ Invalid input for {input_type}. Please try again.")
        except KeyboardInterrupt:
            print("\n⏸️ Workflow interrupted by user.")
            return None


def execute_workflow(user_input: str, thread_id: str = "demo-1") -> Dict[str, Any]:
    """Execute workflow with HITL support and return final state"""
    
    if not validate_input(user_input):
        return {}
    
    config = {"configurable": {"thread_id": thread_id}}
    initial_input = {"input": user_input, "messages": []}
    
    print(f"\n🔄 Starting workflow (Thread: {thread_id})...")
    print("="*50)
    
    try:
        # Execute initial workflow
        result = graph.invoke(initial_input, config=config)
        logger.info(f"Initial workflow complete. Tool selected: {result.get('selected_tool')}")
        
        # Handle HITL interrupts
        hitl_count = 0
        while "__interrupt__" in result:
            hitl_count += 1
            prompt = result["__interrupt__"][0].value
            
            print(f"\n⏸️ Workflow paused (HITL #{hitl_count})")
            print(f"   Question: {prompt}")
            
            # Determine input type from prompt
            input_type = "quantity" if "quantity" in prompt.lower() else \
                        "confirmation" if "yes" in prompt.lower() or "no" in prompt.lower() else \
                        "product" if "product" in prompt.lower() else "text"
            
            user_response = get_user_input(prompt, input_type)
            
            if user_response is None:
                logger.warning("Workflow interrupted by user")
                return {}
            
            # Update state based on input type
            state_update = {}
            if input_type == "product":
                state_update["product"] = user_response.strip().lower()
            elif input_type == "quantity":
                state_update["quantity"] = user_response
            else:  # confirmation
                state_update["confirmation"] = user_response
            
            # Resume workflow
            print(f"   ✅ Resuming workflow...")
            result = graph.invoke(state_update, config=config)
            logger.info(f"Workflow resumed. HITL #{hitl_count} complete.")
        
        print("\n" + "="*50)
        print("✅ Workflow execution complete!")
        print("="*50)
        
        return result
    
    except Exception as e:
        logger.error(f"Workflow execution failed: {str(e)}")
        print(f"\n❌ Error during workflow: {str(e)}")
        return {}



# MAIN EXECUTION
def main():
    """Main CLI interface"""
    print("\n" + "🛒 "*20)
    print("Welcome to Order Management System (LangGraph HITL)")
    print("🛒 "*20)
    print("\nAvailable commands:")
    print("  - 'I want to buy an iPhone'")
    print("  - 'Where is my order?'")
    print("  - 'Cancel my order'")
    print("  - Or describe what you need!\n")
    
    # Configuration
    thread_id = "demo-1"
    
    while True:
        print("\n" + "-"*50)
        
        try:
            user_input = input("\n📝 Your request: ").strip()
            
            if user_input.lower() == "exit":
                print("\n👋 Thank you for using Order Management System!")
                break
            
            if user_input.lower() == "help":
                print("\nAvailable workflows:")
                print("  📦 place_order: Create a new order")
                print("  🔍 track_order: Track an existing order")
                print("  ❌ cancel_order: Cancel an order")
                continue
            
            # Execute workflow
            result = execute_workflow(user_input, thread_id)
            
            # Display results
            if result:
                pretty_print_result(result)
                
                # Ask if user wants to continue
                continue_choice = input("\n🔄 Continue? (yes/no): ").strip().lower()
                if continue_choice != "yes":
                    break
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            print(f"❌ An unexpected error occurred: {str(e)}")
            print("Please try again or contact support.")


if __name__ == "__main__":
    main()
