from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.model import load_model

# Khởi tạo router
router = APIRouter()

# Khởi tạo mô hình
llm = load_model()

# Quản lý kết nối WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

# WebSocket endpoint cho chatbot
@router.websocket("/chat/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Nhận tin nhắn từ client
            data = await websocket.receive_text()
            
            # Gọi mô hình để tạo phản hồi
            try:
                response = llm(
                    prompt=data,
                    max_tokens=128,
                    temperature=0.7,
                    top_p=0.9,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                # Gửi phản hồi lại cho client
                await manager.send_message(response["choices"][0]["text"], websocket)
            except Exception as e:
                await manager.send_message(f"Lỗi khi xử lý yêu cầu: {str(e)}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
