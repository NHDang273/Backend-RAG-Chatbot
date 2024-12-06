from fastapi import FastAPI
from app.database import connect_to_mongo, close_mongo_connection
from app.routers import chat, health

# Khởi tạo ứng dụng FastAPI
app = FastAPI()

# Đăng ký các router
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(health.router, prefix="/api", tags=["Health"])

# Kết nối MongoDB khi server khởi động
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

# Đóng kết nối MongoDB khi server tắt
@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()
