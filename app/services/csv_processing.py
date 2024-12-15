from pymongo import MongoClient

# Kết nối tới MongoDB (thay đổi URI theo môi trường của bạn)
client = MongoClient("mongodb://localhost:27017")
db = client["resume_database"]
processed_resumes_collection = db["processed_resumes"]

def save_csv_to_mongodb(file_name: str, content: str):
    try:
        document = {
            "file_name": file_name,
            "content": content
        }
        processed_resumes_collection.insert_one(document)
    except Exception as e:
        raise Exception(f"Error saving data to MongoDB: {str(e)}")
