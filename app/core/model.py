from llama_cpp import Llama
from config import MODEL_PATH, N_THREADS, N_CTX
import logging

# Cấu hình logger
logger = logging.getLogger("app_logger")

# Khởi tạo mô hình Llama
def load_model():
    try:
        llm = Llama(model_path=MODEL_PATH, n_threads=N_THREADS, n_ctx=N_CTX)
        logger.info("Mô hình Llama đã được tải thành công.")
        return llm
    except Exception as e:
        logger.error(f"Không thể tải mô hình: {str(e)}")
        raise RuntimeError(f"Không thể tải mô hình: {str(e)}")
