# app/model.py

from llama_cpp import Llama
from app.config import MODEL_PATH, N_THREADS, N_CTX

# Khởi tạo mô hình Llama
def load_model():
    try:
        llm = Llama(model_path=MODEL_PATH, n_threads=N_THREADS, n_ctx=N_CTX)
        return llm
    except Exception as e:
        raise RuntimeError(f"Không thể tải mô hình: {str(e)}")
