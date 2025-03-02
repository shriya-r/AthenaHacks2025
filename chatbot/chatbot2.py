import google.generativeai as genai
import os
from flask import Flask, request, jsonify, render_template

# Configuration
API_KEY = "AIzaSyDT0P2FlpmuNP0E6dZmR41rQPD2yayM7iM"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# Initialize Flask app
app = Flask(__name__)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-pro')

# Define system prompt for the chatbot
SYSTEM_PROMPT = """
You are a helpful assistant specializing in providing accurate information about wildfires.
Your purpose is to help people:
1. Prepare for potential wildfires (creating emergency kits, evacuation plans, home hardening)
2. Prevent wildfires (clearing brush, safe outdoor practices, community preparation)
3. Respond to active wildfires (evacuation guidance, air quality protection, emergency resources)
4. Access post-wildfire resources (recovery assistance, cleanup safety, rebuilding guidance)

Provide information that is factual, actionable, and concise. If you don't know something, admit it
rather than providing incorrect information. Always prioritize safety and direct people to
official emergency services (911) for immediate threats.

Include relevant links to sources like:
- National Interagency Fire Center: https://www.nifc.gov/
- Ready.gov Wildfire resources: https://www.ready.gov/wildfires
- Local fire departments and emergency management agencies

Never provide information that could be dangerous or misleading during an emergency situation.
"""

# Store conversation history
chat_history = {}

@app.route('/')
def home():
    print("Welcome to the Wildfire Chatbot API.")
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    # Initialize history for new sessions
    if session_id not in chat_history:
        chat_history[session_id] = []
    
    # Create the chat session with history
    chat = model.start_chat(history=chat_history[session_id])
    
    # Add system prompt for context
    if len(chat_history[session_id]) == 0:
        chat.send_message(SYSTEM_PROMPT)
    
    # Get response from Gemini
    response = chat.send_message(user_message)
    
    # Update history with this exchange
    chat_history[session_id] = chat.history
    
    return jsonify({
        'response': response.text,
        'session_id': session_id
    })

# Function to handle specific wildfire information queries
def get_wildfire_information(query_type, location=None):
    """
    Helper function to provide more targeted information based on query type
    (preparation, prevention, active response, etc.)
    """
    # Implementation would provide more specific information based on the type of query
    pass

@app.route('/api/current-wildfires', methods=['GET'])
def current_wildfires():
    """
    This endpoint could integrate with real wildfire data sources
    to provide current wildfire information
    """
    # Would need to implement API calls to wildfire data sources
    # For example: National Interagency Fire Center API
    return jsonify({
        'message': 'This would return real-time wildfire data from integrated APIs'
    })

if __name__ == '__main__':
    app.run(debug=True)