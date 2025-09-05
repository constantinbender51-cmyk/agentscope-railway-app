import os
import json
from flask import Flask, render_template, request, jsonify
import agentscope
from agentscope.agent import ReActAgent
from agentscope.model import GeminiChatModel
from agentscope.message import Msg
import asyncio
from functools import wraps

app = Flask(__name__)

# Configure AgentScope with Gemini
def init_agentscope():
    """Initialize AgentScope with Gemini model configuration"""
    
    # Model configuration for Gemini 2.5 Flash Lite
    model_config = {
        "config_name": "gemini_flash_lite_config",
        "model_type": "gemini_chat",
        "model_name": "gemini-2.5-flash-lite",
        "api_key": os.getenv("GEMINI_API_KEY"),
        "temperature": 0.7,
        "max_tokens": 1024,
        "stream": True
    }
    
    # Initialize AgentScope
    agentscope.init(
        model_configs=[model_config],
        studio_url=os.getenv("AGENTSCOPE_STUDIO_URL", None)
    )
    
    return model_config

# Initialize the model
model_config = init_agentscope()

# Create a simple ReAct agent
agent = ReActAgent(
    name="Friday",
    sys_prompt="""You are Friday, a helpful AI assistant powered by Gemini 2.5 Flash Lite. 
    You can help users with various tasks including answering questions, providing information, 
    and assisting with problem-solving. Be friendly, concise, and helpful in your responses.""",
    model_config_name="gemini_flash_lite_config"
)

def async_route(f):
    """Decorator to handle async functions in Flask routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return decorated_function

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
@async_route
async def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Create message for the agent
        msg = Msg(name="user", content=user_message, role="user")
        
        # Get response from agent
        response = await agent(msg)
        
        return jsonify({
            'response': response.get_text_content(),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model': 'gemini-2.5-flash-lite',
        'framework': 'AgentScope'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
