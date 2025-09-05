# This script demonstrates how to set up a simple agent using AgentScope
# with the Google Gemini 2.5 Flash-Lite model.

# To run this, you must have the required packages installed:
# pip install -r requirements.txt
#
# You also need to set your Google API key as an environment variable:
# export GOOGLE_API_KEY="YOUR_API_KEY"

import agentscope
from agentscope.models import GeminiChatWrapper
from agentscope.agents import DialogAgent, UserAgent
from agentscope.pipelines import SequentialPipeline
import os

# Initialize AgentScope
agentscope.init()

# Check if the GOOGLE_API_KEY environment variable is set
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY environment variable is not set.")
    print("Please set it with your Google API key.")
    exit(1)

# Create a Gemini-powered agent
# Use the GeminiChatWrapper to use the Gemini API
gemini_model = GeminiChatWrapper(
    model_name="gemini-2.5-flash-lite",
    api_key=api_key
)

# Create a DialogAgent that uses the Gemini model
assistant = DialogAgent(
    name="assistant",
    model_config_name=gemini_model,
    sys_prompt="You are a helpful AI assistant."
)

# Create a UserAgent to handle user input
user = UserAgent()

# Create a sequential pipeline to connect the user and the assistant
pipeline = SequentialPipeline([user, assistant])

# Start the chat loop
print("Start chatting with the assistant. Type 'exit' to quit.")
try:
    while True:
        x = pipeline()
        if x.content == "exit":
            break
except KeyboardInterrupt:
    print("\nChat session ended.")
