import os
import csv
from pdfminer.high_level import extract_text
from docx import Document

def extract_text_from_pdf(pdf_path):
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def extract_text_from_doc(doc_path):
    try:
        document = Document(doc_path)
        text = "\n".join([paragraph.text for paragraph in document.paragraphs])
        return text
    except Exception as e:
        print(f"Error extracting text from DOC/DOCX: {e}")
        return ""

def save_text_to_csv(text, csv_path):
    try:

        cleaned_text = text.replace("\n", " ").replace("\r", " ")
        with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Resume"])  
            writer.writerow([cleaned_text])
        print(f"CSV file saved at: {csv_path}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")


def convert_to_csv(file_path, output_csv_path):
    file_extension = os.path.splitext(file_path)[-1].lower()
    if file_extension == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif file_extension in [".doc", ".docx"]:
        text = extract_text_from_doc(file_path)
    else:
        print("Unsupported file format. Only PDF and DOC/DOCX are supported.")
        return
    
    if text:
        save_text_to_csv(text, output_csv_path)

input_file = "CV.pdf"  
output_csv = "output.csv"  
convert_to_csv(input_file, output_csv)
