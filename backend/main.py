from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
import os
from services.pdf_parser import extract_text_from_pdf
app=FastAPI()

@app.post("/upload-resume")
async def upload_resume(
    file:UploadFile=File(...)
):
    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF files are allowed"}
    file_path=f"temp_{file.filename}"
    with open(file_path,"wb") as f:
        file_content=await file.read()
        f.write(file_content)
    extracted_text=extract_text_from_pdf(file_path)
    os.remove(file_path)
    return{
        "filename":file.filename,
        "text":extracted_text
    }