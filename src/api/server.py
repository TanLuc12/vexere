from fastapi import FastAPI
from pydantic import BaseModel
import gradio as gr
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from src.agent.chatbot import agent

app = FastAPI(title="Vexere AI Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    result = agent.invoke({"messages": [("user", req.message)]})
    return {"response": result["messages"][-1].content}

@app.get("/")
def root():
    return RedirectResponse(url="/gradio")

def chat_fn(history, message):
    result = agent.invoke({"messages": [("user", message)]})
    bot_reply = result["messages"][-1].content
    history.append((message, bot_reply))
    return history, ""

with gr.Blocks() as gradio_app:
    gr.Markdown("## Vexere AI Chatbot (FAQ + After-Service)")
    chatbot = gr.Chatbot(height=400)
    msg = gr.Textbox(placeholder="Nhập câu hỏi...")
    clear = gr.Button("Clear")

    state = gr.State([])

    msg.submit(chat_fn, [state, msg], [chatbot, msg])
    clear.click(lambda: ([], ""), None, [chatbot, msg])

app = gr.mount_gradio_app(app, gradio_app, path="/gradio")
