import os
import asyncio
from agentscope.agent import ReActAgent, UserAgent
from agentscope.model import OpenAIChatModel
from agentscope.memory import InMemoryMemory
from agentscope.tool import Toolkit
from agentscope.message import Msg

# To use this agent, you'll need to set the OPENAI_API_KEY as an environment variable.
# On Railway, you can do this in the "Variables" section of your project settings.
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

# Define the system prompt for our agent.
# The agent will act as a helpful assistant.
sys_prompt = "You are a helpful assistant named Friday."

async def run_conversation():
    """
    Runs a simple conversational loop between a user and an agent.
    """
    # Initialize the model. We'll use OpenAI's gpt-4o-mini as a good starting point.
    # AgentScope is model-agnostic, so you can easily swap this out later.
    model = OpenAIChatModel(
        model_name="gpt-4o-mini",
        api_key=api_key,
    )
    
    # Create the agent. We'll use a ReActAgent, which can reason and use tools if we add them later.
    agent = ReActAgent(
        name="Friday",
        sys_prompt=sys_prompt,
        model=model,
        memory=InMemoryMemory(), # This memory will store the conversation history.
        toolkit=Toolkit(),
    )
    
    # Create the user proxy agent. This is how we interact with our agent.
    user = UserAgent(name="User")
    
    # Start the conversation loop.
    print("Friday: Hello! How can I help you today? (Type 'exit' to end the conversation)")
    
    # Initialize the message to None to start the conversation.
    msg = None
    
    while True:
        # Get a response from the agent.
        response = await agent(msg)
        
        # Check if the user wants to exit.
        if response.content.lower() == "exit":
            print("Friday: Goodbye!")
            break
            
        # Get the user's next message.
        msg = user(response)
        
        if msg.content.lower() == "exit":
            print("Friday: Goodbye!")
            break

if __name__ == "__main__":
    # AgentScope uses an asynchronous event loop.
    asyncio.run(run_conversation())
