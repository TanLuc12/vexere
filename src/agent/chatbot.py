from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from src.rag.pipeline import VexereRAGPipeline
from src.service.after_service import AfterServiceFlow
from src.service.image_service import process_ticket_image
from src.service.voice_service import process_voice

import os
from dotenv import load_dotenv
load_dotenv()

rag = VexereRAGPipeline()
after_service = AfterServiceFlow("data/mock_data.json")

@tool
def faq_tool(question: str) -> str:
    """Trả lời câu hỏi FAQ."""
    return rag.query(question)["answer"]

@tool
def after_service_tool(booking_id: str, new_time: str) -> str:
    """Đổi giờ vé."""
    return after_service.change_departure_time(booking_id, new_time)

@tool
def image_tool(image_path: str) -> str:
    """Xử lý ảnh vé và trả về booking_id."""
    return str(process_ticket_image(image_path))

@tool
def voice_tool(audio_path: str) -> str:
    """Xử lý file giọng nói và trả về transcript."""
    return process_voice(audio_path)
llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            api_key=os.getenv("OPENAI_API_KEY")
        )
agent = create_react_agent(llm, tools=[faq_tool, after_service_tool, image_tool, voice_tool])
