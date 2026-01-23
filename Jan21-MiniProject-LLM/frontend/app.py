import gradio as gr
import requests
import uuid
import os

# Configuration
BACKEND_URL = "http://127.0.0.1:8003"

def get_session_id(request: gr.Request):
    # Try to find session_id in headers not really possible with simple Gradio
    # We will generate one per page load or manage via state
    return str(uuid.uuid4())

def extract_text_from_message(message):
    if isinstance(message, str):
        return message
    if isinstance(message, list) and len(message) > 0:
        if isinstance(message[0], dict) and 'text' in message[0]:
            return message[0]['text']
    if isinstance(message, dict) and 'text' in message:
        return message['text']
    return str(message)

def chat_function(message, history, session_id_state):
    # Sanitize message if it comes in as a multimodal list
    message = extract_text_from_message(message)

    if not message:
        return "", session_id_state
    
    if not session_id_state:
        session_id_state = str(uuid.uuid4())

    payload = {
        "message": message
    }
    
    # Ensure session_id is included if valid string
    if session_id_state and isinstance(session_id_state, str) and session_id_state.strip():
        payload["session_id"] = session_id_state
    
    print(f"DEBUG: Sending payload: {payload}, Type of message: {type(message)}, Type of session_id: {type(session_id_state)}")

    try:
        response = requests.post(f"{BACKEND_URL}/chat", json=payload)
        response.raise_for_status()
        data = response.json()
        bot_response = data["response"]
        new_session_id = data["session_id"]
        
        return bot_response, new_session_id
    except Exception as e:
        return f"Error: {str(e)}", session_id_state

# Gradio Interface
with gr.Blocks(title="Pro Chatbot") as demo:
    session_id_state = gr.State(value="")
    
    with gr.Row():
        gr.Markdown("# Context-Aware Chatbot")
        # Display Session ID? Might be complex to bind dynamically to a label properly without events
    
    chatbot = gr.Chatbot(height=500)
    msg = gr.Textbox(placeholder="Type a message...", container=False, scale=7)
    clear = gr.Button("Clear", variant="secondary")

    def user(user_message, history):
        return "", history + [{"role": "user", "content": user_message}]

    def bot(history, session_id):
        user_message = history[-1]["content"]
        bot_response, new_sid = chat_function(user_message, history, session_id)
        history.append({"role": "assistant", "content": bot_response})
        return history, new_sid

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, [chatbot, session_id_state], [chatbot, session_id_state]
    )
    
    # On load logic to set initial session? 
    # Gradio doesn't strictly have "on load" for State in the same way, but State defaults work.

if __name__ == "__main__":
    demo.launch(server_port=7860, share=False, css="frontend/theme.css")
