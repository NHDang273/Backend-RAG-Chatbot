from fastapi import APIRouter, HTTPException
from database.connection import resume_collection
from services.pdf_processing import extract_text_from_pdf
from services.csv_processing import save_csv_to_mongodb
import os

router = APIRouter()

# API để lấy danh sách tài liệu PDF từ MongoDB
@router.get("/get-pdf-resumes")
async def get_pdf_resumes():
    # Lấy danh sách tất cả các tài liệu PDF từ collection resume
    pdf_documents = list(resume_collection.find({"file_type": "pdf"}))
    
    if not pdf_documents:
        raise HTTPException(status_code=404, detail="No PDF documents found.")
    
    # Trả về danh sách tên các tài liệu PDF
    return {"pdf_documents": pdf_documents}

# API để gửi dữ liệu đã được xử lý từ tài liệu PDF vào MongoDB
@router.post("/process-resumes")
async def process_resumes():
    # Lấy danh sách tài liệu PDF từ MongoDB
    pdf_documents = list(resume_collection.find({"file_type": "pdf"}))
    
    if not pdf_documents:
        raise HTTPException(status_code=404, detail="No PDF documents found.")
    
    # Xử lý từng tài liệu PDF
    for pdf_document in pdf_documents:
        # Lấy đường dẫn tới tài liệu PDF
        pdf_path = os.path.join("app", "data", "pdf_resumes", pdf_document["file_name"])
        
        # Trích xuất văn bản từ tài liệu PDF
        text_content = extract_text_from_pdf(pdf_path)
        
        # Lưu dữ liệu đã xử lý vào MongoDB
        save_csv_to_mongodb(pdf_document["file_name"], text_content)
    
    return {"message": "All PDF resumes have been processed."}

# API để lấy danh sách tài liệu CSV từ MongoDB
@router.get("/get-csv-resumes")
async def get_csv_resumes():
    # Truy vấn dữ liệu từ collection processed_resumes
    csv_documents = list(db["processed_resumes"].find())
    
    if not csv_documents:
        raise HTTPException(status_code=404, detail="No CSV documents found.")
    
    # Chuyển dữ liệu từ MongoDB thành DataFrame và sau đó thành CSV
    df = pd.DataFrame(csv_documents)
    if df.empty:
        raise HTTPException(status_code=404, detail="No valid CSV data found.")
    
    # Chuyển DataFrame thành CSV
    csv_data = df.to_csv(index=False)
    
    # Trả dữ liệu CSV dưới dạng string
    return {"csv_data": csv_data}
