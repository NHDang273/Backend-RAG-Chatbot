# app/config.py

import os
from dotenv import load_dotenv

# Load môi trường từ file .env
load_dotenv()

# Đọc thông tin cấu hình từ .env
MODEL_PATH = os.getenv("MODEL_PATH", "path_to_your_model.gguf")
N_THREADS = int(os.getenv("N_THREADS", 8))
N_CTX = int(os.getenv("N_CTX", 2048))
