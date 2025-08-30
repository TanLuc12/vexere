# 🚍 Vexere AI Assistant

---

## ✨ Tính năng chính

### AI Chatbot thông minh
- **RAG-powered FAQ**: Trả lời câu hỏi thường gặp với độ chính xác cao
- **After-Service Flow**: Hỗ trợ đổi giờ vé tự động
- **Multi-modal**: Xử lý hình ảnh vé và file âm thanh
- **Conversational AI**: Tương tác tự nhiên với người dùng

### 🔧 Công nghệ sử dụng
- **Backend**: FastAPI + Uvicorn
- **AI/ML**: OpenAI GPT-3.5-turbo, LangChain, LangGraph
- **Vector Database**: Postgres
- **UI**: Gradio (Web Interface)
- **Testing**: Pytest

---

## Kiến trúc hệ thống

```
vexere/
├── 📁 data/                    
│   ├── faq_data.csv          
│   └── mock_data.json         
│
├── 📁 src/                     
│   ├── main.py                
│   │
│   ├── 📁 rag/               
│   │   ├── document_loader.py 
│   │   ├── vector_store.py    
│   │   └── pipeline.py        
│   │
│   ├── 📁 service/           
│   │   ├── after_service.py   
│   │   ├── image_service.py   
│   │   └── voice_service.py   
│   │
│   ├── 📁 api/                
│   │   ├── server.py         
│   └── 📁 agent/              
│       └── chatbot.py         
│
├── 📁 tests/                   
│   ├── test_rag.py
│   └── test_after_service.py
│
├── requirements.txt            
├── README.md                  
└── .env                        
```

---

## 🚀 Cài đặt

### 1. Clone repository
```bash
git clone https://github.com/TanLuc12/vexere.git
cd vexere-ai
```

### 2. Tạo môi trường ảo
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu hình environment
Tạo file `.env` trong thư mục gốc:
```env
# Database config
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DATABASE=postgres
POSTGRES_USERNAME=your_username
POSTGRES_PASSWORD=your_password

# OpenAI API
OPENAI_API_KEY=your_openai_api_key


### 5. Chạy ứng dụng
```bash
# Development mode
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000


### 6. Truy cập ứng dụng
- **API Documentation**: http://127.0.0.1:8000/chat
- **Gradio UI**: http://127.0.0.1:8000/gradio


---

## 🧪 Testing

```bash
# Chạy tất cả tests
pytest -v

```
### Gradio Interface
Truy cập http://localhost:8000/gradio 

---




