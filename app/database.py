from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load biến môi trường từ .env
load_dotenv()

# Lấy MONGO_URL từ .env
MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# Khởi tạo client và database
client = None
db = None

async def connect_to_mongo():
    global client, db
    if not MONGO_URL:
        raise RuntimeError("MONGO_URL không được cấu hình!")
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[MONGO_DB_NAME]
    print("Kết nối tới MongoDB Cloud thành công!")

async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("Đã đóng kết nối MongoDB.")
