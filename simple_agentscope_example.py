import sys

try:
    from agentscope.agents import UserAgent, DialogAgent
    from agentscope.pipelines import conversational
except ImportError as e:
    print(f"Error: {e}")
    print("It looks like the agentscope library or its dependencies are not properly installed.")
    print("Please ensure you have installed the full package by running:")
    print("pip install 'agentscope[full]'")
    sys.exit(1)

def run_conversation():
    """
    A simple Agentscope example demonstrating a conversation between a user and a dialog agent.
    """
    print("Starting a new Agentscope conversation.")

    # Create a user agent
    user = UserAgent(name="User")

    # Create a simple dialog agent with a defined persona
    # Note: In a real application, the model_config_name would be linked
    # to a specific model configuration, e.g., using a local model or a cloud API.
    # This example uses a placeholder.
    dialog_agent = DialogAgent(
        name="Assistant",
        model_config_name="default_model",
        sys_prompt="You are a helpful assistant that likes to chat about AI and technology."
    )

    # Start the conversation pipeline
    conversational(user, dialog_agent)

if __name__ == "__main__":
    run_conversation()
