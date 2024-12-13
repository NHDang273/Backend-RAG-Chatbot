from fastapi import FastAPI
from app.routers import chat, health
from app.database.connection import connect_to_mongo, close_mongo_connection
import logging

# Cấu hình logging cho ứng dụng
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("app_logger")

# Khởi tạo ứng dụng FastAPI
app = FastAPI()

# Đăng ký các router
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])  # Chat có hỗ trợ WebSocket

# Kết nối MongoDB khi server khởi động
@app.on_event("startup")
async def startup_event():
    try:
        await connect_to_mongo()
    except Exception as e:
        logger.error(f"Không thể kết nối MongoDB: {e}")
        raise e
    logger.info("MongoDB kết nối thành công")

# Đóng kết nối MongoDB khi server tắt
@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()
    logger.info("Kết nối MongoDB đã được đóng.")
