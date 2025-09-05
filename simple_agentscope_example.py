# This script demonstrates a basic financial assistant using AgentScope.

import os
from agentscope.agents import UserAgent, AgentBase
from agentscope.pipelines import sequential_pipeline
from agentscope.message import Msg
from agentscope.models import Gemini25FlashLite
from dotenv import load_dotenv

# Load environment variables from a .env file.
# This is a good practice to handle sensitive information like API keys.
load_dotenv()

# The AgentScope documentation can be found at https://doc.agentscope.io/
# The provided example here is based on a conversational agent.

class FinancialAssistantAgent(AgentBase):
    """A financial assistant agent that can answer financial questions."""

    def __init__(self, name: str, model_name: str, api_key: str):
        # Initialize the agent with a name, model, and API key.
        super().__init__(name=name)
        
        # Configure the Gemini 2.5 Flash-Lite model for the agent.
        # This model is lightweight and suitable for conversational tasks.
        self.model = Gemini25FlashLite(
            model_name=model_name,
            api_key=api_key,
            # Setting up a system prompt to define the agent's persona.
            # This is crucial for guiding the model's behavior.
            system_prompt="You are a helpful financial assistant. Provide concise and accurate answers to financial questions. You must always cite your sources.",
        )

    def reply(self, x: Msg = None) -> Msg:
        """The agent's reply function. It processes the user's message and returns a response."""
        
        # We process the user's query and generate a response using the model.
        # AgentScope's `speak` method handles the communication with the model API.
        response = self.model.speak(x)
        
        # We return a message object containing the agent's name and the generated content.
        return Msg(name=self.name, content=response.text, url=response.url)

def run_chat():
    """Sets up and runs a chat loop with the agents."""
    
    # Retrieve the API key from environment variables.
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    # If the API key is not found, we inform the user to set it up.
    if not gemini_api_key:
        print("GEMINI_API_KEY not found. Please set the environment variable.")
        print("You can add it to a .env file or use `railway variable set GEMINI_API_KEY=...`")
        return

    # Initialize the user agent. The user agent handles user input.
    user_agent = UserAgent(name="User")

    # Initialize our custom financial assistant agent.
    financial_agent = FinancialAssistantAgent(
        name="FinancialAssistant",
        model_name="gemini-2.5-flash-preview",
        api_key=gemini_api_key,
    )

    # The sequential_pipeline creates a simple conversational flow.
    # The conversation goes back and forth between the user and the financial assistant.
    pipeline = sequential_pipeline(agents=[user_agent, financial_agent])

    print("Welcome to the financial assistant. Type 'exit' to quit.")
    
    # Run the interactive chat loop.
    pipeline.run()

if __name__ == "__main__":
    run_chat()
