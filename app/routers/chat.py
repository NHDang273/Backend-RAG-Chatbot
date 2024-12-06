from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from app.model import load_model

# Khởi tạo router
router = APIRouter()

# Định nghĩa cấu trúc request
class ChatRequest(BaseModel):
    message: str

# Khởi tạo mô hình
llm = load_model()

# Endpoint để xử lý chatbot
@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Gọi mô hình để tạo phản hồi
        response = llm(
            prompt=request.message,
            max_tokens=128,
            temperature=0.7,
            top_p=0.9,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        # Trả về phản hồi
        return {"response": response["choices"][0]["text"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi xử lý yêu cầu: {str(e)}")
