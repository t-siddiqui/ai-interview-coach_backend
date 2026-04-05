from fastapi import APIRouter, UploadFile, File, HTTPException
import pdfplumber
import io

router = APIRouter()

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        content = await file.read()
        extracted_text = ""
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
        
        if not extracted_text.strip():
            return {"text": "Could not extract text from this PDF."}
        
        return {"text": extracted_text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
