# src/web.py
import gradio as gr
from agent import run_agent
from prompts import SYSTEM_PROMPT
from vector_store import vector_store

vector_store.index_all()

def chat(message, history):
    # history у gradio уже в нужном формате [[user, bot], ...]
    agent_history = []
    for user_msg, bot_msg in history:
        agent_history.append({"role": "user", "content": user_msg})
        agent_history.append({"role": "assistant", "content": bot_msg})
    
    answer = run_agent(message, agent_history, SYSTEM_PROMPT)
    return answer

demo = gr.ChatInterface(
    fn=chat,
    title="🦊 FoxTales AI",
    description="Ассистент по миру FoxTales",
)

demo.launch(server_name="0.0.0.0", server_port=7860)